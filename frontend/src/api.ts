const BASE = "/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || res.statusText);
  }
  return res.json();
}

export const api = {
  health: () => request<{ status: string }>("/health"),
  getProfile: () => request<import("./types").UserProfile>("/profile"),
  updateProfile: (profile: import("./types").UserProfile) =>
    request("/profile", { method: "PUT", body: JSON.stringify(profile) }),
  getActivities: (days = 30) => request<import("./types").Activity[]>(`/activities?days=${days}`),
  createActivity: (activity: Omit<import("./types").Activity, "id" | "emissions_kg">) =>
    request("/activities", { method: "POST", body: JSON.stringify(activity) }),
  deleteActivity: (id: string) => request(`/activities/${id}`, { method: "DELETE" }),
  getSummary: (days = 7) => request<import("./types").FootprintSummary>(`/footprint/summary?days=${days}`),
  getInsights: () => request<import("./types").Insight[]>("/insights"),
  getRecommendations: () => request<import("./types").Recommendation[]>("/recommendations"),
  chat: (message: string) =>
    request<import("./types").ChatResponse>("/assistant/chat", {
      method: "POST",
      body: JSON.stringify({ message }),
    }),
  seedDemo: () => request<{ seeded: boolean }>("/demo/seed", { method: "POST" }),
};
