import React from "react";
import { Link } from "react-router-dom";

export default function Footer(){
  return (
    <footer className="bg-green-800 text-white py-6 mt-10">
      <div className="max-w-6xl mx-auto px-6 text-center">
        <p className="text-lg font-semibold">🌾 AgroAI - Smart Farming</p>
        <p className="text-sm text-green-200 mt-2">Empowering farmers with AI-driven solutions.</p>
        <div className="flex justify-center gap-6 mt-4">
          <Link to="/privacy" className="hover:text-green-300">Privacy</Link>
          <Link to="/terms" className="hover:text-green-300">Terms</Link>
          <Link to="/contact" className="hover:text-green-300">Contact</Link>
        </div>
        <p className="mt-6 text-green-300 text-sm">© {new Date().getFullYear()} AgroAI. All rights reserved.</p>
      </div>
    </footer>
  );
}
