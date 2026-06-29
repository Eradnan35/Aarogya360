import { apiClient } from "./api-client";
import { Clinic } from "@/types/api";

const MOCK_CLINIC: Clinic = {
  id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  name: "Aarogya360 Health Center",
  email: "contact@aarogya360.com",
  phone: "+91-9876543210",
  address_line_1: "Suite 405, Wellness Towers",
  address_line_2: "2nd Main Road, HSR Layout Sector 7",
  city: "Bangalore",
  state: "Karnataka",
  country: "India",
  pincode: "560102",
  gstin: "27AAHCA1234A1Z5",
  timezone: "Asia/Kolkata",
  logo_url: "https://lh3.googleusercontent.com/aida-public/AB6AXuBLBrUho7AVJFlm8oy0p7N13qXGIMcOYS2fmYnXidPN1x3fSP0ZEc7LfjqqIDFuj01v-ittlSpOKpDrFKEz9msC1Er-uego859EXjQA8AQ1Pu05pLCrTtwa07M7vx22qQBzSnJ1aMd_0LoL7ttAdbEjtp3oJWVJko320kFvnn77CjwLRPlVjSdCN4Lmsa86NuvkSHtGnG0dSDPuc9aVAlXow-OPx9Mc1Tse6YgW_Y872JFVmYxc94VRfb55HgePYdvYDWuCvSqVtss",
  subscription_plan: "pro",
  is_active: true,
  created_at: "2026-06-01T10:00:00+05:30",
  updated_at: "2026-06-20T14:00:00+05:30",
};

export const clinicService = {
  async getMyClinic(): Promise<Clinic> {
    try {
      const response = await apiClient.get<Clinic>("/clinics/me");
      return response.data;
    } catch {
      return MOCK_CLINIC;
    }
  },

  async updateClinic(input: Partial<Clinic>): Promise<Clinic> {
    const response = await apiClient.put<Clinic>("/clinics/me", input);
    return response.data;
  },
};
