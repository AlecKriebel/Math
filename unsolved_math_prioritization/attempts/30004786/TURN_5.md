# Author turn 5: finite boundary defects suffice

**A weaker sufficient analytic hypothesis, with explicit Mellin poles and the remaining original gap.** This final author route allows a finite boundary correction instead of exact theta inversion. It proves a conditional continuation/functional-equation theorem, but does not derive its boundary hypothesis from the source's bare weak functional premise.

## 1. Average over the compact norm-one idele classes

Retain the number field, local transfer, source normalizations and uniform growth assumptions of turn 1. Choose the same multiplicative norm section a(r). Disintegrate the quotient Haar measure on C_k=k×\\A× as dc dr/r, where dc is its induced Haar measure on the compact norm-one subgroup C_k^1. Keep this normalization fixed on both sides.

For the chosen pure tensor phi and its Fourier transform define

A(r)=integral_(C_k^1) Theta_phi(c a(r)) dc,

A_dual(r)=integral_(C_k^1) Theta_(F phi)(c a(r)) dc.

Both are continuous and decrease faster than every inverse power at infinity by the uniform estimate in turn 1. Inversion preserves dc. Define their actual averaged theta defect

B(r)=A(r)-A_dual(1/r).                         (1)

This is a definition involving actual theta sums, not an arbitrary Poisson functional. The reverse defect, formed from this same pair, is identically

B_reverse(r)=A_dual(r)-A(1/r)=-B(1/r).         (2)

No unproved Fourier-square scalar assertion is needed for (2): it simply exchanges the two displayed functions.

### Finite-defect hypothesis

Assume, for this one permitted tensor with nonzero Mellin multiplier, that for every r>0

B(r)=sum_(lambda,m) c_(lambda,m) r^lambda (log r)^m,   (3)

a finite sum with lambda in C and m nonnegative integers. The coefficients and exponents may depend on phi. Coincident exponents can be grouped. Condition (3) is strictly a sufficient extra analytic hypothesis, not a conclusion of OWR Conjecture1.3. Exact restricted theta inversion is its zero-defect special case.

## 2. Elementary meromorphic Mellin lemma

Put z=s-1/2 and define the upper-tail transforms

H(z)=integral_1^infinity A(r) r^z dr/r,

H_dual(z)=integral_1^infinity A_dual(r) r^z dr/r.

They are entire, since rapid decay is uniform on compact z-sets and allows every logarithmic derivative. For Re(z) sufficiently large, equations (1) and (3) give

Z(z)=integral_0^infinity A(r)r^z dr/r
    =H(z)+H_dual(-z)+J_B(z),                  (4)

where

J_B(z)=sum_(lambda,m) c_(lambda,m) (-1)^m m!/(z+lambda)^(m+1).   (5)

Indeed the lower integral of r^(z+lambda)(log r)^m is the m-th derivative of 1/(z+lambda). The transformed A_dual(1/r) term becomes H_dual(-z). Thus (4) meromorphically continues Z to the plane, with possible poles only at z=-lambda of order at most m+1 after grouping terms.

For the dual function, apply the same splitting in its own initial right half-plane using (2). Its continued transform at -z is

Z_dual(-z)=H_dual(-z)+H(z)+J_(B_reverse)(-z).

A term c r^lambda(log r)^m in B contributes
-c (-1)^m r^(-lambda)(log r)^m to B_reverse. Formula (5) gives

J_(B_reverse)(-z)=J_B(z).                     (6)

Therefore the two meromorphic continuations satisfy

Z(z)=Z_dual(-z),

or, with the source half shift restored,

Z_global(s,phi)=Z_global(1-s,F phi).           (7)

The initial convergence half-planes need not overlap; equations (4)–(6) explicitly construct both continuations and compare them. No divergent full-line integral of a power-log term is assigned a value, and no missing overlap is used as an identity theorem.

## 3. Consequence for the completed L-functions

Use the same two-finite-place tensor and finite nonzero meromorphic multiplier P_phi(s) as in turn 1. In the original convergence half-plane, unfolding identifies Z_global(s,phi)=L(s,sigma,rho)P_phi(s). Equation (4) gives meromorphic continuation, and division by P_phi is legitimate as an identity of meromorphic functions. The dual side is handled identically.

The local functional equations give P_(F phi)(1-s)=epsilon(s,sigma,rho)P_phi(s). Cancelling this nonzero multiplier from (7) proves the completed L-function functional equation with the source epsilon normalization. Division can introduce further poles, so the pole list in Section 2 is asserted for this global test-function integral, not as a final classification of automorphic L-function poles. No entire-L or vertical-growth theorem is claimed.

This is the classical finite-boundary Mellin splitting mechanism written for the source's half-shifted spaces. It is a credited analytic method, not a novelty claim.

## 4. A concrete way an additional boundary hypothesis could imply (3)

Suppose weak Poisson functionals E and E_dual are given, and their idele-translation orbits are continuous so they may be averaged over C_k^1. Define

D_phi(r)=integral_(C_k^1) E(R_(c a(r))phi) dc - A(r),

D_dual(r)=integral_(C_k^1) E_dual(R_(c a(r))F phi) dc - A_dual(r).

Fourier covariance, the weak intertwining identity, and Haar inversion on C_k^1 give

B(r)=-D_phi(r)+D_dual(1/r).                   (8)

If each of these two continuous functions of t=log r lies in a finite-dimensional translation-invariant subspace of C(R), then each is an exponential polynomial in t. Here is the needed finite-dimensional fact: on such a subspace, translation is a continuous representation of the additive real group, hence exp(tT) for a fixed complex matrix T. Evaluating at zero and using the Jordan normal form produces finite sums e^(lambda t)t^m. Continuity of the representation follows by choosing finitely many evaluation points separating the finite-dimensional function space, which identify it with a finite-dimensional coordinate space. Thus (8) implies (3).

This gives a sharply stated finite-dimensional boundary-module route. The assumption concerns actual differences between the functionals and theta averages, not the arbitrary functionals alone. The source's bare weak premise supplies neither this finite-dimensionality nor a corresponding asymptotic expansion.

## 5. Why the finite-module route is not already automatic

The weak functionals constructed in turns 2 and 4 have single-power or two-power averaged norm orbits. For a permitted phi with a nonzero right-half-plane global Mellin evaluation, A(r) is not identically zero: otherwise unfolding its absolutely convergent Mellin integral would give zero. Yet A(r) is rapidly decreasing at infinity.

A nonzero exponential polynomial in t cannot decrease faster than exp(-M t) as t→infinity for every M. For example, take the terms with maximal real exponent and then maximal polynomial degree. Their leading trigonometric polynomial has positive long-interval mean square unless all its coefficients vanish, so it cannot have arbitrary exponential decay; repeat if necessary. Therefore this nonzero A(e^t) is not an exponential polynomial.

For these constructed weak functionals, a finite-dimensional translation module for D_phi would force A(e^t) to be an exponential polynomial, by subtracting D_phi from their finite-power orbit. This is impossible. Hence that additional boundary-module condition is genuinely absent from weak functional invariance and coherent self-duality alone.

This does not prove that the actual defect B of the arithmetic theta pair fails (3): non-finite-dimensional pieces of the two D functions might cancel in (8), and genuine arithmetic input might establish a finite defect directly. It shows only that the proposed finite-dimensional control is an additional statement requiring proof, rather than a formal consequence of the weak construction.

## 6. Five-turn disposition

Five substantive author turns are now complete. Verified conditional deductions give three levels of sufficient input:

1. genuine restricted theta inversion;
2. bilateral agreement of the Poisson functionals with theta on the restricted space, which yields level 1;
3. a finite power-log defect of the averaged theta pair for one nonzero-Mellin tensor, which also yields continuation and the functional equation.

The weak-functional transport and coherent/self-dual constructions explain why the printed existential premise alone does not provide these inputs in the Mellin argument. They are not counterexamples to an actual automorphic L-function conjecture.

The original source-scoped implication remains **unsolved, 5/5 substantive author turns**. The missing step is to obtain the needed canonical theta normalization or finite analytic boundary control from the actual conjectured functional statement and arithmetic data, without simply assuming a refined Poisson formula or global functoriality. Completion estimate 45%, reflecting scoped analytic progress rather than a probability of resolving the general conjecture. Freeze for independent source-and-proof review before any result PR.
