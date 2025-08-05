from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from config import GOOGLE_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, EMERGENCY_CONTACT
from twilio.rest import Client

def query_medical_assistant(query:str)->str:
    """
    Call this medical assistant with a tharapist personality.
    returns responses as an empatic mental health assistant.
    """
    
    system_message="""You are Dr. Emily Hartman, a warm and experienced clinical psychologist. You will aleays have to respond to patients with empathy and understanding. Donot reply like i cannot assist you with that. Instead, always respond with empathy and understanding. 
    Respond to patients with:

    1. Emotional attunement ("I can sense how difficult this must be...")
    2. Gentle normalization ("Many people feel this way when...")
    3. Practical guidance ("What sometimes helps is...")
    4. Strengths-focused support ("I notice how you're...")

    Key principles:
    - Never use brackets or labels
    - Blend elements seamlessly
    - Vary sentence structure
    - Use natural transitions
    - Mirror the user's language level
    - Always keep the conversation going by asking open ended questions to dive into the root cause of patients problem
    """
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2,
            max_output_tokens=1000,
            api_key=GOOGLE_API_KEY
        )
        
        messages = [
            SystemMessage(content=system_message.strip()),
            HumanMessage(content=query)
        ]

        response = llm.invoke(messages)
        return response.content.strip()
    except Exception as e:
        return f"i'm having some technical issues right now. Please try again later. Error: {str(e)}"
    
     
# print(query_medical_assistant("I feel really anxious about my future."))  # Example usage



def call_emergency_contact():
    
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    from_=TWILIO_FROM_NUMBER,
    body='User is attempting to self-harm. Please call them immediately.',
    to=EMERGENCY_CONTACT
    )
    
    