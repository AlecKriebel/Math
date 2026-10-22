# Independent derivation of the assembly/Gamma argument

This document is an independently authored audit derivation. It concerns the final mathematical statement for the principal quadratic iterated-limit ensemble. It does not establish novelty, universal priority, public-release correctness, or an overall case disposition. Imported geometric theorems are identified explicitly. No frozen source or manuscript was edited.

## 1. Exact claim and assumptions

Put n=3g−3. The final theorem claims that, after the fixed-genus number-of-squares limit defining ν_g, normalized cylinder areas divided by s_g converge vaguely on (0,∞) to PPP(dx/(2x)) whenever s_g→0 and gs_g→∞. Thus q_n=ns_g satisfies q_n→∞ and q_n/n→0. No monotonicity, regular variation, or quantitative growth rate is assumed or needed. The theorem also claims joint convergence of every fixed moment of finitely many compact-window counts. Throughout, windows are bounded away from zero and infinity; all moment orders and the number of windows are fixed before n grows.

The imported geometric assumptions are exactly the positive stable-graph mixture and surface correspondence of DL, the uniform logarithmic-marked-point coefficient estimate stated in DL (6.1), the DGZZ count generating-function estimate at a fixed t>1 within its disk, and DGZZ's low-k multivertex estimate. The probability part below is proved from these inputs; none of these substantial geometric inputs is independently reproved here.

## 2. Assembly law and conditioning

Write a_j=ζ(2j)/(2j), H(z)=exp(Σ_{j≥1}a_j z^j), and h_n=[z^n]H(z). For any count vector c with Σ_j j c_j=n, summing the ordered-composition weights gives

    P(C=c) = h_n^(-1) ∏_j a_j^(c_j)/c_j!.

Indeed, there are k!/∏c_j! ordered sequences realizing c, where k=Σ_j c_j. This proves normalization and handles repeated component sizes correctly. If independent Z_j~Poisson(a_j) are used only for j=1,...,n, their joint density conditioned on ΣjZ_j=n equals this law. The conditioning probability is exp(−Σ_{j≤n}a_j)h_n>0. There is no conditioning on an infinite Poisson vector with infinite expected number of components.

Shifting c_j to c_j−r_j in the positive finite sum proves, for R=Σ_j j r_j,

    E ∏_j (C_j)_{r_j} = (h_(n−R)/h_n) ∏_j a_j^(r_j),  R≤n,

and gives zero otherwise. This is the relevant conditional-Poisson form of Arratia–Tavaré Lemma 5/(126). The same shift argument applies to positive real a_j without an integer combinatorial interpretation. Both the ordered-composition law and the selected-component formula agree with the prior weighted permutation law: θ_j=ζ(2j)/2, with cycle weight a_j=θ_j/j. The factor 1/2 is therefore fixed before Gamma marking; it is not supplied by the Gamma shape.

## 3. Coefficients and their necessary uniformity

Absolute convergence for |z|<1 permits interchanging the zeta sum, giving

    H(z) = (1−z)^(−1/2) B(z),
    B(z) = ∏_{m≥2}(1−z/m²)^(−1/2).

On every compact subset of |z|<4 the product converges normally and has no zero, so the branch positive at zero is analytic there. The telescoping finite product ∏_{m=2}^M(1−1/m²)=(M+1)/(2M) gives B(1)=√2. For each 1<ρ<4, its coefficients have absolute bound O(ρ^(−k)). Convolving with the binomial coefficients of (1−z)^(−1/2) yields

    h_n ~ √(2/π)n^(−1/2).

For completeness, split convolution indices at n/2. On k≤n/2, the binomial ratio is bounded, and for every fixed k it tends to one; dominated convergence against the exponentially summable coefficients applies. On k>n/2, the analytic exponential tail dominates the O(√n) ratio bound. The same argument for H(z)^t=(1−z)^(−t/2)B(z)^t, for each fixed t>0, gives

    [z^n]H(z)^t ~ 2^(t/2)n^(t/2−1)/Γ(t/2).

For t<2 the binomial coefficients decay polynomially, while for t≥2 they grow polynomially; the exponentially decaying convolution tail dominates either case. Including the finitely many small indices gives c_1(n+1)^(−1/2)≤h_n≤c_2(n+1)^(−1/2). Hence

    h_(n−R)/h_n ≤ C√((n+1)/(n−R+1)),  0≤R≤n.

If R≤r_n=o(n), both indices in the asymptotic are uniformly large and (n−R)/n→1 uniformly. Thus the ratio tends uniformly to one in exactly the required range. Fixed-R convergence alone would not be enough for the theorem; the manuscript supplies the stronger statement.

## 4. Unmarked Poisson process and moments

For every fixed 0<a<b<∞,

    Σ_(aq≤j≤bq) a_j → (1/2)log(b/a).

This follows from the harmonic sum and the exponentially decaying ζ(2j)−1 correction. A joint factorial moment of fixed orders r_1,...,r_d selects at most r=Σr_l components, each of size at most b_max q. Thus their total size is at most r b_max q=o(n), even along arbitrarily slow or oscillatory intermediate sequences. In the exact selected-component formula, the ratio h_(n−R)/h_n is uniformly 1+o(1). The remaining positive sums factor by disjoint windows and tend to ∏_l[(1/2)log(b_l/a_l)]^(r_l).

The implied ordinary mixed moments converge by the finite Stirling-number conversion. The first moments give tightness of each finite count vector. Higher moments give uniform integrability along subsequences, so each subsequential limit has the displayed mixed moments. Its total count has all moments of Poisson(Σλ_l); this univariate law is moment determinate and has every exponential moment. Consequently the vector has a moment generating function in a neighborhood of zero and is uniquely the independent Poisson vector with these moments. This fills the standard joint-moment justification in the manuscript; no unsupported interchange of an infinite probability-generating series is needed.

For each compact interval the expected count is uniformly bounded. An exhaustion by compact intervals gives tightness of the random Radon counting measures; the count limits on disjoint continuity intervals identify the limiting locally finite Poisson point process. Hence Σ_iδ_(j_i/q)⇒PPP(dx/(2x)) vaguely on (0,∞).

The ABT00 theorem is a valid independent prior route. For Z_j~Poisson(a_j), a_j≤A/j with A=ζ(2)/2. Directly,

    |jP(Z_j=1)−1/2| ≤ C/j,
    jP(Z_j=l) ≤ j^(−1) A^l/l!,  l≥2.

Choose e(j)=1/j and enlarge c_1 if needed; c_l=A^l/l! for l≥2 satisfy Σ l c_l<∞. This verifies ABT's uniform logarithmic condition with θ=1/2, and even its commonly used stronger summability. Theorem 3.1 assumes b_n/n→0 and gives total-variation convergence of the whole count vector up to b_n to its independent Poisson counterpart. It therefore covers the unmarked windows here at every rate q→∞, q=o(n). It does not by itself provide the geometric Gamma/Dirichlet marking or its moment transfer.

## 5. All-rate Gamma smoothing

Conditionally on the composition take independent Y_i~Gamma(2j_i,1). Let f be a globally Lipschitz compactly supported nonnegative test, supported in [a,b]⊂(0,∞). The exact first selected-component identity bounds the expected absolute difference between the marked and unmarked integrals by

    Σ_(j=1)^n a_j(h_(n−j)/h_n) E|f(Y_j/(2q))−f(j/q)|.

For aq/2≤j≤2bq, the coefficient ratio is uniformly bounded for large n and E|Y_j−2j|≤√(2j). The contribution is bounded by

    (C/q) Σ_(aq/2≤j≤2bq) j^(−1/2) = O(q^(−1/2)).

For j<aq/2, f(j/q)=0. The Gamma moment generating function at 1/2 gives

    P(Y_j≥2aq) ≤ e^(−aq)2^(2j) ≤ e^(−a(1−log2)q).

The coefficient ratio remains bounded and Σ_(j≤aq/2)a_j=O(log(q+2)), so this entire range tends to zero. Crucially, its prefactor depends on q, not on log n.

For j>2bq, use the moment generating function at −1/2:

    P(Y_j≤2bq) ≤ e^(bq)(3/2)^(−2j) ≤ e^(−c j),
    c=2log(3/2)−1/2>0.

Up to n/2 the coefficient ratio is bounded, producing an exponentially decaying tail in q. Above n/2 the ratio is at most C√n and the sum is O(√n e^(−cn/2)), also negligible. These estimates require only q→∞ and q/n→0. No union bound over K is taken and no hidden q≫loglog n condition appears.

Since |e^(−x)−e^(−y)|≤|x−y| for x,y≥0, the marked and unmarked Laplace functionals agree asymptotically on these tests. Compactly supported nonnegative Lipschitz tests form a convergence-determining class for locally finite random measures. Thus Z_n=Σ_iδ_(Y_i/(2q)) has the same Poisson limit.

The sum T=ΣY_i has Gamma(2n,1) distribution conditionally on every composition, because the shapes add to 2n. In particular, T/(2n)→1 in probability. The pair (Z_n,2n/T) converges to (Z,1), as the second coordinate has a deterministic limit; independence is unnecessary. The dilation map (μ,c)↦Σ_x μ({x})δ_(cx) is continuous for c>0 in the vague topology. This proves the normalized model process limit because X_i/s=(Y_i/(2q))(2n/T).

## 6. All fixed compact-window moments

For M_n=Σ_i1{Y_i/(2q)∈[a,b]}, put p_j=P(Gamma(2j,1)/(2q)∈[a,b]). The three ranges above, with the middle range bounded trivially by one, give Σ_j a_jp_j≤C_(a,b). Independent marking is valid here before normalization. The selected-component identity then gives

    E(M_n)_r = Σ_(j_1+...+j_r≤n) [h_(n−Σj_i)/h_n] ∏_i a_(j_i)p_(j_i).

For Σj_i≤n/2, the ratio is bounded and the sum is at most C C_(a,b)^r. In the complementary range, one j_i≥n/(2r). Since q/n→0, eventually this index exceeds 2bq; its marking probability is at most exp(−c n/(2r)). The ratio is bounded by C√n, and the other sums are at most O(log n). A factor polynomial in √n and log n is therefore dominated by exp(−c n/(2r)). This proves a uniform bound on each fixed factorial moment and hence on each fixed ordinary moment. Replacing a window by its containing compact interval handles finite unions.

On E={1/2≤T/(2n)≤2}, the normalized [a,b] count is at most the unnormalized [a/2,2b] count. Gamma Chernoff estimates give P(E^c)≤2e^(−c_0 n): for example the lower threshold uses E e^(−T)=2^(−2n), and the upper threshold uses E e^(T/2)=2^(2n). Since K≤n, the r-th moment contribution on E^c is at most 2n^r e^(−c_0 n). Thus every fixed normalized compact-window count moment is bounded uniformly. Applying this bound at a strictly higher order gives uniform integrability of each desired moment. Count convergence at intervals with fixed endpoints follows because the limiting intensity has no atoms. Mixed powers are bounded by a power of the total count on the union. This proves all the stated joint moment limits.

## 7. Geometric transfer and exceptional events

The DL one-vertex monomial expansion has powers x_i^(2j_i−1), Σj_i=n. Summing all heights supplies ζ(2j_i). Simplex integration supplies ∏(2j_i−1)!/(2n−1)!. The weighted-graph mixture uses weighted-graph automorphisms; orbit–stabilizer converts its sum over height-vector orbits to the sum over all ordered height vectors divided by the unweighted graph automorphism factor 2^k k!. Loop flips act trivially on heights, and the k! accounts for loop permutations. This gives latent weights proportional to

    (D_(g,k)/k!) ctilde_(g,k)(j) ∏_i a_(j_i),
    D_(g,k)=A_(g,k)/2^k.

The monomial's normalized area law is exactly Dirichlet(2j_1,...,2j_k), with total shape 2n=6g−6. This is an exact mixture calculation, not a Gamma approximation applied separately to correlated normalized areas.

For k_g=floor((3/5)log(2n)), the published DL uniform coefficient estimate applies at genus g−k and logarithmically many marks, uniformly over all degree allocations. The explicitly canceled successive ratio is

    D_(g,k+1)/D_(g,k)
      =12(g−k)(3g−3−k)/[(6g−5−2k)(6g−6−2k)].

Its logarithm is O((k+1)/g), so D_(g,k)/D_(g,1)=1+O((log g)^2/g) throughout the cutoff. Normalizing positive latent weights preserves a uniform 1+o(1) density ratio, including after applying the common Dirichlet kernel. This is stronger than a pointwise asymptotic for each fixed composition.

DGZZ Theorem 1.12 at t=11/10<8/7 gives E t^K=O(n^(1/20)). Consequently

    P(K>k_g)=O(n^(−η)),
    η=(3/5)log(11/10)−1/20>1/220.

The same one-point generating bound gives every E K^r=O((log n)^r): split the tail at Llog n with L>(1/20)/log(11/10), then sum the exponential Chernoff tail. The model has the identical bounds by the coefficient asymptotic of H^t/H.

DGZZ Theorem 5.2 bounds the multivertex excess at k≤log g/log(9/4) by O((log g)^25 g^(−1)2^k). The chosen coefficient 3/5 lies below 1/log(9/4), and 1−(3/5)log2>0. Thus the multivertex probability within the cutoff is polynomially small after absorbing logarithms. Together these yield polynomially small bad events in both models and total variation convergence after forgetting latent variables.

For a count monomial of total degree r, f≤K^r. Cauchy–Schwarz gives

    E[f;bad] ≤ (E K^(2r))^(1/2) P(bad)^(1/2)=o(1).

On the good events the uniform density comparison multiplies any nonnegative expectation by 1+o(1), independently of the statistic. The normalized model moment is bounded by section 6. Replacing conditional by unconditional model moments changes them by o(1) using the same bad-event bound. This proves geometric moment convergence. Total variation alone would be insufficient, and the manuscript does not rely on it alone.

## 8. Sampling order and boundary scope

For each fixed sufficiently large g, b_max s_g<1. Positive-dimensional simplex components have no atoms at interval endpoints; the one-cylinder atom at area one lies outside the windows. There are at most 3g−3 cylinders at fixed g. Hence the fixed-genus N→∞ convergence transfers the finite counts and all their fixed moments before g is sent to infinity. No rate uniform in g and N is used.

The endpoint assumptions are substantive. At q fixed, the Gamma marking smooths a fixed discrete size spectrum rather than concentrating its points; at s fixed, conditioning and the unit-total-area constraint remain macroscopic. Neither endpoint conclusion is inferred. The theorem makes no relative-error claim about arbitrarily rare events, no uniform assertion as a→0 or b→∞, and no moment assertion with order growing with g.

## 9. Primary theorem read-depth record

All primary PDF byte lengths and hashes matched `PRIMARY_INPUTS.json` before extraction. Text extractions were local private reading aids and were removed after reading; only their finite metadata is retained. The finite source pin records are in `PRIMARY_CACHE_PINCHECKS.json`.

- [Arratia–Tavaré 1994, Lemma 5/(126)](https://www.columbia.edu/cu/simontavare/STpapers-pdf/AT94.pdf): statement and its exponent-shift proof were read; the pinchecked author facsimile was used for clean text. The manuscript's positive-weight identity is exactly its conditional-Poisson algebra.
- [Arratia–Barbour–Tavaré 2000, (1.11)–(1.12), Theorem 3.1 and proof](https://www.columbia.edu/cu/simontavare/STpapers-pdf/ABT00.pdf): ULC requires a decreasing e(i)→0 and Σl c_l<∞; Theorem 3.1 needs b_n/n→0. These hypotheses hold explicitly as in section 4. The theorem was also opened through the primary author's web PDF.
- [DGZZ published version, (1.7)–(1.8), Lemma 3.6, Theorems 1.7, 1.12, 5.2](https://webusers.imj-prg.fr/~anton.zorich/Papers/Large_Genus_Asymptotic_Geometry_2022_Inventiones_published.pdf): exact permutation weight and factorial convention, cylinder-count correspondence, t-disk 8/7, and low-k range/error read. The proof uses the stated low-k result only; it does not extend it to all k.
- [DL published version, Theorem 1.4, Theorem 3.2, (6.1)–(6.3), Lemma 6.4 and proof, Lemma 6.7](https://ems.press/content/serial-article-files/51451?nt=1): fixed-genus surface law, graph-mixture structure, uniform coefficient statement, monomial powers/prefactor, and analytic zeta correction checked. Aggarwal's substantial intersection-number asymptotics are accepted via this explicit cited input rather than independently reproved.

Assessment: the final manuscript's probability/assembly mechanism is sound under the identified published geometric inputs. No mandatory repair was found within this audit family. The exact controls and boundary counterexamples are supporting checks, and do not turn imported geometric results or literature-priority uncertainty into independently established facts.
