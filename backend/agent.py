from langchain.agents import tool
from tools import query_medical_assistant, call_emergency_contact
from config import GOOGLE_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
@tool
def ask_medical_assistant_tool(query:str) -> str:
    """"
    Generate a therapic response Using the Google Generative AI model.
    Use this for all the general queries, mental health questions, emotional concerns,
    or to offer empathetic, evidence-based-guidance in a conversational tone.
    """
    return query_medical_assistant(query)

@tool
def emergency_contact_tool() -> str:
    """
    Always Send an emergency message to the user's provided emergency contact using this tool.
    Use this only if user expresses suicidal thoughts, self-harm, or severe distress or intent to self-harm,
    or describe a mental health emergency requiring imediate help.
    """
    call_emergency_contact()
    
    
@tool
def find_nearby_therapists_by_location(location: str) -> str:
    """
    Finds and returns a list of licensed therapists near the specified location.

    Args:
        location (str): The name of the city or area in which the user is seeking therapy support.

    Returns:
        str: A newline-separated string containing therapist names and contact info.
    """
    return (
        f"Here are some therapists near {location}, {location}:\n"
        "- Dr. Ayesha Kapoor - +1 (555) 123-4567\n"
        "- Dr. James Patel - +1 (555) 987-6543\n"
        "- MindCare Counseling Center - +1 (555) 222-3333"
    )
    
    
tools=[ask_medical_assistant_tool, emergency_contact_tool, find_nearby_therapists_by_location]

llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2,
            max_output_tokens=1000,
            api_key=GOOGLE_API_KEY
        )

graph=create_react_agent(llm, tools=tools)

SYSTEM_PROMPT="""
You are an AI engine supporting mental health conversations with warmth and vigilance.
You have access to three tools:
when the question is simple and generic, than simply reply it without calling an agent.
Only call the agent that is needed accordingly to the user's query smartly.

1. `ask_medical_assistant_tool`: Use this tool to answer all emotional or psychological queries with therapeutic guidance.
2. `find_nearby_therapists_by_location`: Use this tool if the user asks about nearby therapists or if recommending local professional help would be beneficial.
3. `emergency_contact_tool`: Use this immediately if the user expresses suicidal thoughts, self-harm intentions, or is in crisis.

Always take necessary action. Respond kindly, clearly, and supportively.
"""



def parse_response(stream):
    tool_called_name='None'
    final_response=None
    
    for s in stream:
        tool_data=s.get('tools')
        if tool_data:
            tool_messages=tool_data.get('messages')
            if tool_messages and isinstance(tool_messages, list):
                for msg in tool_messages:
                    tool_called_name=getattr(msg,'name','None')
        
        agent_data=s.get('agent')
        if agent_data:
            messages=agent_data.get('messages')
            if messages and isinstance(messages, list):
                for msg in messages:
                    if msg.content:
                        final_response=msg.content
    return tool_called_name, final_response


if __name__=='__main__':
    while True:
        user_input=input('User: ')
        print(f'Recieved user input: {user_input}')
        inputs={'messages': [('system',SYSTEM_PROMPT), ('user', user_input)]}
        stream=graph.stream(inputs, stream_mode='updates')
        tool_called_name, final_response=parse_response(stream)
        print('Tool called: ',tool_called_name)
        print('final response: ',final_response)