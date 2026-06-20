import { useCallback, useEffect, useState } from "react";
import { api } from "./api";
import ActivityForm from "./components/ActivityForm";
import ActivityList from "./components/ActivityList";
import AssistantChat from "./components/AssistantChat";
import Dashboard from "./components/Dashboard";
import InsightsPanel from "./components/InsightsPanel";
import ProfileForm from "./components/ProfileForm";
import Simulator from "./components/Simulator";
import type { Activity, FootprintSummary, Insight, Recommendation, UserProfile } from "./types";

type Tab = "dashboard" | "log" | "simulator" | "assistant" | "profile";

const TABS: { id: Tab; label: string }[] = [
  { id: "dashboard", label: "Dashboard" },
  { id: "log", label: "Log Activity" },
  { id: "simulator", label: "Simulator" },
  { id: "assistant", label: "Assistant" },
  { id: "profile", label: "Profile" },
];

export default function App() {
  const [tab, setTab] = useState<Tab>("dashboard");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [summary, setSummary] = useState<FootprintSummary | null>(null);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [insights, setInsights] = useState<Insight[]>([]);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [timeframe, setTimeframe] = useState<number>(7);

  const refresh = useCallback(async (days = timeframe) => {
    try {
      const [p, s, a, ins, rec] = await Promise.all([
        api.getProfile(),
        api.getSummary(days),
        api.getActivities(days === 365 ? 365 : days * 2),
        api.getInsights(),
        api.getRecommendations(),
      ]);
      setProfile(p);
      setSummary(s);
      setActivities(a);
      setInsights(ins);
      setRecommendations(rec);
      setError("");
    } catch {
      setError("Cannot connect to the API. Start the backend with: uvicorn app.main:app --reload");
    } finally {
      setLoading(false);
    }
  }, [timeframe]);

  useEffect(() => {
    refresh(timeframe);
  }, [refresh, timeframe]);

  async function handleLog(activity: Omit<Activity, "id" | "emissions_kg">) {
    await api.createActivity(activity);
    await refresh();
  }

  async function handleDelete(id: string) {
    await api.deleteActivity(id);
    await refresh();
  }

  async function handleSaveProfile(p: UserProfile) {
    await api.updateProfile(p);
    await refresh();
  }

  async function handleSeedDemo() {
    await api.seedDemo();
    await refresh();
    setTab("dashboard");
  }

  if (loading) {
    return <div className="loading" role="status">Loading EcoGuide…</div>;
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="brand">
          <div className="brand-icon" aria-hidden="true">🌿</div>
          <div>
            <h1>EcoGuide</h1>
            <p>Track · Understand · Reduce</p>
          </div>
        </div>
        <nav aria-label="Main navigation">
          <div className="nav-tabs">
            {TABS.map((t) => (
              <button
                key={t.id}
                className={`nav-tab ${tab === t.id ? "active" : ""}`}
                onClick={() => setTab(t.id)}
                aria-current={tab === t.id ? "page" : undefined}
              >
                {t.label}
              </button>
            ))}
          </div>
        </nav>
      </header>

      {error && (
        <div className="error-banner" role="alert">
          {error}
        </div>
      )}

      {tab === "dashboard" && summary && profile && (
        <>
          <Dashboard
            summary={summary}
            weeklyGoal={profile.weekly_goal_kg}
            timeframe={timeframe}
            onTimeframeChange={setTimeframe}
          />
          <div style={{ marginTop: "1.25rem" }}>
            <InsightsPanel insights={insights} recommendations={recommendations} />
          </div>
          {summary.total_kg === 0 && (
            <div style={{ marginTop: "1.25rem", textAlign: "center" }}>
              <button className="btn btn-secondary" onClick={handleSeedDemo}>
                Load demo data
              </button>
            </div>
          )}
        </>
      )}

      {tab === "log" && (
        <div className="grid-2">
          <ActivityForm onSubmit={handleLog} />
          <ActivityList activities={activities} onDelete={handleDelete} />
        </div>
      )}

      {tab === "simulator" && (
        <Simulator summary={summary} weeklyGoal={profile ? profile.weekly_goal_kg : 80} />
      )}

      {tab === "assistant" && <AssistantChat />}

      {tab === "profile" && profile && (
        <ProfileForm profile={profile} onSave={handleSaveProfile} />
      )}
    </div>
  );
}
