# Substantive turn2: testing the arbitrary-four-genus mutant construction

## Route and outcome

This turn tested whether the published mutant pairs with arbitrarily different four-genera could yield the desired unknotting-number counterexample by combining a four-genus lower bound on one side with an explicit upper bound on the other. The construction is genuine and its lower bound is mutation-sensitive. However, the needed upper bound would also violate the separate connected-sum lower-bound question. The argument below makes that cross-target obstacle precise; it does not assume the connected-sum conjecture is true.

The published mutant construction and four-genus values are credited to Kim–Livingston, *Knot mutation: 4-genus and algebraic concordance*, Pacific Journal of Mathematics220(2005),87–105. The deductions about what an unknotting certificate would imply are the present route test. The source target remains unresolved.

## 1. The actual family, with orientation data retained

Kim–Livingston Section3 constructs a genus-one knot K_J by tying its two bands into J and its concordance inverse -J. Its Seifert matrix is

V=[0 2; 1 0].

The knot J can be selected with sufficiently large sums of Levine–Tristram signatures at seventh roots. Put

L_J=K_J # (-K_J^r),  S_J=K_J # (-K_J),

where r reverses the orientation and - is the concordance inverse (mirror plus orientation reversal). The placement of r matters: it is not an arbitrary replacement of a summand by its mirror. The source proves these are Conway mutants, with S_J slice. For each chosen N, J can be chosen so that g4(k L_J)=k for every k<=N. More generally, N L_J and m L_J #(N-m)S_J are mutants with four-genera N and m.

These are real examples in the original mutation category. The lower bound uses third-cover Casson–Gordon characters with their deck behavior, not a distinguishing invariant of the unchanged unmarked double cover. The source corrects an issue in older two-cover arguments by explicitly using the three-fold cover. That correction is retained.

The Seifert matrix is independent of J. A direct determinant gives, up to a Laurent unit,

Delta_(K_J)(t)=2t²-5t+2=(2t-1)(t-2).                       (1)

It is nonconstant, so every K_J is nontrivial. The determinant is9; neither determinant9 nor algebraic sliceness asserts that K_J is the unknot or has small ordinary unknotting number. Its classical signature function vanishes: the Hermitian form (1-omega)V+(1-conjugate(omega))V^T has zero diagonal and opposite eigenvalues for omega on the unit circle away from1. Thus that signature cannot provide the missing separation.

As a source-consistency check, the third-cover Alexander presentation has Smith factors1,1,1,1,7,7. The deck eigenvalues on the resulting F7 homology are2 and4, each once, matching the primary construction. These checks do not replace the Casson–Gordon theorem or its geometric hypotheses.

## 2. A precise obstruction to the naive four-genus squeeze

Suppose we try to distinguish

A=N L_J,  B=m L_J #(N-m)S_J,

using only the available lower bound u(A)>=g4(A)=N and an upper certificate for u(B). Such a comparison proves a strict inequality only if the upper certificate is

u(B)<=N-1.                                                (2)

But B is a connected sum of **2N nontrivial knots**: every displayed L_J or S_J has two factors, each a mirror or reverse of the same nontrivial K_J. Therefore(2) would in particular violate the separate assertion that a connected sum of r nontrivial knots has unknotting number at least r, with r=2N. It would not be a mere consequence of the already-known four-genus difference.

For N=1 or2 this direct strategy is excluded by the known fact that a nontrivial composite knot cannot have unknotting number1. Its required bound N-1 is at most1, while B is nontrivial composite. For N>=3, the implication above is a conditional cross-target statement: the connected-sum bound is still open in general, so this is not a proof that(2) is impossible. It explains that proving(2) would simultaneously require a much stronger result than the supplied slice/genus data.

This does not rule out distinguishing the same pair with a better lower bound on A, a different upper construction, or another family. It only prevents the invalid inference “one mutant is slice and the other has genus N, so their unknotting numbers differ.” Sliceness supplies no ordinary unknotting upper bound.

## 3. What componentwise crossing changes can certify

Any componentwise unknotting sequence gives the same upper bound

u(A),u(B)<=2N u(K_J),                                      (3)

because mirroring or reversing a knot preserves its individual unknotting number. The product diagrams and the orientation-reversal mutation do not change this count. A componentwise proof can therefore not provide the strict separation in(2) from these data. An improved certificate would have to exploit crossings mixing summands or some other non-componentwise simplification.

It would be incorrect to replace(3) by equality. Brittenham–Hermiller's2025 example explicitly disproves general connected-sum additivity: T(2,7)#mirror(T(2,7)) can be unknotted in at most5 changes rather than the sum6. That theorem neither supplies(2) for the present noninvertible summands nor changes their mutation into a mirror substitution. The two copies T(2,7) and its mirror are invertible; reversing their orientation is not the operation that creates the known nonadditivity example.

More generally, any proposed lower bound L which is unchanged by the mutation cannot certify a strict gap against an actual upper bound r on the other side: L(B)=L(A)<=u(A)<=r. This applies to lower bounds depending only on the unmarked double branched cover and to the mutation-invariant classical signature data. Equivariant information or a genuinely mutation-sensitive lower bound is necessary for that proof strategy.

## 4. Remaining certificate

The route therefore isolates a concrete missing certificate: either an actual non-componentwise unknotting sequence with a rigorously smaller count, or a stronger lower bound on the opposite orientation-reversed sum that exceeds a verified upper bound. Neither is available in this turn. The knot software packages checked in this environment are absent; no unrecognized source executable was run and no unverified diagram identification is used. The retained exact calculations are limited to the named Seifert/third-cover algebra and do not assert an unknotting number.

This is the second substantive author turn. The original question and the unrestricted localization-defect problem from turn1 remain open in the packet; three further substantive turns remain unless a full result is obtained earlier.
