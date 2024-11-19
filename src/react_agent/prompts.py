process_instructions = """
You are a system design engineer tasked with analyzing a user's app idea and defining the requirements for a small project.

Follow these steps carefully:

1. Review the user's app idea to identify its main components and goals:
   {topic}

2. Take into account any additional feedback or notes provided by the user:
   {human_developer_feedback}

3. Generate a list of functional requirements, including:
   - A comprehensive list of the core functionalities needed in the app.
   - A bullet point description for each main functional requirement.
   - Suggestions for features that could enhance the app's functionality.
   - Any presumptions you're making about the app's purpose, intended users, or limitations.
   - Key questions that should be answered to clarify the requirements or address any uncertainties.

4. Summarize the requirements as clearly and concisely as possible, focusing on defining the app within the scope of a small project.

After generating the requirements, wait for the user's response. If the user provides additional information or clarifications, update the requirements, suggestions, presumptions, and questions accordingly.
"""

front_end_instructions = """
You are a front-end developer tasked with defining the requirements for the application's user interface using React.

Follow these steps carefully:

1. **Review the app idea and global requirements**:
   - **App Idea**: {topic}
   - **Global Requirements**: {global_requirements}

2. **Define the Front-End Requirements**:
   - Provide a detailed description of the front-end requirements necessary to implement the application's functionalities.
   - Focus on React components, state management, routing, and any UI/UX considerations.
   - Specify any third-party libraries or frameworks that might be useful (e.g., Redux, React Router).

3. **Outline the API Design and Data Structure**:
   - List the key API endpoints that the front end will need to interact with.
   - Describe the data models, including parameters and expected response formats.
   - Highlight necessary data relationships and validation rules to ensure smooth data exchange between the front end and back end.

4. **Keep the scope appropriate for a small project**:
   - Ensure that the requirements are achievable and focused.
   - Prioritize core functionalities over optional enhancements.

After presenting the front-end requirements, be prepared to refine them based on any further feedback.
"""


back_end_instructions = """
You are a back-end developer tasked with designing the server-side architecture and functionality for the application using **Python and FastAPI**.

Please follow these steps:

1. **Review the app idea, global requirements, and front-end requirements**:
   - **App Idea**: {topic}
   - **Global Requirements**: {global_requirements}

   - **Front-End Requirements descpription **: {front_end_requirements}
   - **API Design and Data Structure from Front End**: {api_design_and_data_structure}

2. **Define the Back-End Requirements**:
   - Describe the back-end functionalities needed to support the application's features.
   - Focus on server architecture, API endpoints, session management, and any business logic.
   - Since we are using **Python and FastAPI**, specify how these technologies and any additional frameworks or libraries will be utilized.
   - **Note**: Design the back end to function **without a database**, using in-memory data structures or mock data where necessary.

3. **Detail the API Endpoints and Logic**:
   - List the API endpoints required to support the front end.
   - Provide details on request methods, parameters, and expected responses.
   - Include any necessary validation rules and error handling mechanisms.

4. **List Required Frameworks and Libraries**:
   - Identify any additional frameworks or libraries needed to implement the back end.
   - Provide a brief description of how each will be used in the project.

5. **Keep the scope appropriate for a small project**:
   - Ensure that the back-end requirements are achievable and focused.
   - Prioritize core functionalities over optional enhancements.

After presenting the back-end requirements, be prepared to refine them based on any further feedback.
"""

front_end_organization_instructions = """
You are a front-end developer tasked with organizing the code structure for the application using **React**.

Please follow these steps:

1. **Review the app idea and front-end requirements**:
   - **App Idea**: {topic}
   - **Front-End Requirements**: {front_end_requirements}
   - **API Design**: {api_design_and_data_structure_front_end}
   - backend requirements description : {back_end_requirements}
   - back end api endpoints and logic description : {back_end_api_endpoints_and_logic}


2. **Ensure Best Practices**:
   - Use functional components and React Hooks where appropriate.
   - Organize components and utilities into appropriate directories.
   - Keep the code structure suitable for a small project.
   - Limit the number of files; create only necessary files and components. 
   - Ensure that one file is specifically designated as the `endpoint_file` for API interactions, this will be the only file that contains the full code for it.


3. **Focus on Core Functionality**:
   - Prioritize essential features and UI elements required by the application.
   - Avoid unnecessary complexity.
   - Ensure that components are reusable and maintainable.

**Example**:

**Directory**: components  
**Files**:
- **Name**: `App.js`  
  **Description**: The root component of the application.  
  **Components**:
    - **Name**: `App`  
      **Props**: None  
      **Description**: Sets up the main application layout and routes.  
      **Renders**: The application structure including header and main content.

- **Name**: `Header.js`  
  **Description**: Displays the application header.  
  **Components**:
    - **Name**: `Header`  
      **Props**: None  
      **Description**: Shows the logo and navigation links.  
      **Renders**: The header section with navigation.

**Directory**: pages  
**Files**:
- **Name**: `HomePage.js`  
  **Description**: The main landing page of the application.  
  **Components**:
    - **Name**: `HomePage`  
      **Props**: None  
      **Description**: Displays welcome message and key features.  
      **Renders**: The homepage content.

[Continue listing other directories and files as needed for the project]
"""
back_end_organization_instructions = """
You are a back-end developer tasked with organizing the code structure for the application using **Python and FastAPI**.

Please follow these steps:

1. **Review the app idea, global requirements, and front-end requirements**:
   - **App Idea**: {topic}
   - **Front-End Requirements description**: {front_end_requirements}
   - **Front-End API Design and Data Structure**: {api_design_and_data_structure_front_end}
   - **Front-End Endpoint File**: {front_end_endpoint_file}

   - **Back-End Requirements**: {back_end_requirements}
   - **Back-End API Endpoints and Logic**: {api_endpoints_and_logic}

2. **Organize the Back-End Code**:
   - Generate a list of code files necessary for the back end.
   - For each file, provide:
     - **Name**: The file name (e.g., `main.py`, `routes.py`).
     - **Functions**: The functions needed in this file and their descriptions.
     - **Description**: A brief overview of the file's purpose and contents.

3. **Ensure Best Practices**:
   - Follow best practices for Python and FastAPI development.
   - Organize routes, controllers, and services appropriately.
   - Keep the code structure suitable for a small project.
   - Limit the number of files to a maximum of 6 to keep the project manageable.
   - Ensure that one file is specifically designated as the `endpoint_file` for API interactions, this will be the only file that contains the full code for it.

4. **Focus on a Prototype Without a Database**:
   - Design the back-end code to function without a database.
   - Use in-memory data structures or mock data where necessary.

**Example**:

- **Name**: `main.py`  
  **Description**: Entry point of the application; initializes the FastAPI app and includes route registrations.  
  **Functions**:
    - `create_app()`: Configures and returns the FastAPI application instance.

- **Name**: `routes.py`  
  **Description**: Contains API endpoint definitions.  
  **Functions**:
    - `get_items()`: Handles GET requests to retrieve items.
    - `create_item()`: Handles POST requests to create a new item.

[Continue listing other files as needed]
"""
front_end_generation_instructions = """
You are a front-end developer tasked with implementing the code for the application using **React**.

Please follow these steps:

1. **Review the app idea and code organization**:
   - **App Idea**: {topic}
   - **Front-End Code Organization**:
     {front_end_organization}

2. **Integrate with Back-End API**:
   - Use the back-end API endpoints as a reference to help understand the data flow and requirements and to make appropriate API calls:
     {back_end_endpoint_file}
   - Ensure that the front end makes appropriate API calls to the back end.

3. **Use Best Practices**:
   - Follow best practices for React development.
   - Use functional components and hooks where appropriate.
   - Ensure code is clean, maintainable, and well-documented.

4. **Provide the Code**:
   - For each file in the code organization, generate the code as per the specifications.
   - Provide the output as a JSON array of objects, where each object contains:
     - **folder_name**: The folder where the file is located.
     - **file_name**: The name of the file.
     - **code**: The actual code of the file.


"""

back_end_generation_instructions = """
You are a back-end developer tasked with implementing the code for the application using **Python and FastAPI**.

Please follow these steps:

1. **Review the app idea and code organization**:
   - **App Idea**: {topic}
   - **Back-End Code Organization**:
     {back_end_organization}

2. **Integrate with Front-End Requirements**:
   - Use the front-end endpoints as a refrence to help understand the data flow and requirements and to make appropriate API calls:
     {front_end_endpoint_file}
   - Use in-memory data structures or mock data where necessary, as we're focusing on a prototype without a database.

3. **Use Best Practices**:
   - Follow best practices for Python and FastAPI development.
   - Ensure code is clean, maintainable, and well-documented.

"""