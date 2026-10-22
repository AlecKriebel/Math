#!/usr/bin/env python3
"""Read-only byte binding and independent finite controls; not a proof certificate."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent
PRIVATE = ROOT / "private"
HEAD = "17d392e35fe4a0169d8d4c205d459155b7673d9b"
BASE = "4b27092a448d53b61408355ce44ec38d103a1ce4"


def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def determinant(a):
    a = [list(map(Q, row)) for row in a]
    value = Q(1)
    for k in range(len(a)):
        j = next((j for j in range(k, len(a)) if a[j][k]), None)
        if j is None:
            return Q(0)
        if j != k:
            a[k], a[j] = a[j], a[k]
            value = -value
        pivot = a[k][k]
        value *= pivot
        for j in range(k + 1, len(a)):
            multiplier = a[j][k] / pivot
            for i in range(k + 1, len(a)):
                a[j][i] -= multiplier * a[k][i]
    return value


def inner(a, b, points, weights):
    return sum(w * sum(c * x**i for i, c in enumerate(a)) *
               sum(c * x**i for i, c in enumerate(b))
               for x, w in zip(points, weights))


def gram_schmidt_norms(n, points, weights):
    polynomials, norms = [], []
    for k in range(n):
        poly = [Q(0)] * k + [Q(1)]
        for old, norm in zip(polynomials, norms):
            coefficient = inner(poly, old, points, weights) / norm
            for i, value in enumerate(old):
                poly[i] -= coefficient * value
        norm = inner(poly, poly, points, weights)
        require(norm > 0, "positive definite finite moment form")
        polynomials.append(poly)
        norms.append(norm)
    return math.prod(norms)


def vandermonde_square(xs):
    return math.prod((xs[i] - xs[j])**2
                     for i in range(len(xs)) for j in range(i))


def algebra_controls():
    cases = []
    for n in range(2, 5):
        points = list(map(Q, range(1, 2*n + 1)))
        weights = [Q(1, 2*n)] * (2*n)
        matrix = [[sum(w*x**(i+j) for x, w in zip(points, weights))
                   for j in range(n)] for i in range(n)]
        direct = determinant(matrix)
        raw = sum(vandermonde_square(xs) for xs in product(points, repeat=n)) / (2*n)**n
        require(direct == raw / math.factorial(n), "Heine factorial")
        require(direct == gram_schmidt_norms(n, points, weights), "monic norm product")
        cells = [points[2*k:2*k+2] for k in range(n)]
        restricted = sum(vandermonde_square(xs) for xs in product(*cells)) / (2*n)**n
        conditional = sum(vandermonde_square(xs) for xs in product(*cells)) / 2**n
        labeled = math.factorial(n) * restricted
        require(labeled / math.factorial(n) == restricted, "labeled-order cancellation")
        require(restricted == Q(1, n**n) * conditional, "cell mass N^-N")
        require(direct >= restricted > 0, "nonnegative restriction")
        for c in [Q(1, 7), Q(1), Q(11, 3)]:
            require(c**(n*n)/c**(n*(n-1)) == c**n, "capacity exponent")
        require(raw != direct, "negative control missing factorial must disagree")
        require(conditional != restricted, "negative control missing N^-N must disagree")
        require(n*n-n*(n-1) != n-1, "negative control wrong capacity exponent")
        cases.append({"N": n, "determinant": str(direct),
                      "one_point_per_cell_integral": str(restricted)})
    return cases


def quantile_controls():
    # Uniform probability on [0,1] union [2,3], reference dx/3.
    # At frequency1/2 the right-endpoint inverse must equal2, not1.
    def q(t):
        return 2*t if t < Q(1, 2) else 2*t+1
    entropies = []
    for m in range(1, 10):
        n = 2**m
        cuts = [Q(0)] + [q(Q(k, n)) for k in range(1, n)] + [Q(3)]
        lengths = [b-a for a, b in zip(cuts, cuts[1:])]
        require(all(x > 0 for x in lengths) and sum(lengths) == 3, "quantile lengths")
        beta = [x/3 for x in lengths]
        h = sum(math.log((1/n)/float(b)) for b in beta)/n
        entropies.append(h)
        if m == 1:
            require(beta == [Q(2, 3), Q(1, 3)], "gap-atom boundary ownership")
            require(beta != [Q(1, 3), Q(2, 3)], "left-endpoint inverse control")
    require(all(a <= b + 1e-14 for a,b in zip(entropies, entropies[1:])), "dyadic refinement")
    require(abs(entropies[-1]-math.log(1.5)) < 0.011, "entropy convergence with gap")
    # Singular Cantor probability, not claimed to be the equilibrium measure.
    # Exact dyadic right-endpoint inverse uses binary digits as ternary0/2.
    singular = []
    for m in range(1, 13):
        n, denominator = 2**m, 3**m
        nums = [0]
        for k in range(1, n):
            nums.append(sum(2*((k >> (m-j)) & 1)*3**(m-j) for j in range(1,m+1)))
        nums.append(denominator)
        increments = [b-a for a,b in zip(nums, nums[1:])]
        require(min(increments) > 0 and sum(increments) == denominator, "singular quantile cells")
        h = sum(math.log(denominator/(n*d)) for d in increments)/n
        singular.append(h)
    require(all(a < b for a,b in zip(singular, singular[1:])), "singular entropy growth")
    require(singular[-1] > 3, "gap collapse did not erase singular entropy")
    return {"two_interval_entropy": entropies,
            "limit_log_3_over_2": math.log(1.5),
            "singular_cantor_entropy": singular,
            "scope": "finite diagnostics; singular Cantor probability is not assumed equilibrium"}


def interval_controls():
    # Exact arcsine equilibrium moments on [-1,1], capacity1/2.
    def moment(k):
        return Q(0) if k % 2 else Q(math.comb(k,k//2), 2**k)
    determinants = []
    for n in range(1,9):
        d = determinant([[moment(i+j) for j in range(n)] for i in range(n)])
        expected = math.prod(Q(1,2**(2*k-1)) for k in range(1,n))
        require(d == expected, "interval monic norm product")
        if determinants:
            norm_squared = d/determinants[-1]
            require(norm_squared / Q(1,2)**(2*(n-1)) == 2, "interval W2^2 equals2")
        determinants.append(d)
    # Affine invariance: L and capacity both scale by the same positive factor.
    for scale in [Q(1,9),Q(1),Q(27)]:
        require(4*(scale/2)/(2*scale) == 1, "interval4c/L")
    return {"degrees": "0..7", "W2_squared_degrees1_to7": 2,
            "PW_interval": 0, "entropy_interval": "log(4/pi)",
            "scope": "moments/norms exact; entropy value follows the written density identity"}


def bindings():
    pr = json.loads((PRIVATE / "pr.json").read_text())
    require(pr["head"]["sha"] == HEAD and pr["base"]["sha"] == BASE, "PR pins")
    require(pr["state"] == "open" and pr["draft"], "captured PR state")
    binding = json.loads((ROOT / "PR_BINDING.json").read_text())
    require(sha(pr["body"].encode()) == binding["body_sha256"], "body hash")
    final = json.loads((ROOT/"FINAL_PR_RECHECK.json").read_text())
    require(final["head"] == HEAD and final["base"] == BASE and
            final["body_sha256"] == binding["body_sha256"] and
            final["state"] == "open" and final["draft"] and final["changed_files"] == 8,
            "fresh final PR recheck")
    files = json.loads((PRIVATE / "files.json").read_text())
    require(len(files) == 8 and not any("QUEUE" in f["filename"] for f in files), "eight-file scope")
    for pin in binding["eight_blobs"]:
        data = (PRIVATE / Path(pin["path"]).name).read_bytes()
        require(len(data) == pin["bytes"] and sha(data) == pin["sha256"], "blob SHA256")
        require(hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
                == pin["git_blob_sha"], "Git blob SHA")
    manifest = json.loads((PRIVATE / "MANIFEST.json").read_text())
    require(sorted(manifest["members"]) == sorted(Path(f["filename"]).name for f in files), "manifest members")
    for entry in manifest["entries"]:
        data = (PRIVATE / entry["file"]).read_bytes()
        require(sha(data) == entry["sha256"] and len(data) == entry["bytes"], "manifest entry")
    receipt = json.loads((ROOT / "PRIMARY_RECEIPT.json").read_text())
    for entry in receipt["sources"]:
        if "error" not in entry:
            data = (PRIVATE / entry["name"]).read_bytes()
            require(len(data) == entry["bytes"] and sha(data) == entry["sha256"], "primary source pin")
    require(sha((PRIVATE/"source_v1.pdf").read_bytes()) ==
            "e9c3152c41d6c3f98aee305ad3dee9c3b123419c12aad32cf855e70952d8d435", "v1 exact PDF")
    require(sha((PRIVATE/"original.pdf").read_bytes()) ==
            "44ab98dccecffaedea3eadaca8631550015ab1f4907e09227964755a350aa5b7", "original exact PDF")
    require(len((PRIVATE/"source_v1.txt").read_text().split("\f")) == 35, "34 extracted primary PDF pages")
    clearance = json.loads((ROOT/"GWS_CLEARANCE.json").read_text())
    require(sha((PRIVATE/"GWS_FULL43.json").read_bytes()) == clearance["sha256"], "fresh GWS body pin")
    require(clearance["numeric_gid"] == 1254632077 and clearance["requested_columns"] == 43,
            "numeric gid full width")
    require(clearance["rows_including_header"] == 191, "tracker snapshot row count")
    require(not any(clearance["lead_scan"].values()), "duplicate lead scan")
    registry = json.loads((PRIVATE/"datacite.json").read_text())["data"]["attributes"]
    require(registry["doi"] == "10.48550/arxiv.2608.17321" and registry["version"] == "1", "registry identity")
    require([c["familyName"] for c in registry["creators"]] == ["Alpan", "Zinchenko"], "source authors")
    # File and seal integrity are evidence custody, not theorem correctness.
    seal = ROOT/"PRIVATE_BODY_SEAL.json"
    require(seal.exists(), "required private body seal")
    for pin in json.loads(seal.read_text())["private_files"]:
        data = (ROOT/pin["path"]).read_bytes()
        require(len(data) == pin["bytes"] and sha(data) == pin["sha256"], "private body seal")
    proposal = json.loads((ROOT/"LITERAL_FOUR_CELL_PROPOSAL.json").read_text())
    cells = proposal["literal_cells"]
    require(len(cells) == 4 and cells[1] == "", "exact four cells; blankB")
    require(cells[2] == "https://doi.org/10.48550/arXiv.2608.17321", "same-paper existing DOI")
    require(proposal["status"] == "PROPOSAL_ONLY_NOT_APPENDED", "accounting incomplete")
    return {"head": HEAD, "base": BASE, "blobs": len(files),
            "source_PDF_pages": 34, "tracker_rows": 191,
            "journal_or_peer_review_certified": False}


if __name__ == "__main__":
    print(json.dumps({"status": "PASS", "bindings": bindings(),
                      "exact_finite_algebra": algebra_controls(),
                      "interval_equilibrium_controls": interval_controls(),
                      "quantile_controls": quantile_controls(),
                      "negative_controls_rejected": ["missing factorial", "missing N^-N",
                        "wrong capacity exponent", "left quantile gap-boundary ownership"],
                      "theorem_correctness_basis": "independent written argument in REPORT.md; not this finite checker",
                      "source_programs_executed": False,
                      "network_or_service_writes": False}, indent=2))
