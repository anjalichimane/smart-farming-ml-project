import React from "react";
import { useNavigate } from "react-router-dom";

import cropImg from "../assets/crop.jpeg";
import fertilizerImg from "../assets/fertilizer.jpeg";
import diseaseImg from "../assets/disease.jpeg";
import dashboardBg from "../assets/dashboard_bg.jpeg";

export default function Dashboard() {
  const navigate = useNavigate();

  // const handleExplore = (path) => {
  //   const user = localStorage.getItem("user");
  //   if (user) {
  //     navigate(path);
  //   } else {
  //     navigate("/login");
  //   }
  // };



  const handleExplore = (path) => {
  const token = localStorage.getItem("token");
  if (token) {
    navigate(path);
  } else {
    navigate("/login");
  }
};




  return (
    <div
      className="relative min-h-screen bg-cover bg-center flex items-center"
      style={{ backgroundImage: `url(${dashboardBg})` }}
    >
      {/* 🔥 Cinematic Gradient Overlay (Softer & Premium) */}
      <div className="absolute inset-0 bg-gradient-to-br from-green-900/60 via-green-800/40 to-black/40"></div>

      {/* Content */}
      <div className="relative z-10 w-full py-20 px-6 md:px-20">
        <h1 className="text-4xl md:text-5xl font-bold text-white text-center mb-16 tracking-wide">
          AgroAI Dashboard
        </h1>

        <div className="grid md:grid-cols-3 gap-10">

          {/* Crop Recommendation */}
          <div className="bg-white/90 backdrop-blur-md shadow-2xl rounded-2xl overflow-hidden hover:scale-105 hover:shadow-green-900/30 transition-all duration-300">
            <img
              src={cropImg}
              alt="Crop"
              className="h-56 w-full object-cover"
            />
            <div className="p-6">
              <h2 className="text-2xl font-semibold text-green-700 mb-2">
                Crop Recommendation
              </h2>
              <p className="text-gray-600 mb-4">
                Model based crop suggestions.
              </p>
              <button
                onClick={() => handleExplore("/crop")}
                className="w-full py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 hover:scale-105 transition-all duration-300"
              >
                Explore
              </button>
            </div>
          </div>

          {/* Fertilizer Recommendation */}
          <div className="bg-white/90 backdrop-blur-md shadow-2xl rounded-2xl overflow-hidden hover:scale-105 hover:shadow-green-900/30 transition-all duration-300">
            <img
              src={fertilizerImg}
              alt="Fertilizer"
              className="h-56 w-full object-cover"
            />
            <div className="p-6">
              <h2 className="text-2xl font-semibold text-green-700 mb-2">
                Fertilizer Recommendation
              </h2>
              <p className="text-gray-600 mb-4">
                Smart fertilizer suggestions.
              </p>
              <button
                onClick={() => handleExplore("/fertilizer")}
                className="w-full py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 hover:scale-105 transition-all duration-300"
              >
                Explore
              </button>
            </div>
          </div>

          {/* Disease Prediction */}
          <div className="bg-white/90 backdrop-blur-md shadow-2xl rounded-2xl overflow-hidden hover:scale-105 hover:shadow-green-900/30 transition-all duration-300">
            <img
              src={diseaseImg}
              alt="Disease"
              className="h-56 w-full object-cover"
            />
            <div className="p-6">
              <h2 className="text-2xl font-semibold text-green-700 mb-2">
                Disease Detection
              </h2>
              <p className="text-gray-600 mb-4">
                Upload a crop image for disease check.
              </p>
              <button
                onClick={() => handleExplore("/disease")}
                className="w-full py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 hover:scale-105 transition-all duration-300"
              >
                Explore
              </button>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}