# Grushin converse question: source-resolution scope adjudication

14 October 2026. Source-scope adjudication of accepted mathematical results. This document neither attempts a new proof nor independently re-audits the mathematical arguments. It distinguishes what the primary source asks from the precisely formulated branches that have received proof acceptance.

## Decision

**The results supply a substantive, accepted branchwise answer to the source question, but do not justify marking the original informal question unconditionally solved.** The two source-fixed Hardy converse formulas are settled under the declared regular and literal-weight conventions. Both proposed noncircular Hardy–Rellich readings now have useful, precise positive or negative dispositions. This is more than deferred formulation work.

At the level of the original queue item, the conservative mathematical disposition is **partial / formulation-qualified, with accepted branch resolutions**. The recommended operational status is **deferred**, specifically for formulation selection. This does not defer or revoke the accepted mathematical findings. If the available status vocabulary has only solved versus unsolved, retain unsolved and put the accepted results in the findings.

The phrase “qualified resolution” is defensible only when its object is explicit, for example **“resolution of the stated Hardy and proposed Hardy–Rellich formulations.”** It is unsafe as a bare substitute for “the Oberwolfach question is solved.” The source has not selected the proposed Hardy–Rellich antecedent or all of the solution and weight conventions. None of the acceptance reports can authenticate that selection on the authors' behalf.

## 1. What the primary source fixes

Roychowdhury's paragraph is on printed p.606 / PDF p.28 of Oberwolfach Report 14/2025. It asks for converses in connection with GJR Corollary 3.1 and Theorem 1.3, and cites the Euclidean equivalences of Ghoussoub–Moradifam. It does not present a separately quantified conjecture or select a replacement for the solution-dependent Hardy–Rellich remainder. Its reference is on p.607 and uses GJR's 2024 title. [Oberwolfach report](https://ems.press/content/serial-article-files/51358?nt=1), [publisher record](https://doi.org/10.4171/OWR/2025/14).

The primary versions must remain distinct:

- **Historical v1:** the setup and the cited statements include $n=1$, hence $Q=3$. Theorem 1.3 is on p.6; Definitions 2.1–2.2 on p.13; Corollary 3.1 on p.14. [GJR v1](https://arxiv.org/pdf/2404.05510v1).
- **v2 and current inspected v3:** the corresponding dimension range starts at $n=2$, hence $Q=4$. In v3, Theorem 1.3 is on p.7; the definitions on p.14; the Hardy corollary on p.16. The v3 discussion on p.8 explicitly limits its stated results to its chosen geometry and $n\ge2$. That does not establish why the historical scope changed or select an intended scope for the OWR question. [GJR v2](https://arxiv.org/pdf/2404.05510v2), [GJR v3](https://arxiv.org/pdf/2404.05510v3).

The reviewed geometry is $x\in\mathbb R^n,t\in\mathbb R$, $Q=n+2$,

\[
\rho=(|x|^4+4t^2)^{1/4},\quad
\psi=|x|^2/\rho^2,\quad
\nabla_G=(\nabla_x,|x|\partial_t),\quad
L_G=\Delta_x+|x|^2\partial_t^2.
\]

Fix $0<R\le\infty$ and use real tests $\mathcal T_R=C_c^\infty(B_R\setminus\{0\})$, $B_R=\{\rho<R\}$, with Lebesgue measure. The radial derivative is the source gauge-polar derivative, not differentiation with respect to $|x|$. The radial-gradient Hardy display still quantifies over **all** these tests.

The exact target is

\[
B_Q(V,W;R):\qquad
(r^{Q-1}Vf')'+r^{Q-1}Wf=0
\quad\text{for a strictly positive }f\text{ on all of }(0,R).
\]

The coefficient multiplying $W$ is one. This is GJR's **Q-dimensional** Bessel property, not its separate ordinary Bessel equation with the dimensional factors omitted. Positivity only on a smaller interval, a positive solution for an unspecified multiple of $W$, or a supersolution without the accepted passage to an exact solution would not answer this target. The source definition imposes no endpoint value, boundedness or integrability of $f$. [GJR v1, p.13](https://arxiv.org/pdf/2404.05510v1), [GJR v3, p.14](https://arxiv.org/pdf/2404.05510v3).

For the accepted results, flux-classical means $f\in C^1(0,R)$, with $r^{Q-1}Vf'\in C^1(0,R)$, and the equation holds pointwise. With $V>0$ and the stated interior coefficient regularity, this gives an ordinary classical solution. For vanishing $V$, this is an explicit convention adopted in the results, not a separately stated source definition.

## 2. Exact antecedents and their source status

The two source-fixed Hardy antecedents are

\[
H_G:\quad \int V(\rho)|\nabla_Gu|^2\ge\int W(\rho)\psi u^2,
\qquad
H_\rho:\quad \int V(\rho)\psi|u_\rho|^2\ge\int W(\rho)\psi u^2,
\]

each required for every $u\in\mathcal T_R$. Their converse questions do not require introducing a new formula. [GJR v1, p.14](https://arxiv.org/pdf/2404.05510v1), [GJR v3, p.16](https://arxiv.org/pdf/2404.05510v3).

For Hardy–Rellich, use the following notation for the terms in the cited display:

\[
\begin{aligned}
A_V[u]&=\int V(\rho)(L_Gu)^2/\psi,\\
D_{V,W}[u]&=\int\left[W(\rho)+(Q-1)\bigl(V(\rho)/\rho^2-V'(\rho)/\rho\bigr)\right]|\nabla_Gu|^2,\\
E_{V,g}[u]&=\int V(\rho)g(\rho)^2\left|\nabla_G(u_\rho/g(\rho))\right|^2,\\
S_Q[V]&=(Q-5)V/r^2+3V'/r-V''.
\end{aligned}
\]

The source assumes $B_Q$, takes $f$ to be its positive solution, assumes $V\ge0$ and $S_Q[V]\ge0$, and obtains $A_V\ge D_{V,W}+E_{V,f}$. Retaining the hypothesis that $f$ solves the desired equation makes a “converse” circular. It is neither an unproved necessity theorem nor a counterexample target. [GJR v1, p.6](https://arxiv.org/pdf/2404.05510v1), [GJR v3, p.7](https://arxiv.org/pdf/2404.05510v3).

Two **proposed**, noncircular readings have instead been accepted for investigation:

1. **Core:** $A_V[u]\ge D_{V,W}[u]$ for all source tests. This drops the nonnegative remainder but preserves the entire derivative correction.
2. **Independent function:** one fixed positive $C^2$ function $g$, with no ODE assumption, satisfies $A_V[u]\ge D_{V,W}[u]+E_{V,g}[u]$ for all source tests.

Neither is a verbatim additional OWR formula. The source gives no basis for identifying these different premises or for changing “one fixed $g$” to “a separate $g_u$ for each test.”

## 3. Accepted branch classification

The statements below rely on the exact proof and independent-acceptance artifacts pinned in the companion `REVIEWED_ARTIFACT_PINS.json`. They do not rely on a proof author's assessment of what the original source intended.

### A. Both Hardy displays, regular leading weight: affirmative

For every $Q=n+2\ge3$, fixed $0<R\le\infty$, $V\in C^1(0,R)$ with $V>0$, and real $W\in C^1(0,R)$, **each** source Hardy antecedent is equivalent to $B_Q$. The common one-dimensional form and the all-test statements are also equivalent. No endpoint conditions are added. This settles both Hardy converses throughout both historical and current dimension ranges in the regular-leading-weight class.

The claim is stronger than a radial-test-only result and does not require $W\ge0$. The $V>0$ restriction must remain visible because the printed forward class allows $V\ge0$.

### B. Both Hardy displays, literal nonnegative leading weight: negative

With the adopted flux-classical convention, either Hardy necessity claim is false for the full literal $V\ge0$ class, even if $W>0$. The accepted example, for any interior $a$, is

\[
V(r)=r^{1-Q}(r-a)^2,\qquad W(r)=\tfrac14r^{1-Q}.
\]

It satisfies both inequalities for every original test but has no strictly positive flux-classical solution across $r=a$. It works for every $Q\ge3$. Thus neither the $W>0$ convention nor the newer dimension range alone repairs this literal Hardy converse. It fails the Hardy–Rellich side condition and is not a side-conditioned Hardy–Rellich example.

This is a genuine negative universal result under a stated solution convention. It is not a classification of every degenerate pair or every possible weak solution notion, and it does not negate A.

### C. Proposed core, regular real potential, current range: negative

For the universal claim over $Q\ge4$, $V>0$, real $W$, and $S_Q[V]\ge0$, the accepted $Q=5$ example disproves necessity:

\[
R=e^{12},\quad V=1,\quad W=\lambda/r^2-r^{-4},\quad S_5[V]=0.
\]

Here $\lambda$ is exactly specified variationally in the proof. The core holds for **all** original source tests, while the exact full-interval $B_5$ property fails. Every source test has finite left energy in this example. The potential is negative near zero, so it cannot answer the $W\ge0$ branch.

One allowed dimension is sufficient to refute the universal current-range assertion. This does **not** separately settle the real-potential assertion in every fixed dimension, and no such classification is required for this particular negative universal conclusion.

### D. Proposed core, nonnegative potential, current range: affirmative

For every $Q\ge4$, $V\in C^2$ with $V>0$, $W\in C^1$ with $W\ge0$, and $S_Q[V]\ge0$, the core implies $B_Q$, on the full fixed interval and without extra endpoint assumptions.

The accepted regular theorem actually requires $W\ge0$ and $S_Q[V]\ge0$ only on some neighborhood of zero; it permits real $W$ elsewhere. The leading weight must still be strictly positive throughout $(0,R)$ for this local version. This is an explicitly proved strengthening, not a source hypothesis recovered from OWR.

The accepted addendum also gives a global side-condition dichotomy: $V\in C^2$, $V\ge0$, $S_Q[V]\ge0$ throughout $(0,R)$ implies either $V>0$ throughout or $V\equiv0$. Together with the accepted zero-weight classification, this extends the **global-side-condition**, nonnegative-potential, $Q\ge4$ result to $V\ge0$. It does not license allowing arbitrary interior zeros when the side condition is imposed only near zero.

### E. Proposed core, positive potential, historical $Q=3$: negative

The accepted historical example is

\[
R=1,\quad V=r^{3/4},\quad W=\lambda r^{3/4},\quad
S_3[V]=\tfrac7{16}r^{-5/4}>0,
\]

with an exact positive variational constant $\lambda$. The original all-test core holds and $B_3$ fails. Both weights are strictly positive. Its accepted proof and independent spectral audit establish the $n=1$ two-sheet angular analysis directly and include all finite-energy source tests, as well as the automatic infinite-energy cases.

This disposes of the historical core branch even under $W>0$, and prevents extending D to $Q=3$. It neither contradicts D nor supplies an authenticated explanation for the source's later dimension change.

### F. Proposed fixed-independent-function remainder, regular leading weight: affirmative

For every $Q\ge3$, $V\in C^1$ with $V>0$, real $W\in C^1$, and one fixed independent positive $g\in C^2$, the all-test remainder premise implies $B_Q$. No $V''$ side condition, sign restriction on $W$, or endpoint condition is needed for this **necessity** assertion.

The given $g$ is forced to be a positive supersolution. The accepted proof separately obtains an exact positive solution, which may be different from $g$. It does not prove that every positive supersolution supplies the full all-test inequality, or that the specified $g$ satisfies the equality ODE. Those stronger assertions must not be reported as accepted.

### G. Zero leading weight and the literal side-conditioned classes

Under the announced integral convention, when $V\equiv0$, either Hardy premise, the core premise, or the fixed-independent-function premise holds exactly when $W\le0$. The exact Bessel property holds exactly when $W\equiv0$. Thus $V=0,W=-1$ defeats each unrestricted real-$W$ literal necessity assertion, including the proposed independent-function reading. $V=W=0$ is not a counterexample.

For the global classical side-conditioned class, the dichotomy in D shows that the nonzero leading-weight cases are precisely the regular cases already covered above. The zero case is exactly classified. There is therefore no remaining unexamined interior-zero case in that particular classical side-conditioned class. For Hardy, which has no such side condition, B gives the genuine nonzero degenerate obstruction.

## 4. Tests and endpoints: accepted gates, not remaining proof gaps

- The only puncture in the test class is the origin. The axis $x=0,t\ne0$ has not been removed.
- For Hardy–Rellich, the accepted convention is the nonnegative extended integral of the off-axis quotient. Its value on the null axis is immaterial. Infinite left energy with finite right side satisfies the inequality. This is a declared formalization of the source display, not an added restriction to axis-avoiding tests.
- Radial tests used for necessity have finite left energy and belong to the original class even on the axis. The $Q=5$ counterexample has finite energy for every test; the $Q=3$ counterexample explicitly handles the finite/infinite split.
- The zero ordinary integral constraint on derivatives of compact radial tests was accounted for. The nonnegative-potential theorem uses a one-sided correction argument, not an unsupported general density theorem. The counterexamples exploit the genuine constrained gap and still establish the full spatial inequality.
- Positive solutions and their obstructions concern the complete fixed $(0,R)$, coefficient one, with no endpoint condition. No boundary assumptions from the Euclidean analogy have been silently imported.

Accordingly, describing these already accepted gates as unresolved would understate the results. A differently selected energy domain, endpoint condition, or degenerate weak-solution convention would be a different formulation requiring its own coverage.

## 5. What remains unspecified, and what is merely outside the proved claims

**Unspecified by the original source:** which noncircular Hardy–Rellich antecedent is intended; whether a regular leading coefficient is intended despite printed $V\ge0$; whether any independent $W$-sign restriction is intended; the degenerate solution convention; a classical interpretation of the $V''$ condition; and any more restrictive energy interpretation. The source version is also unspecified, although the accepted results now explicitly cover both relevant dimension ranges. More proof work cannot itself identify these authorial choices.

**Not established by the accepted packet:** a dimension-by-dimension classification for arbitrary real $W$; a complete characterization of degenerate weights without the global classical side condition; converses under altered endpoint or test conventions; an independent-function premise with test-dependent or other unselected quantifiers; or full all-test sufficiency for a prescribed arbitrary supersolution without the source side condition. These are not all required to refute an already false universal branch. Listing them must not inflate the original question into every imaginable variant.

**No gap remains in the frozen principal assertions A–G.** Their universal positive statements or admissible negative examples have accepted dispositions at exactly the stated scopes. A source-level partial label reflects the unresolved identification of the informal question with one of those formulations, not missing all-test proofs or a failure to handle historical $Q=3$.

The Euclidean reference does not select extra endpoint assumptions or a different Bessel scaling for this question merely by analogy. The retained historical manuscript and journal record are distinct sources; this adjudication makes no fresh literature-exhaustiveness, current-openness, novelty, or human peer-review claim. [Ghoussoub–Moradifam historical manuscript](https://arxiv.org/pdf/0709.1954v1), [journal record](https://doi.org/10.1007/s00208-010-0510-x).

## 6. Recommended disposition wording

**Recommended exact operational status: deferred.** Reason: a noncircular source-level formulation still needs to be selected. Mathematical characterization: partial / formulation-qualified, with accepted branchwise results. Do not change the original item to unqualified solved solely on this evidence.

**Suggested findings text:**

“Both source Hardy displays are equivalent to the coefficient-one full-interval Q-dimensional Bessel property for V>0 and real W, all Q>=3; literal V>=0 converses fail even with W>0 under the stated flux-classical convention. For the explicitly proposed remainder-free Hardy–Rellich core with the source side condition, necessity fails for real W at Q=5, holds for W>=0 at Q>=4, and fails even for V,W>0 at historical Q=3. One fixed independent positive C2 remainder function gives necessity for V>0 and real W, all Q>=3. All-test and endpoint gates are covered. Original Hardy–Rellich formulation remains unspecified; no unqualified full-source resolution claim.”

Every stated principal assertion has an accepted disposition. Further work on unselected dimensions, weak-solution conventions, endpoint conditions or remainder quantifiers would require a new explicit scope, rather than being a missing step in this accepted work.

A documented decision to adopt one exact formulation would permit marking **that formalized subproblem** solved or refuted according to A–G. Such a decision must be described as a choice of working scope, not as a newly discovered statement of source intent. Packaging or explaining the accepted branch classification does not supply the missing evidence of source intent.

## Evidence boundary

The OWR question and the historical/current GJR statements were checked against retained primary text; the OWR question page and both versioned Hardy–Rellich theorem pages were also visually inspected. Twenty-six selected source/proof/acceptance artifact pins were verified against their existing receipts. Exact filenames, hashes, sizes and inspection scope are in the companion pin manifest. That verifies identity and supports this source-scope adjudication; it is not another mathematical acceptance audit.

Only authored analysis and public-source verification metadata are included here. Copied source documents, dataset contents, private sources, personal data and private coordination material are excluded.
