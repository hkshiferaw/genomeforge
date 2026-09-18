from genomeforge.exceptions import InvalidSequenceError
import logging
from genomeforge.config import SequenceRules, DEFAULT_SEQUENCE_RULES




logger = logging.getLogger(__name__)

def gc_content(sequence: str, *, rules: SequenceRules = DEFAULT_SEQUENCE_RULES) -> float:
    """Return the unrounded GC fraction of a non-empty DNA sequence.

    Input is case-insensitive; rule sets should contain uppercase bases.
    The result is between 0.0 and 1.0, counting every accepted base in the
    denominator and bases in rules.gc_bases in the numerator.
    Raises InvalidSequenceError for empty input or bases disallowed by rules.
    """
    validate_dna_sequence(sequence,rules=rules) 
    logger.debug("Calculating GC fraction for sequence of length %d", len(sequence))
    
    gc_count = sum(1 for char in sequence.upper() if char in rules.gc_bases )
    
    gc_fraction = gc_count / len(sequence)
    logger.debug("GC fraction = %f", gc_fraction)
    
    return  gc_fraction

def validate_dna_sequence(sequence: str, *,rules: SequenceRules = DEFAULT_SEQUENCE_RULES) -> None:
    """Validate a non-empty sequence and return None on success.

    Compare uppercased input against rules.valid_bases, which should contain
    uppercase bases. Default rules accept only A, C, G, and T.
    Raise InvalidSequenceError for empty input or any disallowed character.
    """
    if sequence == "":
            raise InvalidSequenceError("Sequence can't be empty!")
    for char in sequence.upper():
            if char not in rules.valid_bases:
                raise InvalidSequenceError(f"Sequence includes {char} which is an invalid character!")
    return None
    
