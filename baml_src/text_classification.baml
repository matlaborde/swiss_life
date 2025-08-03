class Theme {
  title string
  description string
}

class ClassificationResult {
  model_reasoning string
  chosen_theme Theme
}

function TextClassification(text: string, themes: Theme[]) -> ClassificationResult {
  client LlamaNebius
  prompt #"
    {# 
      Prompts are auto-dedented and trimmed.
      We use JINJA for our prompt syntax
      (but we added some static analysis to make sure it's valid!)
    #}

    {{ ctx.output_format(prefix="Classify with the following json:") }}

    You are a helpful assistant that helps classifying texts in given themes
    Available themes:
    {% for theme in themes %}
    - {{ theme.title }}: {{ theme.description }}
    {% endfor %}

    Text: {{ text }}

    Classify this message and provide:
    1. Your reasoning for this classification
    2. The chosen theme, (don't invent theme)

    {{ _.chat('assistant') }}
    JSON response with chosen_theme and model_reasoning:
  "#
}