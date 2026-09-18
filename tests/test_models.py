from genomeforge.models import SequenceRecord
from genomeforge.exceptions import InvalidSequenceError
import pytest


def test_access_identifier():
    test_obj = SequenceRecord(identifier='SEQ1',sequence='AGCT')
    assert test_obj.identifier == "SEQ1"
    
def test_access_sequence():
    test_obj = SequenceRecord(identifier='SEQ1',sequence='AGCT')
    assert test_obj.sequence == "AGCT"

def test_default_description():
    test_obj = SequenceRecord(identifier='SEQ1',sequence='AGCT')
    assert test_obj.description is None
        
def test_correct_length():
    test_obj = SequenceRecord(identifier='SEQ1',sequence='AGCT')
    assert test_obj.length == 4

def test_sequence_gc_fraction():
    test_obj = SequenceRecord(identifier='SEQ1',sequence='AGCT')
    assert test_obj.gc_fraction() == 0.5
    
def test_empty_sequence_error():
    test_obj = SequenceRecord(identifier='SEQ1',sequence='')
    with pytest.raises(InvalidSequenceError,match='empty'):
            test_obj.gc_fraction()

def test_invalid_sequence_error():
    test_obj = SequenceRecord(identifier='SEQ1',sequence='AGXT')
    with pytest.raises(InvalidSequenceError,match="invalid"):
            test_obj.gc_fraction()