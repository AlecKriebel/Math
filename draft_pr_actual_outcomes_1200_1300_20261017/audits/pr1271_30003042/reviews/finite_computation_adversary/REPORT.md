# Adversarial review of the exact finite Chow certificate

**Verdict: no mathematical counterexample found; the claimed finite certificate is independently verified.** The frozen calculation gives

\[
 \nu_2\bigl(a^3\in\mathrm{CH}(\mathrm{IG}(5,16))\bigr)=22,
 \qquad
 \int a^3c_2(T^*)^9c_3(T^*)=14668659594398531584.
\]

This is an actual mathematical review of the proof and executable calculation. It is not publication clearance and does not establish the entire original problem or its novelty. The strongest independently verified result and exact scope are recorded below.

## Inputs, independence, and primary reading

The root-supplied `INPUT_FREEZE.json` is preserved unchanged. `INITIAL_AUTHENTICATION.json` authenticates its two files before review. The candidate's later completed report and manifest were read only after initial independent code/primary reading, and authenticated separately in `ADDITIONAL_INPUT_AUTHENTICATION.json`; all nine manifest entries match. No other mathematical review family's contents were read. Candidate code was copied only into this family's ignored `_local/`, replayed there, and produced output identical to the frozen `results.json`.

I independently downloaded [Karpenko's primary preprint](https://sites.ualberta.ca/~karpenko/publ/spindI15.pdf), read §§2–6 and Appendix A, and visually inspected Appendix A p. 9. I also independently read the type-A/type-C coefficient formulas and projective-bundle proof in [Darondeau–Pragacz](https://www.impan.pl/~pragacz/nur.pdf), introduction p. 3 and Theorem 1.1. Exact retrieval hashes and raw locations are receipts in `PRIMARY_RETRIEVAL.json`; raw PDFs are excluded from authored membership.

Source dependencies are explicit: Karpenko identifies the Chern subring with the symplectic Grassmannian Chow ring, proves rationality of the orbit product in Proposition 3.4, and gives the index formula in Theorem 4.1. The odd-to-even transfer uses §6 and generic specialization. These structural results are cited, rather than independently reproved here.

## Normalization and the printed-source typo

The spin-lattice relation is

\[
 2z=x_1+\cdots+x_5+y_1+y_2+y_3.
\]

The eight orbit factors are \((u\pm y_1\pm y_2\pm y_3)/2\). Therefore the actual Appendix A displayed product is

\[
 a=\prod_{\epsilon\in\{\pm1\}^3}(u+\epsilon_1y_1+\epsilon_2y_2+\epsilon_3y_3)
   =2^8\widetilde z.
\]

**Minor source-description correction:** the preprint's Appendix A prose visibly prints \(2^3\widetilde z\), rather than \(2^{2^3}\widetilde z\). This is an actual printed typo, not merely damaged text extraction. The displayed eight-factor expression, the lattice relation, and the earlier nested exponent determine the intended normalization unambiguously. The candidate uses the correct normalization; its report could explicitly acknowledge the typo. No numeric or proof correction is required.

Replacing the source's tautological roots by the roots of the dual changes all roots' signs. The degree-eight polynomial is unchanged. Using \(e_i=c_i(T^*)\) for the complementary class is integral and legitimate.

## Parabolic, tangent, and normal geometry

The standard type-C maximal parabolic is \(P_5\), with Levi \(A_4\times C_3\). Appendix A reverses the package numbering, so deleting package root 4 deletes standard root 5. There are \(64-10-9=45\) positive roots outside the Levi, and \(2^5\binom85=1792\) fixed points. In contrast, standard \(P_4\) has dimension 42 and 1120 fixed points. Thus the calculation's degree 45 and fixed-point count distinguish the relevant parabolics.

With roots of \(T^*\), the tangent roots are

\[
 2x_i,\quad x_i+x_j\ (i<j),\quad x_i+y_r,\quad x_i-y_r.
\]

Their Euler product is exactly the candidate denominator. The independent checker generates this list from the type-C root pattern, rather than importing the candidate denominator. There are 15 roots from \(\mathrm{Sym}^2T^*\) and 30 mixed roots. Projective-space and quadric controls fix orientation.

The embedding into \(\mathrm{Gr}(5,16)\) is the smooth zero locus of the alternating form as a section of \(\Lambda^2T^*\), with codimension ten. Its normal top Chern class is

\[
 \prod_{i<j}(x_i+x_j)=s_{(4,3,2,1,0)}(x).
\]

The Schur identity follows directly by dividing the staircase alternant \(\Delta(x^2)\) by \(\Delta(x)\). No extra factor of two occurs. The normal bundle uses exterior square; the symplectic tangent contribution uses symmetric square. They play different roles and are both correct in the candidate.

## Integral lower divisibility: no hidden division by two

For the symplectic quotient \(Q=T^\perp/T\) of rank six,

\[
 c(T)c(T^*)c(Q)=1,\qquad
 c(Q)=\prod_i(1-x_i^2)^{-1}.
\]

Consequently \(h_j(x^2)=c_{2j}(Q)=0\) integrally for every \(j\ge4\). These vanishings require only the exact sequences and rank, not a full presentation of the Chow ring.

The candidate's exact polynomial normalization \(A=128b+64h_4(x^2)\) holds before passing to the ring; hence \(a=128b\) in the integral ring. I independently reconstructed this identity in the five root variables, rather than the candidate's five elementary variables. The resulting root polynomial has 490 monomials. Every coefficient in \(A-64h_4(x^2)\) is a multiple of 128.

The second identity is

\[
 b\equiv(e_1e_3+e_1^2e_2)h_4(x)+e_3h_5(x)+e_2h_6(x)+e_1h_7(x)+h_8(x)\pmod2.
\]

It too passes an independent coefficient-by-coefficient root-variable check. Importantly, ordinary \(h_j(x)\) are not declared zero. One first squares this identity in the commutative characteristic-two quotient. Frobenius gives \(h_j(x)^2=h_j(x^2)\), checked separately in the free polynomial ring for \(j=4,\ldots,8\). The rank-six relations then give \(b^2=0\) modulo two. Thus \(b^2\in2\mathrm{CH}(Y)\), also \(b^3\in2\mathrm{CH}(Y)\), and \(a^3\in2^{22}\mathrm{CH}(Y)\).

This implication is integral. It neither assumes that rational-ring denominators are integral nor infers the lower bound from a single pairing. The cellular Chow group is free, so its nonzero class valuation is well defined.

## Independent exact arithmetic and adversarial controls

`check_independent.py` imports no candidate code, reads no candidate results, and contains no expected target pairing. It uses integer root-monomial multiplication and Vandermonde coefficient extraction, with no Pieri operation. Let \(P=b^3e_2^9e_3\). Rectangle/complement duality gives

\[
 \int_{\mathrm{Gr}(5,16)}s_{(4,3,2,1,0)}P
   =[s_{(11,10,9,8,7)}]P
   =[x^{(15,13,11,9,7)}]\,P\Delta(x).
\]

The last formula follows from the Schur alternant: strictly decreasing target exponents pick out the indicated unique partition. The complementary partition identity follows from perfect Schur duality in the \(5\times11\) rectangle. Negative coefficients and cancellation are retained as arbitrary-precision integers. Pruning exponents above the extraction bounds is safe because later factors have nonnegative exponents.

The checker records the 120 signed determinant contributions and independently obtains

\[
 \int b^3e_2^9e_3=6994561955642
     =2\cdot3497280977821.
\]

Multiplication by \(128^3\) produces the claimed witness. Independently enumerated quotient-root localization at the new signed/permuted weights \((103,-13,47,5,79,-31,17,61)\) returns the identical integer from 1792 fixed points. The numerator in that route is the original eight-factor product, without eliminating the residual roots. All rational arithmetic is exact.

Small-geometry controls yield degree one for \(\mathrm{IG}(1,2n)=\mathbf P^{2n-1}\), \(n=1,2,3,4\), degree two for \(\mathrm{LG}(2,4)\), and degree sixteen for \(\mathrm{LG}(3,6)\). Omitting the long roots changes the quadric control from 2 to 20; reversing every tangent root changes it to -2. These mutations demonstrate detection of a missing-power-of-two normalization and orientation reversal.

The candidate's separate vertical-strip Pieri routine is also mathematically correct: choosing distinct rows implements multiplication by an elementary symmetric function, retaining weakly decreasing partitions. A discarded partition outside the rectangle cannot return to it by later additions. Its hook-length and determinant controls and three arithmetic routes pass on replay. The independent monomial route avoids relying on those implementation choices.

Since an integral class divisible by \(2^{23}\) has every integral pairing divisible by \(2^{23}\), the witness proves \(\nu_2(a^3)\le22\). Combined with the lower proof, it proves **exact class valuation 22**, not merely valuation of this one number.

## Precise index consequence and remaining dependencies

For \(n=8,m=5,l=3\), the tested power is \(j=3\) and its deficiency is \(j2^l-k_j=24-22=2\). The maximum in Theorem 4.1 is therefore at least two, so the generic Spin17 fifth index divides eight. This does not evaluate the other powers \(j=0,\ldots,5\), and by itself does not prove the index equals eight.

A direct upper-bound argument uses fewer structural inputs. Proposition 3.4 supplies a rational class \(\widetilde z\). The Chern-ring identification transfers top degree from \(Y\) to the split odd orthogonal Grassmannian with multiplier \(2^5\). Therefore the rational zero-cycle \(\widetilde z^3e_2^9e_3\) has degree

\[
 2^5\frac{14668659594398531584}{2^{24}}
 =27978247822568=8\cdot3497280977821.
\]

With the known two-primary index this directly proves the index divides eight. Theorem 3.6's full generator statement is needed for the equality theorem route, but is not needed for this direct upper argument. The lower-divisibility proof is needed for exact class valuation; the displayed degree witness alone suffices for the upper-bound consequence with these structural inputs.

The flag incidence correspondence gives \(\operatorname{ind}(X_4)\mid\operatorname{ind}(X_5)\). Generic specialization and the codimension-one subform inclusion, as used in §6, then transfer this upper bound to the Spin18 fourth index. Those generic/orthogonal facts have not been independently reconstructed from first principles in this review. Exact Spin index eight requires an additional lower-index argument. The later gamma-filtration conclusion is outside this review.

**Remaining finite gap:** none within the stated integral Chow, Schur-duality, and localization framework. **Remaining whole-project dependencies:** the published rationality/Chern-ring identification, degree transfer, two-primary generic-index facts and specialization/subform passage, plus whatever later implication the original project uses. These must remain citations, not be presented as consequences of executable arithmetic alone.

## Reproduction and custody

Run `python3 check_independent.py` in this family directory. Its deterministic output is `INDEPENDENT_RESULTS.json`; the candidate replay receipt is separate. All fetched primary bytes, screenshots, copied candidate code, and scratch outputs are under ignored `_local/`. `MANIFEST.json` explicitly lists only this family's authored files, excludes itself and raw/input membership, and is created after final reauthentication. No Git index/ref/branch/push/release operation was performed; no external individual or other computation agent was contacted.
