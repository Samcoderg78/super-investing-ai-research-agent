# 2–3 Minute Demo Script

**0:00–0:20 — Introduce the task**
“Hi, this is my Super Investing AI Innovator assignment. It takes an NSE ticker and a folder of source documents, then produces a concise research brief. SRVCABLE is fictional, so the agent only uses the supplied eight-document pack.”

**0:20–0:50 — Show the project and run it**
Show `research_pack/`, `system_prompt.md`, and `agent.py`. In the terminal run:

```bash
python agent.py --ticker SRVCABLE --provider offline
```

Say: “The offline mode is reproducible and requires no API key. If I configure a Gemini API key, the same pipeline can use Gemini Flash; it validates the response before saving it.”

**0:50–1:30 — Show the brief and contradiction detection**
Open `outputs/final_brief.md`. Point to the snapshot and revenue discrepancy: “The official company release says ₹1,248 crore, while a news article says ₹1,428 crore. Instead of silently picking a convenient number, the agent flags the conflict and carries it into open questions.”

**1:30–2:00 — Show one design decision**
Show the `is_relevant` filter and `system_prompt.md`: “A local cable-TV operator has a similar name but is not the listed cable manufacturer, so I exclude it. The stock-tips blog also contains a hidden instruction aimed at AI systems. The system prompt treats retrieved documents as untrusted data, not instructions.”

**2:00–2:25 — Tests and limitation**
Run:

```bash
python -m unittest discover -s tests -v
```

Say: “The tests cover entity mismatch, revenue conflict detection, required sections, and rejection of unknown citations or promotional buy language. A limitation is that the current contradiction detector is rule-based and focused on the known revenue conflict; it is not a complete financial fact-checker.”

**2:25–2:40 — Close**
“The result is a traceable research summary, not a buy/sell recommendation. The next improvement would be a broader numeric fact ledger and semantic claim-to-source verification.”

**Recording honesty:** If the Gemini API key is not configured, do not claim that a live LLM call was made. Show offline mode or configure the key and run `--provider gemini` before recording.
