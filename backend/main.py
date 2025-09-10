from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chroma_db import query_chroma
from typing import List

# Define what a search request and result should look like
class SearchQuery(BaseModel):
    query: str

class SearchResult(BaseModel):
    content: str
    source_file: str
    repo_name: str
    score: float

# Create the FastAPI application
app = FastAPI(title="Documentation Search API")

# This allows the React frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # React's default address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# The main search endpoint
@app.post("/search", response_model=List[SearchResult])
async def search(search_query: SearchQuery):
    """API endpoint that accepts a search query and returns relevant document chunks."""
    # Check for empty query
    if not search_query.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        # 1. Query the vector database
        results = query_chroma(search_query.query)
        formatted_results = []
        
        # 2. If we found results, format them nicely
        if results['ids'][0]:
            for i in range(len(results['ids'][0])):
                # For each result, create a SearchResult object
                result = SearchResult(
                    content=results['documents'][0][i],
                    source_file=results['metadatas'][0][i]['source_file'],
                    repo_name=results['metadatas'][0][i]['repo_name'],
                    # Convert distance to a confidence score (lower distance = higher score)
                    score=round(1.0 - results['distances'][0][i], 2)
                )
                formatted_results.append(result)
        
        # 3. Return the results
        return formatted_results
        
    except Exception as e:
        # Handle any errors gracefully
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

# This runs the application when you execute the script
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
