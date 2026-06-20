import type { Insight, Recommendation } from "../types";

interface Props {
  insights: Insight[];
  recommendations: Recommendation[];
}

export default function InsightsPanel({ insights, recommendations }: Props) {
  return (
    <div className="grid-2">
      <div className="card">
        <h2>Personalized Insights</h2>
        {insights.length === 0 ? (
          <p className="empty-state">Log activities to unlock insights.</p>
        ) : (
          insights.map((ins, i) => (
            <article className="insight-card" key={i}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <h3>{ins.title}</h3>
                <span className={`badge badge-${ins.priority}`}>{ins.priority}</span>
              </div>
              <p>{ins.description}</p>
              {ins.impact_kg > 0 && (
                <p style={{ marginTop: "0.5rem", fontSize: "0.8rem", color: "var(--primary)" }}>
                  Potential impact: {ins.impact_kg} kg CO₂e
                </p>
              )}
            </article>
          ))
        )}
      </div>

      <div className="card">
        <h2>Recommended Actions</h2>
        {recommendations.length === 0 ? (
          <p className="empty-state">No recommendations yet.</p>
        ) : (
          recommendations.map((rec, i) => (
            <article className="rec-card" key={i}>
              <h3>{rec.action}</h3>
              <p style={{ fontSize: "0.875rem", color: "var(--text-muted)", margin: 0 }}>{rec.reason}</p>
              <div className="rec-meta">
                <span>Save ~{rec.estimated_savings_kg} kg</span>
                <span>{rec.difficulty} difficulty</span>
                <span>{rec.category}</span>
              </div>
            </article>
          ))
        )}
      </div>
    </div>
  );
}
