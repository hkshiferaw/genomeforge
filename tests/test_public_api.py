import pytest
from genomeforge import gc_content, SequenceRecord, InvalidSequenceError

def test_gc_calculation():
    assert gc_content('AGCT') == pytest.approx(0.5)
    
def test_empty_input_rejection():
    with pytest.raises(InvalidSequenceError,match='empty'):
        gc_content("")
        
def test_invalid_input_rejection():
    with pytest.raises(InvalidSequenceError,match="invalid"):
        gc_content("AGCTXGGGCC")

def test_sequence_record_creation():
    test_obj = SequenceRecord(identifier='SEQ1',sequence='AAGGCCTT')
    assert test_obj.sequence == "AAGGCCTT"
    assert test_obj.identifier == "SEQ1"
