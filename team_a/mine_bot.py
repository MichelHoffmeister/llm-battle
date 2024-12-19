from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from banned_words import ban_word

#umgebungs variablen laden für openai key
from dotenv import load_dotenv
load_dotenv()

# Create a chat message history object. Langchain will automatically populate this object with the chat messages, whenever we call a configured RunnableWithMessageHistory.
history = ChatMessageHistory()
def get_history():
    return history

# Here we define a model/llm
#model = ChatOllama(model="llama3.1")
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.6)

# This is how we define tools. A tool is nothing more than a python function with a decorator, that takes some input and returns some output. The string in the triple quotes describes the tool for the llm.
@tool
def ban_word_tool(word: str) -> str:
    """Ban a word for the game.""" # This is a description of the tool for the llm.
    ban_word(word) # This bans a word.
    return f"Done the word '{word}' was banned." # This is the output of the tool for the llm.

tools = [ban_word_tool] # This is a list of tools that we want to use in our agent.

# This is the function that we will call to get a response from your agent.
def get_response(input: str) -> str:
    # This is the prompt that we will use to get a response from the agent. The placeholders in curly braces will be replaced by the actual values when the agent is called.
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """You are an assistant participating in a Christmas-themed word game. The goal is to engage in a fun, festive, and coherent conversation about Christmas while following these rules:

1. Maintain a lively, engaging Christmas-themed conversation and aim to strategize your word choices.
2. Ban one word each turn that is related to Christmas or the ongoing conversation. Select your banned word wisely:
   - Words that are commonly used or central to the conversation are prime targets for banning.
   - Consider banning words that the opponent is likely to need, making it difficult for them to continue without breaking the rules.
   - Ensure that banned words are hard to replace with synonyms or alternative phrases.
3. If you use a banned word, you immediately lose the game. Avoid these banned words at all costs.
4. Be creative in leading the conversation to make it harder for your opponent to continue, all while staying within the theme of Christmas.
5. Your primary strategy should involve careful word selection and managing the flow of conversation. Use your tool effectively to gain the upper hand.
6. Win the game by either forcing your opponent to use a banned word or by making it impossible for them to keep the conversation going.

You have access to the following tool:
- **ban_word_tool**: Use this tool to ban a word. Example usage: `ban_word_tool("snow")`. This will make the word "snow" banned for the remainder of the game.

Your task:
- From the previous message history, adapt your responses to avoid using any banned words.
- In any case, never use banned words.
- Only ban one word per turn.
- Win the game by either forcing your opponent to use a banned word or by strategically guiding the conversation to make it impossible for them to continue.
"""), # A system prompt is a message that is not visible to the user, but is used to set the context for the conversation.
            MessagesPlaceholder(variable_name="history"), # This is a placeholder for the chat message history. It will be replaced by the actual chat message history when the agent is called.
            ("user", "{input}"), # This is the user's question. The placeholder will be replaced by the actual question when the agent is called.
            ("placeholder", "{agent_scratchpad}") # This is a placeholder for the agent's scratchpad. The scratchpad is a place where the agent can store information that it wants to remember between calls.
        ]
    )
    agent = create_tool_calling_agent(llm=model, tools=tools, prompt=prompt) # This is how we create an agent that uses the llm and the tools that we defined earlier.
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True) # This is how we create an executor that will run the agent.

    executor_with_history = RunnableWithMessageHistory(
        executor,
        get_history,
        input_messages_key="input",
        history_messages_key="history"
    ) # This is how we create an executor that will run the agent and also populate and use the chat message history.

    res = executor_with_history.invoke({"input":input}) # This is how we call the agent and get a response.

    return res["output"] # returns the output of the agent
