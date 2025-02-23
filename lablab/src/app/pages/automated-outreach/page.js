import Link from "next/link";

export default function AutomatedOutreach() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto bg-white p-10 rounded-xl shadow-lg">
        <h1 className="text-4xl font-bold text-gray-800">🤖 Automated Outreach</h1>
        <p className="mt-4 text-gray-600 text-lg">
          Our AI-powered system **automates email, LinkedIn, and chat outreach**, ensuring your 
          leads get the right message at the right time.
        </p>
        <img src="/images/automated-outreach.jpg" alt="Automated Outreach" className="mt-6 w-full rounded-lg shadow-md" />

        <h2 className="mt-8 text-2xl font-bold text-gray-800">📌 Why It’s Powerful</h2>
        <ul className="list-disc mt-4 text-gray-600 ml-6">
          <li>💬 AI **personalizes** messages based on user data</li>
          <li>📩 Auto-follows up with **engagement tracking**</li>
          <li>📊 A/B Testing to **optimize open & response rates**</li>
        </ul>

        <Link href="/">
          <button className="mt-8 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
            🚀 Automate My Outreach
          </button>
        </Link>
      </div>
    </div>
  );
}
