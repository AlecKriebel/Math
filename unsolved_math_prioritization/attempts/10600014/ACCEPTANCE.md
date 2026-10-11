# Acceptance: the symmetric annihilating Brauer projector

Decision: ACCEPTED_PROJECTOR_COMPONENT. Full original problem: PARTIAL.

## Accepted mathematics

The complete proof is in PROOF.md; the complete source audit and corrections are in AUDIT.md. For n >= 1 the algebra is the free pairing-diagram Brauer algebra B_n(d), with each closed middle loop valued at d. The generic field is C(d), with coefficients in Q(d). The theorem includes BOTH-sided e_i annihilation and BOTH-sided v_i invariance, in addition to nonzero idempotence.

1. Every diagram factors through permutation diagrams and disjoint cup-cap generators. The augmentation is 1 on permutations and 0 on lower-through-rank diagrams. It proves uniqueness and, after normalization a_0=1/n!, idempotence without assuming semisimplicity.
2. Independent left and right permutation invariance gives the orbit sums S_{n,l}. The complete four-case preimage count proves (d+2n-2l-2)a_l+2l a_{l-1}=0.
3. The exact coefficients are a_{n,l}=(-2)^l l!/[n! product_{j=1}^l(d+2n-2-2j)]. The proof works in the specified localization R_n of Q[d]; its torsion-free module argument is not extended to arbitrary rings with zero divisors.
4. The corner F_i B_{i+1}(d) F_i has the basis F_i, F_i e_i F_i, F_i v_i F_i. The three diagram coefficients establish the precise recurrence, including the n=2 base step.
5. The recurrence tower through rank n is defined over T_n=Q[d,(product_{j=0}^{n-2}(d+2j))^(-1)], with T_1=Q[d]. It specializes at every complex value outside E_n={-2j:0<=j<=n-2}; E_1 is empty.
6. At a fixed rank, the exact nonexistence set for this projector is P_n={-2n+2l+2:1<=l<=floor(n/2)}. At a pole the first vanishing contraction coefficient contradicts the forced nonzero preceding coefficient. At E_n minus P_n direct specialization in R_n proves existence without evaluating an undefined recurrence tower.
7. The n=1 case, d=2, negative odd parameters and fixed-rank removable tower obstructions are covered explicitly. The sign idempotent (1-v_1)/2 demonstrates that virtual invariance is indispensable. Free diagrams remain independent even at nonsemisimple parameters or in the presence of a nonfaithful tensor representation.

## Source correction boundaries

The projector component is verified independently of the printed induction in Deng, Jin and Kauffman, arXiv:2103.11355v1. The full audit retains all local display/index qualifications and two separate counterchecks:

- The unnormalized closure trace satisfies tr(1_2)=d^2 and tr(e_1)=tr(v_1)=d. Thus tr(F_2)=(d+2)(d-1)/2. At d=3 this equals 5, whereas the printed Lemma 6.1 gives 15. AUDIT.md preserves the exact normalization and the telescoping expression, with its finite-check boundary.
- The permutation word v_2 v_1 v_2 in B_3 has minimum length 3 and contains v_2 twice. Through rank excludes shorter words containing e_i, and the length-at-most-two permutation enumeration excludes all other shorter words. A different reduced representative with a single v_2 does not repair the printed universal assertion.

These are findings about the inspected v1 only. The journal text was not compared. Neither Section 6 statement is imported as a dependency of the accepted proof.

## Residual work and exclusions

The original problem also requests useful recoupling theory. A specified family of fusion objects, fusion multiplicities and bases, admissibility rules, recoupling isomorphisms, coherence identities and a demonstrated virtual-knot application remain outside this result. No full classification of primitive idempotents or singular blocks, no positive-characteristic assertion, no novelty claim and no blanket acceptance of the source manuscript is made.

The finite exact checks corroborate the displayed all-rank proof; they do not establish universal validity by enumeration. The historical normal, -O and -OO checks are summarized with byte identities in VERIFICATION.json. No raw outputs or executable reproduction package are distributed.

This AI-assisted, unrefereed edition records an internal AI mathematical audit. Acceptance is limited to the expressly stated projector component and parameter criterion; it is not external human peer review or formal proof-assistant certification. The full original recoupling problem remains PARTIAL. This is a written proof/correction/audit edition, not a computational reproduction package. Source inspection and exact mathematical checks described below occurred in the preceding audit on 11 October 2026. Editorial preparation authenticates the retained records without claiming a fresh scholarly-source inspection or a new mathematical-program run.
