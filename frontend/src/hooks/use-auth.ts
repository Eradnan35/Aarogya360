import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { authService } from "@/services/auth.service";

export const useAuthMe = () => {
  return useQuery({
    queryKey: ["auth", "me"],
    queryFn: () => authService.getMe(),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useAuthSessions = () => {
  return useQuery({
    queryKey: ["auth", "sessions"],
    queryFn: () => authService.getSessions(),
  });
};

export const useLogoutMutation = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => authService.logout(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["auth"] });
    },
  });
};
