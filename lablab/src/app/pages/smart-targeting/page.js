"use client";
import { useState } from "react";
import Link from "next/link";
import DOMPurify from 'dompurify';


const scrapeData = async (company) => {
  try {
    // Call your backend API
    // const response = await fetch(`http://localhost:8101/company-info?company=${encodeURIComponent(company)}`);
    const response = await fetch(`https://lablabscrappercompanies.vercel.app/api/company-info?company=${encodeURIComponent(company)}`);

    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching company data:", error);
    return {
      company,
      data: `Failed to fetch data for ${company}. Using mock data.`,
    };
  }
};


export default function SmartTargeting() {
  const [file, setFile] = useState(null);
  const [predictions, setPredictions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [scrapedData, setScrapedData] = useState(null); // State to hold scraped data

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) return alert("Please upload a CSV file.");
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("https://ml-leadgen.vercel.app/predict", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) {
        throw new Error(`Server error: ${res.statusText}`);
      }
      const data = await res.json();
      setPredictions(data.predictions);
    } catch (err) {
      alert(`Error processing file: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Modified handleDiscuss and display logic
  const handleDiscuss = async (company) => {
    setLoading(true);
    try {
      const data = await scrapeData(company);
      // Store in sessionStorage before navigation
      sessionStorage.setItem('currentScrapedData', JSON.stringify(data));
      setScrapedData(data);
    } catch (error) {
      console.error("Error discussing company:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 p-8">
      <div className="max-w-6xl mx-auto bg-white p-10 rounded-3xl shadow-xl overflow-hidden">
        <h1 className="text-5xl font-bold text-center text-gray-800">
          🎯 Smart Targeting
        </h1>
        <p className="mt-6 text-lg text-center text-gray-600">
          Upload a CSV file and let our AI predict the best leads for you.
        </p>

        <div className="mt-8 flex justify-center">
          <input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            className="border-2 border-gray-300 rounded-lg px-4 py-2 cursor-pointer hover:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div className="text-center mt-6">
          <button
            onClick={handleUpload}
            disabled={loading}
            className="px-8 py-3 bg-indigo-600 text-white rounded-lg shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50 transition duration-200"
          >
            {loading ? "Processing..." : "🚀 Upload & Predict"}
          </button>
        </div>

        {predictions && (
          <div className="mt-8 overflow-x-auto rounded-lg shadow-lg">
            <h2 className="text-3xl font-semibold text-gray-800 text-center">
              📊 Predictions
            </h2>
            <table className="min-w-full table-auto mt-6 text-sm text-left text-gray-800">
              <thead className="bg-indigo-600 text-white">
                <tr>
                  <th className="py-3 px-4 text-center">Opportunity ID</th>
                  <th className="py-3 px-4 text-center">Sales Agent</th>
                  <th className="py-3 px-4 text-center">Product</th>
                  <th className="py-3 px-4 text-center">Account</th>
                  <th className="py-3 px-4 text-center">Prediction</th>
                  <th className="py-3 px-4 text-center">Action</th>
                </tr>
              </thead>
              <tbody>
                {predictions.map((prediction, index) => (
                  <tr
                    key={index}
                    className={`border-t hover:bg-indigo-50 ${index % 2 === 0 ? "bg-gray-50" : "bg-white"}`}
                  >
                    <td className="py-3 px-4 text-center">{prediction.opportunity_id}</td>
                    <td className="py-3 px-4 text-center">{prediction.sales_agent}</td>
                    <td className="py-3 px-4 text-center">{prediction.product}</td>
                    <td className="py-3 px-4 text-center">{prediction.account}</td>
                    <td className="py-3 px-4 text-center">{prediction.prediction}</td>
                    <td className="py-3 px-4 text-center">
                      <button
                        onClick={() => handleDiscuss(prediction.account)}
                        className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                      >
                        Discuss
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Link to navigate to the agents-discussion page with scraped data */}
        {scrapedData && (
  <Link
    href="/pages/agents-discussion"
    className="mt-4 inline-block px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
  >
    Continue to Detailed Discussion →
  </Link>
)}
      </div>
    </div>
  );
}