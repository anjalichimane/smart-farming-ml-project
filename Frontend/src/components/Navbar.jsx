
import React, { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

const NavLink = ({ to, label, active, onClick }) => (
  <button
    onClick={onClick}
    className={`px-3 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
      active
        ? "bg-white/10 text-white ring-1 ring-white/20"
        : "text-white/90 hover:bg-white/5"
    }`}
  >
    {label}
  </button>
);

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const { pathname } = useLocation();
  const navigate = useNavigate();

  const token = localStorage.getItem("token");
  const userName = localStorage.getItem("userName");

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("userName");
    navigate("/login");
  };

  const handleProtectedNav = (path) => {
    if (token) {
      navigate(path);
    } else {
      navigate("/login");
    }
  };

  return (
    <header className="sticky top-0 z-50">
      <nav className="backdrop-blur-md bg-green-800/85 border-b border-white/5 shadow-navbar">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">

            {/* LEFT SECTION */}
            <div className="flex items-center gap-4">
              <Link to="/" className="flex items-center gap-2">
                <span className="inline-flex items-center justify-center w-10 h-10 bg-white/10 rounded-full text-lg font-bold">🌱</span>
                <div className="flex flex-col leading-none">
                  <span className="text-white text-lg font-semibold tracking-wide">AgroAI</span>
                  <span className="text-xs text-white/70 -mt-0.5">Smart Farming</span>
                </div>
              </Link>
            </div>

            {/* CENTER LINKS */}
            <div className="hidden md:flex md:items-center md:space-x-4 lg:space-x-6">
              <Link to="/" className="text-white/90 hover:bg-white/5 px-3 py-2 rounded-md">
                Home
              </Link>

              <Link to="/dashboard" className="text-white/90 hover:bg-white/5 px-3 py-2 rounded-md">
                Dashboard
              </Link>

              <NavLink
                label="Crop"
                active={pathname.startsWith("/crop")}
                onClick={() => handleProtectedNav("/crop")}
              />

              <NavLink
                label="Fertilizer"
                active={pathname.startsWith("/fertilizer")}
                onClick={() => handleProtectedNav("/fertilizer")}
              />

              <NavLink
                label="Disease"
                active={pathname.startsWith("/disease")}
                onClick={() => handleProtectedNav("/disease")}
              />

              <Link to="/contact" className="text-white/90 hover:bg-white/5 px-3 py-2 rounded-md">
                Contact
              </Link>
            </div>

            {/* RIGHT SECTION */}
            <div className="hidden md:flex items-center gap-3">

              {!token ? (
                <>
                  <Link
                    to="/login"
                    className="px-3 py-2 text-white/90 hover:bg-white/5 rounded-md"
                  >
                    Log in
                  </Link>

                  <Link
                    to="/signup"
                    className="px-4 py-2 rounded-full bg-white text-green-800 font-semibold"
                  >
                    Sign up
                  </Link>
                </>
              ) : (
                <>
                  <span className="text-white/90 font-medium">
                    👋 {userName}
                  </span>

                  <button
                    onClick={handleLogout}
                    className="px-4 py-2 rounded-full bg-white text-green-800 font-semibold"
                  >
                    Logout
                  </button>
                </>
              )}

            </div>

          </div>
        </div>
      </nav>
    </header>
  );
}