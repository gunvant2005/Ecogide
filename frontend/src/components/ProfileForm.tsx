import { FormEvent, useState } from "react";
import { DIET_OPTIONS, TRANSPORT_OPTIONS } from "../constants";
import type { UserProfile } from "../types";

interface Props {
  profile: UserProfile;
  onSave: (profile: UserProfile) => Promise<void>;
}

export default function ProfileForm({ profile, onSave }: Props) {
  const [form, setForm] = useState(profile);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setSaving(true);
    setSaved(false);
    try {
      await onSave(form);
      setSaved(true);
    } finally {
      setSaving(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="card" aria-labelledby="profile-heading">
      <h2 id="profile-heading">Your Profile</h2>
      <p style={{ fontSize: "0.875rem", color: "var(--text-muted)", marginTop: "-0.5rem" }}>
        Personalize calculations and assistant recommendations.
      </p>

      <div className="form-group">
        <label htmlFor="name">Name</label>
        <input id="name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
      </div>

      <div className="form-group">
        <label htmlFor="household">Household size</label>
        <input id="household" type="number" min={1} max={10} value={form.household_size} onChange={(e) => setForm({ ...form, household_size: +e.target.value })} />
      </div>

      <div className="form-group">
        <label htmlFor="transport">Primary transport</label>
        <select id="transport" value={form.primary_transport} onChange={(e) => setForm({ ...form, primary_transport: e.target.value })}>
          {TRANSPORT_OPTIONS.map((o) => (
            <option key={o.value} value={o.value}>{o.label}</option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="diet">Typical diet</label>
        <select id="diet" value={form.diet_type} onChange={(e) => setForm({ ...form, diet_type: e.target.value })}>
          {DIET_OPTIONS.map((o) => (
            <option key={o.value} value={o.value}>{o.label}</option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="goal">Weekly carbon goal (kg CO₂e)</label>
        <input id="goal" type="number" min={10} max={500} step={5} value={form.weekly_goal_kg} onChange={(e) => setForm({ ...form, weekly_goal_kg: +e.target.value })} />
      </div>

      <div className="form-group">
        <label htmlFor="home">Home type</label>
        <select id="home" value={form.home_type} onChange={(e) => setForm({ ...form, home_type: e.target.value })}>
          <option value="apartment">Apartment</option>
          <option value="house">House</option>
          <option value="shared">Shared housing</option>
        </select>
      </div>

      <button type="submit" className="btn btn-primary" disabled={saving}>
        {saving ? "Saving…" : "Save Profile"}
      </button>
      {saved && <p role="status" style={{ color: "var(--primary)", fontSize: "0.875rem", marginTop: "0.75rem" }}>Profile saved.</p>}
    </form>
  );
}
