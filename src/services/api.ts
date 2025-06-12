import axios from "axios";

const API_URL = "http://localhost:5000"; // Your FastAPI server URL

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const sendMessage = async (message: string) => {
  const response = await api.post("/api/send-message", { message, search_type: "mmr" });
  return response.data;
};


export const uploadFile = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post("/api/upload-file", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const uploadVideo = async (video: File) => {
  const formData = new FormData();
  formData.append("file", video);

  const response = await api.post("/upload-video", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const uploadText = async (text: string) => {
  const response = await api.post("/upload-text", { text });
  return response.data;
};

export const scrapeWebsite = async (url: string) => {
  const response = await api.post("/scrape", { url });
  return response.data;
};

export default api;
