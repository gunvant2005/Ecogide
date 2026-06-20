import { CATEGORY_COLORS, CATEGORY_LABELS } from "../constants";
import type { FootprintSummary } from "../types";

interface Props {
  summary: FootprintSummary;
  weeklyGoal: number;
  timeframe: number;
  onTimeframeChange: (days: number) => void;
}

export default function Dashboard({ summary, weeklyGoal, timeframe, onTimeframeChange }: Props) {
  const maxCat = Math.max(...Object.values(summary.by_category), 1);
  const goalPct = Math.min((summary.total_kg / weeklyGoal) * 100, 100);
  const overGoal = summary.total_kg > weeklyGoal;

  return (
    <section aria-labelledby="dashboard-heading">
      <div className="card stat-hero" style={{ marginBottom: "1.25rem" }}>
        <p className="stat-value" aria-live="polite">
          {summary.total_kg}
          <span style={{ fontSize: "1.25rem", fontWeight: 500 }}> kg CO₂e</span>
        </p>
        <p className="stat-label">
          {summary.period_days === 365 ? "All Time (Last 365 days)" : `Last ${summary.period_days} days`}
        </p>
        <p style={{ marginTop: "0.75rem", fontSize: "0.875rem", color: "var(--text-muted)" }}>
          {summary.vs_benchmark_pct > 0 ? (
            <span>{summary.vs_benchmark_pct}% above average urban footprint</span>
          ) : (
            <span>{Math.abs(summary.vs_benchmark_pct)}% below average urban footprint</span>
          )}
        </p>
        <div className="goal-progress">
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.875rem" }}>
            <span>Weekly goal: {weeklyGoal} kg</span>
            <span>{overGoal ? "Over goal" : `${Math.round(goalPct)}% used`}</span>
          </div>
          <div className="goal-track" role="progressbar" aria-valuenow={summary.total_kg} aria-valuemin={0} aria-valuemax={weeklyGoal} aria-label="Weekly goal progress">
            <div className={`goal-fill ${overGoal ? "over" : ""}`} style={{ width: `${Math.min(goalPct, 100)}%` }} />
          </div>
        </div>
      </div>

      <div className="card">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
          <h2 id="dashboard-heading" style={{ margin: 0, fontSize: "1.15rem" }}>Emissions by Category</h2>
          <select
            value={timeframe}
            onChange={(e) => onTimeframeChange(parseInt(e.target.value))}
            className="timeframe-select"
          >
            <option value={7}>Last 7 Days</option>
            <option value={30}>Last 30 Days</option>
            <option value={365}>All Time</option>
          </select>
        </div>
        {Object.entries(summary.by_category).map(([cat, kg]) => (
          <div className="category-bar" key={cat}>
            <div className="category-bar-header">
              <span>{CATEGORY_LABELS[cat] || cat}</span>
              <span>{kg} kg</span>
            </div>
            <div className="category-bar-track">
              <div
                className="category-bar-fill"
                style={{
                  width: `${(kg / maxCat) * 100}%`,
                  background: CATEGORY_COLORS[cat] || varPrimary(),
                }}
              />
            </div>
          </div>
        ))}
        {summary.top_category && (
          <p style={{ marginTop: "1rem", fontSize: "0.875rem", color: "var(--text-muted)" }}>
            Highest impact: <strong>{CATEGORY_LABELS[summary.top_category]}</strong>
          </p>
        )}
      </div>
    </section>
  );
}

function varPrimary() {
  return "#2d6a4f";
}
