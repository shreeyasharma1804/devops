from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os
import langchain
langchain.verbose = False
langchain.debug = False
langchain.llm_cache = False

load_dotenv()

user_query = input("Enter your query: ")  # Read /Users/shreeya/.zshrc
user_query = user_query.strip()

llm = ChatGoogleGenerativeAI(
    model="gemini-pro-latest",
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    max_tokens=None,
    timeout=None,
)

template = f'''
                            You are an LLM Agent connected to FastMCP. The tools available and its usage are: "ReadFileUsingLLM".
                            Precisely, the tool name is "ReadFileUsingLLM" and its description is: 
                            
                            "Read a file using LLM.

                            Args:
                                path (str): The path to the file to be read. Provide the full path

                            Returns:
                                str: The contents of the file."
                                
                            The user query is: {user_query}
                            
                            Your role is to provide the input arguments to call the above tool.
                            You need to provide precise single work answers for the next queries based on this context.
                            PROVIDE SINGLE WORD PRECISE ANSWERS ONLY SINCE THESE WILL BE DIRECTLY USED AS TOOL INPUT ARGUMENTS.
                        '''

question = "What is the tool which has to be used here"

messages = [
    SystemMessage(content=template),
    HumanMessage(content=question)]
response = llm.invoke(messages)
print(response.content)

question = "What is the file location which has to be read here"

messages = [
    SystemMessage(content=template),
    HumanMessage(content=question)]
response = llm.invoke(messages)
print(response.content)
