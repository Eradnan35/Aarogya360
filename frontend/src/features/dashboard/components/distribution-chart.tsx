"use client";

import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { useAppointmentDistribution } from "@/hooks/use-dashboard";
import { Card } from "@/components/ui/card";
import { MoreVertical } from "lucide-react";

export default function DistributionChart() {
  const { data, isLoading } = useAppointmentDistribution();

  return (
    <Card className="p-6 border-border shadow-sm bg-card flex flex-col justify-between h-[300px]">
      {/* Title Header Section */}
      <div className="flex justify-between items-center mb-6 shrink-0 select-none">
        <div>
          <h4 className="font-bold text-lg text-foreground">Appointment Distribution</h4>
          <p className="text-xs text-muted-foreground">Visits breakdown by clinical specialty</p>
        </div>
        <button className="p-1 hover:bg-surface-low rounded-lg text-muted-foreground transition-all">
          <MoreVertical className="h-5 w-5" />
        </button>
      </div>

      {/* Chart Canvas */}
      <div className="flex-1 w-full relative">
        {isLoading ? (
          <div className="w-full h-full bg-surface-low rounded-lg animate-pulse" />
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={data}
              margin={{ top: 10, right: 10, left: -25, bottom: 0 }}
              barSize={32}
            >
              <XAxis
                dataKey="specialty"
                stroke="hsl(var(--muted-foreground))"
                fontSize={11}
                tickLine={false}
                axisLine={false}
                dy={10}
              />
              <YAxis
                stroke="hsl(var(--muted-foreground))"
                fontSize={11}
                tickLine={false}
                axisLine={false}
                dx={-10}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: "8px",
                  fontSize: "12px",
                  boxShadow: "0 4px 12px rgba(0, 0, 0, 0.05)",
                }}
                cursor={{ fill: "hsl(var(--surface-low) / 0.3)" }}
              />
              <Bar
                dataKey="count"
                radius={[6, 6, 0, 0]}
              >
                {data?.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill="hsl(var(--primary-container) / 0.3)"
                    className="hover:fill-primary transition-colors duration-200 cursor-pointer"
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </Card>
  );
}
