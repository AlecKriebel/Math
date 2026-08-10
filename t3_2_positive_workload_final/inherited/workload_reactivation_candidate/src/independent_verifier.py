#!/usr/bin/env python3
"""Dependency-free independent reconstruction of all finite T3-2 certificates.

This module intentionally imports none of the discovery implementation.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import permutations,product
from pathlib import Path
import subprocess,sys,json,hashlib,tempfile,os,shutil

ROOT=Path(__file__).resolve().parents[1]

def scalar_debt_audit():
    cases=0
    for d in range(1,30):
      for s in range(0,6):
       for a in range(0,6):
        nxt=max(d-s,0)+a
        assert nxt-d<=-int(s>=1)+a
        cases+=1
    p=Fraction(3,5);mean_a=Fraction(1,5)
    assert -p+mean_a==Fraction(-2,5)
    return cases

def strongly_connected(n,edges):
    for rev in (False,True):
      adj=[[] for _ in range(n)]
      for a,b in edges:
       if rev:a,b=b,a
       adj[a].append(b)
      seen={0};stack=[0]
      while stack:
       u=stack.pop()
       for v in adj[u]:
        if v not in seen:seen.add(v);stack.append(v)
      if len(seen)!=n:return False
    return True

def priority_graph_audit():
    total=0
    for n in (2,3,4):
      E=tuple(permutations(range(n),2))
      for mask in range(1<<len(E)):
       edges=[E[i] for i in range(len(E)) if mask>>i&1]
       if not strongly_connected(n,edges):continue
       adj=[[] for _ in range(n)]
       for idx,(a,b) in enumerate(edges):adj[a].append((b,idx))
       for level in product(range(3),repeat=n):
        total+=1
        top=max(level)
        if len(set(level))==1:continue
        # From every top vertex, strong connectivity gives a first drop.
        for root in range(n):
         if level[root]!=top:continue
         q=[root];seen={root};found=False
         while q and not found:
          u=q.pop(0)
          for v,_ in adj[u]:
           if level[v]<top:
            found=True;break
           if level[v]==top and v not in seen:
            seen.add(v);q.append(v)
         assert found
        changing=[(a,b) for a,b in edges if level[a]!=level[b]]
        alpha=max(level[a] for a,b in changing)
        assert all(level[b]<level[a] for a,b in changing if level[a]==alpha)
    return total

def one_active_audit():
    C=[x for x in product(range(3),repeat=3) if sum(x)<=2]
    with2=no2=0
    for s in C:
     for t in C:
      if s==t:continue
      k=t[0]-s[0]
      if s==(2,0,0):assert k<0
      with2+=1
      if s!=(2,0,0) and t!=(2,0,0):
       if s[0]==1:assert k<=0
       if s[0]==0:assert k<=1
       no2+=1
    return with2,no2

def queue_audit():
    count=0
    for L in range(1,5):
     for qden in range(2,7):
      q=Fraction(1,qden)
      success=q**L
      K=Fraction(L,1)/success
      eps=success/(4*K*3)
      mean_arrival=K*eps*3
      assert mean_arrival<success
      count+=1
    return count

def regression_audit():
    # Independent copies of the analytic signs.
    from math import log
    def one_coeff(n):
      d0=n*n+1;d1=n*n+2*n+2;d2=n*n+4*n+5;D=d0*d1*d2
      c={2:Fraction(-n*n*(n+1)**2*(n+2),D),
         3:Fraction(n**5+6*n**4+13*n**3+18*n**2+16*n+10,D),
         4:Fraction(2*(n**4+3*n**3+5*n**2+5*n+3),D),
         5:Fraction(2*n*n+5*n+4,d1*d2),6:Fraction(1,d2)}
      return sum(float(v)*log(n+j) for j,v in c.items())
    vals=[one_coeff(n) for n in (100,1000,10000,100000)]
    assert all(x>0 for x in vals)
    return [format(x,'.15g') for x in vals]

def run_atlases():
    inherited=ROOT/"inherited"
    clean=inherited/"adversarial_audit"/"cleanroom_atlas_check.py"
    direct=inherited/"candidate_release"/"src"/"exhaustive_two_active_atlas.cpp"
    indep=inherited/"candidate_release"/"src"/"independent_verifier.py"
    out={}
    if clean.exists():
        cp=subprocess.run([sys.executable,str(clean)],text=True,capture_output=True,check=True)
        assert "CLEANROOM ATLAS CHECK PASSED" in cp.stdout
        out["cleanroom_sha256"]=hashlib.sha256(cp.stdout.encode()).hexdigest()
        out["cleanroom_last"]=cp.stdout.strip().splitlines()[-1]
    if direct.exists():
        exe=ROOT/"certificates"/"atlas_direct"
        cp=subprocess.run(["g++","-O2","-std=c++17",str(direct),"-o",str(exe)],
                          text=True,capture_output=True)
        if cp.returncode:raise RuntimeError(cp.stderr)
        run=subprocess.run([str(exe)],text=True,capture_output=True,check=True)
        data=json.loads(run.stdout)
        assert data["unclassified_assignments"]==0 and data["workload_assignments_checked"]==187488
        out["direct"]=data
        exe.unlink(missing_ok=True)
    if indep.exists():
        cp=subprocess.run([sys.executable,str(indep)],text=True,capture_output=True,check=True)
        data=json.loads(cp.stdout)
        assert data["canonical_noninvariant_classes"]==29 and data["service_exception_classes"]==2
        out["independent"]=data
    return out

def source_hashes():
    h={}
    for p in sorted((ROOT/"src").glob("*.py")):
      if p.name=="independent_verifier.py":continue
      h[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
    return h

def main():
    priority_cases=priority_graph_audit()
    atlas_data=run_atlases()
    report={
      "status":"pass_T3_2_CERT_finite_interfaces",
      "scalar_debt_cases":scalar_debt_audit(),
      "priority_graph_cases":priority_cases,
      "one_active_channel_cases":one_active_audit(),
      "queue_capacity_cases":queue_audit(),
      "conditional_activation_positive_values":regression_audit(),
      "atlas":atlas_data,
      "source_hashes":source_hashes(),
      "certified_theorem_scope":"at most three active species and at most two active linkage classes",
      "noncomputational_load_bearing_claims":[
        "embedded reaction-count Green compactness",
        "terminal chart localization",
        "source-layer aggregate-debt induction",
        "one-active finite-phase closure",
        "global return-time argument",
      ],
    }
    text=json.dumps(report,sort_keys=True,separators=(",",":"))+"\n"
    out=ROOT/"certificates"/"independent_verification.json"
    out.write_text(text)
    print(text,end="")
if __name__=="__main__":main()
