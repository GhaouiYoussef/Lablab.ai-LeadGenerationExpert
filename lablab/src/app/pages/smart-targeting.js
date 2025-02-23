import Link from "next/link";

export default function SmartTargeting() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto bg-white p-10 rounded-xl shadow-lg">
        <h1 className="text-4xl font-bold text-gray-800">🎯 Smart Targeting</h1>
        <p className="mt-4 text-gray-600 text-lg">
          Our AI-driven system analyzes industry trends, customer behavior, and real-time data
          to find the **best leads for your business**.
        </p>
        <img src="/images/smart-targeting.jpg" alt="Smart Targeting" className="mt-6 w-full rounded-lg shadow-md" />

        <h2 className="mt-8 text-2xl font-bold text-gray-800">📌 How It Works</h2>
        <ul className="list-disc mt-4 text-gray-600 ml-6">
          <li>🚀 AI scans **millions of data points** to identify **high-converting leads**</li>
          <li>🔍 Advanced **lead scoring** ensures **quality over quantity**</li>
          <li>📊 Filters based on **industry, location, and engagement patterns**</li>
        </ul>

        <Link href="/">
          <button className="mt-8 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
            🔥 Start Generating Leads
          </button>
        </Link>
      </div>
    </div>
  );
}
