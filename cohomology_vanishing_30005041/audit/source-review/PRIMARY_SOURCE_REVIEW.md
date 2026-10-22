# Primary-source review of the frozen cohomology checkpoint

Date: 2026-10-03

Verdict: PASS within the stated countable-discrete scope. No blocking source mismatch was found in Propositions 1–3 or Attempt 5. The full fixed-family interval problem remains unsolved in this checkpoint. This review establishes neither novelty nor present-day open-problem status.

## Sources actually inspected

- Mikael de la Salle, joint work with Amine Marrakchi, “Group actions on Lp-spaces: dependance on p,” Oberwolfach Report 11/2022, printed pp. 567–569. The question and relevant comparison were checked directly in the PDF at printed p. 568, PDF page 52.
- Amine Marrakchi and Mikael de la Salle, “Isometric actions on Lp-spaces: dependence on the value of p,” arXiv:2001.02490v3, dated 1 October 2020. Inspected the local text and PDF, especially printed pp. 4–5 and 8–11. The theorem numbering below is the v3 numbering.
- Frozen README.md, ATTEMPTS.md, SOURCES.md, and FROZEN_MANIFEST.json.

The journal version and the Lavy–Olivier paper were not present among the permitted local primary-source files, so this review does not independently certify their numbering or the frozen ledger’s separate bibliographic and literature-search claims. No online research or remote writes were performed.

## 1. Exact original target

OWR p. 567 specifies real-valued Lp spaces and continuous affine isometric actions of a topological group. On p. 568, a single continuous homomorphism

    sigma: G -> Aut(X,[mu]) semidirect L0(X,mu;{-1,1})

produces the family pi_(p,sigma). Question 1 asks whether the exponents for which H1(G,pi_(p,sigma)) vanishes form an interval.

Thus the frozen statement correctly holds fixed the underlying nonsingular action and the sign cocycle. The exponent varies over positive finite values. The family still has its prescribed Lamperti member at p=2; the fact that not all Hilbert-space isometries have Lamperti form does not allow replacing that member by a different representation.

OWR p. 568 explicitly distinguishes this question from the group-wide result in Theorem 3. That theorem constructs an action at a larger exponent, with matching powered displacement norms, but need not preserve the original linear representation. The frozen package preserves this distinction correctly.

## 2. Exact content and boundaries of Theorem 5.4

The arXiv v3 preliminaries, p. 4, define cocycles to be continuous maps into the coefficient topological vector space and coboundaries to be actual differences g.v-v. On p. 10, section 5.2 takes a continuous homomorphism into Aut(X,[mu]) semidirect L0(X,mu,T), on a sigma-finite measure space; the global convention in the preliminaries is that measure spaces are standard. Its corresponding representations and their extensions to L0 are continuous.

For each p, the formal subspace is explicitly defined as the kernel of

    H1(G,pi^(p,mu),Lp) -> H1(G,pi^(p,mu),L0).

This is a subspace of ordinary first cohomology. It is not reduced cohomology, and formal vanishing is weaker than vanishing of all first cohomology. Equivalently, a formal class has a measurable primitive, while ordinary vanishing requires an Lp primitive.

Theorem 5.4, printed p. 10, states the implication

    H1_sharp at q = 0  =>  H1_sharp at p = 0,
    for 1 <= p < q < infinity.

There is no ergodicity, finite invariant measure, absence-of-invariants, local compactness, or finite-generation hypothesis in this theorem. The finite-exponent upper bound is inherited from the preceding setup. The lower endpoint p=1 is included. The theorem as stated does not cover 0<p<1 or infinity. OWR’s shorter summary does not justify removing this explicit lower bound.

Although the arXiv notation uses complex functions and T-valued multipliers, the real signed specialization is valid. For a signed real family, formal vanishing over the real numbers implies formal vanishing for its complexification by applying it separately to real and imaginary parts; conversely, taking real parts of a complex primitive recovers a real primitive for a real cocycle.

Question 5.5, also on p. 10, asks whether the same downward-vanishing implication holds for full H1. This is stronger than merely asking for an interval. The paragraph immediately above Theorem 5.4 says the general full-H1 interval question was not determined.

## 3. Topology and cohomology conventions

The source’s Aut(X,[mu]) topology is given on p. 4 by convergence of pushforwards in total variation against each equivalent probability measure. The source treats L0 as a topological coefficient module and states the action extends continuously to it. The usual L0 interpretation is convergence in measure for an equivalent finite measure, rather than requiring global convergence in an infinite measure.

These distinctions cause no gap in the checkpoint’s algebraic formulas: its default is countable discrete G, and Attempt 5 explicitly uses the algebraic quotient Qp=L0/Lp rather than asserting that this quotient is a Hausdorff topological module. Every group-indexed map is continuous when G is discrete. The L0 action must nevertheless remain the p-dependent weighted action; replacing it by the unweighted action cohomology H1_sigma(G,R) would change the problem. The frozen text retains that dependence.

For nondiscrete groups, one must keep the continuous-cocycle requirement. The frozen default scope does not claim that arbitrary Lp-valued algebraic cocycles are continuous.

## 4. Relation to the checkpoint’s deductions

### Proposition 1

The separately proved signed-power inequality works for every 0<p<q<infinity. Applied to a measurable primitive, it yields an Lq-valued formal cocycle. Formal vanishing at q gives an Lq primitive whose difference from the transformed measurable primitive is invariant. The stated absence of nonzero measurable invariant functions removes that difference. The Mazur inverse then proves the original primitive lies in Lp.

This is valid in the stated discrete setting and does not improperly extrapolate Theorem 5.4 below p=1. The existence or absence of nonzero measurable invariant vectors is indeed independent of the positive exponent through the nonlinear equivariant Mazur bijection. No claim that Mazur maps are linear cochain maps is made.

### Proposition 2

Changing to an equivalent invariant probability measure uses the density conjugacy stated on arXiv pp. 5 and 10. With that measure, the signed representation formula has no Radon–Nikodym factor, and the continuous equivariant inclusion Lb -> La is valid for a<b. Vanishing at a makes every Lb cocycle formal; vanishing at c gives formal vanishing at c; Theorem 5.4 supplies formal vanishing at b. Therefore the interval deduction for 1<=a<b<c is sound. No ergodicity is required by this argument.

### Proposition 3

The bounded multiplier test and the density-invariance equation are consistent with the source’s Radon–Nikodym convention on p. 5. For r=(1/p-1/q)^(-1), bounded multiplication Lq -> Lp is equivalent to a in Lr, including quasi-Banach exponents. Intertwining is equivalent to

    a^r = J_g (a^r composed with T_g^(-1)),

which says a^r mu is invariant. Requiring a to be strictly positive and finite almost everywhere gives equivalence of measures; integrability gives finiteness. This diagnoses only the stated multiplication intertwiners, as the frozen text correctly emphasizes.

### Attempt 5

The elementary identification of formal classes with Qp^G divided by the image of (L0)^G is correct for the stated algebraic modules. The kernel of H1(Lp)->H1(L0) is precisely the formal subspace, so the displayed quotient injects into H1(L0).

For a hypothetical hole 1<=a<b<c with full vanishing at c, Theorem 5.4 already forces formal vanishing at b. Hence any nonzero intermediate class must have a nonzero image in measurable-coefficient cohomology. The lower endpoint cannot be imported into that image through a nonlinear Mazur map. This is a correct necessary condition, not a sufficiency claim or a proof of the interval assertion.

## 5. Important extraction trap and publication caution

The text extraction of arXiv Proposition 5.6, p. 11, drops an overline. Direct PDF inspection confirms its conclusion is membership in the closure of B1, not necessarily in B1 itself. Its truncation proof gives approximation by coboundaries; the subsequent spectral-gap clause is what promotes this to formal vanishing in the stated setting. It would be incorrect to use this proposition to conclude unconditional ordinary formal vanishing for every probability-preserving action. The frozen package does not make that error.

The source itself also supplies nonformal classes, in the discussion preceding Proposition 5.6. Thus the checkpoint’s refusal to identify full and formal cohomology is supported by the primary source, not merely by a caution about an unproved possibility.

No change to the frozen originals was made. Only this independent review was added.
