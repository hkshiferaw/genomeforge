from genomeforge.config import SequenceRules,DEFAULT_SEQUENCE_RULES
from genomeforge.models import SequenceRecord
from genomeforge.exceptions import FastaFormatError
from genomeforge.sequence import validate_dna_sequence
import logging
"""
>seq1 Example sequence
AGCT
TGCA
>seq2
GGCC
"""

logger = logging.getLogger(__name__)

def parse_fasta(text: str, *, rules: SequenceRules = DEFAULT_SEQUENCE_RULES) -> list[SequenceRecord]:
    """Parse newline-separated FASTA text into records in input order.

    Join sequence lines within each record, skip empty lines, and validate
    each assembled sequence using rules. Preserve sequence case. Split each
    header at its first space into an identifier and optional description.
    The input is text, not a file path; whitespace is not stripped.

    Raise FastaFormatError for empty input, sequence data before a header,
    a bare '>' header, or a record without sequence data. Raise
    InvalidSequenceError for sequence characters disallowed by rules.

    Log the number of parsed records at DEBUG level. Custom rules apply
    during validation and are not stored on the returned records.
    """

    def make_sequence_record_to_add(current_header,current_sequence):
            """Validate an assembled sequence and build its SequenceRecord.

            Expect current_header to include the leading '>'. Use the
            enclosing parse_fasta call's rules for sequence validation.
            Raise FastaFormatError for an empty sequence or propagate
            InvalidSequenceError for disallowed bases. Return the record;
            the caller adds it to the results.
            """
            if current_header == '' and current_sequence == '':
                raise FastaFormatError('There is no record to found! Fasta is likely empty.')
            
            if current_sequence == '':
                raise FastaFormatError('Record has a header but no sequence!')
            validate_dna_sequence(current_sequence,rules=rules)
            
            input_header = current_header.split(" ", maxsplit=1)
                        
            if len(input_header)>1:                                                                                                                                                                                                                             
                return SequenceRecord(input_header[0][1:],current_sequence,input_header[1])
            else:
                return SequenceRecord(input_header[0][1:],current_sequence)
        
    
    current_head = ''
    current_seq = ''
    
    seq_records = []
    
    for line in text.split('\n'):
        if line.startswith('>'):
            if line.strip() == '>':
                raise FastaFormatError('Header has no identifier!')
            if current_head != '':
                seq_records.append(make_sequence_record_to_add(current_head,current_seq))
            current_head = line
            current_seq = ''
        elif len(line)>0:
            if current_head =='': ##Sequence before header
                
                raise FastaFormatError('Sequence found without a header!')
            current_seq += line
    
    seq_records.append(make_sequence_record_to_add(current_head,current_seq))
    
    if len(seq_records) == 0:
        raise FastaFormatError('Text has no records.')
    logger.debug("Record count: %d", len(seq_records))
    
    return seq_records
