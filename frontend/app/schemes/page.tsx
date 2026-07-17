"use client";

import { useState } from "react";

type Scheme = {
  scheme_name: string;
  state: string;
  crop_type: string;
  benefits: string;
  documents_required: string[];
  apply_link: string;
};

export default function SchemesPage() {
  const [state, setState] = useState("Kerala");
  const [crop, setCrop] = useState("Paddy");
  const [incomeCategory, setIncomeCategory] = useState("Small and Marginal Farmers");
  const [schemes, setSchemes] = useState<Scheme[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const findSchemes = async () => {
    setLoading(true);
    setSearched(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/schemes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          state,
          crop,
          land_size_category: "Any",
          income_category: incomeCategory,
        }),
      });

      const data = await response.json();
      setSchemes(data.schemes);
    } catch (error) {
      setSchemes([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-1 text-center">
        🏛️ Government Scheme Recommender
      </h1>
      <p className="text-gray-500 text-center mb-6">
        Find schemes you may be eligible for
      </p>

      {/* Form */}
      <div className="bg-gray-50 border rounded-lg p-5 mb-6 space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1 text-gray-800">State</label>
          <select
            value={state}
            onChange={(e) => setState(e.target.value)}
            className="w-full border rounded px-3 py-2 text-gray-900 bg-white"
          >
            <option value="Kerala">Kerala</option>
            <option value="Tamil Nadu">Tamil Nadu</option>
            <option value="Karnataka">Karnataka</option>
            <option value="Andhra Pradesh">Andhra Pradesh</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1 text-gray-800">Crop</label>
          <select
            value={crop}
            onChange={(e) => setCrop(e.target.value)}
            className="w-full border rounded px-3 py-2 text-gray-900 bg-white"
          >
            <option value="Paddy">Paddy</option>
            <option value="Coconut">Coconut</option>
            <option value="Oilseeds">Oilseeds</option>
            <option value="Vegetables">Vegetables</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1 text-gray-800">Income Category</label>
          <select
            value={incomeCategory}
            onChange={(e) => setIncomeCategory(e.target.value)}
            className="w-full border rounded px-3 py-2 text-gray-900 bg-white"
          >
            <option value="Small and Marginal Farmers">
              Small and Marginal Farmers
            </option>
            <option value="All Farmers">All Farmers</option>
          </select>
        </div>

        <button
          onClick={findSchemes}
          disabled={loading}
          className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 disabled:opacity-50"
        >
          {loading ? "Searching..." : "Find Eligible Schemes"}
        </button>
      </div>

      {/* Results */}
      {searched && !loading && (
        <div>
          <p className="text-gray-600 mb-3">{schemes.length} scheme(s) found</p>
          <div className="space-y-4">
            {schemes.map((scheme, idx) => (
              <div key={idx} className="border rounded-lg p-4 bg-white shadow-sm">
                <h3 className="font-bold text-lg text-green-700">
                  {scheme.scheme_name}
                </h3>
                <p className="text-gray-700 my-2">{scheme.benefits}</p>
                <p className="text-sm text-gray-500 mb-2">
                  <span className="font-medium">Documents needed:</span>{" "}
                  {scheme.documents_required.join(", ")}
                </p>
                <a
                  href={scheme.apply_link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 text-sm underline"
                >
                  Apply / Learn more →
                </a>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}