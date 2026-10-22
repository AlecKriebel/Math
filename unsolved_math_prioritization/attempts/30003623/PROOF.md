# Complete authored proof audit of the unrestricted real Chebyshev converse

This is an AI-assisted, unrefereed proof-audit edition. Acceptance records an independent internal AI audit of the existing Alpan–Zinchenko converse. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim. The description of this edition as AI-assisted does not attribute an authoring method to the cited manuscript.

This is not a computational reproduction package. The complete authored mathematical reconstruction is retained once in PROOF.md. Copied source PDFs, HTML, extracted source text, source images, executable code, raw datasets, raw search responses and private coordination material are not distributed. Public source identities and inspection limits are metadata, not substitutes for mathematical proof.

Source retrieval and inspection statements describe the original audit of October 11, 2026 UTC. Editorial preparation authenticated the sealed inputs but performed no new scholarly-source retrieval, source-body inspection, literature survey, or mathematical execution.

## Verdict and attribution

**Audit passes for the converse needed by problem 30003623 / OWR-15954-001.** No mathematical gap was found in the determinant, quantile-entropy, and gap-approximation argument. Both existential questions have negative answers in the original class of regular compact subsets of the real line with positive logarithmic capacity. This is a source-credited result of Gökalp Alpan and Maxim Zinchenko, not a new result of this audit.

The exact source is *A four-way Szegő theorem for L^p extremal polynomials on subsets of R*, arXiv:2608.17321v1, submitted 18 August 2026 at 03:26:39 UTC. Corollary 3.7 is on printed/PDF page 22. The mathematical engine is Lemmas 3.3–3.4 and Theorem 3.5, pages 13–21. The official landing page inspected on 11 October 2026 displayed only v1 and no journal reference. Its arXiv DOI does not establish journal publication or peer review.

- Versioned landing page: https://arxiv.org/abs/2608.17321v1
- Versioned PDF: https://arxiv.org/pdf/2608.17321v1
- Versioned HTML: https://arxiv.org/html/2608.17321v1
- DOI: https://doi.org/10.48550/arXiv.2608.17321

The PDF was independently retrieved from the versioned URL, rather than relying only on another reader's copy. Its SHA-256 is `e9c3152c41d6c3f98aee305ad3dee9c3b123419c12aad32cf855e70952d8d435`; its size is 501,510 bytes; it has 34 pages. It matches the separately retrieved unversioned-URL PDF byte for byte by SHA-256.

## 1. Target and exact hypothesis match

Let E be a compact subset of R, regular for the Dirichlet problem, with c = Cap(E) > 0. Write T_n for the monic degree-n polynomial of least supremum norm on E and

\[
W_{\infty,n}(E)=\|T_n\|_E/c^n.
\]

The target asks whether there can be a constant D < infinity satisfying W_{infinity,n}(E) <= D for **every** n >= 1, even though E is not Parreau–Widom. It also asks whether such an E can have Lebesgue measure zero. A bounded subsequence does not satisfy the target.

For each bounded gap (a_j,b_j) of E, g_E has a unique interior maximum at z_j. Put PW(E) = sum_j g_E(z_j), allowing infinity. The source proves

\[
\sup_{n\ge1}W_{\infty,n}(E)<\infty
\quad\Longleftrightarrow\quad PW(E)<\infty
\quad\Longleftrightarrow\quad
\sup_{n\ge1}W_{2,n}(E,\mu_E)<\infty.
\]

All hypotheses match the standing hypotheses of the original report. For the source's general support K = K_0 union X, specialize K_0 = E, X empty, weight 1, and measure mu_E. The isolated-point and Szegő conditions are automatic. Constant weight 1 meets boundedness, full support, Borel measurability, and upper semicontinuity requirements. Positive Lebesgue measure is **not** an assumption.

The 2017 conditional converse assumes a canonical generator. The new argument does not invoke that condition, characters, character density, the direct Cauchy theorem, or a character-space compactness argument. Its real-line quantile partition is the replacement. This audit does not extend the result to arbitrary complex compact sets.

## 2. Independent reconstruction of the decisive argument

This section records the mathematical verification in fresh notation. It is an audit of the cited argument and claims no novelty. Standard logarithmic-potential facts, finite-gap equilibrium densities, and the variational characterization of relative entropy are identified explicitly below.

### 2.1 Equal-equilibrium-mass cells exist, including for singular measures

Write [A,B] = conv(E), L = B-A, mu = mu_E, and lambda = dx/L on [A,B]. Positive capacity gives L > 0. The probability mu has finite logarithmic energy, hence no atoms. Its support is E. The distribution function

\[
F(x)=\mu([A,x])
\]

is therefore continuous and maps [A,B] onto [0,1]. Its nonsingleton fibers are exactly closed bounded gaps of E. Let q(t) be the right endpoint of the fiber F^{-1}({t}). Then q is Borel and strictly increasing. Put q_0=A, q_N=B, q_k=q(k/N) for 1 <= k < N. The cells

\[
C_1=E\cap[A,q_1],\qquad C_k=E\cap(q_{k-1},q_k]\quad(k\ge2)
\]

have mu-mass 1/N. Their containing intervals have positive lengths ell_k = q_k-q_{k-1}. No atom is split at a cell boundary. Set nu_k = N mu|_{C_k}; these are probabilities.

The partition statistic is

\[
H_N=\frac1N\sum_{k=1}^N\log\frac{L}{N\ell_k}
=\log L-\log N-\frac1N\sum_k\log\ell_k.
\]

This is relative entropy of the two pushforward measures F_*mu and F_*lambda on the N-cell equal-width partition of [0,1]: their cell masses are 1/N and ell_k/L. This identification remains valid when gap frequencies coincide with partition endpoints, because the first cell is closed on the left and all other cells are open on the left.

### 2.2 The quantile map preserves all the relevant entropy

Use the nonnegative convention

\[
\mathcal H(\rho\mid\tau)=\int\log(d\rho/d\tau)\,d\rho,
\]

with value infinity if absolute continuity fails. The paper uses D = -H; keeping the sign explicit avoids reversing its Lemma 3.3.

Let G be the union of closed bounded gaps and let P = F(G), a countable set of gap frequencies. Then mu(G)=0. Outside G, F is one-to-one with inverse q.

If mu << lambda, choose h=dmu/dlambda with h=0 on G. This choice changes h only on a set where mu is zero and its density is zero lambda-almost everywhere; endpoints have lambda measure zero. Then h=(h composed with q) composed with F, almost everywhere. Pushforward integration shows that h composed with q is the density of F_*mu relative to F_*lambda and that its log integral agrees with the original one. Thus

\[
\mathcal H(F_*\mu\mid F_*\lambda)=\mathcal H(\mu\mid\lambda).
\]

If mu is not absolutely continuous relative to lambda, choose a lambda-null Borel set Z outside G with mu(Z)>0. Every point of Z has singleton fiber. Consequently F(Z)=q^{-1}(Z) is Borel and F^{-1}(F(Z))=Z. Its image has F_*lambda-mass zero and F_*mu-mass positive. Both entropies are infinite, establishing the same identity in the singular case. Collapsing gaps therefore does not hide a singular component of mu. The length of a collapsed gap remains as an atom of F_*lambda, at a frequency not charged by F_*mu.

Along N=2^m, the equal-width partitions refine. The log-sum inequality gives monotonicity of H_N. Their entropies converge to the entropy of the measures because positive continuous test functions are uniformly approximable by step functions on these partitions. More explicitly, the variational formula

\[
-\mathcal H(\alpha\mid\beta)
=\inf_{f\in C([0,1]),\ f>0}
\left(\int f\,d\beta-\int(1+\log f)\,d\alpha\right)
\]

has infimum -H_N over positive functions constant on the N cells. The minimizing value on a cell is its alpha-mass divided by its beta-mass. Jensen's inequality gives the other comparison. Taking uniform approximants to each fixed positive continuous f proves

\[
H_{2^m}\uparrow\mathcal H(\mu\mid\lambda).
\]

All cell beta-masses are positive, so these finite-stage calculations have no division by zero. No density of the harmonic-measure frequencies in a character group is needed.

### 2.3 Determinants control the partition entropies

Let t_n be the monic L^2(mu) extremal norm and let G_N be the N by N moment matrix for degrees 0 through N-1. Gram–Schmidt and expansion of the Vandermonde determinant give

\[
\det G_N=\prod_{n=0}^{N-1}t_n^2
=\frac1{N!}\int\prod_{i<j}|x_i-x_j|^2\prod_{k=1}^Nd\mu(x_k).
\]

Restrict the nonnegative integral to configurations having one point in each C_k. There are N! disjoint labeled orders with equal integrals, so the factorial cancels **exactly**. Normalizing the restricted measures supplies N^{-N}. Jensen's inequality then gives, with

\[
I_{ij}=\iint_{C_i\times C_j}\log|x-y|\,d\mu(x)d\mu(y),
\]

the bound

\[
\log\det G_N\ge -N\log N+2N^2\sum_{i<j}I_{ij}.
\]

The logarithms are integrable: on the fixed compact interval their positive parts are bounded; finite logarithmic energy controls the negative part; each nu_k is dominated by Nmu. The Vandermonde integrand is bounded and is positive almost everywhere under the product of the nonatomic cell measures. Thus Jensen and Fubini have their required hypotheses.

The equilibrium energy identity and the partition give

\[
2\sum_{i<j}I_{ij}=\log c-\sum_kI_{kk}.
\]

Since nu_k is a probability supported on an interval of length ell_k, the maximum-energy characterization of capacity gives

\[
N^2I_{kk}\le\log(\ell_k/4).
\]

The sign is important: the self-energy is subtracted, so this **upper** bound yields a lower bound for the determinant. Combining these formulas and using t_0=1 and t_n=c^n W_{2,n} yields

\[
\frac2N\sum_{n=1}^{N-1}\log W_{2,n}
\ge \log\frac{4c}{L}+H_N. \tag{A}
\]

In particular the powers of c are N^2 before subtracting the determinant normalization c^{N(N-1)}, leaving N log c. There is no omitted N!, no unexplained interchange of n and gap limits, and no boundedness assumption concealed in this estimate. It holds for each N >= 2 before any assumption about the sequence W_{2,n}.

### 2.4 Bounded factors force finite entropy

If W_{2,n} <= D for all n, the left side of (A) is at most 2(N-1)log(D)/N. Let N tend through powers of two. The preceding entropy limit gives

\[
\mathcal H(\mu\mid\lambda)\le2\log D-\log(4c/L)<\infty. \tag{B}
\]

For the sharper limsup formulation, put M=limsup W_{2,n}. Every sufficiently large term is <=M+epsilon, and each fixed initial logarithm contributes o(1) to the average. The same upper limit is therefore 2log M. Positivity is available independently: Jensen and the equilibrium potential imply W_{2,n}>=1 in the present unweighted case. No lower asymptotic theorem with PW as a hypothesis is required.

This is already enough for the zero-measure question. Finite relative entropy implies mu << lambda. A probability supported on a Lebesgue-null E cannot be absolutely continuous relative to lambda. Thus bounded factors force |E|>0. This direct consequence avoids any need to import a separate theorem saying PW sets have positive measure.

### 2.5 Entropy controls all the gap heights

To complete the non-PW converse, suppose first the entropy is finite; if it is infinite the desired extended-real inequality below is automatic. Enumerate the bounded gaps and retain only the first m of them, obtaining the decreasing finite-gap outer approximation

\[
E_m=[A,B]\setminus\bigcup_{j=1}^m(a_j,b_j).
\]

Let z_{j,m} maximize g_{E_m} in gap j. The finite-gap equilibrium probability has density

\[
\frac{d\mu_{E_m}}{dx}(x)=
\frac{\prod_{j=1}^m|x-z_{j,m}|}
{\pi\sqrt{|(x-A)(x-B)\prod_{j=1}^m(x-a_j)(x-b_j)|}}.
\]

It is positive almost everywhere on E_m. Since mu << lambda and mu is supported on E, one has mu << mu_{E_m}. Every endpoint occurring in the denominator belongs to the regular set E. The potential identity therefore gives a finite integral log c at each endpoint. Each numerator point is strictly outside E. Integrating the logarithm of this density relative to lambda against mu gives

\[
\int\log\frac{d\mu_{E_m}}{d\lambda}\,d\mu
=\log\frac{L}{\pi c}+\sum_{j=1}^mg_E(z_{j,m}).
\]

The coefficient of log c is m-(m+1)=-1. All logarithmic summands are integrable, so using the chain rule for densities introduces no infinity-minus-infinity ambiguity. Nonnegativity of H(mu|mu_{E_m}) now yields

\[
\mathcal H(\mu\mid\lambda)
\ge\log\frac{L}{\pi c}+\sum_{j=1}^mg_E(z_{j,m}). \tag{C}
\]

If E has finitely many gaps, take all of them in (C), including m=0 for an interval; then E_m=E and the desired inequality follows immediately. Otherwise, for each fixed gap j, g_{E_m} increases to g_E and converges locally uniformly there. The limiting g_E vanishes at the gap endpoints and has a unique positive maximum: its real second derivative is -integral |x-y|^{-2} dmu(y)<0. Because g_{E_m}<=g_E, the maximizers z_{j,m} cannot approach the endpoints once g_{E_m}(z_j) is close to the positive limiting maximum. They lie in a fixed compact subinterval. Local uniform convergence and uniqueness of the limiting maximum imply z_{j,m}->z_j.

Fix r, discard all but the first r nonnegative terms of (C), and let m->infinity; then let r->infinity. This two-stage passage, rather than an unjustified passage of an entire varying infinite sum, proves

\[
\mathcal H(\mu\mid\lambda)
\ge\log\frac{L}{\pi c}+PW(E). \tag{D}
\]

Together (B) and (D) give the audited quantitative converse

\[
PW(E)\le2\log M-\log(4/\pi)<\infty,
\qquad M=\limsup_{n\to\infty}W_{2,n}(E,\mu_E).
\]

Finally, the equilibrium measure is a probability, so for every polynomial P, ||P||_{L^2(mu_E)} <= ||P||_E. Infimizing gives W_{2,n}<=W_{infinity,n}. Bounded unweighted Chebyshev factors therefore meet the premise, proving the unrestricted real converse.

## 3. General weighted-converse checks

The exact target requires only the preceding specialization. For completeness, the additional steps used by Theorem 3.5 were also inspected.

For finite positive measure d rho = w d mu_E + d sigma plus isolated masses, first normalize rho to mass 1. Both its L^2 Widom factors and sqrt(S(E,w)) scale by the same square-root factor, so the asserted ratio is invariant. Replace mu by w mu in the determinant integral above and use monotonicity of the nonnegative Vandermonde integral under adding positive measures. Jensen contributes N integral log w dmu, which is finite because log^+w<=w and S>0 controls the negative part. Equation (A) gains log S(E,w) on the right. The result is

\[
PW(E)\le2\log\bigl(M_2/S(E,w)^{1/2}\bigr)-\log(4/\pi).
\]

For 2<p<infinity, use d eta=w^{2/p}dmu_E. Jensen for the probability mu_E gives ||P||_{L^2(eta)}<=||P||_{L^p(rho)}. The density is integrable by Hölder, has full E support because w>0 mu_E-almost everywhere, and its square-root Szegő factor is S(E,w)^{1/p}. For p=infinity use eta=w^2mu_E and ||P||_{L^2(eta)}<=||wP||_K. Boundedness of w makes eta finite. These reductions use no positive-length premise and no upper semicontinuity of w. Upper semicontinuity is used for the other, upper-bound direction of the four-way theorem, and is automatic in the target specialization.

The implication to the Blaschke condition for isolated X is separate. The proof on pages 9–11 first obtains a zero of each sufficiently high-degree extremal polynomial near each fixed isolated mass: regularity of wmu_E and asymptotic extremality yield equilibrium zero distribution; absence of a nearby zero would make the point value grow at the strictly larger exponential rate c exp(g_E(x)), contradicting its positive mass and the extremal upper norm estimate. Distinct isolated points have disjoint neighborhoods. Jensen then retains their nonnegative Green contributions and passes first to high degree and then over finite subsets of X. The p=infinity case reduces to measures w^qmu_E plus 2^{-j}w(x_j)^q delta_{x_j}, with comparison factor <=2^{1/q}, and lets q->infinity. Full support of the weight forces w(x_j)>0 at each isolated point.

This subsidiary argument uses the standard regular-measure norm comparison and zero-distribution theorems explicitly cited in the paper; their entire monographs were not independently re-proved or inspected for this audit. They are not required for X empty and w=1: the elementary fixed-degree Jensen bound suffices there. No circular use of the new PW converse was found in this dependency chain.

## 4. Specific failure modes checked

1. **Hidden canonical generator:** absent. Gap frequencies are merely a countable set used to describe fibers; they need not be rationally independent or generate anything.
2. **Hidden positive length or absolute continuity:** absent. Lemma 3.4 treats singular mu explicitly; finiteness of entropy is a conclusion of boundedness.
3. **A subsequence substituted for all degrees:** absent. A dyadic subsequence of partition sizes is used, but each determinant averages every polynomial degree from 1 to N-1. Boundedness of isolated degrees alone cannot bound these averages.
4. **Finite-gap constants assumed uniform:** absent in the converse. The finite-gap input is an explicit density identity, followed by nonnegative finite partial sums of the limiting Green heights.
5. **Wrong relative-entropy direction:** checked by using H=-D throughout; both required comparisons have the correct direction.
6. **Missing factorial or capacity normalization:** cancellation and exponent N(N-1) were checked explicitly and visually against page 20.
7. **Energy sign:** an upper bound for self-energy is used only where it is subtracted.
8. **Nonintegrable Jensen expression:** controlled by finite equilibrium energy and the Szegő log integrability; the unweighted case is immediate.
9. **Gap endpoints or quantile plateaus:** endpoints have zero equilibrium mass; the right-endpoint convention and half-open cells preserve the exact masses and refinement.
10. **Interchange of infinitely many gaps and approximation:** the proof keeps r fixed before m tends to infinity and then lets r grow; this is valid.
11. **Limsup versus sup:** every fixed-degree extremal norm is positive and finite on a positive-capacity compact support. Finite limsup is equivalent to finite supremum of the whole sequence here. A bounded-subsequence claim would not be equivalent.
12. **Zero-measure conclusion relying on an unverified premise:** it also follows directly from finite entropy, without the paper's additional Appendix A citation.

## 5. Disposition and limits

- First existential question: **No**, under the original regular, positive-capacity real hypotheses. Bounded all-degree Chebyshev factors imply PW(E)<infinity.
- Second existential question: **No**, in that same class. Bounded factors imply finite entropy relative to interval Lebesgue measure, hence positive Lebesgue measure of E.
- Appropriate disposition: **resolved by a later, publicly available preprint; exact converse independently audited without finding a gap**.
- Attribution belongs to Alpan–Zinchenko, arXiv:2608.17321v1. This audit supplies verification and explanatory reconstruction, not a novelty claim.
- This is not a certification of peer review, a verification of all examples in Section 4, or an audit of every weighted upper-bound dependency. The full proof needed for the original two questions was checked.
- No extension to irregular sets or arbitrary complex planar sets is asserted.

The older target and the reason the canonical-generator proviso mattered were cross-checked against the original OWR report, printed pages 2948–2949, the older converse Theorem 1.4 in arXiv:1709.06707, and Open Problem 2.2 in arXiv:2112.06450. These checks establish target correspondence; they are not used to smuggle the older extra hypothesis into the new proof.

Public target sources:

- https://ems.press/content/serial-article-files/46708?nt=1
- https://arxiv.org/abs/1709.06707
- https://arxiv.org/abs/2112.06450

## 6. Inspection and reproducibility boundary

The complete 34-page PDF was retrieved. Detailed proof inspection covered pages 9–22, including the full central converse on pages 13–21 and exact corollary on page 22; definitions and contextual statements on pages 1–6 and the transition theorem on page 12 were also read. Selected render inspection of pages 20 and 22 confirmed notation, constants, and exact hypotheses. Complete retrieval is not represented as an equation-by-equation audit of the whole 34-page manuscript.

The versioned landing page and versioned HTML were separately retrieved and pinned. Web screenshot retrieval failed with a cache-miss error; local rendering of the independently retrieved PDF succeeded, and the resulting page images were inspected. Utility operations were limited to source retrieval, plain-text extraction, PDF metadata/render inspection, hashing, and authoring the audit files. No source archive, executable manuscript code, experiment, or mathematical source program was run. No remote content, source original, or queue entry was changed.
