function toISO(d) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}
function daysAgoISO(n) {
  const d = new Date();
  d.setDate(d.getDate() - n);
  return toISO(d);
}

export function relativeDate(iso) {
  if (iso === toISO(new Date())) return "Today";
  if (iso === daysAgoISO(1)) return "Yesterday";
  return new Date(iso + "T00:00:00").toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
  });
}

export function groupByBucket(transactions) {
  const today = toISO(new Date());
  const yest = daysAgoISO(1);
  const weekAgo = daysAgoISO(7);
  const g = { today: [], yesterday: [], week: [], earlier: [] };
  for (const t of transactions) {
    const d = t.transaction_date;
    if (d === today) g.today.push(t);
    else if (d === yest) g.yesterday.push(t);
    else if (d > weekAgo) g.week.push(t);
    else g.earlier.push(t);
  }
  return [
    { label: "Today", items: g.today },
    { label: "Yesterday", items: g.yesterday },
    { label: "This week", items: g.week },
    { label: "Earlier", items: g.earlier },
  ].filter((grp) => grp.items.length > 0);
}
