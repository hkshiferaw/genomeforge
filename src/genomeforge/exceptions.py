class InvalidSequenceError(ValueError):
    """Raised when a DNA sequence is empty or contains invalid bases."""
    
class FastaFormatError(ValueError):
    """Raised when fasta structure is malformed"""