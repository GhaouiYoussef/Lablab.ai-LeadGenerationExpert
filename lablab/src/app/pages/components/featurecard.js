const FeatureCard = ({ title, desc, children }) => (

    <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition cursor-pointer">
      <p className="text-blue-600 mt-2">Learn More →</p>
      {children}
      <p className="text-gray-600 mt-2">{desc}</p>
      <p className="text-blue-600 mt-2">Learn More →</p>
    </div>
);