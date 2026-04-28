import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import signupBg from "../assets/signup_bg.jpeg";

export default function Signup() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false); // Track loading state
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await fetch("/api/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, email, password }),
      });

      const data = await res.json();

      if (res.ok) {
        // res.ok is true if status is 200-299
        alert(data.message || "Account created successfully! 🎉");
        navigate("/login");
      } else {
        // Handles errors like "Email already exists" or FastAPI validation errors
        alert(data.detail || data.message || "Registration failed. Please try again.");
      }
    } catch (error) {
      // Handles network errors (server down)
      console.error("Signup Error:", error);
      alert("Cannot connect to the server. Is your Python backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center bg-cover bg-center relative"
      style={{ backgroundImage: `url(${signupBg})` }}
    >
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>

      <div
        className="relative z-10 w-full max-w-md p-8 rounded-2xl
                   bg-white/20 backdrop-blur-xl
                   border border-white/30
                   shadow-[0_8px_32px_0_rgba(0,0,0,0.37)]
                   text-white animate-fadeIn"
      >
        <h2 className="text-3xl font-bold text-center mb-6">🌱 Create Account</h2>

        <form className="space-y-4" onSubmit={handleSignup}>
          <input
            type="text"
            placeholder="Full Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full px-4 py-3 rounded-lg bg-white/30 text-white placeholder-gray-200 focus:outline-none focus:ring-2 focus:ring-green-400 focus:bg-white/40 transition duration-300"
            required
            disabled={loading}
          />

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-3 rounded-lg bg-white/30 text-white placeholder-gray-200 focus:outline-none focus:ring-2 focus:ring-green-400 focus:bg-white/40 transition duration-300"
            required
            disabled={loading}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-3 rounded-lg bg-white/30 text-white placeholder-gray-200 focus:outline-none focus:ring-2 focus:ring-green-400 focus:bg-white/40 transition duration-300"
            required
            disabled={loading}
          />

          <button
            type="submit"
            disabled={loading}
            className={`w-full py-3 rounded-lg font-semibold shadow-lg transition duration-300 active:scale-95 ${
              loading ? "bg-gray-500 cursor-not-allowed" : "bg-green-600 hover:bg-green-700"
            }`}
          >
            {loading ? "Creating Account..." : "Create Account"}
          </button>
        </form>

        <p className="mt-4 text-sm text-center text-gray-200">
          Already have an account?{" "}
          <Link to="/login" className="font-semibold text-green-300 hover:text-green-400">
            Login
          </Link>
        </p>
      </div>
    </div>
  );
}