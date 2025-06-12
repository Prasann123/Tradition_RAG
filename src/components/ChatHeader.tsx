import React from "react";
import { clsx } from "clsx";

const ChatHeader: React.FC<{ theme: "light" | "dark" }> = ({ theme }) => (
  <div
    className={clsx(
      "flex items-center px-6 py-4 border-b",
      theme === "dark"
        ? "bg-gray-800 border-gray-700"
        : "bg-blue-600 border-blue-700"
    )}
  >
    <span
      className={clsx(
        "inline-flex items-center justify-center w-10 h-10 rounded-full text-xl font-bold mr-3",
        theme === "dark"
          ? "bg-gray-900 text-blue-400"
          : "bg-white text-blue-600"
      )}
    >
      🤖
    </span>
    <span className="font-bold text-xl text-white">RAG Assistant</span>
    <span
      className={clsx(
        "ml-auto text-sm",
        theme === "dark" ? "text-gray-300" : "text-white"
      )}
    >
      {new Date().toLocaleDateString()}
    </span>
  </div>
);

export default ChatHeader;
