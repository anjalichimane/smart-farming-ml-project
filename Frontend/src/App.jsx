import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Contact from "./pages/Contact";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import CropRecommendation from "./pages/CropRecommendation";
import FertilizerRecommendation from "./pages/FertilizerRecommendation";
import DiseasePrediction from "./pages/DiseasePrediction";
import PrivacyPolicy from "./pages/PrivacyPolicy";
import TermsAndConditions from "./pages/TermsAndConditions";
import ProtectedRoute from "./components/ProtectedRoute";



export default function App(){
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-grow">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          {/* <Route path="/crop" element={<CropRecommendation />} />
          <Route path="/fertilizer" element={<FertilizerRecommendation />} />
          <Route path="/disease" element={<DiseasePrediction />} /> */}

          <Route
  path="/crop"
  element={
    <ProtectedRoute>
      <CropRecommendation />
    </ProtectedRoute>
  }
/>

<Route
  path="/fertilizer"
  element={
    <ProtectedRoute>
      <FertilizerRecommendation />
    </ProtectedRoute>
  }
/>

<Route
  path="/disease"
  element={
    <ProtectedRoute>
      <DiseasePrediction />
    </ProtectedRoute>
  }
/>




          <Route path="/contact" element={<Contact />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/privacy" element={<PrivacyPolicy />} />
          <Route path="/terms" element={<TermsAndConditions />} />
          <Route path="*" element={<div className="p-12 text-center">Page not found</div>} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}
