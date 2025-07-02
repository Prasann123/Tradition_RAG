import React, { useState, useRef, useEffect } from "react";
import { clsx } from "clsx";
import {
  invokeAgent,
  uploadFile,
  uploadText,
  scrapeWebsite,
} from "./services/api";
import type { AgentConfig } from "./services/api";
import toast, { Toaster } from "react-hot-toast";
// Make sure the file exists at the specified path, or update the path if necessary
import ChatMessages from "./components/ChatMessages";
import ChatInput from "./components/ChatInput";
import ChatSidebar from "./components/ChatSidebar";
import ChatHeader from "./components/ChatHeader";
import ThemeToggle from "./components/ThemeToggle";

// Define a more specific type for sources to avoid using 'any'
type Source = {
  source_name: string;
  page_content: string;
  metadata: Record<string, any>;
};

type Message = {
  id: number;
  type: "text" | "file" | "video";
  content: string;
  fileName?: string;
  isUser?: boolean;
  sources?: Source[];
  answer_source: string;
};

// Utility functions to create messages
const createUserMessage = (content: string): Message => ({
  id: Date.now(),
  type: "text",
  content,
  isUser: true,
  sources: [],
  answer_source: "",
});

const createBotMessage = (
  content: string,
  sources: Source[] = [],
  answer_source: string = ""
): Message => ({
  id: Date.now(),
  type: "text",
  content,
  isUser: false,
  sources,
  answer_source,
});

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [textUpload, setTextUpload] = useState("");
  const [scrapeUrl, setScrapeUrl] = useState("");
  const [theme, setTheme] = useState<"light" | "dark">("light");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [agentConfig, setAgentConfig] = useState<AgentConfig>({
    vectordb: "chroma",
    retriever_type: "vectorstore",
    parser_type: "recursive",
  });
  // Scroll to bottom on new message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    // Only add/remove the dark class on body for dark mode
    if (theme === "dark") {
      document.body.classList.add("dark");
      document.body.classList.remove("light");
    } else {
      document.body.classList.remove("dark");
      document.body.classList.add("light");
    }
  }, [theme]);

  const toggleTheme = () => setTheme((t) => (t === "light" ? "dark" : "light"));

  const handleSend = async () => {
    if (input.trim() === "") return;

    setMessages((prevMessages) => [...prevMessages, createUserMessage(input)]);

    // Save input before clearing it
    const userInput = input;
    setInput("");

    try {
      const response = await invokeAgent(userInput, agentConfig);
      setMessages((prevMessages) => [
        ...prevMessages,
        createBotMessage(
          response.final_answer || "Sorry, I couldn't find an answer.",
          response.sources || [],
          response.answer_source || ""
        ),
      ]);
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        createBotMessage("Sorry, there was an error processing your request."),
      ]);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const loadingToast = toast.loading("Uploading file...");
    const fileMsg: Message = {
      id: Date.now(),
      type: "file" as const,
      content: URL.createObjectURL(file),
      fileName: file.name,
      isUser: true,
      sources: [],
      answer_source: "",
    };
    setMessages((prev) => [...prev, fileMsg]);

    try {
      const response = await uploadFile(file, agentConfig);
      setMessages((prevMessages) => [
        ...prevMessages,
        createBotMessage(response.answer, [], response.answer_source || ""),
      ]);
      toast.success("File uploaded successfully!", { id: loadingToast });
    } catch (error) {
      console.error("Error uploading file:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        createBotMessage("Sorry, there was an error uploading your file."),
      ]);
      toast.error("Failed to upload file", { id: loadingToast });
    }
  };

  const handleTextUpload = async () => {
    if (textUpload.trim() === "") return;

    setMessages((prev) => [...prev, createUserMessage(textUpload)]);
    setTextUpload("");

    try {
      const response = await uploadText(textUpload, agentConfig);
      setMessages((prevMessages) => [
        ...prevMessages,
        createBotMessage(response.answer, [], response.answer_source || ""),
      ]);
    } catch (error) {
      console.error("Error uploading text:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        createBotMessage("Sorry, there was an error processing your text."),
      ]);
    }
  };

  const handleScrape = async () => {
    if (scrapeUrl.trim() === "") return;

    setMessages((prev) => [
      ...prev,
      createUserMessage(`Scraping site: ${scrapeUrl}...`),
    ]);
    setScrapeUrl("");

    try {
      const response = await scrapeWebsite(scrapeUrl, agentConfig);
      setMessages((prevMessages) => [
        ...prevMessages,
        createBotMessage(response.answer, [], response.answer_source || ""),
      ]);
    } catch (error) {
      console.error("Error scraping website:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        createBotMessage("Sorry, there was an error scraping the website."),
      ]);
    }
  };

  return (
    <div
      className={clsx(
        "fixed inset-0 flex items-center justify-center",
        // Remove explicit bg-black, rely on Tailwind's dark:bg-black
        "bg-gray-100",
        theme === "dark" && "dark:bg-black"
      )}
    >
      {" "}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 3000,
          style: {
            background: theme === "dark" ? "#374151" : "#ffffff",
            color: theme === "dark" ? "#ffffff" : "#000000",
          },
        }}
      />
      <ThemeToggle theme={theme} toggleTheme={toggleTheme} />
      <div
        className={clsx(
          "flex w-full max-w-4xl h-[90vh] rounded-xl shadow-xl overflow-hidden",
          "bg-white",
          theme === "dark" && "dark:bg-gray-900"
        )}
      >
        <div className={clsx("flex flex-col flex-1 min-w-0 h-full")}>
          <ChatHeader theme={theme} />
          <ChatMessages
            messages={messages}
            messagesEndRef={messagesEndRef}
            theme={theme}
          />
          <ChatInput
            input={input}
            setInput={setInput}
            handleSend={handleSend}
            theme={theme}
          />
        </div>
        <ChatSidebar
          theme={theme}
          handleFileUpload={handleFileUpload}
          handleTextUpload={handleTextUpload}
          handleScrape={handleScrape}
          textUpload={textUpload}
          setTextUpload={setTextUpload}
          scrapeUrl={scrapeUrl}
          setScrapeUrl={setScrapeUrl}
          agentConfig={agentConfig}
          setAgentConfig={setAgentConfig}
        />
      </div>
    </div>
  );
};

export default Chat;
