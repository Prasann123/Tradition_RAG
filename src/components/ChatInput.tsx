import React from "react";
import { clsx } from "clsx";

const ChatInput: React.FC<{
  input: string;
  setInput: (v: string) => void;
  handleSend: () => void;
  theme: "light" | "dark";
}> = ({ input, setInput, handleSend, theme }) => (
  <div
    className={clsx(
      "w-full border-t p-4 flex items-center gap-3",
      theme === "dark"
        ? "bg-gray-900 border-gray-700"
        : "bg-white border-gray-200"
    )}
  >
    <input
      type="text"
      className={clsx(
        "flex-1 rounded-full px-5 py-2 focus:outline-none focus:ring-2",
        theme === "dark"
          ? "bg-gray-800 border border-gray-700 text-white focus:ring-blue-900 placeholder-gray-400"
          : "border border-gray-300 text-gray-900 focus:ring-blue-300"
      )}
      placeholder="Type your message here..."
      value={input}
      onChange={(e) => setInput(e.target.value)}
      onKeyDown={(e) => e.key === "Enter" && handleSend()}
    />
    <button
      onClick={handleSend}
      className={clsx(
        "px-5 py-2 rounded-full transition shadow-md flex items-center justify-center gap-2",
        theme === "dark"
          ? "bg-blue-700 text-white hover:bg-blue-800"
          : "bg-gradient-to-r from-blue-500 to-blue-600 text-white hover:from-blue-600 hover:to-blue-700"
      )}
      aria-label="Send message"
      type="button"
    >
      Send
      {/* ...svg icon... */}
    </button>
  </div>
);

export default ChatInput;
