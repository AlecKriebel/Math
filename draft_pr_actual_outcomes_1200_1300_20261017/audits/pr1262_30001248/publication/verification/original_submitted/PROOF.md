# Triangle modulus threshold: credited coverage for 30001248 / OWR-3473-009

Date: 2026-10-11 (UTC). This is a source audit and a complete reduction from a cited quantitative local limit theorem, not a claim to a new triangle local limit theorem or to priority for the corollary. It does not certify every proof in the cited papers.

Review and distribution status: AI-assisted and unrefereed. Acceptance means an
internal AI mathematical audit, not external human peer review or formal
proof-assistant certification. This is a prose edition, not a computational
reproduction package. No new LLT, first-resolution, or priority claim is made.

Recovery scope: all three complete authored mathematical reports were recovered
byte-for-byte and match the previously recorded SHA-256 hashes. The earlier
full evidence packages and their external seals are unavailable in this edition.
Statements below about earlier source inspection and finite checks describe
historical work recorded in those exact reports; they are not claims that the
old supporting packages were recovered or that the checks were newly rerun.

## 1. Exact target and verdict

Problem 30001248 / OWR-3473-009 asks, for fixed p in (0,1) and the triangle count X in G(n,p), how far modular equidistribution and the local limit theorem extend beyond q=o(n²/log n). The mathematical target is the relative uniform-in-residue metric defined below, for ordinary unlabeled triangles and fixed p.

Let T count unordered triples spanning a triangle in the simple undirected labeled-vertex graph G(n,p), with no loops, independent edges, and fixed 0<p<1. A triangle is counted once, not six times. Write μ=E T, σ²=Var T, and let q=q(n) be any positive integer. Define the original relative, uniform-in-residue metric

    Δ_n(q) = max_{0≤a<q} |q P(T≡a mod q) − 1|.

Then, using the published quantitative LLT of Sah and Sawhney as an explicitly imported premise, the complete answer is

    Δ_n(q(n)) → 0  if and only if  q(n)=o(n²).

No primality or divisibility condition is needed. The fixed-p triangle LLT itself was already asserted in Scott–Tateno's 2009 report and subsequently proved quantitatively; a modulus is not a parameter in an ordinary LLT. Thus the curated triangle target is covered by prior LLTs plus the explicit summation and sharpness arguments below. The source's broader final conjecture, an analogous Gaussian LLT for every fixed subgraph H, is false without restrictions: H=2K₂ is a credited counterexample of Sah–Sawhney, reconstructed in Section 8. That broader conjecture is not substituted for the exact triangle question.

## 2. Source-matched coverage

- Scott, joint with Tateno, “On the Number of Triangles in a Random Graph,” Oberwolfach Report 23/2009, printed pp.1279–1280, PDF pp.55–56: p is fixed in (0,1); Theorem 2 gives Δ_n(q)→0 for integer q=o(n²/log n), with no primality condition. Theorem 3 already gives a uniform triangle LLT with Gaussian unit-cell masses and error o(n⁻²). The surrounding text notes the necessary scale q=o(n²) and ends by conjecturing analogous results for any fixed H. The report gives a proof description, not a full technical proof. [Primary source](https://ems.press/journals/owr/articles/3473).
- Berkowitz, arXiv:1610.01281v3, pp.1–3: quantitative triangle point and L¹ bounds are stated for fixed p. The retained v3 has narrow printed normalization defects, detailed in Section 9. These are not grounds to reject the paper as a whole. The present proof does not depend on reading the defective display as a literal true formula. [Version](https://arxiv.org/abs/1610.01281v3).
- Sah–Sawhney, arXiv:2006.11369v1, Theorem 1.1, p.3, with count convention and independent-model transfer in pp.28–31: for fixed connected H with at least two vertices, p bounded away from 0 and 1, true mean μ_H and standard deviation σ_H, the supremum over every integer x of |σ_H P(X_H=x)−φ((x−μ_H)/σ_H)| is O_{H,λ,ε}(n⁻¹ᐟ²⁺ε), and an L¹ bound of the same normalized rate is also given. The imported premise here is only the first, uniform pointwise bound, specialized to H=K₃. [Version](https://arxiv.org/abs/2006.11369v1); [published DOI](https://doi.org/10.1112/jlms.12523).
- Sah–Sawhney, Theorem 1.2, p.3: the induced-copy analogue requires p to remain separated from a graph-dependent finite set of problematic densities, as well as from 0 and 1. Theorem 1.3, pp.3–4, gives a disconnected ordinary-subgraph counterexample 2K₂ and a separate induced-copy counterexample at p=1/2. Neither a theorem for all induced counts at all p nor a theorem for all disconnected ordinary counts follows.
- DeMarco–Kahn–Redlich, EJC 22(1) (2015), P1.37, pp.1–2: q>1 is fixed, the connected graphs are pairwise nonisomorphic and have at least two vertices, and counts are unlabeled. Their sparse result assumes p/ n^{-1/m(G)}→∞; exponential constants depend on q and the graph family. This is useful fixed-q coverage, not a bound uniform for growing q. [DOI](https://doi.org/10.37236/4094).
- Sah–Sawhney–Zhu, arXiv:2412.09535v1, pp.1–3: Theorem 1.1 explicitly restates the clean connected-H premise above. The joint theorem is for a fixed finite downward-closed collection of nonisomorphic connected graphs with at least two vertices, at p bounded away from 0 and 1, with permissible graph-factor coordinates and their skew-lattice normalization. It is a nonlinear transform of Gaussian graph factors; it is not an independent product-Gaussian theorem for arbitrary raw subgraph counts. The joint theorem is not needed for the triangle conclusion. [Version](https://arxiv.org/abs/2412.09535v1).

The 2020 source's omission of “at least two vertices” in its short Theorem 1.1 wording does not license division by the zero variance of the one-vertex count. Its nontrivial graph-count setting, and the explicit 2024 restatement, resolve that boundary. All uses here have H=K₃.

## 3. Exact moments, scale, lattice, and an independent CLT

Let N=binom(n,2), write I_e for an edge indicator and Y_e=I_e−p, and set v=p(1−p). Expanding each triangle gives the exact orthogonal decomposition

    T−μ = p²(n−2) Σ_e Y_e
            + p Σ_{unordered adjacent edge pairs {e,f}} Y_e Y_f
            + Σ_{triangles {e,f,g}} Y_e Y_f Y_g.

Distinct sets of edges index orthogonal centered products under the independent edge measure. There are 3 binom(n,3) adjacent edge pairs. Therefore

    μ = binom(n,3) p³,
    σ² = binom(n,2)(n−2)² p⁵(1−p)
           + 3 binom(n,3)p⁴(1−p)²
           + binom(n,3)p³(1−p)³
       = binom(n,3)p³(1−p³) + 12 binom(n,4)p⁵(1−p).

The coefficient 12 in the last expression counts ordered distinct triangle pairs sharing an edge; using 6 would miss the factor 2 in the variance sum. In particular,

    σ² ~ [p⁵(1−p)/2] n⁴,  and  σ=Θ_p(n²).

Let α=p⁵(1−p)>0 and D=N(n−2)². The exact formula gives σ²≥αD. The first component L=p²(n−2)ΣY_e has variance αD. The remaining component has variance O_p(n³), so (T−μ−L)/σ→0 in L². The ordinary binomial central limit theorem applied to ΣI_e, together with Var L/σ²→1, proves

    Z_n=(T−μ)/σ ⇒ N(0,1).

This supplies the CLT needed for sharpness independently of the subgraph LLT premise. Also E|Z_n|≤1 because E Z_n²=1.

The support of T contains both 0 (the empty graph) and 1 (exactly one triangle with all other vertices isolated), each with positive probability for n≥3. Thus its maximal integer lattice span is 1. Counts of labeled triangle embeddings would instead be 6T, have span 6, and require a different statement. In particular they cannot be uniform modulo an integer sharing a nontrivial divisor with 6. No such labeled-count replacement is made here.

## 4. A quantitative pointwise premise, not just an additive o(1)

Choose λ>0 with λ<p<1−λ. Sah–Sawhney Theorem 1.1 applied to K₃ gives, for any fixed ε>0,

    sup_{k∈Z} |P(T=k) − g_n(k)| ≤ δ_n/σ,
    g_n(x) = σ⁻¹ φ((x−μ)/σ),
    δ_n = C_{p,ε} n^{-1/2+ε},
    φ(u) = (2π)^(-1/2) exp(−u²/2).

The supremum is over all integers, with a constant independent of k and q. Take 0<ε<1/2, for example ε=1/4. Quantitative decay is important: δ_n sqrt(log n)→0. Neither an unspecified o(1) normalized LLT error nor a naked total-variation convergence statement may simply be multiplied or summed to conclude the relative growing-q result.

This is an ordinary invocation of a prior theorem. The whole 2020 PDF is retained, but only the locations in the source ledger were inspected. Its complete Fourier/decoupling proof is not independently re-proved or certified here. No unpublished lemma or claimed 2024 publication status is required.

## 5. Uniform tails at the exact standard-deviation scale

Changing one of the N independent edges changes T by at most n−2. The bounded-differences estimate follows from the Doob exposure martingale and Hoeffding's lemma: a martingale increment with conditional range length at most c has centered exponential moment at most exp(t²c²/8). Multiplication and Markov's inequality, optimized at t=4u/D, give

    P(|T−μ|≥u) ≤ 2 exp(−2u²/D).

Here D=Σ_e(n−2)². Since σ²≥αD,

    P(|T−μ|≥Rσ) ≤ 2 exp(−2αR²).

For n≥3 put

    R_n = sqrt((16/α) log n).

Then the graph tail is at most 2n⁻³². Constants depend only on the fixed p. For sufficiently large n, σ≥1 and R_n≥4. Put h=1/σ. Monotonicity of φ on each tail, comparing each grid point to its preceding interval towards the origin, yields

    Σ_{k∈Z: |k−μ|>R_nσ} g_n(k)
       ≤ 2 ∫_{R_n−h}^∞ φ(u)du
       ≤ 2 exp(−(R_n−1)²/2)
       ≤ 2 exp(−R_n²/4)
       = 2 n^{-4/α} ≤ 2n⁻¹⁶.

The final inequality uses α=p⁵(1−p)≤p(1−p)≤1/4. These are total tails, so they bound every residue's tail simultaneously, including after multiplication by any q≤σ=O_p(n²).

## 6. Central residue sums and the Gaussian lattice

Fix any integer 1≤q≤σ and residue a. The interval |k−μ|≤R_nσ contains at most 2R_nσ/q+1 integers in a+qZ. Summing the uniform LLT only on that finite interval, and bounding the two tails separately as in Section 5, gives

    q |P(T≡a mod q) − Σ_{k∈a+qZ} g_n(k)|
      ≤ δ_n(2R_n+q/σ) + 2q(n⁻³²+n⁻¹⁶).                     (1)

No bound is summed over infinitely many points. The number of central summands, both tails, and all factors of q have been retained explicitly.

For completeness, if f is absolutely continuous, f∈L¹(R), and ∫|f'|<∞, a shifted mesh of width h>0 satisfies

    |h Σ_{j∈Z} f(b+jh) − ∫_R f(u)du| ≤ h ∫_R |f'(u)|du.

Indeed, compare h f(b+jh) with the integral over [b+jh,b+(j+1)h], bound the difference by h times the integral of |f'| on that interval, and sum. The Gaussian is integrable and has total variation ∫|φ'|=sqrt(2/π). Taking h=q/σ and b=(a−μ)/σ proves the estimate uniform in a and μ

    |q Σ_{k∈a+qZ} g_n(k) − 1| ≤ sqrt(2/π) q/σ.             (2)

Combining (1) and (2) gives the explicit all-residue bound

    Δ_n(q) ≤ C_{p,ε} n^{-1/2+ε}(2R_n+q/σ)
               + 2q(n⁻³²+n⁻¹⁶) + sqrt(2/π) q/σ,
    1≤q≤σ.                                                  (3)

In particular, every positive integer sequence q=o(σ)=o(n²) eventually lies in this range; every term in (3) tends to zero. This proves the full relative growing-q sufficiency, including sequences approaching σ arbitrarily slowly, such as q≈σ/log log log n. The bound is on max_a|qP−1|, not merely max_a|P−1/q|, total variation, fixed residues, or prime q.

One may improve (2) by Gaussian Fourier summation, but its elementary O(q/σ) error already proves the exact requested range. No improved error rate is claimed here.

## 7. Sharpness: every sequence outside o(n²) fails

Suppose Δ_n(q_n)→0 but q_n is not o(σ_n). There is a subsequence with q_n/σ_n≥c>0. On a further subsequence, r_n=σ_n/q_n converges to some r∈[0,1/c]. Along this subsequence q_n≥2 eventually. Relative uniformity forces its first modular Fourier coefficient to vanish:

    |E exp(2πi T/q_n)|
     = |Σ_{a=0}^{q_n−1} (P(T≡a)−1/q_n) exp(2πi a/q_n)|
     ≤ Σ_a |P(T≡a)−1/q_n| ≤ Δ_n(q_n) → 0.

But the centering phase has modulus 1, so the same modulus equals

    |E exp(i t_n Z_n)|,   t_n=2πσ_n/q_n → t=2πr.

The varying-frequency step is justified quantitatively by

    |E exp(i t_n Z_n)−E exp(i t Z_n)|
       ≤ |t_n−t| E|Z_n| ≤ |t_n−t| → 0.

The CLT from Section 3 implies E exp(i t Z_n)→exp(−t²/2). The limiting modulus is exp(−2π²r²)>0, including 1 if r=0. This contradicts the preceding vanishing coefficient. Hence relative uniformity requires q=o(σ), proving the “if and only if” claim.

This is a qualitative necessity argument based on the CLT; it does not claim a finite-n lower bound uniform in every q. A sequence with q/σ bounded below only on a subsequence already fails convergence of Δ to zero. The argument therefore covers oscillating sequences as well as q≈cσ and q≫σ.

## 8. Compact reconstruction of the credited disconnected obstruction

This section independently reconstructs Sah–Sawhney's 2K₂ example for ordinary unlabeled copies, using elementary conditional moments. It is not a new counterexample claim.

Let M be the number of edges, W=Σ_v binom(d_v,2) the number of unordered adjacent edge pairs, and Y the number of unordered disjoint edge pairs. Exactly

    Y = binom(M,2) − W.

For N=binom(n,2), m=floor(pN), and r=m/N, condition on M=m. The resulting graph is uniform G(n,m). Put A=N(n−2), the number of adjacent edge pairs, and π_j=(m)_j/(N)_j. A fixed adjacent pair has 2 edges. Each of its two edges is in 2(n−2) adjacent pairs, so the number of other adjacent pairs sharing exactly one edge is 4n−10. Consequently B=A(4n−10) is the number of ordered pairs of distinct adjacent pairs sharing one edge. Exact conditional moments give

    Var(W|M=m)
      = A(π₂−π₄)+B(π₃−π₄)+A²(π₄−π₂²).                  (4)

For j=2,3,4, with r bounded away from 0 and 1, the finite-product expansion is uniform:

    π_j = r^j − binom(j,2) r^(j−1)(1−r)/N + O_p(N⁻²).

Thus π₃−π₄=r³(1−r)+O_p(N⁻¹) and
π₄−π₂²=−4r³(1−r)/N+O_p(N⁻²). The potentially n⁴-order contributions in (4) cancel because

    B−4A²/N = A[(4n−10)−4(n−2)] = −2A = O(n³).

The remaining errors are O(A)+O(B/N)+O(A²/N²)=O_p(n³). Thus Var(W|M=m)=O_p(n³), and the same holds for Y given M=m.

Chebyshev's inequality puts at least 3/4 of the conditional mass of Y in an interval of O_p(n^{3/2}) consecutive integers. Therefore at least one integer y_n has P(Y=y_n|M=m)≥c_p n^{-3/2}. Stirling's formula for the binomial M gives P(M=floor(pN))≥c'_p n⁻¹. Hence

    sup_y P(Y=y) ≥ c''_p n^{-5/2}.                          (5)

Its actual unconditional standard deviation is Θ_p(n³), not n^{5/2}: the orthogonal expansion over independent centered edges is

    Y−E Y = p binom(n−2,2) Σ_e Y_e
               + Σ_{unordered disjoint pairs {e,f}} Y_eY_f,
    Var Y = N binom(n−2,2)² p³(1−p)
               + 3 binom(n,4)p²(1−p)² = Θ_p(n⁶).

The span is 1, since the empty graph gives Y=0 and exactly two disjoint edges give Y=1. Thus (5) is a factor Ω_p(sqrt n) larger than the Gaussian LLT scale 1/σ_Y. A uniform Gaussian LLT would imply sup_y P(Y=y)≤(1/sqrt(2π)+o(1))/σ_Y, contradicting (5). The obstruction is genuine even after using the correct count category and lattice span. No claim that every disconnected graph behaves identically is needed.

## 9. Narrow transcription and version corrections

The retained Berkowitz PDF has SHA-256 411873584c8992f0b802fe98b3c65f2022c78058fa2d70d14b9ac804e2ceee1d, 291,012 bytes, and the stamp arXiv:1610.01281v3, 21 Mar 2017. Its title page displays November 27, 2024. The arXiv landing history still identifies v3 with the March 2017 revision. The internal date is reported as an observed date mismatch, not treated as a new arXiv version or assigned an unverified cause.

Visual inspection confirms that its p.2 Theorem 1 displays p³ binom(n,2) where the triangle mean is p³ binom(n,3). Its p.1 introduction correctly uses binom(n,3), but calls σ=Var(T) while using standard-deviation normalization. Its p.3 normalized-variable discussion explicitly has mean zero and variance one. The minimal repair for the formulas used in this audit is therefore μ=binom(n,3)p³ and σ=sqrt(Var T), with the exact variance in Section 3. This audit does not edit the source PDF, assert that every version has the same defects, dismiss the rest of the paper, or certify its full proof.

The clean Sah–Sawhney formulation, also explicitly restated in the 2024 joint paper, avoids reliance on that repair. For the original 2009 Gaussian cell convention define

    c_n(k)=∫_{(k−μ−1/2)/σ}^{(k−μ+1/2)/σ} φ(u)du.

The midpoint Taylor bound gives |c_n(k)−g_n(k)|≤||φ''||∞/(24σ³), uniformly in k. Consequently the cited quantitative density LLT also gives the original cell-mass LLT, with error O_{p,ε}(n^{-5/2+ε})+O_p(n⁻⁶), in particular o(n⁻²) when ε<1/2. This is an explicit equivalence of conventions, not a silent change of target.

## 10. Disposition, limits, and validation meaning

For the exact fixed-p triangle record, there is no remaining mathematical range gap after the cited quantitative theorem is imported and Sections 3–7 are checked. Appropriate credit is to the existing triangle/connected-subgraph LLT literature and the original Scott–Tateno question. The corollary and its sharpness are reconstructed here for coverage; no exhaustive search for the first place this corollary was stated, and no novelty claim, is made.

The generic “any fixed H” Gaussian extension is false as stated. Connected ordinary counts have prior positive coverage; induced counts require the source's restrictions; joint/disconnected counts may have non-Gaussian local structure. Sparse p(n), general varying-p endpoints, optimal error constants, all induced densities, and arbitrary disconnected modular ranges are not parts silently added to or solved by this triangle result.

The edition's byte checks authenticate the recovered report identities; they do not establish mathematical truth or authorship. Finite exact checks validate the moment formulas and combinatorial counts only, not the asymptotic LLT imported from the literature. The source-read ledger separates whole-file retention, actual inspected passages, and uninspected deep proofs. The mathematical acceptance is recorded in AUDIT.md and ACCEPTANCE.md. The earlier report records that only audit-authored finite checks were run and no source-author program was executed. No such numerical computation was newly rerun for this prose edition.
