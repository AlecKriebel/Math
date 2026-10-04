# Independent adversarial audit: Function Theory 3.32

Audit date: 2026-10-04 UTC. Target: rank 573, numeric ID 2303032,
AMR-022-3032. Frozen author manifest SHA-256:
`5b6f7dba27b77fec14d52c73e409ff25c18bcf08ca8486be509adb827c69d740`.

## Verdict

**Accept the historical classification `already_solved`, with `1/5` substantive
turns, under the dossier's explicit scope restriction.** The primary result
answers the named problem in the historical literature. This is not a new
result and not a certificate of a fully reconstructed sharp integrability
classification.

The reconstructed sufficient range passes this audit, conditional on the
explicitly identified classical potential-theoretic inputs. The cone
counterexamples establish sharpness and endpoint failure for `1<a<=2`, and
the smooth limiting endpoint has an independent bounded-ball example below.
For `a>2`, neither the optimality construction at the smaller bound nor the
endpoint classification has been independently established by this audit.
The frozen files disclose that limitation adequately. **No mandatory
mathematical correction to those files was found.**

Do not convert this verdict into `verified_solved`, a new-solution claim, a
complete-independent-proof claim, or an assertion that the exact admissible
set is proved to be `0<p<p_*` in every regime. No remote writes were made.

## 1. Identity, source statements, and quantifiers

I read the full pinned catalogue record and the corresponding source page.
Problem 3.32 concerns all positive superharmonic functions on a bounded
Lipschitz domain, with an interior-cone half-angle certificate. It has no
bounded boundary-data hypothesis. Its 2018 update points to Aikawa.
The public note properly treats the requested exponent as a guarantee for
a geometric class, not the exact critical exponent of every individual
member of that class.

I independently reopened the [1994 author manuscript](https://www.isc.chubu.ac.jp/aikawa/research/AikawaPapers/int.pdf)
and [2019 author manuscript](https://www.isc.chubu.ac.jp/aikawa/research/AikawaPapers/iccapta.pdf)
through the web tool. I also inspected fresh local renderings of the
hash-verified PDFs: 1994 manuscript p.8, 2019 manuscript p.5, and
Hayman--Lingham PDF page 71, printed p.70. The source images were not added
to the audit or public package. The web screenshot route returned a cache
miss; local PDF rendering provided the visual crosscheck.

1994 Section 4 explicitly identifies Problems 3.32 and 3.34. Corollary 6(i)
and 2019 Theorem 1.7 both give the strict sufficient range

    0 < p < min{ n/(n+a-2), 1/(a-1) }.

Their parameter is the positive cone harmonic homogeneity degree, not an
angle measured in radians. The 1994 manuscript's subsequent piecewise
display has the wrong sign in its `a>2` branch, while the immediately
preceding corollary and the 2019 theorem agree. The frozen correction is
necessary and correct. The local scaling correction to 1994 Lemma 3 is
also correct: ball `L^p` versus `L^1` scales as `r^(n/p-n)`.

The [2018 collection](https://arxiv.org/abs/1809.07200v2) uses the same letter
in the question and update for two different quantities. This makes a
literal substitution unreliable; the dossier correctly resolves it through
the primary definitions. In two dimensions `a=pi/(2 theta)`; in four,
`a=pi/theta-1`. The spherical eigenvalue definition in the public proof
makes the convention unambiguous in all dimensions.

The primary corollaries are stated for `k`-Lipschitz domains, with
`theta=arctan(1/k)`. A general uniform interior-cone certificate need not
produce charts with that exact Lipschitz constant. The public argument
correctly does not assert this converse. The 1998 Lemma 15(ii) is useful
corroboration of the cone Green estimate, but its written definition places
uniform-radius cones at interior points. For the public note's boundary-cone
reading, its separate cone-axis comparison plus Lipschitz Harnack-chain
argument supplies the needed bridge. A pointwise, nonuniform cone assumption
on a general non-Lipschitz domain is outside this audit. Problem 3.34 must
not be relabelled on the strength of this dossier alone.

## 2. Independent analytic examination

### Finite pole value, coarea, and singularities

A nontrivial positive superharmonic function has a finite value somewhere
and is locally integrable. Choosing that point as the Green pole avoids an
infinite right-hand side. All gradient estimates are confined to a boundary
layer separated from the pole. For regular levels, `G_D-t` is the Green
function of `{G_D>t}` with that pole, and its outward derivative has sign
`-|grad G_D|`. Harmonic-measure comparison therefore gives the inequality
in Section 4, with the stated normalizing constant.

The coarea application can be exhausted away from both the pole and zero
level and then extended by monotone convergence. It requires no prior
integrability of the target weighted expression. Truncating the level
parameter above at `T` avoids applying a positive power weight through the
Green singularity. This is a real improvement in explicitness over a
literal untruncated reading of a shortened source exposition.

### Weak Harnack and the gradient set

The positive-set estimate has the correct units. A Green kernel in an
enlarged ball has a uniform lower bound of order `r^(2-n)` on the inner
ball, and its local `L^s` norm has order `r^(2-n+n/s)` when
`s<n/(n-2)`. In dimension two the scaled logarithmic kernel has every finite
positive moment. Balayage or a local Riesz decomposition plus Harnack
justifies the representation step. Exceptional polar values do not change
these volume integrals.

The reconstruction does not assume a pointwise lower bound on the Green
gradient. From the boundary Hölder estimate, a point on the inward segment
can be chosen with at most half the Green value at its other end. The
fundamental theorem of calculus yields one point of sufficiently large
gradient. An interior Hessian bound, on a slightly larger ball still
strictly inside the domain, turns that point into a ball of fixed relative
radius. This proves the needed positive-volume set. The nested constants
can be chosen in the order used in the note; none depends on the specific
boundary-layer point. A bounded-overlap covering then legitimately sums
the estimates. Critical points of the Green function do not invalidate
this step.

### Weighted estimate and exponent conversion

Combining the positive-set estimate with coarea gives the weighted `L^1`
statement for every `epsilon>0`. The Green lower bound has the correct
direction: raising it to the positive exponent `1+epsilon/a` produces the
factor `delta^(a+epsilon-2)`. Compact interior regions are handled by local
integrability.

For `a<2`, the chosen Whitney weight is exactly
`-n(1-1/p)`. Its epsilon is positive precisely in the asserted strict range.
All local exponents lie strictly below the local Green singularity
threshold. The use of Minkowski is restricted to `p>=1`; `p<1` follows
from `L^1` and finite volume.

For `a>=2`, Hölder applies with conjugate exponents `1/p` and `1/(1-p)`.
The boundary-layer exponent is less than one exactly when
`(a-1+epsilon)p<1`. Lipschitz graph charts give a boundary layer of volume
`O(t)`, so this strict inequality suffices. At `a=2`, the proof includes
all `p<1` and does not sneak in `p=1`. At `p=1/(a-1)` and `a>2`, the
Hölder criterion fails for every positive epsilon; this proof cannot
classify that endpoint.

The polynomial identity

    n(a-1) - (n+a-2) = (n-1)(a-2)

correctly places the regime switch at `a=2`. The two branches are positive
for the permitted parameters, and both equal one there.

## 3. Cone geometry and endpoints

The radial characteristic roots are `a` and `-(a+n-2)`. The positive
angular eigenfunction is bounded on its closed spherical cap. Consequently
the negative-root harmonic function has local radial integral

    constant * integral_0^r0 r^(n-1-p(a+n-2)) dr.

It converges strictly below `n/(n+a-2)` and diverges logarithmically at
equality. This is an actual harmonic counterexample, hence also a
superharmonic counterexample, without an appeal to discretized controls.

The proposed bounded realization is valid. For the convex hull of `0` and
`B(t e_n,t sin(theta))`, the tangent circle has axial coordinate
`t cos(theta)^2` and transverse radius `t sin(theta) cos(theta)`. Thus the
conical side has exactly the intended half-angle and meets the spherical
cap tangentially. The boundary is Lipschitz at the vertex and `C^1`
elsewhere. Near the vertex a fixed short piece of a translated cone stays
in the conical portion; on the remaining compact `C^1` boundary, a uniform
cone radius is available for any fixed angle below `pi/2`. The model
therefore belongs to the intended class. There is no unexamined sharp
corner where a planar cap meets the side.

When `a<=2`, the cone obstruction equals the sufficient threshold. At
`a=2`, the quadratic `(n-1)x_n^2-|x'|^2` is harmonic, and its Kelvin
transform has degree `-n`; this verifies the exact `L^1` transition and
`cos(theta)=1/sqrt(n)`.

For precision, `a=1` is a smooth limiting case, since the initial domain
class takes `theta<pi/2`. A bounded smooth endpoint counterexample is the
unit-ball Poisson kernel with a boundary pole `e_n`:

    u(x) = (1-|x|^2)/|x-e_n|^n.

Within a fixed inward angular sector near that pole, its numerator is
comparable to `|x-e_n|`, so it is comparable to `r^(1-n)`. The volume
integral diverges at `p=n/(n-1)`. This supplies an explicit bounded-domain
check of the smooth endpoint, without claiming that every bounded `C^1`
domain has uniform cones of half-angle exactly `pi/2`.

For `a>2`, the single cone remains integrable at the smaller endpoint
`p=1/(a-1)`. Indeed its radial power is greater than `-1` there. It cannot
establish the advertised narrow-angle optimality. A named theorem's strict
sufficiency and a prose statement that a bound is sharp do not by themselves
specify whether equality belongs to the guarantee. They also do not assert
failure in every fixed domain. The original construction and endpoint
analysis remain unverified here.

## 4. Historical disposition and turn budget

The 1994 source explicitly associates its result with the target and
asserts sharpness. The later 1998 and 2000 introductions also describe the
prior Lipschitz exponent as sharp, and the 2019 exposition presents the
problem as settled. This is adequate published-theorem provenance for
removing the target from a queue of novel open problems. It contradicts
the imported desk report's unsupported statement that the 2018 source
left the sharp threshold open.

It is not adequate for describing the present artifact as a complete
independent proof of universal optimality, and the frozen status does not
do that. Its `not_independently_reconstructed` fields should remain visible
in any release summary. If a downstream policy insists on complete
independent reconstruction even for a historical status label, approval is
conditional on that separate policy decision; no missing construction is
silently waived by this audit.

The log records one substantive theorem-verification response. The source
checks, replay, and adversarial checks here do not conceal a new search for
the missing construction. `1/5` is consistent with the stated response-based
budget. This audit does not add a novel proof-attempt turn.

## 5. Reproduction and integrity

- Frozen author manifest hash matches the assigned value.
- All 9 files covered by the public manifest match; the tenth public file
  is that non-self-referential manifest.
- `verify.py` reproduces `CHECKS.json` exactly: **125,813 assertions**.
- The source-dir replay passes **125,818 assertions**, including all five
  PDF byte digests. This verifies the supplied source bytes, not a fresh
  independent download of every PDF.
- Both public Python files compile without writing into the frozen folder.
- `INDEPENDENT_CONTROLS.py` checks seven symbolic polynomial identities and
  selected exact rational negative controls independently of the author's
  grid. Its result and limitations are in `INDEPENDENT_CHECKS.json`.
- None of these computations certifies Green estimates, cone eigenvalues,
  boundary regularity, or `a>2` optimality. The analytic conclusions above
  come from the mathematical audit, not assertion counts.
- No helpers were used, no source PDF or screenshot was republished, and
  no remote file, branch, or queue was changed.

The audit's own manifest binds this report and its replay artifacts.
