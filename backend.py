#  BackEnd.py

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
import sqlite3
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
import requests

#Load env variables
load_dotenv()

#-------------
#Create a LLm
#-------------
llm = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash',
    temperature = 0
)

#-------------
#2.Tools
#-------------
search_tool = DuckDuckGoSearchRun(region="us-en")

@tool
def calculator(first_num: float, second_num: float,operation: str) -> dict:
    """
    Perform a basic arithmetic operation on two numbers.
    supported operation: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}
        
        return {
            "first_num": first_num,
            "second_num": second_num,
            "operation": operation,
            "result": result
        }

    except Exception as e:
        return {"error": str(e)}
    
@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=BZCUFPUJ9RAVFBCK"
    r = requests.get (url)
    return r. json()

#-------------
# Making tool container
#-------------
tools = [search_tool, get_stock_price, calculator]
# LLM WITH TOOLS
llm_with_tools = llm.bind_tools(tools)

#-------------
#3. Create a State
#-------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

#-------------
#4. Create Node Functions
#-------------
def chat_node(state: ChatState):
    #take user query from state
    messages = state['messages']
    #send it to llm
    response = llm_with_tools.invoke(messages)
    #store response in state
    return {'messages':[response]}

tool_node = ToolNode(tools)

#-------------
#5. Making SQl database
#-------------
conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)

#-------------
#5. CheckPointer
#-------------
checkpointer = SqliteSaver(conn=conn)

#-------------
#6. HELPER -- It will give you all the stored checkpoints
#-------------
def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None) :
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)

#-------------
#7. Create Graph
#-------------
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

#add EDGES to graph
graph.add_edge(START,'chat_node')

graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools","chat_node")

#compile the graph
chatbot = graph.compile(checkpointer=checkpointer)

