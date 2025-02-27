"use client";
import { useState } from "react";
import axios from "axios";
import Link from "next/link";

const NavBar = () => (
  <nav className="bg-blue-600 text-white py-4">
    <div className="max-w-5xl mx-auto flex justify-between items-center px-4">
      <div className="text-2xl font-bold">LeadGenAI</div>
      <div className="space-x-4">
        <Link href="#hero" className="hover:underline">Home</Link>
        <Link href="#features" className="hover:underline">Features</Link>
        <Link href="#discussion" className="hover:underline">Discussion</Link>
        <Link href="#testimonials" className="hover:underline">Testimonials</Link>
        <Link href="#pricing" className="hover:underline">Pricing</Link>
        <Link href="#contact" className="hover:underline">Contact</Link>
      </div>
    </div>
  </nav>
);

const FeatureCard = ({ title, link, desc }) => (
  <Link href={link}>
    <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition cursor-pointer">
      <h3 className="text-xl font-bold text-gray-800">{title}</h3>
      <p className="text-gray-600 mt-2">{desc}</p>
      <p className="text-blue-600 mt-2">Learn More →</p>
    </div>
  </Link>
);

const TestimonialCard = ({ name, text }) => (
  <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition">
    <p className="text-gray-600 italic">"{text}"</p>
    <h4 className="mt-3 text-gray-800 font-bold">{name}</h4>
  </div>
);

const PricingCard = ({ title, price, features }) => (
  <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition text-center">
    <h3 className="text-xl font-bold text-gray-800">{title}</h3>
    <p className="text-blue-600 text-2xl font-bold">{price}</p>
    <ul className="mt-3 text-gray-600">
      {features.map((feature, idx) => (
        <li key={idx}>✔ {feature}</li>
      ))}
    </ul>
  </div>
);

export default function Home() {
  const [company, setCompany] = useState("");
  const [industry, setIndustry] = useState("");
  const [loading, setLoading] = useState(false);
  const [loading_discussion, setLoading_Discussion] = useState(false);
  const [error, setError] = useState("");
  const [scrapedData, setScrapedData] = useState(null);
  const [discussionData, setDiscussionData] = useState(null);

  const handleFetchData = async () => {
    setLoading(true);
    setError("");
    setScrapedData(null);
    setDiscussionData(null);
    // setLoading_Discussion(true);
    try {
      let response = await axios.get(`https://lablabscrappercompanies.vercel.app/company-info`, {
        params: { company },
      });

      if (!response.data?.data) throw new Error("No relevant data found.");

      setScrapedData(response.data);
      sessionStorage.setItem("currentScrapedData", JSON.stringify(response.data));
      setLoading_Discussion(true);
      const discussionResponse = await axios.get(`https://pythonapp-agent.vercel.app/api/agents-discussion/`, {
      // const discussionResponse = await axios.get(`http://localhost:8000/api/agents-discussion/`, {
        params: {
          WebSiteSummary: response.data.data,
          UserCompany: company || "AI Consulting",
        },
      });

      setDiscussionData(discussionResponse.data);
      document.getElementById("discussion").scrollIntoView({ behavior: "smooth" });

    } catch (err) {
      console.error("Error fetching data:", err);
      setError("Failed to fetch company details. Trying alternative source...");

      try {
        const fallbackResponse = await axios.get(`https://lablabscrappercompanies.vercel.app/company-info`, {
          params: { company },
        });

        if (!fallbackResponse.data?.data) throw new Error("Fallback also failed.");

        setScrapedData(fallbackResponse.data);
        sessionStorage.setItem("currentScrapedData", JSON.stringify(fallbackResponse.data));
        
        setLoading_Discussion(true);
        const discussionResponse = await axios.get(`https://pythonapp-agent.vercel.app/api/agents-discussion/`, {
        // const discussionResponse = await axios.get(`http://localhost:8000/api/agents-discussion/`, {
          params: {
            WebSiteSummary: fallbackResponse.data.data,
            UserCompany: company || "AI Consulting",
          },
        });

        setDiscussionData(discussionResponse.data);
        document.getElementById("discussion").scrollIntoView({ behavior: "smooth" });

      } catch (fallbackError) {
        console.error("Fallback error:", fallbackError);
        setError("Both sources failed. Please try again later.");
      }
    }
    setLoading(false);
    setLoading_Discussion(false);
  };

  return (
    <div className="bg-gray-100 min-h-screen">
      <NavBar />
      
      {/* Hero Section */}
      <section id="hero" className="bg-blue-600 text-white text-center py-20 px-4">
        <h1 className="text-5xl font-bold">🚀 AI-Powered Lead Generation</h1>
        <p className="mt-4 text-lg">Let AI find and analyze your ideal clients in seconds.</p>
        <button className="mt-6 px-6 py-3 bg-white text-blue-600 font-bold rounded-lg hover:bg-gray-200 transition">
          Get Started
        </button>
      </section>

      {/* Features Section */}
      <section id="features" className="py-16 px-6 max-w-5xl mx-auto text-center">
        <h2 className="text-3xl font-bold text-gray-800">Why Choose Our AI?</h2>
        <div className="grid md:grid-cols-3 gap-6 mt-8">
          <FeatureCard 
            title="🎯 Smart Targeting" 
            link="pages/smart-targeting" 
            desc="Our AI analyzes market data to find the best leads for your business." 
          />
          <FeatureCard 
            title="🤖 Automated Outreach" 
            link="pages/automated-outreach" 
            desc="Automate outreach with AI-driven conversations and engagement."
          />
          <FeatureCard 
            title="📊 Data Insights" 
            link="pages/data-insights"  
            desc="Get real-time analytics on lead quality and conversion rates."
          />
        </div>
      </section>

      {/* Analysis Section */}
      <section className="py-16 px-6 max-w-4xl mx-auto">
        <div className="bg-white shadow-lg rounded-xl border border-gray-100 p-8">
          <h1 className="text-3xl font-bold text-gray-800 text-center">🚀 AI-Powered Leads Evaluation</h1>
          <p className="text-center text-gray-600 mt-2">Enter your company details to see AI agents in action.</p>

          <div className="mt-6 p-6 bg-gray-50 rounded-lg border border-gray-200">
            <label className="block text-gray-700 font-semibold mb-2">🔹 Target Potential Client Company Name</label>
            <input
              type="text"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              placeholder="E.g., Acme Corp"
              className="w-full p-3 border rounded-lg focus:outline-none text-black focus:ring focus:border-blue-300"
            />

            <label className="block text-gray-700 font-semibold mt-4 mb-2">🔹 Your Company Industry Specialization</label>
            <input
              type="text"
              value={industry}
              onChange={(e) => setIndustry(e.target.value)}
              placeholder="E.g., AI SaaS, Marketing, E-commerce"
              className="w-full p-3 border rounded-lg focus:outline-none text-black focus:ring focus:border-blue-300"
            />

            <button
              onClick={handleFetchData}
              className="mt-4 w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all duration-300 ease-in-out"
            >
              {loading ? "Processing..." : "🔍 Analyze Company"}
            </button>

            {error && <p className="mt-4 text-red-600">{error}</p>}
          </div>

          {scrapedData && (
            <div className="mt-6 p-6 bg-green-50 rounded-lg border-l-4 border-green-500">
              <h2 className="text-xl font-bold text-green-700">✅ Scraped Data:</h2>
              <p className="mt-2 text-gray-700">{scrapedData.data}</p>
            </div>
          )}
        </div>
      </section>

      {/* Discussion Section */}
      <section id="discussion" className="py-16 px-6 bg-gray-50">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-800">🤖 AI-Powered Decision Making</h2>
          <p className="text-center text-gray-600 mt-2">Watch two AI agents debate lead quality before you make a decision.</p>

          <div className="mt-6">
            {discussionData ? (
              <div className="p-6 bg-white shadow-md rounded-lg border border-gray-300">
                <h3 className="text-xl font-semibold text-gray-800">🗣️ AI Discussion Result:</h3>
                <p className="mt-2 text-gray-700"><strong>Summary:</strong> {discussionData.summary}</p>
                <h4 className="text-lg font-semibold mt-4">📜 Discussion History:</h4>
                <ul className="list-disc list-inside text-gray-700 mt-2">
                  {discussionData.history?.map((entry, index) => (
                    <li key={index}>
                      <strong>{entry.agent}:</strong> {entry.message}
                    </li>
                  ))}
                </ul>
              </div>
            ) : (
<p className="text-center text-gray-500">
  {loading_discussion ? (
    <span className="flex items-center justify-center">
      <svg className="animate-spin h-5 w-5 mr-2 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      Processing...
    </span>
  ) : (
    "Waiting for AI discussion results..."
  )}
</p>
            )}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section id="testimonials" className="py-16 px-6 max-w-5xl mx-auto text-center">
        <h2 className="text-3xl font-bold text-gray-800">What Our Clients Say</h2>
        <div className="grid md:grid-cols-2 gap-6 mt-8">
          <TestimonialCard name="Sarah L." text="This software revolutionized our lead generation process!" />
          <TestimonialCard name="John D." text="We saw a 40% increase in qualified leads within a month!" />
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="py-16 px-6 bg-gray-50">
        <h2 className="text-3xl font-bold text-center text-gray-800">💰 Pricing Plans</h2>
        <div className="grid md:grid-cols-3 gap-6 mt-8 max-w-4xl mx-auto">
          <PricingCard title="Starter" price="$19/mo" features={["Basic AI Analysis", "50 Leads/month"]} />
          <PricingCard title="Pro" price="$49/mo" features={["Advanced AI Scoring", "200 Leads/month"]} />
          <PricingCard title="Enterprise" price="Custom" features={["Unlimited Leads", "Custom AI Models"]} />
        </div>
      </section>

      {/* Contact */}
      <section id="contact" className="py-16 px-6 max-w-3xl mx-auto text-center">
        <h2 className="text-3xl font-bold text-gray-800">📩 Contact Us</h2>
        <p className="text-gray-600 mt-2">Have questions? Request a demo today!</p>
        <input
          type="email"
          placeholder="Enter your email"
          className="mt-4 p-3 w-full border text-black rounded-lg"
        />
        <button className="mt-4 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
          Request Demo
        </button>
      </section>
    </div>
  );
}