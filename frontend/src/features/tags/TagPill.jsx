export default function TagPill({ name }) {
  return (
    <span className="bg-card text-ink flex items-center gap-1 rounded-full border border-dashed border-[#C7CBF2] px-3.5 py-2 font-sans text-[13.5px] font-bold">
      <span className="text-accent">#</span>
      {name}
    </span>
  );
}
