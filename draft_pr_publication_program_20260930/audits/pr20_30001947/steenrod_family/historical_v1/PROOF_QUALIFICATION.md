# Precise qualification of the displayed Steenrod proof

Written after the independent seal; it supplements rather than changes FIRST_PASS_RECONSTRUCTION.md.

## Disposition

The exact target is supported at the published theorem level by the number-valued corollary in Goresky-Pardon §10.2, printed p.339. The frozen candidate says it read that proof; it does not claim a new proof. Its already-solved literature disposition has a valid theorem-level adapter, fully spelled out in the sealed reconstruction. However, this audit cannot certify the literal chain-level proof on p.340 as independently reconstructed for every allowed X. A displayed integral lift is a real unchecked premise, not merely an OCR inconvenience. No counterexample to the target statement or to the number-valued corollary has been found.

The historical footnote in Friedman's May 11, 2015 manuscript, p.28 n.14, explicitly accepts the complete oriented bordism computation. That corroborates literature status. It gives no explanation of the cochain lift, and therefore does not remove this technical qualification by itself. The prior frozen review also does not discuss it.

## Exact type issue

Goresky-Pardon p.330 §4.1 defines Sq^i on perversity p with target perversity 2p. On p.339 §10.2 the displayed lemma instead prints

    Sq^1 Sq^(2i) = Sq^(2i+1): IH_j^m(X;F2) -> IH_(j-2i-1)^m(X;F2),

and its sheaf maps J_a are displayed with source IC_m(F2) tensor IC_m(F2) and target IC_m(F2)[-a]. The following page displays integral D_a with the analogous target IC_m(Z)[-a]. These precise formulae were inspected visually, not accepted from OCR.

The broader reading that every square stays in m is unavailable from the paper's preceding construction, or from Goresky 1984 §§3.3-3.7, pp.491-495. Goresky-Pardon §10.3, pp.340-341, itself points out that Sq^1 need not be defined on middle intersection homology. Accordingly, the candidate may safely use the narrow number-valued corollary but should not promote the printed lemma into an unrestricted middle-perversity Steenrod algebra assertion.

## The integral lift and an exact target-degree countercontrol

The p.340 proof chooses an integral c~ in IC_m^q(Z) lifting a mod-two cycle c in IC_m^q(F2), with

    d c~ = 2y,  y in IC_m^(q+1)(Z),  q=2a+2k+1.

It uses the integral D_a identities and reduces the final expression modulo two and coboundaries. That algebra works once the displayed lift exists. But reduction of integral Deligne middle complexes need not give the mod-two Deligne middle complex. §6.3, pp.332-333, records precisely the obstruction to a Bockstein preserving a perversity. §8.3 supplies the top-perversity Bockstein from orientability of links; it does not supply a middle-perversity Bockstein.

This objection occurs in the degree needed for j=1, not only in an irrelevant low-degree sheaf stalk. Let L=RP^3, Y=Sigma L, and X=Y x S^2. L is an oriented three-manifold; its cellular integral cochain differential between degrees one and two is multiplication by two, with the other adjacent differentials zero. Thus H^1(L;Z)=0, H^2(L;Z)=Z/2, while H^1(L;F2)=H^2(L;F2)=F2.

The only singular strata of X are the two cone vertices times S^2, both of codimension four. Their links are L. Hence X is compact and integrally oriented, and the F2-Witt condition has no odd-codimension link to test. It is a legitimate six-dimensional member of the target class. With m(4)=1, the link torsion test in §6.3 is

    Tor_Z(H^2(L;Z),F2)=F2 != 0.

The cone computation truncates link cohomology above degree one. Mayer-Vietoris for the two cones forming Y gives

| degree | IH_m^degree(Y;Z) | IH_m^degree(Y;F2) |
| --- | --- | --- |
| 0 | Z | F2 |
| 1 | 0 | F2 |
| 2 | 0 | 0 |
| 3 | Z/2 | F2 |
| 4 | Z | F2 |

Tensoring with the ordinary two-cell complex of S^2 (whose cohomology is free in degrees zero and two) gives

    IH_m^3(X;Z)=Z/2,
    IH_m^3(X;F2)=F2 direct-sum F2,
    IH_m^4(X;Z)=Z.

In particular, the mod-two summand IH_m^1(Y;F2) tensor H^2(S^2;F2) is absent from the image of integral reduction. Suppose a representative c of that summand admitted exactly the p.340 lift with y allowable in IC_m^4(Z). Because d^2=0, y is a cocycle; 2[y]=0, whereas IH_m^4(X;Z) is torsionfree. Therefore y=d z for an allowable integral z. The cochain c~-2z would be an integral cocycle reducing to c, contradicting absence from the image. This demonstrates the failure of an automatic premise for q=3 (a=0,k=1), the actual odd middle degree of X.

This countercontrol does not produce a nontrivial Witt class. Its two middle mod-two summands pair hyperbolically: the Y degree-one and degree-three factors are dual, and the S^2 degrees zero and two are dual. Each diagonal is zero. It therefore illustrates exactly why an integral-lift objection must not be reported as a counterexample to the conclusion.

## What remains unsupported in this family

The source's literal universal cochain lift, and a fully type-correct version of the displayed integral D_a construction on these particular mod-two middle classes, are not verified. A different cochain model, a perversity-changing construction with a carefully justified final number, or another independently checkable argument might resolve that issue. This audit did not attempt a substantive new replacement proof. Reopening the chain-level route requires such a materially new mechanism or source clarification.

The normality/local-orientation/algebra adapters and the exact published corollary's implication for the target remain valid. The precise acceptance level is therefore **theorem-level literature support with a recorded unresolved displayed-proof premise**, rather than an unqualified new independent proof certificate. No categorical priority statement is made.
