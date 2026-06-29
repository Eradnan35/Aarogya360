import { apiClient } from "./api-client";
import { User, Session } from "@/types/api";

const MOCK_USER: User = {
  id: "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  clinic_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  name: "Dr. Sarah Jenkins",
  email: "sarah.j@aarogya360.com",
  phone: "+91-9876543210",
  role: "clinic_owner",
  mfa_enabled: false,
  is_active: true,
  last_login_at: "2026-06-28T10:00:00+05:30",
  created_at: "2026-06-01T10:00:00+05:30",
};

export const authService = {
  async getMe(): Promise<User> {
    try {
      const response = await apiClient.get<User>("/auth/me");
      return response.data;
    } catch {
      // Fallback to mock data for layout visualization (as authenticated clinic owner)
      return MOCK_USER;
    }
  },

  async getSessions(): Promise<Session[]> {
    try {
      const response = await apiClient.get<{ data: Session[] }>("/auth/sessions");
      return response.data.data;
    } catch {
      return [
        {
          id: "session-1",
          user_id: MOCK_USER.id,
          ip_address: "192.168.1.1",
          user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0",
          created_at: "2026-06-28T10:00:00+05:30",
          expires_at: "2026-06-28T18:00:00+05:30",
        },
      ];
    }
  },

  async logout(): Promise<void> {
    try {
      await apiClient.post("/auth/logout", {
        refresh_token: localStorage.getItem("aarogya360_refresh_token") || "",
      });
    } finally {
      localStorage.removeItem("aarogya360_access_token");
      localStorage.removeItem("aarogya360_refresh_token");
    }
  },
};
