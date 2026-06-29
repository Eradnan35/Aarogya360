import { useQuery } from "@tanstack/react-query";
import { dashboardService } from "@/services/dashboard.service";

export const useDashboardStats = () => {
  return useQuery({
    queryKey: ["dashboard", "stats"],
    queryFn: () => dashboardService.getStats(),
  });
};

export const usePatientGrowth = () => {
  return useQuery({
    queryKey: ["dashboard", "growth"],
    queryFn: () => dashboardService.getPatientGrowth(),
  });
};

export const useAppointmentDistribution = () => {
  return useQuery({
    queryKey: ["dashboard", "distribution"],
    queryFn: () => dashboardService.getAppointmentDistribution(),
  });
};

export const useLiveQueue = () => {
  return useQuery({
    queryKey: ["dashboard", "queue"],
    queryFn: () => dashboardService.getLiveQueue(),
    refetchInterval: 10000, // Refresh queue every 10 seconds (live clinical feel)
  });
};

export const useUpcomingAppointments = () => {
  return useQuery({
    queryKey: ["dashboard", "upcoming"],
    queryFn: () => dashboardService.getUpcomingAppointments(),
  });
};

export const useActivityLogs = () => {
  return useQuery({
    queryKey: ["dashboard", "activity"],
    queryFn: () => dashboardService.getActivityLogs(),
  });
};
