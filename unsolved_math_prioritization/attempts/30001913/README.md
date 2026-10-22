# Hodge–Tate facets and extremality: audited partial results

Problem **30001913 / OWR-11139-006**, rank **836**. **Unsolved, 5/5 approaches used.** AI-assisted and unrefereed. No complete proof, target counterexample, formal verification, or novelty claim.

The [author results](author/RESULTS.md), [five approaches](author/APPROACHES.md), [complete independent audit](audit/AUDIT.md), and [acceptance](audit/ACCEPTANCE.json) are preserved byte-for-byte. No correction was required. Historical audit-pending/publication-pending fields in the frozen inputs are unchanged; this publication metadata supplies the later disposition.

## Exact scope

The original target retains three-variable reflexive Newton polytope, zero origin coefficient, unit vertex coefficients, binomial edge coefficients, and componentwise genus-zero projective normalizations. Original extremality includes irreducibility and nonconstancy.

- The conditional bound 0 ≤ defect(V) ≤ b3(Z) assumes a nonconstant irreducible direct summand of R²g_*Q for the stated smooth projective compactification. Rational-center blowups supply a conditional criterion, not a global resolution theorem.
- The explicit family F_a satisfies the facet-genus condition exactly at a=0,±4. Its extremality uses credited prior examples and exact period identities, not a finite numerical certification.
- The local nodal calculation does not construct global algebraic branches or a global rational-center resolution.
- The abstract rank-two monodromy countermodel is not a Laurent-polynomial counterexample.
- The 2025 smooth-component/intersection hypotheses exclude the irreducible nodal faces considered here. Its H¹-vanishing definition omits original irreducibility; the definitions are not silently equated.

See the original sources and precise inspected locations in [public source verification](audit/SOURCE_VERIFICATION.json). Source documents, source text, dataset contents, and private coordination are excluded.

## Authenticated replay

Obtain the publication manifest SHA-256 and bootstrap SHA-256 from the draft PR verification metadata through a trusted channel. Use Python 3.11+ and an absolute package path. First authenticate bootstrap.py, then run it with **-I -S -B**. The externally pinned launcher is:

```python
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode): raise SystemExit('REJECT: require -I -S -B')
import hashlib, pathlib, stat
r=pathlib.Path(sys.argv[1]); p=r/'bootstrap.py'
for q in (r,*r.parents):
    if not stat.S_ISDIR(q.lstat().st_mode): raise SystemExit('REJECT: root ancestry')
s=p.lstat()
if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1: raise SystemExit('REJECT: bootstrap type')
b=p.read_bytes()
if hashlib.sha256(b).hexdigest()!=sys.argv[3]: raise SystemExit('REJECT: bootstrap anchor')
sys.argv=[str(p),str(r),sys.argv[2],*sys.argv[4:]]
exec(compile(b,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
```

Save those launcher lines outside the package and invoke python -I -S -B LAUNCHER ABSOLUTE_ROOT MANIFEST_SHA BOOTSTRAP_SHA. Repeat with -O. Append integrity for inventory-only validation, or test_publication.py for publication mutation controls. The default runs the 54 independent author replay/adversarial cases and the 13,617 independent exact mathematical controls, comparing full JSON outputs to the frozen results.

The bootstrap validates the complete tree before executing any bundled payload; rejects extra/missing paths, import shadows, caches, symlinks, nonregular files, and hardlinks; verifies both original archives and every member; and executes authenticated bytes in a temporary private snapshot. All child launches disable bytecode. Two historical audit tests per optimization mode intentionally omit one startup isolation flag to check rejection in a clean temporary directory. No malicious concurrent writer is modeled.

Remote byte readback, relocated normal/optimized replay, exact changed paths, two-cell queue diff, and exact-head CI observations are reported in the draft PR. Zero CI checks is not a CI pass.
