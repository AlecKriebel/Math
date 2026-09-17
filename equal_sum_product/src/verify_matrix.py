#!/usr/bin/env python3
"""Independent, standard-library-only, arbitrary-precision matrix checker.

Input is a JSON matrix, or {"matrix": [...], "N": integer}. Metadata is ignored.
Default dimensions are m >= 3, n >= 2. Use --min-rows 2 for the source control.
The checker tests the actual entries, not an impossibility theorem or search
constraints. All integer sums and products use Python's arbitrary-precision int.
"""
import argparse
import json
import sys

VERSION = "1.0.0"
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def verify(matrix: object, *, min_rows: int = 3, expected_N: object = None) -> dict:
    errors = []
    report = {"checker_version": VERSION, "valid": False, "errors": errors}
    if type(min_rows) is not int or min_rows < 1:
        raise ValueError("min_rows must be a positive integer")
    if type(matrix) is not list or not matrix:
        errors.append("matrix must be a nonempty JSON array of rows")
        return report
    if any(type(row) is not list for row in matrix):
        errors.append("every row must be a JSON array")
        return report
    m, n = len(matrix), len(matrix[0])
    report.update(m=m, n=n)
    if m < min_rows:
        errors.append(f"need at least {min_rows} rows")
    if n < 2:
        errors.append("need at least 2 columns")
    if any(len(row) != n for row in matrix):
        errors.append("matrix is not rectangular")
        return report
    entries = [a for row in matrix for a in row]
    if any(type(a) is not int or a <= 0 for a in entries):
        errors.append("every entry must be a positive integer (not bool or float)")
        return report
    if not entries:
        errors.append("matrix has no entries")
        return report
    distinct = len(set(entries)) == m * n
    report.update(entry_count=m*n, distinct_entry_count=len(set(entries)),
                  globally_distinct=distinct)
    if not distinct:
        errors.append("entries are not globally distinct")
    # Recompute every quantity directly. Do not import search or proof code.
    row_sums = [sum(row) for row in matrix]
    column_products = []
    for j in range(n):
        product = 1
        for i in range(m):
            product *= matrix[i][j]
        column_products.append(product)
    N = row_sums[0]
    report.update(N=N, row_sums=row_sums, column_products=column_products,
                  equal_row_sums=all(s == N for s in row_sums),
                  equal_column_products=all(p == column_products[0]
                                            for p in column_products),
                  all_sums_and_products_equal_N=(all(s == N for s in row_sums)
                                                and all(p == N for p in column_products)))
    if not report["equal_row_sums"]:
        errors.append("row sums differ")
    if not report["equal_column_products"]:
        errors.append("column products differ")
    if any(p != N for p in column_products):
        errors.append("column products do not all equal the row-sum N")
    if expected_N is not None:
        report["declared_N"] = expected_N
        if type(expected_N) is not int or expected_N <= 0:
            errors.append("declared N must be a positive integer")
        elif expected_N != N:
            errors.append("declared N differs from the recomputed row-sum N")
    report["valid"] = not errors
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="JSON file, or - for stdin")
    parser.add_argument("--min-rows", type=int, default=3)
    args = parser.parse_args()
    try:
        if args.file == "-":
            payload = json.load(sys.stdin)
        else:
            with open(args.file, encoding="utf-8") as stream:
                payload = json.load(stream)
        if type(payload) is dict:
            if "matrix" not in payload:
                raise ValueError("JSON object must contain matrix")
            if "N" in payload and (type(payload["N"]) is not int or payload["N"] <= 0):
                raise ValueError("declared N must be a positive integer")
            report = verify(payload["matrix"], min_rows=args.min_rows,
                            expected_N=payload.get("N"))
        else:
            report = verify(payload, min_rows=args.min_rows)
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"checker_version": VERSION, "valid": False,
                          "errors": [str(exc)]}, indent=2))
        return 2
    print(json.dumps(report, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
