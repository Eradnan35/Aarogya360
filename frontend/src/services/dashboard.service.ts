import { 
  DashboardStats, 
  PatientGrowthPoint, 
  AppointmentDistributionPoint, 
  LiveQueueItem, 
  UpcomingAppointmentItem, 
  ActivityLogItem 
} from "@/types/dashboard";

// Simulate network latency
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export const dashboardService = {
  async getStats(): Promise<DashboardStats> {
    await delay(300);
    return {
      totalPatients: {
        id: "total_patients",
        label: "Total Patients",
        value: "1,284",
        trend: "+12%",
        trendType: "up",
        iconName: "person",
      },
      appointmentsToday: {
        id: "appointments_today",
        label: "Appointments",
        value: "42",
        trend: "Today",
        trendType: "neutral",
        iconName: "event_note",
      },
      activeDoctors: {
        id: "active_doctors",
        label: "Active Doctors",
        value: "15",
        trend: "On Duty",
        trendType: "neutral",
        iconName: "medical_information",
      },
      activeStaff: {
        id: "active_staff",
        label: "Active Staff",
        value: "28",
        trend: "Shift A",
        trendType: "neutral",
        iconName: "groups",
      },
      queueCount: {
        id: "queue_count",
        label: "Queue Count",
        value: "08",
        trend: "High",
        trendType: "warning",
        iconName: "hourglass_empty",
      },
      revenue: {
        id: "revenue",
        label: "Revenue",
        value: "$12.4k",
        trend: "+5%",
        trendType: "up",
        iconName: "payments",
      },
    };
  },

  async getPatientGrowth(): Promise<PatientGrowthPoint[]> {
    await delay(300);
    return [
      { day: "Mon", count: 180 },
      { day: "Tue", count: 210 },
      { day: "Wed", count: 200 },
      { day: "Thu", count: 240 },
      { day: "Fri", count: 230 },
      { day: "Sat", count: 270 },
      { day: "Sun", count: 290 },
    ];
  },

  async getAppointmentDistribution(): Promise<AppointmentDistributionPoint[]> {
    await delay(300);
    return [
      { specialty: "General", count: 60 },
      { specialty: "Dental", count: 85 },
      { specialty: "Eye", count: 45 },
      { specialty: "Physio", count: 70 },
      { specialty: "Cardio", count: 95 },
    ];
  },

  async getLiveQueue(): Promise<LiveQueueItem[]> {
    await delay(200);
    return [
      {
        queueId: "#Q-1042",
        patientName: "James Schmidt",
        patientInitials: "JS",
        doctorName: "Dr. Sarah Connor",
        status: "Consulting",
        waitingTime: "12 mins",
        patientId: "patient-1",
      },
      {
        queueId: "#Q-1043",
        patientName: "Lydia Miller",
        patientInitials: "LM",
        doctorName: "Dr. Robert Vance",
        status: "Next Up",
        waitingTime: "24 mins",
        patientId: "patient-2",
      },
      {
        queueId: "#Q-1044",
        patientName: "Ben Parker",
        patientInitials: "BP",
        doctorName: "Dr. Sarah Connor",
        status: "Waiting",
        waitingTime: "45 mins",
        patientId: "patient-3",
      },
    ];
  },

  async getUpcomingAppointments(): Promise<UpcomingAppointmentItem[]> {
    await delay(200);
    return [
      {
        id: "upcoming-1",
        patientName: "Cardiac Checkup",
        purpose: "General follow-up",
        time: "02:30 PM",
        doctorName: "Dr. Robert Vance",
        dateBadge: { month: "OCT", day: "24" },
      },
      {
        id: "upcoming-2",
        patientName: "Pediatric Annual",
        purpose: "Vaccination check",
        time: "03:15 PM",
        doctorName: "Dr. Sarah Connor",
        dateBadge: { month: "OCT", day: "24" },
      },
      {
        id: "upcoming-3",
        patientName: "Dental Cleaning",
        purpose: "Routine hygiene",
        time: "04:00 PM",
        doctorName: "Dr. Mike Ross",
        dateBadge: { month: "OCT", day: "24" },
      },
    ];
  },

  async getActivityLogs(): Promise<ActivityLogItem[]> {
    await delay(200);
    return [
      {
        id: "log-1",
        actor: "Nurse Jenny",
        action: "Completed check-in for James Schmidt",
        timeText: "2 mins ago",
        type: "success",
      },
      {
        id: "log-2",
        actor: "System",
        action: "Inventory alert: Sterile gloves low",
        timeText: "15 mins ago",
        type: "warning",
      },
      {
        id: "log-3",
        actor: "Dr. Connor",
        action: "Updated prescription for Patient #882",
        timeText: "42 mins ago",
        type: "info",
      },
    ];
  },
};
