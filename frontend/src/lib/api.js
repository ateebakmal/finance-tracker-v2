import axios from "axios";
import { tokenStore } from "./tokenStore";

// Every data request in the app goes through this instance.
export const api = axios.create({
  baseURL: "/api", // relative -> uses your Vite proxy -> same-origin, no CORS
  withCredentials: true, // send the httpOnly refresh cookie
});

// A bare instance for refresh ONLY. If refresh went through `api`, a failing
// refresh would hit the 401 interceptor -> call refresh again -> forever.
const refreshClient = axios.create({
  baseURL: "/api",
  withCredentials: true,
});

/* 1. Request interceptor — attach the token to every outgoing request */
api.interceptors.request.use((config) => {
  const token = tokenStore.get();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

/* 2. Single-flight refresh — many 401s share ONE refresh call.
   Critical for you: your backend ROTATES the refresh token, so parallel
   refreshes would send an already-dead cookie and fail. */
let refreshPromise = null;

export function refreshAccessToken() {
  if (!refreshPromise) {
    refreshPromise = refreshClient
      .post("/auth/refresh")
      .then((res) => {
        tokenStore.set(res.data.access_token);
        return res.data.access_token;
      })
      .finally(() => {
        refreshPromise = null; // let a future 401 start a fresh refresh
      });
  }
  return refreshPromise;
}

/* 3. Response interceptor — 401 -> refresh -> retry once, else give up.
   AuthProvider registers what "give up" means (clear React user state). */
let onSessionExpired = () => {};
export function setSessionExpiredHandler(fn) {
  onSessionExpired = fn;
}

api.interceptors.response.use(
  (response) => response, // 2xx passes straight through
  async (error) => {
    const original = error.config;

    // Only handle "token expired", and never twice for the same request.
    if (error.response?.status !== 401 || original._retry) {
      return Promise.reject(error);
    }
    original._retry = true; // guard against an infinite refresh loop

    try {
      await refreshAccessToken();
      return api(original); // replay the original request with the new token
    } catch (refreshError) {
      tokenStore.clear();
      onSessionExpired(); // tell React the session is truly over
      return Promise.reject(refreshError);
    }
  },
);

export function getApiErrorMessage(error) {
  return (
    error?.response?.data?.detail ?? error?.message ?? "Something went wrong"
  );
}

export async function logoutRequest() {
  await api.post("/auth/logout");
}
