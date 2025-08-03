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


class TextClassificationInput(BaseModel):
    text: str
    themes: list[Theme] = [
        Theme(title="Technical support", description="The customer is calling for technical support"),
        Theme(title="Billing", description="The customer is calling for billing issues"),
        Theme(title="Refund", description="The customer is calling for a refund"),
    ]


class FormCompletionInput(BaseModel):
    text: str

class FormCompletionInputGen(BaseModel):
    text: str
    form_schema: str

class FormCompletionInputStreamed(BaseModel):
    text: str
    form_schema: str

@app.get("/")
async def root():
    return {"Welcome to Swiss Life technical test API"}

@app.post("/text-classification")
async def text_classification(payload: TextClassificationInput):
    try:
        baml_themes = [Theme(title=t.title, description=t.description) for t in payload.themes]

        result: ClassificationResult = b.TextClassification(
            text=payload.text,
            themes=baml_themes
        )

        return result

    except Exception as e:
        return {"error": str(e)}

@app.post("/form-completion")
async def form_completion(payload: FormCompletionInput):
    try:
        result: FinalFormInformations = b.ExtractFormData(
            text=payload.text
        )

        return result

    except Exception as e:
        return {"error": str(e)}

@app.post("/text-classification_ci")
async def text_classification_ci(payload: TextClassificationInput, n_runs:int=10):
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

@app.post("/form-completion-generalized")
async def form_completion_generalized(payload: FormCompletionInputGen):
    try:

        schema=json.dumps(payload.form_schema)

        input_obj = TextInputGen(text=payload.text, form_schema=schema)
        result: FinalFormInformations = b.ExtractFormDataGen(input_obj)

        return result

    except Exception as e:
        return {"error": str(e)}

@app.post("/form-completion-streamed")
async def form_completion_streamed(payload: FormCompletionInputStreamed):
    try:
        schema = json.dumps(payload.form_schema)
        input_obj = TextInputGen(text=payload.text, form_schema=schema)
        result_stream = b.stream.ExtractFormDataStreamed(input_obj)

        list_partials = []
        for partial in result_stream:
            cleaned = partial.replace("\\n", "").replace("\n", "").replace("\r", "").replace("\\", "").replace("\"", "").replace("  ", " ")
            if cleaned not in list_partials:
                list_partials.append(cleaned)
        
        final = result_stream.get_final_response()
        final_cleaned = final.replace("\\n", "").replace("\n", "").replace("\r", "").replace("\\", "").replace("\"", "").replace("  ", " ")
        return {
            "partials": list_partials,
            "final": final_cleaned
        }

    except Exception as e:
        return {"error": str(e)}