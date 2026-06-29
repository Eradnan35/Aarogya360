"use client";

import React from "react";
import { 
  LayoutDashboard, 
  Store, 
  Users, 
  Building2, 
  Stethoscope, 
  Search, 
  CalendarRange, 
  ListOrdered, 
  ShieldCheck, 
  UserCircle,
  ChevronLeft
} from "lucide-react";
import { cn } from "@/lib/utils";

interface SidebarProps {
  collapsed: boolean;
  setCollapsed: (collapsed: boolean) => void;
  mobileOpen: boolean;
  setMobileOpen: (open: boolean) => void;
}

interface NavItem {
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  href: string;
  active?: boolean;
}

export default function Sidebar({ collapsed, setCollapsed, mobileOpen, setMobileOpen }: SidebarProps) {
  const navItems: NavItem[] = [
    { label: "Dashboard", icon: LayoutDashboard, href: "#", active: true },
    { label: "Clinic Profile", icon: Store, href: "#" },
    { label: "Staff Management", icon: Users, href: "#" },
    { label: "Departments", icon: Building2, href: "#" },
    { label: "Doctors Directory", icon: Stethoscope, href: "#" },
    { label: "Patients", icon: Search, href: "#" },
    { label: "Appointments", icon: CalendarRange, href: "#" },
    { label: "Queue Management", icon: ListOrdered, href: "#" },
  ];

  const adminItems: NavItem[] = [
    { label: "Security & Sessions", icon: ShieldCheck, href: "#" },
    { label: "My Profile", icon: UserCircle, href: "#" },
  ];

  const sidebarContent = (
    <div className="flex flex-col h-full bg-surface border-r border-border py-6 px-4 select-none">
      {/* Brand Header */}
      <div className={cn("flex items-center mb-8 gap-3 px-2 justify-between")}>
        <div className="flex items-center gap-3 overflow-hidden">
          <div className="w-10 h-10 bg-primary-container rounded-lg flex items-center justify-center shrink-0 shadow-md">
            <svg
              className="h-6 w-6 text-white"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.746 3.746 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.746 3.746 0 011.043 3.296A3.745 3.745 0 0121 12z"
              />
            </svg>
          </div>
          {!collapsed && (
            <div className="flex flex-col">
              <span className="font-bold text-lg text-primary leading-tight">Aarogya360</span>
              <span className="text-xs font-semibold text-muted-foreground">Clinic Management</span>
            </div>
          )}
        </div>
        
        {/* Collapse toggle (desktop only) */}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="hidden md:flex p-1.5 hover:bg-surface-low rounded-lg text-muted-foreground transition-all"
        >
          <ChevronLeft className={cn("h-4 w-4 transition-transform", collapsed && "rotate-180")} />
        </button>
      </div>

      {/* Nav List */}
      <nav className="flex-grow flex flex-col gap-1 overflow-y-auto pr-1 no-scrollbar">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <a
              key={item.label}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-4 py-3 rounded-lg font-medium text-sm transition-all duration-200",
                item.active 
                  ? "bg-primary-container text-white shadow-md active:scale-95" 
                  : "text-muted-foreground hover:bg-surface-low hover:text-foreground"
              )}
              title={collapsed ? item.label : undefined}
            >
              <Icon className="h-5 w-5 shrink-0" />
              {!collapsed && <span>{item.label}</span>}
            </a>
          );
        })}
      </nav>

      {/* Admin Logins / Settings (Sticky at bottom) */}
      <div className="border-t border-border pt-6 flex flex-col gap-1 mt-auto shrink-0">
        {adminItems.map((item) => {
          const Icon = item.icon;
          return (
            <a
              key={item.label}
              href={item.href}
              className="flex items-center gap-3 px-4 py-3 rounded-lg font-medium text-sm text-muted-foreground hover:bg-surface-low hover:text-foreground transition-all"
              title={collapsed ? item.label : undefined}
            >
              <Icon className="h-5 w-5 shrink-0" />
              {!collapsed && <span>{item.label}</span>}
            </a>
          );
        })}
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className={cn(
        "hidden md:block fixed left-0 top-0 h-full bg-surface border-r border-border transition-all duration-300 z-50",
        collapsed ? "w-[80px]" : "w-[260px]"
      )}>
        {sidebarContent}
      </aside>

      {/* Mobile Drawer Backdrop */}
      {mobileOpen && (
        <div 
          onClick={() => setMobileOpen(false)}
          className="md:hidden fixed inset-0 bg-black/40 backdrop-blur-sm z-[90] animate-in fade-in duration-200"
        />
      )}

      {/* Mobile Sidebar (Drawer style) */}
      <aside className={cn(
        "md:hidden fixed left-0 top-0 h-full w-[260px] bg-surface border-r border-border z-[100] transition-transform duration-300",
        mobileOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        {sidebarContent}
      </aside>
    </>
  );
}
