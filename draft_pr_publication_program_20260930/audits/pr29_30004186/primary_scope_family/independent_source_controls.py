#!/usr/bin/env python3
"""Bounded source/scope/provenance adversarial controls; no PDE simulation.

This independently checks distinctions. It does not turn finite assertions into
a nonlinear existence proof, historical model attestation, or priority claim.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
HEAD = "5ac4a57e08dd72a6f16768f2288b9c0349999431"
BASE = "c6975ca76f9f667f1250ba403d0e6da2aafe14d0"
TARGET = "unsolved_math_prioritization/attempts/30004186/"
CAN_SHA = "95458afe7f030f3f0aec3b9d5150857e7dedcb8688e6325c4a0407497feb1b6c"
CTX = "759ed8f6518e7a61a2356296cdc080f951f41bc93ca448182f1ce2143cda5a7b"
SEAL_SHA = "73c09afcb60622609bea8742a01f8667c231d34b32cb5df5556814cab33af6bd"
checks = []
mutants = []

def check(name, ok, evidence):
    assert bool(ok), name
    checks.append({"name": name, "status": "PASS", "evidence": evidence})

def reject(name, predicate, evidence):
    assert not bool(predicate), name
    mutants.append({"name": name, "status": "REJECTED", "evidence": evidence})

def sha(data):
    return hashlib.sha256(data).hexdigest()

def ctx(problem, prior):
    return sha(json.dumps([problem, prior], sort_keys=True).encode())

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)

# Equation discrimination: RO has coefficients 1,1 for u*u_xx,u_x**2;
# NPW, moved to the left, has 2,1. Common scaling multiplies both.
a, b, c = s.symbols("a b c", nonzero=True)
common = a*a*b*b
ro = [common, common]
npw = [2*common, common]
check("nonlinear_coefficient_ratio_invariant", s.cancel(ro[0]/ro[1]) == 1,
      "RO ratio=1 under nonzero affine amplitude/space/time and Galilean scaling")
reject("npw_as_scaled_exact_RO", s.cancel(npw[0]/npw[1]) == 1,
       "NPW ratio=2; affine rescaling does not remove squared-gradient source")
z = s.symbols("z", real=True)
ro_profile = (3*z*z-s.pi*s.pi)/18
eta_profile = z*z/8-s.pi*s.pi/16
check("profile_model_curvature_differs", s.diff(ro_profile,z,2)==s.Rational(1,3)
      and s.diff(eta_profile,z,2)==s.Rational(1,4),
      "The independently read primary models have distinct curvature normalizations")
check("NPW_profile_mean_constraint", s.simplify(s.integrate(eta_profile+s.diff(eta_profile,z)**2,
      (z,-s.pi,s.pi)))==0, "integral[eta+eta_x**2]=0")
reject("NPW_zero_mean_profile", s.integrate(eta_profile,(z,-s.pi,s.pi))==0,
       "Mean eta=-pi**2/48; RO profile has zero mean")

# A shrinking-support witness forbids upgrading fixed gradient discrepancy to
# fixed H1/L2 discrepancy. It is a norm counterexample, not a PDE trajectory.
q = s.symbols("q", real=True)
ep, width, length = s.symbols("ep width length", positive=True)
f = q*(1-q)**2
mass = ep*width**2*s.integrate(f,(q,0,1))
l2sq = ep**2*width**3*s.integrate(f*f,(q,0,1))-mass**2/length
derivative_sq = ep**2*width*s.integrate(s.diff(f,q)**2,(q,0,1))
h1sq = l2sq+derivative_sq
check("shrinking_support_gradient_endpoint", s.diff(f,q).subs(q,0)==1,
      "one-sided slope ep; polynomial derivative bounded in absolute value by 1")
check("shrinking_support_exact_norms", s.simplify(l2sq-(ep**2*width**3/105
      -ep**2*width**4/(144*length)))==0 and derivative_sq==2*ep**2*width/15,
      "Mean-zero correction included in exact L2 norm")
check("shrinking_support_H1_limit", s.limit(h1sq,width,0,dir="+")==0,
      "Fixed gradient ep, H1 and L2 tend to zero")
reject("fixed_gradient_implies_fixed_H1_escape", s.limit(h1sq,width,0,dir="+")>0,
       "No lower support-width bound is supplied by gradient escape alone")

# Qualitative orbital stability admits a nonlinear modulus. It does not imply
# a Lipschitz bound B times the initial perturbation used in the old v1 proof.
B = s.symbols("B", positive=True)
d = 1/(4*B*B)
check("qualitative_modulus_countercontrol", s.simplify(s.sqrt(d)-B*d)>0,
      "sqrt(d)=1/(2B)>B*d=1/(4B), although sqrt(d) tends to zero")
reject("qualitative_stability_implies_Bdelta", s.sqrt(d)<=B*d,
       "A stable continuity modulus can be sqrt(initial size)")
delta = s.symbols("delta", positive=True)
reject("shrinking_escape_is_fixed_threshold", s.limit(B*delta,delta,0,dir="+")>0,
       "A proportional escape threshold vanishes with initial size")

# Translation of a derivative jump is not strongly continuous in W1,infinity.
shift = s.symbols("shift", positive=True)
k = s.pi/3
jump_difference = 2*k-shift/3
check("translated_peak_jump_limit", s.limit(jump_difference,shift,0,dir="+")==2*k,
      "on (0,shift), derivatives of the two translated quadratic peaks differ by 2k-shift/3")
reject("periodic_W1infinity_translation_strong_continuity",
       s.limit(jump_difference,shift,0,dir="+")==0,
       "Candidate correctly uses C1 characteristic/moving-corner coordinates")

# Authenticate the raw join type and context, not only the pretty-printed row.
cache = ROOT/"unsolved_math_prioritization/cache"
manifest = json.loads((ROOT/"unsolved_math_prioritization/manifest.json").read_text())
tree = json.loads((HERE/"UPSTREAM_TREE_RECEIPT.json").read_text())["data"]
tree = {x["path"]:x for x in tree}
for name in ["problems.json","research_results.json"]:
    raw=(cache/name).read_bytes()
    expected=manifest["files"][name]
    check("raw_"+name,sha(raw)==expected["sha256"]==tree[name]["lfs"]["oid"]
          and len(raw)==expected["bytes"]==tree[name]["size"],
          "Independent immutable upstream-tree LFS SHA/size, manifest and cached bytes agree")
problems=json.loads((cache/"problems.json").read_text())
reports=json.loads((cache/"research_results.json").read_text())
row=[x for x in problems if x["id"]==30004186]
check("unique_numeric_and_code",len(row)==1 and sum(x["problem_number"]=="OWR-17128-002"
      for x in problems)==1,"Raw pinned row is unambiguous")
problem=row[0]
check("absent_prior_key", "OWR-17128-002" not in reports,"Absence in pinned prior corpus authenticated")
check("context_digest",ctx(problem,{})==CTX,"Actual context uses [problem,{}]")
reject("NULL_prior_context",ctx(problem,None)==CTX,"SQL text {} fallback is not null")
reject("source_only_context",sha(json.dumps(problem,sort_keys=True).encode())==CTX,
       "Source-record bytes/semantics alone do not bind prior context")
wrong=dict(problem,id=30004185)
reject("numeric_identity_mutant",ctx(wrong,{})==CTX,"Changing numeric identity changes context")
newprior={"status":"solved"}
reject("prior_injection_context",ctx(problem,newprior)==CTX,"Adding a prior theorem changes context")

changed=git("diff","--name-only",BASE,HEAD).decode().splitlines()
check("17_paths_16_numeric",len(changed)==17 and sum(x.startswith(TARGET) for x in changed)==16
      and "unsolved_math_prioritization/QUEUE.md" in changed,
      "Whole original diff has numeric package plus shared queue")
reject("numeric_only_scope_claim",all(x.startswith(TARGET) for x in changed),
       "Original PR prose and shared_queue_modified:false need correction")
check("candidate_frozen",sha(git("show",HEAD+":"+TARGET+"CANDIDATE.md"))==CAN_SHA,
      "Candidate checked directly from original Git head")
check("early_seal_unchanged",sha((HERE/"EARLY_INDEPENDENT_SEAL.md").read_bytes())==SEAL_SHA,
      "Source-first independence seal remains byte-for-byte unchanged")
readiness=json.loads(git("show",HEAD+":"+TARGET+"readiness.json"))
reject("original_readiness_already_authenticated",readiness.get("review_hash")==CTX,
       "Original readiness has source hash but no actual context digest")

result={"utc":datetime.now(timezone.utc).isoformat(),"status":"PASS",
        "sympy_version":s.__version__,"checks":checks,"mutants":mutants,
        "check_count":len(checks),"rejected_mutants":len(mutants),
        "script_sha256":sha(Path(__file__).read_bytes()),
        "limits":"Source/model/norm/quantifier/provenance controls only; no new proof attempt, no full-target resolution or historical model/priority certification."}
if "--no-write" not in sys.argv:
    (HERE/"INDEPENDENT_CONTROLS_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
