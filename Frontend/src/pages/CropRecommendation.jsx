
import React, { useState } from "react";
import bgImage from "../assets/crop_bg.jpeg";

const API_BASE = "http://127.0.0.1:8000";

export default function CropRecommendation() {
  const [form, setForm] = useState({
    nitrogen: "",
    phosphorus: "",
    potassium: "",
    temperature: "",
    humidity: "",
    ph: "",
    rainfall: "",
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    for (const key of Object.keys(form)) {
      if (form[key] === "") {
        alert(`Please enter ${key}`);
        return;
      }
    }

    const payload = {
      N: parseFloat(form.nitrogen),
      P: parseFloat(form.phosphorus),
      K: parseFloat(form.potassium),
      temperature: parseFloat(form.temperature),
      humidity: parseFloat(form.humidity),
      ph: parseFloat(form.ph),
      rainfall: parseFloat(form.rainfall),
    };

    try {
      setLoading(true);
      setResult(null);

      const res = await fetch(`${API_BASE}/predict/crop`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      alert("Crop prediction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center bg-cover bg-center relative"
      style={{ backgroundImage: `url(${bgImage})` }}
    >
      {/* Dark Overlay */}
      <div className="absolute inset-0 bg-black/60"></div>

      <div className="relative z-10 bg-white/90 backdrop-blur-lg shadow-2xl rounded-3xl p-8 w-full max-w-2xl transition hover:scale-[1.01] duration-300">

        <h1 className="text-3xl font-bold text-green-800 text-center mb-6">
          🌾 Crop Recommendation
        </h1>

        <form onSubmit={handleSubmit} className="space-y-5">

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">

            {[
              { label: "Nitrogen (N)", name: "nitrogen", placeholder: "e.g. 90" },
              { label: "Phosphorus (P)", name: "phosphorus", placeholder: "e.g. 40" },
              { label: "Potassium (K)", name: "potassium", placeholder: "e.g. 40" },
              { label: "Temperature (°C)", name: "temperature", placeholder: "e.g. 25" },
              { label: "Humidity (%)", name: "humidity", placeholder: "e.g. 80" },
              { label: "Soil pH", name: "ph", placeholder: "e.g. 6.5" },
            ].map((field) => (
              <div key={field.name}>
                <label className="block text-sm font-semibold mb-1">
                  {field.label}
                </label>
                <input
                  type="number"
                  name={field.name}
                  value={form[field.name]}
                  onChange={handleChange}
                  placeholder={field.placeholder}
                  step="any"
                  required
                  className="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-green-600 focus:outline-none"
                />
              </div>
            ))}

            <div className="sm:col-span-2">
              <label className="block text-sm font-semibold mb-1">
                Rainfall (mm)
              </label>
              <input
                type="number"
                name="rainfall"
                value={form.rainfall}
                onChange={handleChange}
                placeholder="e.g. 200"
                step="any"
                required
                className="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-green-600 focus:outline-none"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-green-600 hover:bg-green-700 hover:scale-105 transition transform text-white py-3 rounded-lg font-semibold shadow-md"
          >
            {loading ? "Predicting..." : "Predict Crop"}
          </button>
        </form>

        {result && (
          <div className="mt-6 p-5 bg-green-100 border border-green-300 rounded-xl text-center shadow">
            <h3 className="text-lg font-semibold text-green-800">Prediction Result</h3>
            <p className="mt-2">
              Recommended Crop: <strong>{result.prediction}</strong>
            </p>
            <p>
              Confidence: <strong>{result.confidence}%</strong>
            </p>
          </div>
        )}
      </div>
    </div>
  );
}