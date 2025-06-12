import React from "react";
import { clsx } from "clsx";

const ThemeToggle: React.FC<{
  theme: "light" | "dark";
  toggleTheme: () => void;
}> = ({ theme, toggleTheme }) => (
  <button
    onClick={toggleTheme}
    className={clsx(
      "fixed top-4 right-4 z-50 px-3 py-1 rounded-full text-sm font-medium shadow transition",
      theme === "dark"
        ? "bg-gray-800 text-white hover:bg-gray-700 border border-gray-700"
        : "bg-gray-200 text-gray-800 hover:bg-gray-300 border border-gray-300"
    )}
    aria-label="Toggle theme"
    type="button"
  >
    {theme === "dark" ? "🌙 Dark" : "☀️ Light"}
  </button>
);

export default ThemeToggle;
