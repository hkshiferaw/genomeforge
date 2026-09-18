from dataclasses import dataclass
from genomeforge.sequence import gc_content

@dataclass
class SequenceRecord:
    """Store a sequence identifier, sequence text, and optional description.

    Construction stores the supplied values without validating the sequence.
    Calling gc_fraction() validates it using the default DNA rules.
    """
    identifier: str
    sequence: str
    description: str | None = None
    
    @property
    def length(self)->int:
        """Return the number of characters in the stored sequence."""
        return len(self.sequence)
    
    def gc_fraction(self)-> float:
        """Return the GC fraction, raising InvalidSequenceError for invalid DNA."""
        return gc_content(self.sequence)
