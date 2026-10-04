# Independent audit of Barth tangential limit verification

Date: 2026-10-04 UTC. Target: 2303019 / AMR-022-3019 / Hayman–Lingham Problem 3.19, observed queue rank 571.

## Verdict

**PASS. Accept `already_solved`, with one substantive verification turn recorded as `1/5`, credited to Hiroaki Aikawa (1990). No mathematical correction to the frozen author package is required.** This is verification of a published result, not a new resolution or priority claim.

The entire six-section proof was independently checked, including arbitrary continuous tangential geometry, every-angle coverage, bounded real boundary data, the infinite construction, and the strictly positive normalization. The analytic argument proves the quantified statement. Replaying the finite controls is a separate reproducibility check and is not the basis for the universal conclusion.

The exact frozen manifest SHA-256 is `d21cc63288ee27d315269164446384790c89bda4338c91d3e567e39193f9d822`. All eight listed payload hashes matched before review and again at completion. `PROOF.md` has SHA-256 `e86ae119289aff4c0214e50d7dd33077182141ebfead1d4ba8df2521b9869855`. No frozen file was edited. This audit made no remote writes.

## Exact statement and attribution

The imported target asks, for each fixed tangential path ending at 1, for one positive real harmonic function whose limit fails on every rotated copy of that path. Its logical order is

    for every admissible C, there exists v, for every theta.

It does not ask for a function independent of C. The construction uses C to choose the annuli and grids, then chooses a single boundary function before any rotation angle is fixed. This is the required quantifier order.

I independently inspected [Hayman–Lingham, printed page 66](https://arxiv.org/pdf/1809.07200v2#page=67), including the actual page pixels rendered anew from the locally hashed PDF. Problem 3.19 is followed immediately by an affirmative update crediting Aikawa. Bibliographic item [12], printed page 203, identifies the 1990 Proc. AMS article. Thus the imported report's claim that the question was still open in that edition is directly contradicted by its own cited source.

I also read the theorem on printed page 458 and the relevant lemmas and construction on pages 459–463 of [Aikawa's 1990 article, mirrored primary-paper text](https://scispace.com/pdf/harmonic-functions-having-no-tangential-limits-3exruh87fv.pdf). Its proof explicitly uses real signed boundary functions, radial grids covering every rotation, summable overwrites, and separated lower and upper limits. Attribution of that mechanism to Aikawa is correct. The reconstruction replaces the article's local-density estimate with an independently sufficient compact-circle estimate; it does not misrepresent this replacement as a new theorem.

[The author-hosted follow-up, Section 1, Theorem A](https://www.isc.chubu.ac.jp/aikawa/research/AikawaPapers/har.pdf), independently confirms the disk theorem and its implication for Barth's question. Its first page was rendered anew and visually inspected. It also gives the eventual-outside-every-cone interpretation of tangentiality. [Aikawa's official publication list](https://www.isc.chubu.ac.jp/aikawa/research/list.html), entries 48 and 50, confirms the two publication records. The 1991 author manuscript is correctly distinguished from the journal facsimile.

Source-access limits are preserved: the 1990 mirror supplied extracted text, but screenshot requests failed with a cache miss; the journal DOI endpoint did not yield the paper in this audit. I do not claim a successful local-byte or visual inspection of the 1990 article. OCR inequalities and constants were not trusted as proof: the frozen reconstruction's own estimates were checked below. The other primary sources and the self-contained reconstruction independently resolve the mathematical scope.

## Full mathematical audit

Line references below refer to the frozen `PROOF.md`.

### Path hypothesis and endpoint geometry

Lines 9–13 use the standard strong tangential condition: along the terminal path, `|1-z|/(1-|z|)` tends to infinity. This agrees with Aikawa's eventual exclusion from every Stolz region, explicitly stated before Lemma 5 in the 1990 text. It does not silently replace tangentiality with a merely unbounded ratio or a limsup condition.

Lines 29–33 are valid. Since the curve tends to 1, one may restrict and reparametrize a terminal piece into the sector with principal argument in `(-pi/4, pi/4)` and away from 0. Thus both the continuous argument and radial coordinate are well-defined. The triangle inequality gives

    |1-r exp(i alpha)| <= (1-r) + r |1-exp(i alpha)|
                        <= (1-r) + |alpha|.

Consequently the assumed diverging quotient forces `|alpha|/(1-r)` to diverge. The argument does not require a tangent vector, finite length, differentiability, or a radial graph.

The last-exit construction in lines 45–53 survives nonmonotone radius and self-intersections. For `a` above the initial radius, the level `r=a` is nonempty by continuity and the limit `r(t)->1`. It is closed and lies in a compact parameter interval, because eventually `r(t)>a`. It therefore has a last point `t_a`. After that point the radius is strictly larger than `a`: a later point below `a`, followed by convergence to 1, would force another crossing. For every fixed `T<1`, compactness gives `max_[0,T] r<1`; hence `a->1` forces `t_a->1`.

It follows that `|alpha(t_a)|/(1-a)->infinity`, so `alpha(t_a)` is nonzero for all sufficiently large `a`. Since `alpha(t)->0`, a later `t'` with `|alpha(t')|<|alpha(t_a)|/2` exists. The maximum radius on `[t_a,t']` is strictly below 1, so `b` can be chosen strictly above that maximum and below 1. A first subsequent crossing `t_b` of `b` exists, occurs after `t'`, and gives `a<=r(t)<=b` on `[t_a,t_b]`.

The continuous argument image of this compact parameter interval is a closed interval, regardless of injectivity of the curve. The reverse triangle inequality gives its length at least

    |alpha(t_a)-alpha(t')| >= |alpha(t_a)|-|alpha(t')|
                            > |alpha(t_a)|/2.

Therefore `ell/(1-a)` can exceed any prescribed number while `a` exceeds any previously fixed radius. The entire subpath lies in a terminal portion; hence its angular diameter tends to zero if required. The later choices of `b` cannot invalidate this terminal containment. **No geometric gap found.**

### Every rotation meets the same grid

Lines 57–65 use `N=ceil(2 pi/ell)` and spacing `Delta=2 pi/N<=ell`. For a lift `[L,L+ell]` of the rotated angular interval, take `q=ceil(L/Delta)`. Then

    L <= q Delta < L+Delta <= L+ell,

with the left endpoint permitted. Modulo `N`, this is one of the designated grid angles. The continuous angular projection supplies a point of the rotated subpath with that angle, and its radius lies in the same closed annulus. Closed endpoints make the equality case `Delta=ell` safe. Modulo reduction handles wraparound, including angles 0 and `2 pi`.

This is an exact argument for every angle at each stage. There is no dense-set reduction, countable union of exceptional-angle sets, or appeal to an almost-everywhere boundary theorem.

Lines 67–71 are also valid. The arc radius is `m d<1<pi`, so each circle arc has length `2m d`. Finite subadditivity, including overlaps and wraparound, gives

    |E| <= 2m d N <= 4 pi m (d/ell) + 2m d.

The same construction makes both terms arbitrarily small, with `a` as far out as required. It is not necessary to make the arcs disjoint. **No coverage or small-support gap found.**

### Poisson bounds with all constants checked

Lines 75–80 define the conventional Poisson integral on the angle circle; the use of `f(eta+t)` is consistent because the kernel is even. For bounded real measurable data it is harmonic, real, and bounded by the data's supremum norm. The positive kernel has normalized total mass 1. These facts follow directly from the real part of the analytic kernel `(exp(i t)+z)/(exp(i t)-z)` and its geometric-series expansion on compact subdisks.

For lines 82–97, concavity of sine gives `sin(|t|/2)>=|t|/pi` on `|t|<=pi`. Thus

    1-cos t >= 2 t^2/pi^2,
    1-r^2 <= 2(1-r) <= 2d,
    (1-r)^2+2r(1-cos t) >= 2 t^2/pi^2

when `r>=1/2`. Division yields exactly the asserted `P_r(t)<=pi^2 d/t^2`. It holds also at `r=a`; the excluded `t=0` is outside the integration domain being estimated. Since `md<pi`, normalized mass outside the sign arc is at most

    pi d integral_(md)^pi t^(-2) dt = pi/m-d < pi/m < 1/4.

On the arc, `s f=1`; outside, `s f>=-1`. Therefore `s P[f]>=1-2 mass(outside)>1/2`. The sign conclusion is uniform for every radius between `a` and 1 and for both signs.

For lines 99–106, the denominator is at least `(1-r)^2`; hence

    P_r(t) <= (1+r)/(1-r) <= (1+R)/(1-R)

on `r<=R<1`. Integrating over `E` gives precisely `K(R)|E|`, with Lebesgue angular length unnormalized and `1/(2 pi)` included in `K`. There is no missing `2 pi`, factor 2, or reversal of the radial inequality. **Both estimates and their strict margins pass.**

### Recursive choices and infinite boundary stabilization

Lines 112–122 have a valid induction order. At stage `j`, `b_(j-1)<1` is already fixed, so `K(b_(j-1))` is finite. Set, for example,

    delta_j=min(2^(-j), epsilon_j/K(b_(j-1))).

The previous geometric argument permits a new `a_j` above the previous radius, above `1-2^(-j)`, and above `15/16`, with `|E_j|<=delta_j`. Then choose the associated `b_j`. Although later `K(b_j)` may be extremely large, that affects only a later stage where supports can again be chosen arbitrarily small. No uniform bound on all `K(b_j)` is assumed.

The overwriting rule in lines 124–130 preserves real values in `{-1,0,1}`. It gives the displayed support bound even when old and new signs are opposite. With `sum |E_j|<infinity`,

    measure(limsup E_j) <= sum_(j>=J) |E_j| -> 0.

This is the first Borel–Cantelli estimate proved by subadditivity; independence of the sets is neither used nor needed. Away from that null set, only finitely many overwrites occur, so eventual values define measurable bounded `f` after assigning any value on the exceptional null set. Thus `f_j->f` almost everywhere.

The compact-uniform conclusion in line 132 is justified, not just pointwise dominated convergence. More explicitly,

    sup_(|z|<=R) |P[f_j](z)-P[f](z)|
        <= K(R) integral_(-pi)^pi |f_j-f| dt -> 0.

Dominated convergence applies to this last integral because `|f_j-f|<=2` on the finite circle. Harmonicity of `P[f]` is available directly from the Poisson representation, so no unmentioned harmonic-limit theorem is needed. **The infinite boundary construction passes.**

### Later overwrites preserve earlier interior signs

Lines 134–147 use the correct nested-disk direction: for `k>j`, `b_j<=b_(k-1)`. Hence the bound imposed on the `k`th overwrite is valid at every point of the entire `j`th grid, including its outer endpoint. The factor 2 is retained. The exact infinite tail is

    2 sum_(k=j+1)^infinity 2^(-k-4) = 2^(-j-3) <= 1/16

for `j>=1`. Compact convergence justifies passage from the finite telescope to `h-h_j`. Since `s_j h_j>1/2` on `M_j`, the final `s_j h` remains strictly greater than `7/16`, and therefore greater than `1/4`. It does not matter that later boundary data overwrite parts of earlier sign arcs; their interior effect is the quantity being controlled. **No tail-index or sign-preservation gap found.**

### Oscillation and strict positivity

For an arbitrary fixed angle, every grid supplies a point of the corresponding rotated subpath. Its radius is at least `a_j>1-2^(-j)`, and thus tends to 1. Both parity subsequences are infinite. On the even subsequence the final real harmonic function exceeds `1/4`; on the odd subsequence it is less than `-1/4`. This proves the claimed separated limsup and liminf for each angle. The null set involved in boundary stabilization does not become an exceptional set of angles: it only selects a representative of the boundary integrand, while the estimates for the interior Poisson integral hold everywhere.

Finally `v=(h+2)/4` is real harmonic and lies in `[1/4,3/4]`, in particular strictly between 0 and 1. The affine map sends `-1/4` to `7/16` and `1/4` to `9/16`, preserving a gap of `1/8`. Boundedness excludes an infinite extended-real limit, while the gap excludes a finite limit. The claimed conclusion is weaker than the actual sign margins, so there is no strict-versus-nonstrict limit error. **The exact target is proved.**

## Imported dependencies and deliberate scope limits

The reconstruction depends only on elementary real continuity and compactness, the intermediate value property, sine concavity and elementary circle constants, geometric series, countable subadditivity of Lebesgue measure, dominated convergence, and the displayed Poisson-kernel facts. Its analytic integral facts are justified by bounded kernels and their derivatives on compact disks. It does not invoke an unverified modern theorem or the original article's more technical density estimate.

Neither the analytic-function analogue nor the almost-everywhere Littlewood theorem is used as a substitute for real harmonic oscillation. A complex function can fail to converge while its real part converges; the proof avoids that issue by constructing real signed data directly.

Continuity is essential to the grid argument. A disconnected sequential set need not project onto an interval even when its angular diameter is large. Mere nontangential paths do not provide the required ratio. A function working simultaneously for every possible initial path is not established or claimed. [The later primary preprint, arXiv:2511.12679v2](https://arxiv.org/html/2511.12679v2), confirms the distinction between earlier curvilinear results and later sequential-region work; none of its results is imported into this proof.

## Reproducibility and limitations of the finite controls

I read `controls.py`, executed it with Python's standard library, and compared its output byte-for-byte with frozen `validation.json`. The output is identical: **12 families, 2,956,209 passing assertions**, replay SHA-256 `d7da91119a28cc522d70db59500598741a41642ea97914a209ac76df8a6aaa98`.

The grid controls test finitely many rational circle intervals. The overwrite controls exhaust all four-stage subset masks on four atoms. Kernel controls test selected rational radii and cosine values. The tail controls compare finite sums with a supplied exact-tail expression. They do not mechanically prove every interval, every cosine value, an infinite tail identity, arbitrary curve selection, or every angle. Those facts were checked analytically above. The frozen package correctly makes this distinction.

`AUDIT_CHECKS.json` records the replay and before/after integrity checks. `audit_verify.py` reproduces the integrity and replay checks without changing the frozen package. Its success is a reproducibility receipt, not a formal proof certificate.

The two locally available source PDFs were independently rehashed:

- Hayman–Lingham: `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`.
- Aikawa author manuscript: `11b25713f26a35bf49a0dc9ef18ed6831970fdc203b3efd8af9c3267812b11ea`.

These match the author's provenance report. Source PDFs, article text, and page images are not included in the audit deliverables and must not be publicly redistributed with them.

The supplied exact catalogue record and complete prior report were read. The record's statement agrees with the primary source and the prior report contains no candidate proof. The whole 69 MB upstream corpus and 80 MB research-report corpus were not downloaded or independently rehashed in this audit; their whole-file hashes remain the author's provenance assertions. Live repository search absence, queue freshness, and remote publication are not certified by this mathematical audit. Those operational checks should be revalidated by the publishing task before any queue mutation. None is an imported mathematical dependency.

## Corrections and publication recommendation

Required mathematical corrections: **none**.

Optional explanatory additions, already supplied in this audit, are the explicit lifted-interval ceiling argument for the grid and the explicit `K(R)` times `L1` bound for compact-uniform convergence. They clarify steps already valid in the frozen proof and are not repairs.

Keep the frozen record as the author's pre-audit package, including its historically correct `independent_audit: pending` field. Append this independent audit rather than rewriting that history. The publishing task may record the accepted result in a separate receipt. Retain `already_solved` and the Aikawa attribution; do not label the campaign as the solver, or count the independent review as a fresh proof-attempt turn. Acceptance of `1/5` is consistent with the single substantive reconstruction documented by the author; this review did not conduct new search to fill a missing argument.

**Final recommendation: accept the frozen proof unchanged, append this audit, and publish only original verification materials and public source links under the separately authorized repository workflow.**
