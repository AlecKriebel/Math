"""Compare complete author and independent GAP rows, ignoring enumeration order."""
from pathlib import Path
import datetime
import hashlib
import json

HERE = Path(__file__).resolve().parent
author = HERE.parent / "artifacts" / "library_scan.ndjson"
independent = HERE / "independent_library_scan.ndjson"
left = [json.loads(line) for line in author.read_text().splitlines()]
right = [json.loads(line) for line in independent.read_text().splitlines()]
left_by_name = {row[0]: row for row in left}
right_by_name = {row[0]: row for row in right}
assert len(left_by_name) == len(left) == len(right) == len(right_by_name)
assert left_by_name == right_by_name
report = {
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "rows": len(left),
    "complete_row_equality_by_table_name": True,
    "author_input_sha256": hashlib.sha256(author.read_bytes()).hexdigest(),
    "independent_input_sha256": hashlib.sha256(independent.read_bytes()).hexdigest(),
    "independent_method": "Reversed table-name iteration; Collected(List(Irr(table), chi -> chi[1])) for degrees; direct class-size summation over ClassPositionsOfSolvableRadical. Same trusted GAP radical attribute, whose source implementation was separately audited."
}
(HERE / "independent_library_comparison.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
