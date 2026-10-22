# Independent exact replacement of the finite Chow calculation

The decisive finite step is verified. In the integral Chow ring of the split symplectic Grassmannian (Y=\operatorname{IG}(5,16)=\operatorname{Sp}_{16}/P_5), the Appendix A class (a=2^8\widetilde z) has

\[
\nu_2(a^3)=22.
\]

Here divisibility is in the free integral Chow group, not in a rational or localized ring. An independently constructed integral complementary class gives the checkable witness

\[
\int_Y a^3c_2(T^*)^9c_3(T^*)
 =14668659594398531584
 =2^{22}\cdot3497280977821.
\]

This is a replacement computation. No Maple program, printed Maple coefficient, or Schubert word from the paper is an input to the executable checker. The proof of the lower divisibility also appears below; a pairing alone would only give the upper bound on the class valuation.

The target and source are Karpenko's [final preprint](https://sites.ualberta.ca/~karpenko/publ/spindI15.pdf), §§2–6 and Appendix A, and the [published version](https://doi.org/10.5565/PUBLMAT6722310), pp. 748–754. The source ledger records fresh byte identities and inspected scopes. This report independently checks the finite computation, while the passage from this Chow ring to generic Spin indices still invokes the paper's theorems.

## Exact geometry, normalization, and root conventions

Write (T) for the rank-five tautological bundle on (Y). Use formal roots (x_1,\ldots,x_5) of (T^*), and formal roots (\pm y_1,\pm y_2,\pm y_3) of the rank-six symplectic quotient (T^\perp/T). Put (u=x_1+\cdots+x_5). The polynomial being checked is exactly

\[
a=\prod_{(\epsilon_1,\epsilon_2,\epsilon_3)\in\{\pm1\}^3}
  (u+\epsilon_1y_1+\epsilon_2y_2+\epsilon_3y_3).
\]

In the spin weight lattice, each factor is twice one member of the orbit of (z). There are eight factors; hence (a=2^8\widetilde z). This fixes the nested exponent without relying on extraction of superscripts from PDF text. The source's (x_i) are roots of (T). Replacing all (x_i,y_j) by their negatives to use (T^*) leaves this degree-eight polynomial unchanged. The complementary class is allowed to use the dual bundle.

Under the Appendix A weight substitution, package weights numbered (8,7,\ldots,1) are the standard (C_8) fundamental weights numbered (1,2,\ldots,8). Thus its successive differences are the standard coordinate weights (x_1,\ldots,x_5,y_1,y_2,y_3). Erasing package root 4 erases standard root 5. The Levi system is (A_4\times C_3), with Weyl group (S_5\times W(C_3)). Consequently

\[
\dim Y=64-(10+9)=45,\qquad
|W(C_8)/W_P|=2^5\binom85=1792.
\]

The target cube has codimension 24. The complementary class has codimension (9\cdot2+3=21). No middle- or top-degree convention is being inferred from the source's Schubert words.

## An integral normalized polynomial and the lower bound

Let (e_i=e_i(x_1,\ldots,x_5)=c_i(T^*)), and let (h_j(x)) denote complete homogeneous symmetric polynomials. The tautological exact sequences give

\[
c(T)c(T^*)c(T^\perp/T)=1,
\qquad h_j(x_1^2,\ldots,x_5^2)=0\quad(j\ge4),
\]

because the last bundle has rank six. In particular these are integral relations, without any division by two.

For (q_i=e_i(y_1^2,y_2^2,y_3^2)), direct multiplication of the eight factors gives

\[
a=u^8-4q_1u^6+(6q_1^2-8q_2)u^4
 +(-4q_1^3+16q_1q_2-64q_3)u^2+(q_1^2-4q_2)^2.
\]

The ambient trivial symplectic bundle implies (q_i=(-1)^ih_i(x^2)) for (i=1,2,3). Substitute these expressions and call the resulting integral polynomial (A(e)). The checker verifies the free-polynomial identity

\[
A(e)=128b(e)+64h_4(x^2),
\]

where

\[
\begin{aligned}
b={}&-e_4^2-e_3e_5+2e_2e_3^2+5e_2^2e_4-2e_2^4
 +3e_1e_3e_4+4e_1e_2e_5-9e_1e_2^2e_3\\
 &-2e_1^2e_3^2-6e_1^2e_2e_4+7e_1^2e_2^3-e_1^3e_5
 +7e_1^3e_2e_3+e_1^4e_4-5e_1^4e_2^2-e_1^5e_3+e_1^6e_2.
\end{aligned}
\]

Therefore (a=128b) in the actual integral ring. A second free-polynomial identity, verified coefficient by coefficient modulo two, is

\[
b\equiv(e_1e_3+e_1^2e_2)h_4(x)+e_3h_5(x)+e_2h_6(x)+e_1h_7(x)+h_8(x)\pmod2.
\]

Squaring this identity in characteristic two replaces every (h_j(x)^2) by (h_j(x^2)). All five such terms vanish by the rank-six quotient relation. Hence (b^2=0) in \(\operatorname{CH}(Y)/2\), and (b^3\) is divisible by 2 integrally. Thus (a^3=2^{21}b^3\) is divisible by (2^{22}). This part requires neither the full ring presentation nor a claimed Schubert expansion.

## Entirely integer evaluation of the witness

Inside the ordinary Grassmannian \(\operatorname{Gr}(5,16)\), (Y\) is the smooth zero locus of the alternating form regarded as a section of \(\Lambda^2T^*\). Its codimension-ten class is

\[
\prod_{i<j}(x_i+x_j)=s_{(4,3,2,1,0)}(x).
\]

The equality follows immediately by dividing the alternant for the staircase Schur polynomial by the Vandermonde. Integration on \(\operatorname{Gr}(5,16)\) extracts the coefficient of \(s_{(11,11,11,11,11)}\) in a symmetric polynomial of degree 55. Equivalently it extracts \([x_1^{15}x_2^{14}x_3^{13}x_4^{12}x_5^{11}]f(x)\prod_{i<j}(x_i-x_j)\). The ordinary and symplectic coefficient formulas, with roots of the dual tautological bundle, are given in [Darondeau–Pragacz, *Universal Gysin formulas for flag bundles*](https://www.impan.pl/~pragacz/nur.pdf), introduction p. 3 and Theorems 1.1 and 2.1. Their proof iterates projective-bundle pushforward; no numerical approximation is involved.

The checker starts with the staircase partition, multiplies by (e_2^9e_3\), then three times by the explicitly generated polynomial (b\). Multiplication by (e_k\) uses the elementary vertical-strip Pieri identity, adding (k\) boxes in distinct rows. It keeps at most five rows and width eleven. Discarding a partition outside that rectangle cannot alter the target coefficient: all subsequent multiplications add boxes. Signed coefficients of (b\) are preserved as integers. The successive nonzero state counts are 176, 89, 18, and 1. The remaining coefficient is

\[
\int_Y b^3e_2^9e_3=6994561955642=2\cdot3497280977821.
\]

This is a direct finite integer artifact, not a test of a printed expected Schubert output. Two controls verify that the same Pieri operator gives coefficient one for (e_5^{11}\), and the independent hook-length value for (e_1^{55}\) on \(\operatorname{Gr}(5,16)\).

It follows that \((b^3/2)\bmod2\) is nonzero: its pairing with (e_2^9e_3\) is odd. A class divisible by (2^{23}\) has every integral complementary pairing divisible by (2^{23}\). Our witness violates that condition. Together with the lower bound above, this proves exact class valuation 22.

## Independent arithmetic cross-checks

The checker also evaluates the original eight-factor polynomial at all 1792 torus fixed points for each of three unrelated sets of nonzero weights with distinct absolute values. For a signed subset (x\) of size five and the three unused positive weights (y\), the tangent denominator is

\[
\prod_{i\le j}(x_i+x_j)\prod_{i=1}^5\prod_{j=1}^3(x_i^2-y_j^2).
\]

These are the 15 weights of \(\operatorname{Sym}^2T^*\) and the 30 weights from the quotient. The numerator is (a(x,y)^3e_2(x)^9e_3(x)\). All rational fractions are exact and their sum is the same integer (14668659594398531584\). This checks the standard-root parabolic, class formula, dimension, signs, and normalization against the integer Schur route.

A third evaluation uses 4368 ordinary \(\operatorname{Gr}(5,16)\) fixed points with 16 distinct weights and the eliminated polynomial (A(e)\), including the isotropic zero-locus factor. It agrees as well. Small geometry controls give degree 1 for \(\operatorname{IG}(1,6)=\mathbf P^5\) and degree 2 for \(\operatorname{IG}(2,4)\), a quadric threefold. The integer Schur route is the main witness; the rational fixed-point routes are supplementary and do not define the normalized class.

## What follows and what remains a citation dependency

In Karpenko's notation, (n=8,m=5,l=3,j=3\). The relevant codimension is (j2^l=24\le45\), and the independently verified exponent is (k_3=22\). Consequently the maximum deficiency in Theorem 4.1 is at least (24-22=2\), giving \(\operatorname{ind}X_5\mid2^{5-2}=8\). The smaller fourth Grassmannian has index dividing that of the fifth. The odd-to-even subform and generic-index arguments in §6 then yield the needed Spin18 fourth-index upper bound 8.

The identification of the Chern subring (C\) with \(\operatorname{CH}(Y)\), the generic odd-spin rational-Chow description (Theorem 3.6), and the index formula (Theorem 4.1) remain cited mathematical inputs. This family does not independently reprove them, the generic-specialization bridge, or the later gamma-filtration implication. It does not claim a full proof-assistant formalization or external human review. It independently replaces the previously un-replayed finite Maple step, and its conclusion agrees with the published calculation. No new Spin index theorem or novelty claim is asserted.

## Reproduction and custody

Run `python3 check_chow.py` from this folder; Python 3.9 or later and its standard library suffice. It reads no source files and requires no network. The included `results.json` is deterministic. Fresh normal, `-O`, and `-OO` runs all passed and produced byte-identical output; the run receipt records interpreter version, code hash, and output hashes. Every check uses an explicit exception, so optimization cannot remove validation.

Only authored analysis, self-contained code, and result/identity receipts are public artifacts. Fetched PDFs, extracted source text, exploratory scripts, and scratch outputs remain under ignored `_local/` and are excluded from the explicit manifest. Input absolute paths in the ledger are receipts, not membership declarations. No other review family's contents were read and no external individual was contacted. The parent agent is responsible for integration and publication; this family performed no Git index, checkout, reference, commit, push, or release mutation.
