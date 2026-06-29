"use client";

import React, { useState } from "react";
import Sidebar from "./sidebar";
import Header from "./header";
import RegisterPatientModal from "@/features/dashboard/components/register-patient-modal";


interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [registerOpen, setRegisterOpen] = useState(false);

  return (
    <div 
      className="min-h-screen bg-background text-foreground flex flex-col font-sans"
      style={{
        // Define dynamic sidebar width variables for standard layout calculations
        "--sidebar-width": collapsed ? "80px" : "260px"
      } as React.CSSProperties}
    >
      {/* Sidebar navigation components */}
      <Sidebar 
        collapsed={collapsed} 
        setCollapsed={setCollapsed}
        mobileOpen={mobileOpen} 
        setMobileOpen={setMobileOpen}
      />

      {/* Main panel wrapping header and inner contents */}
      <div className="flex-1 flex flex-col md:pl-[var(--sidebar-width)] transition-all duration-300">
        <Header 
          onMenuToggle={() => setMobileOpen(!mobileOpen)}
          onRegisterPatientClick={() => setRegisterOpen(true)}
        />
        
        {/* Main scrollable page canvas */}
        <main className="flex-1 pt-16 px-margin-desktop pb-12 overflow-x-hidden">
          {children}
        </main>
      </div>

      {/* Global Register Patient Modal Overlay */}
      <RegisterPatientModal 
        open={registerOpen} 
        onOpenChange={setRegisterOpen} 
      />
    </div>
  );
}
