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
    human_feedback_requirements,
    initiate_all_interviews,
    process_requirements,
    front_end_process,
    back_end_process,
    organize_front_end_code,
    organize_back_end_code , # Added this import
    generate_front_end_code,
    generate_back_end_code,
    required_software,
)

### Build Interview Graph

builder = StateGraph(DeveloperState)
builder.add_node("process_requirements", process_requirements)

# Rename the node from 'human_feedback' to 'get_human_feedback'
builder.add_node("human_feedback_requirements", human_feedback_requirements)

builder.add_node("front_end_process", front_end_process)
builder.add_node("back_end_process", back_end_process)

builder.add_node("organize_front_end_code", organize_front_end_code)
builder.add_node("organize_back_end_code", organize_back_end_code)  # Added this node
builder.add_node("generate_front_end_code", generate_front_end_code)
builder.add_node("generate_back_end_code", generate_back_end_code)  # Added this node
builder.add_node("required_software", required_software)  # Added this node

builder.add_edge(START, "process_requirements")





builder.add_edge("process_requirements", "human_feedback_requirements")

# Update the node name in conditional edges
builder.add_conditional_edges(
    "human_feedback_requirements",
    initiate_all_interviews,
    ["process_requirements", "front_end_process"]
)

builder.add_edge("front_end_process", "back_end_process")
builder.add_edge("back_end_process", "organize_front_end_code")
builder.add_edge("organize_front_end_code", "organize_back_end_code")  # Added this edge
builder.add_edge("organize_back_end_code", "generate_front_end_code")  # Connect to END
builder.add_edge("generate_front_end_code", "generate_back_end_code")  # Connect to END
builder.add_edge("generate_back_end_code", "required_software")  # Connect to END
builder.add_edge("required_software", END)  # Connect to END


# Update the interrupt_before list
#graph = builder.compile(interrupt_before=['human_feedback_requirements'])
graph = builder.compile()