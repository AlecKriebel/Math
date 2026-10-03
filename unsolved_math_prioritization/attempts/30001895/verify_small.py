"""Independent small-instance brute-force check of exhaustive_uniform.cpp."""
from itertools import combinations
from pathlib import Path
import json
import subprocess
import tempfile


def run():
    here = Path(__file__).resolve().parent
    checks = []
    with tempfile.TemporaryDirectory() as tmp:
        binary = str(Path(tmp) / "exhaustive")
        subprocess.run(["g++", "-O2", "-std=c++17", "-Wall", "-Wextra", "-Werror",
                        str(here / "exhaustive_uniform.cpp"), "-o", binary], check=True)
        for n, r in [(4, 2), (5, 3)]:
            edges = [sum(1 << v for v in edge) for edge in combinations(range(n), r)]
            proper = equalities = violations = 0
            for mask in range(1 << len(edges)):
                selected = [e for j, e in enumerate(edges) if mask >> j & 1]
                delta = max(sum(bool(e >> v & 1) for e in selected) for v in range(n))
                if delta <= r:
                    continue
                proper += 1
                tau = min(x.bit_count() for x in range(1 << n)
                          if all(x & e for e in selected))
                nu = 0
                for sub in range(1 << len(selected)):
                    if sub.bit_count() <= nu:
                        continue
                    if all(sum(bool(sub >> i & 1) and bool(e >> v & 1)
                               for i, e in enumerate(selected)) <= r for v in range(n)):
                        nu = sub.bit_count()
                gap = tau + r - 1 - nu
                equalities += gap == 0
                violations += gap > 0
            expected = json.loads(subprocess.check_output([binary, str(n), str(r)], text=True))
            actual = dict(delta_gt_r=proper, equalities=equalities, violations=violations)
            assert all(expected[k] == v for k, v in actual.items())
            checks.append(dict(n=n, r=r, agrees=True, **actual))
    output = dict(method="Direct enumeration of all vertex subsets and all edge subfamilies, independent of the C++ recurrences.", checks=checks)
    print(json.dumps(output, indent=2))
    return output


if __name__ == "__main__":
    run()
