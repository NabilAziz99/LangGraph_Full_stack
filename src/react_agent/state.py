from langchain_openai import ChatOpenAI

def is_palindrome(s: str) -> bool:
    """
    check if a string is a palindrome
    Args:
        s: first string
    """
    s = s.replace(" ", "").lower()
    return s == s[::-1]

def reverse_string(s:str):
     """
    Reverse the string
    Args:
        s: first string
     """
     return s[::-1]
    
    
    
    
    




llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools([is_palindrome, reverse_string])









from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

# Node
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([is_palindrome,reverse_string]))
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", END)
graph = builder.compile()

from langchain_core.messages import HumanMessage
messages = [HumanMessage(content="Is this civyic a palindrome? then take it and reverse it")]
messages = graph.invoke({"messages": messages})
for m in messages['messages']:
    m.pretty_print()