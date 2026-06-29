export type UserRole = "clinic_owner" | "doctor" | "receptionist" | "lab_technician" | "system_admin";

export interface User {
  id: string;
  clinic_id: string;
  name: string;
  email: string;
  phone: string;
  role: UserRole;
  mfa_enabled: boolean;
  is_active: boolean;
  last_login_at?: string;
  created_at: string;
  updated_at?: string;
}

export interface Session {
  id: string;
  user_id: string;
  ip_address?: string;
  user_agent?: string;
  created_at: string;
  expires_at: string;
}

export interface Clinic {
  id: string;
  name: string;
  email: string;
  phone: string;
  address_line_1: string;
  address_line_2?: string;
  city: string;
  state: string;
  country: string;
  pincode: string;
  gstin?: string;
  timezone: string;
  logo_url?: string;
  subscription_plan: "free_trial" | "basic" | "pro" | "enterprise";
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface Department {
  id: string;
  clinic_id: string;
  name: string;
  description?: string;
  created_at: string;
  updated_at?: string;
}

export interface Doctor {
  id: string;
  clinic_id: string;
  user_id: string;
  department_id?: string;
  specialization: string;
  qualification: string;
  registration_number: string;
  consultation_fee: number;
  experience_years: number;
  created_at: string;
  user?: Partial<User>;
}

export interface Patient {
  id: string;
  name: string;
  phone: string;
  email?: string;
  date_of_birth?: string;
  gender: "male" | "female" | "other";
  blood_group?: "A+" | "A-" | "B+" | "B-" | "AB+" | "AB-" | "O+" | "O-";
  address?: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
  is_minor: boolean;
  qr_code: string;
  abha_id?: string;
  created_at: string;
  updated_at?: string;
}

export type AppointmentStatus = "scheduled" | "arrived" | "in_progress" | "completed" | "cancelled" | "no_show";

export interface Appointment {
  id: string;
  clinic_id: string;
  doctor_id: string;
  patient_id: string;
  slot_start: string;
  slot_end: string;
  token_number: number;
  status: AppointmentStatus;
  notes?: string;
  created_at: string;
  updated_at?: string;
  patient?: Partial<Patient>;
  doctor?: Partial<Doctor>;
}

export interface ErrorResponse {
  error_code: string;
  message: string;
  details?: Record<string, string[]> | null;
}
