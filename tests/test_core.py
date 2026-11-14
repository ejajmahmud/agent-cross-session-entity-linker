"""Unit tests for agent-cross-session-entity-linker."""
import unittest
from agent_cross_session_entity_linker.core import CrossSessionEntityLinker

class TestCrossSessionEntityLinker(unittest.TestCase):
    def setUp(self):
        self.linker = CrossSessionEntityLinker()
        self.linker.register_canonical_entity("ENT_APP", "Antigravity")
        self.linker.add_alias("ENT_APP", "AGY")

    def test_exact_and_alias_resolution(self):
        self.assertEqual(self.linker.resolve("Antigravity"), "ENT_APP")
        self.assertEqual(self.linker.resolve("agy"), "ENT_APP")

    def test_unresolved_entity(self):
        self.assertIsNone(self.linker.resolve("RandomStranger"))
