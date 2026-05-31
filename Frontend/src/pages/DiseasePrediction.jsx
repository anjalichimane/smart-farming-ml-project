import React, { useState } from "react";
import bgImage from "../assets/disease_bg.jpeg";

const DiseasePrediction = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    setSelectedImage(file);
    setResult("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedImage) {
      alert("Please upload an image before submitting!");
      return;
    }

    setLoading(true);
    setResult("");

    const formData = new FormData();
    // FIX: Changed "image_file" to "file" to match FastAPI backend parameter
    formData.append("file", selectedImage);

    const API_URL = "https://smart-farming-ml-project.onrender.com";

try {
  const response = await fetch(`${API_URL}/predict/disease`, {
    method: "POST",
    body: formData,
  });

      const data = await response.json();

      if (response.ok && data.prediction) {
        setResult(
          `Predicted Disease: ${data.prediction} (Confidence: ${data.confidence}%)`
        );
      } else {
        // Handle cases where the model returns an error or 422
        setResult("Error: " + (data.detail || "Prediction not available."));
      }
    } catch (error) {
      console.error(error);
      setResult("Server error! Ensure your Python backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center bg-cover bg-center relative"
      style={{
        backgroundImage: `url(${bgImage})`,
      }}
    >
      {/* Dark Overlay */}
      <div className="absolute inset-0 bg-black/60"></div>

      <div className="relative z-10 bg-white/90 backdrop-blur-lg shadow-2xl rounded-3xl w-full max-w-lg p-8 text-center transition duration-300 hover:scale-[1.02]">
        <h2 className="text-3xl font-bold text-green-800 mb-6">
          🌿 Disease Prediction
        </h2>

        <form onSubmit={handleSubmit} className="space-y-5">
          <label className="block text-gray-700 font-medium mb-1">
            Upload Crop Leaf Image
          </label>
          <input
            type="file"
            accept="image/*"
            onChange={handleImageUpload}
            className="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-green-600 focus:outline-none bg-white"
          />

          {selectedImage && (
            <div className="flex justify-center mt-4">
              <img
                src={URL.createObjectURL(selectedImage)}
                alt="Preview"
                className="rounded-xl shadow-md w-48 h-48 object-cover border-2 border-green-300"
              />
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-green-600 hover:bg-green-700 hover:scale-105 transition transform text-white font-semibold py-3 rounded-lg shadow-md disabled:bg-gray-400"
          >
            {loading ? "Analyzing Image..." : "Predict Disease"}
          </button>
        </form>

        {result && !loading && (
          <div className="mt-5 text-lg font-medium text-green-800 bg-green-100 p-4 rounded-xl border border-green-300 shadow-inner">
            {result}
          </div>
        )}
      </div>
    </div>
  );
};

export default DiseasePrediction;