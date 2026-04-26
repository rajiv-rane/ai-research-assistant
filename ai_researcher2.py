# Step1: Define state
from typing_extensions import TypedDict
from typing import Annotated, Literal
from langgraph.graph.message import add_messages
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from dotenv import load_dotenv
import os

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]

# Step2: Define Tools
from arxiv_tool import arxiv_search
from read_pdf import read_pdf
from write_pdf import render_latex_pdf
from langgraph.prebuilt import ToolNode

tools = [arxiv_search, read_pdf, render_latex_pdf]
tool_node = ToolNode(tools)

# Step3: Setup LLM
from langchain_google_genai import ChatGoogleGenerativeAI, HarmCategory, HarmBlockThreshold

model = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    api_key=os.getenv("GOOGLE_API_KEY"),
    max_retries=1,
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
).bind_tools(tools)

# Step4: Setup graph
from langgraph.graph import END, START, StateGraph

def call_model(state: State):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}

def should_continue(state: State) -> Literal["tools", END]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow = StateGraph(State)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

from langgraph.checkpoint.memory import MemorySaver
checkpointer = MemorySaver()
# Fresh thread ID to avoid any 'poisoned' history from previous empty responses
config = {"configurable": {"thread_id": "fresh_start_v5"}}

graph = workflow.compile(checkpointer=checkpointer)

# INITIAL PROMPT (CLEANED OF SAFETY TRIGGERS)
INITIAL_PROMPT = """
You are an expert researcher in high-level academic fields. 
Goal: Analyze recent research papers to identify new directions and write original research papers. 
Tool Use: ALWAYS use arxiv.org via the provided tools to search and read papers.
Process:
1. Discuss a topic with the user.
2. Search and present recent papers.
3. Read the selected paper in depth.
4. Propose future research ideas.
5. Write the final paper with mathematical equations and render as a LaTeX PDF.
Always provide PDF links for paper references."""

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if hasattr(message, 'content') and message.content:
            print("-" * 20)
            if message.type == "human":
                print(f"User: {message.content}")
            elif message.type == "ai":
                print(f"AI: {message.content}")
            elif message.type == "tool":
                print(f"Tool Result (Excerpt): {message.content[:300]}...")
            print("-" * 20)

# EXECUTION LOOP
first_message = True
while True:
    user_input = input("User: ")
    if user_input:
        if first_message:
            # Combine combined for first turn to fix role alternating
            messages = [HumanMessage(content=f"{INITIAL_PROMPT}\n\nMy research topic is: {user_input}")]
            first_message = False
        else:
            messages = [HumanMessage(content=user_input)]
            
        input_data = {"messages": messages}
        print_stream(graph.stream(input_data, config, stream_mode="values"))