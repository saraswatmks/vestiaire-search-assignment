"""Predicts the category of a search query."""
import argparse
import os
import sys

import pandas as pd

from src.query import QueryToCategory


def main(args=None) -> int:

    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    pargs, _ = parser.parse_known_args(args)

    # initialise config
    qc = QueryToCategory()
    qc.search(pargs.query)

    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main())
