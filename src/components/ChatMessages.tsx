import React from "react";
import { clsx } from "clsx";

// Define a more specific type for sources to avoid using 'any'
type Source = {
  source_name: string;
  page_content: string;
  metadata: Record<string, unknown>; // Use unknown for better type safety
};

type Message = {
  id: number;
  type: "text" | "file" | "video";
  content: string;
  fileName?: string;
  isUser?: boolean; // Add this property
  sources?: Source[];
  answer_source: string;
};

const ChatMessages: React.FC<{
  messages: Message[];
  messagesEndRef: React.RefObject<HTMLDivElement | null>;
  theme: "light" | "dark";
}> = ({ messages, messagesEndRef, theme }) => {
  console.log("ChatMessages rendering with messages:", messages); // Debug log

  return (
    <div
      className={clsx(
        "flex-1 overflow-y-auto px-6 py-6",
        theme === "dark" ? "bg-gray-950" : "bg-blue-50"
      )}
    >
      {messages.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-full text-gray-400 space-y-4">
          <span className="text-5xl">💬</span>
          <p className="text-xl font-medium">
            Your conversation will appear here
          </p>
          <p>Upload content or ask a question to get started</p>
        </div>
      ) : (
        messages.map((msg) => {
          // Determine if message is from user based on type or explicit flag
          const isUser =
            msg.isUser !== undefined
              ? msg.isUser
              : msg.type === "file" || msg.type === "video";

          return (
            <div
              key={msg.id}
              className={`flex items-end mb-4 ${
                isUser ? "justify-end" : "justify-start"
              } w-full`}
            >
              <div
                className={clsx(
                  "max-w-xs lg:max-w-md px-4 py-2 rounded-lg",
                  isUser
                    ? theme === "dark"
                      ? "bg-blue-600 text-white"
                      : "bg-blue-500 text-white"
                    : theme === "dark"
                    ? "bg-gray-700 text-white"
                    : "bg-white text-gray-900 shadow"
                )}
              >
                {msg.type === "text" ? (
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                ) : msg.type === "file" ? (
                  <div>
                    <p>📄 {msg.fileName}</p>
                  </div>
                ) : (
                  <div>
                    <p>🎥 {msg.fileName}</p>
                  </div>
                )}
                {/* Add this block to render the sources */}
             
                {/* Show answer source if available */}
                {msg.answer_source && (
                  <div className="mt-1 text-xs text-right text-gray-400 italic">
                    Answer source: {msg.answer_source}
                  </div>
                )}
              </div>
            </div>
          );
        })
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatMessages;
