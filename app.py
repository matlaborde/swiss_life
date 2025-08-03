from fastapi import FastAPI
import os
import json
from baml_client import b
from baml_client.types import ClassificationResult, Theme, TextInput, FinalFormInformations, TextInputGen  
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

#Input for text classification model
class TextClassificationInput(BaseModel):
    text: str
    themes: list[Theme] = [
        Theme(title="Technical support", description="The customer is calling for technical support"),
        Theme(title="Billing", description="The customer is calling for billing issues"),
        Theme(title="Refund", description="The customer is calling for a refund"),
    ]

#Input for form completion model
class FormCompletionInput(BaseModel):
    text: str

#Input for form completion model with schema
class FormCompletionInputGen(BaseModel):
    text: str
    form_schema: str

#Input for form completion model with schema streamed
class FormCompletionInputStreamed(BaseModel):
    text: str
    form_schema: str

#Root endpoint
@app.get("/")
async def root():
    return {"Welcome to Swiss Life technical test API"}

#Text classification endpoint
@app.post("/text-classification")
async def text_classification(payload: TextClassificationInput):
    #Input : a text and a list of themes
    #Output : the theme that is the most likely to be the one the customer is calling for
    try:
        baml_themes = [Theme(title=t.title, description=t.description) for t in payload.themes]

        result: ClassificationResult = b.TextClassification(
            text=payload.text,
            themes=baml_themes
        )

        return result

    except Exception as e:
        return {"error": str(e)}

#Form completion endpoint
@app.post("/form-completion")
async def form_completion(payload: FormCompletionInput):
    #Input : a text
    #Output : a dictionary of the form data
    try:
        result: FinalFormInformations = b.ExtractFormData(
            text=payload.text
        )

        return result

    except Exception as e:
        return {"error": str(e)}

#Text classification endpoint with probabilities
@app.post("/text-classification_ci")
async def text_classification_ci(payload: TextClassificationInput, n_runs:int=10):
    #Input : a text and a list of themes
    #Output : the theme that is the most likely to be the one the customer is calling for + the probabilities of each theme
    try:
        baml_themes = [Theme(title=t.title, description=t.description) for t in payload.themes]

        theme_counts = {t.title: 0 for t in payload.themes}
        results = []

        for _ in range(n_runs):
            result: ClassificationResult = b.TextClassification_ci(
                text=payload.text,
                themes=baml_themes
            )
            theme_title = result.chosen_theme.title
            theme_counts[theme_title] += 1
            results.append(result)

        theme_probs = {
            title: f"{(count / n_runs) * 100:.1f}%" for title, count in theme_counts.items()
        }

        final_theme = max(theme_counts, key=theme_counts.get)
        final_theme_obj = next(t for t in baml_themes if t.title == final_theme)

        return {
            "probabilities": theme_probs,
            "chosen_theme": final_theme_obj,
            "n_runs": n_runs
        }

    except Exception as e:
        return {"error": str(e)}

#Form completion endpoint with schema
@app.post("/form-completion-generalized")
async def form_completion_generalized(payload: FormCompletionInputGen):
    #Input : a text and a schema
    #Output : a dictionary of the form completed, based on the schema provided
    try:
        schema=json.dumps(payload.form_schema)

        input_obj = TextInputGen(text=payload.text, form_schema=schema)
        result: FinalFormInformations = b.ExtractFormDataGen(input_obj)

        return result

    except Exception as e:
        return {"error": str(e)}

#Form completion endpoint with schema streamed
@app.post("/form-completion-streamed")
async def form_completion_streamed(payload: FormCompletionInputStreamed):
    #Input : a text and a schema
    #Output : all partial results from streaming, and a final result which is a dictionary of the form completed, based on the schema provided
    try:
        schema = json.dumps(payload.form_schema)
        input_obj = TextInputGen(text=payload.text, form_schema=schema)
        result_stream = b.stream.ExtractFormDataStreamed(input_obj)

        list_partials = []
        for partial in result_stream:
            #a way to clean the partial results, not the cleanest way but it works
            cleaned = partial.replace("\\n", "").replace("\n", "").replace("\r", "").replace("\\", "").replace("\"", "").replace("  ", " ")
            if cleaned not in list_partials:
                list_partials.append(cleaned)
        
        final = result_stream.get_final_response()
        #a way to clean the final results, not the cleanest way but it works
        final_cleaned = final.replace("\\n", "").replace("\n", "").replace("\r", "").replace("\\", "").replace("\"", "").replace("  ", " ")
        return {
            "partials": list_partials,
            "final": final_cleaned
        }

    except Exception as e:
        return {"error": str(e)}