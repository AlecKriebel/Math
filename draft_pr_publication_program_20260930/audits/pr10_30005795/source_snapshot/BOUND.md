# A known log-canonical-threshold bound for the negative-part integral

**Record:** 30005795 / OWR-14298162-002  
**Assessment:** source correction and reconstruction of an existing method; no new mathematical discovery claimed  
**Checked:** 2026-09-30 UTC  
**Execution model:** gpt-6-astra, xhigh (not ultra)

## 1. What the source actually asks

The relevant source is Ivan Cheltsov and Elena Denisova, *Calabi problem for smooth Fano threefolds*, in Oberwolfach Report 14/2024, pp. 836–843. Section 1 chooses a surface S with Du Val singularities. Section 3, p. 839, discusses the contribution of the negative part of the Zariski decomposition of -K_X-uS. The question is followed immediately by a worked log-canonical example on p. 840.

The final quantifier on p. 839 says “for every prime divisor F over X.” This is a genuine printed typo, visually checked in the PDF, not merely an extraction error. The expressions ord_F(N(u)|_S) and A_S(F) instead require a prime divisor **over S**. The preceding formulas and the following example use that correct domain. Moreover, the cleaned dataset statement omits the Du Val hypothesis inherited from Section 1. We restore both explicitly rather than claiming to solve the ill-defined literal sentence.

Put V=(-K_X)^3 and w(u)=3(P(u)^2·S)/V. In the source's nef-restriction setup w(u)≥0. The intended task is to bound

\[
 I(F)=\int_0^\tau w(u)\operatorname{ord}_F(N(u)|_S)\,du
\]

by K A_S(F). The application only needs divisors whose center on S contains the distinguished point P. A global version covering every prime divisor over S is also available.

## 2. The bound

Suppose

\[
 N(u)|_S=\sum_{j=1}^r f_j(u)D_j,
 \qquad f_j(u)\ge0,
\]

where D_j are fixed effective Cartier divisors on the klt surface S and the integrals below are finite. Write

\[
 a_j=\int_0^\tau w(u)f_j(u)\,du,
 \qquad c_j=\operatorname{lct}(S;D_j).
\]

Discard D_j=0. Each remaining global threshold c_j is strictly positive. Then

\[
 \boxed{K_0=\sum_{j=1}^r\frac{a_j}{c_j}}
\]

satisfies I(F)≤K_0 A_S(F) for **every** prime divisor F over S. If the question insists on K>0 even when I vanishes identically, take K=1+K_0.

For the local application use c_{j,P}=lct_P(S;D_j) instead and restrict to P∈c_S(F). If P is outside the support of D_j, its local threshold is infinite and its contribution is zero. Local thresholds cannot silently be substituted into a claim about all centers on S.

### Proof

For a prime divisor F over S, log canonicity of (S,c_jD_j) gives

\[
 A_S(F)-c_j\operatorname{ord}_F(D_j)\ge0.
\]

The required endpoint log canonicity, as well as c_j>0, follows by computing the threshold on a log resolution of (S,D_j): all discrepancies of the klt surface are positive, and there are only finitely many relevant coefficients. Consequently

\[
 \begin{aligned}
 I(F)
 &=\sum_j a_j\operatorname{ord}_F(D_j)\\
 &\le\sum_j\frac{a_j}{c_j}A_S(F)
 =K_0A_S(F).
 \end{aligned}
\]

This uses only a finite sum, nonnegative weights and the definition of the log canonical threshold. The same argument on a neighborhood of P proves the local assertion. ∎

## 3. Why the finiteness assumptions fit the Fano setup

A smooth complex Fano variety is a Mori dream space by Birkar–Cascini–Hacon–McKernan, Corollary 1.3.2. Its finite Mori chamber decomposition gives finite-support, chamberwise linear negative parts; see also Okawa, *On images of Mori dream spaces*, §2.3. Along the compact segment -K_X-uS, the coefficient functions are bounded and piecewise linear, and the intersection weight is bounded and piecewise polynomial. Thus every a_j above is finite. The relevant negative prime divisors E_j on X restrict to effective Cartier divisors D_j=E_j|_S because X is smooth and E_j≠S.

For completeness, S is not a fixed divisorial component along this segment. At its effective endpoint D_tau=-K_X-τS, any effective representative containing bS with b>0 would give an effective representative of -K_X-(τ+b)S, contradicting the definition of τ. Such an endpoint representative exists on a Mori dream space. A convex combination with an effective representative of -K_X avoiding S then supplies representatives avoiding S for the remaining segment. Hence the asymptotic fixed coefficient along S is zero.

This discussion uses the usual Mori-dream-space/divisorial interpretation of the negative part, rather than asserting that all positive parts are nef on the original threefold. In the setting explicitly used in the report, P(u)|_S is nef, which is enough for w≥0. Even if one instead works with a chamberwise divisor on the original model and its intersection weight has either sign, replacing w by max(w,0) in a_j gives a finite upper bound for the original integral, since all valuation orders of the restricted negative part are nonnegative.

## 4. Optimal constant, when desired

For the nonnegative-weight setup set B=Σ_j a_jD_j. Linearity gives I(F)=ord_F(B). Therefore the least nonnegative global constant is

\[
 K_{\rm opt}=\sup_F\frac{\operatorname{ord}_F(B)}{A_S(F)}
 =\frac1{\operatorname{lct}(S;B)}.
\]

Use the convention K_opt=0 when B=0. This is a characterization and a finite log-resolution computation, not a numerical value independent of X and S. The componentwise bound K_0 may be larger than K_opt; it does not assume the threshold of a sum equals a sum of thresholds. Neither formula by itself guarantees a strong enough bound to prove K-stability in a particular family.

## 5. Prior literature and classification

Cheltsov–Fujita–Kishimoto–Okada, *K-stable divisors in P¹×P¹×P² of degree (1,1,2)*, Nagoya Mathematical Journal 251 (2023), 686–714, Appendix B, **Lemma 27**, explicitly proves the componentwise local estimate above. Its first inequality is precisely the negative-part contribution with c_j=lct_P(S;E_j|_S). The displayed second inequality uses a del Pezzo fibration assumption; the first inequality and its one-line proof do not use that assumption. The author-hosted preprint numbers the same result **Lemma 26**. These numbering differences were checked.

That 2023 paper is reference [3] in the 2024 lecture report. The report's method question should therefore not be advertised as a newly solved 2024 open problem. The appropriate disposition is **known bound / source-status correction**, with a statement-repair warning. Upstream record 30005796 is explicitly another extraction of the same question and should not receive a separate research budget or discovery credit.

No claim is made that every effective threshold or best application-specific K is easy to compute, that there is a universal K independent of the input, or that the original report poses a new sharp-constant conjecture. No such stronger target was identified.

## Sources

1. Cheltsov–Denisova contribution, [official OWR PDF](https://ems.press/content/serial-article-files/48650), pp. 836–840 and bibliography p. 843; DOI [10.4171/OWR/2024/14](https://doi.org/10.4171/OWR/2024/14).
2. Cheltsov–Fujita–Kishimoto–Okada, [published article, Appendix B, Lemma 27](https://www.cambridge.org/core/journals/nagoya-mathematical-journal/article/kstable-divisors-in-mathbb-p1times-mathbb-p1times-mathbb-p2-of-degree-112/999FB6032A21485AD71CF230CC802E6C), DOI [10.1017/nmj.2023.5](https://doi.org/10.1017/nmj.2023.5).
3. Same authors, [author-hosted preprint, Appendix B, Lemma 26](https://www.maths.ed.ac.uk/cheltsov/pdf/220608539.pdf).
4. Birkar–Cascini–Hacon–McKernan, [*Existence of minimal models for varieties of log general type*](https://www.ams.org/jams/2010-23-02/S0894-0347-09-00649-3/viewer/), JAMS 23 (2010), Corollary 1.3.2.
5. Okawa, [*On images of Mori dream spaces*](https://arxiv.org/abs/1104.1326), §2.3 on chamberwise Zariski decompositions.
