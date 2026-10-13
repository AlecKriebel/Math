# Independent adversarial audit: exponential parameter-hair interiors

Problem 5300062 / AMR-052-0062, rank 796. Audit date: 2026-10-05.

## Verdict

**REPAIR_REQUIRED_V1.** The frozen report has one missing cited-hypothesis check,
with a dependent low-potential adjustment. The three exact replacements in
CORRECTIONS.md and REPORT_MANDATORY.patch repair it. With those changes, the
C-infinity theorem for standard parameter-ray interiors survives this audit.
A separately frozen v2 and bounded-delta acceptance remain necessary. This audit
does not silently edit the original report or upgrade the original freeze to an
unqualified pass.

The main target remains **UNSOLVED, 5/5 approaches**. The accepted mathematical
scope after repair is a regular C-infinity standard potential parametrization
of every parameter-ray interior at every exponentially bounded address, including
unbounded addresses. No general geometric real-analyticity, endpoint regularity,
landing theorem, or novelty claim is accepted. This is an independent AI audit,
not human refereeing or machine-checked formal mathematics.

## 1. The actual repair

The invocation of [FS, Lemma 4.4] requires t>t_s^*+2 log(K+3). The frozen proof
only assumes a>max{x_0,K+6}, where t_s^*<=x_0. Those conditions need not imply
the cited sufficient threshold. A numerical witness is K=1, x_0=100 and
a=100.01. It demonstrates a missing implication, not a counterexample to the
limiting curve or the claimed theorem.

Replace the tail condition by a>max{x_0+2 log(K+3),K+6}, explain the bound
t_s^*<=x_0, and impose the corresponding extra gap after shifting the address.
This is a genuine mathematical hypothesis repair. The remaining estimates become
no weaker. For the shifted construction, F^N(inf J)-F^N(u) tends to infinity,
so the strengthened condition is available at every t_*>t_s. No endpoint limit
is thereby admitted.

## 2. Independent reconstruction of the analytic argument

### 2.1 Address growth and the interior margin

For any t_s<u, choose v strictly between them. The limsup definition supplies
|s_(m+1)|<=F^m(v) for every sufficiently large m. Once the forward iterates of
v and u are at least 2, their difference grows by at least a factor 2 per step.
The ratio F^m(v)/F^m(u) therefore tends to zero. This absorbs 2 pi and every
fixed multiplicative constant. Hence, for all sufficiently large N and every
j>=0,

    2 pi |s_(N+j+1)| <= F^(N+j)(u).

The quantifier is all j, not merely finitely many tested entries. At the shifted
address, x_0=F^N(u) works. The strict gap u<inf J is the essential resource.
This argument includes unbounded exponentially bounded addresses and explains
why no endpoint estimate follows.

### 2.2 Real baselines and log branches

For a>K+6, descending through the finite pullbacks gives the real-part bound
F^j(t)-K-1>5 at every intermediate level. In the descent,

    F^(j+1)(t)-K-1 = exp(F^j(t))-(K+2),

and (K+2) exp(-F^j(t))<1-exp(-1) is sufficient for the stated logarithmic
inequality. Complex parameter values with |kappa|<=K and arbitrary integer
address offsets preserve this estimate. The offsets change imaginary parts,
not the lower real-part bound.

The shrinking radius controls the penultimate forward iterate v=F^(n-1)(z),
not U=F^n(z). Nonnegative coefficients give

    |v-F^(n-1)(t)| <= r_n (F^(n-1))'(b+eta) <= 1/16.

Consequently Re U and |U| are each at least exp(F^(n-1)(t))/2. This follows,
for example, from exp(-1/16) cos(1/16)-exp(-7)>1/2. Thus both correction
logarithms are holomorphic on the stated disks.

The correct germ is q(v)=v+Log(1-exp(-v)); it need not equal a naive repeated
principal-log expression at every nonreal point. The expressions A and B in
the report agree with the original approximants at real t and analytically
continue those germs. For real t, U is positive and |d/U|<=1/16 guarantees
that Log(U+d)=Log U+Log(1+d/U) uses the same branch. It would be incorrect to
require Im U itself to remain small or to replace the continued germ by a
fresh principal log of exp(U)-1.

The independent program deliberately exhibits 12 cases where that naive
principal-log replacement changes the value by nonzero multiples of 2 pi i,
while the continued two-log identity remains accurate. These are diagnostic
finite controls, not the justification of the holomorphic-germ argument.

### 2.3 Uniform difference estimates

On each disk, |q'|<=2 yields |A(z,kappa)-A(t,kappa)|<=1/8. The address bound
and the real-part estimate give |d/U|<=1/16 eventually, uniformly in t and
|kappa|<=K; hence |B-A|<=1/8. Relative to the real-t baseline of g_n, both
values stay within 1/4. Each remaining logarithm has derivative less than
1/4 on every connecting segment, since those segments lie in Re w>4.
Induction therefore keeps all continued pullbacks on their valid branches.
No bounded-address assumption enters this induction.

Writing X=F^(n-1)(x_0) and Y=F^(n-1)(a), the estimate can be made explicit:

    |d| <= K+exp(X),
    |B-A| <= 4(K+1) exp(X-Y).

The outer logarithms do not increase the difference. Thus the report's
constant C can indeed depend only on K for the displayed estimate. Dependence
of the eventual starting index on the fixed address and interval is harmless.

### 2.4 Every fixed derivative order is summable

Let c=b+eta. The chain rule gives

    log D_n = sum_(j=0)^(n-2) F^j(c)
            <= (n-1)F^(n-2)(c).

Since c<F(a), comparison of two iterates with starting points c and F(a)
yields (n-1)F^(n-2)(c)/F^(n-1)(a)->0. Likewise
F^(n-1)(x_0)/F^(n-1)(a)->0. For every fixed k, the logarithm of the Cauchy
upper bound is therefore at most -F^(n-1)(a)/2 eventually. Its sum converges,
since F^(n-1)(a)>=2^(n-1)a.

This establishes locally uniform convergence of each potential derivative,
uniformly for parameters in the fixed compact disk. The thresholds may depend
on k. Holomorphy in kappa and a second Cauchy estimate on a strictly smaller
parameter disk give uniform convergence of every mixed parameter/potential
derivative. Choosing K with margin around the parameter of interest avoids
using Cauchy's formula on a boundary point without an open neighborhood.
The standard uniform-derivative convergence theorem now gives joint real
C-infinity dependence. Separate fixed-parameter smoothness alone would not
suffice; the proof supplies the needed joint estimate.

There is no common positive complex-potential radius and no uniform-in-order
factorial estimate. The argument consequently supplies no real analyticity.

### 2.5 Low-potential pullback and parameter transversality

After the mandatory strengthened choice of N, the shifted ray is in the
proven smooth region. The derivative of the finite iterate E_kappa^N in its
phase variable is a finite product of nonzero exponentials. The holomorphic
inverse-function theorem with kappa as an additional variable supplies a
local inverse chart. Composition with the shifted smooth family and F^N(t)
is jointly smooth. Local continuity and the domain statement in [FS, Lemma
3.5] identify this branch with the original dynamic ray. The proof does not
use global principal branches or attempt to invert through zero.

At the singular-value equation Phi(t,kappa)=0, [FS, Theorem 3.7] explicitly
asserts a simple root in kappa. Thus the real parameter Jacobian has determinant
|Phi_kappa|^2>0. The smooth implicit-function theorem applies, and the
nonvanishing potential derivative in [FS, Proposition 4.6] implies
G_s'=-Phi_t/Phi_kappa !=0. No inference from mere injectivity to a nonzero
derivative is being made. Finally exp(kappa) is a local biholomorphism;
it preserves the local regular smooth curve statement, without globally
identifying address labels or injectivity on the parameter cylinder.

## 3. Boundaries and countercontrols

The smooth flat-graph example correctly blocks the proposed shortcut from
holomorphic parameter dependence plus simple roots to analytic root curves.
It is a logical example, not an exponential-family counterexample.

For real lambda>1/e, the minimum of lambda exp(x)-x is 1+log(lambda)>0.
Every real orbit increases without a finite limit, since a finite limit would
be a fixed point. The singular orbit therefore escapes with zero itinerary.
The constant address is slow, so the ray/endpoint classification puts these
parameters on the ray interior. This is a real-analytic geometric parameter
arc, without establishing analyticity of its prescribed potential coordinate.
At lambda=1/e the singular orbit tends to the parabolic fixed point 1 instead.

The September 2026 Cui-Huang-Wang manuscript concerns dynamic hairs for one
fixed real map with 0<lambda<1/e. Its attracting-basin density argument is
inside that dynamical plane. Neither phase translation nor lambda=exp(kappa)
transfers it to parameter hairs. It therefore does not settle this selected
problem. The original report correctly maintains that distinction.

## 4. Source and identity audit

The 1992 source page was independently rendered from the hashed PDF. Its
superscript is infinity, and its question is about parameter-plane hairs;
the termination question appears alongside it. The displayed problem was
visually inspected rather than trusting the text extractor's superscript.

The arXiv Foerster-Schleicher text was checked at Definitions 2.3-2.5,
Theorem 2.6, Lemma 3.5, Theorem 3.7 and its remark, Lemma 4.4, and Proposition
4.6. The thesis was checked at Corollary 3.5.2 and its following remark.
These sources establish C1 parameter-ray regularity and suggest, without
providing there a completed all-order parameter proof, the C-infinity extension.
The final 2009 publisher metadata was checked, but its full journal text was
not accessible through the attempted official PDF route. No stronger statement
about that uninspected final text is made. Viana's dynamic-plane theorem was
scope-checked on the first two scanned pages; it is not being credited as a
parameter theorem. Public links and precise limits are in SOURCE_AUDIT.json.

The complete cached problem and research corpora, plus the complete catalog,
were independently hashed. Both dataset files match the freshly fetched pinned
repository manifest; the catalog's Git blob matches freshly fetched directory
metadata. The selected problem is unique and its 126-byte statement hash
matches. Unlike the author freeze, this audit also recomputes the review hash
using the repository's exact serialization of the selected problem and research
report; it matches b7b442519b7489ed54933de971ba4f04b049ea50aedd2cf1e246a7d566e9b392.
The selected desk-review shard was freshly retrieved and separately authenticated.
Neither that review nor the dataset's short literature summary is a prior proof.

For prior-attempt coverage, all 1,955 Git tree nodes in the cached untruncated
14,882-entry recursive attempts listing were rebuilt and matched their hashes,
including the root freshly bound through pinned directory metadata. No path
matched this ID. Fresh exact code, ID/title PR and branch searches also found
no match. This is a bounded negative check, not proof that deleted, unindexed,
private or unpublished attempts do not exist.

## 5. Computational and packaging audit

Independent code rebuilt 480 exact rational-jet identities using finite power
sums rather than the author's derivative recurrences. Another 297 numerical
controls were rebuilt at 80 decimal digits using independent differentiation
and closed derivative products, alongside the 12 branch traps and the tail
hypothesis countercontrol. All passed. These are non-interval-certified finite
controls; they do not prove any universal analytic assertion.

The original retained controls replayed exactly. Strict manifest inventory,
relocation, content edits, missing/extra files, empty extra directories, symlinks,
coherent manifest rewriting with the original external anchor, and optimized
Python modes are tested separately. See results/integrity_controls.json.

The safe archive includes only authored analysis, the mandatory textual patch,
code, metadata and retained results. It excludes PDFs, page images, extracted
source text, raw corpora, selected corpus records, raw repository snapshots and
private coordination files. No remote write was performed. Any later v2
acceptance must be a separately identified artifact rather than rewriting this
historical v1 audit verdict.
