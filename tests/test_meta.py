import unittest

from ptcg_agent_lab.meta import (
    MetaEntry,
    allocate_occurrence_counts,
    interleaved_schedule,
)


class MetaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.entries = [
            MetaEntry("grim", 50),
            MetaEntry("alakazam", 30),
            MetaEntry("other", 20),
        ]

    def test_allocation_preserves_total(self) -> None:
        counts = allocate_occurrence_counts(self.entries, 17)
        self.assertEqual(sum(counts.values()), 17)
        self.assertGreater(counts["grim"], counts["other"])

    def test_schedule_has_requested_length(self) -> None:
        schedule = interleaved_schedule(self.entries, 25)
        self.assertEqual(len(schedule), 25)
        self.assertEqual(schedule.count("grim"), 13)


if __name__ == "__main__":
    unittest.main()
