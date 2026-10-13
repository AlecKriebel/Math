"""Prepare narrowly specified proof-expansion and reliable verifier repairs."""
from pathlib import Path
import datetime,hashlib,json
A=Path(__file__).resolve().parent;O=A/'original_submission/files/unsolved_math_prioritization/attempts/30003677';D=A/'repaired_candidate_v1'
def require(c,m):
 if not c:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 require(not D.exists(),'Existing repairs require reconciliation');D.mkdir()
 s=(O/'CANDIDATE.md').read_text()
 s=s.replace('Two approaches were considered. Independent review is pending. Priority is unestablished.','The stated hypotheses and conclusion are the target of verification. Historical priority is unestablished.')
 old='''The expected number of ringing events through any fixed `T` is therefore finite, being bounded by the integral of `λ₂` times this expression. Equivalently, the finite-mean continuous-time branching process is nonexplosive. Each event reveals a finite degree, so the total number of exposed half-edges through `T` is finite almost surely. The fixed-length path likewise has only finitely many incident half-edges almost surely.'''
 new='''For a noncircular justification, construct the genealogical tree with `d₀` initial active individuals and independent offspring `D*−1` and exponential lifetimes. Generation `r−1` has expected size `d₀ν^(r−1)`. A given individual in that generation rings by `T` only when its `r` ancestral lifetimes sum to at most `T`. Independence and the exponential joint-density simplex bound give

`E[number of rings by T] ≤ Σ_(r≥1) d₀ν^(r−1)(λ₂T)^r/r! < ∞`.

Tonelli's theorem applies to the nonnegative genealogical count, so infinitely many rings by a fixed time have probability zero. This constructs nonexplosion before using the expected-active-population identity above. Every event mark is a finite degree, so all incident half-edges at reached vertices form a finite set almost surely. The fixed-length path likewise has only finitely many incident half-edges almost surely.'''
 require(s.count(old)==1,'Nonexplosion repair anchor changed');s=s.replace(old,new)
 old='''Choose `M` so large that these two limiting explorations expose at most `M` half-edges with probability at least `1−ε`. Couple the finite-graph explorations until this cutoff, using the preceding finite-sampling argument and the same independent exponential clocks.'''
 new='''Choose `M` so large that these two limiting explorations expose at most `M` incident half-edges with probability at least `1−ε`. Couple the finite-graph explorations until this cutoff, stopping also at any repeated discovered vertex, frontier collision or intersection with the other exploration. Before such a collision, every exposed frontier edge is distinct and receives its independent type-specific exponential cost when its first infected endpoint starts traversal; this agrees with the fixed undirected edge-weight model on the revealed tree. No assertion of two independent endpoint clocks for the same cyclic-graph edge is needed. The preceding uniform-partner sampling and size-biased coupling make the stopped-exploration discrepancy tend to zero for fixed `M`.'''
 require(s.count(old)==1,'Clock repair anchor changed');s=s.replace(old,new)
 (D/'CANDIDATE.md').write_text(s)
 author=(O/'verify.py').read_text();require(author.count('    assert v,label')==1,'Author guard changed')
 author=author.replace('    assert v,label','    if not v: raise RuntimeError(label)')
 (D/'verify.py').write_text(author)
 independent=(O/'review/independent_checks.py').read_text();require(independent.count('    assert value,category')==1,'Independent guard changed')
 independent=independent.replace('    assert value,category','    if not value: raise RuntimeError(category)')
 old="(p/'independent_results.json').write_text(json.dumps(r,indent=2)+'\\n');print(json.dumps(r,indent=2))"
 require(independent.count(old)==1,'Independent output anchor changed');independent=independent.replace(old,'print(json.dumps(r,indent=2))')
 (D/'review/author_replay').mkdir(parents=True)
 (D/'review/author_replay/CANDIDATE.md').write_text(s)
 (D/'review/author_replay/verify.py').write_text(author)
 (D/'review/independent_checks.py').write_text(independent)
 for p in D.rglob('*.py'):require('assert ' not in p.read_text(),'Residual optimization-sensitive assertion')
 j={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'status':'PREPARED_NARROW_MATHEMATICAL_PROOF_EXPANSIONS_AND_EXPLICIT_FAILURE_CONTROLS','mathematical_claim_unchanged':True,'historical_originals_unchanged':True,'proof_repairs':['Noncircular genealogical expectation finite-time nonexplosion','Explicit incident-stub cutoff and frontier/cross-exploration collision stopping','Static undirected clocks justified only on collision-free local tree'],'code_repairs':['Assertions replaced with explicit RuntimeError','Independent checker prints receipt without writing beside a frozen source file'],'publication_or_priority_clearance':False,'files':{str(p.relative_to(D)):pin(p) for p in D.rglob('*') if p.is_file()}}
 (A/'MATHEMATICAL_REPAIR_PREPARATION.json').write_text(json.dumps(j,indent=2)+'\n')
 print(json.dumps({'status':j['status'],'files':len(j['files']),'mathematical_claim_unchanged':True}))
if __name__=='__main__':main()
