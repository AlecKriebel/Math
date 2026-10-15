# PR12 independent Banach/duality adversarial audit

Audit target: `../source_snapshot/PROOF.md`, SHA256
`f38ae2dd97bb2aeb8f1e97da0f4133b84b6d43d803e2b38df2c91acc56817a8e`.
This hash was independently checked against the snapshot manifest. The
candidate was read before any prior review or other family's mathematical
findings. The preserved historical review was not opened. The independent
Green-formula subagent read the candidate directly and initially audited
Section 6 against definition (1.3).

**Verdict: PASS for the mathematics audited here.** No blocking defect was
found in the forcing/shadowing equivalence, Lemma 2.1, dual localization,
or the generalized-hyperbolicity-to-shadowing converse. Reconstruction of
Sections 1–6 also found no hidden gap in the complete theorem under its
explicit assumptions. The finite-dimensional, nonreflexive, nonseparable,
real/complex, zero-band, and p=1 cases do not require an additional hypothesis.

This is an independently checkable mathematical review, not formal proof
certification. Historical priority, literature completeness, and all claims
about recent papers remain outside this family's verdict. The theorem is
not asserted here for p=infinity or vector-valued L^p.

## 1. Exact claim and success criteria

The candidate concerns a sigma-finite measure space, a bijective bimeasurable
map f, constants c_+, c_- with both measure bounds in (1.1), and a wandering
set W of finite positive measure whose integer translates partition X up
to null sets. For each fixed scalar L^p, 1<=p<infinity, its claims are:

1. Two-sided shadowing implies a decomposition into complementary measurable
   support bands M,N, with TM contained in M, T^{-1}N contained in N, and
   uniform exponential decay in those respective directions.
2. Any topological direct sum satisfying those invariance and decay conditions
   implies two-sided shadowing, even for arbitrary real/complex Banach spaces.
3. Those properties are equivalent to the existence of common d>=1 and
   eta in (0,1) with min(rho_{n-d},rho_{n+d})<=eta rho_n almost everywhere,
   simultaneously for every integer n.

The audit tests the actual two-sided definition, which permits unbounded
pseudotrajectories and unbounded exact orbits. Replacing it by a definition
that quantifies only over bounded pseudotrajectories would require a separate
argument. No such replacement occurs in the candidate.

Success requires valid constants uniform over all forcings and fibers, correct
dual endpoint indices, scalar L^1 duality, a measurable complete splitting,
and a right inverse of the difference operator without assuming commuting
projections. These are established below. None of the proof uses the claimed
full recent shadowing characterization as a premise.

## 2. Check against original source assumptions

The [official OWR report](https://ems.press/content/serial-article-files/49477)
was independently read on 2026-10-01. Pages 1079–1080 use scalar L^p,
1<=p<infinity, both boundedness assumptions, a finite positive wandering
set, and two-sided shadowing. Its generalized-hyperbolicity definition places
the two restriction spectra inside the open unit disk. The two questions
occur on printed page 1080. The candidate's hypotheses match that setting.
The report initially presents operators on separable complex Banach spaces;
the candidate explicitly extends the resulting theorem to real and
nonseparable scalar L^p spaces, and the proof supports that extension.

The [original preprint](https://arxiv.org/pdf/2009.11526), Definitions
2.5.1 and 2.6.3, independently confirms the finite-positive-W convention and
the bounded invertible composition-operator setting. Its Definition 2.4.2
uses one-step proper contractions; the candidate acknowledges equivalent
renorming rather than claiming contraction in the original norm.

No downloaded source files or prior reviewer outputs were used. Web reading
was read-only; no individual was contacted.

## 3. Forcing/shadowing equivalence, with explicit constants

Let A be a bounded invertible operator on a real or complex Banach space E.
Fix shadowing accuracy 1 and let delta_0>0 be its error tolerance. Given
bounded b=(b_j) with beta=sup_j ||b_j||>0, set

\[
c=\frac{\delta_0}{2\beta}.
\]

Start x_0=0. For nonnegative j recursively set
x_{j+1}=Ax_j+c b_j. For negative j, define
x_j=A^{-1}(x_{j+1}-c b_j). Every coordinate belongs to E. No boundedness of
x is needed. Its errors have norm at most delta_0/2, so it is shadowed by
some orbit A^j z with ||x_j-A^j z||<1 for every j. Set

\[
y_j=c^{-1}(x_j-A^jz).
\]

Then y_{j+1}-Ay_j=b_j and

\[
\sup_j\|y_j\|\le \frac{2}{\delta_0}\beta.
\]

Zero forcing has the zero solution. Thus K=2/delta_0 works uniformly. A
continuous or linear choice of y is unnecessary for this implication.

Conversely, suppose every bounded forcing admits a solution with
||y||_infinity<=K||b||_infinity. Given accuracy epsilon>0, choose
delta=epsilon/(2K) for a nonzero space. For a pseudotrajectory x, define
b_j=x_{j+1}-Ax_j and choose its bounded solution. Then x_j-y_j=A^jz
for z=x_0-y_0, for all positive and negative j. Its error is at most
epsilon/2<epsilon. The zero space is immediate. This proves the equivalence
without reflexivity, separability, compactness, or a bounded selection theorem.

## 4. Lemma 2.1: dual inequality and exact endpoints

Write S=A^*. For a finitely supported sequence u_j in E^*, choose b_j in
the unit ball on its finite support with

\[
\operatorname{Re}u_j(b_j)\ge \|u_j\|-\varepsilon_j,
\qquad \sum_j\varepsilon_j\le\varepsilon.
\]

For real scalars choose a sign as needed; for complex scalars multiply a
nearly norming vector by a phase. Set b_j=0 outside that finite support.
The forcing property gives a bounded y with ||y||_infinity<=K. Since u
and its translated sequence are finitely supported, all sums below are
finite regardless of any orbit behavior:

\[
\sum_j u_j(b_j)
=\sum_j u_j(y_{j+1}-Ay_j)
=\sum_j (u_{j-1}-Su_j)(y_j).
\]

Taking real parts and letting epsilon decrease to zero proves

\[
\sum_j\|u_j\|\le K\sum_j\|u_{j-1}-Su_j\|.\tag{D}
\]

Norm attainment is not assumed. The solution y may vary with epsilon;
the right-hand bound is independent of y and epsilon, so passage to the
limit is still valid.

For nonzero u, set a_j=||S^j u||. Given integers a<=b, let
u_j=S^{-j}u on -b<=j<=-a and zero elsewhere. The only nonzero residuals
u_{j-1}-Su_j are exactly

\[
j=-b:\ -S^{b+1}u,
\qquad j=-a+1:\ S^a u.
\]

Their indices are distinct even when a=b. Substitution into (D) yields

\[
\sum_{j=a}^b a_j\le K(a_a+a_{b+1}).\tag{E}
\]

The candidate has both endpoints correct. In particular, [-j,j-1]
contains zero for j>=1, so (E) gives a_0<=K(a_{-j}+a_j).

Now suppose a_{-d}<=2a_0 and a_d<=2a_0. Applying (E) to [-d,d-1]
gives sum_{-d}^{d-1}a_j<=4Ka_0. The d-1 pairs with indices
(-j,j), 1<=j<=d-1, all belong to that segment; therefore

\[
\frac{d-1}{K}a_0
\le \sum_{j=1}^{d-1}(a_{-j}+a_j)
\le 4Ka_0.
\]

Since a_0>0 and K>0, this implies d-1<=4K^2, contrary to
d>4K^2+1. Thus the claimed strict maximum bound >2||u|| follows.
The proof does not claim sharpness of this numerical d.

The adjoint inverse exists because (A^{-1})^*=(A^*)^{-1}. No part of this
argument identifies E with its double dual or assumes any special geometry.

## 5. Measure coordinates and endpoint localization

The measure assumptions justify positivity and finiteness of every density.
For n>=0 and A subset W,

\[
c_-^{-n}\nu(A)\le\nu_n(A)\le c_+^n\nu(A),
\]

and for m>=0,

\[
c_+^{-m}\nu(A)\le\nu_{-m}(A)\le c_-^m\nu(A).
\]

Both constants are positive because W has positive measure and f is
bijective. Hence the Radon–Nikodym densities are finite, strictly positive,
and measurable almost everywhere. More locally, for every n,

\[
\frac1{c_-}\rho_n\le\rho_{n+1}\le c_+\rho_n.
\]

These inequalities follow from the measure bounds on f^nA, followed by the
usual test-set characterization of inequalities between densities. They
provide the bounds ||B||<=c_-^{1/p} and ||B^{-1}||<=c_+^{1/p}.

The candidate's U is isometric by partitioning the integral over f^nW;
its inverse on each such piece sends a measurable g_n to
rho_n^{-1/p}g_n composed with f^{-n}. Changing representatives on null sets
does not affect either map, because all integer iterates preserve null
sets in both directions. If the partition holds only modulo null sets,
remove the saturation under all iterates of the exceptional set. That is
still a measurable null set and makes the coordinate calculation literal.

Omega=W times Z is sigma-finite. For scalar L^p its entire Banach dual is
L^q when 1<p<infinity and L^infinity when p=1. This remains true if the
measure algebra is nonseparable. The proof is not using vector-valued
Bochner duality or an unproved direct-integral theorem.

The adjoint pairing gives (Sh)_{n+1}=a_n h_n, as stated. Positivity of the
real coefficients a_n also removes a possible complex-conjugation issue.
For h supported in coordinate n, the two powers multiply it by

\[
v_+=\left(\frac{\rho_n}{\rho_{n+d}}\right)^{1/p},
\qquad
v_-=\left(\frac{\rho_n}{\rho_{n-d}}\right)^{1/p}.
\]

If the measurable set {v_+<2 and v_-<2} has positive measure, one of its
countably many subsets
{v_+<=2-1/k and v_-<=2-1/k}, k>=1, has positive measure. Use its indicator
in that coordinate. For finite q the indicator is in L^q since W has
finite measure; for q=infinity its norm is exactly 1. Both adjoint-power
norms are at most (2-1/k)||h||, violating Lemma 2.1.

Consequently max(v_+,v_-)>=2 almost everywhere. Rearrangement gives the
candidate's density condition with eta=2^{-p}. In fact the same lemma
excludes a positive-measure set where both factors are <=2, but the proof
does not need this stronger formulation. The nonstrict density inequality
in (1.5) is therefore valid. Taking the countable union over n gives one
exceptional null set. The value d is chosen once at the operator level,
before localization, and is uniform over all fibers.

## 6. Full-theorem reconstruction and boundary checks

The remainder of the forward implication is consistent with the audited
duality step. Assign A_0 using the left drop and C_0 as its complement.
At n in A_0, a right drop at n-d would imply
rho_n<=eta rho_{n-d}<=eta^2 rho_n, impossible for positive rho_n and
eta<1. Thus the left drop propagates indefinitely. On C_0 the right drop
is forced; membership of n+d in A_0 would give the same contradiction.
Equality at a drop, including a point where both directions drop, causes
no gap: such a point is assigned to A_0.

Since B maps supports by the invertible coordinate permutation n maps to
n-1, the bands M_0,C_0 have the stated d-step invariance and contraction.
Intersecting B^j M_0, 0<=j<d, gives a closed measurable support band M.
Its support A satisfies tau A contained in A. Its complementary band N
therefore satisfies tau^{-1}A^c contained in A^c. The finite union of
supports of B^jN_0 is exactly A^c; splitting that union into disjoint pieces
gives the asserted algebraic sum equality, without a closed-sum assumption.

On each piece, conjugating the backward d-step estimate by B^j costs at
most D=max_{0<=j<d}||B^j||||B^{-j}||. The images of different pieces
remain disjoint, so the pth powers of their L^p norms add. This includes
p=1 and yields ||B^{-md}|_N||<=D eta^{m/p}. Finally, the finitely many
remainder powers in k=md+r give uniform exponential bounds with rate
eta^{1/(pd)}<1. No arbitrary power-splitting theorem is invoked.

Trivial bands are legitimate. For example, rho_n=2^n makes A_0=Omega
with d=1, eta=1/2, so M=E and N=0. The opposite density slope gives
M=0 and N=E. The zero restriction is read through its trivial norm decay.
The projection on any nonzero support band has norm 1, and the zero-band
projection has norm 0, exactly as qualified in the candidate.

For real spaces, the spectral-radius language is understood through the
usual complexification, or equivalently the norm-growth formula for powers.
Uniform decay follows in either interpretation. Given decay rate alpha<1,
choose gamma in (alpha,1), put

\[
|m|_M=\sup_{j\ge0}\gamma^{-j}\|T^j m\|,
\qquad
|n|_N=\sup_{j\ge0}\gamma^{-j}\|T^{-j}n\|,
\]

and equip E=M direct-sum N with |m+n|=|m|_M+|n|_N. This is an equivalent
norm, with |Tm|_M<=gamma|m|_M and |T^{-1}n|_N<=gamma|n|_N. It verifies
the one-step-renorming assertion even though P,Q need not commute with T.

## 7. Green formula with noncommuting projections

Independently of the composition setting, assume the full topological
direct sum in (1.3). Its complementary projections P,Q are bounded,
P+Q=I, and their ranges are M,N. Closedness and complementarity also
imply this boundedness via the closed graph theorem. The restrictions
need not be onto their respective bands.

For some C>=1 and alpha in (0,1), their nonnegative powers have norm at
most C alpha^j. If beta=||b||_infinity, the candidate's Green series have
term bounds C alpha^j||P|| beta and C alpha^{j+1}||Q|| beta. They converge
absolutely and uniformly in n, and

\[
\|y\|_\infty\le
K_G\|b\|_\infty,
\qquad
K_G=\frac{C(\|P\|+\alpha\|Q\|)}{1-\alpha}.
\]

For the common truncation through j=J, expanding the difference yields
the exact identity

\[
y_{n+1}^{(J)}-Ty_n^{(J)}
=b_n-T^{J+1}Pb_{n-1-J}-T^{-J-1}Qb_{n+J+1}.
\]

The two residual norms are bounded by
C alpha^{J+1}(||P||+||Q||) beta, uniformly in n. Boundedness of T permits
passage through the norm limit. The only identity used on the middle
term is P+Q=I. Projections are never passed through T. This explicitly
verifies the candidate's sentence about commutation after (6.1).

For an actual noncommuting example on ell^p(Z), take
(Tx)_n=w_n x_{n+1}, with w_n=1/2 for n<0 and w_n=2 for n>=0.
Let M be coordinates n<=0 and N coordinates n>=1. Forward powers on M
and backward powers on N have norm 2^{-j}. But PT e_1=2e_0 while
TP e_1=0. Thus this is a genuine noncommuting test, not a diagonal example.
The formula works on it, as proved analytically and probed exactly below.

Existence, not uniqueness, is what is needed. The same shift has bounded
nonzero homogeneous orbit T^n e_0 with norm 2^{-|n|}. The candidate never
asserts uniqueness of the bounded forced solution. Formula (6.1) is a
bounded right inverse of the difference operator, not necessarily an inverse.

## 8. Falsifiable probes and material assumption tests

The standard-library program `adversarial_probes.py` uses exact rational
arithmetic. A successful run recorded in `probes_result.json` checks:

- 77 finite adjoint-orbit segments of a nondiagonal invertible rational
  matrix, including positive and negative a,b and single-coordinate segments;
- 168 finite Green truncation identities on the noncommuting shift above,
  with both support bands and multiple forced times present;
- 48 explicit witnesses to failure of uniform fiber constants;
- an L^infinity example where two global norms mask a bad positive-mass
  fiber and its localized indicator exposes that fiber.

The Green probe also checks the full recurrence for finite-support forcing
after all time-supported terms are included, and checks the bounded
homogeneous orbit. The probes corroborate indexing and counterexample
diagnostics; no finite computation is being substituted for the derivations.

The uniform-fiber test has a complete analytic realization. Let
X=N_{>=1} times Z, f(i,n)=(i,n+1), and

\[
\mu(\{(i,n)\})=2^{-i}(1+1/i)^n.
\]

This is sigma-finite, W=N_{>=1} times {0} has mass 1, and both measure
bounds hold with c_+=2,c_-=1. The densities are rho_n(i)=(1+1/i)^n.
Each individual normalized fiber is a strict contraction, hence has
shadowing. Nevertheless, for fixed d, the smaller density quotient
(1+1/i)^{-d} tends to 1 as i increases. It violates every common eta<1.
Every atom has positive measure, however small, so none can be dismissed
in an essential supremum. The adjoint on an indicator of that atom has
power factors (1+1/i)^{d/p} and its reciprocal, whose maximum tends to 1.
Lemma 2.1 therefore excludes shadowing of the complete operator. This
confirms that the proof is correctly using operator-level uniformity rather
than an invalid fiberwise shadowing argument.

For the density boundary eta=1, take rho_n=1 and the unweighted bilateral
shift A. The forcing b_j=A^{j+1}e_0 is bounded. Any solution would satisfy
A^{-j}y_j=y_0+j e_0, so ||y_j|| grows at least |j|-||y_0||. Thus no bounded
solution exists. Correspondingly, (E) would demand arbitrarily long sums
of the constant a_0 be bounded by 2Ka_0. The strict eta<1 hypothesis is
material and has not been weakened in the proof.

For the spectral-radius boundary <=1, T=I on a nonzero scalar Banach
space and constant forcing b_j=1 gives y_j=y_0+j, again unbounded.
For missing complementarity, M=N=0 would make the four displayed
invariance/decay conditions vacuous for T=I; the candidate explicitly
requires the complete direct sum and avoids this failure.

The candidate excludes p=infinity. At that endpoint the L^infinity dual
need not be represented by scalar L^1, and the stated proof would not
apply. The finite-p claim, including p=1, does apply. This is a scope
boundary, not a defect in the stated target theorem.

## 9. Optional exposition repairs and final assessment

No mathematical repair is required by this family. The following small
clarifications would make independent checking easier:

1. At lines 89–94, display one explicit scaling such as
   c=delta_0/(2||b||_infinity), K=2/delta_0, and the backward recursion.
2. At lines 114–119, state the two residual coordinates -b and -a+1
   explicitly, with values -S^{b+1}u and S^a u.
3. At lines 327–345, state K_G and the finite-tail identity above, and
   specify b_n=x_{n+1}-Tx_n before subtracting y_n.
4. If real spectral language is retained, one parenthetical phrase can
   identify the standard complexification/norm-growth convention.
5. Write d in N_{>=1} in the density criterion; its coordinate indices and
   every subsequent construction already treat d as a positive integer.

These are optional completeness/exposition recommendations. Their absence
does not invalidate the existing derivations.

**Strongest verified result:** under (1.1)–(1.2), the complete argument
proves the advertised equivalence on scalar real or complex L^p for every
fixed 1<=p<infinity, with complementary measurable support bands in the
forward implication. Lemma 2.1 and the Green construction work on arbitrary
real or complex Banach spaces under their explicit hypotheses. The density
localization remains valid at p=1.

**Remaining mathematical gap within this audited scope:** none found.
**Outside-scope remaining questions:** independent priority/literature
assessment and publication claims, which require their own source audit.
