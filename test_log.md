# Test Log — Super Investing AI Research Agent

## 1. Overview

This document records the three prompt experiments performed for the Super Investing AI Innovator Intern assignment, along with the automated regression tests used to evaluate the research agent.

The experiments compare a baseline prompt, an evidence-aware prompt, and a strict prompt with output validation. All experiments use the supplied fictional SRVCABLE research pack and do not rely on live company data.

**Objective:** Improve research coverage, source traceability, handling of contradictory evidence, and output structure while reducing the risk of unsupported or promotional conclusions.

## 2. Prompt Experiment 1 — Baseline

**Mode:** `baseline`

**Output:** `outputs/run_1_naive.md`

**Approach:** The baseline prompt summarizes a single Business Daily article rather than systematically comparing the full research pack.

### Observed results

- Captured reported revenue growth, profit, margin contraction, and copper-cost pressure.
- Used the revenue figure reported in the selected article.
- Did not reconcile that figure against the official company release.
- Omitted relevant information available in other research documents.
- Provided limited follow-up questions.

### Limitation

The single-source approach provided incomplete coverage and did not adequately surface the known revenue discrepancy.

**Conclusion:** This experiment established a baseline for evaluating the benefits of cross-document evidence analysis.

## 3. Prompt Experiment 2 — Evidence-aware

**Mode:** `evidence`

**Output:** `outputs/run_2_evidence_aware.md`

**Approach:** The evidence-aware prompt incorporates multiple relevant documents, requests source attribution, identifies the known revenue discrepancy, and instructs the model to exclude the unrelated cable-TV operator.

### Observed results

- Incorporated evidence from multiple research documents.
- Included source IDs to help trace claims to the research pack.
- Surfaced the discrepancy between the official revenue figure of INR 1,248 crore and the Business Daily figure of INR 1,428 crore.
- Expanded the analysis to include the order book, capacity expansion, receivables, and GST demand.
- Provided broader business context than the baseline output.

### Remaining limitation

The observed output contained only two open questions, fewer than the strict prompt's target of at least three.

**Conclusion:** Cross-document evidence instructions improved coverage and made the revenue discrepancy explicit, but the output still needed stronger structural requirements.

## 4. Prompt Experiment 3 — Strict prompt and validation

**Mode:** `strict`

**Output:** `outputs/run_3_strict_validated.md`

**Approach:** The strict prompt uses the full evidence bundle and requests five sections: Snapshot, Bull Case, Bear Case, Open Questions, and Sources. It also requires source attribution, discussion of the known revenue discrepancy, exclusion of the unrelated entity, and avoidance of promotional stock-tip language.

The strict mode applies the agent's output validator to the generated response.

### Observed results

- Produced a more comprehensive research brief than the earlier experiments.
- Included multiple bullish and bearish considerations.
- Discussed the revenue discrepancy instead of silently choosing one figure.
- Included three open questions.
- Provided source IDs and a disclaimer.
- Covered additional considerations, including the order book, capacity expansion, exports, margins, receivables, GST demand, and promoter pledging.

### Validation considerations

The output's structure and content were reviewed against the experiment requirements. Automated validation checks only the conditions implemented in `validate_llm_output()`; it does not independently prove that every factual claim is supported by its cited document.

**Conclusion:** The strict experiment produced the most comprehensive of the three observed outputs and added a programmatic validation step.

## 5. Comparison of the Experiments

| Evaluation area | Baseline | Evidence-aware | Strict |
|---|---|---|---|
| Evidence coverage | Primarily one article | Multiple relevant documents | Multiple relevant documents |
| Revenue discrepancy | Not reconciled | Explicitly surfaced | Explicitly surfaced |
| Source attribution | Limited | Source IDs requested | Source IDs and validation |
| Output structure | Basic summary | Expanded research brief | Five required sections |
| Open questions | Limited | Two observed | Three observed |
| Programmatic validation | Not applied by experiment mode | Not applied by experiment mode | Applied |

The table summarizes the observed outputs and configured experiment behavior. It should not be interpreted as proof that every factual statement or citation is correct.

## 6. Automated Regression Tests

**Command executed:**

```bash
python -m unittest discover -s tests -v
```

**Observed result:** `Ran 5 tests ... OK`

All five automated regression tests passed in this run, covering document loading and entity exclusion, revenue conflict detection, offline brief requirements, rejection of unknown citations, and rejection of specified promotional language.
### Test coverage

| Test | Purpose |
|---|---|
| `test_eight_docs_loaded_and_unrelated_entity_excluded` | Checks that the expected documents are loaded and the unrelated entity is excluded. |
| `test_revenue_conflict_detected` | Checks detection of the known revenue discrepancy. |
| `test_offline_brief_includes_required_sections_and_risks` | Checks required sections and risk coverage in the offline brief. |
| `test_output_validator_rejects_unknown_citation` | Checks rejection of source IDs that are not recognized. |
| `test_output_validator_rejects_promo_language` | Checks rejection of specified promotional stock-tip language. |

These are regression tests for the behaviors they explicitly exercise. They do not cover every possible input, model response, or factual error.

## 7. Final Brief Generation

The final research brief is saved at:

`outputs/final_brief.md`

The final brief was regenerated using the strict Gemini experiment after correcting character encoding and tightening citation validation.

**Generation command:**

```powershell
python agent.py --ticker SRVCABLE --provider gemini --model gemini-3.5-flash-lite --experiment strict --output .\outputs\final_brief.md
```

The command uses the configured Gemini API key from the environment. A successful run should report Gemini as the generator and save the brief to the specified path.

The final brief should be reviewed for:

- All five required sections.
- Discussion of the INR 1,248 crore versus INR 1,428 crore revenue discrepancy.
- Source IDs that correspond to relevant documents.
- At least two Bull Case points and two Bear Case points.
- At least three Open Questions.
- No unsupported buy/sell recommendation or promotional stock-tip claims.

These content checks should be distinguished from automated checks: a requirement is programmatically enforced only if the current implementation explicitly validates it.

## 8. Known Limitations

- Revenue discrepancy detection is tailored to the supplied research pack.
- Citation validation checks source-ID references but does not independently establish semantic support for every claim.
- Prompt instructions cannot guarantee that a language model will produce complete or factually correct output.
- The experiment comparison is based on the generated outputs; it is not a controlled statistical evaluation of model performance.
- API availability, model access, and quotas may vary.
- The company and case materials are fictional and must not be used to make real investment decisions.

## 9. Overall Conclusion

The three experiments demonstrate the practical value of progressively improving the prompt strategy. The baseline relied on a single article, the evidence-aware version incorporated multiple sources and surfaced contradictory revenue figures, and the strict version added stronger structural requirements and programmatic output validation.

The main improvement was preserving the unresolved revenue discrepancy rather than selecting a figure without explanation. The tests provide additional checks for selected behaviors, while manual review remains necessary to assess factual support and research quality.
