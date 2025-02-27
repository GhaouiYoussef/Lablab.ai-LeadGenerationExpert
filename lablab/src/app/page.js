"use client";
import { useState } from "react";
import axios from "axios";
import AgentsDiscussion from './pages/agents-discussion/page.js';

export default function MainPage() {
  const [company, setCompany] = useState("");
  const [industry, setIndustry] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [scrapedData, setScrapedData] = useState(null);
  const [discussionData, setDiscussionData] = useState(null);

  const handleFetchData = async () => {
    setLoading(true);
    setError("");
    setScrapedData(null);
    setDiscussionData(null);

    try {
      // First attempt with primary API
      // let response = await axios.get(`https://lablabscrappercompanies.vercel.app/company-info`, {
      let response = await axios.get(`http://localhost:8001/company-info`, {
        params: { company },
      });

      if (!response.data || !response.data.data) {
        throw new Error("No relevant data found.");
      }

      console.log("Scraped Data:", response.data);
      setScrapedData(response.data);
      sessionStorage.setItem("currentScrapedData", JSON.stringify(response.data));

      // Call AI agent discussion API with the extracted summary
      // const discussionResponse = await axios.get(`https://pythonapp-agent.vercel.app/api/agents-discussion/`, {
      const discussionResponse = await axios.get(`http://localhost:8000/api/agents-discussion/`, {
        params: {
          WebSiteSummary: response.data.data,
          UserCompany: company || "AI Consulting",
        },
      });

      console.log("AI Discussion Data:", discussionResponse.data);
      setDiscussionData(discussionResponse.data);

      // Scroll to discussion section
      document.getElementById("discussion").scrollIntoView({ behavior: "smooth" });

    } catch (err) {
      console.error("Error fetching data:", err);
      setError("Failed to fetch company details. Trying alternative source...");

      try {
        // Second attempt with backup API
        let fallbackResponse = await axios.get(`https://pythonapp-agent.vercel.app/api/company-info`, {
          params: { company },
        });

        if (!fallbackResponse.data || !fallbackResponse.data.data) {
          throw new Error("Fallback also failed.");
        }

        console.log("Fallback Scraped Data:", fallbackResponse.data);
        setScrapedData(fallbackResponse.data);
        sessionStorage.setItem("currentScrapedData", JSON.stringify(fallbackResponse.data));

        // Call AI agent discussion API
        const discussionResponse = await axios.get(`https://pythonapp-agent.vercel.app/api/agents-discussion/`, {
          params: {
            WebSiteSummary: fallbackResponse.data.data,
            UserCompany: company || "AI Consulting",
          },
        });

        console.log("AI Discussion Data:", discussionResponse.data);
        setDiscussionData(discussionResponse.data);

        // Scroll to discussion section
        document.getElementById("discussion").scrollIntoView({ behavior: "smooth" });

      } catch (fallbackError) {
        console.error("Error fetching fallback data:", fallbackError);
        setError("Both sources failed. Please try again later.");
      }
    }

    setLoading(false);
  };

  return (
    <div className="p-8 max-w-4xl mx-auto bg-white shadow-lg rounded-xl border border-gray-100">
      <h1 className="text-3xl font-bold text-gray-800 text-center">🚀 AI-Powered Leads Evaluation</h1>
      <p className="text-center text-gray-600 mt-2">Enter your company details to see AI agents in action.</p>

      {/* Company Input Form */}
      <div className="mt-6 p-6 bg-gray-50 rounded-lg border border-gray-200">
        <label className="block text-gray-700 font-semibold mb-2">🔹 Your Company Name</label>
        <input
          type="text"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          placeholder="E.g., Acme Corp"
          className="w-full p-3 border rounded-lg focus:outline-none focus:ring focus:border-blue-300"
        />

        <label className="block text-gray-700 font-semibold mt-4 mb-2">🔹 Industry Specialization</label>
        <input
          type="text"
          value={industry}
          onChange={(e) => setIndustry(e.target.value)}
          placeholder="E.g., AI SaaS, Marketing, E-commerce"
          className="w-full p-3 border rounded-lg focus:outline-none focus:ring focus:border-blue-300"
        />

        <button
          onClick={handleFetchData}
          className="mt-4 w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all duration-300 ease-in-out"
        >
          {loading ? "Processing..." : "🔍 Analyze Company"}
        </button>

        {/* Error Message */}
        {error && <p className="mt-4 text-red-600">{error}</p>}
      </div>

      {/* Show Scraped Data (Before Discussion) */}
      {scrapedData && (
        <div className="mt-6 p-6 bg-green-50 rounded-lg border-l-4 border-green-500">
          <h2 className="text-xl font-bold text-green-700">✅ Scraped Data:</h2>
          <p className="mt-2 text-gray-700">{scrapedData.data}</p>
        </div>
      )}

      {/* 💬 Live AI Discussion */}
      <section id="discussion" className="py-16 px-6 bg-gray-50">
        <h2 className="text-3xl font-bold text-center text-gray-800">🤖 AI-Powered Decision Making</h2>
        <p className="text-center text-gray-600 mt-2">Watch two AI agents debate lead quality before you make a decision.</p>

        <div className="mt-6">
          {discussionData ? (
            <div className="p-6 bg-white shadow-md rounded-lg border border-gray-300">
              <h3 className="text-xl font-semibold text-gray-800">🗣️ AI Discussion Result:</h3>
              {discussionData ? (
              <div className="p-6 bg-white shadow-md rounded-lg border border-gray-300">
                <h3 className="text-xl font-semibold text-gray-800">🗣️ AI Discussion Result:</h3>
                <p className="mt-2 text-gray-700"><strong>Summary:</strong> {discussionData.summary}</p>
                <h4 className="text-lg font-semibold mt-4">📜 Discussion History:</h4>
                <ul className="list-disc list-inside text-gray-700 mt-2">
                  {discussionData.history?.map((entry, index) => (
                    <li key={index}>{entry}</li>
                  ))}
                </ul>
              </div>
            ) : (
              <p className="text-center text-gray-500">Waiting for AI discussion results...</p>
            )}

            </div>
          ) : (
            <p className="text-center text-gray-500">Waiting for AI discussion results...</p>
          )}
          <AgentsDiscussion />
        </div>
      </section>
    </div>
  );
}
