from genomeforge.models import SequenceRecord
from genomeforge.fasta import parse_fasta
from genomeforge.exceptions import FastaFormatError, InvalidSequenceError
from genomeforge.config import SequenceRules,DEFAULT_SEQUENCE_RULES
import pytest
import logging

"""
Create tests/test_fasta.py covering:
- two records, including one wrapped sequence
- description parsing
- blank-line handling
- custom rules that allow N
- invalid DNA propagates InvalidSequenceError 
- each malformed-structure case above raises FastaFormatError
- debug logging records the parsed record count
"""

def test_parse_single_record():
    text = ">seq1\nAGCT\n"

    records = parse_fasta(text)

    assert len(records) == 1
    assert records[0].identifier == "seq1"
    assert records[0].sequence == "AGCT"
    assert records[0].description is None
    
def test_parse_single_record_with_description():
    text = ">seq1 Example Sequence\nAGCT\n"

    records = parse_fasta(text)

    assert len(records) == 1
    assert records[0].identifier == "seq1"
    assert records[0].sequence == "AGCT"
    assert records[0].description == 'Example Sequence'
    
def test_parse_multiple_records():
    text = ">seq1\nAG\nCT\n>seq2\nGGCC\n"

    records = parse_fasta(text)

    assert len(records) == 2
    
    assert records[0].identifier == "seq1"
    assert records[0].sequence == "AGCT"
    assert records[1].identifier == "seq2"
    assert records[1].sequence == "GGCC"

def test_invalid_fasta_sequence_header():
    with pytest.raises(FastaFormatError,match="Sequence found without a header!"):
        text = "AGCT\n"
        records = parse_fasta(text)
def test_invalid_fasta_sequence_when_seqid_is_blank():
    with pytest.raises(FastaFormatError,match="Header has no identifier"):
        text = "> \nAGCT\n"
        records = parse_fasta(text)
        
def test_blank_line_doesnt_impact_sequence():
    text = ">seq1\nAG\n\nCT\n"

    records = parse_fasta(text)

    assert records[0].sequence == "AGCT"
    
    
def test_custom_rules_allow_N_sequence():
    text = ">seq1\nAGNCCT\n"

    records = parse_fasta(text,rules=SequenceRules(valid_bases=frozenset("ACGTN"),gc_bases=frozenset("GC"),))

    assert records[0].sequence == "AGNCCT"

def test_default_rules_reject_N_sequence():
    
    with pytest.raises(InvalidSequenceError,match="invalid"):
            text = ">seq1\nAGNCCT\n"
            records = parse_fasta(text)
    
def test_no_idenfier_in_header():
    with pytest.raises(FastaFormatError,match="Header has no identifier!"):
        text = ">\nGGCCAT"
        records = parse_fasta(text)

def test_empty_fasta_error():
    with pytest.raises(FastaFormatError,match="There is no record to found! Fasta is likely empty."):
        text = ""
        records = parse_fasta(text)

def test_empty_lines_forces_error():
    with pytest.raises(FastaFormatError,match="There is no record to found! Fasta is likely empty."):
        text = "\n\n"
        records = parse_fasta(text)
    
        
def test_no_fasta_sequence_error():
    with pytest.raises(FastaFormatError,match="no sequence"):
        text = ">seq1\n>seq2"
        records = parse_fasta(text)

def test_no_fasta_sequence_error_at_the_end():
    with pytest.raises(FastaFormatError,match="no sequence"):
        text = ">seq1\nAGGCCTT\n>seq2"
        records = parse_fasta(text)
        
        
def test_invalid_fasta_sequence_error():
    with pytest.raises(InvalidSequenceError,match="invalid"):
        text = ">seq1\nAGXT\n"
        records = parse_fasta(text)

def test_parse_fasta_logs_record_count(caplog):
    with caplog.at_level(logging.DEBUG, logger="genomeforge.fasta"):
        text = ">seq1\nAG\nCT\n>seq2\nGGCC\n"
        records = parse_fasta(text)
        
        assert "Record count: 2" in caplog.text
        
