"use client";

import React from "react";
import { Users, Calendar, Stethoscope, UserCheck, Hourglass, DollarSign } from "lucide-react";
import { useDashboardStats } from "@/hooks/use-dashboard";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  person: Users,
  event_note: Calendar,
  medical_information: Stethoscope,
  groups: UserCheck,
  hourglass_empty: Hourglass,
  payments: DollarSign,
};

export default function StatsCards() {
  const { data: stats, isLoading, error } = useDashboardStats();

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
        {Array.from({ length: 6 }).map((_, idx) => (
          <div 
            key={idx} 
            className="h-28 bg-surface-low border border-border rounded-xl animate-pulse"
          />
        ))}
      </div>
    );
  }

  if (error || !stats) return null;

  const items = Object.values(stats);

  return (
    <section className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8 select-none">
      {items.map((item) => {
        const Icon = iconMap[item.iconName] || Users;
        const isUp = item.trendType === "up";
        const isWarning = item.trendType === "warning";

        return (
          <Card 
            key={item.id}
            className="p-4 flex flex-col justify-between border-border hover:border-primary transition-all duration-300 group cursor-pointer shadow-sm relative overflow-hidden"
          >
            {/* Top Row: Icon + Trend Indicator */}
            <div className="flex justify-between items-start mb-3">
              <div className="p-2 bg-primary/10 text-primary rounded-lg group-hover:bg-primary group-hover:text-white transition-colors duration-300 shrink-0">
                <Icon className="h-5 w-5" />
              </div>
              <span className={cn(
                "text-[10px] font-extrabold px-1.5 py-0.5 rounded-full shrink-0",
                isUp && "bg-green-100 text-green-800",
                isWarning && "bg-red-100 text-red-800",
                !isUp && !isWarning && "bg-surface-container-high text-muted-foreground"
              )}>
                {item.trend}
              </span>
            </div>

            {/* Bottom Row: Title + Metric */}
            <div className="flex flex-col">
              <span className="text-xs text-muted-foreground font-medium mb-0.5">{item.label}</span>
              <span className="text-xl font-bold text-foreground leading-tight">{item.value}</span>
            </div>
          </Card>
        );
      })}
    </section>
  );
}
