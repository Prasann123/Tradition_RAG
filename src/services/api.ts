import axios from "axios";

const API_URL = "http://localhost:5000"; // Your FastAPI server URL

export interface AgentConfig {
  vectordb?: "chroma" | "milvus";
  retriever_type?: "vectorstore" | "multi_query";
  parser_type?: "recursive" | "simple";
}

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const invokeAgent = async (query: string, config: AgentConfig) => {
  // Calls the correct backend endpoint with the correct data structure.
  const response = await api.post("api/invoke_agent", { query, config });
  return response.data;
};

export const uploadFile = async (file: File, config: AgentConfig) => {
  const formData = new FormData();
  formData.append("file", file);

  // Add config values to formData
  if (config.vectordb) {
    formData.append("vectordb", config.vectordb);
  }
  if (config.parser_type) {
    formData.append("parser_type", config.parser_type);
  }

  // Note: The backend route for this is likely under /api/ as well
  const response = await api.post("/api/upload-file", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const uploadText = async (text: string, config: AgentConfig) => {
  const response = await api.post("/api/upload-text", { text, config });
  return response.data;
};

export const scrapeWebsite = async (url: string, config: AgentConfig) => {
  const response = await api.post("/api/scrape", { url, config });
  return response.data;
};

export default api;
