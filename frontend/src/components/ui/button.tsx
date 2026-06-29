import * as React from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "container" | "outline" | "ghost" | "destructive";
  size?: "default" | "sm" | "lg" | "icon";
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "default", ...props }, ref) => {
    return (
      <button
        className={cn(
          "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 active:scale-95",
          // Variant mappings based on Aarogya360 tokens
          variant === "default" && "bg-primary text-primary-foreground shadow hover:bg-primary/95",
          variant === "container" && "bg-primary-container text-primary-foreground shadow-sm hover:bg-primary-container/90",
          variant === "outline" && "border border-input bg-background text-foreground hover:bg-surface-low hover:text-foreground",
          variant === "ghost" && "hover:bg-surface-low hover:text-foreground text-muted-foreground",
          variant === "destructive" && "bg-destructive text-destructive-foreground hover:bg-destructive/90",
          // Size mappings
          size === "default" && "h-10 px-4 py-2 text-sm",
          size === "sm" && "h-8 rounded-md px-3 text-xs",
          size === "lg" && "h-11 rounded-md px-8 text-sm",
          size === "icon" && "h-10 w-10",
          className
        )}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";

export { Button };
