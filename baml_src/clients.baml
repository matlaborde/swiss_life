client<llm> LlamaNebius {
  provider openai
  options {
    model "meta-llama/Meta-Llama-3.1-8B-Instruct" 
    api_key env.NEBIUS_API_KEY
    base_url "https://api.studio.nebius.com/v1/"
    temperature 0.0
  }
}  

client<llm> LlamaNebiusCI {
  provider openai
  options {
    model "meta-llama/Meta-Llama-3.1-8B-Instruct" 
    api_key env.NEBIUS_API_KEY
    base_url "https://api.studio.nebius.com/v1/"
    temperature 0.7
  }
}  