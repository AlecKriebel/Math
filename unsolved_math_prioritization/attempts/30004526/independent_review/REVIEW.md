# Independent audit: local strong Lefschetzness and Q(0)

**Target:** 30004526 / OWR-2654827-002.  
**Verdict:** **PASS_SCOPED_TOP_HESSIAN_CUBIC_EQUIVALENCE_AND_PERAZZO_OBSTRUCTION.** No mandatory mathematical correction.  
**Disposition:** the original implication remains **unsolved, 2/5**. The result is restricted to characteristic zero; it is not a general local strong-Lefschetz theorem. This is a separate adversarial AI review, not human peer review or certification of novelty.

## 1. Scope and primary sources

The frozen `PARTIAL_RESULT.md` has SHA-256

`1321a6684a831a00c066eee06882dee334400ddf9ed3d350c7e19c4cf0633ac9`.

I checked the full original OWR contribution, Question 4 on printed p. 1542, and the local Jordan-type definition on pp. 1549–1550. The question concerns local, potentially nongraded Artinian Gorenstein algebras and the maximal-ideal symmetric decomposition. The adjacent discussion of decompositions for a principal ideal does not turn the unadorned Q(0) into a Jordan block or a central-simple module.

The full primary Iarrobino–Macias Marques manuscript confirms this interpretation independently: Definition 1.3 defines local strong Lefschetzness by Jordan type equal to the conjugate of the reordered Hilbert sequence; p. 4 identifies Q_A(0) with the apolar algebra of the highest-degree dual form; Question 2.32(b) on p. 23 asks the relevant implication. Part (a), about the associated graded algebra itself, is different. The author's attribution to Johanna Steinmeyer is retained.

Sources checked: [OWR 31/2020](https://publications.mfo.de/bitstream/handle/mfo/3804/OWR_2020_31.pdf?isAllowed=y&sequence=4), [Iarrobino–Macias Marques, arXiv:2112.14664v1](https://arxiv.org/abs/2112.14664v1), and [Elias–Rossi, arXiv:0911.3565](https://arxiv.org/abs/0911.3565). The last paper's canonical-graded result and its general cubic classification are genuine earlier structure theorems. The submitted direct rank proof does not claim those theorems as new.

Ordinary derivatives and divided-power contraction are equivalent here by factorial rescaling because the field has characteristic zero. The package does not incorrectly transfer factorial identities to positive characteristic. Its infinite-field assumption is sufficient for the generic-element terminology; its concrete implications use the actual chosen element.

## 2. Re-derivation of the nonlinear-element rank identity

Let A be the apolar quotient of a polynomial F with highest degree j, and let M=R·F. The map from A to M given by differential action is an isomorphism of R-modules, not merely a dimension count. Therefore multiplication by any element ell corresponds to ell(D). A formal-power-series representative of ell causes no difficulty: only its finite jet through degree j can act nontrivially on F.

Write ell=L+H, with H of order at least two and L determined by a vector c. If ell^j is nonzero, then
\[
 \ell(D)^jF=L(D)^jF_j=j!F_j(c)\ne0.
\]
For T=ell(D)^(j−2), the image of the cyclic generator F has degree two and nonzero leading quadratic. Images of first derivatives of F have degree at most one. Their linear coefficients are precisely the rows of the Hessian of F_j at c, multiplied by the nonzero scalar (j−2)!. Images of derivatives of order at least two are constants or zero. A nonzero constant is present, since
\[
 T(D_L^2F)=j!F_j(c).
\]
Consequently the image has one quadratic direction, rank(Hess F_j(c)) independent linear directions modulo constants, and one constant direction. This gives exactly
\[
 \operatorname{rank}(m_\ell^{j-2})=2+\operatorname{rank}\operatorname{Hess}(F_j)(c).
\]
There is no hidden extra image from higher terms of ell: those terms lower degree further and can alter only the already counted lower-degree components. Nor can a cancellation among the first derivatives introduce a second quadratic direction. This verifies the strongest all-nonlinear-elements assertion in the package.

## 3. Hilbert partition and the cubic equivalence

Every interior entry of the local Hilbert function is positive. Since its two endpoint entries are one, the first column of the conjugate partition has length j+1 and contributes three to the rank of the (j−2)-nd power. Every later column contributes one exactly when it reaches all j−1 interior entries. Thus the required rank for strong Lefschetz Jordan type is min(h_1,…,h_(j−1))+2, as stated. The top Jordan block also forces ell^j≠0, so the preceding rank formula is applicable.

The equality h_(j−1)=s, where s is the essential-variable dimension of F_j, is valid even with lower-degree terms in additional variables. Derivatives of order j−1 have linear leading parts determined solely by F_j; all higher derivatives are constants. Passing from m^(j−1) to m^j removes exactly that one-dimensional constant space. The quotient Q_A(0) supplies the degreewise Hilbert inequalities used later.

For j=3 this gives H(A)=(1,r,s,1), r≥s. Strong Lefschetzness of A forces the cubic top Hessian to have rank s and the top evaluation to be nonzero. For the graded cubic algebra Q_A(0), these are exactly the nontrivial complementary-degree Lefschetz maps. Conversely, a Lefschetz linear form for Q_A(0) has multiplication ranks on A
\[
 \dim A,\quad s+2,\quad2,\quad1,\quad0.
\]
The rank-two statement for the square follows from one nonzero linear image of F and one nonzero constant image; all remaining images are constants. These ranks yield the partition (4,2^(s−1),1^(r−s)), which is exactly the required conjugate Hilbert partition. The converse therefore covers all lower-degree cubic deformations, without assuming that the local algebra is already graded.

## 4. The entire stated quartic deformation family

For G=XU³+YU²V+ZV³, I independently checked the derivative spaces. The first derivatives have dimension five. The second derivatives are spanned by the three independent pure quadrics U², UV, V² and the three independent mixed quadrics 6XU+2YV, 2YU, 6ZV. Third derivatives span the five essential linear variables; fourth derivatives span constants. Hence the homogeneous Hilbert function is (1,5,6,5,1).

The Hessian's upper-left three-by-three block is zero. Its first three output coordinates lie in the image of a three-by-two matrix, of dimension at most two, and only two output coordinates remain. Its rank is therefore at most four at every point, including singular choices of U,V. A rank-four evaluation is a diagnostic, but generic rank is unnecessary for the obstruction.

For any lower-degree perturbation, the top apolar quotient forces h_1≥5 and h_2≥6, while the previous inverse-system argument gives h_3=5. Thus the interior minimum is exactly five. Strong Lefschetzness would require a rank-five top Hessian, impossible. Additional variables appearing only in lower-degree terms append zero rows and columns to that top Hessian and do not evade the argument. This is an all-coefficient proof, not an extrapolation from the finite deformation examples.

## 5. Independent controls and their limits

The submitted checker was replayed beside an isolated frozen copy. All **6,276 assertions** passed and its written receipt reproduced byte for byte. Its checker and receipt hashes are respectively

`74c5795112ed4b39616d294589a55b3e3d1736e17fd81b9101f04064e75e23e2`

and

`64dea331c4359ec28c22ba3d8714150e8e4f3aa4b90ebc06d70f91680db293dc`.

The separate checker uses exact rational moment-pairing matrices rather than the submitted derivative-closure implementation. For a dual polynomial F, its matrix entries are the constant evaluations of D^(a+b)F. Shifting these moments by powers of ell computes multiplication ranks on the actual local apolar quotient, because the pairing kernel is exactly Ann(F). Tests include higher-order nonlinear terms through order four, socle degrees three through seven, and variables appearing only in lower terms. Independent catalecticant and block-Hessian controls check the Perazzo top form. All **3,359 independent exact assertions** passed across 12 local moment-matrix cases and the separate partition/Perazzo controls. The receipt records each case.

These controls supplement the proof. They do not establish the statement for all socle degrees, prove realizability of arbitrary integer Hilbert sequences, or turn the Perazzo obstruction into a counterexample to the source question.

## 6. Final disposition

The top-Hessian identity, necessary Hilbert-minimum equality, complete cubic equivalence, and entire declared quartic deformation exclusion are valid as written. No mandatory correction is needed. The original general implication remains unresolved: the argument controls only the first Hessian, does not settle all higher Lefschetz maps, and leaves interior Hilbert dips and other leading forms available. The characteristic-zero and prior-structure-theorem qualifications must stay explicit.
