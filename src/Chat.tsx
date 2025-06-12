import React, { useState, useRef, useEffect } from "react";
import { clsx } from "clsx";
import {
  sendMessage,
  uploadFile,
  uploadVideo,
  uploadText,
  scrapeWebsite,
} from "./services/api";
import toast, { Toaster } from "react-hot-toast";
// Make sure the file exists at the specified path, or update the path if necessary
import ChatMessages from "./components/ChatMessages";
import ChatInput from "./components/ChatInput";
import ChatSidebar from "./components/ChatSidebar";
import ChatHeader from "./components/ChatHeader";
import ThemeToggle from "./components/ThemeToggle";

type Message = {
  id: number;
  type: "text" | "file" | "video";
  content: string;
  fileName?: string;
  isUser?: boolean; // Optional flag to indicate if the message is from the user
};

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [textUpload, setTextUpload] = useState("");
  const [scrapeUrl, setScrapeUrl] = useState("");
  const [theme, setTheme] = useState<"light" | "dark">("light");
  const [isUploading, setIsUploading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

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

    // Add user message to UI immediately
    const userMessage: Message = {
      id: Date.now(),
      type: "text",
      content: input,
      isUser: true,
    };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    // Save input before clearing it
    const userInput = input;
    setInput("");

    try {
      // Use the saved input
      const response = await sendMessage(userInput);

      let answerContent;
      if (response && response.answer) {
        if (typeof response.answer === "string") {
          answerContent = response.answer;
        } else if (
          typeof response.answer === "object" &&
          response.answer.answer
        ) {
          answerContent = response.answer.answer;
        } else {
          answerContent = "No answer received";
        }
      } else {
        answerContent =
          response.message || response.content || "No answer received";
      }
      // Add console log to debug
      console.log("Chat response:", response);
      console.log("Source doc:", response.answer?.source_doc);
      const botMessage: Message = {
        id: Date.now() + 1,
        type: "text",
        content: answerContent,
        isUser: false,
      };
      // Add bot response to UI
      console.log("Bot message to add:", botMessage);
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: Date.now(),
          type: "text",
          content: "Sorry, there was an error processing your request.",
        },
      ]);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Add file message to UI immediately
    setIsUploading(true);
    const loadingToast = toast.loading("Uploading file...");
    const fileMsg = {
      id: Date.now(),
      type: "file" as const,
      content: URL.createObjectURL(file),
      fileName: file.name,
    };
    setMessages([...messages, fileMsg]);

    try {
      // Upload file to FastAPI backend
      const response = await uploadFile(file);

      // Add bot response to UI
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: Date.now(),
          type: "text",
          content: response.answer,
          isUser: false,
        },
      ]);
      toast.success("File uploaded successfully!", { id: loadingToast });
    } catch (error) {
      console.error("Error uploading file:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: Date.now(),
          type: "text",
          content: "Sorry, there was an error uploading your file.",
        },
      ]);
      toast.error("Failed to upload file", { id: loadingToast });
    } finally {
      setIsUploading(false);
    }
  };

  const handleVideoUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Add video message to UI immediately
    const videoMsg = {
      id: Date.now(),
      type: "video" as const,
      content: URL.createObjectURL(file),
      fileName: file.name,
    };
    setMessages([...messages, videoMsg]);

    try {
      // Upload video to FastAPI backend
      const response = await uploadVideo(file);

      // Add bot response to UI
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: Date.now(),
          type: "text",
          content: response.answer,
          isUser: false,
        },
      ]);
    } catch (error) {
      console.error("Error uploading video:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: Date.now(),
          type: "text",
          content: "Sorry, there was an error uploading your video.",
        },
      ]);
    }
  };

  const handleTextUpload = async () => {
    if (textUpload.trim() === "") return;

    // Add text message to UI immediately
    const textMsg: Message = {
      id: Date.now(),
      type: "text",
      content: textUpload,
    };
    setMessages([...messages, textMsg]);
    setTextUpload("");

    try {
      // Upload text to FastAPI backend
      const response = await uploadText(textUpload);

      // Add bot response to UI
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: Date.now(),
          type: "text",
          content: response.answer,
          isUser: false,
        },
      ]);
    } catch (error) {
      console.error("Error uploading text:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: Date.now(),
          type: "text",
          content: "Sorry, there was an error processing your text.",
        },
      ]);
    }
  };

  const handleScrape = async () => {
    if (scrapeUrl.trim() === "") return;

    // Add scrape message to UI immediately
    const scrapeMsg: Message = {
      id: Date.now(),
      type: "text",
      content: `Scraping site: ${scrapeUrl}...`,
    };
    setMessages([...messages, scrapeMsg]);
    setScrapeUrl("");

    try {
      // Call FastAPI backend to scrape website
      const response = await scrapeWebsite(scrapeUrl);

      // Add bot response to UI
      setMessages((prevMessages) => [
        ...prevMessages,
        { id: Date.now(), type: "text", content: response.answer },
      ]);
    } catch (error) {
      console.error("Error scraping website:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: Date.now(),
          type: "text",
          content: "Sorry, there was an error scraping the website.",
        },
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
          handleVideoUpload={handleVideoUpload}
          handleTextUpload={handleTextUpload}
          handleScrape={handleScrape}
          textUpload={textUpload}
          setTextUpload={setTextUpload}
          scrapeUrl={scrapeUrl}
          setScrapeUrl={setScrapeUrl}
          isUploading={isUploading}
        />
      </div>
    </div>
  );
};

export default Chat;
