#!/usr/bin/env python3
"""Read-only input checks and exact rational checks for this priority audit.

The only write is CHECK_RESULTS.json inside this audit's directory.
No third-party code, simulation, network call, or central proof search is run.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
checks = []


def check(name, condition, evidence=None):
    checks.append({"name": name, "pass": bool(condition), "evidence": evidence})


def fraction(x):
    return {"fraction": str(x), "decimal_for_orientation_only": float(x)}


ledger = json.loads((HERE / "SOURCE_LEDGER.json").read_text())
for source in ledger["sources"]:
    for entry in source["files"]:
        path = HERE / entry["path"]
        data = path.read_bytes()
        check("source pin: " + entry["path"],
              len(data) == entry["bytes"]
              and hashlib.sha256(data).hexdigest() == entry["sha256"])

meta = json.loads((HERE / "private_sources/ferudun_metadata_20261015.json").read_text())
paper = (HERE / "private_sources/eulersolve_0023_v1.pdf").read_bytes()
check("primary PDF matches served metadata hash",
      hashlib.sha256(paper).hexdigest() == meta["files"]["paper.pdf"]["sha256"])
check("served primary version and claimed release",
      meta["version"] == "1.0" and meta["publication_date"] == "2026-10-14")
text = (HERE / "private_sources/eulersolve_0023_v1.txt").read_text()
check("primary extract explicitly names Conjecture 32(a)",
      "Conjecture 32(a)" in text)
check("primary extract explicitly limits k<1 quantitative extension",
      "this part is only a" in text and "sketch" in text)

# Independently check the source's explicit scalar-strip instance.
alpha, beta, a = F(2), F(3), F(1, 4)
k = 2 * alpha / beta
delta, r, rho = F(1, 20), F(1, 100), F(1, 100000)
q0 = k * (a + 1 / (12 * a))
ha = a / (k * (4 * a * a + 1))
ka = (a * a + F(1, 4)) / (2 * a * a)


def q(h):
    return q0 / (1 - ka * (2 * k * h) ** 2)


check("source k and two-city stable-slope range", k == F(4, 3) and k * k < 3)
check("source q0 and h_a", q0 == F(7, 9) and ha == F(3, 20))
check("source small interval hypothesis", delta < ha / 2)
check("source q(2delta)", q(2 * delta) == F(35, 37) and q(2 * delta) < 1)
check("source position-neighborhood hypothesis", 0 < rho < min(r, F(1, 2) - a))
x = rho / r
# artanh bounds follow by bounding the positive power-series tail.
atanh_lo = x + x**3 / 3
atanh_hi = x + x**3 / (3 * (1 - x*x))
eps_lo, eps_hi = atanh_lo / k, atanh_hi / k
check("epsilon upper bound fits delta", 0 < eps_lo <= eps_hi < delta,
      {"epsilon_lower": fraction(eps_lo), "epsilon_upper": fraction(eps_hi)})


def atan_bounds(x, terms):
    s = sum(((-1)**j * x**(2*j+1) / (2*j+1) for j in range(terms)), F(0))
    next_term = (-1)**terms * x**(2*terms+1) / (2*terms+1)
    return min(s, s + next_term), max(s, s + next_term)


# Machin's identity pi=16 arctan(1/5)-4 arctan(1/239), with alternating bounds.
a5lo, a5hi = atan_bounds(F(1, 5), 20)
a239lo, a239hi = atan_bounds(F(1, 239), 6)
pi_lo, pi_hi = 16*a5lo - 4*a239hi, 16*a5hi - 4*a239lo
check("independent classical pi enclosure", 3 < pi_lo <= pi_hi < F(355, 113))
q_hi = q(delta + eps_hi)
eta_lo = (delta/2) * (1 - q_hi) - eps_hi - 2 * F(355, 113) * r*r
check("q(delta+epsilon) upper bound", q_hi < F(81510, 100000))
check("strict positive inward-strip margin", eta_lo > F(32441, 10000000),
      {"eta_lower": fraction(eta_lo)})
check("explicit invariant interval", F(1, 2)-delta == F(9, 20)
      and F(1, 2)+delta == F(11, 20))

# Every-k slope formula is affine: k in (0,1) gives g'(1/2)=7k/12-1<-5/12.
# This is finite exact arithmetic for the uniform coefficient; the report gives
# the analytic derivative/continuity/barrier argument, which finite checks cannot replace.
check("same-regime slope coefficient is strictly below one", F(7, 12) < 1)
check("same-regime drift slope uniform upper bound", F(7, 12)-1 == -F(5, 12))

chronology = json.loads((HERE.parent / "ROOT_PR_CHRONOLOGY.json").read_text())
check("own PR frozen head", chronology["pr"]["headRefOid"]
      == "fba74a301786f9648e48722e76f440097b0746c2")
check("own PR recorded creation predates other paper's asserted date",
      chronology["pr"]["createdAt"][:10] < meta["publication_date"],
      {"PR_createdAt": chronology["pr"]["createdAt"],
       "other_claimed_publication_date": meta["publication_date"],
       "limitation": "Recorded chronology only, not global priority or historic byte authentication."})

out = {"timestamp_utc": datetime.now(timezone.utc).isoformat(),
       "checks": checks, "passed": sum(c["pass"] for c in checks),
       "total": len(checks), "all_pass": all(c["pass"] for c in checks),
       "limits": "Source identities, source assertions, finite rational constants and recorded chronology only. Analytic transfer is written in TRANSFER_CHECK.md. No global novelty or stochastic proof certification."}
(HERE / "CHECK_RESULTS.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps({k: out[k] for k in ("passed", "total", "all_pass")}))
raise SystemExit(0 if out["all_pass"] else 1)
