import { apiClient } from "./api-client";
import { Patient } from "@/types/api";

export interface RegisterPatientInput {
  name: string;
  phone: string;
  email?: string;
  date_of_birth?: string;
  gender: "male" | "female" | "other";
  blood_group?: string;
  address?: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
  is_minor: boolean;
  guardian_patient_id?: string;
}

export const patientService = {
  async registerPatient(input: RegisterPatientInput): Promise<Patient> {
    const response = await apiClient.post<Patient>("/patients", input);
    return response.data;
  },

  async searchPatients(query: { q?: string; phone?: string; patient_id?: string }): Promise<Patient[]> {
    const response = await apiClient.get<{ data: Patient[] }>("/patients", {
      params: query,
    });
    return response.data.data;
  },

  async getPatient(patientId: string): Promise<Patient> {
    const response = await apiClient.get<Patient>(`/patients/${patientId}`);
    return response.data;
  },
};
