import { useMemo, useState } from "react";
import { useProfile } from "@/features/profiles/useProfile";
import { useTransaction } from "./useTransaction.js";
import { groupByBucket } from "./utils";
import TransactionRow from "./TransactionRow";
import Segmented from "@/components/Segmented";
import Card from "@/components/Card";
import IconChip from "@/components/IconChip";
import { SearchIcon, TargetIcon, RepeatIcon } from "@/components/icons";

export default function TransactionsPage() {
  const { activeProfileId } = useProfile();
  const {
    data: all = [],
    isLoading,
    isError,
  } = useTransaction(activeProfileId);

  const [filter, setFilter] = useState("all");
  const [showSearch, setShowSearch] = useState(false);
  const [query, setQuery] = useState("");

  const groups = useMemo(() => {
    const filtered = all.filter((t) => {
      if (filter !== "all" && t.transaction_type !== filter) return false;
      if (query) {
        const hay =
          `${t.description ?? ""} ${t.category?.category_name ?? ""}`.toLowerCase();
        if (!hay.includes(query.toLowerCase())) return false;
      }
      return true;
    });
    return groupByBucket(filtered);
  }, [all, filter, query]);

  console.log(all);
  return (
    <div className="space-y-5 px-5 pt-6">
      <div className="flex items-center justify-between">
        <h1 className="text-ink font-sans text-[22px] font-extrabold tracking-[-0.02em]">
          Transactions
        </h1>
        <button
          onClick={() => setShowSearch((v) => !v)}
          className="border-line bg-card text-muted grid h-9 w-9 place-items-center rounded-xl border"
          aria-label="Search"
        >
          <SearchIcon className="h-5 w-5" />
        </button>
      </div>

      {showSearch && (
        <input
          autoFocus
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search transactions"
          className="border-line bg-card text-ink placeholder:text-faint focus:border-accent w-full rounded-2xl border px-4 py-3 font-sans text-[14px] focus:outline-none"
        />
      )}

      <div className="flex gap-3">
        <button
          onClick={() => {}}
          className="border-line bg-card flex flex-1 items-center gap-3 rounded-[18px] border p-4"
        >
          <IconChip tone="neutral">
            <TargetIcon className="h-5 w-5" />
          </IconChip>
          <span className="text-ink font-sans text-[14.5px] font-bold">
            Budgets
          </span>
        </button>
        <button
          onClick={() => {}}
          className="border-line bg-card flex flex-1 items-center gap-3 rounded-[18px] border p-4"
        >
          <IconChip tone="neutral">
            <RepeatIcon className="h-5 w-5" />
          </IconChip>
          <span className="text-ink font-sans text-[14.5px] font-bold">
            Recurring
          </span>
        </button>
      </div>

      <Segmented
        value={filter}
        onChange={setFilter}
        options={[
          { value: "all", label: "All" },
          { value: "income", label: "Income" },
          { value: "expense", label: "Expense" },
        ]}
      />

      {isLoading ? (
        <p className="text-muted text-[13px]">Loading…</p>
      ) : isError ? (
        <p className="text-neg text-[13px]">Couldn’t load transactions.</p>
      ) : groups.length === 0 ? (
        <p className="text-muted text-[13px]">No transactions found.</p>
      ) : (
        groups.map((g) => (
          <div key={g.label} className="space-y-2">
            <p className="text-faint px-1 text-[11px] font-bold tracking-[0.1em] uppercase">
              {g.label}
            </p>
            <Card className="divide-line divide-y px-4">
              {g.items.map((t) => (
                <TransactionRow key={t.id} transaction={t} />
              ))}
            </Card>
          </div>
        ))
      )}
    </div>
  );
}
