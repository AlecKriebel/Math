# Independent adversarial check of the Green formula

Checkpoint: 2026-10-01 05:35 UTC (2026-09-30 22:35 PDT).

Scope: Section 6, formula (6.1), and the complete definition surrounding
(1.3) in `../source_snapshot/PROOF.md`. No source edits, outside input,
git operations, or reliance on another reviewer's findings.

**Verdict: PASS.** Formula (6.1) supplies a bounded linear right inverse
for the two-sided difference operator on bounded sequences under precisely
the stated complete splitting hypotheses. Projection commutation is not
needed. This verifies the generalized-hyperbolicity-to-shadowing implication
on arbitrary real or complex Banach spaces. It does not audit the other
direction or any novelty claim.

Completion estimate for this narrowly assigned verification: **100%**.

## Claim and hypotheses actually used

Let E be a real or complex Banach space, T a bounded invertible operator,
and E=M direct-sum N a topological direct sum of closed subspaces. Let P
and Q be its bounded complementary projections, so P+Q=I, range(P)=M,
and range(Q)=N. Assume

\[
TM\subset M,\qquad T^{-1}N\subset N,\qquad
r(T|_M)<1,\qquad r(T^{-1}|_N)<1.
\]

These are the full hypotheses given before and in (1.3), not just the
four displayed conditions considered without the direct-sum requirement.
The restrictions need not be surjective. The boundedness of P and Q
follows from the topological direct sum; it also follows from closedness,
complementarity, and the closed graph theorem.

Choose alpha strictly between the maximum of the two restriction radii
and 1. The spectral-radius formula gives a finite C (enlarge it to cover
the finitely many initial powers) such that

\[
\|T^j|_M\|\le C\alpha^j,\qquad
\|T^{-j}|_N\|\le C\alpha^j\quad(j\ge0).
\]

For a real Banach space, spectral radius is understood through the usual
complexification, or equivalently through the norm growth of powers.
Equivalent complexification norms change the power norms by at most
fixed multiplicative factors, so the same exponential estimates follow.
There is no complex-only step later in the argument.

## Convergence and a concrete uniform bound

For any b in ell-infinity(Z,E), set beta=sup_n ||b_n|| and define

\[
y_n=\sum_{j\ge0}T^jPb_{n-1-j}
       -\sum_{j\ge0}T^{-j-1}Qb_{n+j}.
\]

One-sided invariance is sufficient: Pb_k is in M and Qb_k is in N, so

\[
\|T^jPb_k\|\le C\alpha^j\|P\|\beta,\qquad
\|T^{-j-1}Qb_k\|\le C\alpha^{j+1}\|Q\|\beta.
\]

Both series converge absolutely, uniformly in n, in the Banach space E.
In fact, they converge as sequences in ell-infinity(Z,E), and

\[
\|y\|_\infty\le K\|b\|_\infty,\qquad
K=\frac{C(\|P\|+\alpha\|Q\|)}{1-\alpha}.
\]

No relation between P or Q and T was used in these estimates.

## Finite telescoping identity: the cancellation is checkable

Define the common finite truncation

\[
y_n^{(J)}=\sum_{j=0}^{J}T^jPb_{n-1-j}
       -\sum_{j=0}^{J}T^{-j-1}Qb_{n+j}.
\]

Expanding y_(n+1)^(J)-T y_n^(J), without commuting a projection through
T, gives exactly

\[
y_{n+1}^{(J)}-Ty_n^{(J)}
=Pb_n+Qb_n
-T^{J+1}Pb_{n-1-J}
-T^{-J-1}Qb_{n+J+1}.
\]

The two tail norms have sum at most

\[
C\alpha^{J+1}(\|P\|+\|Q\|)\beta,
\]

uniformly in n. Since P+Q=I, letting J tend to infinity proves

\[
y_{n+1}-Ty_n=b_n\quad(n\in\mathbb Z).
\]

Boundedness of T justifies passing it through the norm limit. Index
shifts only move the sequence indices; they never require TP=PT or
TQ=QT. Thus the sentence immediately following (6.1) is correct.

## From the solution to two-sided shadowing

For a pseudotrajectory x, use b_n=x_(n+1)-Tx_n and let z_n=x_n-y_n.
Then z_(n+1)=Tz_n. Invertibility gives z_n=T^n z_0 for every positive
and negative integer n. Also ||x_n-T^n z_0|| <= K||b||_infinity.
For E nonzero, choosing delta=epsilon/(2K) gives strict epsilon
shadowing for every pseudotrajectory with all errors less than delta.
The zero space is immediate. This closes the quantitative implication.

## Adversarial noncommuting example

Take E=ell-p(Z), for any 1<=p<infinity, over either scalar field. Define

\[
(Tx)_n=w_nx_{n+1},\qquad
w_n=\begin{cases}1/2,&n<0,\\2,&n\ge0.\end{cases}
\]

It is a bounded invertible bilateral shift. Let M be the coordinate band
n<=0 and N the band n>=1, with their coordinate projections P and Q.
For every j>=0,

\[
TM\subset M,\quad T^{-1}N\subset N,\qquad
\|T^j|_M\|=2^{-j},\quad
\|T^{-j}|_N\|=2^{-j}.
\]

But T e_1=2e_0, hence P T e_1=2e_0 while T P e_1=0. This splitting
really has noncommuting projections. The preceding finite identity and
bounds apply to it unchanged. For example, for the forcing b_0=e_1,
b_n=0 for n!=0, the formula gives y_1=0 and y_0=-T^(-1)e_1=-e_2/2,
so y_1-Ty_0=e_1 at the forced index.

The same example exposes a potential overclaim which the source does
**not** make: bounded solutions need not be unique. The nonzero orbit
T^n e_0 has norm 2^(-|n|) for all integer n, so it is a bounded
homogeneous solution. Formula (6.1) is a right inverse, not necessarily
an inverse, of the difference operator.

## Boundary cases and assumptions checked

- M=0 or N=0 is allowed: its series vanishes and the other series still
  satisfies the same proof. The restriction on a zero space is treated
  by its trivial norm decay.
- No reflexivity, separability, Hilbert structure, finite-dimensional
  assumption, positivity, measurability, or norm attainment is used.
- The strict spectral-radius inequalities are material. If they are
  replaced by <=1, T=I on a nonzero scalar space with constant forcing
  b_n=1 has no bounded solution, since y_(n+1)-y_n=1.
- Complementarity is material. Merely writing the four displayed
  conditions with M=N=0 would satisfy their decay parts for T=I but
  would not imply shadowing. The source explicitly supplies E=M direct-
  sum N, P+Q=I, so this is not a missing hypothesis there.
- Only forward invariance of M and backward invariance of N is used.
  Equality of either invariant image, or two-sided invariance of each
  subspace, is unnecessary.

**Strongest verified result:** under the complete definition (1.3),
formula (6.1) converges uniformly and absolutely and solves every bounded
forcing with the displayed explicit K. It proves two-sided shadowing
over both real and complex scalar fields.

**Remaining gap in this assigned claim:** none. Other proof sections
and novelty remain outside this independent check.

## Follow-up adversarial review of the consolidated report

Checkpoint: 2026-10-01 05:44 UTC (2026-09-30 22:44 PDT).

At the parent reviewer's request, I then read the freshly written
`REPORT.md` and `adversarial_probes.py`. This expanded check includes the
report's density bounds, uniform-fiber counterexample, real-space renorming,
duality and support-band reconstruction, and its provenance statements.
I did not read the preserved historical review and did not assess literature
priority. I ran the probe program directly without modifying it or any
canonical source.

**Mathematical verdict: PASS for the expanded checks.** No new blocking
error or mathematical overclaim was found. Completion of this added review:
**100%**. The following derivations make the focused checks reproducible.

### Density bounds have the correct directions

For a measurable A subset W, iteration of the first measure bound gives
nu_n(A)<=c_+^n nu(A) for n>=0. Applying the second bound n times to
f^n A gives nu(A)<=c_-^n nu_n(A). The negative-index bounds are obtained
by the identical argument with the two constants exchanged. Thus the
report's bounds

\[
c_-^{-n}\nu(A)\le\nu_n(A)\le c_+^n\nu(A),\qquad
c_+^{-m}\nu(A)\le\nu_{-m}(A)\le c_-^m\nu(A)
\]

are correct for nonnegative integers n,m. Both constants must be positive:
the two inequalities applied to W and fW rule out either zero or negative
constant because nu(W)>0 and mu(fW) is finite. For every integer n,
applying the original inequalities to f^n A directly gives

\[
c_-^{-1}\nu_n(A)\le\nu_{n+1}(A)\le c_+\nu_n(A).
\]

Testing all measurable A then gives the same inequalities for their
densities almost everywhere. Consequently a_n=(rho_n/rho_(n+1))^(1/p)
is at most c_-^(1/p), and its reciprocal is at most c_+^(1/p), exactly
as claimed. A common full-measure set can be chosen for all integer n.

### The uniform-fiber example is a genuine counterexample to uniformity

Write q_i=1+1/i. For mu({(i,n)})=2^(-i)q_i^n and f(i,n)=(i,n+1),
every atom has finite positive mass, so the countable atomic space is
sigma-finite, and W has mass sum_(i>=1)2^(-i)=1. On each atom, the ratios
of the image and inverse-image masses to the original mass are q_i<=2
and q_i^(-1)<=1. Summing over any measurable set proves c_+=2,c_-=1,
including sets of infinite measure.

Normalization of fiber i gives the scalar bilateral shift q_i^(-1/p)U,
where U is an isometry. Its forward norm rate is strictly below 1, so
each individual fiber has shadowing. In contrast, for any common positive
integer d and eta<1,

\[
\frac{\min\{\rho_{n-d}(i),\rho_{n+d}(i)\}}{\rho_n(i)}
=q_i^{-d}\longrightarrow1.
\]

Every offending i is an atom of positive W measure, so the violation
cannot be removed as a null set. Independently of using the target
equivalence as a premise, the proven necessary Lemma 2.1 rules out global
shadowing: for a coordinate-n dual indicator on atom i, the maximum
adjoint power ratio is q_i^(d/p), which is below 2 for i sufficiently
large, for every fixed d. Thus this counterexample is not circular.

### Renorming works over either scalar field

For alpha<gamma<1, the report's sup norms have the explicit bounds

\[
\|m\|\le |m|_M\le C\|m\|,\qquad
\|n\|\le |n|_N\le C\|n\|.
\]

The upper bounds follow because (alpha/gamma)^j<=1. For x=m+n,

\[
\|x\|\le |x|\le C(\|P\|+\|Q\|)\|x\|.
\]

Therefore this is a complete equivalent norm on E. Index shifting gives

\[
|Tm|_M
=\gamma\sup_{k\ge1}\gamma^{-k}\|T^k m\|
\le\gamma|m|_M,
\]

and the same calculation gives |T^(-1)n|_N<=gamma|n|_N. One-sided
invariance ensures these norms are evaluated on their own subspaces.
No projection is moved past T, no complex scalars are needed, and
zero summands cause no difficulty. The one-step-contraction assertion
is valid in this equivalent norm.

### Other reconstruction and probes

I found no error in the report's exact dual residual endpoints, scalar
L^1 dual localization, propagation of density drops, complementary-band
construction by finite intersections, or summation of the disjoint pth
power estimates. In particular, the stronger observation excluding a
positive-measure set where both adjoint multiplication factors are <=2
follows by the same localized indicator and Lemma 2.1's strict >2 bound.
The constant-density boundary forcing also has the asserted exact
transformed recurrence v_(j+1)-v_j=e_0.

The probe run returned all passes with exactly 77 endpoint checks,
168 noncommuting Green identities, 48 uniform-fiber witnesses, and
one L-infinity localization example. These finite exact computations
corroborate the algebra and examples; the analytic arguments supply
the claims for arbitrary indices and spaces.

### Provenance correction identified and relayed

The report's initial sentence that this Green subagent had read *only*
Section 6 and definition (1.3) was factually too narrow. I displayed
the complete candidate proof in two reads, then initially audited only
the Section 6 claim. I reported this immediately to the parent, who
confirmed replacing that sentence with wording distinguishing what
was read from the initial audit scope. My own verification was derived
before reading this consolidated report, and neither the preserved
historical review nor another reviewer finding was used in that initial
derivation. I can directly attest those facts for this subagent; other
reviewers' reading histories are theirs to attest.

**Remaining mathematical gap found in this follow-up:** none. Novelty,
priority, and bibliographic claims remain outside the follow-up verdict.
