# Root source-first INITIAL — SU(5) lens-space calculation

2026-11-17 UTC. Source-only reading complete100%; overall review40%. No full-original disposition yet. This is an independently written derivation from the current published manuscript before current peer findings, support programs/results/audits, priority supplement or new outside primary proofs were opened.

## Actual reading and custody

Personally read all292 lines of native `assets/pr95_note.tex`, the entire five-page searchable PDF text and all five fresh owned110dpi PDF images individually. All three installed pdfinfo/pdftotext/pdftoppm calls exited0 with empty stderr; individual calls, times and streams are in EXTRACTION_RECEIPT.json. No native scientific checker or source helper has run. Read exact original LICENSE.txt and selected native metadata/asset entries. Current family/source handoff titles and checksum metadata were known before this review; no current family report, archived support science/opinion or priority-supplement body has been opened. General prior knowledge of RT invariants, lens spaces, roots/weights and earlier catalogue work is disclosed; this is not a claim of having no mathematical background.

Record23174156, DOI10.5281/zenodo.23174156, native1.0, declared5October2026, created2026-10-05T23:36:06.236810UTC. The PDF actually prints5October2026 and no numeric version. Current native file entries were updated10October2026; an original creation date is not a proof that every current byte was visible on that date. Native order: SHA256SUMS.txt, pr95_note.tex, pr95_support.zip, PR95_PRIORITY_QUALIFICATION.md, pr95_note.pdf, README.md, LICENSE.txt. Original authored manuscript/code/results/docs are CC BY4.0, third-party rights retained. Source custody is separate and all186 source files/18directories must remain unchanged.

## Exact hypothesis and success criterion

The target is the printed Guadagnini–Pilo Conjecture7.5 in Ohtsuki's collection, not an assertion that it is worldwide open now. At ordinary **full** SU(5) WZW level5, shifted level10, and fixed normalization `tauhat(S3)=1`, show `|tauhat(L(5,1))|²=3475+1550sqrt5`, `|tauhat(L(5,2))|²=4025+1800sqrt5`, positive unequal numbers for manifolds sharing fundamental group Z/5. A proof must match this full ordinary category and its actual surgery normalization, not a root-lattice restricted category, projective quotient, spin/background/bundle sector, retained framing or inserted link. The root lattice in the calculation is a computational quotient; verify this in the actual primary theorem. Category existence and RT surgery are explicit imported inputs, not reconstructed by the finite calculation.

## Own hand derivation from the printed formula

In A4, choose simple roots `alpha_i=e_i-e_(i+1)`. Their Gram matrix has diagonal2 and adjacent−1, determinant5, giving covolumes sqrt5 and1/sqrt5. Positive-root count10, rank4, rho=(2,1,0,−1,−2), rho²=10. The integrable dominant labels have four nonnegative Dynkin entries summing at most5, counted by stars-and-bars `binom(9,4)=126`. This count alone does not identify the full RT category; the primary theorem interface remains to check.

Taking the manuscript's Hansen–Takata expression conditionally as written, at p5/r10 the quadratic phase is `exp(2pi*i*q*nu²)=1` since nu² is integral. Simple-root coordinates provide exactly625 quotient representatives. For integral sum-zero v, their additive character sum factors as four geometric sums on `(v_i-v_(i+1))mod5`. It is625 exactly when all five residues coincide. This is membership in5X, not5Y; requiring all residues individually zero would incorrectly discard four survivors.

For each nonzero qmod5 and constant cmod5, `w rho_i` must be the unique member of {2,1,0,−1,−2} congruent to `q rho_i−c`. Rho contains every residue once, so there are exactly five permutations, no unaccounted survivors. For q1, c0–4 give the five successive cyclic shifts in the manuscript. Their parity is+ (a5-cycle is even), with dot products10,0,−5,−5,0. For q2, c2 gives `(2,0,−2,1,−1)`, permutation indices(0,2,4,1,3) with three inversions, hence sign−. Changing c composes an even5-cycle, so every q2 survivor has sign−. The remaining displayed rows give dot products5,5,−5,0,−5 by direct integer multiplication. Thus, with z=exp(2pi*i/50), t=z5=exp(pi*i/5), the complete sums are

`B1=t^-2+2+2t`, `B2=−(1+2t^-1+2t)`.

Put phi=t+t^-1=(1+sqrt5)/2 in the actual positive embedding. For B1, diagonal norm terms sum9; cross terms are `4(t+t^-1)+2(t²+t^-2)+2(t³+t^-3)`. The last two cancel, giving `9+4phi=11+2sqrt5`. For B2, `1+2phi=2+sqrt5`, so its square is `9+4sqrt5`. These are exact identities, not floating-point comparisons or acceptance of a saved output target.

For normalization at p1 the quotient has one class and the Weyl sum is A. In the Weyl denominator, ten positive-root phase differences contribute `(-2i)^10=−2^10`; hence A is minus the positive sine product, rather than its absolute value being silently substituted. Write a=2sin18=phi^-1, b=2sin36, c=2sin54=phi, d=2sin72. Then ac=1, bd=sqrt5, b²=(5−sqrt5)/2, and

`P=a^4*b^3*c²*d=a²*b²*sqrt5=5sqrt5−10>0`.

Thus `A=10−5sqrt5`, `A²=225−100sqrt5>0` (225²>100²*5). The p5 prefactor relative to p1 is1/25 and the character sum supplies625, giving exactly25 times Bq/A and a unit Dedekind phase. Therefore the squared magnitudes are625*|Bq|²/A². Rationalization uses `(225−100sqrt5)(225+100sqrt5)=625`, so multiplication gives exactly `(3475,1550)` and `(4025,1800)` as constant/sqrt5 coefficients. Their difference is550+250sqrt5>0. It cannot be removed by a fixed nonzero theory-wide normalization.

The printed vacuum value is `s=−A/(100sqrt5)>0`, with `s²=(9−4sqrt5)/2000` and inverse `100+40sqrt5`. These identities follow directly by rationalization. The purported matrix-word comparison must use this ordinary normalized S and divide the vacuum word by s **once**; a categorical Hopf matrix DS would otherwise introduce spurious powers. Primary Corollary4.2/Eqs26–30,35 and source code must still be checked. Central charge `k dimSU5/(k+hdual)=5*24/10=12`, so the scalar linking the usual linear T to the given twist is exp(−2pi*i*12/24)=−1, of unit modulus. The anomaly and signature phases can change phase, not magnitude; their actual category conventions remain external checks.

For orientation, replace w by w*w0 where w0rho=−rho and detw0=(−1)^10=+1. Sending q to−q then conjugates the exponentials and Dedekind phase; i10=−1 is real. Hence the magnitudes agree for q1/4 and q2/3. Inverse-denominator conventions exchange2 and3, preserving the two unequal magnitude classes. This checks common orientation/q conventions without asserting every surgery convention matches automatically.

The unknot exterior's preferred longitude is nullhomotopic while its meridian generates Z. Filling along −5/q therefore kills the fifth meridian power; van Kampen gives Z/5, independently of q. Both are closed connected oriented lens spaces. No homotopy equivalence, all-level classification, or minimal counterexample is needed. Levels r10 and k5 must never be conflated; p5 is **not** coprime to r10.

## Remaining falsifiable gates and limits

1. Read actual Hansen–Takata v2 Theorem5.1 and surrounding category/level/lattice definitions. Check every phase/covolume/shift and that it is the full ordinary SU5 invariant at admissible r10, with no condition gcd(p,r)=1. Its later coprime simplification cannot be substituted. Match S3 normalization and matrix-word interface from actual primary passages.
2. Read the actual printed Ohtsuki Conjecture7.5 and Guadagnini–Pilo context. Check that compact simple simply connected G includes this SU5 example and that the conjecture concerns the same ordinary invariant/magnitudes, not only an SU2 lens-space theorem.
3. Only after this seal, inspect both current independent reports, supporting exact programs in full, recorded ordinary reproduction streams and negative controls. Independently match the code's cyclotomic embeddings, character criterion, normalization, all126 labels/120 Weyl permutations and expected exact arithmetic. Choose further execution only if a meaningful unresolved check requires it; do not replay to inspect or duplicate a satisfactory finite test.
4. Inspect the native priority qualification and actual accessible primary Kuriya listing/report and Kubo–Yokoyama distinctions. A directly relevant inaccessible Kuriya text is a real novelty-comparison limit. Do not infer absence or exact conclusions from a title, and do not contact anyone. The original paper already explicitly disclaims firstness/new historical resolution; evaluate its actual qualified claim without inventing such promotion.
5. Inspect ancillary claims and all native asset/rights/order consistency. No follow-up is presently justified. If a substantive mathematical or unresolved input gap appears, record it as deferred and move on; do not repair or promote a weaker target.

Strongest currently checked result: the printed lattice expression, **conditional on its actual primary interface**, yields the two exact unequal magnitudes by the hand derivation above, and the two lens spaces have the same fundamental group. External formula/category identification, supporting finite implementation and qualified context are still pending. Full-original disposition and canonical page remain unapproved.
