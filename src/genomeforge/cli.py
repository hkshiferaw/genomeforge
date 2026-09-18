import argparse
from genomeforge.sequence import gc_content
from genomeforge.exceptions import InvalidSequenceError
import sys

def main(argv: list[str] | None = None) -> int:
    """Run the GC command using argv, or process arguments when argv is None.

    Print a percentage with two decimal places to stdout and return 0 on
    success. For invalid sequence input, print the error to stderr and return
    2. Argument parsing may raise SystemExit for help or malformed arguments.
    """
    parser = argparse.ArgumentParser(
        description="GenomeForge GC calculation."
    )
    parser.add_argument("input_sequence", help="The sequence to be analyzed")

    args = parser.parse_args(argv)

    sequence = args.input_sequence

    try:
        result = gc_content(sequence)
    except InvalidSequenceError as e:
        print(e, file=sys.stderr)
        return 2
    print(f"{result:.2%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
