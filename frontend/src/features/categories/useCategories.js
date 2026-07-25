import { api } from "@/lib/api";
import { queryKeys } from "@/lib/queryKeys";
import { useQuery } from "@tanstack/react-query";

async function getCategories(profileId) {
  const res = await api.get(`/profiles/${profileId}/categories`);
  return res.data;
}

export function useCategories(profileId) {
  return useQuery({
    queryKey: queryKeys.categories.byProfileId.all(profileId),
    queryFn: () => getCategories(profileId),
    enabled: !!profileId,
  });
}
