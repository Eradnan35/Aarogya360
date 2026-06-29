"use client";

import React from "react";
import { ChevronRight } from "lucide-react";
import { useUpcomingAppointments } from "@/hooks/use-dashboard";
import { Card } from "@/components/ui/card";

export default function UpcomingAppointments() {
  const { data: appointments, isLoading } = useUpcomingAppointments();

  return (
    <Card className="p-6 border-border shadow-sm bg-card flex flex-col justify-between h-[300px]">
      {/* Title Header Section */}
      <div className="flex justify-between items-center mb-4 shrink-0 select-none">
        <h4 className="font-bold text-lg text-foreground">Up Next</h4>
        <a 
          href="#" 
          className="text-primary text-xs font-bold hover:underline transition-all"
        >
          View All
        </a>
      </div>

      {/* List Section */}
      <div className="flex-1 space-y-3 overflow-y-auto no-scrollbar pr-1">
        {isLoading ? (
          <div className="space-y-3">
            {Array.from({ length: 3 }).map((_, idx) => (
              <div key={idx} className="h-14 bg-surface-low rounded-lg animate-pulse" />
            ))}
          </div>
        ) : (
          appointments?.map((item) => (
            <div
              key={item.id}
              className="flex items-center gap-4 p-3 hover:bg-surface-low rounded-lg border border-transparent hover:border-border transition-all duration-200 cursor-pointer group"
            >
              {/* Date Box */}
              <div className="w-12 h-12 flex flex-col items-center justify-center bg-primary-container/10 text-primary rounded-lg font-bold shrink-0">
                <span className="text-[9px] leading-tight font-extrabold uppercase">{item.dateBadge.month}</span>
                <span className="text-lg leading-none font-black">{item.dateBadge.day}</span>
              </div>

              {/* Appointment details */}
              <div className="flex-grow min-w-0">
                <p className="text-sm font-bold text-foreground truncate">{item.patientName}</p>
                <p className="text-xs text-muted-foreground truncate font-medium">
                  {item.time} • {item.doctorName}
                </p>
              </div>

              <ChevronRight className="h-5 w-5 text-muted-foreground group-hover:text-primary transition-colors shrink-0" />
            </div>
          ))
        )}
      </div>
    </Card>
  );
}
