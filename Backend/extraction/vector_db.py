import os
import uuid
import chromadb
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter

# Load environment variables
load_dotenv()

# Set your OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')

# Function to initialize ChromaDB client
def init_chroma():
    """Initialize ChromaDB client."""
    client = chromadb.Client()
    return client

# Function to create and store embeddings into ChromaDB with chunking
def create_and_store_embeddings(parsed_data):
    """Store window and door embeddings into ChromaDB after splitting into chunks."""
    chroma_client = init_chroma()

    # Define the embeddings using OpenAI through Langchain
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # Create or get a collection in ChromaDB for storing the embeddings
    collection = chroma_client.get_or_create_collection("window_door_specifications")

    # Initialize lists to store documents, metadata, and IDs
    documents = []
    metadatas = []
    ids = []

    # Initialize the text splitter
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    # Process window specifications and split into chunks
    for window in parsed_data['windows']:
        window_text = f"Window Type: {window['window_type']}, Material: {window['material']}, " \
                      f"Width: {window['width_inches']} inches, Height: {window['height_inches']} inches, " \
                      f"Glass Type: {window['glass_type']}, Color: {window['color']}, Quantity: {window['quantity']}, " \
                      f"Manufacturer: {window['manufacturer']}"

        # Split the text into manageable chunks
        chunks = text_splitter.split_text(window_text)
        
        for chunk in chunks:
            documents.append(chunk)
            metadatas.append({
                "type": "window",
                "window_type": window['window_type'],
                "material": window['material'],
                "width_inches": window['width_inches'],
                "height_inches": window['height_inches'],
                "glass_type": window['glass_type'],
                "color": window['color'],
                "quantity": window['quantity'],
                "manufacturer": window['manufacturer']
            })
            ids.append(str(uuid.uuid4()))  # Generate a unique ID for each chunk

    # Process door specifications and split into chunks
    for door in parsed_data['doors']:
        door_text = f"Door Type: {door['door_type']}, Material: {door['material']}, " \
                    f"Width: {door['width_inches']} inches, Height: {door['height_inches']} inches, " \
                    f"Glass Type: {door['glass_type']}, Color: {door['color']}, Quantity: {door['quantity']}, " \
                    f"Manufacturer: {door['manufacturer']}"

        # Split the text into manageable chunks
        chunks = text_splitter.split_text(door_text)

        for chunk in chunks:
            documents.append(chunk)
            metadatas.append({
                "type": "door",
                "door_type": door['door_type'],
                "material": door['material'],
                "width_inches": door['width_inches'],
                "height_inches": door['height_inches'],
                "glass_type": door['glass_type'],
                "color": door['color'],
                "quantity": door['quantity'],
                "manufacturer": door['manufacturer']
            })
            ids.append(str(uuid.uuid4()))  # Generate a unique ID for each chunk

    # Store the chunks and metadata in ChromaDB with unique IDs
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print("Embeddings for chunks stored successfully in ChromaDB.")
