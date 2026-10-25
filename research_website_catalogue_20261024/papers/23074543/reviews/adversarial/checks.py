"""Independent bounded diagnostics; never executes the supplied verification package.

Reads original bytes and writes only own custody/diagnostic JSON in this directory.
No network, subprocess, package installation, extraction, or original-file mutation.
"""

from datetime import datetime, timezone
from hashlib import sha256
from itertools import combinations
from pathlib import Path, PurePosixPath
import json
import stat
import sys
import zipfile
import sympy as s

HERE = Path(__file__).resolve().parent
SOURCES = HERE.parents[1] / "sources"
PAPER = HERE.parents[1]
EXPECTED_SOURCE_SEAL = "d90cab38270ee9029390eb6f4bafa1c994aae335beb1c5cdd453d29a1fa4e50c"


def digest(blob):
    return sha256(blob).hexdigest()


def write_json(name, value):
    target = HERE / name
    if target.exists():
        raise RuntimeError(f"Refusing overwrite of evidence {target}")
    target.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def custody():
    seal_bytes = (SOURCES / "SOURCE_READY_SEAL.json").read_bytes()
    assert digest(seal_bytes) == EXPECTED_SOURCE_SEAL
    seal = json.loads(seal_bytes)
    assert seal["file_count"] == len(seal["files"]) == 97
    bindings = []
    for entry in seal["files"]:
        blob = (SOURCES / entry["path"]).read_bytes()
        actual = {"path": entry["path"], "bytes": len(blob), "sha256": digest(blob)}
        actual["matches_source_ready_binding"] = (
            actual["bytes"] == entry["bytes"] and actual["sha256"] == entry["sha256"]
        )
        assert actual["matches_source_ready_binding"]
        bindings.append(actual)
    archive_members = []
    with zipfile.ZipFile(SOURCES / "source-and-verification.zip") as archive:
        entries = archive.infolist()
        assert len(entries) == 87
        assert len({entry.filename for entry in entries}) == len(entries)
        for entry in entries:
            name = PurePosixPath(entry.filename)
            mode = entry.external_attr >> 16
            safe = (
                not name.is_absolute()
                and ".." not in name.parts
                and "\\" not in entry.filename
                and not stat.S_ISLNK(mode)
                and not entry.is_dir()
            )
            assert safe
            # ZipFile.read performs its own CRC validation. No extraction occurs.
            blob = archive.read(entry)
            extracted = (SOURCES / "published-source" / entry.filename).read_bytes()
            assert blob == extracted
            archive_members.append({
                "member": entry.filename, "bytes": len(blob),
                "sha256": digest(blob), "CRC32": f"{entry.CRC:08x}",
                "safe": safe, "CRC_read_pass": True,
                "matches_extracted_original": True,
            })
    metadata = json.loads((SOURCES / "zenodo-record.raw.json").read_text())
    created = datetime.fromisoformat(metadata["created"])
    from zoneinfo import ZoneInfo
    return {
        "utc": datetime.now(timezone.utc).isoformat(),
        "status": "ALL_97_ORIGINAL_BINDINGS_AND_87_ARCHIVE_MEMBERS_VERIFIED",
        "source_ready_seal_sha256": EXPECTED_SOURCE_SEAL,
        "bindings": bindings,
        "archive_members": archive_members,
        "edition": {
            "record": metadata["id"], "version": metadata["metadata"].get("version"),
            "declared_publication_date": metadata["metadata"]["publication_date"],
            "record_created_utc": metadata["created"],
            "record_created_America_Los_Angeles": created.astimezone(ZoneInfo("America/Los_Angeles")).isoformat(),
            "record_updated_utc": metadata["updated"],
            "date_interpretation": "Declared 2026-09-30 is consistent with local record creation date; it is not an independently certified priority timestamp.",
        },
        "original_source_code_executed": False,
        "original_bytes_mutated": False,
    }


def diagnostic_checks():
    a, b, X, Y, Z = s.symbols("a b X Y Z", real=True)
    P = (X**2 + Y**2 + Z**2 - 5)**2 - 4*(4-Y**2)*(1-Z**2)
    substitution = {X: a+b, Y**2: 4-a**2, Z**2: 1-b**2}
    residual = s.expand(P.subs(X, a+b)).subs({Y**2: 4-a**2, Z**2: 1-b**2})
    assert s.expand(residual) == 0
    separation = P.subs({X: 0, Y: 0, Z: 1})
    assert separation == 16
    P_wrong = (X**2 + Y**2 + Z**2 - 5)**2 - (4-Y**2)*(1-Z**2)
    wrong_residual = s.expand(s.expand(P_wrong.subs(X, a+b)).subs({Y**2: 4-a**2, Z**2: 1-b**2}))
    assert wrong_residual == 3*a**2*b**2
    assert wrong_residual.subs({a: 1, b: 1}) == 3

    # Three non-orthonormal rank-2 maps in R^5. Every pair has rank 4,
    # all three have rank 5, and u annihilates two summands simultaneously.
    A1 = s.Matrix([[2,1], [0,3], [0,0], [0,0], [0,0]])
    A2 = s.Matrix([[0,0], [0,0], [1,2], [0,2], [0,0]])
    A3 = s.Matrix([[1,2], [1,2], [1,2], [1,2], [1,3]])
    maps = [A1, A2, A3]
    ranks = []
    for n in range(1, 4):
        for J in combinations(range(3), n):
            actual = s.Matrix.hstack(*(maps[j] for j in J)).rank()
            assert actual == min(5, 2*n)
            ranks.append({"subset": [j+1 for j in J], "rank": actual})
    u = s.Matrix([0,0,0,0,1])
    v1, v2 = s.Matrix([s.Rational(3,5),s.Rational(4,5)]), s.Matrix([s.Rational(5,13),s.Rational(12,13)])
    w = s.Matrix([s.Rational(3,10),s.Rational(1,6),s.Rational(5,13),s.Rational(1,13),0])
    assert (v1.T*v1)[0] == (v2.T*v2)[0] == 1
    assert A1.T*u == A2.T*u == s.zeros(2,1)
    assert A1.T*w == v1 and A2.T*w == v2
    eps = s.symbols("eps", positive=True)

    def point(A, normal):
        t = A.T*normal
        return (A*t / s.sqrt((t.T*t)[0])).applyfunc(s.simplify)

    assert point(A1, u+eps*w) == A1*v1
    assert point(A2, u+eps*w) == A2*v2
    p3 = point(A3, u+eps*w)
    p3_limit = p3.applyfunc(lambda z: s.limit(z, eps, 0, dir="+"))
    assert (p3_limit-point(A3,u)).applyfunc(s.simplify) == s.zeros(5,1)

    # A repeated-span negative control: opposite boundary coordinates cannot
    # be simultaneously selected by a common first-order normal.
    repeated = s.Matrix([[1,0], [0,1], [0,0]])
    transposed = s.Matrix.hstack(repeated, repeated).T
    incompatible = s.Matrix([1,0,-1,0])
    assert transposed.rank() == 2
    assert transposed.row_join(incompatible).rank() == 3

    # Finite rational Vandermonde diagnostic. The general determinant proof
    # belongs to the report, and no finite test purports to establish it.
    columns = [s.Matrix([t**k for k in range(5)]) for t in range(9)]
    blocks = [s.Matrix.hstack(*columns[:2]), s.Matrix.hstack(*columns[2:5]), s.Matrix.hstack(*columns[5:])]
    vandermonde_ranks = []
    sizes = [2,3,4]
    for n in range(1,4):
        for J in combinations(range(3),n):
            rank = s.Matrix.hstack(*(blocks[j] for j in J)).rank()
            expected = min(5,sum(sizes[j] for j in J))
            assert rank == expected
            vandermonde_ranks.append({"subset": [j+1 for j in J], "rank": rank})
    return {
        "utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "sympy": s.__version__,
        "separating_polynomial_residual": str(s.expand(residual)),
        "P_e3": str(separation), "wrong_polynomial_negative_control": str(wrong_residual),
        "nonorthonormal_multi_annihilator_GP_ranks": ranks,
        "prescribed_v1": list(map(str,v1)), "prescribed_v2": list(map(str,v2)),
        "solving_w": list(map(str,w)),
        "positive_epsilon_support_points_exact": True,
        "remaining_support_point_limit_exact": True,
        "repeated_span_constraint_rank": 2, "incompatible_augmented_rank": 3,
        "rational_vandermonde_ranks": vandermonde_ranks,
        "all_assertions_passed": True,
        "scope": "Exact finite diagnostics and negative controls; universal conclusions rely on the separate mathematical derivations.",
    }


if __name__ == "__main__":
    write_json("ORIGINAL_BINDING_RECEIPT.json", custody())
    write_json("EXACT_CONTROLS.json", diagnostic_checks())
    print("Custody: all 97 bindings and 87 members verified. Exact diagnostic assertions passed.")
