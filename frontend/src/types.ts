export interface UserProfile {
  name: string;
  household_size: number;
  primary_transport: string;
  diet_type: string;
  weekly_goal_kg: number;
  home_type: string;
}

export interface Activity {
  id?: string;
  category: string;
  sub_type: string;
  quantity: number;
  unit: string;
  date: string;
  notes?: string;
  emissions_kg?: number;
}

export interface FootprintSummary {
  total_kg: number;
  by_category: Record<string, number>;
  period_days: number;
  vs_benchmark_pct: number;
  vs_goal_pct: number;
  top_category: string | null;
}

export interface Insight {
  title: string;
  description: string;
  impact_kg: number;
  priority: string;
}

export interface Recommendation {
  action: string;
  category: string;
  estimated_savings_kg: number;
  difficulty: string;
  reason: string;
}

export interface AssistantMessage {
  role: "user" | "assistant";
  content: string;
  suggested_actions?: string[];
}

export interface ChatResponse {
  reply: string;
  suggested_actions: string[];
  intent: string;
}
