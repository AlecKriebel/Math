# Independent verification of the frozen prior-general-theory deduction

Verdict: **PASS** for the exact full-plane endpoint-connector target. No repair of the mathematical deduction is required. This is an independent analytic verification, not formal proof certification or external peer review.

The strongest verified implication is

\[
 M_2(\Gamma(E,\mathbb R\setminus E))<\infty
 \quad\Longrightarrow\quad C_{1,2}(E)=0
 \quad\Longrightarrow\quad M_2(\Gamma(E,S_2))=0.
\]

Consequently positive outer modulus implies infinite complement modulus. Both globally rectifiable connectors and continuous connectors locally rectifiable off the endpoints are covered. Densities may be extended nonnegative Borel functions and admissibility is required on every connector. The plane is the connector domain; there is no extra condition that curve interiors avoid either plate.

## Frozen input and independence

The parent-provided manifest SHA-256 `a3220499ca6c3f0d3f6f4021b252fd4f6fa597a641d5d18ccedfc1ce8bc419c4` matches. All ten declared member sizes/hashes match. The complete frozen DERIVATION, REPORT, VERDICT and SOURCES were read. Their mathematical source bodies were checked against the frozen hashes and primary source locations. INPUT_HASHES.json and EVIDENCE_INVENTORY.json record exact inspection scopes.

No submitted proof, source-question reconstruction, Riesz route, root working checks, other mathematical reviews, or other independent priority-family output was used. No independent-family output was read at any stage of this review. The parent's convention confirmation was used only to settle scope, not to supply a proof. All writes are inside this review's directory. No checkout, index, commit, push, release, external message, or application mutation was made.

## Exact imported results checked

- **Hesse:** Definitions 3.1–3.2, printed p.132 (PDF page 2), and Theorem 5.5, printed p.141 (PDF page 11), were read and rendered. The closure bar on the curve image in Definition 3.2 is present. The potentials are continuous on the domain and the compact plates, are ACL on the finite part of the domain, and have exact values 0 and 1. The equality's interior-plate hypothesis holds here. The theorem is not being applied to touching or noncompact plates. The original journal metadata gives December 1975, volume 13, pp.131–144, DOI 10.1007/BF02386202. [Primary scan](https://archive.ymsc.tsinghua.edu.cn/pacm_download/116/7225-11512_2006_Article_BF02386202.pdf), [publisher metadata](https://link.springer.com/article/10.1007/BF02386202).
- **Fractional trace:** DNPV Proposition 3.8 and its Fourier estimate apply at input exponent s=1, hence map planar H^1=W^{1,2} continuously into line H^{1/2}. Proposition 3.4 identifies the latter Fourier space with its Gagliardo definition. Its restriction s∈(0,1) is used at the output exponent 1/2, not at the input exponent 1. The arXiv history dates v3 to 19 November 2011. [Version record](https://arxiv.org/abs/1104.4345), [v3 body](https://arxiv.org/pdf/1104.4345v3).
- **Critical rigidity:** Brezis Corollary 1 and Remark 3 apply to the integer-valued trace on connected R with p=2, N=1. They force a finite H^{1/2} characteristic function to be constant almost everywhere. The inspected author body is not being used to assert oldest priority. Remark 3 itself attributes the special case to an earlier Hardt–Kinderlehrer–Lin lemma, whose original body was not authenticated in this review. The journal record confirms the matching title, author and 2002 publication. [Author body](https://sites.math.rutgers.edu/~brezis/PUBlications/180.pdf), [journal metadata](https://www.mathnet.ru/eng/rm533).
- **Capacity representatives:** In the served Diening–Harjulehto–Hästö–Růžička draft, Definition 10.1.1 is the inhomogeneous whole-space Sobolev capacity. Lemma 11.1.2 gives quasi-everywhere subsequential convergence for continuous Sobolev Cauchy sequences; its quasiuniform conclusion supplies a quasicontinuous limit. Lemma 11.1.4(a) gives uniqueness up to capacity zero. Corollary 11.2.5 gives quasicontinuous zero extensions for zero-boundary functions. All hypotheses hold for constant exponent 2 and Euclidean half-planes, with ordinary smooth density. The relevant pages were visually checked. [Author-hosted draft](https://www.math.lmu.de/~diening/archive/book.pdf).
- **Half-space kernel:** Hunter Theorem 3.42 is explicitly introduced in the first-order setting. The displayed k in its final sentence is not used as a higher-order theorem: this proof uses k=1 only. The direct cutoff argument below independently verifies the needed implication. [Course notes](https://www.math.ucdavis.edu/~hunter/m218a_09/ch3.pdf).

## Analytic verification of each interface

**1. Finite modulus supplies exactly the needed uniform compact-condenser bound.** Assume a finite-energy admissible Borel density rho exists. Put Q=(-2,3)×(-2,2) and use the frozen increasing compact exhaustion F_j. Nonemptiness follows already from real points to the left of 0; the distance and rectangle-margin conditions ensure each F_j is compactly inside Q and disjoint from compact E. Every point of (R\E)∩Q belongs to some F_j because its distance from the closed E and from the rectangle's vertical boundary is positive.

For epsilon>0, define rho_epsilon piecewise to be rho+epsilon in Q and zero outside Q. A Hesse curve in Q of infinite total Euclidean length has infinite rho_epsilon-length. A finite-length Hesse curve has an arclength reparametrization extending to a compact rectifiable curve whose image equals the old image closure. That compact curve meets both E and F_j, so a subconnector has rho-length at least 1 by the assumed full-plane admissibility. Its endpoints are interior to Q. Nonnegative line integrals on the whole Hesse curve dominate the subconnector integral. Values at isolated endpoints do not contribute arclength. Thus rho_epsilon is admissible for Hesse's entire locally rectifiable image-closure family, even when rho is infinite on a planar null set. Minkowski's inequality gives ||rho_epsilon||_2→||rho 1_Q||_2, so Hesse's modulus is uniformly bounded by ∫_Q rho².

Hesse then supplies continuous ACL u_j with the exact plate values and uniformly bounded energy. Truncation to [0,1] preserves ACL and decreases energy. Since Q has finite area, bounded u_j and their L² first derivatives are in W^{1,2}(Q). For fixed eta compactly supported in Q and equal to 1 near E, w_j=eta(1-u_j), extended by zero, is continuous on R² and belongs to W^{1,2}(R²). The product rule gives a bound depending only on eta and the common gradient bound. All w_j have support in the same compact K, equal 1 on E and 0 on F_j.

**2. Tail convexification does preserve the thin plate.** Weak compactness followed by Mazur gives finite convex combinations of tails of a subsequence, v_n→w strongly in W^{1,2}. Since original subsequence indices increase, every term in sufficiently late tails vanishes on any fixed F_k. Convex combinations retain the common value 1 on E, the common zero value on F_k, the [0,1] bound and support K. The continuous-sequence capacity lemma gives a subsequence with pointwise convergence outside one capacity-zero set N to a quasicontinuous representative w*. Strong L² convergence identifies that pointwise limit with w almost everywhere; capacity-zero sets are Lebesgue null. Therefore w*=1 on E\N and w*=0 on ((R\E)∩Q)\N. This uses capacity convergence, not an arbitrary almost-everywhere representative.

**3. The ordinary trace really is 1_E.** On every real point outside E, v_n eventually vanishes, either by exhaustion or by the common support. On E it is identically 1. Dominated convergence on the fixed compact line support therefore yields v_n|_R→1_E in L²(R). For a continuous compactly supported Sobolev v_n, smooth mollification converges both uniformly and in W^{1,2}; this proves its ordinary trace is its pointwise restriction almost everywhere. Trace continuity consequently gives Tw=1_E, and the trace lies in H^{1/2}(R). Brezis's rigidity makes 1_E constant almost everywhere. Since it has compact support, the constant is 0. Thus Tw=0 and |E|=0. No capacity conclusion is drawn from length alone.

**4. Zero trace kills the capacity on the entire line.** The global trace agrees with each one-sided half-plane trace: smooth approximation proves equality of these continuous operators. The upper and lower restrictions therefore have zero trace. To check the kernel implication directly, on almost every vertical slice of the upper half-plane take the absolutely continuous representative with w(x,0)=0. Then

\[
 |w(x,y)|^2\le y\int_0^y|\partial_y w(x,t)|^2\,dt.
\]

For a cutoff chi_epsilon which is 0 below epsilon, 1 above 2epsilon and has derivative at most c/epsilon, Fubini yields

\[
 \int_{\epsilon<y<2\epsilon}|\chi_\epsilon' w|^2
 \le 2c^2\int_{0<y<2\epsilon}|\partial_yw|^2\longrightarrow0.
\]

The remaining W^{1,2} errors are integrals of |w|²+|grad w|² over a shrinking boundary layer. Compact support then permits smoothing inside the half-plane. The lower half-plane is identical. Thus both restrictions belong to their ordinary W^{1,2}_0 spaces.

The zero-extension corollary provides whole-plane quasicontinuous representatives w_+, w_- vanishing quasi-everywhere outside the corresponding open half-plane, including on its boundary. Their sum equals w almost everywhere and is zero quasi-everywhere on R. Quasicontinuous uniqueness implies w*=w_++w_- quasi-everywhere. Combining w*=0 quasi-everywhere on R with w*=1 quasi-everywhere on E shows E is contained in a finite union of capacity-zero sets. Hence C_{1,2}(E)=0. Both half-planes are essential to this representative comparison; a statement only about |E| would leave the zero-length positive-capacity case open.

**5. The final gradients are admissible for every curve.** Capacity zero gives nonnegative h_m∈W^{1,2} with norm→0 which are at least 1 almost everywhere on some open O_m⊃E. Multiply by the fixed cutoff xi equal to 1 near E and supported in B(0,3/2). Choose a nonnegative unit-integral mollifier radius smaller than dist(E,R²\(O_m∩{xi=1}))/2, and small enough for support in B(0,7/4). Compactness makes this radius positive. The convolution phi_m is smooth, phi_m≥1 on E, vanishes on S_2, and has gradient energy→0 by the Sobolev product estimate and convolution contraction.

For every compact rectifiable endpoint connector, the chain rule for the smooth phi_m gives ∫_gamma|grad phi_m|≥|phi_m(start)-phi_m(end)|≥1. For a continuous curve locally rectifiable away from its endpoints, exhaust its open parameter interval by compact subintervals, apply that inequality there, and pass to the endpoints using continuity and monotone convergence of nonnegative line integrals. Hence no exceptional family remains. The smooth gradients themselves are finite continuous Borel densities, sufficient even in the larger allowed extended-density class.

If the modulus infimum is finite, a finite-energy admissible density exists by the definition of infimum. Its nonexistence under positive outer modulus therefore means the complement modulus is infinity. E empty is vacuous. Finite sets, E=[0,1], positive-length compact sets and zero-length positive-capacity compact sets introduce no missing case.

## Adversarial tests and exact residual limitations

The following possible failures were tested analytically and did not occur: applying a compact theorem to noncompact F; losing values on thin E in a weak limit; confusing pointwise restriction with trace; concluding capacity zero from length zero; using only one half-plane; treating almost-every-curve control as all-curve control; omitting infinite-length Hesse curves; assuming endpoints have a meaningful density contribution; and applying the s∈(0,1) Fourier/Gagliardo result at s=1. No numerical or finite-case experiment substitutes for any proof step.

The claim supported by this check is a complete deduction assembled on 17 October 2026 from the cited general theory. It is not an authenticated earlier printed resolution of Problem 7.58. The frozen report's distinction is sound.

The served monograph body is internally dated 3 December 2010; its chapter begins on printed p.333 and the cited lemmas are at pp.334–341. The publisher's final chapter occupies pp.339–366. The body/page match to the final edition and the historical public-posting date of the exact served draft were not established. The current publisher page authenticates the 2011 book and separately shows eBook publication 29 March 2011; the chapter page has several 2011 date fields. None proves a 2010 public posting or author recognition of the exact corollary. [Book metadata](https://link.springer.com/book/10.1007/978-3-642-18363-8), [chapter metadata](https://link.springer.com/chapter/10.1007/978-3-642-18363-8_11).

No earlier-explicit-resolution, oldest-source, first-solution, worldwide-openness, or novelty conclusion follows from this verification. The broader search's negative claim is outside this narrow proof audit and was not independently replicated. No required mathematical repairs are identified. Optional expository clarifications are to retain the explicit whole-plane/no-interior-avoidance convention, distinguish draft from final numbering, and define restricted extended densities piecewise to avoid the notation 0·infinity.
