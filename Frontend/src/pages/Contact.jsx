import React from "react";
import bgImage from "../assets/login_bg.jpeg"; // same background as login

export default function Contact() {
  return (
    <div
      className="min-h-screen flex items-center justify-center bg-cover bg-center relative"
      style={{ backgroundImage: `url(${bgImage})` }}
    >
      {/* Dark Overlay */}
      <div className="absolute inset-0 bg-black/60"></div>

      {/* Glass Card */}
      <div className="relative z-10 w-full max-w-2xl bg-white/90 backdrop-blur-lg rounded-3xl shadow-2xl p-10">

        {/* Heading */}
        <h2 className="text-3xl font-bold text-center mb-6 text-green-800">
          🌿 Contact AgroAI
        </h2>

        <p className="text-center text-gray-600 mb-8">
          Have questions about crop, fertilizer, or disease prediction?
          We’re happy to help.
        </p>

        {/* Form */}
        <form className="space-y-5">

          <input
            type="text"
            placeholder="Enter your name"
            className="w-full border border-gray-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-green-500"
            required
          />

          <input
            type="email"
            placeholder="Enter your email"
            className="w-full border border-gray-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-green-500"
            required
          />

          <textarea
            rows="5"
            placeholder="Write your message..."
            className="w-full border border-gray-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-green-500"
            required
          ></textarea>

          <button
            type="submit"
            className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-semibold transition duration-300"
          >
            Send Message
          </button>
        </form>

      </div>
    </div>
  );
}