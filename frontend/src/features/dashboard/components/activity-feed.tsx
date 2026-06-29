"use client";

import React from "react";
import { useActivityLogs } from "@/hooks/use-dashboard";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

export default function ActivityFeed() {
  const { data: logs, isLoading } = useActivityLogs();

  return (
    <Card className="p-6 border-border shadow-sm bg-card flex flex-col justify-between h-[380px]">
      {/* Title */}
      <h4 className="font-bold text-lg text-foreground mb-4 shrink-0 select-none">Staff Activity</h4>

      {/* Timeline List */}
      <div className="flex-grow overflow-y-auto no-scrollbar relative before:absolute before:left-[11px] before:top-2 before:bottom-2 before:w-px before:bg-border">
        {isLoading ? (
          <div className="space-y-4 pl-8">
            {Array.from({ length: 3 }).map((_, idx) => (
              <div key={idx} className="h-10 bg-surface-low rounded-lg animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="space-y-6">
            {logs?.map((item) => {
              const isSuccess = item.type === "success";
              const isWarning = item.type === "warning";
              const isInfo = item.type === "info";

              return (
                <div key={item.id} className="relative pl-8 select-none">
                  {/* Timeline Bullet Node */}
                  <div className={cn(
                    "absolute left-0 top-1 w-[22px] h-[22px] bg-card border-2 rounded-full flex items-center justify-center z-10",
                    isSuccess && "border-green-500",
                    isWarning && "border-yellow-500",
                    isInfo && "border-blue-500",
                    !isSuccess && !isWarning && !isInfo && "border-border"
                  )}>
                    <div className={cn(
                      "w-1.5 h-1.5 rounded-full",
                      isSuccess && "bg-green-500",
                      isWarning && "bg-yellow-500",
                      isInfo && "bg-blue-500",
                      !isSuccess && !isWarning && !isInfo && "bg-muted-foreground"
                    )} />
                  </div>

                  {/* Log Content */}
                  <div className="flex flex-col">
                    <span className="text-xs font-bold text-foreground leading-snug">{item.actor}</span>
                    <span className="text-xs text-muted-foreground font-medium mt-0.5 leading-normal">
                      {item.action}
                    </span>
                    <span className="text-[10px] text-muted-foreground mt-1 font-semibold">
                      {item.timeText}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </Card>
  );
}
