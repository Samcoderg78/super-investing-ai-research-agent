# Test Log — Three Design Iterations

**Important execution note:** These three recorded design iterations were run locally in offline mode because no `GEMINI_API_KEY` was configured in the build environment. They test the ingestion, source handling, and output design; they are **not claimed as three live Gemini API calls**. The project supports Gemini through `--provider gemini`. If you configure a key before submission, run the live API version and update this log with the actual model response, time, and any observed failures.

## Run 1 — Naive single-source baseline
- **Design:** Summarized the Business Daily Q1 article as the main context, without a source ledger or cross-document comparison.
- **Artifact:** `outputs/run_1_naive.md`.
- **What went wrong:** It repeated ₹1,428 crore as if it were the settled Q1 revenue and missed the official company filing's ₹1,248 crore figure. It also had no explicit defence against the hidden instruction in the stock-tips blog or the similarly named local cable-TV operator.
- **Change made:** Load the full document pack with source metadata and compare numeric claims across documents before drafting.

## Run 2 — Evidence-aware source-first generator
- **Design:** Added front-matter parsing, document IDs, publication dates, a relevance filter, and rule-based revenue conflict detection. The brief cites source IDs and distinguishes management guidance from reported results.
- **Artifact:** `outputs/run_2_evidence_aware.md`.
- **Observed result:** The two revenue figures (₹1,248 crore and ₹1,428 crore) were both surfaced, and the official filing was used as the primary reference without pretending the discrepancy was resolved.
- **Remaining issue:** The transcript excerpt omits the issuer name in its body, so a simple company-name filter initially excluded it. The filter was amended to retain the issuer's `ir_concall_` source file. The unrelated local cable-TV article remains excluded.

## Run 3 — Strict output validation and regression tests
- **Design:** Kept the evidence-first approach; added a separate system prompt, an optional Gemini API path, output checks for required sections and source IDs, a check that the known revenue conflict is disclosed, and rejection of promotional stock-tip language. Added regression tests.
- **Artifact:** `outputs/run_3_strict_validated.md` and `outputs/final_brief.md`.
- **Observed result:** 7 relevant documents retained from the 8-document pack; the local cable-TV article was excluded; 2 distinct revenue conflict entries were detected; all 5 unit tests passed.
- **Remaining limitation:** The detector is targeted at this pack and does not semantically verify every cited claim. The current run used the deterministic offline generator because no API key was configured. The live Gemini path still needs to be exercised with a real key before describing the final brief as LLM-generated.

## Automated checks executed
Command: `python -m unittest discover -s tests -v`

Result: **5 tests passed** — pack/entity filtering, revenue conflict detection, required sections and key risks, rejection of unknown citations, and rejection of promotional buy language.
