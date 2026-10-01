# Independent source/proof review: 10400219

## Binding verdict

**PASS_COMPLETE_CREDITED_SOURCE_CORRECTION. No mandatory correction.** Recommend **already_solved, 0/5 new author turns**.

The verdict binds STATUS_CORRECTION.md SHA-256 `4d0faeda8ce34c89683fd03e8b824b8cba902bd12d74ac6a880ef2ad7b77eb93`, SOURCE_AUDIT.md SHA-256 `f48dd43d1d1b7a9f9beffcfb8088b8516dbaa30ceb349327fa6091a8c52fd9dc`, and FROZEN_MANIFEST.json SHA-256 `0e7949ca3d3be30ce1d0e92145e2324048be780b5b0d0d00cd469281b5c811ee`.

All nine bound author files and both primary PDFs hash-match. The source-arithmetic receipt replays byte-for-byte. I did not contribute to this source-correction packet. This is a separate AI source and mathematical audit, not human peer review or priority certification.

## Exact question, edition and credit

I visually inspected the actual Ohtsuki page, printed 538 / PDF 166. Problem 12.14 asks Askitas's question about reaching a slice knot with a number of ordinary crossing changes equal to the embedded four-ball genus. The immediately following Update explicitly records Livingston's negative answer using 7_4. Livingston's opening paragraph calls the earlier-numbered question 12.1 and repeats the same wording; this is an edition/numbering change, not a different problem. The compilation is in volume 4 (2002), with the final article front matter dated 1 June 2004.

I read all ten pages of the [published Livingston article](https://msp.org/agt/2002/2-2/agt-v2-n2-p14-p.pdf), including its final addendum. The counterexample concerns the total ordinary slicing number u_s. The signed maximum U_s, generalized twists, and later gap conjectures are different questions and are not marked solved here. The addendum acknowledges an earlier 8_16 example from Murakami–Yasuhara; no first-priority claim is justified or made.

The obstruction uses Alexander factorization and a metabolizer for the double-cover linking form. These are necessary for a smooth slice disk and also for a locally flat topological slice disk. Thus no switch to immersed disks or wild embeddings is involved. The source's usual embedded slice category is safely covered.

## Geometric scope of the published proof

The argument is not a search over crossings of one diagram. Section 2 starts with an arbitrary crossing disk. In the two-fold cover its lift is an annulus, and either boundary lift is isotopic to its core. The crossing modification becomes odd-half-integral surgery on that core. The Figure 1 auxiliary surgery representation then arranges the crossing arc to avoid the disk bounded by K', by handle slides. This is why the S-to-K' entries in the equivariant presentation vanish for an arbitrary proposed crossing change.

I checked the entire derivation through the infinite-cyclic and double covers, with Figure 1 and p. 1057 rendered. The arbitrary crossing data remain in the unknown Laurent polynomials f and g; the proof does not constrain them to a finite family. The relations f(1)=±1 and g(1)=0 have the stated surgery and disk-linking origins. Reducing g modulo t²−1 correctly sums the even and odd lift-linking coefficients. This geometric derivation is a credited published input, not something the finite checker alone establishes.

For the elementary bounds, the double-twist diagram has a genus-one Seifert surface. Its determinant is 15, so it is not slice and the four-genus is exactly one. In the rational-tangle convention [4,−4], changing two crossings in the four-crossing twist box reduces that box to zero; [0,−4] has numerator −1 and is an unknot. This verifies the ordinary two-change upper bound. The published one-change obstruction is what distinguishes slicing number two from merely unknotting number two.

## Independent algebraic audit

Eliminating the −2 auxiliary entry from the three-by-three matrix gives the determinant

$$
 f(t)(4t-7+4t^{-1})+2g(t)g(t^{-1}).
$$

Put F(t)=4t²−7t+4. Its discriminant is −15 and it is primitive and irreducible. In the field Q[t]/(F), conjugation sends t to 7/4−t=t^{-1}. This independently verifies that the reciprocal roots are (7±sqrt(−15))/8. The printed denominator 4 on p. 1057 is genuinely erroneous: it gives a root product 4 rather than 1 and does not annihilate F.

With the corrected root, the slice factorization and the determinant identity would force a rational field element of norm ±2 unless g vanishes at that root. Writing such an element as (a+b sqrt(−15))/c in primitive integers gives a²+15b²=±2c². Reduction modulo 5 forces 5 to divide a and c, because neither 2 nor −2 is a quadratic residue; reduction modulo 25 then forces 5 to divide b. This contradicts primitivity. The later valuation paragraph in the printed proof is unnecessary. Thus the denominator correction leaves a complete, elementary norm obstruction rather than an unsupported repair.

It follows that F divides g rationally. Primitive-polynomial Gauss divisibility makes the quotient integral after clearing Laurent powers. Since g(1)=0 and F(1)=1, one obtains g=(t−1)Fh with integral Laurent h. Direct reduction in Z[t]/(t²−1) gives the even/odd pair (−15h(−1),15h(−1)). Hence the crossing lift is null homologous in L(15,4).

After the null-homologous slide, the two surgery summands have linking values 4/15 and 2/p, where p is odd. Square order forces p=±3^(2j+1)5^(2k+1)q² with q coprime to 30. On the 5-primary part the form is diagonal on Z/5 plus Z/5^(2k+1), with first entry 2/5 and a second numerator that is a square unit modulo 5. A self-isotropic vector with nonzero first coordinate would require a square congruent to ±2. Therefore every isotropic vector has first coordinate zero and second coordinate divisible by 5^(k+1). They comprise only 5^k elements, whereas a metabolizer requires 5^(k+1). This proves the incompatible conclusion required by Theorems 3.1 and 4.1.

The surgery coefficient p=0 is not an overlooked case: p is odd. Orientation reversal changes the overall form sign without changing metabolicity, and both signs of p are covered.

## Controls and final disposition

The author checker was inspected before replay and its 33,689-assertion output matches exactly. A separately written checker passes **167,573 exact assertions**, using a different quadratic-field presentation, a square-class formulation of the primary linking form, complete finite isotropic-vector sets, rational slide algebra, and direct reduction in Z[t]/(t²−1). These finite checks support but do not replace the published topological proof or the written all-exponent argument.

The original source already identifies the complete counterexample. This packet correctly restores that known status, with classical credit and no new substantive author turn. No mandatory mathematical or source-scope change is needed. Five portable review files are supplied: this report, the hash/replay receipt, the independent checker and its receipt, and the review manifest. Exclude author_replay/ and any source-reading material. The parent retains the publication gate.
