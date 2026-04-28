import React, { useState } from "react";
import bgImage from "../assets/fertilizer_bg.jpeg";

// Define the Backend URL
const API_BASE = "http://127.0.0.1:8000";

export default function FertilizerRecommendation() {
  const [formData, setFormData] = useState({
    district: "",
    soilColor: "",
    nitrogen: "",
    phosphorous: "", // Note: mapping this to 'Phosphorus' in the payload
    potassium: "",
    ph: "",
    rainfall: "",
    temperature: "",
    crop: "",
  });

  // NEW: States for API handling
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setPrediction(null);

    // Check if any field is empty
    const isEmpty = Object.values(formData).some(
      (value) => String(value).trim() === ""
    );

    if (isEmpty) {
      setError("⚠ Please fill all the fields before getting recommendation.");
      setLoading(false);
      return;
    }

    // Helper to ensure input matches the training data casing (e.g., "Black")
    const toTitleCase = (str) => 
      str ? str.charAt(0).toUpperCase() + str.slice(1).toLowerCase() : "";

    // CRITICAL: Constructing the payload exactly as the FastAPI Model expects
    const payload = {
      District_Name: toTitleCase(formData.district),
      Soil_color: toTitleCase(formData.soilColor),
      Nitrogen: parseFloat(formData.nitrogen),
      Phosphorus: parseFloat(formData.phosphorous), // Backend uses 'Phosphorus'
      Potassium: parseFloat(formData.potassium),
      pH: parseFloat(formData.ph),
      Rainfall: parseFloat(formData.rainfall),
      Temperature: parseFloat(formData.temperature),
      Crop: toTitleCase(formData.crop)
    };

    try {
      const response = await fetch(`${API_BASE}/predict/fertilizer`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok) {
        // Assuming your backend returns { "prediction": "Urea", "status": "success" }
        setPrediction(data.prediction);
      } else {
        setError("Model Error: " + (data.detail || "Prediction failed"));
      }
    } catch (err) {
      console.error("Connection Error:", err);
      setError("Could not connect to the backend server. Is it running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-[90vh] flex items-center justify-center bg-cover bg-center relative"
      style={{ backgroundImage: `url(${bgImage})` }}
    >
      {/* Dark Overlay */}
      <div className="absolute inset-0 bg-black/60"></div>

      <div className="relative z-10 bg-white/90 backdrop-blur-lg rounded-3xl shadow-2xl w-full max-w-4xl p-6 transition hover:scale-[1.01] duration-300">

        <h1 className="text-2xl font-bold text-center text-green-800 mb-3">
          🌱 Fertilizer Recommendation
        </h1>

        <p className="text-center text-gray-600 mb-5 text-sm">
          Enter soil and crop parameters to get the best fertilizer suggestion.
        </p>

        <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">

          {/* District */}
          <div>
            <label className="block font-medium mb-1 text-sm">District Name</label>
            <input
              type="text"
              name="district"
              value={formData.district}
              onChange={handleChange}
              placeholder="Enter district name"
              className="w-full border border-gray-300 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-green-500 outline-none"
            />
          </div>

          {/* Soil Color */}
          <div>
            <label className="block font-medium mb-1 text-sm">Soil Color</label>
            <select
              name="soilColor"
              value={formData.soilColor}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-green-500 outline-none"
            >
              <option value="">Select Soil Color</option>
              <option value="Black">Black</option>
              <option value="Red">Red</option>
              <option value="Brown">Brown</option>
              <option value="Yellow">Yellow</option>
            </select>
          </div>

          {/* Nitrogen */}
          <div>
            <label className="block font-medium mb-1 text-sm">Nitrogen (N)</label>
            <input
              type="number"
              name="nitrogen"
              value={formData.nitrogen}
              onChange={handleChange}
              placeholder="Enter Nitrogen value"
              className="w-full border border-gray-300 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-green-500 outline-none"
            />
          </div>

          {/* Phosphorous */}
          <div>
            <label className="block font-medium mb-1 text-sm">Phosphorous (P)</label>
            <input
              type="number"
              name="phosphorous"
              value={formData.phosphorous}
              onChange={handleChange}
              placeholder="Enter Phosphorous value"
              className="w-full border border-gray-300 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-green-500 outline-none"
            />
          </div>

          {/* Potassium */}
          <div>
            <label className="block font-medium mb-1 text-sm">Potassium (K)</label>
            <input
              type="number"
              name="potassium"
              value={formData.potassium}
              onChange={handleChange}
              placeholder="Enter Potassium value"
              className="w-full border border-gray-300 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-green-500 outline-none"
            />
          </div>

          {/* pH */}
          <div>
            <label className="block font-medium mb-1 text-sm">pH Value</label>
            <input
              type="number"
              step="0.1"
              name="ph"
              value={formData.ph}
              onChange={handleChange}
              placeholder="Enter pH value"
              className="w-full border border-gray-300 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-green-500 outline-none"
            />
          </div>

          {/* Rainfall */}
          <div>
            <label className="block font-medium mb-1 text-sm">Rainfall (mm)</label>
            <input
              type="number"
              name="rainfall"
              value={formData.rainfall}
              onChange={handleChange}
              placeholder="Enter rainfall"
              className="w-full border border-gray-300 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-green-500 outline-none"
            />
          </div>

          {/* Temperature */}
          <div>
            <label className="block font-medium mb-1 text-sm">Temperature (°C)</label>
            <input
              type="number"
              name="temperature"
              value={formData.temperature}
              onChange={handleChange}
              placeholder="Enter temperature"
              className="w-full border border-gray-300 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-green-500 outline-none"
            />
          </div>

          {/* Crop */}
          <div className="md:col-span-2">
            <label className="block font-medium mb-1 text-sm">Crop</label>
            <select
              name="crop"
              value={formData.crop}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-green-500 outline-none"
            >
              <option value="">Select Crop</option>
              <option value="Wheat">Wheat</option>
              <option value="Rice">Rice</option>
              <option value="Maize">Maize</option>
              <option value="Cotton">Cotton</option>
              <option value="Sugarcane">Sugarcane</option>
            </select>
          </div>

          {/* Button */}
          <div className="md:col-span-2 flex justify-center mt-4">
            <button
              type="submit"
              disabled={loading}
              className="bg-green-600 hover:bg-green-700 hover:scale-105 transition transform text-white px-8 py-2 rounded-xl font-semibold shadow-lg text-sm disabled:bg-gray-400"
            >
              {loading ? "Processing..." : "Get Recommendation"}
            </button>
          </div>
        </form>

        {/* Display Prediction Result */}
        {prediction && (
          <div className="mt-6 p-4 bg-green-100 border-l-8 border-green-600 rounded-xl text-center shadow-inner animate-bounce-short">
            <h2 className="text-lg font-bold text-green-800">Recommended Fertilizer:</h2>
            <p className="text-3xl font-black text-green-900 uppercase tracking-tighter">
              {prediction}
            </p>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mt-4 bg-red-100 border border-red-300 rounded-xl p-3 text-center text-red-700 text-sm">
            {error}
          </div>
        )}

      </div>
    </div>
  );
}