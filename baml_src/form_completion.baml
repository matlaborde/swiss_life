class TextInput {
  text string
}

class PersonalInfo {
  first_name string
  last_name string
  gender string?
}

class ContactInfo {
  email string
  phone string?
  preferred_contact_method string
  call_reasons string[]?
}

class FinalFormInformations {
  personal_info PersonalInfo
  contact_info ContactInfo
}

function ExtractFormData(text: string) -> FinalFormInformations {
  client LlamaNebius
  prompt #"
    Analyze the following conversation between an agent and a customer to extract customer information.
    
    Conversation: {{ text }}
    
    Extract the following information from the conversation and return it in the exact JSON format specified:
    - First name and last name of the customer, assign to first_name the token most likely to be the first name.
    - Gender (if mentioned, otherwise null)
    - Email address
    - Phone number (if mentioned, otherwise null)
    - Preferred contact method (email or phone)
    - Reasons for the call (if mentioned, otherwise null)
    
    Return the data in this exact structure:
    {
      "personal_info": {
        "first_name": "string",
        "last_name": "string", 
        "gender": "Male, Female or Other"
      },
      "contact_info": {
        "email": "string",
        "phone": "string or null",
        "preferred_contact_method": "Email or Phone",
        "call_reasons": "string or null"
      }
    }
    
    {{ "{{ ctx.output_format }}" }}
  "#
}

