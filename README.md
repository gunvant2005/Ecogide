# EcoGuide — Carbon Footprint Assistant

EcoGuide helps individuals **understand, track, and reduce** their carbon footprint through simple activity logging, personalized insights, and a context-aware smart assistant.

## Chosen Vertical

**Urban Professional** — a city-dwelling individual who commutes daily, eats out regularly, and uses home energy. This persona needs practical, low-friction tools to see where emissions come from and which small swaps have the biggest impact.

## Approach and Logic

### Architecture

```
┌─────────────┐     REST API      ┌──────────────────────────────────┐
│  React UI   │ ◄──────────────► │  Flask Backend                    │
│  Dashboard  │                   │  ┌─────────────────────────────┐  │
│  Log Form   │                   │  │ Carbon Calculator           │  │
│  Assistant  │                   │  │ (emission factors × qty)    │  │
└─────────────┘                   │  ├─────────────────────────────┤  │
                                  │  │ Insights Engine             │  │
                                  │  │ (benchmark + goal analysis) │  │
                                  │  ├─────────────────────────────┤  │
                                  │  │ Assistant Engine            │  │
                                  │  │ (intent + context routing)  │  │
                                  │  └─────────────────────────────┘  │
                                  └──────────────────────────────────┘
```

### Decision Logic

1. **Emission calculation** — Each logged activity is multiplied by a standard kg CO₂e factor (transport per km, food per meal, energy per kWh, shopping per item).

2. **Context aggregation** — The system summarizes the last 7 days by category, compares against a weekly urban benchmark (120 kg), and tracks progress toward the user's personal goal.

3. **Insight prioritization** — Rules rank insights by:
   - Whether the user exceeds benchmark or personal goal
   - Which category contributes the highest share of emissions
   - Profile attributes (primary transport mode, diet type)

4. **Assistant routing** — Natural-language messages are classified by intent (greeting, footprint status, transport help, reduction tips, etc.). Responses are generated from live user data — not generic advice.

5. **Recommendations** — Action cards estimate savings in kg CO₂e and difficulty, targeting the user's highest-impact category first.

## How It Works

### Quick Start

**Prerequisites:** Python 3.10+, Node.js 18+

```bash
# Terminal 1 — Backend
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
python -m app.main

# Terminal 2 — Frontend
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** in your browser.

### User Flow

1. **Set up profile** — Name, transport mode, diet, weekly goal
2. **Log activities** — Transport (km), meals, energy (kWh), shopping
3. **View dashboard** — Total footprint, category breakdown, goal progress
4. **Read insights** — Personalized observations based on your data
5. **Chat with EcoGuide** — Ask "How am I doing?", "Tips to reduce", etc.

Click **Load demo data** on the dashboard to explore with sample activities.

### Running Tests

```bash
cd backend
pip install -r requirements.txt
pytest -v
```

## Assumptions

| Assumption | Rationale |
|---|---|
| Emission factors are approximate averages | Based on IPCC/EPA-style estimates for educational use; real values vary by region and supplier |
| Single-user local storage (JSON files) | Keeps the demo self-contained without requiring a database |
| Weekly 120 kg urban benchmark | Represents a simplified average for comparison, not a scientific standard |
| Rule-based assistant (no external LLM API) | Ensures reproducibility, zero API cost, and deterministic evaluation |
| Activities are self-reported | Users manually log trips and meals rather than integrating with vehicle/telematics APIs |

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py              # REST API endpoints
│   │   ├── models.py            # Pydantic schemas
│   │   ├── constants.py         # Emission factors
│   │   └── services/
│   │       ├── carbon_calculator.py
│   │       ├── insights_engine.py
│   │       ├── assistant_engine.py
│   │       └── storage.py
│   └── tests/
├── frontend/
│   └── src/
│       ├── App.tsx
│       └── components/
└── README.md
```

## Evaluation Alignment

| Focus Area | Implementation |
|---|---|
| **Code Quality** | Modular services, typed models, separation of concerns |
| **Security** | Input validation, no secrets, CORS restricted to dev origins |
| **Efficiency** | Lightweight stack, JSON file storage, no heavy dependencies |
| **Testing** | 13 unit/integration tests covering calculator, assistant, and API |
| **Accessibility** | Semantic HTML, ARIA labels, keyboard navigation, focus styles, screen-reader live regions |

## License

MIT — built for educational and challenge submission purposes.
