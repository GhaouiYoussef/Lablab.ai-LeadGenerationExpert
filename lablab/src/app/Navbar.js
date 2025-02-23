import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="bg-indigo-600 p-4">
      <div className="max-w-6xl mx-auto flex justify-between items-center">
        <div className="text-white text-2xl font-bold">LeadGen AI</div>
        <div className="space-x-4">
          <Link href="/">
            <a className="text-white hover:text-gray-200">Home</a>
          </Link>
          <Link href="/smart-targeting">
            <a className="text-white hover:text-gray-200">Smart Targeting</a>
          </Link>
          <Link href="/automated-outreach">
            <a className="text-white hover:text-gray-200">Automated Outreach</a>
          </Link>
          <Link href="/data-insights">
            <a className="text-white hover:text-gray-200">Data Insights</a>
          </Link>
        </div>
      </div>
    </nav>
  );
}