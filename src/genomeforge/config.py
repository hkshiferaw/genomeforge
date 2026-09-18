from dataclasses import dataclass

@dataclass(frozen=True)
class SequenceRules():
    valid_bases: frozenset[str]

    gc_bases: frozenset[str]
    
DEFAULT_SEQUENCE_RULES = SequenceRules(
    valid_bases=frozenset("ACGT"),
    gc_bases=frozenset("GC"),
)