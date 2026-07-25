export const queryKeys = {
  transactions: {
    byProfileId: {
      all: (profileId) => ["transactions", "all", profileId],
      summary: (profileId) => ["transactions", "summary", profileId],
    },
  },
  categories: {
    byProfileId: {
      all: (profileId) => ["categories", "all", profileId],
    },
  },
  tags: {
    byProfileId: {
      all: (profileId) => ["tags", "all", profileId],
    },
  },
};
