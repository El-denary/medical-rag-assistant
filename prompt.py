REWRITE_PROMPT = """You are a query rewriting assistant. Your task is to rewrite the user's query to make it more effective for information retrieval.

Guidelines:
Preserve the original intent of the query
Make the query more specific and detailed
Use natural language and complete sentences

"""


def query_rewrite_extend(user_input: str, chat_history: list) -> str:
    """
    Extend the query rewriting prompt with user input and chat history.
    """
    # Convert chat history list to string format
    chat_history_str = ""
    if chat_history:
        for msg in chat_history:
            if hasattr(msg, 'content'):
                chat_history_str += f"{msg.content}\n"
            else:
                chat_history_str += f"{str(msg)}\n"

    prompt = f"""
User Query: {user_input}

Chat History:
{chat_history_str}

Rewritten Query:
    """
    return prompt

SYSTEM_PROMPT = """
Answer concisely in 2-4 sentences. Only expand if the question truly requires detail.
"""

def system_prompt_extend(user_input: str, chat_history: str, content: str) -> str:
    """
    Extend the system prompt with user input, chat history, and content.
    """
    prompt = f"""
User Query: {user_input}

Chat History:
{chat_history}

Content:
{content}

Please provide a helpful response based on the above information.
    """
    return prompt