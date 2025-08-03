import json
import requests

#Test text classification endpoint
def test_text_classification():
    payload = {
        "text": "I am calling because I have a problem with my internet connection",
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

    payload = {
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

    response = requests.post('http://127.0.0.1:8000/text-classification', json=payload)
    return response.json()

#Test form completion endpoint
def test_form_completion():
    payload = {
        "text": "Agent: Good morning! Thank you for reaching out. I'll need to collect some basic details to assist you better. Could you please provide your first and last name? Customer: Sure! My name is John Doe. Agent: Thank you, John. May I also ask for your gender? Customer: I'd prefer not to share that at the moment. Agent: No problem at all. Now, for contact purposes, could you share your email address? Customer: Yes, my email is johndoe@example.com. Agent: Great! Do you have a phone number where we can reach you? Customer: I'd rather not provide that right now. Agent: That's completely fine. How would you prefer us to contact you—by email or phone? Customer: Please contact me via Email. Agent: Understood! Lastly, can you share the reason for your call today? Customer: I'm not ready to specify that just yet. Agent: That's okay, John! I've noted everything down. If you need any further assistance, feel free to reach out. Have a great day!"
    }
    
    payload = {
        "text" : "Agent: Good morning! Thank you for reaching out. I'll need to collect some basic details to assist you better. Could you please provide your first and last name? Customer: Hello, my name is Thomas Colopsky. Agent : Thanks you ! May I also ask for your gender? Customer: I'm a man. Agent: Thanks sir ! Now for contact puposes, could you share your email address? Customer: Yes, my email is swisslife123@example.fr. Agent : Great! Do you have a phone number where we can reach you? Customer: yes it's 06 xx yy zz uu. Agent: Thanks for your answer, would you prefer us to contact you by email or phone ? Please contact me by phone. Agent: Understood! Lastly, can you share the reason for your call today? Customer: I'm calling because my internet has been quite buggy recently, could you help me resolving that problem ? Agent: Sure let me redirect you to the technical support, have a nice day ! "
    }
    response = requests.post('http://127.0.0.1:8000/form-completion', json=payload)
    return response.json()

#Test text classification endpoint with probabilities
def test_text_classification_with_probas():

    #Number of runs for the test, /!\ the more runs, the more time it takes to run the test + the more requests are made to the model (which is not free)
    n_run_test = 25

    payload = {
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

    response = requests.post(f'http://127.0.0.1:8000/text-classification_ci?n_runs={n_run_test}', json=payload)
    return response.json()

#Test generalized form completion endpoint
def test_generalized_form_completion():

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
    
    response = requests.post('http://127.0.0.1:8000/form-completion-generalized', json=payload)
    return response.json()

#Test streamed form completion endpoint
def test_streamed_form_completion():

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
    
    #Since we are streaming the results, we are iterating over the lines and printing the results
    with requests.post('http://127.0.0.1:8000/form-completion-streamed', json=payload, stream=True) as r:
        for line in r.iter_lines():
            if line:
                try:
                    print('\n', 'BONUS 3 : ', '\n')
                    parsed = json.loads(line.decode())
                    print("Partial Results")
                    for partial in parsed["partials"]:
                        print(json.dumps(partial))
                        print('\n')  

                    print("Final Result")
                    print(json.dumps(parsed["final"]))

                except Exception as e:
                    print('error :', e)
    
if __name__ == "__main__":
   
    classified_text_json = test_text_classification()
    print("TASK 1 : ", classified_text_json, '\n')
    
    form_json = test_form_completion()
    print("TASK 2 : ", form_json, '\n')

    classified_text_json_with_probas = test_text_classification_with_probas()
    print("BONUS 1 : ", classified_text_json_with_probas, '\n')

    generalized_form_json = test_generalized_form_completion()
    print("BONUS 2 : ", generalized_form_json)

    streamed_form_json = test_streamed_form_completion()
