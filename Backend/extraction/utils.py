import os
import tempfile
import requests
import re
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from typing import Optional, List
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set your OpenAI API key
API_KEY = os.getenv('OPENAI_API_KEY')  # Load from environment variable
if API_KEY is None:
    raise ValueError("OpenAI API key must be set.")

# Define schemas
class WindowSpecification(BaseModel):
    window_type: Optional[str] = Field(default=None, description="The type of the window")
    material: Optional[str] = Field(default=None, description="The material of the window")
    width_inches: Optional[str] = Field(default=None, description="Width in inches")
    height_inches: Optional[str] = Field(default=None, description="Height in inches")
    glass_type: Optional[str] = Field(default=None, description="Type of glass used in the window")
    color: Optional[str] = Field(default=None, description="Color of the window")
    quantity: Optional[int] = Field(default=None, description="Quantity of windows")
    manufacturer: Optional[str] = Field(default=None, description="Manufacturer of the window")

class DoorSpecification(BaseModel):
    door_type: Optional[str] = Field(default=None, description="The type of the door")
    material: Optional[str] = Field(default=None, description="The material of the door")
    width_inches: Optional[str] = Field(default=None, description="Width in inches")
    height_inches: Optional[str] = Field(default=None, description="Height in inches")
    glass_type: Optional[str] = Field(default=None, description="Type of glass used in the door")
    color: Optional[str] = Field(default=None, description="Color of the door")
    quantity: Optional[int] = Field(default=None, description="Quantity of doors")
    manufacturer: Optional[str] = Field(default=None, description="Manufacturer of the door")

class ProjectSpecifications(BaseModel):
    windows: List[WindowSpecification]
    doors: List[DoorSpecification]

# Load and split the PDF document
def load_and_split_pdf(file_obj):
    """Load a PDF and split it into smaller chunks."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file_obj.read())
        temp_file_path = temp_file.name

    loader = PyPDFLoader(temp_file_path)
    pages = loader.load()
    os.remove(temp_file_path)

    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(pages)
    return chunks

# Function to extract structured data from text using OpenAI API
def extract_structured_data_from_text(text: str):
    """Extract structured data from the given text using the OpenAI API."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": (
                    "You are an expert extraction algorithm. Analyze the following text and extract all relevant specifications for windows and doors. "
                    "Consider different formats including tables, paragraphs, or bullet points. Handle dimensions denoted as 'W' and 'H'. "
                    "Provide details for:\n"
                    "- Window Type\n"
                    "- Material\n"
                    "- Width (inches)\n"
                    "- Height (inches)\n"
                    "- Glass Type\n"
                    "- Color\n"
                    "- Quantity\n"
                    "- Manufacturer\n\n"
                    f"Here's the text:\n\n{text}\n\n"
                    "If any detail is unknown, return 'null'."
                )
            }
        ]
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        response_json = response.json()
        return response_json.get("choices")[0]["message"]["content"]
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None  # Handle errors as necessary

# Function to parse the unstructured output
def parse_extracted_data(raw_data: str) -> ProjectSpecifications:
    """Parse the raw output from the OpenAI API into structured data."""
    windows = []
    doors = []

    # Flexible regex patterns for specifications based on table-like structure
    window_pattern = re.compile(r"\|\s*([\w\s\-]+)\s*\|\s*([\w\s]+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([\w\s\-]+)\s*\|\s*([\w]+)\s*\|\s*(\d+)\s*\|\s*([\w\s]+)\s*\|")
    door_pattern = re.compile(r"\|\s*([\w\s\-]+)\s*\|\s*([\w\s]+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([\w\s\-]+)\s*\|\s*([\w]+)\s*\|\s*(\d+)\s*\|\s*([\w\s]+)\s*\|")

    # Extracting Window Specifications
    for match in window_pattern.finditer(raw_data):
        windows.append(WindowSpecification(
            window_type=match.group(1).strip(),
            material=match.group(2).strip(),
            width_inches=str(match.group(3)),  # Convert to string
            height_inches=str(match.group(4)),  # Convert to string
            glass_type=match.group(5).strip(),
            color=match.group(6).strip(),
            quantity=int(match.group(7)),
            manufacturer=match.group(8).strip()
        ))

    # Extracting Door Specifications
    for match in door_pattern.finditer(raw_data):
        doors.append(DoorSpecification(
            door_type=match.group(1).strip(),
            material=match.group(2).strip(),
            width_inches=str(match.group(3)),  # Convert to string
            height_inches=str(match.group(4)),  # Convert to string
            glass_type=match.group(5).strip(),
            color=match.group(6).strip(),
            quantity=int(match.group(7)),
            manufacturer=match.group(8).strip()
        ))

    return ProjectSpecifications(windows=windows, doors=doors)


# Main function to process the PDF and extract structured data
def process_pdf(file_obj):
    """Process the uploaded PDF and extract structured window and door specifications."""
    chunks = load_and_split_pdf(file_obj)

    # Combine the text chunks into one string for the OpenAI API
    combined_text = "\n".join(chunk.page_content for chunk in chunks)

    # Check if the combined text is empty
    if not combined_text.strip():
        print("No content extracted from the PDF.")
        return {"windows": [], "doors": []}  # Return empty if no text is found
    
    # Pass the combined text to the OpenAI model for structured data extraction
    structured_data = extract_structured_data_from_text(combined_text)
    if structured_data is None:
        return {"windows": [], "doors": []}

    # Parse the extracted raw data into structured JSON
    parsed_data = parse_extracted_data(structured_data)
    print(parsed_data)
    return {
        "windows": [window.dict() for window in parsed_data.windows],
        "doors": [door.dict() for door in parsed_data.doors]
    }
