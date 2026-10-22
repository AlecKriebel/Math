# Independent audit of the four point quantum symmetrizer comparison

13 October 2026. This report reviews the mathematical assertions in *Quantum-symmetrizer adjudication: two different coefficient statements* and the corresponding core claims in Alper Ferudun's pinned 1 October 2026 manuscript.

## Verdict

**Accepted with explicit scope.** For the solution \(X=\mathbb Z/4\), \(r(x,y)=(y,x+1)\), over every field of characteristic different from 2:

1. The signed quantum-symmetrizer image \(A\otimes B\otimes A\) fails to resolve the structure algebra \(A\). Its degree-2, weight-3 homology has at least the two exhibited independent classes. This verifies Ferudun's core Theorem 1.3(a) and answers the precisely specified FGG Question 44 negatively.
2. With both generator actions equal to zero, no quotient chain complex through which the specified QS comparison factors can repair the comparison. Its degree-3 image misses Hochschild homology. Dually the Hochschild-to-braided cohomology map is noninjective, including every subcomplex containing its image. This verifies the core of Ferudun's Theorem 1.3(b).
3. With both generator actions equal to one, the same example admits the proposed all-degree chain quotient: remove the all-sum line in each degree at least 2. The induced QS is a quasi-isomorphism, over every such field, with no rational-only restriction.

No mathematical gap requiring a correction was found in these three statements. The quotient in item 3 is a quotient of chain complexes after fixing the coefficient module. It is not certified as an algebra-ideal quotient, Hopf-ideal quotient, coefficient-independent construction, or solution for all Yang--Baxter braidings. Those stronger restrictions would be different questions.

**The terse OWR Problem 2 remains subject to a source-scope qualification.** Its short wording and neighboring positive cases do not fix all the coefficient and quotient conventions needed to identify it with one of the statements above. In particular, the verified zero-character obstruction cannot be advertised as ruling out all constant-character quotients. Item 3 explicitly disproves that broader reading for this example. Ferudun's Remark 3.3 limits its constant-character calculation to the Nichols-image quotient and does not claim to have treated every quotient.

## Signed comparison and source conventions

FGG's Definition 31 defines the quantum symmetrizer using positive reduced braid lifts; Theorem 32 applies it to the braiding \(-r\). Thus

\[
Q_2=1-r,\qquad Q_3=1-r_1-r_2+r_1r_2+r_2r_1-r_1r_2r_1.
\]

The sign is essential. With \(R=\operatorname{im}(1-r)\), \(A=T(V)/(R)\), \(B_n=\operatorname{im}Q_n\), parabolic factorizations give both \(B_n\subset K_n\) and the two endpoint inclusions into \(V\otimes B_{n-1}\) and \(B_{n-1}\otimes V\). Hence the normalized bar restriction has only its two endpoint terms. This is the image complex asked about in FGG Question 44, rather than an unrelated use of the word Nichols algebra.

Lebed's Theorem 2 was checked in the PDF itself. Its chain differential is the alternating sum of the left face minus the right face, with the selected strand braided to the appropriate endpoint. Theorem 5 gives the same signed comparison with matching coefficients; Theorem 6 asserts a quasi-isomorphism for a particular critical quotient in the idempotent case. These are not raw tensor-space bijectivity statements. The arrow on cochains is reversed by precomposition.

Lebed's module definition does not require invertible generator actions. Consequently the zero-character module is legitimate, although it is distinct from the usual monoid-trivial module. In *Plactic monoids*, pages 17--18 explicitly discuss quasi-isomorphism and distinguish the constant character from the character zero on nonempty words.

## Degree three obstruction and descent

Over a field extension containing \(i^2=-1\), take
\(u_j=\sum_{a=0}^3 i^{-ja}x_a\). The Fourier change of basis is invertible because 4 is invertible. Directly,
\(r(u_a\otimes u_b)=i^a u_b\otimes u_a\).

In the ordered basis
\((u_1u_1u_0,u_1u_0u_1,u_0u_1u_1)\), the independently recomputed matrix is

\[
\begin{pmatrix}
1-i&-1+i&1-i\\
-1-i&2&-1+i\\
-1+i&-1-i&1-i
\end{pmatrix}.
\]

The row \((i,1+i,1)\) annihilates it, and its upper-left 2-by-2 minor is \(-2i\). It therefore has rank exactly 2 in every characteristic allowed here. Every adjacent pair in these three tensors belongs to \(R\). Multidegree preservation then makes \(u_0u_1u_1\) a member of \(K_3\) outside \(B_3\).

The cycle formed from its two endpoint placements is nonzero in degree-2 homology. A degree-3 boundary of weight 3 would have to come from \(B_3\), and the projection to the outer-weight summand \((1,2,0)\) recovers its middle tensor injectively. The missing tensor consequently cannot be supplied by another boundary. Other weights cannot contribute.

The conjugate Fourier multidegree gives a second independent class. Their real and imaginary combinations have coefficients in the original field. Since 2 and \(i\) are invertible, independence descends. This descent does not require complex conjugation to be an automorphism of the original field: the two root choices define two distinct Fourier multidegrees, and the displayed invertible linear change between the two classes and their rational-coordinate combinations is sufficient. Field extension is faithfully flat and commutes with the homology in question.

For zero-character Hochschild chains, endpoints vanish and the weight-3 part of degree 3 has kernel exactly \(K_3\); degree 4 has no weight-3 chains. Thus \(HH_3(A;k_0)_3=K_3\). Every comparison with degree-3 image contained in \(B_3\) misses the exhibited class. This proves the stated quantifier over every factoring chain quotient, not merely the specific quotient by \(\ker Q\).

The cohomological witness is equally valid: a functional on \(V^{\otimes3}\) annihilating \(B_3\) but not \(K_3\), extended by zero to other weights, is a Hochschild cocycle. It is not a coboundary because it detects a cycle. Its pullback under QS is identically zero. No finite-dimensional-duality shortcut or reversed-arrow ambiguity is required.

## Constant character quotient

For \(k_1\), \(\epsilon_1(u_0)=4\) and \(\epsilon_1(u_j)=0\) for \(j\ne0\). Braiding a letter to the left multiplies it by the eigenvalues of the preceding letters; moving the letter to the right contributes a power of its own eigenvalue. After endpoint evaluation, only zero-index letters survive. Thus the inspected source convention gives exactly

\[
d(u_{j_1}\cdots u_{j_n})=
4\sum_{s:j_s=0}(-1)^{s-1}
\left(i^{j_1+\cdots+j_{s-1}}-1\right)
 u_{j_1}\cdots\widehat{u_{j_s}}\cdots u_{j_n}.
\]

The differential preserves the ordered list of nonzero-index letters. In a nonempty such block, choose the gap immediately following the first nonzero letter \(u_b\). The coefficient for deleting one zero-index letter in that gap is \(c=4(i^b-1)\), which is nonzero for every \(b\in\{1,2,3\}\). If the initial gap has length \(a_0\) and the chosen gap has even length, insert one \(u_0\) in the chosen gap with coefficient \((-1)^{a_0+1}/c\); otherwise set the homotopy to zero.

Deletion in the chosen gap gives the identity in \(dh+hd\), because its alternating sum is zero for an even gap and one signed term for an odd gap. Initial-gap deletions have coefficient zero. Each later-gap deletion anticommutes with the insertion because the insertion shifts its position by one. This proves the contraction in every degree. It leaves exactly the lines \(k u_0^{\otimes n}\) as homology.

The proposed subcomplex has those lines only for \(n\ge2\). It is closed under the differential and is killed by QS because the alternating sum of permutation signs vanishes. The quotient has homology \(k,k,0,0,\ldots\). This conclusion includes the degree-2/degree-1 boundary of the definition: the long exact sequence gives no extra degree-2 class because the degree-2 inclusion is already an isomorphism on homology and the subcomplex has zero degree 1.

For the target, set \(t=u_0\) and let \(J\) be the ideal generated by the other Fourier letters. The relations give \(tJ=Jt=0\) and the vector-space decomposition \(A_L=L[t]\oplus J\). Projection killing the other letters proves that the polynomial summand has no extra relations and has zero intersection with \(J\). Multiplication by the central element \(t-4\) is injective: it is polynomial multiplication on \(L[t]\) and the nonzero scalar \(-4\) on \(J\). Its cokernel is the character module, because \(t=4\) forces \(J=0\). The resulting two-term free resolution is defined over the original field and exactness descends faithfully.

For the same one-dimensional character on both sides, Hochschild chains and the two-sided bar complex for \(\operatorname{Tor}^A(k_1,k_1)\) have identical formulas: their two endpoint actions are both scalar evaluation at that character. Thus the two-term resolution computes \(HH_n(A;k_1)=k,k,0,\ldots\).

The comparison is an isomorphism in degree 0. In degree 1, the character derivation \(\delta(x_a)=1\) is well-defined: it vanishes on every quadratic defining relation, and the character-derivation identity then makes it vanish on the ideal they generate. It detects \(QS_1(t)=t\) with value 4. Hence the degree-1 homology map is nonzero between one-dimensional spaces. This establishes the all-degree quasi-isomorphism. Algebraic dualization over a field is exact, so its cohomological version also follows.

## Independent computation

The accompanying audit program was written from the definitions. It neither executes nor imports Ferudun's ZIP or the candidate's checker. It builds the original \(X\)-basis matrices, obtains the quadratic relation basis from the two 8-element permutation orbits, and computes the adjacent-product constraints and weight-3 boundary matrix independently.

Over \(\mathbb Q\), it gives:

- \(\operatorname{rank}Q_2=14\), \(\operatorname{rank}Q_3=47\), \(\dim K_3=49\).
- Adding the two real-coordinate witnesses raises the image rank to 49.
- \(\dim C_{2,3}=112\), \(\operatorname{rank}d_{2,3}=63\), so \(\dim H_2(C)_3=2\).

Odd-prime checks for 3, 5, 7, 11, 13, 17, and 19 preserve the independence of the two witnesses. **At characteristic 3, the complete degree-3 rank changes:** \(\operatorname{rank}Q_3=46\), \(\dim K_3=49\), and \(\operatorname{rank}d_{2,3}=63\), giving \(\dim H_2(C)_3=3\). The two witnesses increase rank 46 to 48. Consequently “two independent classes” is uniform in odd characteristic; “exactly two” is not and must remain restricted to the rational computation. This is an independently observed finite-field check, additional to the symbolic two-class argument.

The original-basis face simplification was checked on all 5,461 words of degrees 0 through 6. The Fourier differential, its square, and the contraction identity were then checked using explicitly performed braid crossings on all 21,845 words of degrees 0 through 7 over each of \(\mathbb F_5,\mathbb F_{13},\mathbb F_{17}\), totaling 65,535 words. These finite tests supplement, rather than replace, the preceding all-degree proof.

## Source identity and limits

The inspected public sources are:

- [OWR Report 51/2019](https://ems.press/content/serial-article-files/46831?nt=1), Problem 2 on printed page 3237, PDF page 31, visually inspected. The question's contextual wording remains underqualified for the stronger interpretations discussed here.
- [Farinati and García Galofre arXiv v2](https://arxiv.org/abs/1508.07970v2), Definition 31/Theorem 32 and Corollaries 42--43/Question 44, pages 18 and 22--23. Page 18 was visually inspected; relevant neighboring statements were read in extracted text.
- [Lebed idempotent braidings arXiv v1](https://arxiv.org/abs/1607.08081v1), Definition 3.1 and Theorems 2, 5, 6, pages 8--10 and 19--20. Page 9 was visually inspected to confirm the face maps and signs; the other cited statements were read in extracted text.
- [Lebed Plactic monoids](https://arxiv.org/abs/1612.05768), pinned text pages 17--18, used only for the distinction between coefficient conventions and comparison notions.
- [Ferudun Zenodo record 23072076](https://zenodo.org/records/23072076), pinned PDF dated 1 October 2026, read in sections 1--3 and its scope remarks; pages 5--6 were visually inspected. The pinned manuscript calls itself unrefereed and discloses AI assistance. This audit accepts the scoped mathematical content above, not its full census or every other theorem.

All five pinned PDFs were rehashed. Their byte identities and this audit's inspection scope are recorded separately. No fresh exhaustive literature search, novelty certification, full dependency audit, global-dimension proof audit, characteristic-two result, or publication/contact action is part of this report.
