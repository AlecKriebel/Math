# Author turn 4: the self-dual and coherent-pair weak premises

**A stronger formulation obstruction, still not a counterexample to the automorphic L-function conclusion.** This turn tests whether requiring the same functional in a self-dual case, or requiring compatible identities in both dual directions, repairs the weakness found in turn 2.

## 1. The exact compatibility scalar

Write F:V→W for the adelic Fourier operator and G:W→V for the opposite-representation operator with the same additive character. Turn 3, using the source's actual fiber normalization, gives

GF=kappa R_b on V, and FG=kappa R_b on W,

where b=(-1)^n is principal and kappa=product_v omega_(pi_v)(-1). Each factor is ±1 and almost all are 1. The dual central-character value at -1 is the same, so the scalar in the reverse order is also kappa. No automorphy of the transferred pi is being assumed.

On k×-invariant linear functionals, precomposition with R_b acts as the identity. Thus precomposition by the Fourier square acts by the scalar kappa.

If E_V=E_W F and E_W=E_V G are both required and E_V is nonzero, then

E_V=E_V GF=kappa E_V,

so kappa must be 1. In the self-dual case V=W with F=G and a single E=EF, the same necessity follows. This detects a central-character compatibility condition, not a Mellin continuation theorem.

The analysis below is explicitly conditional on kappa=1. For a genuinely automorphic transfer pi this holds by its central character's triviality on k×. A more general deduction from local transfer of sigma requires the appropriate central-character compatibility in local Langlands theory; it is not silently inferred here from the bare existence of the local representations. No example violating this compatibility under all of the original automorphic hypotheses is claimed.

## 2. Nonzero symmetrized functionals

Choose a real s0 sufficiently large for the convergent adelic zeta evaluations on both V and W, and put a=s0-1/2>0. Let ell_V and ell_W be these nonzero evaluations as in turn 2. Their idele-translation law is

ell_V R_x=|x|^(-a) ell_V,    ell_W R_x=|x|^(-a) ell_W.

Fourier covariance gives the opposite character for their transforms:

(ell_W F)R_x=|x|^a ell_W F,    (ell_V G)R_x=|x|^a ell_V G.

Define

E_V=ell_V+ell_W F,    E_W=ell_W+ell_V G.       (1)

Both are k×-invariant. Under kappa=1, invariance under the principal b gives

E_W F=ell_W F+ell_V GF=ell_W F+ell_V=E_V,

and likewise E_V G=E_W. Thus they solve both compatible weak identities.

Neither functional vanishes. Indeed the two summands in each expression are nonzero and transform by the distinct positive-norm characters r^(-a) and r^a. If their sum were zero, translating by an idele of norm r≠1 and subtracting r^a times the alleged zero identity would force ell_V=0, a contradiction. The same argument applies to W. This uses the surjectivity of the idele norm onto positive reals and does not evaluate a divergent Mellin integral.

For a self-dual representation, the scalar function spaces and Fourier constructions are identified. Taking the same zeta evaluation on the two identical spaces makes (1) the single functional

E=ell+ell F.

It is nonzero and EF=E. Therefore the self-dual single-functional interpretation does not by itself impose theta normalization when its necessary scalar compatibility holds.

## 3. Domain, continuity, and theta mismatch

All functionals act on the algebraic restricted tensor-product spaces used in turns 1–3. Explicit controlling seminorms are

p_V(phi)+p_W(F phi),    p_W(eta)+p_V(G eta),

where p is the corresponding absolutely convergent weighted-L1 seminorm at s0. Hence the sums are continuous for these specified seminorms. No assertion is made about an unspecified stronger completed topology or an externally imposed distribution class.

For any phi, the norm orbit of E_V is

E_V(R_x phi)=r^(-a) ell_V(phi)+r^a ell_W(F phi), r=|x|.

Whenever ell_V(phi)≠0, this cannot have decay faster than every inverse power as r→infinity: either the second coefficient is nonzero and there is growing r^a behavior, or it is zero and the nonzero r^(-a) term remains. These are distinct real powers, so no large-r cancellation can remove both.

Such a phi can be chosen in the restricted double-circle test space. Use a compact local factor at one finite place and the inverse Fourier transform of a compact factor at another finite place, as in turn 1. The associated local Mellin factors are nonzero meromorphic functions. Choosing sufficiently large real s0 away from their discrete zero or pole sets makes ell_V(phi) nonzero; choose s0 before defining (1). The same common positive half-plane is available for both spaces. In the self-dual case this gives the same conclusion for the single functional.

Actual theta sums on this subspace have the rapid large-norm decay proved from the source estimates in turn 1. Thus these coherent weak functionals cannot automatically be substituted for theta evaluation. Adding compatibility across the dual pair removes neither the need for theta normalization nor the analytic input it supplies.

## 4. Outcome and remaining target

This turn closes the self-duality loophole in the earlier transport objection: under the explicitly necessary scalar condition, nonzero coherent functionals can still be fabricated from right-half-plane zeta evaluations. If the scalar condition fails, the coherent weak premise is inconsistent rather than analytically informative.

The construction does not show that any genuine automorphic L-function lacks continuation or a functional equation. It does not supply a countermodel satisfying the full arithmetic source hypotheses and a false analytic conclusion. It establishes that weak invariance, Fourier covariance, self-dual identification, and two-direction consistency do not identify the particular theta functional needed by the Mellin proof.

Four substantive author turns complete. The original implication remains unresolved. Completion estimate 40%. The fifth route will test a precisely weaker analytic boundary-control hypothesis, to isolate whether a manageable finite-dimensional correction to theta agreement could replace exact bilateral normalization.
