"""Rebuild the finite certificate in temporary storage and check every node."""
from pathlib import Path
import copy
import gzip
import json
import subprocess
import tempfile
from verify_tau3_certificate import verify, verify_case


def main():
    here = Path(__file__).resolve().parent
    cases, results = [], []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        binary = tmp / "critical_search"
        subprocess.run(["g++", "-O2", "-std=c++17", "-Wall", "-Wextra", "-Werror",
                        str(here / "critical_tau3_search.cpp"), "-o", str(binary)], check=True)
        for m in range(6, 11):
            for d in range(4, m - 1):
                proof = tmp / f"proof_{m}_{d}.json"
                run = subprocess.run([str(binary), str(m), str(d), str(proof)],
                                     text=True, capture_output=True, check=True)
                results.append(json.loads(run.stdout))
                cases.append(json.loads(proof.read_text()))
        data = dict(format="critical-tau3-cover-tree-v1", cases=cases)
        packed = gzip.compress(json.dumps(data, separators=(",", ":")).encode(),
                               compresslevel=9, mtime=0)
        certificate = tmp / "certificate.json.gz"
        certificate.write_bytes(packed)
        checked = verify(certificate)
        assert all(not result["satisfiable"] for result in results)
        same = packed == (here / "turn3_tau3_certificate.json.gz").read_bytes()
        assert json.loads(gzip.decompress(packed)) == json.loads(
            gzip.decompress((here / "turn3_tau3_certificate.json.gz").read_bytes()))
        rejected = []
        altered = copy.deepcopy(cases[0])
        altered["nodes"][0][0] = 0  # not a five-element target
        try:
            verify_case(altered)
        except AssertionError:
            rejected.append("invalid target")
        else:
            raise AssertionError("checker accepted an invalid target")
        altered = copy.deepcopy(cases[0])
        assert altered["nodes"][0][1]
        altered["nodes"][0][1].pop()  # omit a required branch
        try:
            verify_case(altered)
        except AssertionError:
            rejected.append("omitted branch")
        else:
            raise AssertionError("checker accepted an incomplete branch list")
        checked["reproduced_compressed_bytes"] = same
        checked["corruptions_rejected"] = rejected
        print(json.dumps(checked, indent=2))


if __name__ == "__main__":
    main()
