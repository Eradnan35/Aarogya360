
export interface StatItem {
  id: string;
  label: string;
  value: string | number;
  trend: string;
  trendType: "up" | "down" | "neutral" | "warning";
  iconName: string;
  badgeText?: string;
}

export interface DashboardStats {
  totalPatients: StatItem;
  appointmentsToday: StatItem;
  activeDoctors: StatItem;
  activeStaff: StatItem;
  queueCount: StatItem;
  revenue: StatItem;
}

export interface PatientGrowthPoint {
  day: string;
  count: number;
}

export interface AppointmentDistributionPoint {
  specialty: string;
  count: number;
}

export interface LiveQueueItem {
  queueId: string;
  patientName: string;
  patientInitials: string;
  doctorName: string;
  status: "Consulting" | "Next Up" | "Waiting";
  waitingTime: string;
  patientId: string;
}

export interface UpcomingAppointmentItem {
  id: string;
  patientName: string;
  purpose: string;
  time: string;
  doctorName: string;
  dateBadge: {
    month: string;
    day: string;
  };
}

export interface ActivityLogItem {
  id: string;
  actor: string;
  action: string;
  timeText: string;
  type: "info" | "success" | "warning" | "error" | "default";
}
