from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from state import State 
from langchain_core.messages import HumanMessage, SystemMessage

from prompt import *
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vdb = Chroma(
   embedding_function=embeddings,
   persist_directory="./chroma_db"
    
)

def retriever_agent (state: State) -> str:
    rewritten_query = state.get("rewritten_query")

    retriever = vdb.as_retriever(search_kwargs={"k": 3})
    results = retriever.invoke(rewritten_query)

    return {
        "content": results
    }

def rewritten_query_agent(state: State) -> str:
    user_input = state.get("query")
    chat_history = state.get("messages")

    messages = [
        SystemMessage(content=REWRITE_PROMPT),
        
        HumanMessage(content=query_rewrite_extend(user_input, chat_history))
    ]

    try:
      response = llm.invoke(messages)
      rewritten_query = response.content
      return {
          "rewritten_query": rewritten_query
      }
    except Exception as e:
      print(f"Error in rewritten_query: {e}")
      return None
    

def response_agent(state: State) -> str:
    rewritten_query = state.get("rewritten_query")
    chat_history = state.get("messages")
    content = state.get("content")

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
      
        HumanMessage(content=system_prompt_extend(rewritten_query, chat_history, content))
    ]

    try:
      response = llm.invoke(messages)
      answer = response.content

      return {
          "response": answer }
    except Exception as e:
      print(f"Error in response_agent: {e}")
      return None
