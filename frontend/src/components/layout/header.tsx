"use client";

import React from "react";
import { Search, Bell, HelpCircle, UserPlus, Menu, Sun, Moon } from "lucide-react";
import { useAuth } from "@/providers/auth-provider";
import { useTheme } from "@/providers/theme-provider";
import { Button } from "@/components/ui/button";
import { Avatar } from "@/components/ui/avatar";

interface HeaderProps {
  onMenuToggle: () => void;
  onRegisterPatientClick: () => void;
}

export default function Header({ onMenuToggle, onRegisterPatientClick }: HeaderProps) {
  const { user } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="fixed top-0 right-0 left-0 md:left-[var(--sidebar-width)] h-16 bg-surface border-b border-border flex justify-between items-center px-margin-desktop z-40 transition-all duration-300">
      
      {/* Search Input & Mobile Toggle */}
      <div className="flex items-center gap-4 flex-1 max-w-sm mr-4">
        <button
          onClick={onMenuToggle}
          className="md:hidden p-2 hover:bg-surface-low rounded-lg text-muted-foreground transition-all"
          aria-label="Toggle navigation drawer"
        >
          <Menu className="h-5 w-5" />
        </button>

        <div className="relative w-full max-w-[320px] group hidden sm:block">
          <Search className="h-4.5 w-4.5 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground group-focus-within:text-primary transition-colors" />
          <input
            className="w-full bg-surface-low border border-border rounded-full py-1.5 pl-9 pr-4 text-xs placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
            placeholder="Search patients, doctors or history..."
            type="text"
          />
        </div>
      </div>

      {/* Action Utilities & User Section */}
      <div className="flex items-center gap-4 select-none shrink-0">
        
        {/* Theme toggle */}
        <button
          onClick={toggleTheme}
          className="w-9 h-9 flex items-center justify-center rounded-full hover:bg-surface-low text-muted-foreground transition-colors active:scale-95"
          title="Toggle color mode"
        >
          {theme === "light" ? <Moon className="h-5 w-5" /> : <Sun className="h-5 w-5" />}
        </button>

        {/* Notifications */}
        <button className="relative w-9 h-9 flex items-center justify-center rounded-full hover:bg-surface-low text-muted-foreground transition-colors active:scale-95">
          <Bell className="h-5 w-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-destructive rounded-full border border-surface-lowest" />
        </button>

        {/* Help Center */}
        <button className="hidden sm:flex w-9 h-9 items-center justify-center rounded-full hover:bg-surface-low text-muted-foreground transition-colors active:scale-95">
          <HelpCircle className="h-5 w-5" />
        </button>

        <div className="h-6 w-px bg-border hidden sm:block mx-1" />

        {/* Register Patient Global Shortcut */}
        <Button
          onClick={onRegisterPatientClick}
          className="bg-primary text-white hover:bg-primary/95 text-xs h-9 font-semibold flex items-center gap-1.5 px-4 shadow-sm"
        >
          <UserPlus className="h-4 w-4" />
          <span className="hidden sm:inline">Register Patient</span>
        </Button>

        {/* User Dropdown Profiler */}
        {user && (
          <div className="flex items-center gap-3 cursor-pointer group">
            <div className="text-right hidden xl:block leading-tight">
              <p className="text-xs font-bold text-foreground leading-tight">{user.name}</p>
              <p className="text-[10px] text-muted-foreground capitalize leading-tight">
                {user.role.replace("_", " ")}
              </p>
            </div>
            
            <Avatar 
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuCZ5D9CK62Cn4sp-9ffD38TYzEEDVabuUsN_8ufp9qYmUc7SO_YVIj56mX-BYaRLEaJ_QQNQ6ffkXl5SMOuEJ0CdCyk_Q0dfBxHhSrdsyxVep5vx1yPog3_cs2PrLxpC-VESb1JT_cjqRviylIxCScVu9fjPjVgWHsAPsYMXKQhYYekKPRoETpq8YF--qIHpJUoXSJcBbjHZB1i9LzcJY1tEhf7r9nYjxOnwiEWDGrWpp859hZBIW5_SJZ_wd0z2NQs9gVqZQKOnSk"
              fallback={user.name}
              className="w-9 h-9 border-2 border-primary/20 shadow-sm group-hover:border-primary/50 transition-all duration-200"
            />
          </div>
        )}
      </div>
    </header>
  );
}
