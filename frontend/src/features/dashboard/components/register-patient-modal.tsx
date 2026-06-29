"use client";

import React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as zod from "zod";
import { useMutation } from "@tanstack/react-query";
import { patientService, RegisterPatientInput } from "@/services/patient.service";
import { getErrorMessage } from "@/services/api-client";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Info } from "lucide-react";

// Form validation schema based on OpenAPI spec
const registerPatientSchema = zod.object({
  name: zod.string()
    .min(2, "Name must be at least 2 characters")
    .max(200, "Name cannot exceed 200 characters"),
  phone: zod.string()
    .regex(/^\+91-\d{10}$/, "Phone must match +91-XXXXXXXXXX format"),
  email: zod.string()
    .email("Invalid email address")
    .or(zod.literal(""))
    .optional(),
  date_of_birth: zod.string()
    .or(zod.literal(""))
    .optional(),
  gender: zod.enum(["male", "female", "other"]),
  blood_group: zod.string().optional(),
  address: zod.string().optional(),
  emergency_contact_name: zod.string().optional(),
  emergency_contact_phone: zod.string()
    .regex(/^\+91-\d{10}$/, "Emergency phone must match +91-XXXXXXXXXX format")
    .or(zod.literal(""))
    .optional(),
  is_minor: zod.boolean(),
});

type RegisterPatientFormData = zod.infer<typeof registerPatientSchema>;

interface RegisterPatientModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export default function RegisterPatientModal({ open, onOpenChange }: RegisterPatientModalProps) {
  const {
    register,
    handleSubmit,
    reset,
    watch,
    formState: { errors },
  } = useForm<RegisterPatientFormData>({
    resolver: zodResolver(registerPatientSchema),
    defaultValues: {
      name: "",
      phone: "+91-",
      email: "",
      date_of_birth: "",
      gender: "male",
      blood_group: "",
      address: "",
      emergency_contact_name: "",
      emergency_contact_phone: "",
      is_minor: false,
    },
  });

  const isMinor = watch("is_minor");

  // TanStack query mutation to execute patient registration
  const mutation = useMutation({
    mutationFn: (data: RegisterPatientInput) => patientService.registerPatient(data),
    onSuccess: (newPatient) => {
      alert(`Patient ${newPatient.name} registered successfully with PID: ${newPatient.qr_code}!`);
      reset();
      onOpenChange(false);
    },
    onError: (err) => {
      alert(`Registration failed: ${getErrorMessage(err)}`);
    },
  });

  const onSubmit = (data: RegisterPatientFormData) => {
    const payload: RegisterPatientInput = {
      ...data,
      email: data.email || undefined,
      date_of_birth: data.date_of_birth || undefined,
      blood_group: data.blood_group || undefined,
      address: data.address || undefined,
      emergency_contact_name: data.emergency_contact_name || undefined,
      emergency_contact_phone: data.emergency_contact_phone || undefined,
    };
    mutation.mutate(payload);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-lg select-none">
        <DialogHeader>
          <DialogTitle>Register Patient</DialogTitle>
          <DialogDescription>
            Onboard a new patient record into the clinical database.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 overflow-y-auto max-h-[70vh] px-1 no-scrollbar">
          
          {/* Full Name */}
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-muted-foreground px-1">Full Name</label>
            <Input 
              {...register("name")} 
              placeholder="e.g. Rahul Mishra"
              className={errors.name ? "border-destructive focus-visible:ring-destructive" : ""}
            />
            {errors.name && (
              <span className="text-[10px] text-destructive px-1 font-semibold">{errors.name.message}</span>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4">
            {/* Primary Phone */}
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-semibold text-muted-foreground px-1">Primary Phone</label>
              <Input 
                {...register("phone")} 
                placeholder="+91-XXXXXXXXXX"
                className={errors.phone ? "border-destructive focus-visible:ring-destructive" : ""}
              />
              {errors.phone && (
                <span className="text-[10px] text-destructive px-1 font-semibold">{errors.phone.message}</span>
              )}
            </div>

            {/* Email Address */}
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-semibold text-muted-foreground px-1">Email Address</label>
              <Input 
                type="email" 
                {...register("email")} 
                placeholder="email@example.com"
                className={errors.email ? "border-destructive focus-visible:ring-destructive" : ""}
              />
              {errors.email && (
                <span className="text-[10px] text-destructive px-1 font-semibold">{errors.email.message}</span>
              )}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            {/* DOB */}
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-semibold text-muted-foreground px-1">Date of Birth</label>
              <Input type="date" {...register("date_of_birth")} />
            </div>

            {/* Gender */}
            <Select
              label="Gender"
              options={[
                { label: "Male", value: "male" },
                { label: "Female", value: "female" },
                { label: "Other", value: "other" },
              ]}
              {...register("gender")}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            {/* Blood Group */}
            <Select
              label="Blood Group"
              options={[
                { label: "A+", value: "A+" },
                { label: "A-", value: "A-" },
                { label: "B+", value: "B+" },
                { label: "B-", value: "B-" },
                { label: "AB+", value: "AB+" },
                { label: "AB-", value: "AB-" },
                { label: "O+", value: "O+" },
                { label: "O-", value: "O-" },
              ]}
              placeholder="Select blood group..."
              {...register("blood_group")}
            />

            {/* Minor Switch */}
            <div className="flex flex-col gap-1.5 justify-center pl-2">
              <label className="flex items-center gap-2 cursor-pointer mt-5">
                <input 
                  type="checkbox" 
                  {...register("is_minor")}
                  className="rounded border-border text-primary focus:ring-primary h-4.5 w-4.5 cursor-pointer"
                />
                <span className="text-xs font-bold text-foreground">Under 18 Years (Minor)</span>
              </label>
            </div>
          </div>

          {/* Full Address */}
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-muted-foreground px-1">Full Address</label>
            <Input {...register("address")} placeholder="Door no, Street, City, State" />
          </div>

          {/* Minor Guardian Info Alert */}
          {isMinor && (
            <div className="bg-primary/5 p-4 rounded-xl flex gap-3 items-start border border-primary/10">
              <Info className="h-5 w-5 text-primary shrink-0 mt-0.5" />
              <p className="text-[11px] text-primary leading-relaxed font-semibold">
                This patient is registered as a minor. A guardian consent link (via parent/guardian PID) is required before booking active slots.
              </p>
            </div>
          )}

          {/* Form Actions Footer */}
          <div className="flex gap-4 pt-4 border-t border-border mt-6 shrink-0">
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              className="flex-1 font-semibold"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={mutation.isPending}
              className="flex-grow font-semibold"
            >
              {mutation.isPending ? "Registering..." : "Register"}
            </Button>
          </div>

        </form>
      </DialogContent>
    </Dialog>
  );
}
