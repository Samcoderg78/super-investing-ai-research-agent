# Super Investing — AI Innovator Intern Assignment

A source-grounded AI research agent that analyzes a predefined collection of research documents and generates a structured investment research brief for **Sarvottam Cables Ltd. (NSE: SRVCABLE)**.

> **Important:** SRVCABLE and the company information in this project are fictional and are provided exclusively for the assignment. This project is for research and demonstration purposes, not investment advice.

## Overview

The agent processes a collection of Markdown research documents, identifies relevant evidence, detects a known revenue discrepancy, excludes an unrelated business entity, and generates a structured research brief with traceable source IDs.

The project also compares three prompting strategies to demonstrate how evidence-aware instructions and stricter output requirements can improve the completeness and traceability of LLM-generated research.

## Key Features

- **Document processing:** Loads the supplied Markdown research pack and extracts document metadata and content.
- **Entity filtering:** Excludes the unrelated Sarvottam Cable Network cable-TV operator.
- **Conflict detection:** Identifies the discrepancy between the official revenue figure of INR 1,248 crore and the Business Daily figure of INR 1,428 crore.
- **Evidence-grounded generation:** Supplies relevant documents, source IDs, publication information, and URLs to the language model.
- **Prompt-injection resistance:** Treats document content as untrusted evidence rather than instructions to follow.
- **Structured research output:** Organizes findings into Snapshot, Bull Case, Bear Case, Open Questions, and Sources.
- **Output validation:** Checks required sections, source-ID references, known conflict disclosure, and specified promotional language.
- **Offline mode:** Generates a deterministic research brief without requiring an API key.
- **Experiment modes:** Supports baseline, evidence-aware, and strict prompting strategies.
- **Automated tests:** Includes regression tests for document filtering, conflict detection, required content, citation handling, and promotional-language rejection.

## Architecture

The workflow follows these steps:

1. Load the supplied research documents.
2. Extract document metadata and content.
3. Filter out the known unrelated entity.
4. Build an evidence bundle containing relevant documents and source IDs.
5. Detect the known revenue discrepancy.
6. Generate the research brief using either the Gemini API or the offline generator.
7. Validate the generated output when strict Gemini mode is used.
8. Save the brief to the requested output path.

```text
Research Pack
     |
     v
Document Loading
     |
     v
Relevance and Entity Filtering
     |
     v
Evidence Bundle + Conflict Detection
     |
     v
Prompt Strategy
     |
     +------------------+
     |                  |
     v                  v
 Gemini API        Offline Generator
     |                  |
     v                  |
 Output Validation      |
     |                  |
     +--------+---------+
              |
              v
       Research Brief
```

## Requirements

- Python 3.10 or later recommended.
- The Python standard library for offline execution.
- A Gemini API key for LLM-based generation.

No third-party Python package installation is required for the standard-library implementation.

## Getting Started

Clone the repository and navigate into the project directory:

```bash
git clone https://github.com/Samcoderg78/super-investing-ai-research-agent.git
cd super-investing-ai-research-agent
```

### 1. Run the offline generator

```bash
python agent.py --ticker SRVCABLE --provider offline
```

By default, the output is written to:

```text
outputs/final_brief.md
```

To save the result to a different path:

```bash
python agent.py --ticker SRVCABLE --provider offline --output outputs/offline_brief.md
```

Offline mode is useful for testing the workflow without an API key or making an external model request.

### 2. Run the automated tests

```bash
python -m unittest discover -s tests -v
```

The test suite covers:

- Loading the expected research documents and excluding the unrelated entity.
- Detecting the known revenue discrepancy.
- Checking required research-brief content.
- Rejecting unknown source IDs.
- Rejecting specified promotional stock-tip language.

A passing test suite demonstrates that the tested behaviors work as expected. It does not establish that every generated statement is factually correct.

## Optional: Gemini API Generation

The agent supports Gemini-based research generation. API availability, model access, pricing, and quotas depend on Google's current terms and your account.

### 1. Configure your API key

Obtain an API key through Google AI Studio and set it as an environment variable. Never commit your actual API key to the repository.

**PowerShell:**

```powershell
$env:GEMINI_API_KEY="YOUR_KEY_HERE"
```

Optionally, set the model name:

```powershell
$env:GEMINI_MODEL="gemini-3.5-flash-lite"
```

Use a model identifier currently supported by your Google AI Studio account if this model is unavailable.

### 2. Generate the final research brief

```powershell
python agent.py --ticker SRVCABLE --provider gemini --model gemini-3.5-flash-lite --experiment strict --output outputs/final_brief.md
```

Explicit Gemini mode reports an error if the API call fails instead of silently substituting an offline result.

Alternatively, automatic mode can select Gemini when `GEMINI_API_KEY` is configured and fall back to the offline generator when model generation or validation fails:

```powershell
python agent.py --ticker SRVCABLE --provider auto
```

When using automatic mode, check the console output to confirm which provider generated the brief.

## Prompt Experiments

The agent supports three experiment modes through the `--experiment` argument.

### Experiment 1 — Baseline

```powershell
python agent.py --ticker SRVCABLE --provider gemini --experiment baseline --output outputs/run_1_naive.md
```

Uses a basic prompt focused on a single news article. This provides a baseline for comparing the effects of broader evidence and stricter requirements.

### Experiment 2 — Evidence-aware

```powershell
python agent.py --ticker SRVCABLE --provider gemini --experiment evidence --output outputs/run_2_evidence_aware.md
```

Uses multiple relevant documents, requests source attribution, surfaces the known revenue discrepancy, and excludes the unrelated cable-TV operator.

### Experiment 3 — Strict

```powershell
python agent.py --ticker SRVCABLE --provider gemini --experiment strict --output outputs/run_3_strict_validated.md
```

Uses the full evidence bundle and stronger output requirements. Strict mode applies the output validator to the generated response.

The three commands write to separate files so their results can be compared without overwriting one another.

**Experiment outputs:**

| File | Purpose |
|---|---|
| `outputs/run_1_naive.md` | Baseline prompt result |
| `outputs/run_2_evidence_aware.md` | Multi-document evidence-aware result |
| `outputs/run_3_strict_validated.md` | Strict prompt result |
| `outputs/final_brief.md` | Final research brief |

The observed experiment results and test coverage are documented in `test_log.md`.

## Expected Research Brief Structure

The generated brief uses five primary sections:

1. **Snapshot** — A concise summary of the company and relevant developments.
2. **Bull Case** — Evidence that could support a positive business outlook.
3. **Bear Case** — Risks, uncertainties, and potentially adverse developments.
4. **Open Questions** — Unresolved issues requiring further investigation.
5. **Sources** — Source IDs and references used in the analysis.

The brief is intended to distinguish supporting evidence from risks and unresolved questions rather than produce an unsupported buy/sell recommendation.

## Project Structure

```text
super-investing-ai-research-agent/
├── agent.py
├── system_prompt.md
├── research_pack/
├── tests/
│   └── test_agent.py
├── outputs/
│   ├── final_brief.md
│   ├── run_1_naive.md
│   ├── run_2_evidence_aware.md
│   └── run_3_strict_validated.md
├── README.md
├── test_log.md
├── demo_script.md
├── requirements.txt
├── .env.example
└── .gitignore
```

## Design Decisions

### Source-first research

The agent uses the supplied research pack rather than searching the web for the fictional company. This keeps the analysis within the assignment's evidence boundary.

### Conflicts remain visible

The known revenue discrepancy between INR 1,248 crore and INR 1,428 crore is surfaced rather than resolved through unsupported assumptions. The official filing is treated as the primary reference, but the discrepancy remains an open reconciliation item.

### Entity resolution

The unrelated Sarvottam Cable Network cable-TV operator is excluded because its identity and business do not match the listed cable manufacturer in the assignment.

### Prompt-injection resistance

Instructions embedded in research documents are treated as untrusted content. Promotional claims or instructions to provide stock tips are not accepted as authoritative evidence.

### Conservative conclusions

The agent is designed to present evidence, risks, and open questions without generating a buy/sell rating or guaranteeing investment outcomes.

## Limitations

- The revenue conflict detector uses assignment-specific rules and is not a general financial reconciliation engine.
- Citation validation checks source IDs but does not independently establish that every claim is entailed by its cited document.
- Prompt instructions cannot guarantee complete or factually accurate LLM output.
- The offline generator is deterministic and should not be interpreted as equivalent to LLM-based synthesis.
- Gemini model access, pricing, quotas, and API behavior can change.
- The fictional research pack is not suitable for real-world investment decisions.

## Reproducibility

Run the test suite:

```bash
python -m unittest discover -s tests -v
```

Run the offline workflow:

```bash
python agent.py --ticker SRVCABLE --provider offline
```

Run the strict Gemini workflow:

```powershell
python agent.py --ticker SRVCABLE --provider gemini --model gemini-3.5-flash-lite --experiment strict --output outputs/final_brief.md
```

Refer to `test_log.md` for the observed experiment results and validation details. Refer to `demo_script.md` for the suggested 2–3 minute project demonstration.

## Disclaimer

This is a fictional assignment project intended to demonstrate document processing, evidence-aware LLM prompting, source attribution, conflict detection, and output validation. It is not financial advice or a recommendation to buy or sell any security.


## Bonus: Live-data Research

The project includes an optional live-research module, `live_agent.py`, which retrieves recent news headlines through Google News RSS and market snapshots through Yahoo Finance's chart endpoint. It uses Gemini to generate a concise research brief with source IDs, publication dates, URLs, and open questions.

### Run on real NSE tickers

```powershell
python live_agent.py --ticker TCS
python live_agent.py --ticker INFY
```

Supported tickers are TCS, INFY, RELIANCE, HDFCBANK, and WIPRO. The script requires `GEMINI_API_KEY`.

Generated outputs:
- `outputs/live_tcs.md`
- `outputs/live_infy.md`

### Observations

The TCS and Infosys runs each retrieved eight news headlines and generated a brief using Gemini. The results demonstrated that the agent could combine a market snapshot with recent news and explicitly acknowledge when evidence was limited to headlines.

### Limitations

Google News RSS and Yahoo Finance's chart endpoint are unofficial interfaces and may change or provide delayed data. Headlines alone cannot establish the full context of a company's financial results. Market figures and important claims should be verified against official company disclosures and exchange-authorized sources. The live briefs are for demonstration, not investment advice.