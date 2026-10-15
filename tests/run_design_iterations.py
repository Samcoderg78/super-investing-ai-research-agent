"""Reproduce the three documented offline design iterations for the assignment."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import agent

pack = agent.load_documents(ROOT / 'research_pack')
# Run 1: naive baseline. Only the news article is summarized, as in a raw-context prototype.
news = next(d for d in pack if d.doc_id.startswith('businessdaily_'))
run1 = """# Run 1 — Naive baseline (prototype)

## Snapshot
Business Daily reports Sarvottam Cables Q1 revenue of ₹1,428 crore, up 35% YoY, and profit of ₹82 crore. Operating margin fell to 11.2% as copper prices rose.

## Bull case
- Revenue growth and demand from utilities/data centres look strong.

## Bear case
- Copper costs compressed margins.

## Open questions
- Can the company pass higher copper costs to customers?

## Sources
- Business Daily Online (9 Aug 2026): https://businessdaily.example/markets/sarvottam-cables-q1-results

**Known issue:** this first pass trusted one news article, missed the official filing's conflicting revenue figure, and had no entity or prompt-injection safeguards.
"""
(ROOT / 'outputs' / 'run_1_naive.md').write_text(run1, encoding='utf-8')
# Run 2: source-aware approach with a structured evidence bundle and conflict detection.
bundle = agent.evidence_bundle(pack, 'SRVCABLE')
run2 = agent.build_offline_brief(bundle)
(ROOT / 'outputs' / 'run_2_evidence_aware.md').write_text(run2, encoding='utf-8')
# Run 3: final version; validate section coverage and known conflict explicitly.
agent.validate_llm_output(run2, bundle)
assert len(bundle['documents']) == 7
assert len(bundle['revenue_conflicts']) == 2
assert 'Sarvottam Cable Network' not in run2
assert 'strong buy' not in run2.lower()
(ROOT / 'outputs' / 'run_3_strict_validated.md').write_text(run2, encoding='utf-8')
print('Run 1: naive baseline written; known revenue discrepancy was missed.')
print('Run 2: evidence-aware brief written; two revenue values surfaced.')
print('Run 3: strict validation passed; 7 relevant docs, 2 revenue conflict entries, unrelated entity excluded.')
