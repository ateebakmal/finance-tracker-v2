import { api } from "@/lib/api";
import { queryKeys } from "@/lib/queryKeys";
import { useQuery } from "@tanstack/react-query";

async function fetchTransactions(profileId) {
  const res = await api.get(`/profiles/${profileId}/transactions`);
  return res.data;
}

export function useTransaction(profileId) {
  return useQuery({
    queryKey: queryKeys.transactions.byProfileId.all(profileId),
    queryFn: () => fetchTransactions(profileId),
    enabled: !!profileId,
    staleTime: 5 * 60 * 1000,
    refetchOnReconnect: true,
  });
}
