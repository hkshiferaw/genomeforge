# GenomeForge

A bioinformatics pipeline toolkit, built as a hands-on learning project.

## Status

GenomeForge currently provides DNA validation, GC-fraction calculation,
sequence records, configurable sequence rules, and a command-line interface.
It is a learning project; FASTA parsing and complete analysis pipelines are
not implemented yet.

## Installation

Requires Python 3.10 or newer. From the repository directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

The editable installation uses the local source and installs the `genomeforge`
command. Repeat installation after changing console-script configuration.

## Library usage

```python
from genomeforge import gc_content, SequenceRecord

gc_content("AGCT")  # 0.5
record = SequenceRecord(identifier="SEQ1", sequence="AGCT")
record.length  # 4
record.gc_fraction()  # 0.5
```

Default rules accept A, C, G, and T in either case. Calculations return an
unrounded fraction between 0.0 and 1.0. Empty sequences or disallowed characters
raise `InvalidSequenceError`, a subclass of `ValueError`. Whitespace is not
stripped. Records accept data at construction and validate it when
`gc_fraction()` is called.

Use `validate_dna_sequence()` to validate without calculating; it returns
`None` for valid input.

### Custom rules

```python
from genomeforge import gc_content, SequenceRules

rules = SequenceRules(
    valid_bases=frozenset("ACGTN"),
    gc_bases=frozenset("GC"),
)
gc_content("ACGN", rules=rules)  # 0.5
```

Supply uppercase bases in the rule sets. In this example, N is accepted and
included in the total sequence length, but is not counted as G or C. Default
rules reject N. Custom rules are also accepted by `validate_dna_sequence()`;
the record method and CLI use default rules.

## Command-line usage

```bash
genomeforge AGCT
# 50.00%
genomeforge --help
```

The command formats the fraction as a percentage with two decimal places.
Success writes to standard output and exits with status 0. Invalid sequences
write an error to standard error and exit with status 2.

## Tests

With the virtual environment active:

```bash
python -m pip install pytest
python -m pytest -q
```

## License

MIT — see [LICENSE](LICENSE).
