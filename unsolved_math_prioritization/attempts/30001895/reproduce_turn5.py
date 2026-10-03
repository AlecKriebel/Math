"""Reproduce completed certificates only; do not resume unfinished searches."""
from pathlib import Path
import gzip
import hashlib
import json
import subprocess
import tempfile
from build_degree8_certificate import small_link_records, trace_cases
from verify_degree8_certificate import verify as verify_degree8
from verify_tau4_certificate import verify as verify_tau4
from count_tau4_pairs import table


def main():
    here = Path(__file__).resolve().parent
    rebuilt = {"format":"degree-eight-link-trace-v1", "link_records":small_link_records(),
               "trace_cases":trace_cases()}
    text = json.dumps(rebuilt, separators=(",", ":")) + "\n"
    assert text.encode() == (here / "turn5_degree8_certificate.json").read_bytes()
    degree8 = verify_degree8(here / "turn5_degree8_certificate.json")
    assert json.loads(json.dumps(table())) == json.loads((here / "turn5_counting_bounds.json").read_text())
    packed = (here / "turn5_tau4_partial_certificate.json.gz").read_bytes()
    data = json.loads(gzip.decompress(packed))
    with tempfile.TemporaryDirectory() as directory:
        directory = Path(directory)
        binary = directory / "search"
        subprocess.run(["g++", "-O2", "-std=c++17", "-Wall", "-Wextra", "-Werror",
                        str(here / "critical_tau4_search.cpp"), "-o", str(binary)], check=True)
        cases = []
        for case in data["cases"]:
            target = directory / "proof.json"
            run = subprocess.run([str(binary),str(case["edges"]),str(case["maximum_degree"]),
                                  str(target),"25000"],text=True,capture_output=True,check=True)
            result = json.loads(run.stdout)
            assert not result["aborted"] and result["satisfiable"] is False
            cases.append(json.loads(target.read_text()))
        regenerated = {"format":"critical-tau4-partial-cover-tree-v1", "cases":cases}
        assert regenerated == data
        regenerated_bytes = gzip.compress(json.dumps(regenerated,separators=(",", ":")).encode(),
                                          compresslevel=9,mtime=0)
        assert regenerated_bytes == packed
    tau4 = verify_tau4(here / "turn5_tau4_partial_certificate.json.gz")
    print(json.dumps({"degree8":degree8,"tau4_completed_cases":tau4,
                      "degree8_bytes_reproduced":True,"tau4_completed_bytes_reproduced":True,
                      "counting_table_reproduced":True,
                      "unfinished_cases_resumed":False},indent=2))


if __name__ == "__main__":
    main()
