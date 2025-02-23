import Link from "next/link";

export default function DataInsights() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto bg-white p-10 rounded-xl shadow-lg">
        <h1 className="text-4xl font-bold text-gray-800">📊 Data-Driven Insights</h1>
        <p className="mt-4 text-gray-600 text-lg">
          Track lead engagement, conversion rates, and AI-driven **lead quality scores** to make **informed decisions**.
        </p>
        <img src="/images/data-insights.jpg" alt="Data Insights" className="mt-6 w-full rounded-lg shadow-md" />

        <h2 className="mt-8 text-2xl font-bold text-gray-800">📌 Key Benefits</h2>
        <ul className="list-disc mt-4 text-gray-600 ml-6">
          <li>📈 **Real-time** analytics dashboard</li>
          <li>🔍 AI-driven **lead quality scores**</li>
          <li>📊 Track **engagement, open rates, and conversions**</li>
        </ul>

        <Link href="/">
          <button className="mt-8 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
            📊 Start Tracking Leads
          </button>
        </Link>
      </div>
    </div>
  );
}
