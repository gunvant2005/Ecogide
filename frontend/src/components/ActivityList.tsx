import { CATEGORY_LABELS } from "../constants";
import type { Activity } from "../types";

interface Props {
  activities: Activity[];
  onDelete: (id: string) => void;
}

export default function ActivityList({ activities, onDelete }: Props) {
  if (activities.length === 0) {
    return (
      <div className="card empty-state">
        <p>No activities logged yet. Add your first one to start tracking.</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h2>Recent Activities</h2>
      <ul className="activity-list" aria-label="Recent activities">
        {activities.map((a) => (
          <li className="activity-item" key={a.id}>
            <div>
              <strong>{CATEGORY_LABELS[a.category] || a.category}</strong>
              <div className="activity-meta">
                {a.sub_type.replace(/_/g, " ")} · {a.quantity} {a.unit} · {a.date}
              </div>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
              <span className="emissions-tag">{a.emissions_kg?.toFixed(1)} kg</span>
              {a.id && (
                <button
                  className="btn btn-ghost"
                  style={{ padding: "0.3rem 0.6rem", fontSize: "0.75rem" }}
                  onClick={() => onDelete(a.id!)}
                  aria-label={`Delete ${a.category} activity from ${a.date}`}
                >
                  Delete
                </button>
              )}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
