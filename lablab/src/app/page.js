"use client";
import { useState } from "react";
import AgentsDiscussion from "./pages/agents-discussion/page";
import Link from "next/link";

// 📌 NavBar Component
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

export default function Home() {
  return (
    <div className="bg-gray-100 min-h-screen">
      <NavBar />
      {/* 🌟 Hero Section */}
      <section id="hero" className="bg-blue-600 text-white text-center py-20 px-4">
        <h1 className="text-5xl font-bold">🚀 AI-Powered Lead Generation</h1>
        <p className="mt-4 text-lg">Let AI find and analyze your ideal clients in seconds.</p>
        <button className="mt-6 px-6 py-3 bg-white text-blue-600 font-bold rounded-lg hover:bg-gray-200 transition">
          Get Started
        </button>
      </section>

      {/* 🔥 Features Section */}
      <section id="features" className="py-16 px-6 max-w-5xl mx-auto text-center">
        <h2 className="text-3xl font-bold text-gray-800">Why Choose Our AI?</h2>
        <div className="grid md:grid-cols-3 gap-6 mt-8">
          <FeatureCard title="🎯 Smart Targeting" link="pages/smart-targeting" desc="Our AI analyzes market data to find the best leads for your business." />
          <FeatureCard title="🤖 Automated Outreach" link="pages/automated-outreach" desc="Automate outreach with AI-driven conversations and engagement."/>
          <FeatureCard title="📊 Data Insights" link="pages/data-insights"  desc="Get real-time analytics on lead quality and conversion rates."/>
        </div>
      </section>

      {/* 💬 Live AI Discussion */}
      <section id="discussion" className="py-16 px-6 bg-gray-50">
        <h2 className="text-3xl font-bold text-center text-gray-800">🤖 AI-Powered Decision Making</h2>
        <p className="text-center text-gray-600 mt-2">Watch two AI agents debate lead quality before you make a decision.</p>
        <div className="mt-6">
          <AgentsDiscussion />
        </div>
      </section>

      {/* ⭐ Testimonials */}
      <section id="testimonials" className="py-16 px-6 max-w-5xl mx-auto text-center">
        <h2 className="text-3xl font-bold text-gray-800">What Our Clients Say</h2>
        <div className="grid md:grid-cols-2 gap-6 mt-8">
          <TestimonialCard name="Sarah L." text="This software revolutionized our lead generation process!" />
          <TestimonialCard name="John D." text="We saw a 40% increase in qualified leads within a month!" />
        </div>
      </section>

      {/* 💰 Pricing */}
      <section id="pricing" className="py-16 px-6 bg-gray-50">
        <h2 className="text-3xl font-bold text-center text-gray-800">💰 Pricing Plans</h2>
        <div className="grid md:grid-cols-3 gap-6 mt-8 max-w-4xl mx-auto">
          <PricingCard title="Starter" price="$19/mo" features={["Basic AI Analysis", "50 Leads/month"]} />
          <PricingCard title="Pro" price="$49/mo" features={["Advanced AI Scoring", "200 Leads/month"]} />
          <PricingCard title="Enterprise" price="Custom" features={["Unlimited Leads", "Custom AI Models"]} />
        </div>
      </section>

      {/* 📩 Contact */}
      <section id="contact" className="py-16 px-6 max-w-3xl mx-auto text-center">
        <h2 className="text-3xl font-bold text-gray-800">📩 Contact Us</h2>
        <p className="text-gray-600 mt-2">Have questions? Request a demo today!</p>
        <input
          type="email"
          placeholder="Enter your email"
          className="mt-4 p-3 w-full border rounded-lg"
        />
        <button className="mt-4 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
          Request Demo
        </button>
      </section>
    </div>
  );
}

const FeatureCard = ({ title, link, desc }) => (
  <Link href={link}>
    <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition cursor-pointer">
      <h3 className="text-xl font-bold text-gray-800">{title}</h3>
      <p className="text-gray-600 mt-2">{desc}</p>
      <p className="text-blue-600 mt-2">Learn More →</p>
    </div>
  </Link>
);

// 📌 Testimonial Card
const TestimonialCard = ({ name, text }) => (
  <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition">
    <p className="text-gray-600 italic">"{text}"</p>
    <h4 className="mt-3 text-gray-800 font-bold">{name}</h4>
  </div>
);

// 📌 Pricing Card
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