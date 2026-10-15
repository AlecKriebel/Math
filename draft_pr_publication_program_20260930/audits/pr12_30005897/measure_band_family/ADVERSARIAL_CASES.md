# Boundary and counterexample attempts

These cases were constructed independently of candidate verification code.
`stress_checks.py` uses exact integer logarithms and rational powers of two;
its finite assertions check specified formulas and do not constitute a proof
of the universal theorem. The complete derivation is `DERIVATION.md`.

## A. A nontrivial composition example without bounded distortion

Let W=N_0 with nu({k})=2^(-k-1), X=W×Z, and

    mu({(k,n)}) = nu({k}) rho_n(k),
    rho_n(k) = 2^(k-|n-k|),
    f(k,n)=(k,n+1).

At n=0, rho_0=1 and mu(W×{0})=1. This is a sigma-finite space and a
bijective bimeasurable dissipative system. Adjacent density ratios lie
in [1/2,2], so mu(fA)<=2mu(A) and mu(f^-1A)<=2mu(A) for every A.
For every k,n,

    min(rho_(n-1)(k),rho_(n+1)(k)) = (1/2)rho_n(k).

Thus d=1 and eta=1/2 work uniformly, despite the peak locations k being
unbounded over W. The candidate bands are exactly n<=k and n>k. The
normalized shift has forward decay 2^(-j/p) on the first and inverse decay
2^(-j/p) on the second. The original composition operator therefore has
two-sided shadowing for every finite p>=1 by the explicit Green-series
construction.

Yet for n>=0 the range of rho_n over W has infimum 2^-n (at k=0) and
supremum 2^n (at every k>=n), a ratio 2^(2n). Any bounded-distortion
constant comparing each fiber density to its level average would need
at least a growing multiple of 2^n. In fact the exact level masses are

    mu(f^n W) = 2^n                      (n<=0),
    mu(f^n W) = 3/2 - 2^(-n-1)           (n>=0).

The positive-tail aggregate masses tend to 3/2, although the operator
has shadowing. This is a verified stress example, not a priority claim.
It demonstrates concretely why a uniform fiber cut need not have a
bounded location and why aggregate-mass intuition is unreliable here.

## B. Genuinely different cuts in different residue classes

Fix d>=2. For r=0,...,d-1, integers k_r and offsets e_r define

    h_(r+dq) = -|q-k_r| + e_r,
    rho_n = 2^(h_n-h_0).

Each residue is a tent, so d,eta=1/2 satisfy the condition at every n.
Its A0 membership is q<=k_r, with residue peak n_r=r+d k_r. The finite
intersection of all unit shifts is exactly

    A = {n<=min_r n_r}.

Indeed for any n<=min n_r, the first coordinate of every residue at or
after n lies no later than that residue's peak; for n>min n_r, the first
coordinate of the earliest-peak residue is already outside A0. The
complement is a final ray. Thus different residue cuts do not spoil
unit-step invariance.

The test families allow a common fiber translation ranging to ±10,000
residue steps and relative cuts chosen independently within ±20 steps,
plus variable offsets. An explicit uniform adjacent log bound is

    L = max_r (|k_r-k_(r+1)|+|e_r-e_(r+1)|+1),

where the residues wrap cyclically. This bounds both B and B^-1, and the
independent finite-union proof gives the uniform block inverse factor
D^p<=2^(2L(d-1)). Exact checks verify that estimate beyond and between all
residue peaks, including the potentially expanding intermediate zone.

## C. Unbounded relative residue cuts are an invalid counterexample

For parity tents h_(2q)=-|q-A|+e and h_(2q+1)=-|q-B|+e', the differences
on far left and far right tend to e-e' ±(A-B). Any uniform adjacent log
bound must bound both values, so it must be at least |A-B|. Making the
relative peaks separate without bound across fibers loses boundedness of
B or B^-1; adjusting the offsets cannot repair both tails simultaneously.

More generally the source-independent subaudit proves

    |t_r-t_s| <= 1 + |r-s| log Q/(-log eta)

for growth/decay thresholds of any admissible residue sequences with
uniform neighboring ratio Q. A finite threshold cannot coexist with an
infinite threshold; opposite infinite thresholds cannot coexist. These
facts independently rule out the intended mixed-residue obstruction.

## D. Fiberwise shadowing without uniform constants really fails

Let W=N with any finite positive atomic measure and

    rho_n(k)=2^(-|n|/k), k>=1.

Adjacent ratios are uniformly between 1/2 and 2. Every individual fiber
is a generalized-hyperbolic tent shift, but its decay rate approaches 1
as k→infinity. For any proposed d and eta<1,

    min(rho_-d(k),rho_d(k))/rho_0(k)=2^(-d/k)→1,

so no common density condition holds. Also, choose the dual indicator at
level zero on an atom k large enough that 2^(d/(kp))<=2. Both d-th dual
iterates then have norm at most twice the input norm. This contradicts
the necessary uniform estimate derived from shadowing. Hence the whole
Lp operator has no shadowing, even though every fiber does. The
localization proof correctly excludes this tempting weakening.

The script checks the especially transparent eta=1/2 case by choosing
k=2d for every tested d. The limiting formula proves failure for every
d and every eta<1, not only the finitely tested pairs.

## E. Constant or flat tails

If rho_n(w) is constant along a positive-measure fiber set for arbitrarily
long positive or negative tails, take n far enough into that tail that
both n±d remain constant. The density condition fails there for every
eta<1. The dual indicator test has both iterate norms exactly equal to
the input norm, contradicting shadowing's necessary estimate. No choice
of a moving band boundary repairs a genuinely infinite flat tail of
positive measure.

A plateau of finite length can be compatible with some larger d;
uniform shadowing then requires the plateau lengths and other constants
to have a common bound. An unbounded family of plateau lengths has the
same localized obstruction to any common d.

## F. Nonseparable sigma-finite p=1 example

Let W={0,1}^I for an uncountable index set I with product Bernoulli
probability measure and product sigma algebra. L1(W) is nonseparable:
the coordinate indicators for distinct indices have pairwise L1 distance
1/2. Choose one coordinate i_0 and put J(w)=w_(i_0) in {0,1}. Define

    rho_n(w)=2^(|J(w)|-|n-J(w)|).

These are measurable positive densities, rho_0=1, neighboring ratios
are between 1/2 and 2, and d=1,eta=1/2 work. Form X=W×Z with density
rho_n at level n and f shifting upward. It is sigma-finite, W at level
zero has finite positive measure, and the uniform stable/unstable split
is n<=J(w) and n>J(w). The proof works at p=1 on this nonseparable space;
scalar L1*=L∞ is the only dual identification required. The construction
neither assumes nor produces a separable model of W.

## G. Null sets and common exceptional sets

A single bad fiber of nu-measure zero contributes zero product measure
when crossed with Z. Its orbit images are also mu-null by bounded
nonsingularity. Modifying densities there or discarding it changes
neither the represented operator nor a support band in Lp. Conversely,
one cannot discard a positive-measure bad fiber set; localization detects
it by an indicator. Countability of the coordinate indices makes a
common exceptional set legitimate even when W's sigma algebra is not
countably generated.

## H. Both-direction drops, equality, empty bands, and scalar field

At a tent peak both neighbors can drop by exactly eta. Assigning the
point to A0 yields forward propagation; assigning the complementary
points to C0 yields inverse propagation. The contradiction establishing
propagation is 1<=eta^2, so equality at the allowed drop boundary does
not weaken it.

For rho_n=2^n, A0=A=Omega and N=0; B is globally contracting. For
rho_n=2^-n, M=0 and N=E; B^-1 is globally contracting. The theorem's
definition permits both legitimate zero-band cases. Norms and spectra
on the zero space can be handled by the convention r=0, or simply by the
uniform-decay definition, avoiding a convention issue.

Positive coefficients preserve disjoint supports for arbitrary real or
complex inputs. Tests include inputs with modulus five, realizable by
3+4i as well as by 5, and exact p-th moments for p=1,2,3,8. No positivity
of test vectors and no Hilbert-space orthogonality enter the proof.

## I. Unit-circle eigenvectors do not falsify this theorem

The finite-measure model rho_n=2^-|n| has the constant original function
as a T-eigenvector of eigenvalue 1, yet its lower/upper bands give
uniform decay in the prescribed different time directions. Generalized
hyperbolicity does not require both complementary bands to be invariant
under T in both directions. The eigenvector decomposes across bands;
neither component is individually fixed.

One can see directly why a constant forcing is solvable: the coordinate
function n belongs to Lp of this exponentially weighted finite measure,
and phi∘f-phi=1. Thus an argument that merely discovers a unit-circle
eigenvalue transfers the problem to an invalid hyperbolicity requirement.
It is not an obstruction to the stated generalized-hyperbolic conclusion.

## Status and exact limits

No counterexample or missing assumption was found for the exact
1<=p<infinity, bounded invertible, dissipative claim. The separate
source-independent residue-threshold derivation also verifies the scalar
splitting proposition. The recorded computations are exact and
reproducible but finite. This family does not assess bibliographic
priority, source-paper scope, or publication readiness outside the
mathematical proof obligations assigned to it.
