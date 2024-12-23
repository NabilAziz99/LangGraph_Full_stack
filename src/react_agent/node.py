# node.py

import operator
from pydantic import BaseModel, Field
from typing import List, Optional
from typing_extensions import TypedDict

from langchain_community.document_loaders import WikipediaLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, get_buffer_string
from langchain_openai import ChatOpenAI
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from prompts import (
    process_instructions,
    front_end_instructions,
    back_end_instructions,
    back_end_organization_instructions,
    front_end_organization_instructions,
    front_end_generation_instructions,
    back_end_generation_instructions,
    project_setup_instructions,
    
    
)
from langgraph.constants import Send
from schemas import (
    FunctionalRequirements,
    DeveloperState,
    FrontEndRequirements,
    BackEndRequirements,
    FrontEndDependencies,
    BackEndDependencies,
    CodeOrganization,
    ProjectSetup,
 
)

from langgraph.graph import END, MessagesState, START, StateGraph

llm = ChatOpenAI(model="gpt-4o", temperature=0)

### Function Definitions

def process_requirements(state: DeveloperState):
    """Process requirements"""
    topic = state.topic
    human_developer_feedback = state.human_feedback or ''

    # Enforce structured output
    structured_llm = llm.with_structured_output(FunctionalRequirements)

    # System message
    system_message = process_instructions.format(
        topic=topic,
        human_developer_feedback=human_developer_feedback,
    )

    # Generate requirements
    requirements = structured_llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content="Process the requirements.")
    ])

    # Update the state
    return {"global_requirements": requirements}


def human_feedback_requirements(state: DeveloperState):
    """No-op node that should be interrupted on"""
    human_developer_feedback = state.human_feedback or ''

    return {"human_feedback": human_developer_feedback}
 


def initiate_all_interviews(state: DeveloperState):
    """Conditional edge to initiate all interviews via Send() API or return to process_requirements"""
    human_developer_feedback = state.human_feedback or ''
    if human_developer_feedback != 'approve':
        return "process_requirements"
    else:
        return "front_end_process"


def front_end_process(state: DeveloperState):
    """Define front-end requirements"""
    global_requirements = [req.description for req in state.global_requirements.requirements]
    topic = state.topic

    structured_llm = llm.with_structured_output(FrontEndDependencies)

    system_message = front_end_instructions.format(
        global_requirements=global_requirements,
        topic=topic,
    )

    requirements = structured_llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content="Define the front-end requirements using React.js and any other necessary libraries.")
    ])

    # Update the state
    return {"front_end": requirements}


def back_end_process(state: DeveloperState):
    """Define back-end requirements using Python and FastAPI"""
    # Extract necessary information from the state
    topic = state.topic
    global_requirements = [req.description for req in state.global_requirements.requirements]
    front_end_requirements = state.front_end.requirements.description
    api_design_and_data_structure = state.front_end.requirements.api_design

    # Enforce structured output
    structured_llm = llm.with_structured_output(BackEndDependencies)

    # Format the prompt with the current state information
    system_message = back_end_instructions.format(
        topic=topic,
        global_requirements=global_requirements,
        front_end_requirements=front_end_requirements,
        api_design_and_data_structure=api_design_and_data_structure,
    )

    # Invoke the LLM to generate the back-end requirements
    back_end_requirements = structured_llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content="Define the back-end requirements using Python and FastAPI.")
    ])

    # Update the state with the generated requirements
    return {"back_end": back_end_requirements}


def organize_front_end_code(state: DeveloperState):
    """Organize front-end code based on the requirements."""
    # Extract necessary information from the state
    topic = state.topic
    front_end_requirements = state.front_end.requirements.description
    api_design_and_data_structure_front_end = state.front_end.requirements.api_design
    back_end_requirement_description = state.back_end.requirements.description
    back_end_requirement_end_points = state.back_end.requirements.api_endpoints


    # Prepare the LLM to generate code organization
    structured_llm = llm.with_structured_output(CodeOrganization)

    system_message = front_end_organization_instructions.format(
        topic=topic,
        front_end_requirements=front_end_requirements,
        api_design_and_data_structure_front_end=api_design_and_data_structure_front_end,
        back_end_requirements=back_end_requirement_description,
        back_end_api_endpoints_and_logic=back_end_requirement_end_points,
    )

    # Invoke the LLM to generate code organization
    organized_code = structured_llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content="Process the front-end requirements.")
    ])

    # Return the organized code
    return {"front_end_organization": organized_code}


def organize_back_end_code(state: DeveloperState):
    """Organize back-end code based on the requirements."""
    # Extract necessary information from the state
    topic = state.topic
    back_end_requirements = state.back_end.requirements.description
    back_end_api_endpoints_and_logic = state.back_end.requirements.api_endpoints
    front_end_requirements = state.front_end.requirements.description
    api_design_and_data_structure_front_end = state.front_end.requirements.api_design

    # Locate the endpoint file dynamically
    front_end_endpoint_file = None
    for folder in state.front_end_organization.folders:
        if folder.endpoint_file:
            front_end_endpoint_file = folder.endpoint_file
            break

    if not front_end_endpoint_file:
        raise ValueError("No endpoint file found in front-end organization.")

    # Prepare the LLM to generate code organization
    structured_llm = llm.with_structured_output(CodeOrganization)

    # Prepare the system message using back-end instructions
    system_message = back_end_organization_instructions.format(
        topic=topic,
        front_end_requirements=front_end_requirements,
        api_design_and_data_structure_front_end=api_design_and_data_structure_front_end,
        back_end_requirements=back_end_requirements,
        api_endpoints_and_logic=back_end_api_endpoints_and_logic,
        front_end_endpoint_file=front_end_endpoint_file,  # Use description or relevant info
    )

    # Invoke the LLM to generate the organized back-end code
    organized_code = structured_llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content="Organize the back-end code."),
    ])

    return {"back_end_organization": organized_code}

def generate_front_end_code(state: DeveloperState):
    """Generate front-end code based on the code organization."""
    topic = state.topic
    front_end_organization = state.front_end_organization
    back_end_endpoint_file = None

    # Find the back-end endpoint file
    for folder in state.back_end_organization.folders:
        if folder.endpoint_file:
            back_end_endpoint_file = folder.endpoint_file
            break

    if not back_end_endpoint_file:
        raise ValueError("No endpoint file found in back-end organization.")

    # Prepare the LLM to generate code
    structured_llm = llm.with_structured_output(CodeOrganization)
    # Prepare the system message
    system_message = front_end_generation_instructions.format(
        topic=topic,
        front_end_organization=front_end_organization.folders,
        back_end_endpoint_file=back_end_endpoint_file# Use description or relevant content
    )

    # Invoke the LLM to generate the code
    code_generation = structured_llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content="Please generate the front-end code."),
    ])

    # Update the state with the generated code
    return {"generate_frontend_code": code_generation}


def generate_back_end_code(state: DeveloperState):
    """Generate back-end code based on the code organization."""
    topic = state.topic
    back_end_organization = state.back_end_organization
    front_end_endpoint_file = None

    # Find the front-end endpoint file
    for folder in state.front_end_organization.folders:
        if folder.endpoint_file:
            front_end_endpoint_file = folder.endpoint_file
            break

    if not front_end_endpoint_file:
        raise ValueError("No endpoint file found in front-end organization.")

    # Prepare the LLM to generate code
    structured_llm = llm.with_structured_output(CodeOrganization)

    # Prepare the system message
    system_message = back_end_generation_instructions.format(
        topic=topic,
        back_end_organization=back_end_organization.folders,
        front_end_endpoint_file=front_end_endpoint_file # Use description or relevant content
    )

    # Invoke the LLM to generate the code
    code_generation = structured_llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content="Please generate the back-end code."),
    ])

    # Update the state with the generated code
    return {"generate_backend_code": code_generation}




def required_software(state: DeveloperState):
    """Check for required software"""
    back_end_organization = state.back_end_organization
    front_end_organization = state.front_end_organization
    
    structured_llm = llm.with_structured_output(ProjectSetup)
    system_message = project_setup_instructions.format(
        front_end_organization=front_end_organization,
        back_end_organization=back_end_organization # Use description or relevant content
    )
    setup_instructions = structured_llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content="Please check for required software."),
    ])
    return    {"project_setup_instructions": setup_instructions}
