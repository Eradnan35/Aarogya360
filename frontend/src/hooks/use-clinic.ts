import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { clinicService } from "@/services/clinic.service";
import { Clinic } from "@/types/api";

export const useMyClinic = () => {
  return useQuery({
    queryKey: ["clinic", "me"],
    queryFn: () => clinicService.getMyClinic(),
  });
};

export const useUpdateClinicMutation = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (input: Partial<Clinic>) => clinicService.updateClinic(input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["clinic"] });
    },
  });
};
