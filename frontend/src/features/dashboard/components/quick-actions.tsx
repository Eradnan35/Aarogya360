"use client";

import React from "react";
import { UserPlus, CalendarPlus, BadgeAlert, Building2 } from "lucide-react";
import { Card } from "@/components/ui/card";

interface QuickActionsProps {
  onAddPatientClick: () => void;
}

export default function QuickActions({ onAddPatientClick }: QuickActionsProps) {
  return (
    <Card className="bg-primary text-primary-foreground rounded-xl p-6 shadow-lg relative overflow-hidden h-[300px] flex flex-col justify-between select-none">
      {/* Title */}
      <h4 className="font-bold text-lg mb-4 shrink-0">Quick Actions</h4>

      {/* Button Grid */}
      <div className="grid grid-cols-2 gap-3 flex-grow">
        <button
          onClick={onAddPatientClick}
          className="flex flex-col items-center justify-center p-4 bg-white/10 hover:bg-white/20 rounded-xl transition-all border border-white/10 active:scale-95 group"
        >
          <UserPlus className="h-6 w-6 mb-2 group-hover:scale-110 transition-transform" />
          <span className="text-xs font-semibold">Add Patient</span>
        </button>

        <button className="flex flex-col items-center justify-center p-4 bg-white/10 hover:bg-white/20 rounded-xl transition-all border border-white/10 active:scale-95 group">
          <CalendarPlus className="h-6 w-6 mb-2 group-hover:scale-110 transition-transform" />
          <span className="text-xs font-semibold">Book Visit</span>
        </button>

        <button className="flex flex-col items-center justify-center p-4 bg-white/10 hover:bg-white/20 rounded-xl transition-all border border-white/10 active:scale-95 group">
          <BadgeAlert className="h-6 w-6 mb-2 group-hover:scale-110 transition-transform" />
          <span className="text-xs font-semibold">Add Staff</span>
        </button>

        <button className="flex flex-col items-center justify-center p-4 bg-white/10 hover:bg-white/20 rounded-xl transition-all border border-white/10 active:scale-95 group">
          <Building2 className="h-6 w-6 mb-2 group-hover:scale-110 transition-transform" />
          <span className="text-xs font-semibold">New Dept</span>
        </button>
      </div>

      {/* Decorative Blob */}
      <div className="absolute -right-10 -bottom-10 w-40 h-40 bg-white/5 rounded-full blur-3xl pointer-events-none" />
    </Card>
  );
}
