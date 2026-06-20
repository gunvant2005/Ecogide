import { useState } from "react";
import type { FootprintSummary } from "../types";

interface Props {
  summary: FootprintSummary | null;
  weeklyGoal: number;
}

export default function Simulator({ summary, weeklyGoal }: Props) {
  const currentFootprint = summary?.total_kg || 0;
  const recentEnergy = summary?.by_category?.energy || 0;

  // Sliders state
  const [carSwappedKm, setCarSwappedKm] = useState(0);
  const [beefSwappedMeals, setBeefSwappedMeals] = useState(0);
  const [thermostatCelsius, setThermostatCelsius] = useState(0);
  const [ledLighting, setLedLighting] = useState(false);

  // Carbon saving calculations (coefficients in kg CO2e)
  const transportSavings = carSwappedKm * (0.21 - 0.04); // petrol car (0.21) vs train (0.04)
  const foodSavings = beefSwappedMeals * (6.5 - 0.85); // beef (6.5) vs vegan/vegetarian average (0.85)
  const thermostatSavings = thermostatCelsius * (recentEnergy > 0 ? recentEnergy * 0.08 : 3.0);
  const lightingSavings = ledLighting ? 5.0 : 0.0;

  const totalWeeklySavings = parseFloat(
    (transportSavings + foodSavings + thermostatSavings + lightingSavings).toFixed(1)
  );
  
  const simulatedFootprint = Math.max(0, parseFloat((currentFootprint - totalWeeklySavings).toFixed(1)));

  // Tree Offset Math (1 mature tree absorbs ~22 kg CO2e per year, which is ~0.42 kg per week)
  const currentTreesNeeded = Math.ceil(currentFootprint / 0.42);
  const simulatedTreesNeeded = Math.ceil(simulatedFootprint / 0.42);
  const treesSaved = Math.max(0, currentTreesNeeded - simulatedTreesNeeded);

  // SVG Chart rendering dimensions
  const chartHeight = 180;
  const chartWidth = 400;
  const barPadding = 12;
  const maxVal = Math.max(120, currentFootprint, simulatedFootprint, weeklyGoal, 10);
  
  const getBarHeight = (val: number) => (val / maxVal) * (chartHeight - 40);

  const chartData = [
    { label: "Benchmark", val: 120, color: "#9ca3af" },
    { label: "Goal", val: weeklyGoal, color: "#40916c" },
    { label: "Current", val: currentFootprint, color: "#c1121f" },
    { label: "Simulated", val: simulatedFootprint, color: "#52b788" },
  ];

  return (
    <div className="grid-2">
      <div className="card glass-card">
        <h2 style={{ fontFamily: "var(--font-display)", color: "var(--primary)", margin: "0 0 1.25rem 0" }}>
          Habit Simulator
        </h2>
        <p style={{ fontSize: "0.9rem", color: "var(--text-muted)", marginBottom: "1.5rem" }}>
          Drag the sliders to see how making simple swaps in your daily routine can reduce your weekly carbon footprint.
        </p>

        {/* Transport Swap */}
        <div className="form-group slider-group">
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.5rem" }}>
            <span className="slider-label">🚗 Commute Swap (Petrol Car → Train)</span>
            <span className="slider-value"><strong>{carSwappedKm} km</strong>/wk</span>
          </div>
          <input
            type="range"
            min="0"
            max="150"
            step="5"
            value={carSwappedKm}
            onChange={(e) => setCarSwappedKm(parseInt(e.target.value))}
            className="styled-slider"
          />
          <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
            Saves ~{transportSavings.toFixed(1)} kg CO₂e
          </span>
        </div>

        {/* Diet Swap */}
        <div className="form-group slider-group" style={{ marginTop: "1.25rem" }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.5rem" }}>
            <span className="slider-label">🥩 Diet Swap (Beef → Plant-based)</span>
            <span className="slider-value"><strong>{beefSwappedMeals} meals</strong>/wk</span>
          </div>
          <input
            type="range"
            min="0"
            max="14"
            step="1"
            value={beefSwappedMeals}
            onChange={(e) => setBeefSwappedMeals(parseInt(e.target.value))}
            className="styled-slider"
          />
          <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
            Saves ~{foodSavings.toFixed(1)} kg CO₂e
          </span>
        </div>

        {/* Thermostat Swap */}
        <div className="form-group slider-group" style={{ marginTop: "1.25rem" }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.5rem" }}>
            <span className="slider-label">🌡️ Thermostat Reduction</span>
            <span className="slider-value"><strong>-{thermostatCelsius}°C</strong></span>
          </div>
          <input
            type="range"
            min="0"
            max="3"
            step="1"
            value={thermostatCelsius}
            onChange={(e) => setThermostatCelsius(parseInt(e.target.value))}
            className="styled-slider"
          />
          <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
            Saves ~{thermostatSavings.toFixed(1)} kg CO₂e (8% of heating emissions per degree)
          </span>
        </div>

        {/* Home Lighting Toggle */}
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginTop: "1.5rem", borderTop: "1px solid var(--border)", paddingTop: "1rem" }}>
          <div>
            <span className="slider-label" style={{ display: "block", fontWeight: "600" }}>💡 Switch to LED Lighting</span>
            <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>Replaces standard incandescent bulbs (saves 5 kg CO₂e/wk)</span>
          </div>
          <input
            type="checkbox"
            id="ledToggle"
            checked={ledLighting}
            onChange={(e) => setLedLighting(e.target.checked)}
            style={{ width: "20px", height: "20px", cursor: "pointer", accentColor: "var(--primary)" }}
          />
        </div>
      </div>

      <div className="card glass-card" style={{ display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
        <div>
          <h2 style={{ fontFamily: "var(--font-display)", color: "var(--primary)", margin: "0 0 1.25rem 0" }}>
            Simulated Impact
          </h2>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem", marginBottom: "1.25rem" }}>
            <div style={{ background: "var(--surface-alt)", padding: "0.75rem", borderRadius: "8px", textAlign: "center" }}>
              <span style={{ fontSize: "0.75rem", color: "var(--text-muted)", display: "block" }}>Weekly Savings</span>
              <strong style={{ fontSize: "1.5rem", color: "var(--primary-light)" }}>-{totalWeeklySavings} kg</strong>
            </div>
            <div style={{ background: "var(--surface-alt)", padding: "0.75rem", borderRadius: "8px", textAlign: "center" }}>
              <span style={{ fontSize: "0.75rem", color: "var(--text-muted)", display: "block" }}>Simulated Footprint</span>
              <strong style={{ fontSize: "1.5rem", color: simulatedFootprint <= weeklyGoal ? "var(--primary)" : "var(--danger)" }}>
                {simulatedFootprint} kg
              </strong>
            </div>
          </div>

          {/* SVG Visual Graph */}
          <div style={{ display: "flex", justifyContent: "center", margin: "1rem 0" }}>
            <svg width={chartWidth} height={chartHeight} viewBox={`0 0 ${chartWidth} ${chartHeight}`} style={{ overflow: "visible" }}>
              {chartData.map((d, i) => {
                const barH = getBarHeight(d.val);
                const barW = (chartWidth - barPadding * 5) / 4;
                const x = barPadding + i * (barW + barPadding);
                const y = chartHeight - barH - 30;

                return (
                  <g key={d.label}>
                    {/* Bar */}
                    <rect
                      x={x}
                      y={y}
                      width={barW}
                      height={barH}
                      fill={d.color}
                      rx="4"
                      style={{ transition: "all 0.5s ease-in-out" }}
                    />
                    {/* Value label */}
                    <text
                      x={x + barW / 2}
                      y={y - 8}
                      textAnchor="middle"
                      fontSize="0.8rem"
                      fontWeight="bold"
                      fill="var(--text)"
                    >
                      {d.val} kg
                    </text>
                    {/* Category Label */}
                    <text
                      x={x + barW / 2}
                      y={chartHeight - 10}
                      textAnchor="middle"
                      fontSize="0.75rem"
                      fill="var(--text-muted)"
                    >
                      {d.label}
                    </text>
                  </g>
                );
              })}
              <line
                x1="0"
                y1={chartHeight - 30}
                x2={chartWidth}
                y2={chartHeight - 30}
                stroke="var(--border)"
                strokeWidth="1"
              />
            </svg>
          </div>
        </div>

        {/* Tree Offset Section */}
        <div style={{ borderTop: "1px solid var(--border)", paddingTop: "1rem", marginTop: "1rem", display: "flex", gap: "1rem", alignItems: "center" }}>
          <div style={{ fontSize: "2rem" }}>🌳</div>
          <div>
            <span style={{ fontWeight: "600", fontSize: "0.9rem", display: "block" }}>
              Annual Offset Requirement
            </span>
            <span style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>
              Current: <strong>{currentTreesNeeded}</strong> trees vs. Simulated: <strong>{simulatedTreesNeeded}</strong> trees.
              {treesSaved > 0 && (
                <span style={{ color: "var(--primary-light)", fontWeight: "600" }}>
                  {" "}Saving {treesSaved} trees annually!
                </span>
              )}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
