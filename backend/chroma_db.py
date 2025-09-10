import chromadb
from sentence_transformers import SentenceTransformer

# Load the model that converts text into number arrays (vectors)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Connect to the ChromaDB database. It will create a 'chroma_data' folder to store information.
chroma_client = chromadb.PersistentClient(path="chroma_data")
# Get or create a collection named "docs" to store our text chunks
collection = chroma_client.get_or_create_collection(name="docs")

def generate_embedding(text: str):
    """Takes a string of text and turns it into a list of numbers (a vector)."""
    return embedder.encode(text).tolist()

def add_to_chroma(chunk_id: str, text: str, metadata: dict):
    """Adds a piece of text (chunk) to the vector database."""
    embedding = generate_embedding(text)
    collection.add(
        documents=[text],       # The actual text chunk
        embeddings=[embedding], # Its numerical representation
        metadatas=[metadata],   # Its info (file name, repo name)
        ids=[chunk_id]          # A unique ID for this chunk
    )

def query_chroma(query_text: str, n_results: int = 5):
    """Searches the database for chunks similar to the query."""
    query_embedding = generate_embedding(query_text)
    # Ask ChromaDB to find the closest vectors to our query vector
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=['documents', 'metadatas', 'distances'] # Return the text, info, and match score
    )
    return results
