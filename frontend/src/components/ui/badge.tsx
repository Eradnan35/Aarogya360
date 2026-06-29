import * as React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "success" | "info" | "warning" | "error" | "default";
}

function Badge({ className, variant = "default", ...props }: BadgeProps) {
  return (
    <div
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-bold transition-colors focus:outline-none uppercase tracking-wide",
        // Color mappings matching standard Aarogya360 pills
        variant === "default" && "border-border bg-surface-container text-foreground",
        variant === "success" && "border-green-200 bg-green-100 text-green-800",
        variant === "info" && "border-blue-200 bg-blue-100 text-blue-800",
        variant === "warning" && "border-yellow-200 bg-yellow-100 text-yellow-800",
        variant === "error" && "border-red-200 bg-red-100 text-red-800",
        className
      )}
      {...props}
    />
  );
}

export { Badge };
