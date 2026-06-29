"use client";

import React, { useState } from "react";
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { usePatientGrowth } from "@/hooks/use-dashboard";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function GrowthChart() {
  const { data, isLoading } = usePatientGrowth();
  const [range, setRange] = useState<"weekly" | "monthly">("weekly");

  return (
    <Card className="p-6 border-border shadow-sm bg-card flex flex-col justify-between h-[380px]">
      {/* Title Header Section */}
      <div className="flex justify-between items-center mb-6 shrink-0 select-none">
        <div>
          <h4 className="font-bold text-lg text-foreground">Patient Growth Trend</h4>
          <p className="text-xs text-muted-foreground">Detailed daily registrations</p>
        </div>
        <div className="flex gap-2">
          <Button
            variant={range === "weekly" ? "container" : "outline"}
            size="sm"
            onClick={() => setRange("weekly")}
            className="h-8 text-xs font-semibold px-3"
          >
            Weekly
          </Button>
          <Button
            variant={range === "monthly" ? "container" : "outline"}
            size="sm"
            onClick={() => setRange("monthly")}
            className="h-8 text-xs font-semibold px-3"
          >
            Monthly
          </Button>
        </div>
      </div>

      {/* Chart Canvas */}
      <div className="flex-1 w-full relative">
        {isLoading ? (
          <div className="w-full h-full bg-surface-low rounded-lg animate-pulse" />
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart
              data={data}
              margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
            >
              <defs>
                <linearGradient id="gradient-blue" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#0066ff" stopOpacity={0.2} />
                  <stop offset="95%" stopColor="#0066ff" stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <XAxis 
                dataKey="day" 
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
              />
              <Area
                type="monotone"
                dataKey="count"
                stroke="#0066ff"
                strokeWidth={3}
                fillOpacity={1}
                fill="url(#gradient-blue)"
                activeDot={{ r: 6, strokeWidth: 0, fill: "#0066ff" }}
              />
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>
    </Card>
  );
}
