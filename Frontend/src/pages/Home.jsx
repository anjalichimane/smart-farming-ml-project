
import React from "react";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  const handleExploreClick = () => {
    navigate("/dashboard");
  };

  return (
    <section
      className="relative h-screen flex flex-col items-center justify-center text-center text-white"
      style={{
        backgroundImage:
          "url('https://cdn.pixabay.com/photo/2024/07/26/11/49/ai-generated-8923423_1280.jpg')",
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      {/* Dark overlay for text visibility */}
      <div className="absolute inset-0 bg-black opacity-60"></div>

      {/* Content */}
      <div className="relative z-10 px-6">
        <h1 className="text-5xl md:text-6xl font-bold mb-4">
          🌾 Welcome to <span className="text-green-400">AgroAI</span>
        </h1>
        <p className="text-xl md:text-2xl mb-6 max-w-2xl mx-auto">
          Empowering Farmers With Artificial Intelligence - For Smarter Crop Disease Detection, 
          Fertilizer Recommendation, Crop Recommendation And Sustainable Farming.
        </p>
        <button
          onClick={handleExploreClick}
          className="btn btn-success px-8 py-3 text-lg hover:scale-105 transition-transform duration-300"
        >
          Explore Features
        </button>
      </div>
    </section>
  );
};

export default Home;
