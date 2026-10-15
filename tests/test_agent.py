import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import agent

class AgentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs = agent.load_documents(ROOT / "research_pack")
        cls.bundle = agent.evidence_bundle(cls.docs, "SRVCABLE")

    def test_eight_docs_loaded_and_unrelated_entity_excluded(self):
        self.assertEqual(len(self.docs), 8)
        self.assertIn("nagpurcitytimes_2026-08-20", self.bundle["excluded_documents"])
        self.assertNotIn("nagpurcitytimes_2026-08-20", {d["id"] for d in self.bundle["documents"]})

    def test_revenue_conflict_detected(self):
        values = {x["value_crore"] for x in self.bundle["revenue_conflicts"]}
        self.assertIn(1248, values)
        self.assertIn(1428, values)

    def test_offline_brief_includes_required_sections_and_risks(self):
        brief = agent.build_offline_brief(self.bundle)
        for section in ["## Snapshot", "## Bull case", "## Bear case", "## Open questions", "## Sources"]:
            self.assertIn(section, brief)
        self.assertIn("₹46.3 crore", brief)
        self.assertIn("78 to 96", brief)
        self.assertIn("₹1,248 crore", brief)
        self.assertIn("₹1,428 crore", brief)

    def test_output_validator_rejects_unknown_citation(self):
        invalid = "## Snapshot\nA fact [not_a_real_source]\n## Bull case\nX\n## Bear case\nY\n## Open questions\nRevenue figures differ.\n## Sources\nX"
        with self.assertRaises(ValueError):
            agent.validate_llm_output(invalid, self.bundle)

    def test_output_validator_rejects_promo_language(self):
        invalid = "## Snapshot\nFact [ir_press_release_2026-08-08]\n## Bull case\nStrong buy [multibaggeralerts_2026-08-12]\n## Bear case\nRisk [nse_announcement_2026-09-02]\n## Open questions\nRevenue discrepancy.\n## Sources\nsource"
        with self.assertRaises(ValueError):
            agent.validate_llm_output(invalid, self.bundle)

if __name__ == "__main__":
    unittest.main()
