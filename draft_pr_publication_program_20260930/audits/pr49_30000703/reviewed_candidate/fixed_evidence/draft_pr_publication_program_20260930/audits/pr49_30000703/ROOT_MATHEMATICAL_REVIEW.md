# ROOT review of the exact unrestricted boundary question

The submitted conclusion is valid for the literal selected problem, as an
application of the credited Kraus–Roth–Ruscheweyh reflection theorem. The
appropriate disposition is **already_solved**, original0/5, new0/audit0,
without a new result, paper, DOI or tracker row. Acceptance and the current
whole-package review remain separate pending steps.

Exact original head036a5ed59bee5ed79f08349290481584610f1456; GitHub base and
merge basec6975ca76f9f667f1250ba403d0e6da2aafe14d0. The original has16
scientific files and a17-path diff of52829 bytes, SHA256
9aafdb42b2983020e919d6ff66b03720e1d858eebd98b4e46fa6b3909923fb50.

## Claim, imported premise and universal deduction

For a holomorphic map f:D→D, define

    Φ(z)=(1−|z|²)|f′(z)|/(1−|f(z)|²).

The denominator is positive inside D; Schwarz–Pick gives0≤Φ≤1. The selected
hypothesis is Φ(z)→1 as z→1 through every interior approach. It is equivalent
to holomorphic continuation through some open circle arc containing1,
carrying that arc into the unit circle. The continuation gives η=f(1) with
|η|=1 and conj(η)f′(1)=α>0, hence a local inverse. Neither global injectivity
nor whole-circle continuation is asserted.

The non-elementary imported premise is Theorem1 in Roth's original
[OWR9/2007 contribution, printed528–530](https://ems.press/content/serial-article-files/46093).
It equates positive unrestricted liminf of Φ at every point of an open arc
with holomorphic continuation mapping the arc into the circle. Its credit
is [Kraus, Roth and Ruscheweyh, J. Analyse Math.101(2007),219–256](https://link.springer.com/article/10.1007/s11854-007-0009-x).
ROOT freshly read the official extracted theorem and Problem1 text, the
later primary [arXiv2410.13965v1 §8.2 equation8.3](https://arxiv.org/html/2410.13965v1#S8.SS2),
and publisher metadata. Equation8.3 independently records the exact
single-point unrestricted equivalence. ROOT claims no fresh PDF-byte hash
or personally viewed PDF pixels and has not independently reconstructed
the complete2007 journal proof. Both mathematical reviewers separately
authenticated relevant original and v1 PDF bytes/pages. The journal theorem
remains explicitly imported; finite checks do not prove it.

To apply the imported theorem, choose c>0 and0<δ<1 with Φ(z)>c on
D∩B(1,δ), which follows even from positive unrestricted liminf at1. Take
Γ={ξ∈∂D:|ξ−1|<δ/2}. For each fixed ξ∈Γ, every z∈D with
|z−ξ|<δ/2 satisfies |z−1|<δ by the triangle inequality. Thus its unrestricted
liminf is at least c. This is exactly the arc theorem's hypothesis. No
uniform convergence on an arc, interchange of limits, or angular-to-full
neighborhood inference is used. A radius or fixed Stolz angle gives no such
bound near neighboring circle points.

## Derivative sign and unrestricted converse

After continuation, continuity permits a zero-free neighborhood of1. Put
u=−log|f|, harmonic across the arc, positive on the disk side and zero on
the circle. Constants into D cannot satisfy the hypothesis. A ball with
center1−a and radius a is internally tangent at1 and can be chosen within
the zero-free neighborhood. Let m>0 be the minimum of u on its concentric
circle of radius a/2. On the intervening annulus compare u with

    v(z)=m log(a/|z−(1−a)|)/log2.

The minimum principle gives u≥v from both boundary circles. Along1−t,
v=m log(a/(a−t))/log2. Differentiability then makes the inward derivative of
u at least m/(a log2)>0. This supplies the Hopf sign without treating the
boundary derivative as an assumption.

Differentiating |f(e^it)|²=1 gives Im(conj(η)f′(1))=0. The outward radial
derivative of log|f| is Re(conj(η)f′(1)), positive by the barrier. Thus
α=conj(η)f′(1)>0 and f(z)=η+αη(z−1)+O(|z−1|²). The inverse function
theorem is local. At a general ξ the correct coefficient is
conj(f(ξ))ξf′(ξ)>0; no conjugation factor is omitted.

For the converse, write N(r,t)=1−|f(re^it)|² near the continued arc. Since
N(1,t)=0, the exact fundamental-theorem identity is

    N(r,t)/(1−r²)
      =−1/(1+r) ∫₀¹ ∂r N(1+s(r−1),t) ds.

This quotient extends continuously to the boundary and has value α at1.
Meanwhile |f′|→α, so Φ=|f′|/[N/(1−r²)]→1 under every interior approach.
This proves the converse without dividing an uncontrolled Taylor remainder
by a possibly much smaller1−|z|². For example (1−t^m)e^it with m>2 makes
|z−1|²/(1−|z|²) diverge. A merely radial l'Hopital computation would fail
to establish the required quantifier.

Local nonvanishing also makes the exterior reciprocal-conjugate reflection
1/conj(f(1/conj z)) holomorphic on a smaller exterior neighborhood. It
matches the circle-valued continuation by uniqueness. Zeros or critical
points elsewhere in the disk are allowed, and arc endpoints are outside
the claimed extension neighborhood.

## Attempts to falsify the scope

Powers z^k, k≥2, have Φ=k r^(k−1)/(1+r²+…+r^(2k−2))→1. They disprove
global automorphism claims while satisfying the local theorem. For a>0 and
|η|=1, f(z)=η exp(−a(1−z)/(1+z)) maps D into D because
u=Re((1−z)/(1+z))=(1−|z|²)/|1+z|²>0. Direct differentiation gives
Φ=a u/sinh(a u)→1 unrestrictedly near1 and f′(1)=aη/2. Every positive α
occurs. The essential singularity at−1 blocks whole-circle and finite
Blaschke conclusions. Constants on the circle are outside the stated
codomain; constants inside haveΦ=0.

The right-half-plane map F(W)=W+a log(1+W), a>0, supplies a useful weaker
hypothesis counterexample. ReF>0. In a fixed non-tangential sector at
infinity, F/W→1, F′→1 and ReF/ReW→1. On W=1+iy its distortion tends0,
since ReF=1+(a/2)log(4+y²) while |F′|→1. This supports the distinction
between angular/radial and unrestricted conditions. It is no counterexample
to the selected theorem. No rate strong enough for global rigidity was
assumed. The neighboring OWR metric-boundary-regularity problem remains
outside this review.

The geometry family independently checked a pullback-metric collar and its
last-crossing intrinsic-distance lower bound, with curvature−4 versus−1
normalizations cancelling in the ratio. Its local logarithm leading-term
argument independently verifies positive α. Neither pullback completeness
nor finite controls are presented as a new proof of the imported reflection
theorem. The boundary family independently supplied the barrier, defining
function argument and312 exact controls with two meaningful rejected sign/
tangential mutations. Both reports have no mandatory mathematical defect.

## Reproduction, provenance and custody

ROOT personally read all16 original bodies, all9 JSON values, both unique
helper sources, old review, saved receipts and metadata. The initial large
display trimmed part of the independent helper; ROOT separately reread that
complete helper and187-label saved receipt before authorizing reproduction.
Actual ROOT child60012 reproduced33 read-only Git body/tree/diff operations
and three unchanged helper children. Full saved69/69/187 receipts and every
recursive JSON scalar type match. The duplicated69 source/result is the
same author calculation and is not independent mathematics. These symbolic
checks verify formulas and finite margins, not the central analytic theorem.

Original350+self preparation and both mathematical families are closed with
separate real ROOT closure/readback captures. The boundary family has
473+self files; geometry107+self. ROOT read their entire reports, verdicts,
universal proofs and closers before executing those closures. The geometry
closer ran with actual repository cwd, deriving its correct family from
__file__; its suggested family cwd is not falsely reported as actual.

Upstream prior-report absence, SQLite literal{} and original literalnull
are distinct. The original null file is preserved as an administrative
marker. The plain source has integer ID30000703 and its imported weaker
angular assessment is dated and superseded for this exact target. ROOT's
independent full raw/SQL audit is recorded separately with genuine actual
capture, including a retained failed schema-key comparison and distinct
corrected version. Historical model, deadline, priority-search, PDF-access,
rendering and old PASS claims stay attributed; no current runtime or human
review identity is invented.

Original turns.json is a single object with count0, empty substantive
attempts and a five-attempt limit. There is no separate original count field
for a source-verification response; that administrative description must
not be promoted into a fabricated original ledger entry. These current
audits consume no new substantive proof-search attempt. Extensive AI use;
unrefereed, no human peer review or formal certification claim. Assigned
mathematical review completion100%; new discovery0%. Global source/history
qualifications, a new current-package review and actual native integration
remain necessary before merge.

## 2026-10-03 06:44 UTC actual provenance checkpoint

ROOT raw child62744 completed06:43:47.174022UTC with exit0. It reread149266659 raw/prior bytes and independently verified all15458 literal importer payload/report serializations and recursive value types. Exact unique-key comparison matches every original row witness despite its raw-input ordering and the independent SQL lexical ordering. The initial60964 schema-key error and61299 row-order assumption are retained with complete actual failed captures and literal sources; only distinct V3 passed. Selected upstream report absent, SQLite literal{}, and original null administrative marker are verified, not conflated. Mathematical review100%; original reproduction/provenance100%; current-packet/native acceptance pending. No new substantive turn or paper/DOI.
