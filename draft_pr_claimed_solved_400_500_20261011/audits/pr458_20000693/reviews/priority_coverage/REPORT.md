# Independent primary-literature priority and coverage audit

PR458; problem `20000693`; frozen head `87a39f7b4e5ef81aacf98464f86586cc95684d7f`. This report addresses priority and coverage of the fixed, finite, unshifted Dirichlet-product heuristic. It does not authorize publication, classification, merge, or a gate action.

The displayed integer-product core has explicit prior heuristic coverage. Heap2013 supplies the multiplicity-square exponent, constituent Barnes factors, and coefficient-square Euler product. Sahay2021 supplies the complete common-modulus integer Dirichlet-product constant and a hybrid derivation. The frozen candidate enlarges the combined literal quantifiers to arbitrary independently chosen nonnegative real weights and arbitrary original fixed moduli. That enlargement requires explicit arguments, but it uses the same prime-phase and constituent CUE mechanisms. This audit finds no demonstrated new moment-model mechanism or proved general high-moment asymptotic.

The source asks for a heuristic. Lack of a theorem for the actual general moments is therefore not, by itself, failure to meet that target. A repaired, clearly attributed synthesis can satisfy the declared Dirichlet example. The original frozen packet still needs its finite-cutoff explanation and Keating–Snaith citation repaired. The present root clarification improves the mathematical record; it has not rewritten the frozen submission. An exact earlier single-source formula for the entire enlarged joint scope was not certified by this finite search. No exhaustive coverage, first-solver, or absence-of-novelty theorem follows.

## Input discipline and independence

The initial reconstruction is preserved in `INITIAL_CLAIM_MAP.md`, with `INITIAL_INPUT_BINDINGS.json` binding AIM's directly fetched primary page and frozen author files. It predates reading the frozen source review and present root `HYBRID_LOCAL_CLARIFICATION.md`, `ROOT_MODEL_RECONSTRUCTION.md`, and `CLAIM_LEDGER.md`. The parent task supplied preliminary mathematical framing; the frozen `SOURCE_GATE.md` supplied literature suggestions. These exposures are disclosed, not treated as independent evidence.

No sibling priority report or current root priority recommendation was read. `VERDICT_CHECKPOINT.md` preserves the independent provisional verdict before sealing. Parent messages supplied the correct Heap section reference and subsequently reported its own visual readings; neither supplied a priority disposition. All core primary PDFs used here were downloaded independently. Available root cached PDFs were not used to establish this family's hashes or primary formula comparisons. Foreign downloads, extracts, renders, and HTTP responses remain in `private_sources/` and are excluded from the positive public manifest.

`PRIMARY_SOURCES.json` gives URLs, access dates, byte counts, SHA256 values, versions, equation locations, and full-page visual-inspection receipts. `SEARCH_LOG.md` records the bounded search and unassessed discoveries. The PDF skill was used to render complete pages and inspect formulas visually. No original proof-search attempt, source edit, Git/index change, outreach, or publication action was performed.

## The literal source and the author-chosen scope

[AIM §5 Problem5.3](http://aimpl.org/zetamoments/5/), attributed to C. Turnage-Butterbaugh, asks for a heuristic for moments of imprimitive L-functions, or an L-function factoring into degree-one factors. Its example is

\[
 \int |L(\tfrac12+it,\chi_1)\cdots L(\tfrac12+it,\chi_k)|^2\,dt,
\]

followed by “or different powers.” The page does not specify bounds, exponent domain, growing-conductor uniformity, shifts, error terms, or a lower-order polynomial. Its problem status is blank in the fetched HTML. Neighboring Problem5.1 explicitly names Conrey–Keating ideas;5.3 does not prescribe a unique mechanism. The primary page's word *imprimitive* is not defined there. In this literature it can mean a reducible product of primitive lower-degree L-functions, rather than only a Dirichlet character induced from a smaller modulus.

The frozen author chooses a precise domain: a finite tuple of characters \(\chi_i\bmod q_i\), all \(q_i\) fixed, and fixed \(a_i\ge0\), with

\[
 I_{\mathbf a}(T)=\int_T^{2T}\prod_i|L(\tfrac12+it,\chi_i)|^{2a_i}\,dt.
\]

Let \(\psi_i\) be the primitive inducer. Group by equality of primitive characters and set

\[
 M_\psi=\sum_{i:\psi_i=\psi}a_i,
 \qquad E=\sum_\psi M_\psi^2,
 \qquad \mathcal G=\prod_\psi\frac{G(1+M_\psi)^2}{G(1+2M_\psi)}.
\]

For the branch analytic at zero and equal to one there, define

\[
 B_p(z)=\prod_i(1-\chi_i(p)z)^{-a_i}=\sum_{r\ge0}b_p(r)z^r,
\]
\[
 J_p=\sum_{r\ge0}|b_p(r)|^2p^{-r}
 =\frac1{2\pi}\int_0^{2\pi}\prod_i
 |1-\chi_i(p)e^{i\theta}/\sqrt p|^{-2a_i}\,d\theta.
\]

The proposed coefficient is \(\mathcal A\mathcal G\), where

\[
 \mathcal A=\lim_{y\to\infty}\prod_{p\le y}(1-p^{-1})^EJ_p,
 \qquad I_{\mathbf a}(T)\sim T\mathcal A\mathcal G(\log T)^E.
\tag{H}
\]

The prime limit is ordered. Finite deleted factors, principal characters, repetitions, distinct conjugates, and zero weights are included. Fixed conductor logarithms give the same leading term. Negative powers, growing weights/moduli, shifted or unbalanced moments, and universal higher-degree imprimitive families are outside this chosen scope. The source's broad request is not automatically resolved in all possible meanings of *imprimitive* by this domain choice.

## Exact primary coverage

| Primary item actually inspected | Exact relevant scope and status | Relation to (H) |
|---|---|---|
| [Heap1303.6119v1](https://arxiv.org/pdf/1303.6119v1), printed5–6, Conjecture4; printed36–39 §7 | Distinct primitive Selberg constituents \(L_j\), positive integer multiplicities \(e_j\), one common real outer \(k\); functional-equation and convolution hypotheses at (18)–(20). Conjectural. | At \(k=1\), primitive integer product/repetition core. Effective weights \(e_jk\), exponent \(\sum(e_jk)^2\), joint coefficient Euler factor and separate constituent Barnes factors. |
| [Sahay2103.13542v1](https://arxiv.org/pdf/2103.13542v1), printed4–10 and24–25 | Nonnegative integer tuple indexed by characters at fixed common \(q\); Thm1.7 depends on Conj1.4 and1.6. | Exact common-modulus Dirichlet constant already printed in March2021, including imprimitive deletions. |
| [Sahayv2](https://arxiv.org/pdf/2103.13542v2), printed4–8 and18–19 | Same weight/modulus quantifiers and conditional Thm1.7, September2021. | No enlargement to independently arbitrary real weights. |
| [Sahayv3](https://arxiv.org/pdf/2103.13542v3), printed4–8,12–18,33–34 | Same tuple; prime mean proved in Thm1.5; splitting and zero mean conjectured. §4 uses a CUE and an explicit distinct-character independence assumption. | Complete integer hybrid comparison and conditional/absolute Euler distinction. |
| [Keating–Snaith published PDF](https://people.maths.bris.ac.uk/~mancs/papers/RMTzeta.pdf), printed59 eq6, printed60 eq15 | Exact CUE characteristic-polynomial moments with \(\Re s>-1\); Barnes asymptotic. | Real \(M_\psi\ge0\) is valid for each matrix factor. No proof of actual L-function zero independence or splitting. |
| [Topacogullari1909.11517v1](https://arxiv.org/pdf/1909.11517v1), printed2–3, Thm1.1/1.3 | Actual fourth moment of one primitive Dirichlet L-function; actual squared product of two different primitives, with possibly different moduli. | Known \(E=4\) repeated and \(E=2\) distinct benchmarks, cross-L and finite-prime normalizations. |
| [Milinovich–Turnage-Butterbaugh author copy](https://home.olemiss.edu/~mbmilino/automorphic.pdf), printed1–2, (1.2)/Thm1.1 | Independently positive real weights on distinct primitives; conjectural exponent with unspecified constant; GRH upper bounds with \(\varepsilon\). | Independent-real exponent and statistical motivation already stated in2014. Does not print the full arithmetic/Barnes coefficient there. |

Heap v1 §6, printed28–35, is the modified moment recipe for the quadratic Dedekind product. Its (162)–(168) already uses a joint local phase and cross-L extraction. §7 starts on printed36, not §6. The unequal integer example \(\zeta^2L(\chi)\) at (185), printed37, already has exponent5 and two separate Barnes factors. The negative outer range printed in Conjecture4 is not independently certified here for repeated effective weights; the candidate wisely makes no negative-power assertion.

Sahay's constant, in each inspected version, has the form

\[
 c_{\ell}(q)=\left\{\prod_p(1-p^{-1})^{\lambda}
       \sum_{r\ge0}\frac{|d_{\ell}(p^r)|^2}{p^r}\right\}
       \left\{\prod_\chi\frac{G(1+\ell_\chi)^2}{G(1+2\ell_\chi)}\right\},
 \quad\lambda=\sum_\chi\ell_\chi^2.
\tag{S}
\]

Its conductor logarithms are \(\prod_\chi\log(q^*(\chi)T)^{\ell_\chi^2}\). All three versions explicitly identify the result as conjectural because of its hypotheses. In v3 the prime theorem assumes eventual \(q^2<X\ll(\log T)^{2-\varepsilon}\); fixed \(q\) makes this compatible with \(X\to\infty\). Earlier versions' cutoff details differ, but their integer/common-modulus quantifiers and leading constant do not. GRH occurs inside the zero heuristic; GRH alone is not the formal condition that proves Thm1.7.

The Keating–Snaith PDF is the published Commun.Math.Phys.214(2000),57–89 version. Heap's publisher metadata confirms online15November2019 /170(1), January2021,191–219; Sahay's confirms online28November2022 /174(3), May2023,631–661. Requests for their published Cambridge PDFs redirected to access/abstract HTML. This audit therefore asserts the formulas/equation numbers of the specified arXiv versions, not that the final journal editions preserve every number or convergence assertion.

## Falsifiable scope substitutions and extension steps

**Integer constituents and one outer real weight.** In Heap, setting \(d_j=1\), outer \(k=1\), and \(e_j\) equal to the number of appearances of a primitive Dirichlet factor gives \(E=\sum e_j^2\). The coefficient of \(p^{-r s}\) in the product is the coefficient of \(z^r\) in \(\prod_j(1-\psi_j(p)z)^{-e_j}\). Thus the same local \(J_p\) occurs, and the Barnes factor is \(G(1+e_j)^2/G(1+2e_j)\). Heap's notation for \(g_L\) includes a compensating \(\Gamma(1+Ek^2)\); it cancels the normalization in the moment formula. Adding a further \(\Gamma(E+1)^{-1}\) to (H) would be wrong.

An arbitrary positive rational weight tuple can be written \(a_j=e_j\kappa\) with a common positive real \(\kappa\) and integers \(e_j\). The tuple \((1,\sqrt2)\) cannot: its ratio is irrational. Hence Heap's common outer real parameter is not the same quantifier as arbitrary independently real weights. Sahay's \(\ell_\chi\in\mathbb Z_{\ge0}\) also does not directly quantify that tuple. Density of rational tuples does not allow exchanging a weight limit with an unknown \(T\to\infty\) asymptotic.

**Exact common-modulus reduction.** If all original characters are modulo \(q\), a primitive inducer determines a unique induced character modulo \(q\). Repetitions can be merged with \(\ell_\chi=\sum a_i\) when this sum is an integer. Then \(d_\ell(p^r)=b_p(r)\), \(\lambda=E\), and (S) equals (H)'s coefficient exactly. Primes dividing \(q\) have all \(\chi(p)=0\), so \(J_p=1\) there; those deletions have not been omitted. This equality is a coefficient comparison, not a claim that conditional Thm1.7 is unconditional.

**Different original moduli.** Let \(Q=\operatorname{lcm}(q_i)\) and let \(\widetilde\chi_i\) be the character modulo \(Q\) induced by \(\psi_i\). On the critical line,

\[
 L(s,\chi_i)=L(s,\widetilde\chi_i)
 \prod_{\substack{p\mid Q\\p\nmid q_i}}(1-\psi_i(p)p^{-s})^{-1}.
\tag{D}
\]

The factors restored in (D) are reciprocal Euler factors. They are not a finite Dirichlet polynomial. For each prime they share the same \(p^{-it}\) phase with every other factor at that prime. Thus replacing their contribution by the product of separate phase averages would lose correlation. The candidate's joint \(J_p\) handles it directly. Relative to the primitive core,

\[
 \frac{\mathcal A}{\mathcal A^*}=\prod_{p\mid Q}\frac{J_p}{J_p^*}.
\tag{F}
\]

This is an exact finite identity between the defined constants. It keeps \(E\) and \(\mathcal G\) unchanged. The factors in (D) are bounded above and away from zero for fixed moduli on \(\Re s=1/2\); that transfers order bounds, but cannot by itself transfer the exact leading coefficient of an actual moment. Equation(F) remains a prediction about the latter unless weighted joint moment control is supplied. As a model extension it is local bookkeeping using the same phase measure. Sahayv3 printed33–34 explicitly remarks that the analogous two-factor constant can be checked for different moduli using Topacogullari; differing moduli are not a wholly new literature idea.

**Shared primitive and conjugate boundary cases.** For \(\zeta(s)L(s,\chi_0\bmod2)=\zeta(s)^2(1-2^{-s})\), the primitive class has total weight2, hence \(E=4\) and one Barnes factor \(1/12\). Put \(x=1/p\). At \(p=2\), \(J_p^*=(1+x)/(1-x)^3\) but \(J_p=1/(1-x)\), giving ratio \((1-x)^2/(1+x)=1/6\). The resulting leading coefficient is \(1/(12\pi^2)\), rather than the primitive-core \(1/(2\pi^2)\). Treating the two rows as independent zero models would incorrectly give exponent2.

For a nonreal primitive \(\psi\), its conjugate \(\overline\psi\) is different. Weights \(a,b\) therefore give \(E=a^2+b^2\), not \((a+b)^2\). The cross quotient is \(\psi^2\), which is nonprincipal because \(\psi\ne\overline\psi\). The functional equation relates opposite heights and does not identify the two same-height factors. This case is inside Topacogullari's distinct-character benchmark, whose printed3 remark explicitly addresses the opposite-height correlation issue. These checks make primitive equality, rather than modulus labels or conjugacy, the falsifiable grouping rule.

**Real weights at the model level.** For a fixed tuple, coefficient domination by \((A)_r/r!\), \(A=\sum a_i\), gives convergent local series on \(|z|=p^{-1/2}\), and Parseval gives the phase representation. No critical-line branch is needed for the original absolute-value integrand. The exact CUE identity at \(s=2m\) is

\[
 \mathbb E_{U(N)}|\det(I-U)|^{2m}
 =\prod_{j=1}^N\frac{\Gamma(j)\Gamma(j+2m)}{\Gamma(j+m)^2}
 \sim \frac{G(1+m)^2}{G(1+2m)}N^{m^2},\qquad m\ge0.
\tag{C}
\]

Inserting each grouped \(M_\psi\) into (C) is legitimate mathematics of the model. Assigning the actual primitive-zero factors that law, taking the matrices independent, and splitting actual prime and zero means remain hypotheses. The zero-weight/empty tuple is exact: the integrand is1, \(I=T\), \(\mathcal A=\mathcal G=1\). It follows by deleting zero rows, with no ambiguous \(0^0\) convention. These extensions need to be written explicitly; they do not introduce a new statistical mechanism.

## Ordered arithmetic convergence and the predecessor's unsupported assertion

This audit independently checked convergence rather than inheriting a cited assertion. At a good prime,

\[
 J_p=1+\frac{|\sum_\psi M_\psi\psi(p)|^2}{p}+O_{\mathbf a}(p^{-2}),
\]
\[
 |\sum_\psi M_\psi\psi(p)|^2
 =E+2\sum_{\psi<\phi}M_\psi M_\phi\Re(\psi\overline\phi)(p).
\tag{L}
\]

For distinct primitive characters, the quotient induced to a common modulus is nonprincipal. With \(S=\{p:p\mid Q\}\), set

\[
 H_p=(1-p^{-1})^EJ_p
       \prod_{\psi<\phi}|1-(\psi\overline\phi)(p)/p|^{2M_\psi M_\phi},
 \qquad p\notin S.
\]

Equation(L) cancels every first-order term, so \(H_p=1+O_{\mathbf a}(p^{-2})\). Positivity and coefficient domination then give a positive absolutely convergent residual. Fixed-modulus prime number theorems give ordered convergence of the nonprincipal prime sums and of the Euler representation of the nonzero \(L^S(1,\rho)\). Consequently

\[
 \mathcal A=\prod_{p\in S}(1-p^{-1})^EJ_p\;
   \prod_{p\notin S}H_p\;
   \prod_{\psi<\phi}|L^S(1,\psi\overline\phi)|^{2M_\psi M_\phi}.
\tag{R}
\]

This verifies the candidate's arithmetic constant independently of actual moment hypotheses. The unregularized product generally is not absolutely convergent. Enlarging \(S\) consistently moves local factors between the products and partial L-values, leaving (R) unchanged.

Heapv1 printed39 (194) instead claims that after extracting diagonal convolution factors the remaining Euler product \(U_k(s)\) is absolutely convergent for \(\Re s>1/2\). That claim fails even in a Dirichlet example. Take \(L=\zeta L(\cdot,\chi)\), \(\chi\) primitive quadratic, \(e_1=e_2=k=1\), and \(x=p^{-s}\) at good primes. The diagonal coefficient-square series has local linear coefficient \(2+2\chi(p)\). Each individual convolution has local factor \((1-x)^{-1}\). Stripping both leaves

\[
 U_{1,p}(s)=1+2\chi(p)p^{-s}+O(p^{-2\Re s}).
\]

Since \(|\chi(p)|=1\) at every good prime, the absolute sum of deviations already diverges at \(s=1\), and thus cannot converge absolutely throughout the claimed half-plane. Bounded cross-prime partial sums in (191) do not imply absolute convergence, and an \(O(1)\) statement alone does not even establish a limiting ordered constant. Noninteger powers also require branch/singularity care before treating a fractional exponent as a literal pole order. These are limits of that displayed justification, not a refutation of its conjectural leading formula or an assertion about an uninspected journal edition.

The candidate's Dirichlet-specific argument (R) avoids this defect. It is an explicit, checkable regularization. It is also not an uncovered correlation mechanism: Heapv1 §6 (162)–(168) already extracts cross-L factors in the quadratic family, and Sahayv3 Thm1.5/Lemma3.1 and printed15–16 separate an absolutely convergent residual from a conditionally convergent first-order product using residue-class Mertens. The latter lemma allows a fixed real exponent in its residue-class product. Extending the first-order algebra to real \(M_\psi\) is therefore supported by standard Dirichlet prime results. The proof in the candidate is useful precision and repair of a loose older justification; this audit does not establish its historical novelty as a theorem.

## The finite-cutoff distinction in the current clarification

The frozen `author/HEURISTIC.md` §5 says that the prime component of the primitive hybrid decomposition has local phase mean \(J_p\). Literally this is false for the sharp cutoff of Sahay's Thm1.3. Reading the primary formula confirms the prime exponential is cut off by \(p^r\le X\); smoothing enters the zero kernel, not an exact replacement by a full Euler factor.

For the primitive part its actual local analytic function is

\[
 C^*_{p,X}(z)=\exp\left(\sum_{r:\,p^r\le X}
                 \frac{\sum_i a_i\psi_i(p)^r}{r}z^r\right).
\]

At a deleted prime multiply by \(\prod_{i:p\mid q_i}(1-\psi_i(p)z)^{a_i}\). Denote the resulting function by \(C_{p,X}\), and its common-phase mean by \(J_{p,X}\). For each fixed prime, \(C_{p,X}\to B_p\) uniformly on the phase circle and \(J_{p,X}\to J_p\). For \(p\le X\), first-degree coefficients agree. A common coefficient majorant bounds the second-and-higher-degree tails by \(O_{\mathbf a}(p^{-2})\); dominated convergence of log ratios gives

\[
 \prod_{p\le X}J_{p,X}/\prod_{p\le X}J_p\longrightarrow1.
\]

Thus (H)'s arithmetic constant is recovered for the ideal joint phase model. This is the precise bridge proved in the root `HYBRID_LOCAL_CLARIFICATION.md`, whose statements were compared here with the sharp primary definition. It repairs the model explanation without proving simultaneous \(T,X(T)\) mean estimates or prime/zero splitting.

A direct falsification of the frozen literal sentence is \(X=3,p=2\), one zeta row of weight1. Then \(C_{2,3}(z)=e^z\), giving \(J_{2,3}=\sum_{r\ge0}(1/2)^r/(r!)^2<2\), while the full Euler \(J_2=(1-1/2)^{-1}=2\). The same example at \(X=2\) is within Thm1.3's \(X\ge2\) domain; it must not be dismissed as an excluded endpoint. Sahay's integer prime-mean proof already controls replacement of cutoff coefficients with full coefficients asymptotically. The root general real-weight clarification is a correction/verification of the model derivation, distinct from novelty of the requested heuristic.

## Proved low moments and current bounds: their exact use

For two distinct primitive characters, put \(u=\chi_1(p)\), \(v=\chi_2(p)\), \(\eta=u\overline v\), and \(x=1/p\) at a prime dividing neither conductor. An independent coefficient calculation gives

\[
 J_p=\frac{1-x^2}{(1-x)^2(1-\eta x)(1-\overline\eta x)},
 \qquad (1-x)^2J_p=\frac{1-x^2}{(1-\eta x)(1-\overline\eta x)}.
\tag{P}
\]

At a prime dividing exactly one of the primitive conductors, \(J_p=(1-x)^{-1}\); at a prime dividing both, \(J_p=1\). Combining these finite cases with (P) gives the leading arithmetic coefficient in Topacogullari's Thm1.3,

\[
 \frac6{\pi^2}|L(1,\overline\chi_1\chi_2)|^2
 \frac{\varphi(q_1)\varphi(q_2)}{\varphi(q_1q_2)}
 \prod_{p\mid q_1q_2}\left(1-\frac1{p+1}\right),
\]

with \(E=2\) and both Barnes factors1. The product character at1 is understood with its modulus-level deletions, consistently with the finite cases above. For one primitive fourth moment, \(J_p=(1+x)/(1-x)^3\) at good primes, so \((1-x)^4J_p=1-x^2\). At conductor primes \(J_p=1\). With \(\mathcal G=1/12\), this gives

\[
 \frac1{2\pi^2}\prod_{p\mid q}\frac{(1-p^{-1})^3}{1+p^{-1}},
\]

equivalent to Thm1.1's printed expression. These are actual low-moment benchmarks, not extrapolation proofs. The formal Thm1.1 is for primitive characters; the paper notes possible imprimitive extensions, but this audit does not certify a separately stated all-imprimitive theorem. Changing \([1,T]\) to \([T,2T]\) by subtraction preserves these leading coefficients for fixed moduli.

[Hagen2409.19780v1](https://arxiv.org/pdf/2409.19780v1), printed1–2, proves the expected order under GRH and GRC for independently positive real weights of distinct irreducible cuspidal automorphic factors. [Hagen2609.11619v1](https://arxiv.org/pdf/2609.11619v1), printed1–2, gives unconditional lower bounds for all fixed positive real weights, and upper bounds when \(\sum d_jk_j\le2\), for its stated GL1 and primitive holomorphic GL2 factors. Neither gives the full arithmetic/Barnes leading constant. Repeated factors can be aggregated and fixed finite deletions bound an imprimitive product above and below, extending order statements without establishing an exact coefficient.

The 2024 introduction's informal independence of whole L-function moments must not be read as an exact factorization of arithmetic constants: (P) retains cross-L factors. The 2026 introduction's description of the sparse asymptotic literature is not used as an exhaustive survey; Topacogullari's direct earlier theorem is part of this audit. Baluyot–Gonek2025 and Gun–Kumar–Thakur2026 were additionally discovered, but no exact full-formula coverage conclusion rests on their unassessed or inaccessible portions. These limits are recorded in `SEARCH_LOG.md`.

## Recommendation, repairs, and exact gaps

The evidence supports **prior coverage of the literal integer-product heuristic core, with the candidate an attributed synthesis and explicit extension in the chosen fixed Dirichlet domain**. It supports **conditional acceptance of the clarified model after the original record is repaired**, not approval of the frozen packet as presently written. It does not support presenting a new high-moment theorem or a novel moment-model discovery. This recommendation is limited to the displayed degree-one Dirichlet example and fixed nonnegative weights; it is not a disposition of every higher-degree reading of the original broad request.

The independent-real and arbitrary-original-modulus quantifiers are a real literal scope difference. A reviewer must not erase it by relabeling Heap's outer \(k\) as an arbitrary vector, by relabeling Sahay's integer tuple as real, or by asserting that bounded finite Euler factors transport a proved coefficient. Conversely, this scope difference does not demonstrate novelty: the enlargement combines already present analytic local powers, exact real CUE moments, primitive aggregation, and finite shared-phase corrections. No substantive new mechanism is identified by this audit. The frozen author already credits the principal formula and expressly disclaims a novel discovery; the recommendation agrees with that narrow characterization on independently checked primary evidence.

Required repairs within this family's assessment are:

1. **H1, substantive derivation repair.** Replace the frozen §5 finite-\(X\) local-mean identification with the actual sharp-cutoff \(C_{p,X},J_{p,X}\), fixed-prime limit, dominated-convergence phase-model bridge, and distinct growing-cutoff/actual-moment hypotheses. Preserve the counterexample and do not count root clarification as an edit to the frozen source.
2. **KS1, citation repair.** Frozen `SOURCE_GATE.md` line38 cites (10)–(12) for the real-power Barnes asymptotic. In the independently inspected published PDF those are cumulant formulas. Cite printed59 eq6 and printed60 eq15. The correct finite-CUE formula already in `HEURISTIC.md` is not invalidated by the citation error.

The H1 finding blocks approval of the original model explanation as written. KS1 is a mandatory bibliographic correction, not a second central mathematical obstruction. Further priority documentation should give Sahay's earliest v1 date, specify common-modulus integer coverage, include the prior2014 independent-real exponent, and distinguish the old Heap convergence defect from the candidate's correct ordered Dirichlet regularization. Those additions improve falsifiability; attribution of Heap/Sahay is already present, so they are not counted as additional discovery-blocking findings.

The permitted root claim ledger also reports assert-elision false-PASS behavior and reproduction/documentation concerns. A direct read here confirms that both frozen numerical suites use `assert` and emit a PASS field, but this family did not rerun optimized interpreters, inject false formulas, or audit the full environment. Those are separate reproduction findings, not independent priority-family counts or repairs performed here. Fresh root verification code/doc work would be evidence/maintenance, not novelty of the heuristic. No source or verifier was changed by this family.

There is no remaining central obstruction identified to a **coherent clarified heuristic model** in the declared domain. Three unproved ingredients remain if the goal is strengthened to an actual generic asymptotic: (i) replacing primitive zero factors by their CUE statistics and establishing distinct-primitive independence at the needed moment strength; (ii) controlling the actual prime mean at a simultaneous growing cutoff; and (iii) proving weighted prime/zero splitting. GRH alone, fixed-prime equidistribution, or finite CUE identities do not supply them. These are explicitly outside theorem claims of the accepted heuristic, not suppressed by a zero count for central heuristic gaps.

The exact **priority-search gap** is different: this audit has not certified a single predecessor printing the full leading constant with all four joint features—arbitrary independent nonnegative real weights, arbitrary original fixed moduli, repeated primitive inducers, and every correlated deleted Euler factor. The audited formulas and standard extension deductions make novelty unsupported, but the finite search cannot exclude an earlier exact formulation or establish a first date for the combined spelling-out. A contradictory primary formula, an overlooked new model mechanism, or a failed local identity above would falsify or require revision of this recommendation.

## Sealing and artifact limits

`RESULT.json` encodes the recommendation, integer counts and their scopes, blocking issue, two required repairs, actual-moment unproved inputs, and precise priority-search gap. `PUBLIC_FILES.json` is a positive allowlist of this family's authored review files, with reviewer-relative paths, sizes and SHA256. It excludes itself, private sources, foreign full text, environments, and caches. It does not describe all available files as public. The initial claim map, bindings, provisional verdict and UTC/% log remain part of the checkable record. Root will independently rereview these results and decide any later action.
