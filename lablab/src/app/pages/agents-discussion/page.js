"use client";
import { useState, useRef, useEffect } from "react";
import axios from "axios";
import DOMPurify from 'dompurify';

export default function AgentsDiscussion() {
  const [discussionHistory, setDiscussionHistory] = useState([]);
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [scrapedData, setScrapedData] = useState(null);
  const scrollRef = useRef(null);

  // Retrieve scraped data from cache
  useEffect(() => {
    const cachedData = sessionStorage.getItem('currentScrapedData');
    if (cachedData) {
      try {
        const parsedData = JSON.parse(cachedData);
        setScrapedData(parsedData);
        // Clear cache after retrieval
        sessionStorage.removeItem('currentScrapedData');
      } catch (error) {
        console.error("Error parsing cached data:", error);
        setError("Invalid cached data format");
      }
    } else {
      setError("No discussion data found - please start from the main page");
    }
  }, []);

  // Fetch discussion data
  const fetchDiscussion = async () => {
    setLoading(true);
    setError("");
    try {
      // const response = await axios.get("http://localhost:8080/api/agents-discussion", {
      const response = await axios.get("https://pythonapp-agent.vercel.app/api/agents-discussion", {
        params: { 
          WebSiteSummary: scrapedData?.data 
        }
      });
      console.log(response.data);
      setDiscussionHistory(response.data.history);
      setSummary(response.data.summary);
      scrollToBottom(); // Auto-scroll on new data
    } catch (error) {
      console.error("Error fetching discussion:", error);
      setError("Failed to fetch discussion data.");
    }
    setLoading(false);
  };

  // Scroll to the latest message
  const scrollToBottom = () => {
    setTimeout(() => {
      scrollRef.current?.scrollIntoView({ behavior: "smooth" });
    }, 100);
  };

  // Speech synthesis (Text-to-Speech)
  const speakText = (text) => {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-US";
    utterance.rate = 1;
    window.speechSynthesis.speak(utterance);
  };

  return (
    <div className="p-8 max-w-3xl mx-auto bg-white shadow-lg rounded-xl border border-gray-100 transition-all duration-300 hover:shadow-xl">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">🤖 Agents Discussion</h1>

      {/* Display scraped data */}
      {scrapedData && (
        <div className="mb-6 p-5 bg-gray-50 rounded-lg border-l-4 border-gray-500">
          <strong className="text-gray-700">📊 Scraped Data:</strong>
          <p className="mt-2 text-gray-700">{scrapedData.data}</p>
        </div>
      )}

      {/* Buttons */}
      <div className="flex gap-4 mb-6">
        <button
          onClick={fetchDiscussion}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all duration-300 ease-in-out transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          {loading ? "Fetching..." : "Fetch Discussion"}
        </button>
      </div>

      {/* Loading animation */}
      {loading && (
        <div className="mt-6 flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
          <p className="ml-3 text-gray-600">Loading...</p>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="mt-6 p-4 bg-red-50 rounded-lg border-l-4 border-red-500">
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {/* Summary */}
      {summary && (
        <div className="mt-6 p-5 bg-blue-50 rounded-lg border-l-4 border-blue-500">
          <strong className="text-blue-700">📝 Summary:</strong>
          <p className="mt-2 text-gray-700">{summary}</p>
          <button
            onClick={() => speakText(summary)}
            className="mt-2 px-4 py-2 text-sm bg-gray-200 rounded-lg hover:bg-gray-300 transition duration-300"
          >
            🔊 Read Aloud
          </button>
        </div>
      )}

      {/* Discussion History */}
      <div className="mt-6 space-y-4 max-h-96 overflow-y-auto border border-gray-200 p-4 rounded-lg">
        {discussionHistory.length > 0 ? (
          discussionHistory.map((entry, index) => (
            <div
              key={index}
              className={`p-4 rounded-lg border-l-4 transition-all duration-300 ${
                entry.agent === "Agent 1" ? "border-blue-400 bg-blue-50" : "border-green-400 bg-green-50"
              }`}
            >
              <strong className="text-gray-700">{entry.agent}:</strong>
              <p className="mt-1 text-gray-600">{entry.message}</p>
              <button
                onClick={() => speakText(entry.message)}
                className="mt-2 px-3 py-1 text-xs bg-gray-200 rounded-lg hover:bg-gray-300 transition duration-300"
              >
                🔊 Read Aloud
              </button>
            </div>
          ))
        ) : (
          <p className="text-gray-500 text-center">No discussion available yet.</p>
        )}
        {/* Scroll anchor */}
        <div ref={scrollRef}></div>
      </div>
    </div>
  );
}