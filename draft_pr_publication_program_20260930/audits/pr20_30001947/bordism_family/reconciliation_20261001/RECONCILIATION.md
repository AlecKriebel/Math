# Supplemental reconciliation: integral lifts in the Goresky–Pardon proof

Checkpoint UTC: 2026-10-01T18:34:11Z. Completion estimate: 100% of requested proof-level reconciliation. Frozen original candidate head remains 7914dfa8c2ddf0efb784a29accc8a05b5a24a690. The original independent seals, report, verdict, log and manifest remain unchanged. This supplement supersedes their unconditional proof-verification language; it does not rewrite the historical first-pass record or claim that the published theorem is false.

**Outcome:** the reported control and the same-middle-perversity integral-lift obstruction are correct in Goresky–Pardon's own conventions. The literal lift premise on printed p.340 is false for an admissible target-dimensional space. Section10.7 explicitly relies on §10.2 and therefore supplies no independent escape from that premise. The exact prior theorem is still positively present in the literature and explicitly acknowledged by the proposer; an independently verified universal proof has not been established by this source audit.

## Exact convention audit

[Goresky–Pardon, *Wu numbers of singular spaces*](https://www.math.ias.edu/~goresky/pdf/Wu.jour.pdf), §3.1 (printed pp.329–330), uses normally oriented PL allowable chains of geometric dimension n−q as a cochain complex IC_p^q. On a compact integral-oriented X, its cohomology IH_p^q(X;Z) is I^p H_{n−q}(X;Z). This is not the algebraic dual complex Hom(IC_p, Z), whose perversity changes under integral duality when link torsion is present. The distinction matters: applying a cohomological universal coefficient theorem to the latter complex would test the wrong object.

The p.340 scan explicitly specifies a mod-two cocycle c in Γ(IC_m^q(F_2)), then an integral lift c~ in Γ(IC_m^q(Z)), with d c~=2y and y in Γ(IC_m^{q+1}(Z)). Both the input lift and its halved differential have the SAME lower-middle perversity m. The stated integral D_j maps also have two IC_m(Z) inputs. Thus a lift to unrestricted ordinary cochains, or a lift whose half-boundary only belongs to perversity m+1, is insufficient for the printed calculation.

## Independent computation of the concrete control

Let L=RP^3, Y=ΣL, and X=Y×S^2. The singular strata of X are its two copies of S^2, both of codimension four, with link RP^3. The regular part is (−1,1)×RP^3×S^2, which is integral-oriented. The links are connected and oriented, so X is already normal and locally orientable. Its only genuine singular codimension is even, so the F_2-Witt odd-codimension condition is vacuous. This is an admissible closed compact classical PL F_2-Witt space of dimension six.

At codimension four, m(4)=1. The cone cutoff is 4−m(4)−1=2. The two-cone Mayer–Vietoris calculation gives, for G=Z or F_2,

    I^m H_i(Y;G) = H_i(L;G)       for i<2,
                   0             for i=2,
                   H_{i−1}(L;G)  for i>2.

The integral homology of RP^3 is (Z,Z/2,0,Z), and its mod-two homology has one F_2 in each degree zero through three. Consequently

| i | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| I^m H_i(Y;Z) | Z | Z/2 | 0 | 0 | Z |
| I^m H_i(Y;F_2) | F_2 | F_2 | 0 | F_2 | F_2 |

The S^2 factor has free homology, so the product gives I^m H_i(X;G)=I^m H_i(Y;G)⊕I^m H_{i−2}(Y;G). Translating into the exact GP convention yields

    IH_m^3(X;Z)   = I^m H_3(X;Z) = Z/2,
    IH_m^3(X;F_2) = I^m H_3(X;F_2) = F_2^2,
    IH_m^4(X;Z)   = I^m H_2(X;Z) = Z.

For an independent finite-complex check, start with the cellular cochains of RP^3: δ^1=2, with other differentials zero. A cone's Deligne truncation τ_{≤1} has degree-one module ker(2), which is zero over Z and F_2 over F_2. Form the mapping fiber of the difference of the two cone restrictions into the equatorial RP^3 complex, then tensor the cellular S^2 complex. This yields explicit coefficient-dependent matrices in [EXACT_LIFT_CONTROL.json](EXACT_LIFT_CONTROL.json), reconstructed by [exact_lift_control.py](exact_lift_control.py). It verifies every d²=0, the mod-two cohomology dimensions (1,1,1,2,1,1,1), the integer free ranks (1,0,1,0,1,0,1), and integer degree-three Smith invariants (1,2), giving Z/2. Degree four has kernel Z and no incoming boundary. No triangulation or cup-i operation is claimed to have been computed.

This calculation uses the standard allowability-with-coefficients complex, not IC_m(Z) tensor F_2. Friedman's [book manuscript](https://faculty.tcu.edu/gfriedman/ihbook.pdf), printed pp.214–216, independently explains why these coefficient constructions differ; its suspension formula and proof appear at printed pp.272–273.

## Why the required lift cannot exist

Consider the reduction map on GP degree-three cohomology. Its integral source is Z/2 and its mod-two target has dimension two, so its image has dimension at most one. Let [c] be a mod-two class outside this image.

Suppose some representative c had precisely the lift required on p.340: an allowable integral cochain c~ of degree three with reduction c and d c~=2y, where y is an allowable integral degree-four cochain of the same perversity. Integral PL cochain modules have no two-torsion, so d²c~=2d y=0 implies d y=0. Also 2[y]=[d c~]=0. Since IH_m^4(X;Z)=Z has no two-torsion, [y]=0, hence y=d z for an allowable integral degree-three z. Then c~−2z is an allowable integral cocycle reducing to c. This would put [c] in the reduction image, a contradiction.

Thus at least one mod-two middle class has NO such allowable integral lift, for ANY representative, not merely for one unfortunate choice of chains. The exact finite complex exhibits a representative with coordinates (0,1,1,0) in degree three. It is a cocycle, is nonexact, and lies outside the integral cochain reduction image.

There is also a geometric explanation. Choose an integral one-cycle z generating H_1(RP^3;Z)=Z/2 and an integral two-chain B with ∂B=2z. The difference of its north and south cones gives a three-chain whose mod-two reduction is the suspension of the nonzero H_2(RP^3;F_2) class. The three-chain may meet each suspension vertex because 3−4+m(4)=0. Its integral boundary, however, is twice the difference of the two cones on z. That two-chain meets those vertices, while 2−4+m(4)=−1 forbids such intersections. The mod-two boundary disappears; the integral half-boundary is not middle-allowable. Taking the product with a point of S^2 gives exactly the missing middle class of X. The abstract argument above rules out alternative same-perversity lifts as well.

## Why local orientation, top Bockstein and normalization do not repair it

GP §6.3 requires, for every codimension-c link L,

    Tor_Z(IH_p^{p(c)+1}(L;Z), F_2)=0

for the same-perversity cohomology Bockstein to extend. For the present manifold link,

    p=m, c=4: H^2(RP^3;Z)=Z/2, so the Tor group is F_2 and the criterion FAILS;
    p=t, c=4: H^3(RP^3;Z)=Z, so the Tor group is zero and the criterion PASSES.

Equivalently, the link Bockstein H^1(RP^3;F_2)→H^2(RP^3;Z) is nonzero. This directly tests the actual §6.3 condition. Integral orientation ensures the relevant top-perversity Bockstein; it does not ensure the lower-middle one. GP §6.5(2) says a Bockstein can instead increase perversity by one. That is exactly what the geometric half-boundary requires here. It does not supply the same-m input required by the printed D_j formula, and the paper does not give the necessary mixed-perversity repair at that step.

X is already normal, so normalization changes nothing. Local orientability also holds throughout the control. Neither hypothesis can remove its concrete same-middle lift obstruction. GP §10.3, continued on printed p.341, explicitly warns that Sq^1 is not generally defined on middle intersection homology; this agrees with the restriction rather than resolving it. The lemma's final Sq^1 acts at the top perversity after an even square, but that fact does not retroactively produce an allowable integral lift of its arbitrary original middle input.

This is a defect in the literal printed proof premise, not a falsification of the claimed relation: for this X the middle pairing is still hyperbolic. A possible corrected operation argument would need a separately checked construction and perversity bookkeeping. No such construction is asserted here.

## Pairing and dependence of the bordism argument

The middle homology of X splits as

    (I^m H_3(Y;F_2)⊗H_0(S^2;F_2)) ⊕
    (I^m H_1(Y;F_2)⊗H_2(S^2;F_2)).

The self-pairing of the first summand vanishes by taking distinct point representatives on S^2. The self-pairing of the second vanishes by general position of two one-cycles in the four-dimensional Y. Their cross-pairing is one, by F_2 intersection duality between degrees three and one in Y and the point/fundamental-class pairing on S^2. Thus the Gram matrix is [[0,1],[1,0]], Witt class zero. Its odd middle Wu class is zero. Therefore the control is NOT a counterexample to the theorem, the original problem's negative answer, or even the odd-square conclusion on this particular X. It falsifies the unrestricted input-lift assertion in the proof.

GP §10.7 Part A explicitly derives the dimension-4j+2 Euler-characteristic vanishing using Lemma10.2. The boundary criterion it invokes after that vanishing does not itself establish the vanishing. Section10.4 also invokes the same lemma. Therefore the bordism route does not provide an independent verified universal proof when the lemma's printed premise is under audit. My previously recorded normalization and boundary-Lagrangian adapters remain valid conditional deductions; they do not prove the missing universal source premise.

## Current verdict and mandatory audit-language correction

The exact published prior remains [GP §10.5 Theorem A](https://www.math.ias.edu/~goresky/pdf/Wu.jour.pdf), and [Friedman §5.2.1 footnote14](https://faculty.tcu.edu/gfriedman/papers/stratwitt.pdf) explicitly identifies the original question as already settled by it. These are positive evidence for the literature-status correction, not a proof-level repair of the printed lift step. The book corroboration likewise repeats the computation without repairing this step in the inspected text.

**Mandatory correction to this audit's certification:** replace its initial unconditional “no exact mathematical gap remains / independently verified universal result” language with two distinct claims: (a) an exact prior published theorem and proposer acknowledgment support the known-negative literature status; (b) the universal proof has not been independently verified because the same-middle lift premise used in the printed proof is false and its repair is unprovided in the inspected sources. Any candidate readiness claim of a fully verified direct odd-square proof must carry the same qualification. Do not assert that the theorem is false or that the problem is mathematically open merely from this proof caveat.

**Blocked route:** independent universal proof verification through GP §10.2→§10.7. **Exact remaining gap:** a checked argument establishing the needed odd-square relation or the dimension-4j+2 vanishing without the false same-middle lift premise. Reopen only for materially new source evidence or a verified repair, not by re-invoking the theorem statement or author footnote.

No new central problem-solving attempt, outward communication, Git action or PR disposition was performed. The strongest independently verified supplementary result is the admissible dimension-six proof-premise control, its same-perversity lift obstruction, and its hyperbolic middle form. The literature-status classification and a universal theorem-proof certification are now explicitly separated.
