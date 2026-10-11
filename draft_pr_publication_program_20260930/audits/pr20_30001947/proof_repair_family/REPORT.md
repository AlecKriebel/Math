# PR20 / problem 30001947: existing-source proof repair audit

**Result:** exact published prior support remains positive, but no independently verified repair of the displayed universal cochain proof was found in this bounded primary-source audit. The proof qualification is material. This is neither a counterexample to the target theorem nor a claim that the original question is open worldwide.

The assigned audit is complete. The goal of certifying a repaired universal proof is not achieved. The independent criterion was sealed before reading sibling reports; source conventions and the principal controls were checked independently. No Git action, outreach, release, installation, or new substantive proof attempt was performed.

## Exact target and acceptance levels

The target is a compact PL pseudomanifold without boundary or codimension-one strata, integrally oriented on its regular stratum, satisfying the mod-two Witt link condition, of dimension 4j+2. Its nonsingular mod-two middle form should have zero class in the symmetric bilinear Witt group. Alternation of the form is a sufficient stronger claim. Merely metabolic does not imply alternating in characteristic two.

[Goresky–Pardon 1989](https://www.math.ias.edu/~goresky/pdf/Wu.jour.pdf), §10.2, printed p.339, states the exact number-valued odd-square vanishing. Its §10.5 Theorem A states the oriented Witt bordism consequence. Section10.7 PartA invokes §10.2 for the 4j+2 case. These are positive published prior statements, with the later proposer acknowledgment already established by the sibling status audit. That acknowledgment does not independently repair the cochain premise.

Published theorem status, a valid theorem-to-target adapter, and a rebuilt proof certificate are distinct acceptance levels. This family certifies the first distinction and the failed repair controls, not the universal rebuilt proof. Dimension two has the ordinary oriented-surface verification independently of the disputed higher-dimensional lifting step.

## Literal source premise and its exact control

GP §3.1 uses the Deligne cohomology convention with cutoff p(c) on a codimension-c link. The p.340 calculation asks for an integral lower-middle cochain lifting a mod-two cocycle, with its differential twice an integral cochain in the same perversity. Proposition6.3 imposes a link torsion condition for a Bockstein that preserves perversity. Section8.3 obtains the top-perversity case from local orientability. It does not supply the lower-middle case. Relevant formula pages333,339,340 were visually inspected.

Let Y=ΣRP3 and X=Y×S2. RP3 is an integrally oriented three-manifold. The only singular strata of X are two copies of S2, of codimension four; their links are RP3. The mod-two Witt condition has no odd-codimension stratum to test. Thus X is an exact six-dimensional target control. Here m(4)=1, and the obstruction group at the link is Tor(H2(RP3;Z),F2)=F2.

The cochain calculation is reproduced by [verify_controls.py](verify_controls.py). Start with cellular RP3 cochains Ck=Z for k=0,1,2,3, with d1=2 and other differentials zero. Each vertex neighborhood uses the good truncation A=τ≤1C. The two-cone Mayer–Vietoris complex is the homotopy fiber of A⊕A→C, with degree-k terms A^k⊕A^k⊕C^(k−1) and differential

    (a,b,l) ↦ (da,db,a−b−dl).

Over Z, A1=ker(d1)=0. Over F2, A1=F2. This is exactly the coefficient-sensitive distinction; replacing good truncation with brutal truncation would erase it. Exact integer kernels and determinantal Smith divisors, and mod-two row reduction, give:

| Degree k | IH_m^k(Y;Z) | IH_m^k(Y;F2) |
| --- | --- | --- |
| 0 | Z | F2 |
| 1 | 0 | F2 |
| 2 | 0 | 0 |
| 3 | Z/2 | F2 |
| 4 | Z | F2 |

The two free cells of S2 give the direct sum of this complex and its degree-two shift. Consequently

    IH_m^3(X;Z)=Z/2, IH_m^3(X;F2)=F2², IH_m^4(X;Z)=Z.

Integral reduction in middle degree has rank one. The missing mod-two class is the degree-one class on Y times the degree-two class on S2. If a representative c of it had the printed lift dc~=2y with y still lower-middle allowable, then y would be a cocycle. Since IH_m^4(X;Z) has no 2-torsion, y=dz for an allowable integral z. Then c~−2z would be an integral cocycle reducing to c, contradicting the computed reduction rank. The printed automatic premise therefore fails in the target degree q=3.

This does **not** falsify the target conclusion: the degree-one and degree-three Y factors are dual, as are degrees zero and two of S2. The middle pairing is [[0,1],[1,0]], with zero diagonals and zero Witt class. The pairing claim here is the analytic product-duality computation; the script checks the resulting matrix, rather than computing intersections of a triangulation.

Changing only lower-middle to upper-middle does not repair this control: m(4)=n(4)=1. A genuinely larger perversity could admit more lifts, but would require a separately verified product and top-evaluation adapter.

## Modern Adem route: a failed numerical adapter

[Chataur–Saralegi-Aranguren–Tanré 2016](https://msp.org/agt/2016/16-4/agt-v16-n4-p02-p.pdf), TheoremB, printed pp.1867–1868, gives Steenrod/Adem relations for loose perversities. Its full proof pp.1869–1871 and its Goresky-comparison proof pp.1872–1877 were inspected. For p=m, the relation Sq1 Sq^(2j)=Sq^(2j+1), j≥1, is asserted in destination

    r=min(4m,2m+1,m+2j+1).

The ordinary top square has destination 2m≤t. At codimension four, however, r(4)=3 while t(4)=2. Thus the modern relation is not automatically an equality of the required top-valued numbers. This statement uses the published theorem as stated; it does not assert a defect in that modern theorem.

The numerical loss can be checked on the same X. Its top-perversity degree-six group is F2. Giving its codimension-four strata loose value three makes the degree-six group zero. In the two-cone model this is immediate: τ≤3C(RP3;F2)=C, so the suspension complex computes H*(RP3;F2), with no degree-four group; its product with S2 has no degree-six group. In contrast, cutoff two retains the suspended degree-three link class in degree four. These assertions agree with the suspension calculation in CST2016 Example5.4, p.1881, and are reproduced by the script.

Therefore the comparison from top into this larger loose destination is not injective even in the exact target category. An equality after that comparison cannot establish equality of numbers before it. The missing artifact is a type-correct numerical Adem relation retaining top evaluation, or a proved adapter for the specific classes and homotopies. Generic loose-perversity Adem relations do not supply it.

## Other bounded routes and remaining gap

[CST, *Blown-up intersection cohomology*](https://arxiv.org/pdf/1701.00684), §§4,12,13, supplies integral cup/cup1 constructions, cone computations, and coefficient-comparison results. Its full relevant comparison proof was read. Working separately over every coefficient ring does not give a same-perversity short exact coefficient sequence. The field or local torsion-free comparison hypotheses must be checked; they cannot be imported as an automatic integral lift for all mod-two Witt spaces.

[Brasselet–Libardi–Rizziolli–Saia 2019](https://publi.math.unideb.hu/paper/2294/download/10_5486_PMD_2019_8265.pdf), §§4.1–4.2, pp.306–308, repeats the relevant relation as Lemma4.7 explicitly attributed to GP §10.2, without a replacement proof. It is corroboration of acceptance, not independent repair evidence. Searches for GP-specific errata/corrections located no verified source-specific repair in the bounded set.

The exact unresolved audit gap is a universal, independently checkable justification of numerical odd-middle-square vanishing under integral orientation and precisely the mod-two Witt condition, avoiding the false universal same-middle lift premise. The printed-lift route, plain upper-middle substitution, generic loose-Adem adapter, and dependent bordism-restatement route are blocked until materially new source evidence or a verified adapter appears. This audit did not initiate a replacement proof program.

The appropriate publication correction is to preserve the exact prior attribution and source-status conclusion while qualifying any claim of independently reconstructing the p.340 proof. Do not publish the control as a theorem counterexample or label the original problem globally open. No full foreign source is in the first-party manifest; those files are under ignored tmp/primary_sources. Version, hash, locator, search-boundary, and verification receipts are supplied separately.
