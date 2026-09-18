from genomeforge import sequence
from genomeforge.exceptions import InvalidSequenceError
from genomeforge.config import SequenceRules
import pytest
import logging

@pytest.mark.parametrize(
    "dna_sequence, expected",
    [
      ("AGCTTGGCCC",0.7),
      ("taaggccctttc",0.5),
      ("GCCGCCGCCGCCGGGC",1),
      ("AATTAA",0),
      ("AGC",2/3),
      ("AGCT",0.5)
        
    ])
def test_gc_calculation(dna_sequence,expected):
    assert sequence.gc_content(dna_sequence) == pytest.approx(expected)

def test_empty_input_rejection():
    with pytest.raises(InvalidSequenceError,match='empty'):
        sequence.gc_content("")
        
def test_invalid_input_rejection():
    with pytest.raises(InvalidSequenceError,match="invalid"):
        sequence.gc_content("AGCTXGGGCC")
        
def test_valid_upper_sequence():
    assert sequence.validate_dna_sequence("AGCTGGGCC") is None
    
def test_valid_lower_sequence():
    assert sequence.validate_dna_sequence("aggccctttgggg") is None
    
def test_empty_sequence_throws_error():
    with pytest.raises(InvalidSequenceError,match='empty'):
            sequence.validate_dna_sequence("")
    
def test_invalid_sequence_throws_error():
    with pytest.raises(InvalidSequenceError,match="invalid"):
        sequence.validate_dna_sequence("AGCTXGGGCC")

def test_gc_content_logs_debug_details(caplog):
    with caplog.at_level(logging.DEBUG, logger="genomeforge.sequence"):
        result = sequence.gc_content("AGCT")

    assert result == 0.5
    assert "sequence of length 4" in caplog.text
    assert "GC fraction" in caplog.text

def test_custom_valid_sequence():
    custom_rules = SequenceRules(
        valid_bases=frozenset("ACGTN"),
        gc_bases=frozenset("GC"),
    )
    result = sequence.gc_content("AGCN",rules=custom_rules)
    assert result == pytest.approx(0.5)

def test_default_rules_reject_n():
    with pytest.raises(InvalidSequenceError,match='invalid'):
        sequence.gc_content("AGCN")
