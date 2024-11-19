# graph.py

import operator
from pydantic import BaseModel, Field
from typing import Annotated, List
from typing_extensions import TypedDict

from langchain_community.document_loaders import WikipediaLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, get_buffer_string
from langchain_openai import ChatOpenAI
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from langgraph.constants import Send

from langgraph.graph import END, MessagesState, START, StateGraph
from schemas import DeveloperState
from node import (
    human_feedback,
    initiate_all_interviews,
    process_requirements,
    front_end_process,
    back_end_process,
    organize_front_end_code,
    organize_back_end_code,  # Added this import
    generate_front_end_code,
    generate_back_end_code
)

### Build Interview Graph

# Assuming all necessary imports and node functions are already defined above

# Initialize the StateGraph with DeveloperState
builder = StateGraph(DeveloperState)

# Add existing nodes
builder.add_node("process_requirements", process_requirements)
# builder.add_node("get_human_feedback", human_feedback)  # Commented out as per user instructions
builder.add_node("front_end_process", front_end_process)
builder.add_node("back_end_process", back_end_process)
builder.add_node("organize_front_end_code", organize_front_end_code)
builder.add_node("organize_back_end_code", organize_back_end_code)

# Add the new nodes for code generation
builder.add_node("generate_front_end_code", generate_front_end_code)
builder.add_node("generate_back_end_code", generate_back_end_code)

# Define edges
builder.add_edge(START, "process_requirements")
builder.add_edge("process_requirements", "front_end_process")
builder.add_edge("front_end_process", "back_end_process")
builder.add_edge("back_end_process", "organize_front_end_code")
builder.add_edge("organize_front_end_code", "organize_back_end_code")
builder.add_edge("organize_back_end_code", "generate_front_end_code")
builder.add_edge("generate_front_end_code", "generate_back_end_code")
builder.add_edge("generate_back_end_code", END)

# Compile the graph
graph = builder.compile()