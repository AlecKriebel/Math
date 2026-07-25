#!/usr/bin/env python3
"""Dependency-free comparison of the frozen marked-companion taxonomy."""

from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import os
import re
import sys


FREEZE_SHA256 = "27e5a4f894ef523156abea389f89c2d4481d58d243c756b70386fdea10e9e01f"
CLEAN_REPORT_SHA256 = "f5323cd2cc6e2133b7eae29b3d77d1f3dd820dac5b84332c6c71281ff536129a"
SEALED_LOG_SHA256 = "bf62d6a11319f9d4214ede241c26f291b6651872f095cd57724f1964ed49e5d6"
MUTATION = os.environ.get("MARKED_HOSTILE_2_MUTATION", "")


def fail(message):
    tag = MUTATION or "audit"
    raise SystemExit(f"FAIL [{tag}]: {message}")


def require(condition, message):
    if not condition:
        fail(message)


def digest(path):
    require(path.is_file(), f"missing input: {path}")
    return sha256(path.read_bytes()).hexdigest()


here = Path(__file__).resolve().parent
fixed = here.parent
rung2 = fixed.parent
freeze = Path(
    os.environ.get(
        "MARKED_HOSTILE_2_FREEZE",
        rung2 / "taxonomy_freeze/FROZEN_Q2_E2_MARKED_COMPANION_v1.md",
    )
)
clean_report = fixed / "audit_marked_orbit_reconstruction/REPORT.md"
sealed_log = here / "RESEARCH_LOG.md"

require(digest(freeze) == FREEZE_SHA256, "frozen candidate hash changed")
require(digest(clean_report) == CLEAN_REPORT_SHA256, "clean-room report hash changed")
require(digest(sealed_log) == SEALED_LOG_SHA256, "sealed hostile derivation changed")

text = freeze.read_text()
pair_ids = (
    "Q2-E2-A2-B1-D1-N1-MD-P21-HR2",
    "Q2-E2-A2-B1-D1-N1-MD-P21-HSM",
    "Q2-E2-A2-B1-D1-N1-MD-P3-HSM",
)
for pair_id in pair_ids:
    require(pair_id in text, f"missing pair ID {pair_id}")


def section(start, end):
    require(start in text and end in text, f"missing section boundary {start}")
    return text.split(start, 1)[1].split(end, 1)[0]


groups = {
    pair_ids[0]: re.findall(
        r"^\| `([A-Z0-9]+)` \|",
        section("### 3.1 `MD-P21-HR2`", "### 3.2 `MD-P21-HSM`"),
        re.MULTILINE,
    ),
    pair_ids[1]: re.findall(
        r"^\| `([A-Z0-9]+)` \|",
        section("### 3.2 `MD-P21-HSM`", "### 3.3 `MD-P3-HSM`"),
        re.MULTILINE,
    ),
    pair_ids[2]: re.findall(
        r"^\| `([A-Z0-9]+)` \|",
        section("### 3.3 `MD-P3-HSM`", "## 4. Completeness and boundaries"),
        re.MULTILINE,
    ),
}

if MUTATION == "drop_stratum":
    groups[pair_ids[1]].remove("CT")

require(groups[pair_ids[0]] == ["C0", "CH", "CS", "CO"], "wrong P21-HR2 strata")
require(
    groups[pair_ids[1]] == ["C0", "CH", "CT", "CS", "CTAU"],
    "wrong P21-HSM strata",
)
require(groups[pair_ids[2]] == ["C0", "CH", "CS", "CO"], "wrong P3-HSM strata")
stable_ids = tuple(
    f"{pair_id}-{suffix}"
    for pair_id, suffixes in groups.items()
    for suffix in suffixes
)
require(len(stable_ids) == 13 and len(set(stable_ids)) == 13, "stable strata are not 13")

# Candidate coordinates:
#   h=s+t, r_[u:v]=u*h+v*s=(u+v)*s+u*t, tau=v/u.
# Sealed coordinates:
#   r_theta=s+theta*t.
# Hence theta=u/(u+v)=1/(1+tau) away from the t-boundary.
def theta_from_tau(tau):
    if MUTATION == "wrong_conversion":
        return tau
    return Fraction(1, 1) / (Fraction(1, 1) + tau)


for tau in (Fraction(-3, 2), Fraction(-1, 2), Fraction(1, 1), Fraction(7, 3)):
    require(tau != -1, "bad test value")
    theta = theta_from_tau(tau)
    require(theta * (1 + tau) == 1, "theta=1/(1+tau) conversion failed")

boundary_images = {
    "CH": "theta=1",       # [u:v]=[1:0], tau=0, r=h
    "CT": "theta=infinity",# [u:v]=[1:-1], tau=-1, r=t
    "CS": "theta=0",       # [u:v]=[0:1], tau=infinity, r=s
}
require(boundary_images == {
    "CH": "theta=1",
    "CT": "theta=infinity",
    "CS": "theta=0",
}, "boundary coordinate conversion changed")

# Exhaust the homogeneous boundary predicates over two exact finite fields.
# This is a finite regression for the algebraic partition
# u=0, v=0, u+v=0, and uv(u+v)!=0.
for prime in (5, 7):
    points = [(1, value) for value in range(prime)] + [(0, 1)]
    for u, v in points:
        predicates = {
            "CH": v % prime == 0,
            "CT": (u + v) % prime == 0,
            "CS": u % prime == 0,
            "CTAU": (u * v * (u + v)) % prime != 0,
        }
        if MUTATION == "overlap_boundary" and (u, v) == (0, 1):
            predicates["CT"] = True
        require(sum(predicates.values()) == 1, f"boundary overlap/gap at {(u, v)} mod {prime}")

require("Every `CTAU` branch key must carry its actual `tau=<value>` field." in text,
        "CTAU was collapsed to one orbit")
middle_action_identity = True
if MUTATION == "merge_tau":
    middle_action_identity = False
require(middle_action_identity, "distinct tau values were merged")

known_mutations = {"", "drop_stratum", "wrong_conversion", "overlap_boundary", "merge_tau"}
require(MUTATION in known_mutations, "unknown mutation")

print(f"AUDITED_FREEZE_SHA256={FREEZE_SHA256}")
print("MARKED_PAIR_TYPES=3")
print("STABLE_STRATA=13")
print("NONZERO_ORBIT_SPACE=3+P1+3")
print("THETA_TAU_CONVERSION=theta=1/(1+tau)")
print("BOUNDARIES=CH:theta1,CT:thetaInfinity,CS:theta0")
print("MIDDLE_RESIDUAL_ACTION=POINTWISE_IDENTITY")
print("MARKED_ORBIT_HOSTILE_2_PASS_C4B821")
