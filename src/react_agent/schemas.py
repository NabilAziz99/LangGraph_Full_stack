# schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional
from typing_extensions import TypedDict

# Requirement Models

class Requirement(BaseModel):
    """
    Represents a functional requirement with suggestions, presumptions, and questions.

    Attributes:
        description (str): Bullet point description of the functional requirement.
        suggestions (str): Bullet point of suggestions related to the functional requirement.
        presumptions (str): List of presumptions related to the functional requirement.
        questions (List[str]): List of questions related to the functional requirement.
    """
    description: str = Field(
        description="Bullet point description of the functional requirement.",
    )
    suggestions: str = Field(
        description="Bullet point of suggestions related to the functional requirement.",
    )
    presumptions: str = Field(
        description="List of presumptions related to the functional requirement.",
    )
    questions: List[str] = Field(
        description="List of questions related to the functional requirement.",
    )

    @property
    def summary(self) -> str:
        return (
            f"Description: {self.description}\n"
            f"Suggestions: {self.suggestions}\n"
            f"Presumptions: {self.presumptions}\n"
            f"Questions: {', '.join(self.questions)}\n"
        )

class FunctionalRequirements(BaseModel):
    """
    Represents the comprehensive list of functional requirements.

    Attributes:
        requirements (List[Requirement]): List of functional requirements.
    """
    requirements: List[Requirement] = Field(
        description="List of functional requirements with suggestions, presumptions, and questions.",
    )

    @property
    def summary(self) -> str:
        summaries = [req.summary for req in self.requirements]
        return "\n".join(summaries)

# Framework Models

class RequiredFramework(BaseModel):
    """
    Represents an additional framework or library needed to implement the application.

    Attributes:
        name (str): The name of the framework or library.
        description (str): A description of how the framework or library will be used.
    """
    name: str = Field(
        description="The name of the framework or library.",
    )
    description: str = Field(
        description="A description of how the framework or library will be used.",
    )

# Front-End Models

class FrontEndRequirements(BaseModel):
    """
    Represents the front-end requirement information.

    Attributes:
        description (str): Description of the front-end requirements.
        api_design (str): Key API endpoints, data models, parameters, and response formats.
    """
    description: str = Field(
        description="Description of the front-end requirements.",
    )
    api_design: str = Field(
        description="Key API endpoints, data models, parameters, and response formats. Necessary data relationships and validation rules for smooth data exchange."
    )

class FrontEndDependencies(BaseModel):
    """
    Represents the front-end requirements along with their dependencies.

    Attributes:
        requirements (FrontEndRequirements): The front-end requirements.
        frameworks (List[RequiredFramework]): List of additional frameworks and libraries needed to implement the front end, with descriptions.
    """
    requirements: FrontEndRequirements = Field(
        description="The front-end requirements.",
    )
    frameworks: List[RequiredFramework] = Field(
        description="List of additional frameworks and libraries needed to implement the front end, with descriptions.",
    )

# Back-End Models

class BackEndRequirements(BaseModel):
    """
    Represents the back-end requirements for the project.

    Attributes:
        description (str): Description of the back-end requirements.
        api_endpoints (str): List of API endpoints with request methods, parameters, responses, and logic.
    """
    description: str = Field(
        description="Description of the back-end requirements.",
    )
    api_endpoints: str = Field(
        description="List of API endpoints with request methods, parameters, responses, and logic.",
    )

class BackEndDependencies(BaseModel):
    """
    Represents the back-end requirements along with their dependencies.

    Attributes:
        requirements (BackEndRequirements): The back-end requirements.
        frameworks (List[RequiredFramework]): List of additional frameworks and libraries needed to implement the back end, with descriptions.
    """
    requirements: BackEndRequirements = Field(
        description="The back-end requirements.",
    )
    frameworks: List[RequiredFramework] = Field(
        description="List of additional frameworks and libraries needed to implement the back end, with descriptions.",
    )

# Code Organization Models

class Method(BaseModel):
    """
    Represents a method within a file.

    Attributes:
        name (str): The name of the method.
        signature (str): The method's signature, including parameters.
        return_statement (str): What the method returns.
        description (str): A brief description of what the method does.
    """
    name: str = Field(
        description="The name of the method.",
    )
    signature: str = Field(
        description="The method's signature, including parameters.",
    )
    return_statement: str = Field(
        description="What the method returns.",
    )
    description: str = Field(
        description="A brief description of what the method does.",
    )

class File(BaseModel):
    """
    Represents a file in the project.

    Attributes:
        name (str): The name of the file.
        description (str): A brief description of what the file does.
        methods (List[Method]): A list of methods within the file.
        code (Optional[str]): The actual code of the file, if applicable (e.g., for the endpoint file).
    """
    name: str = Field(
        description="The name of the file.",
    )
    description: str = Field(
        description="A brief description of what the file does.",
    )
    methods: List[Method] = Field(
        description="A list of methods within the file.",
    )
    code: Optional[str] = Field(
        default=None,
        description="The actual code of the file, if applicable (e.g., for the endpoint file or if you were instructed to do so).",
    )

class Folder(BaseModel):
    """
    Represents a folder containing files.

    Attributes:
        name (str): The name of the folder.
        files (List[File]): A list of files within the folder.
    """
    name: str = Field(
        description="The name of the folder.",
    )
    files: List[File] = Field(
        default_factory=list,
        description="A list of files within the folder.",
    ) 
    endpoint_file: Optional[File] = Field(
        default=None,
        description="The file containing the actual endpoint logic, available only in one specific folder.",
    )

class CodeOrganization(BaseModel):
    """
    Organizes the code structure by maintaining a list of folders.

    Attributes:
        folders (List[Folder]): A list of folders in the project.
    """
    folders: List[Folder] = Field(
        description="A list of folders in the project.",
    )
    

'''
class CodeGeneration(BaseModel):
    """
    Represents the generated code for a file.

    Attributes:
        file_name (str): The name of the file.
        code (str): The actual code of the file.
    """
    file_name: str = Field(
        description="The name of the file.",
    )
    code: str = Field(
        description="The actual code of the file.",
    )

class CodeFolder(BaseModel):
    """
    Represents a folder containing generated code files.

    Attributes:
        folder_name (str): The name of the folder.
        files (List[CodeGeneration]): A list of code files within the folder.
    """
    folder_name: str = Field(
        description="The folder name where the files are located.",
    )
    files: List[CodeGeneration] = Field(
        description="List of code files in the folder.",
    )
'''
# Developer State

class DeveloperState(BaseModel):
    topic: str = Field(
        description="The project topic or app idea.",
    )
    global_requirements: Optional[FunctionalRequirements] = Field(
        default=None,
        description="The global functional requirements.",
    )
    front_end: Optional[FrontEndDependencies] = Field(
        default=None,
        description="The front-end requirements and dependencies.",
    )
    back_end: Optional[BackEndDependencies] = Field(
        default=None,
        description="The back-end requirements and dependencies.",
    )
    human_feedback: Optional[str] = Field(
        default=None,

        description="Any human developer feedback.",
    )
    front_end_organization: Optional[CodeOrganization] = Field(
        default=None,
        description="The organization of front-end code.",
    )
    back_end_organization: Optional[CodeOrganization] = Field(
        default=None,
        description="The organization of back-end code.",
    )
    generate_backend_code: Optional[CodeOrganization] = Field(
        default=None,
        description="Generated back-end code files organized by folders.",
    )
    generate_frontend_code: Optional[CodeOrganization] = Field(
        default=None,
        description="Generated front-end code files organized by folders.",
    )