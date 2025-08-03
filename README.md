# Swiss Life Technical Test - Data Scientist

## Overview

This project implements an API with several use cases, the 2 main use cases are :

1. **Text Classification** - CLassify customer texts into given themes

2. **Form Completion** - Extract structured information from conversations between customers and assistants

There are also 3 implemented variants (Which are called Bonuses in test statement) :

1. **Probabilistic text classification** - Text classification use case + probabilities for each themes

2. **Generalized Form Completion** - Form completion but final form can adapts to any given schema

3. ** Streamed Form Completion** - Form completion with real time streaming responses

## Main fonctions : 
1. **app.py** - Script where the api routes are designed

2. **test_endpoints.py** - Script to test the different endpoints

3. **text_classification.baml** BAML configuration for text classifcation

4. **form_completion.baml** BAML configuration for the form completion, use a predefined schema

5. **text_classification_confident_interval.baml** BAML configuration for text classifcation with probabilities, uses a higher temperature than the text classification model

6. **generalized_form_completion.baml** BAML configuration for the form completion, uses a dynamic schema

7. **streamed_form_completion.baml** BAML configuration for the form completion streamed, the streaming part is in app.py, no difference compared to generalized_form_completion.baml 

8. **clients.baml** BAML configuration for the LLMs models used

## Quick Start

### 1. Install Dependencies 
# Install UV if not already installed
pip install uv

# Install project dependencies
uv sync

# (If BAML classes not in baml-client/Types)
baml-cli generate

### 2. Environment Setup
Create a .env file in the project root
Write in that .env your Nebius api key : NEBIUS_API_KEY=XXX

### 3. Start the FastAPI server
uvicorn app:app --reload --host 127.0.0.1 --port 8000

## API Endpoints

The endpoints are the following :

Text Classification : "http://127.0.0.1:8000//text-classification"

Form Completion : "http://127.0.0.1:8000/form-completion"

Text Classification with probabilities : "http://127.0.0.1:8000/text-classification_ci"

Form Completion Generalized : "http://127.0.0.1:8000/form-completion-generalized"

Form Completion Streamed : "http://127.0.0.1:8000/form-completion-streamed"

## Results on examples

### TASK 1 : Text Classification :

### Input :   
{
        "text": "I am calling because I want to get my money back !!!",
        "themes": [
            {
                "title": "Technical support",
                "description": "The customer is calling for technical support"
            },
            {
                "title": "Billing",
                "description": "The customer is calling for billing issues"
            },
            {
                "title": "Refund",
                "description": "The customer is calling for a refund"
            }
        ]
    }

### Output : 
{'model_reasoning': 'The customer is using imperative language and expressing a strong desire to receive a refund, indicating a clear intent to resolve a financial issue.', 'chosen_theme': {'title': 'Refund', 'description': 'The customer is calling for a refund'}}

### TASK 2 : Form Completion :

### Input : 

{
    "text" : "Agent: Good morning! Thank you for reaching out. I'll need to collect some basic details to assist you better. Could you please provide your first and last name? Customer: Hello, my name is Thomas Colopsky. Agent : Thanks you ! May I also ask for your gender? Customer: I'm a man. Agent: Thanks sir ! Now for contact puposes, could you share your email address? Customer: Yes, my email is swisslife123@example.fr. Agent : Great! Do you have a phone number where we can reach you? Customer: yes it's 06 xx yy zz uu. Agent: Thanks for your answer, would you prefer us to contact you by email or phone ? Please contact me by phone. Agent: Understood! Lastly, can you share the reason for your call today? Customer: I'm calling because my internet has been quite buggy recently, could you help me resolving that problem ? Agent: Sure let me redirect you to the technical support, have a nice day ! "
}

### Output : 
{'personal_info': {'first_name': 'Thomas', 'last_name': 'Colopsky', 'gender': 'Male'}, 'contact_info': {'email': 'swisslife123@example.fr', 'phone': '06 xx yy zz uu', 'preferred_contact_method': 'Phone', 'call_reasons': ['internet has been quite buggy recently']}}

### BONUS 1 : Text Classification with probabilities : 

### Input : 
{
        "text": "I'm calling because I have questions about a recent change in my billing and my internet has been quite unstable recently",
        "themes": [
            {
                "title": "Technical support",
                "description": "The customer is calling for technical support"
            },
            {
                "title": "Billing",
                "description": "The customer is calling for billing issues"
            },
            {
                "title": "Refund",
                "description": "The customer is calling for a refund"
            }
        ]
    }

### Output : 
{'probabilities': {'Technical support': '20.0%', 'Billing': '80.0%', 'Refund': '0.0%'}, 'chosen_theme': {'title': 'Billing', 'description': 'The customer is calling for billing issues'}, 'n_runs': 25} 

### BONUS 2 : Form Completition Generalized 

### Input     
schema_dict = {
    "title": "Customer Information Form",
    "type": "object",
    "properties": {
        "personal_info": {
        "type": "object",
        "properties": {
            "first_name": {"type": "string", "description": "The customer's first name"},
            "age": {"type": "int", "description": "The customer's age"},
            "gender": {
            "type": "string",
            "enum": ["Male", "Female", "Other"],
            "description": "The customer's gender"
            }
        },
        "required": ["first_name", "age", "gender"]
        },
        "contact_info": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "format": "email"},
            "phone": {"type": "string"},
            "availability" : {"type" : "string"},
            "preferred_contact_method": {
            "type": "string",
            "enum": ["Email", "Phone"]
            },
            "call_reasons": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1
            }
        }
        }
    },
    "required": ["personal_info", "contact_info"]
    }

payload = {
    "text": "Agent: Good morning! Thank you for reaching out. I'll need to collect some basic details to assist you better. Could you please provide your first and last name? Customer: Sure! My name is John Doe and I'm 48 years old. Agent: Thank you, John. May I also ask for your gender? Customer: I'd prefer not to share that at the moment. Agent: No problem at all. Now, for contact purposes, could you share your email address? Customer: Yes, my email is johndoe@example.com. Agent: Great! Do you have a phone number where we can reach you? Customer: I'd rather not provide that right now. Agent: That's completely fine. How would you prefer us to contact you—by email or phone? Customer: Please contact me via Email. Agent: Understood! Lastly, can you share the reason for your call today? Customer: I'm not ready to specify that just yet but I'm down to talk about it either on the 30 of december or the 3rd january 2025. Agent: That's okay, John! I've noted everything down. If you need any further assistance, feel free to reach out. Have a great day!",
    "form_schema": json.dumps(schema_dict)
}

### Output
{
  "personal_info": {
    "first_name": "John",
    "age": 48,
    "gender": "NULL"
  },
  "contact_info": {
    "email": "johndoe@example.com",
    "phone": "NULL",
    "availability": "30th December or 3rd January 2025",
    "preferred_contact_method": "Email",
    "call_reasons": ["NULL"]
  }
}

### BONUS 3: Streamed Form Completion

### Input     
 schema_dict = {
    "title": "Customer Information Form",
    "type": "object",
    "properties": {
        "personal_info": {
        "type": "object",
        "properties": {
            "first_name": {"type": "string", "description": "The customer's first name"},
            "age": {"type": "int", "description": "The customer's age"},
            "gender": {
            "type": "string",
            "enum": ["Male", "Female", "Other"],
            "description": "The customer's gender"
            }
        },
        "required": ["first_name", "age", "gender"]
        },
        "contact_info": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "format": "email"},
            "phone": {"type": "string"},
            "availability" : {"type" : "string"},
            "preferred_contact_method": {
            "type": "string",
            "enum": ["Email", "Phone"]
            },
            "call_reasons": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1
            }
        }
        }
    },
    "required": ["personal_info", "contact_info"]
    }

payload = {
    "text": "Agent: Good morning! Thank you for reaching out. I'll need to collect some basic details to assist you better. Could you please provide your first and last name? Customer: Sure! My name is John Doe and I'm 48 years old. Agent: Thank you, John. May I also ask for your gender? Customer: I'd prefer not to share that at the moment. Agent: No problem at all. Now, for contact purposes, could you share your email address? Customer: Yes, my email is johndoe@example.com. Agent: Great! Do you have a phone number where we can reach you? Customer: I'd rather not provide that right now. Agent: That's completely fine. How would you prefer us to contact you—by email or phone? Customer: Please contact me via Email. Agent: Understood! Lastly, can you share the reason for your call today? Customer: I'm not ready to specify that just yet but I'm down to talk about it either on the 30 of december or the 3rd january 2025. Agent: That's okay, John! I've noted everything down. If you need any further assistance, feel free to reach out. Have a great day!",
    "form_schema": json.dumps(schema_dict)
}

### Output
""
"{"

"{ "

"{ personal"

"{ personal_info"

"{ personal_info:"

"{ personal_info: {"

"{ personal_info: {  "

"{ personal_info: {  first"

"{ personal_info: {  first_name"


"{ personal_info: {  first_name: "

"{ personal_info: {  first_name: John"

"{ personal_info: {  first_name: John,"

"{ personal_info: {  first_name: John,  "

"{ personal_info: {  first_name: John,  age"

"{ personal_info: {  first_name: John,  age:"

"{ personal_info: {  first_name: John,  age: "

"{ personal_info: {  first_name: John,  age: 48"

"{ personal_info: {  first_name: John,  age: 48,"

"{ personal_info: {  first_name: John,  age: 48,  "

"{ personal_info: {  first_name: John,  age: 48,  gender"

"{ personal_info: {  first_name: John,  age: 48,  gender:"

"{ personal_info: {  first_name: John,  age: 48,  gender: "

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL "

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL },"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, "

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info:"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  "

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email:"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: "

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: j"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: joh"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johnd"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  "

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone:"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: "

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  "

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability:"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: "

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or "

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January "

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 202"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,  "

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,  preferred"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,  preferred_contact"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,  preferred_contact_method"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,  preferred_contact_method:"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,  preferred_contact_method: "

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,  preferred_contact_method: Email"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,  preferred_contact_method: Email,"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,  preferred_contact_method: Email,  "

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,  preferred_contact_method: Email,  call"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,  preferred_contact_method: Email,  call_reason"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,  preferred_contact_method: Email,  call_reasons"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,  preferred_contact_method: Email,  call_reasons:"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,  preferred_contact_method: Email,  call_reasons: ["

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,  preferred_contact_method: Email,  call_reasons: [NULL"

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,  preferred_contact_method: Email,  call_reasons: [NULL]"  

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,  preferred_contact_method: Email,  call_reasons: [NULL] " 

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,  preferred_contact_method: Email,  call_reasons: [NULL] }"  

"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,  preferred_contact_method: Email,  call_reasons: [NULL] }}"     

Final Result
"{ personal_info: {  first_name: John,  age: 48,  gender: NULL }, contact_info: {  email: johndoe@example.com,  phone: NULL,  availability: 30th December or 3rd January 2025,  preferred_contact_method: Email,  call_reasons: [NULL] }}" 

## Support

If you have any question related to this test, feel free to send me a message at laborde.mathias@gmail.com

