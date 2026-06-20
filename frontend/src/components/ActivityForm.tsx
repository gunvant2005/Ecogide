import { FormEvent, useState } from "react";
import { CATEGORY_OPTIONS } from "../constants";
import type { Activity } from "../types";

interface Props {
  onSubmit: (activity: Omit<Activity, "id" | "emissions_kg">) => Promise<void>;
}

export default function ActivityForm({ onSubmit }: Props) {
  const [category, setCategory] = useState<keyof typeof CATEGORY_OPTIONS>("transport");
  const [subType, setSubType] = useState<string>(CATEGORY_OPTIONS.transport.subTypes[0].value);
  const [quantity, setQuantity] = useState("1");
  const [date, setDate] = useState(new Date().toISOString().slice(0, 10));
  const [notes, setNotes] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const catConfig = CATEGORY_OPTIONS[category];

  function handleCategoryChange(newCat: keyof typeof CATEGORY_OPTIONS) {
    setCategory(newCat);
    setSubType(CATEGORY_OPTIONS[newCat].subTypes[0].value);
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    try {
      await onSubmit({
        category,
        sub_type: subType,
        quantity: parseFloat(quantity),
        unit: catConfig.unit,
        date,
        notes,
      });
      setQuantity("1");
      setNotes("");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="card" aria-labelledby="log-form-heading">
      <h2 id="log-form-heading">Log Activity</h2>

      <div className="form-group">
        <label htmlFor="category">Category</label>
        <select id="category" value={category} onChange={(e) => handleCategoryChange(e.target.value as keyof typeof CATEGORY_OPTIONS)}>
          {Object.entries(CATEGORY_OPTIONS).map(([key, cfg]) => (
            <option key={key} value={key}>{cfg.label}</option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="subType">Type</label>
        <select id="subType" value={subType} onChange={(e) => setSubType(e.target.value)}>
          {catConfig.subTypes.map((st) => (
            <option key={st.value} value={st.value}>{st.label}</option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="quantity">Quantity ({catConfig.unit})</label>
        <input id="quantity" type="number" min="0.1" step="0.1" required value={quantity} onChange={(e) => setQuantity(e.target.value)} />
      </div>

      <div className="form-group">
        <label htmlFor="date">Date</label>
        <input id="date" type="date" required value={date} onChange={(e) => setDate(e.target.value)} />
      </div>

      <div className="form-group">
        <label htmlFor="notes">Notes (optional)</label>
        <textarea id="notes" rows={2} value={notes} onChange={(e) => setNotes(e.target.value)} />
      </div>

      <button type="submit" className="btn btn-primary" disabled={submitting}>
        {submitting ? "Saving…" : "Log Activity"}
      </button>
    </form>
  );
}
