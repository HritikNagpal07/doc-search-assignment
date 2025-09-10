# Documentation Search Assignment

A semantic search system for GitHub documentation built with FastAPI, ChromaDB, and React.

## How to Run This Project

### Backend (FastAPI)
1. Navigate to the `backend` folder: `cd backend`
2. Install Python libraries: `pip install -r requirements.txt`
3. Add your Markdown files to the `backend/documents` folder.
4. Initialize the database and load the files: `python ingest_documents.py`
5. Start the server: `uvicorn main:app --reload`

The backend will run on `http://localhost:8000`

### Frontend (React)
1. Navigate to the `frontend` folder: `cd frontend`
2. Install Node.js libraries: `npm install`
3. Start the application: `npm start`

The frontend will run on `http://localhost:3000`

## How It Works
1. **Document Processing:** Markdown files are split into smaller chunks of text.
2. **Vector Embeddings:** Each text chunk is converted into a numerical vector (embedding) using the `all-MiniLM-L6-v2` model.
3. **Vector Search:** These embeddings are stored in ChromaDB, a vector database.
4. **Search:** When a user enters a query, it is also converted to an embedding. ChromaDB finds the most similar text chunks from the database.
5. **Results:** The most relevant chunks are displayed to the user with their source information.
