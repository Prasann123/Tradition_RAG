import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./index.css";
import App from "./App.tsx";
import Chat from "./Chat.tsx"; // Make sure this component exists
import TravelPlanner from "./components/Travel_Agent/travel_planner.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/Chat" element={<Chat />} />
        <Route path="/travel-agent" element={<TravelPlanner />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
