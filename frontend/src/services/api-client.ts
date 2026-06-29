import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add interceptor to inject auth token dynamically
apiClient.interceptors.request.use(
  (config) => {
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("aarogya360_access_token");
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

interface NetworkError {
  response?: {
    data?: {
      message?: string;
    };
  };
  message?: string;
}

export const getErrorMessage = (error: NetworkError | Error | unknown): string => {
  const err = error as NetworkError;
  if (err.response?.data?.message) {
    return err.response.data.message;
  }
  return err.message || "An unexpected error occurred.";
};
