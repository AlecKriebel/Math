# Independent priority audit: the original all-probability question

Target: PR 466, problem 30000999 / OWR-2042-008. Audited frozen head: `77a27c5da92b8f42f79b2f27e40f5c9a6403ddb9`. Audit date: 2026-10-12 UTC. This is a recommendation, not a status change.

## Recommendation and its precise meaning

Recommend **`already_solved` for the original unrestricted-probability target**, with the reason recorded as **an immediate consequence of classical noninjectivity**, rather than as a newly discovered 2026 resolution. The frozen proof's negative answer to that literal question is correct. Its antipodal counterexample uses a symmetry of the very definition, and the corresponding odd-function obstruction is explicitly present in an independently inspected primary publication from 1913.

I did **not** locate a primary publication explicitly writing Stephens's exact inverse-Wasserstein inequality and its negative answer. Accordingly, this report does not claim that a particular earlier paper published that exact Wasserstein theorem, or that a documented subsequent closure of the 2008 question has been found. The justified classification is that its conclusion follows routinely from earlier documented mathematics. Lack of an exact-wording search hit cannot make that deduction novel or certify that the question remained mathematically open until 2026.

If a catalogue defines `already_solved` narrowly to require an explicitly published answer in the catalogue's own wording, record the reason above separately and do not fabricate that bibliographic fact. Under a mathematical-priority classification, the original question should not be promoted as a novel solved problem. The stronger theorem about **even, smooth, uniformly positive densities** is a distinct claim; this audit neither awards nor rejects its novelty.

## Independence, inputs, and evidence standard

Before any earlier independent audit or peer report was accessed, I wrote `INITIAL_HYPOTHESIS.md` and began the independent search ledger. I read the frozen author `release/PROOF.md`, `release/SOURCE_GATE.md`, and the exact-head receipt as claims to check. No prior independent audit or peer report was read at any stage of this audit.

Primary evidence was retrieved independently from the official EMS report, the original Funk article in the Göttingen digitization, and Quellmalz's published 2020 article. The older scanned pages were rendered and visually inspected. Full foreign PDFs, extractions, images, and retrieval metadata remain private. Public outputs contain original analysis and sanitized bibliographic information only. No Git, queue, PR, paper, cloud, or external-person communication action was performed.

## What the original source actually asks

Stephens's contribution, “Measuring the Geodesic Radon Transform with Mass Transport,” occupies printed pp. 1762–1764 of *Oberwolfach Report 31/2008*. Printed p. 1763 defines normalized equator averaging on continuous functions and its dual action on spherical measures; it uses all probabilities on the sphere and intrinsic geodesic (W_p), (1\le p<\infty). It ends by asking about a uniform inequality in the reverse direction. The contribution imposes no evenness, support, or projective-quotient condition. It discusses moving point masses, confirming that atoms are admissible. [Official report](https://ems.press/content/serial-article-files/46174), [report DOI](https://doi.org/10.4171/OWR/2008/31).

The printed question is prose rather than a displayed reverse formula. Its nontrivial interpretation is a positive lower contraction factor, equivalently a finite inverse constant:

\[
 W_p(\mu,\nu)\le C(p,n)\,W_p(R\mu,R\nu)
 \quad\text{for every }\mu,\nu\in\mathcal P(S^{n-1}).
\]

A zero lower factor would only be the trivial inequality (0\le W_p(R\mu,R\nu)). The frozen proof addresses the meaningful inverse inequality above.

The report's displayed forward contraction formula has the usual (n\ge3) setting. It does not explicitly state a separate dimension restriction in the closing question. The negative argument below holds in every ordinary equator-transform dimension (n\ge3), and also in the (n=2) extension obtained by normalized counting measure on the two-point equator. This distinction avoids using a divergent (n=2) forward-constant formula as evidence about the source.

## Checkable implication: classical parity forces the exact negative answer

This section is an independent derivation. Let (S=S^{n-1}\subset\mathbb R^n), with intrinsic distance (d(x,y)=\arccos(x\cdot y)), and let

\[
 E(u)=\{x\in S:x\cdot u=0\},\qquad
 F\varphi(u)=\int_{E(u)}\varphi(x)\,d\sigma_u(x),
\]

where (sigma_u) is normalized equator measure. The dual is defined by

\[
 \int_S\varphi\,d(R\mu)=\int_S F\varphi\,d\mu
 \quad(\varphi\in C(S)).
\]

The geometric equality (E(u)=E(-u)), including their normalized measures, gives (F\varphi(u)=F\varphi(-u)) for every test function. Therefore

\[
 R\delta_u=R\delta_{-u}=\sigma_u.
\]

The only coupling of the two input point masses is (delta_{(u,-u)}), hence

\[
 W_p(\delta_u,\delta_{-u})
 =\left(d(u,-u)^p\right)^{1/p}=\pi,
 \qquad W_p(R\delta_u,R\delta_{-u})=0.
\]

This contradicts the proposed inequality for every finite (C(p,n)), for every finite (p\ge1). All moments exist because the sphere is compact. The proof is independent of any high-frequency asymptotic, regularity estimate, or transport construction. It also rules out every inverse modulus (W_p(\mu,\nu)\le\omega(W_p(R\mu,R\nu))) with (omega(0)=0) on the unrestricted domain.

Equivalently, let (A(u)=-u). Because (F\varphi) is even,

\[
 R(A_\#\mu)=R\mu,\qquad
 R\mu=R\bigl(\tfrac12(\mu+A_\#\mu)\bigr).
\]

Thus the transform forgets antipodal-odd information before any choice of metric is made. A finite inverse bound between genuine metrics would imply injectivity: equal outputs would force zero input distance and hence equal inputs. We use this necessary implication only; we do **not** assert that injectivity suffices for a Lipschitz inverse.

### A positive smooth probability version of the same obstruction

The point-mass example is already within the original domain. To check that probability normalization or positivity does not hide an assumption, let (sigma) be normalized spherical surface measure, (0<a<1), and

\[
 d\mu_\pm=(1\pm a x_1)\,d\sigma.
\]

These are distinct smooth probabilities with densities bounded below by (1-a>0). For every continuous (\varphi), antipodal invariance of (sigma) and evenness of (F\varphi) give

\[
 \int_S F\varphi(x)x_1\,d\sigma(x)=0,
 \quad\text{so }R\mu_+=R\mu_-.
\]

The coordinate function (x_1) is 1-Lipschitz for intrinsic distance, since its increment is bounded by the Euclidean chord length, which is bounded by the arc length. Every coupling consequently has transport cost at least the difference of coordinate expectations. Rotational symmetry gives (int x_1^2\,d\sigma=1/n), so

\[
 W_1(\mu_+,\mu_-)\ge\frac{2a}{n}>0,
 \qquad W_p(\mu_+,\mu_-)\ge W_1(\mu_+,\mu_-).
\]

The last inequality follows from the (L^p\)-versus-(L^1) inequality for each probability coupling and then taking infima. This construction connects the function-level odd kernel to the dual probability-measure question without assuming self-adjointness. The densities are **not even**; this example therefore does not establish the frozen proof's separate even-density theorem.

## Directly verified earlier primary mathematics

### Funk 1913: the original obstruction

Paul Funk's “Über Flächen mit lauter geschlossenen geodätischen Linien,” *Mathematische Annalen* 74 (1913), 278–300, was independently obtained through the Göttingen digitization linked by EuDML. The publisher confirms June 1913 and notes a relation to the 1911 dissertation; that earlier dissertation was not inspected, so 1913 is the earliest directly verified publication used here. [Publisher metadata and DOI](https://link.springer.com/article/10.1007/BF01456044), [primary digitized article](https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0074/LOG_0027.pdf).

Printed p. 283 defines antipodal even and odd parts. Printed p. 284 assigns each great-circle integral to its two opposite poles and states Theorem I: an odd function has zero circle-integral transform. This was verified from the scan, not inferred from a modern citation. The article's surrounding harmonic-series hypotheses include the smooth polynomial (x_1) used above. Its unnormalized circle integral on (S^2) differs from Stephens's function transform by the constant (2\pi), which does not change its kernel. The theorem is function-level and not a Wasserstein statement.

I do not need to assert that every continuous-function nullspace converse in the 1913 text is hypothesis-free. Its explicit forward odd cancellation and antipodal-pole observation suffice. Nor do I claim that its (S^2) theorem by itself is an already-published theorem in every higher dimension; the elementary equator identity above supplies those dimensions directly.

### Quellmalz 2020: normalized all-dimensional corroboration

Michael Quellmalz, “The Funk–Radon transform for hyperplane sections through a common point,” *Analysis and Mathematical Physics* 10, 38 (2020), was checked in the official full text and author-hosted journal PDF. Its Eq. (2.5) defines the normalized classical equator transform for ambient dimension (d\ge3). Theorem 4.1 at (z=0) specializes to (Ff=0) iff (f) is odd for continuous (f). The proof traces the classical nullspace to Groemer (1996), Proposition 3.4.12; that book proposition was not independently inspected here. [Published article](https://link.springer.com/article/10.1007/s13324-020-00383-2).

This independently verifies a precise pre-2026 normalized statement beyond the original (S^2) source. It is corroboration, not the basis for claiming that an explicit Wasserstein answer was published in 2020. Its Sobolev invertibility statement concerns even functions and distinct norms, so it cannot be substituted for the separate even-density Wasserstein theorem.

## Historical and later-literature checks

The official University of Toronto seminar record identifies a Stephens talk on October 17, 2008. Its linked abstract describes spherical probability measures, Wasserstein distance, forward contraction, and the range criterion, without an evenness repair or an explicit reverse answer. This corroborates the historical formulation, not later closure. [Official seminar abstract](https://www.math.utoronto.ca/appmath/AppMath_08_09/stephens.txt).

The independent ledger records exact-title, author, transform, inverse, stability, and Wasserstein queries, alongside attempts at historical and modern sources. The current problem-catalogue URL was not retrievable; its absence supplies no status evidence. The 2008 source itself asks the question, and this report does not rewrite that historical fact or infer a private intended evenness restriction.

Several later results can look relevant while addressing a different transform or distance:

| Primary candidate | Definition that prevents substitution for the original question |
|---|---|
| Bonet et al., *Spherical Sliced-Wasserstein*, 2022 preprint / 2023 conference | Its transform takes values on (S^1\times V_{d,2}), uses half great-circle sections, and the discrepancy averages slice-wise distances. This is not the sphere-to-sphere normalized equator dual. [Primary preprint](https://arxiv.org/abs/2206.08780). |
| Tran et al., *Stereographic Spherical Sliced Wasserstein Distances*, ICML 2024 | Its metric uses stereographic projection and generalized Radon transforms. Its Appendix F relates spherical slice families to stereographic transforms; these are not just equators through the origin. [Official proceedings](https://proceedings.mlr.press/v235/tran24a.html). |
| Quellmalz, Buecher, Steidl, *Parallelly Sliced Optimal Transport on Spheres and on the Rotation Group*, 2024 | The sphere transform retains a slice-offset variable (t\in[-1,1]) and all projection directions. Theorem 3.7 compares the resulting parallelly sliced metric with intrinsic (W_p), including a Hölder inverse estimate. Removing the offset data to retain only equators changes the operator and destroys the displayed point-separation mechanism. [Published full text](https://link.springer.com/article/10.1007/s10851-024-01206-w). |

Other rejected name matches include Euclidean spherical Radon transforms integrating spheres through the origin, spherical slices through a fixed pole, and Funk metrics in Finsler geometry. An inverse or injectivity claim in one of these settings is not a theorem about Stephens's (R). Some source-access attempts were incomplete; they are recorded as retrieval limitations, not as negative literature evidence.

No examined later primary text was identified as an explicit exact answer to the original reverse inequality. This is a bounded search outcome only. Its exact remaining bibliographic gap is finding, if it exists, a paper or documented mathematical answer that expressly addresses the 2008 Wasserstein formulation. That gap does not alter the checkable parity counterexample or its classical provenance.

## Original target versus the stronger adjunct

The original all-probability question is already contradicted by two antipodal point masses, or by smooth positive densities differing by an odd coordinate. Restricting to even measures removes these examples and changes the mathematical question. On that domain the classical function transform is injective; lack of a uniform inverse Lipschitz bound then requires a quantitative mechanism rather than the odd kernel.

The frozen proof's even-density high-frequency claim has different hypotheses and a different mechanism. Its claimed sequence, rates, dimension boundary, transport estimates, and priority need independent checking. Validity or novelty of that restricted theorem cannot imply that the unrestricted 2008 question was open. Conversely, classical failure on all probabilities does not refute the even-density theorem or settle whether its exact conclusion is a routine deduction from other earlier results.

## Audit disposition

- **Original negative conclusion:** independently verified, exact admissible counterexample given.
- **Original priority:** classical obstruction directly documented in 1913; the inverse-bound failure is a routine deduction. Recommend `already_solved`, with the stated meaning.
- **Explicit earlier exact Wasserstein publication:** unlocated in this bounded search; no assertion of nonexistence or first publication.
- **Stronger even-density theorem:** separate; no novelty or already-solved certificate from this audit.
- **Changes made:** research notes in this audit's own folder only. No status, PR, Git, external messaging, or cloud action.

Completion estimate: **100% of this assigned original-question priority audit**. This is not an estimate that the separate even-density research problem or all possible historical bibliography has been completed.
