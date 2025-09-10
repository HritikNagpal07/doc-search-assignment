from chroma_db import add_to_chroma
from database import insert_document, init_db
from pathlib import Path

def split_text(text: str, chunk_size: int = 300) -> list:
    """Splits a long text into smaller chunks. This is a simple word-based splitter."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def ingest_documents():
    """The main function that loads files, splits them, and stores them in the databases."""
    # Initialize the SQLite database
    init_db()
    documents_path = Path("./documents")
    
    # Loop through every Markdown file in the "documents" folder
    for file_path in documents_path.glob("*.md"):
        print(f"Processing {file_path.name}...")
        
        try:
            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # In a real scenario, you'd parse this from the file. Using placeholder.
            repo_name = "sample_repo"
            title = file_path.stem  # The filename without the .md extension
            
            # 1. Store the file's metadata in SQLite
            insert_document(str(file_path), repo_name, title)
            
            # 2. Split the file content into chunks
            chunks = split_text(content)
            
            # 3. Add each chunk to ChromaDB
            for idx, chunk in enumerate(chunks):
                # Create a unique ID for this chunk
                chunk_id = f"{file_path.stem}_{idx}"
                # Create metadata to remember where this chunk came from
                metadata = {"source_file": str(file_path.name), "repo_name": repo_name}
                # Add it to the vector database
                add_to_chroma(chunk_id, chunk, metadata)
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print("Document ingestion completed! The system is ready to search.")

# This runs the function when you execute the script
if __name__ == "__main__":
    ingest_documents()
