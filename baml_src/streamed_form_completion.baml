class TextInputStreamed {
  text string
  form_schema string
}

function ExtractFormDataStreamed(input: TextInputStreamed) -> string {
  client LlamaNebius
  prompt #"
    Analyze the following conversation between an agent and a customer to extract customer information.
    
    Conversation: {{input.text}}
    
    Based on the schema below, extract the relevant fields and fill the values accordingly. If you can't find the information, set it up to NULL value

    Schema: {{input.form_schema}}

    Don't add any explanation. 

    {{ "{{ ctx.output_format }}" }}
  "#
}

