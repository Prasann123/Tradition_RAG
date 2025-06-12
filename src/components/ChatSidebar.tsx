import React, { useRef, useState } from "react";
import { clsx } from "clsx";

// ...props typing...

const ChatSidebar: React.FC<{
  theme: "light" | "dark";
  handleFileUpload: (e: React.ChangeEvent<HTMLInputElement>) => void;
  handleVideoUpload: (e: React.ChangeEvent<HTMLInputElement>) => void;
  handleTextUpload: () => void;
  handleScrape: () => void;
  textUpload: string;
  setTextUpload: (v: string) => void;
  scrapeUrl: string;
  setScrapeUrl: (v: string) => void;
}> = ({
  theme,
  handleFileUpload,
  handleVideoUpload,
  handleTextUpload,
  handleScrape,
  textUpload,
  setTextUpload,
  scrapeUrl,
  setScrapeUrl,
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const videoInputRef = useRef<HTMLInputElement>(null);
  const [fileName, setFileName] = useState<string>("");
  const [videoName, setVideoName] = useState<string>("");

  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) setFileName(e.target.files[0].name);
    handleFileUpload(e);
  };
  const onVideoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) setVideoName(e.target.files[0].name);
    handleVideoUpload(e);
  };

  return (
    <aside
      className={clsx(
        "w-72 flex-shrink-0 flex flex-col border-l p-4 bg-gray-100 dark:bg-gray-800 border-gray-200 dark:border-gray-700 h-full"
      )}
    >
      <div className="space-y-5">
        <div className="flex flex-col gap-4">
          {/* File Upload */}
          <div>
            <label
              className={clsx(
                "block text-sm font-medium mb-2",
                theme === "dark" ? "text-gray-300" : "text-gray-700"
              )}
            >
              Upload a file
            </label>
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png,.mp4"
              onChange={onFileChange}
              className="hidden"
              aria-label="Upload a file"
            />
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className={clsx(
                "w-full rounded-md py-2 px-3 text-sm font-semibold transition-shadow flex items-center justify-between",
                theme === "dark"
                  ? "bg-gray-900 text-white border border-gray-700 hover:bg-gray-700"
                  : "bg-white text-gray-900 border border-gray-300 hover:bg-gray-200"
              )}
            >
              {fileName ? fileName : "Choose File"}
            </button>
          </div>
          {/* Video Upload */}
          <div>
   {/*          <label
              className={clsx(
                "block text-sm font-medium mb-2",
                theme === "dark" ? "text-gray-300" : "text-gray-700"
              )}
            >
              Upload a video
            </label>
            <input
              ref={videoInputRef}
              type="file"
              accept=".mp4,.mov,.avi"
              onChange={onVideoChange}
              className="hidden"
              aria-label="Upload a video"
            /> */}
  {/*           <button
              type="button"
              onClick={() => videoInputRef.current?.click()}
              className={clsx(
                "w-full rounded-md py-2 px-3 text-sm font-semibold transition-shadow flex items-center justify-between",
                theme === "dark"
                  ? "bg-gray-900 text-white border border-gray-700 hover:bg-gray-700"
                  : "bg-white text-gray-900 border border-gray-300 hover:bg-gray-200"
              )}
            >
              {videoName ? videoName : "Choose Video"}
            </button> */}
          </div>
          {/* Text Upload */}
          <div>
            <label
              className={clsx(
                "block text-sm font-medium mb-2",
                theme === "dark" ? "text-gray-300" : "text-gray-700"
              )}
            >
              Upload text
            </label>
            <textarea
              value={textUpload}
              onChange={(e) => setTextUpload(e.target.value)}
              className={clsx(
                "block w-full text-sm rounded-md shadow-sm focus:ring-2 focus:ring-blue-500",
                theme === "dark"
                  ? "bg-gray-900 border-gray-700 text-white placeholder-gray-500"
                  : "bg-white border-gray-300 text-gray-900 placeholder-gray-400"
              )}
              rows={3}
              placeholder="Paste your text content here"
              aria-label="Upload text content"
            />
            <button
              onClick={handleTextUpload}
              className={clsx(
                "mt-2 w-full rounded-md py-2 text-sm font-semibold transition-shadow",
                theme === "dark"
                  ? "bg-blue-700 text-white shadow-md hover:shadow-lg"
                  : "bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-md hover:shadow-lg"
              )}
              aria-label="Upload text"
              type="button"
            >
              Upload
            </button>
          </div>
          {/* URL Scrape */}
          <div>
            <label
              className={clsx(
                "block text-sm font-medium mb-2",
                theme === "dark" ? "text-gray-300" : "text-gray-700"
              )}
            >
              Scrape a website
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={scrapeUrl}
                onChange={(e) => setScrapeUrl(e.target.value)}
                className={clsx(
                  "flex-1 rounded-md shadow-sm text-sm focus:ring-2 focus:ring-blue-500",
                  theme === "dark"
                    ? "bg-gray-900 border-gray-700 text-white placeholder-gray-500"
                    : "bg-white border-gray-300 text-gray-900 placeholder-gray-400"
                )}
                placeholder="Enter website URL"
                aria-label="Scrape website URL"
              />
              <button
                onClick={handleScrape}
                className={clsx(
                  "px-4 py-2 rounded-md text-sm font-semibold transition-shadow",
                  theme === "dark"
                    ? "bg-blue-700 text-white shadow-md hover:shadow-lg"
                    : "bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-md hover:shadow-lg"
                )}
                aria-label="Scrape website"
                type="button"
              >
                Scrape
              </button>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default ChatSidebar;
