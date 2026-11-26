# AI Finance Agent

A natural-language expense tracker powered by the **OpenAI Agents SDK** and **Streamlit**. Log expenses by chatting ("I spent $12 on lunch"), then explore totals, category breakdowns, and charts in a clean dashboard.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-Agents%20SDK-412991?logo=openai&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- **Chat-based expense tracking** — record expenses in plain English
- **AI agent with tools** — the model decides when to record, total, list, or analyze
- **Live dashboard** — total spending, average expense, and recent transactions
- **Analytics tab** — category breakdown and spending charts with Plotly
- **Quick actions** — one-click totals, averages, recent expenses, and category summaries
- **Local SQLite storage** — no external database required

## How it works

```
Streamlit UI
   │
   ▼
OpenAI Agent (gpt-4.1-mini)
   │  tool calls
   ├── record_expense
   ├── show_total_spending
   ├── show_average_spending
   ├── list_recent_expenses
   └── analyze_spending_by_category
   │
   ▼
SQLite (finance.db)
```

## Tech stack

| Layer | Technology |
| --- | --- |
| UI | Streamlit |
| Agent | OpenAI Agents SDK (`openai-agents`) |
| Model | `gpt-4.1-mini` |
| Charts | Plotly, pandas |
| Storage | SQLite |

## Project structure

```
.
├── app.py           # Streamlit dashboard and chat UI
├── agent.py         # Agent definition, tools, and runner
├── db.py            # SQLite data access layer
├── requirements.txt
├── .env.example
└── README.md
```

## Getting started

**Prerequisites:** Python 3.10+ and an [OpenAI API key](https://platform.openai.com/api-keys).

```bash
git clone https://github.com/Ahmad-1276/finance_agent_sdk.git
cd finance_agent_sdk

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# open .env and set OPENAI_API_KEY=sk-...

streamlit run app.py
```

Streamlit opens <http://localhost:8501>.

The SQLite database (`finance.db`) is created automatically on first run and is ignored by Git.

## Usage examples

- `I spent 45 on groceries`
- `How much did I spend in total?`
- `Show my average expense`
- `What did I buy recently?`
- `Break down my spending by category`

## Configuration

| Variable | Description |
| --- | --- |
| `OPENAI_API_KEY` | OpenAI API key used by the agent |

## License

MIT — see [LICENSE](LICENSE).
