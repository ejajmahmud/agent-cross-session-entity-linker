"""Core cross-session entity linker implementation."""
from typing import Dict, List, Set, Optional

class PhoneticMatcher:
    @staticmethod
    def simple_soundex(s: str) -> str:
        s = s.upper().strip()
        if not s:
            return ""
        first = s[0]
        # Simple character group encoding
        mapping = {"B": "1", "F": "1", "P": "1", "V": "1",
                   "C": "2", "G": "2", "J": "2", "K": "2", "Q": "2", "S": "2", "X": "2", "Z": "2",
                   "D": "3", "T": "3",
                   "L": "4",
                   "M": "5", "N": "5",
                   "R": "6"}
        encoded = [mapping.get(c, "") for c in s[1:]]
        filtered = [c for c in encoded if c]
        return (first + "".join(filtered) + "000")[:4]

class EntityCluster:
    def __init__(self, canonical_id: str, primary_name: str):
        self.canonical_id = canonical_id
        self.primary_name = primary_name
        self.aliases: Set[str] = {primary_name.lower()}

    def add_alias(self, alias: str):
        self.aliases.add(alias.lower())

class CrossSessionEntityLinker:
    def __init__(self):
        self.clusters: Dict[str, EntityCluster] = {}
        self.alias_to_id: Dict[str, str] = {}

    def register_canonical_entity(self, canonical_id: str, primary_name: str) -> EntityCluster:
        cluster = EntityCluster(canonical_id, primary_name)
        self.clusters[canonical_id] = cluster
        self.alias_to_id[primary_name.lower()] = canonical_id
        return cluster

    def add_alias(self, canonical_id: str, alias: str):
        if canonical_id in self.clusters:
            self.clusters[canonical_id].add_alias(alias)
            self.alias_to_id[alias.lower()] = canonical_id

    def resolve(self, surface_text: str) -> Optional[str]:
        clean = surface_text.strip().lower()
        # 1. Exact alias match
        if clean in self.alias_to_id:
            return self.alias_to_id[clean]

        # 2. Substring matching in aliases
        for alias, cid in self.alias_to_id.items():
            if alias in clean or clean in alias:
                return cid

        # 3. Phonetic matching
        target_code = PhoneticMatcher.simple_soundex(clean)
        for alias, cid in self.alias_to_id.items():
            if PhoneticMatcher.simple_soundex(alias) == target_code:
                return cid

        return None
