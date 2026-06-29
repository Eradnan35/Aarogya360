"use client";

import React, { useState } from "react";
import DashboardLayout from "@/components/layout/dashboard-layout";
import StatsCards from "@/features/dashboard/components/stats-cards";
import GrowthChart from "@/features/dashboard/components/growth-chart";
import LiveQueue from "@/features/dashboard/components/live-queue";
import QuickActions from "@/features/dashboard/components/quick-actions";
import UpcomingAppointments from "@/features/dashboard/components/upcoming-appointments";
import ActivityFeed from "@/features/dashboard/components/activity-feed";
import DistributionChart from "@/features/dashboard/components/distribution-chart";
import RegisterPatientModal from "@/features/dashboard/components/register-patient-modal";
import { useAuth } from "@/providers/auth-provider";
import { CalendarDays, RefreshCw } from "lucide-react";
import { Card } from "@/components/ui/card";

export default function DashboardPage() {
  const { user } = useAuth();
  const [registerOpen, setRegisterOpen] = useState(false);

  const formattedDate = new Date().toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });

  return (
    <DashboardLayout>
      {/* Welcome & Context Banner Section */}
      <section className="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4 select-none">
        <div>
          <h2 className="text-2xl font-bold text-foreground">Clinic Dashboard Overview</h2>
          <p className="text-sm text-muted-foreground mt-0.5 font-medium">
            Welcome back, {user ? user.name : "Dr. Jenkins"}. Here’s what’s happening today.
          </p>
        </div>
        <div className="flex items-center gap-2 bg-surface-container border border-border px-3 py-2 rounded-lg text-xs font-bold text-foreground shadow-sm">
          <CalendarDays className="h-4.5 w-4.5 text-primary shrink-0" />
          <span>{formattedDate} - Today</span>
        </div>
      </section>

      {/* Stats KPI Overview Bento Grid */}
      <StatsCards />

      {/* Core Grid layout */}
      <div className="grid grid-cols-12 gap-6">
        
        {/* Left Side: Charts & Table Details (8 columns) */}
        <div className="col-span-12 lg:col-span-8 space-y-6">
          <GrowthChart />
          <LiveQueue />
        </div>

        {/* Right Side: Quick Action widgets, Calendar, Activity feeds (4 columns) */}
        <div className="col-span-12 lg:col-span-4 space-y-6">
          <QuickActions onAddPatientClick={() => setRegisterOpen(true)} />
          <UpcomingAppointments />
          <ActivityFeed />
        </div>
      </div>

      {/* Secondary Bottom Grid widgets */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
        <DistributionChart />

        {/* New Weekly Patients Widget */}
        <Card className="p-6 border-border shadow-sm bg-card flex flex-col justify-between h-[300px]">
          <div className="flex justify-between items-center mb-6 shrink-0 select-none">
            <div>
              <h4 className="font-bold text-lg text-foreground">New Patients This Week</h4>
              <p className="text-xs text-muted-foreground">Recent profile registrations</p>
            </div>
            <button className="p-1 hover:bg-surface-low rounded-lg text-muted-foreground transition-all">
              <RefreshCw className="h-5 w-5" />
            </button>
          </div>

          {/* Patient Badges Grid */}
          <div className="flex-grow flex flex-wrap gap-4 overflow-y-auto no-scrollbar">
            {[
              { name: "Alicia Keys", reg: "Reg: 2h ago", initials: "AK", bg: "bg-blue-100 text-blue-600" },
              { name: "Tom Holland", reg: "Reg: 4h ago", initials: "TH", bg: "bg-purple-100 text-purple-600" },
              { name: "Zendaya Coleman", reg: "Reg: 6h ago", initials: "ZC", bg: "bg-orange-100 text-orange-600" },
              { name: "Chris Pratt", reg: "Reg: 1d ago", initials: "CP", bg: "bg-teal-100 text-teal-600" },
            ].map((pat, idx) => (
              <div 
                key={idx}
                className="flex items-center gap-3 bg-surface-low border border-border p-3 rounded-xl w-full sm:w-[calc(50%-8px)] group hover:border-primary/45 transition-colors cursor-pointer select-none"
              >
                <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm shrink-0 ${pat.bg}`}>
                  {pat.initials}
                </div>
                <div className="min-w-0">
                  <p className="text-sm font-bold text-foreground truncate">{pat.name}</p>
                  <p className="text-[10px] text-muted-foreground font-semibold truncate">{pat.reg}</p>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </section>

      {/* Register Patient modal trigger bind */}
      <RegisterPatientModal open={registerOpen} onOpenChange={setRegisterOpen} />
    </DashboardLayout>
  );
}
