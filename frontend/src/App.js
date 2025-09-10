import React, { useState } from 'react';
import axios from 'axios';

// This is the address of our backend API
const API_BASE = 'http://localhost:8000';

function App() {
  // React hooks to manage state
  const [query, setQuery] = useState(''); // Stores the user's search query
  const [results, setResults] = useState([]); // Stores the search results
  const [loading, setLoading] = useState(false); // True when waiting for results
  const [error, setError] = useState(''); // Stores an error message if something goes wrong

  // This function is called when the user clicks the Search button
  const handleSearch = async (e) => {
    e.preventDefault(); // Prevents the form from refreshing the page
    if (!query.trim()) return; // Don't search if the query is empty

    setLoading(true); // Show the loading indicator
    setError(''); // Clear any old errors
    setResults([]); // Clear any old results
    
    try {
      // Send the search query to our backend API
      const response = await axios.post(`${API_BASE}/search`, { query: query });
      // If successful, save the results we got back
      setResults(response.data);
    } catch (err) {
      // If something went wrong, show the error message
      setError(err.response?.data?.detail || 'Search failed. Please check if the backend is running.');
    } finally {
      // This runs whether we succeeded or failed
      setLoading(false); // Hide the loading indicator
    }
  };

  // This defines the UI that the user sees
  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Page Title */}
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">
          Documentation Search
        </h1>

        {/* Search Input Form */}
        <form onSubmit={handleSearch} className="mb-8">
          <div className="flex gap-2">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)} // Update the query state as the user types
              placeholder="Enter your search query..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {/* Show 'Searching...' on the button while loading */}
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>
        </form>

        {/* Show error message if there is one */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {/* Results List */}
        <div className="space-y-4">
          {results.map((result, index) => (
            <div key={index} className="bg-white p-6 rounded-lg shadow">
              <div className="flex justify-between items-start mb-2">
                <span className="text-sm text-gray-600 bg-gray-100 px-2 py-1 rounded">
                  {/* Show which repository this result came from */}
                  {result.repo_name}
                </span>
                {/* Show the match score as a percentage */}
                <span className="text-sm text-blue-600">
                  Score: {(result.score * 100).toFixed(1)}%
                </span>
              </div>
              {/* The actual text from the document */}
              <p className="text-gray-800 mb-2">{result.content}</p>
              {/* The name of the file this was found in */}
              <p className="text-sm text-gray-500">
                Source: {result.source_file}
              </p>
            </div>
          ))}
        </div>

        {/* Show a message if there are no results and we aren't loading */}
        {results.length === 0 && !loading && !error && (
          <div className="text-center text-gray-500 py-12">
            Enter a search query to find relevant documentation. Try "authentication" or "database".
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
