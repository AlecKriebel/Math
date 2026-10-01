# Independent measure and band reconstruction

Exact candidate: PR12 head `19dfaccb52a7640eec79af28a778b4f22f93479a`.
The inspected `source_snapshot/PROOF.md` has SHA-256
`f38ae2dd97bb2aeb8f1e97da0f4133b84b6d43d803e2b38df2c91acc56817a8e`.
This reconstruction was written without reading the preserved reviewer,
`verify.py`, or candidate verification output. The target/source record and
exact source proof were read. No priority conclusion is attempted here.

## Exact claim and success criterion

Let f be a bimeasurable bijection of a sigma-finite measure space, with
mu(fA)<=c_+ mu(A) and mu(f^-1 A)<=c_- mu(A) for finite constants. Let W
have positive finite measure and have disjoint iterates covering X modulo
null sets. Fix a scalar real or complex Lp with 1<=p<infinity.

The claim is the equivalence of: (i) two-sided shadowing for T phi=phi∘f;
(ii) a closed complementary splitting M⊕N, TM⊂M and T^-1N⊂N, on which
forward and inverse powers respectively decay uniformly exponentially;
(iii) a common integer d>=1 and eta in (0,1) such that

    min(rho_(n-d)(w), rho_(n+d)(w)) <= eta rho_n(w)

for all integer n and all w outside one measurable nu-null set, where
nu=mu|W, nu_n(A)=mu(f^nA), and rho_n=d nu_n/d nu. In (ii) M,N may be
chosen as measurable support bands. The audit succeeds only if every
implication is uniform over the entire measure space and accommodates
p=1, nonseparable Lp, moving fiber cuts, distinct residue cuts, and zero
bands. Finite computation is corroboration; it cannot replace these
quantified implications.

## 1. Measure-theoretic prerequisites

The constants c_+,c_- are positive in the nonzero system. Iterating the
inequalities gives finite constants C_n such that nu_n<=C_n nu and
nu<=C_-n nu_n. In particular nu_n is a finite measure and is equivalent
to nu. Radon–Nikodym yields positive finite rho_n almost everywhere.
The inequalities nu_(n+1)<=c_+nu_n and nu_n<=c_-nu_(n+1) give

    1/c_+ <= rho_n/rho_(n+1) <= c_-.

Choose measurable versions of the densities and remove the union of their
countably many exceptional sets; every inequality is then simultaneous.
Nothing requires a countably generated sigma algebra or separability.

For complete precision, the modulo-null wandering decomposition can be
replaced by an exact decomposition of a conull invariant subset. Remove
from W the measurable null union of W∩f^kW over all nonzero integers k.
Call the remainder W'. Its iterates are literally pairwise disjoint.
Their union X' is invariant under f and f^-1 and conull: removal has only
removed the countable union of f^n(W\W'), which is null by the two
nonsingularity inequalities. Restricting to X',W' does not change Lp or
any densities modulo null sets. This is routine unpacking of the source's
"up to a null set" convention, not a missing mathematical hypothesis.
A null exceptional fiber set subsequently removed also has a null union
of orbit images, by the same argument.

## 2. The isometric representation and adjoint

For a measurable phi, define

    (U phi)_n(w) = rho_n(w)^(1/p) phi(f^n w).

For each n the pushforward definition of nu_n gives

    integral_(f^n W) |phi|^p dmu
      = integral_W |phi(f^n w)|^p rho_n(w) dnu.

Summing this identity over n proves isometry into the scalar product-space
Lp(W×Z,nu×counting). In particular Tonelli is being used for a nonnegative
countable sum, with no separability assumption. Given any scalar Lp
function g on the product, set

    phi(x) = rho_n(f^-n x)^(-1/p) g_n(f^-n x),  x in f^n W.

Each piece is measurable, the partition is countable, and the preceding
identity proves its norm and membership. Positive finite densities ensure
the inverse formula is valid almost everywhere; choices on null sets do
not change either equivalence class. Thus U is onto.

Direct substitution, including the indices, gives

    (Bg)_n = a_n g_(n+1),  a_n=(rho_n/rho_(n+1))^(1/p).

The a_n are positive, bounded above, and bounded away from zero uniformly.
The support map is the measurable permutation tau(w,n)=(w,n-1). Both B
and B^-1 preserve disjointness of supports, and B Lp(F)=Lp(tau F) for every
measurable F, exactly modulo null sets. This is why complementation and
finite intersection commute with B; a general bounded operator would not
have those properties.

Scalar Lp duality on this sigma-finite product gives E*=Lq, including
L1*=L∞. The p=1 identification is valid for nonseparable L1: a bounded
functional defines compatible absolutely continuous signed/complex
measures on a countable finite-measure exhaustion; their RN densities
patch to an essentially bounded scalar function. No Bochner duality or
measurable selection in a nonseparable fiber is involved. A real dual
pairing, or the complex pairing with the appropriate conjugation, gives
because a_n is real and positive

    (B* h)_(n+1)=a_n h_n.

For h supported at level n, the factors in (B*)^d and (B*)^-d are exactly
(rho_n/rho_(n+d))^(1/p) and (rho_n/rho_(n-d))^(1/p). Multiplying successive
weights telescopes and proves the formula for any integer n, including
negative coordinates and inverse powers. In the complex case the
conjugations leave these positive coefficients unchanged.

## 3. Pointwise localization is uniform

Assume the necessary Banach dual estimate

    max(||(B*)^d h||, ||(B*)^-d h||) > 2||h||,  h≠0,

with one fixed d. For a fixed coordinate n let F be a positive-measure
set on which both scalar factors are <2. The union over positive rational
epsilon of sets where both factors are <=2-epsilon is F, so one such
set F_epsilon has positive measure. Since nu(W)<infinity, the indicator
h=1_(F_epsilon) at level n belongs to every required Lq; for q=infinity
its norm is 1. Both output norms are <=(2-epsilon)||h||, a contradiction.
Hence their maximum is >=2 almost everywhere. Rearrangement gives the
common eta=2^-p. The countable union over n gives a common exceptional
set; there is no uncountable union over w.

Indeed one could directly forbid a positive-measure set on which *both*
factors are <=2, obtaining a slightly stronger pointwise statement. The
candidate's weaker >=2 conclusion is sufficient, and its strict-epsilon
localization is correct. Operator norm lower bounds without quantifying
all test h would not permit this step, and fiberwise shadowing with
nonuniform constants would not permit one common d.

## 4. Power bands from the density condition

At good fibers put A0={(w,n):rho_(n-d)<=eta rho_n} and C0=A0^c.
For n∈A0, the density alternative at n-d cannot be the right drop
rho_n<=eta rho_(n-d), since together they imply 1<=eta^2.
Consequently n-d∈A0 and iteration yields

    rho_(n-md)<=eta^m rho_n, n∈A0.

For n∈C0 the condition forces rho_(n+d)<=eta rho_n. At n+d,
membership in A0 would imply rho_n<=eta rho_(n+d), again impossible.
Thus n+d∈C0 and

    rho_(n+md)<=eta^m rho_n, n∈C0.

A point with both left and right drops is assigned to A0; the left
propagation still works. Equality at the permitted eta boundary causes
no change because eta^2<1 is a strict contradiction. Positivity of rho_n
is essential here and has already been verified.

For g supported in A0,

    ||B^(md)g||_p^p
      = integral_W sum_n (rho_(n-md)/rho_n)|g_n|^p dnu
      <= eta^m ||g||_p^p.

For g supported in C0, replacing n-md by n+md proves the inverse bound.
These are input-coordinate formulas; confusing input n with output n-md
would reverse the coefficient, but the candidate does not do so. The
support propagation gives B^dM0⊂M0 and B^-dN0⊂N0 as well as decay.

## 5. Finite intersections repair unit-step invariance

Let A=intersection_(j=0,...,d-1) tau^j A0, M=Lp(A), N=Lp(A^c).
Equivalently,

    (w,n)∈A iff (w,n+j)∈A0 for every 0<=j<d.

If n∈A, the tests for n-1+j with 1<=j<d are among the tests for n.
For j=0, n-1=(n+d-1)-d belongs to A0 by d-step propagation. Thus n-1∈A:
BM⊂M. Complementation yields n∈A^c => n+1∈A^c, so B^-1N⊂N.
This direct coordinate proof independently checks the abstract
intersection identity in candidate lines 260–282.

Every fiber of A is a unit-step initial segment of Z, or all/none. Its
cut may depend measurably on w and be unbounded over W. No finite global
location of the cut is needed. Initial-segment measurability follows from
the measurable set A; it does not require choosing a measurable basis or
projecting an uncountable measurable family.

The complement is the union of tau^j C0, so

    N = sum_(j=0,...,d-1) B^j N0.

This equality is an actual closed support band, not merely the closure
of an abstract finite subspace sum. To verify, partition the finite union
into F_0=tau^0C0 and F_j=tau^jC0\union_(i<j)tau^iC0. Every g∈N decomposes
as the finite disjoint sum g_j=1_(F_j)g, and g_j∈B^jN0. The support
projections have norm <=1 (norm zero if the band is zero).

M⊂M0 gives forward block decay immediately. For g_j∈B^jN0,
commutation of integer powers gives

    ||B^(-md)g_j||
      <= ||B^j|| eta^(m/p) ||B^-j|| ||g_j||.

Let D=max_(0<=j<d)||B^j|| ||B^-j||. The g_j and their images under
B^-md are both disjointly supported, since B^-md is an invertible
weighted permutation. Therefore

    ||B^(-md)g||_p^p
       = sum_j ||B^(-md)g_j||_p^p
       <= D^p eta^m sum_j ||g_j||_p^p
       = D^p eta^m ||g||_p^p.

This identity includes p=1 exactly. It does not use Hilbert orthogonality,
positivity of g, or a commuting projection. The j are only finitely many,
so bounded invertibility of B gives finite D even for nonseparable W.

For k=md+r, 0<=r<d, set alpha=eta^(1/(pd)). The block bounds imply

    ||B^k|M|| <= C_M alpha^k,
    ||B^-k|N|| <= C_N alpha^k,

where C_M=max_(r<d)||B^r||alpha^-r and
C_N=D max_(r<d)||B^-r||alpha^-r. Both are finite. These are the exact
norm-decay properties requested by generalized hyperbolicity. In the
real case this avoids any ambiguity in defining spectral radius before
complexification; in either convention the rate is <=alpha. A zero M
or N meets the same bounds trivially. U^-1 preserves support bands and
transports all inclusions and estimates to T.

## 6. Whole-theorem reconstruction, including endpoints

For completeness the remaining two Banach steps were independently
checked, rather than treated as hypotheses.

Shadowing, at one fixed accuracy, provides a fixed forcing bound K by
scaling any bounded bi-infinite forcing and recursively constructing a
pseudotrajectory in both time directions using invertibility. Subtract
its shadowing exact orbit and scale back. For every finite dual sequence
u_j, choose independent unit-ball b_j approximating the real part of
u_j(b_j) to ||u_j||. The bounded forcing solution then gives

    sum_j ||u_j|| <= K sum_j ||u_(j-1)-A*u_j||.

No norm attainment or separability is involved. For S=A*,
u_j=S^-j u on -b<=j<=-a and zero elsewhere, interior terms vanish.
The boundary residuals are S^(b+1)u and S^a u, hence exactly

    sum_(j=a,...,b) ||S^j u|| <= K(||S^a u||+||S^(b+1)u||).

Taking [-j,j-1] yields ||u||<=K(||S^-j u||+||S^j u||).
If both endpoints at ±d were <=2||u||, [-d,d-1] bounds the whole sum
by 4K||u||, while summing the last inequality for j=1,...,d-1 bounds
its interior subset below by (d-1)||u||/K. This is impossible for
integer d>4K^2+1. The index b+1 in the endpoint, and the missing j=d
in the lower sum, have both been checked. This establishes the necessary
uniform dual estimate used above.

For the converse let M⊕N be any generalized-hyperbolic splitting and
P,Q its bounded complementary projections. Uniform norm decay makes

    y_n = sum_(j>=0) T^j P b_(n-1-j)
          -sum_(j>=0) T^(-j-1) Q b_(n+j)

uniformly absolutely convergent for every bounded b. Subtracting Ty_n
from y_(n+1) telescopes the first sum to Pb_n and the second to Qb_n;
no commutation of P or Q with T is needed. Its uniform bound permits
choosing a shadowing tolerance, and subtracting y from a pseudotrajectory
produces a true orbit for all integer times by invertibility.

Thus the audited claim is established as written. The endpoint p=infinity
is expressly excluded. The normalized weights do not give this theorem
there; in particular the limiting coefficient rho^(1/p) would be 1.
No extension to p<1, noninvertible T, a nonwandering complement of positive
measure, or unbounded B/B^-1 is licensed by this argument.
