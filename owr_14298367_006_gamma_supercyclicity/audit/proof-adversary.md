# Independent adversarial proof audit

Audit date: 2026-09-23 UTC. Reviewer: an independent Codex subagent, assigned to falsify the submitted proof. Mathematical-audit completion estimate: **100% for the submitted implication chain**. This document does not perform a priority audit, certify novelty, or replace external peer review.

## Verdict and exact scope

**The submitted argument is mathematically valid in the separable setting of the cited Oberwolfach problem.** I found no substantive gap in the two-sided tail argument, the arbitrary-scalar-set quantifiers, or the vector-valued construction. The proof must explicitly retain separability of the ambient complex Banach spaces; bounded distortion alone does not imply it. This is an existing standing hypothesis in the report, not a new restriction on the scalar set.

More precisely, let (1\le p<\infty), let (c_j\in(0,\infty)), and suppose (S(a)_j=a_{j+1}) is bounded on (\ell^p(\mathbb Z,c)). If (E\ne\{0\}) is a separable complex Banach space, then for every set (\Gamma\subseteq\mathbb C), scalar (S) is (\Gamma)-supercyclic if and only if its coordinatewise version (S_E) on (\ell^p(\mathbb Z,c;E)) is (\Gamma)-supercyclic. Bounded invertibility, assumed in the candidate, is sufficient but stronger than needed: the inverse translations used in the proof need only act on finitely supported vectors.

Under the original dissipative, bounded-distortion, bounded invertible composition-operator hypotheses, with (L^p(X,\mu)) separable, the candidate's two conjugacies then prove the requested equivalence with the associated weighted shift for every (\Gamma). No topological, measurable, phase, multiplicative-closure, or radial-closure assumption on (\Gamma) is needed.

Primary source checked: [Oberwolfach Report 19/2024](https://ems.press/content/serial-article-files/49477), printed pp. 1079–1083. The report specifies bounded invertible composition operators on pp. 1079–1080; the relevant contribution explicitly adopts separable Banach spaces on p. 1081; and the open question appears on p. 1083. This audit used those pages to confirm scope, not to infer validity of the new argument.

## 1. Scalar necessity: every estimate checks

For a nonempty finite (F\subset\mathbb Z), take (v=2\sum_{j\in F}e_j). A dense (\Gamma)-orbit hits every nonempty open set at arbitrarily large times: for a fixed (N), the finite union (\bigcup_{n=0}^{N}\mathbb C S^n x) is closed and has empty interior in the infinite-dimensional scalar sequence space. Every nonempty open set therefore contains a smaller nonempty open set avoiding it. Density gives a hit with time greater than (N). This reasoning never assumes (\Gamma) itself is closed or countable.

Thus one may choose (n_r\to\infty), actual scalars (\lambda_r\in\Gamma\setminus\{0\}), and errors (\varepsilon_r\downarrow0) such that

\[
\|\lambda_rS^{n_r}x-v\|_c<\varepsilon_r<\min_{j\in F}c_j^{1/p}.
\]

It follows coordinatewise that ( |x_{j+n_r}|>|\lambda_r|^{-1}) for (j\in F). Therefore

\[
|\lambda_r|^{-p}\sum_{j\in F}c_{j+n_r}
<\sum_{j\in F}c_{j+n_r}|x_{j+n_r}|^p\longrightarrow0.
\]

The last limit follows directly because (x\in\ell^p(\mathbb Z,c)) and the finite blocks escape to (+\infty). The candidate instead chooses pairwise disjoint blocks and proves summability; that stronger argument is also correct.

For the other direction, fix the first hit (n_1,\lambda_1). For sufficiently large (r), every (q=j+n_1-n_r), (j\in F), lies outside (F). Evaluating the approximation at this finite set of coordinates gives

\[
|\lambda_r|^p\sum_{j\in F}c_{j+n_1-n_r}
<|\lambda_1|^p\varepsilon_r^p.
\]

The translation convention is essential here and was checked: (S^n e_k=e_{k-n}). Hence boundedness of (S^{n_1}) yields

\[
c_{j-n_r}\le\|S^{n_1}\|^p c_{j+n_1-n_r},
\]

and consequently

\[
|\lambda_r|^p\sum_{j\in F}c_{j-n_r}
\le\|S^{n_1}\|^p|\lambda_1|^p\varepsilon_r^p\longrightarrow0.
\]

The factors involving the first hit are fixed as (r\to\infty); they need not be bounded uniformly over (F). This distinction is what makes the anchoring step valid even for extremely sparse or unbounded (\Gamma).

Both tail quantities therefore become arbitrarily small at a common (n_r\to\infty) and a common actual scalar (\lambda_r\in\Gamma\setminus\{0\}), exactly as required. There is no hidden replacement of a scalar by a quotient that might leave (\Gamma).

## 2. Submitted vector construction: no circularity or uncontrolled terms

The repeated countable dense list of finitely supported (E)-valued vectors exists because (E) is separable and (p<\infty). In the induction the finite set (F_m) contains three kinds of supports:

1. (y_m), which controls the norm of the new summand;
2. (S^{-k_i}y_i), (i<m), which controls earlier summands at the new time;
3. (S^{k_i}y_m), (i<m), which ensures the new summand has a controlled effect at all previous times.

These are all determined before selecting (k_m,\lambda_m), so the induction is not circular. The quantity (M_m) is a finite maximum. Applying the two tail bounds to any of these vectors is legitimate because

\[
\|S^{-k}z\|_c^p=\sum_jc_{j+k}\|z_j\|_E^p,
\qquad
\|S^kz\|_c^p=\sum_jc_{j-k}\|z_j\|_E^p.
\]

The denominator in (\theta_m) accounts for both kinds of interference. For earlier terms, the total is bounded by

\[
\theta_m\sum_{i<m}|\lambda_i|^{-1}\le2^{-m}.
\]

For a later term (r>m), the inclusion of (S^{k_m}y_r) at stage (r) gives the bound (|\lambda_m|\theta_r\le2^{-r}); their sum is at most (2^{-m}). The summands have norm at most (2^{-m}), so the constructed series converges absolutely in the Banach space. Boundedness of each fixed (lambda_mS^{k_m}) justifies applying it to that series. The resulting error bound (2^{1-m}) tends to zero, and the dense-tail property of the target list proves density of the (\Gamma)-orbit.

Two harmless notation fixes should appear in a polished version: set (k_0=0), and require (F_m) to be nonempty (add (0) if necessary). These do not change the construction.

## 3. A shorter independent sufficiency proof

This supplies an independent check and can replace the long induction if brevity is preferred.

From the tail condition, select increasing (n_k) and (\lambda_k\in\Gamma\setminus\{0\}) such that both tail quantities for (F_k=[-k,k]\cap\mathbb Z) are less than (1/k). Set

\[
A_k=\lambda_kS_E^{n_k},
\qquad R_kv=\lambda_k^{-1}S_E^{-n_k}v
\quad(v\in c_{00}(\mathbb Z;E)).
\]

For every finitely supported (u,v), the tail estimates imply (A_ku\to0), (R_kv\to0), and (A_kR_kv=v). Let (U,V) be arbitrary nonempty open subsets and choose finitely supported (u\in U), (v\in V). For large (k), the vector (u+R_kv) lies in (U), and its image (A_ku+v) lies in (V). Thus (\bigcup_kA_k^{-1}(V)) is open and dense. Applying the Baire theorem to a countable base of target open sets gives a vector (x) for which ({A_kx:k\ge1}) is dense. This is a subset of its (\Gamma)-orbit.

This proof also shows why one must not casually invoke a transitivity theorem for a (\Gamma)-orbit without checking its hypotheses: here the open-density argument is supplied directly for the countable family (A_k), so no scalar-set algebra is required.

## 4. Conjugacies and measure-theoretic details

All indexing in the candidate is consistent with the convention ((B_wa)_j=w_{j+1}a_{j+1}). If (c_j=\mu(f^jW)/\mu(W)) and (D(a)_j=c_j^{-1/p}a_j), then

\[
(DB_wa)_j=c_j^{-1/p}(c_j/c_{j+1})^{1/p}a_{j+1}
=c_{j+1}^{-1/p}a_{j+1}=(SDa)_j.
\]

For the composition operator, bounded distortion makes the transported measure (\mu_j(A)=\mu(f^jA)) equivalent to (c_j\mu|_W), with uniform comparison factor (K). Extending this measure inequality to nonnegative measurable functions proves the norm comparison for (J\varphi=(\varphi\circ f^j|_W)_j). Radon–Nikodym derivatives are valid here, but unnecessary.

Surjectivity uses the bimeasurability of (f): choose representatives (u_j) and define (\varphi=u_j\circ f^{-j}) on (f^jW). Countably many measurable pieces give a measurable function. Different choices of representatives affect only a null set because each transported measure is equivalent to (\mu|_W). The norm comparison gives membership in (L^p) and a bounded inverse. The identity (JT_f=S_EJ) then holds on equivalence classes.

The standing bounds for composition by (f) and (f^{-1}) ensure (0<\mu(f^jW)<\infty) for every (j), so no zero or infinite coefficients occur. Finally, extension by zero embeds (E=L^p(W)) isometrically into (L^p(X)); hence (E) is separable. It is nonzero because (0<\mu(W)<\infty).

## 5. Adversarial boundary checks

- **Empty scalar set or only zero:** neither operator is (\Gamma)-supercyclic on the nonzero sequence spaces. The tail criterion has no admissible scalar and is false, consistently.
- **Arbitrary phases, sparse sets, and nonmeasurable sets:** only membership of each chosen (\lambda_k) is used. All quantitative conditions use (|\lambda_k|). The proof does not choose an argument, take a measurable selection, or assume any closure property of (\Gamma).
- **(p=1):** all estimates remain valid; no strict convexity, Hilbert-space orthogonality, or reflexivity is used.
- **Finite-dimensional nonzero (E):** valid, since the bilateral sequence space is still infinite-dimensional. **(E=0)** must remain excluded from the amplification statement.
- **(p=\infty):** excluded; density of finitely supported vectors would fail. No extension to that case is established here.
- **Unbounded inverse shift:** a bounded inverse is not required for the abstract amplification theorem because all inverse-shift expressions are finitely supported before taking limits. Keeping bounded invertibility in the published theorem is safe and matches the source setting.
- **Infinite support of the constructed vector:** the estimates control the complete series, not merely a truncation. A numerical script that checks truncations would illustrate the argument but would not verify the theorem universally.

### Separability cannot be omitted

For an explicit boundary counterexample, let (I) be uncountable and let (\Omega=\{0,1\}^I) carry its Bernoulli product probability measure (\nu). Its coordinate functions give an uncountable uniformly separated subset of (L^p(\Omega,\nu)), since the (p)-th power of the distance between distinct coordinates is (1/2). Thus this (L^p) is nonseparable.

Take (X=\mathbb Z\times\Omega), give slice (j) measure (2^{-|j|}\nu), let (f(j,\omega)=(j+1,\omega)), and take (W=\{0\}\times\Omega). This has bounded distortion with (K=1), and both composition directions are bounded. The scalar model has (c_j=2^{-|j|}), so both finite-block tails tend to zero with (\lambda=1); the scalar shift is hypercyclic by the independently proved sufficiency argument. But no operator on the nonseparable (L^p(X)) can be (\Gamma)-supercyclic for any (\Gamma\subseteq\mathbb C): every such orbit lies in the countable union of the complex lines through its ordinary orbit, whose closure is separable.

Accordingly, the statement should say explicitly that (L^p(X)) is separable, as in the source's standing setting. The phrase “no additional hypotheses” is justified for (\Gamma), not as permission to delete the standing hypotheses on the underlying space.

## Remaining gap

No mathematical gap remains in the stated separable theorem after the two minor notation clarifications. The audit does not establish priority. A clean priority claim requires separate examination of the literature on arbitrary-(\Gamma) supercyclicity of weighted shifts and translations, and of subsequent papers resolving the specific 2024 question.
