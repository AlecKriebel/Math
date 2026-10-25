# Early independent analytic reconstruction of23387774

This note is fixed after complete actual seven-page PDF and sole deposited TeX reading, including visual inspection of every reader page, but before external primary-body reading, historical/package records, sibling/current-root opinions or source-lane conclusions. No deposited program was executed. The manuscript's own historical narrative and references were naturally read; they are not independent evidence for attribution or the exact hypotheses of imported theorems.

## Exact target, ensemble and boundaries

Fix genus g≥2, principal holomorphic quadratic stratum Q(1^(4g−4)), isomorphism classes of square-tiled half-translation surfaces with at most N unit squares, and one count per maximal horizontal cylinder. The areas X_i are divided by total area, so their sum is one. The stipulated law ν_g is the fixed-genus N→∞ limit, with all positive integer cylinder heights allowed (m=∞). Only afterward does g→∞. The asserted equality of unweighted and automorphism-weighted fixed-genus limits is a primary interface requiring verification.

For every deterministic s_g>0 with s_g→0 and g s_g→∞, the target is convergence of Σδ_(X_i/s_g), as a locally finite point process on (0,∞) with its vague topology, to PPP(dx/(2x)). Every finite family of disjoint compact intervals away from zero must have independent Poisson limiting counts and all fixed joint ordinary moments must converge. For [g^(−1/2),2g^(−1/2)] the mean/variance limit is (log2)/2 and zero-count probability tends to 2^(−1/2).

This is neither a diagonal N(g) statement nor an arbitrary-stratum/direction assertion, nor the microscopic boundary g s_g=O(1), nor macroscopic s_g≈1. The vertical marginal follows by exchanging the square directions, but simultaneous horizontal/vertical independence is not claimed. Intensity dx/(2x) has infinite total mass near zero and infinity but finite mass on every compact subset of (0,∞), consistent with vague convergence of finite configurations whose total count grows.

## Independent probability mechanism

### 1. Assembly normalization and factorial extraction

Let n=3g−3, a_j=ζ(2j)/(2j)>0 and H(z)=exp(Σ_(j≥1)a_jz^j), h_n=[z^n]H. A positive ordered composition (j₁,…,j_k) of n has weight (h_n k!)⁻¹∏a_(j_i). For a count vector (c_j) with Σj c_j=n and k=Σc_j, exactly k!/∏c_j! distinct ordered sequences have those multiplicities. Their combined probability is h_n⁻¹∏a_j^(c_j)/c_j!, whose sum is one by the exponential generating product. This is exactly the independent Poisson(a_j) count vector conditioned on total size n; the conditioning probability is e^(−Σ_(j≤n)a_j)h_n>0.

Removing a fixed selection of r_j distinct components of each size cancels the corresponding factorials. Thus, for R=Σj r_j≤n,

    E∏(C_j)_(r_j) = (h_(n−R)/h_n)∏a_j^(r_j),

and the moment is zero when R>n. This follows algebraically; it does not require a Poisson approximation theorem or a new assembly theorem.

Expanding ζ(2j)=Σ_(m≥1)m^(−2j) yields H=(1−z)^(−1/2)B(z), where B=∏_(m≥2)(1−z/m²)^(−1/2) is analytic and nonzero in |z|<4. The finite product ∏_(m=2)^M(1−m⁻²)=(M+1)/(2M) shows B(1)=√2. Convolution of exponentially decreasing B coefficients with central-binomial coefficients gives

    h_n∼√(2/π)n^(−1/2),
    c₁(n+1)^(−1/2)≤h_n≤c₂(n+1)^(−1/2).

Consequently h_(n−R)/h_n≤C√((n+1)/(n−R+1)). If R≤R_n=o(n), the ratio tends uniformly to one: both indices tend uniformly to infinity and √(n/(n−R))→1. The identical argument with B^t and (1−z)^(−t/2), for each fixed t>0, gives [z^n]H^t∼2^(t/2)n^(t/2−1)/Γ(t/2). This proves E t^K=O(n^((t−1)/2)) in the model. No uniformity in t is needed.

### 2. Unmarked intermediate process

Put q=n s_g. The hypotheses are exactly q→∞ and q=o(n). For each fixed 0<a<b<∞,

    Σ_(a q≤j≤b q)a_j→(1/2)log(b/a),

because ζ(2j)−1 decreases exponentially once j→∞, and the harmonic Riemann sum tends to log(b/a). In any fixed joint factorial moment of window counts, the total selected size R is at most a fixed multiple of q, hence o(n). The exact factorial identity and uniform coefficient ratio therefore yield the product of the limiting Poisson factorial moments. This also gives uniform bounds on all fixed count moments in those windows. The Poisson moment laws determine the finite joint distribution. Bounded expected counts on each compact interval give local tightness; approximation by finitely many interval steps then gives the unmarked point-process limit. The paper's separate ABT citation is an antecedent, not a deductive necessity for this explicit argument.

### 3. Gamma marks at arbitrarily slow q→∞

Given the composition, mark its components independently by Y_i∼Gamma(2j_i,rate1), and first consider Z_n=Σδ_(Y_i/(2q)). For a nonnegative compactly supported Lipschitz f, supported in [a,b]⊂(0,∞), compare Z_n f to Σf(j_i/q) on the same composition and marks. Linearity of expected sums gives

    E|difference| ≤ Σ_(j=1)^n a_j(h_(n−j)/h_n)
                        E|f(Y_j/(2q))−f(j/q)|.

This equality/inequality uses the first assembly factorial moment, rather than a maximum error over K components.

For a q/2≤j≤2b q, the coefficient ratio is bounded eventually, and E|Y_j/(2q)−j/q|≤√(2j)/(2q). Since Σ_(j≈q)1/j=O(1), the Lipschitz contribution is O(q^(−1/2)).

For j<a q/2, the unmarked test vanishes. The Gamma MGF at 1/2 gives

    P(Y_j≥2a q)≤e^(−a q)2^(2j)≤e^(−a(1−log2)q).

The weighted sum is O(log(q+2)e^(−c_aq)), tending to zero for every q→∞, even as slow as log log log n.

For j>2b q, the unmarked test again vanishes. The Laplace transform at 1/2 gives

    P(Y_j≤2b q)≤e^(b q)(3/2)^(−2j)≤e^(−c j),
    c=2log(3/2)−1/2>0.

Up to n/2, h_(n−j)/h_n is bounded, and the exponential sum tends to zero as q→∞. Above n/2 it is at most C√n, which is dominated by the exponential tail. No condition q≫log n, q≫log log n or q≫K is used. A union bound requiring every mark to track its mean would transfer an unnecessary rate restriction to the core problem; it is not the argument being validated.

Since |e^(−x)−e^(−y)|≤|x−y| for nonnegative x,y, the expected comparison transfers Laplace functionals of compactly supported Lipschitz tests. These determine the marked vague limit.

### 4. Normalization by the total Gamma variable

For every composition, Σ2j_i=2n. Thus T=ΣY_i has exactly Gamma(2n,1) distribution even after mixing, and T/(2n)→1 in probability. There is no need for independence of T and Z_n. The normalized process is the positive dilation by 2n/T:

    (Y_i/T)/s_g = (Y_i/(2q))(2n/T).

Joint convergence to (limiting process,1) follows from a deterministic-limit Slutsky argument. Positive dilation is continuous for the vague topology at any positive finite dilation: compact test supports remain in a fixed compact set and converge uniformly. Therefore the normalized model has the same point-process limit.

The exact total parameter is 2n=6g−6. A different fixed microscopic normalization cannot be silently substituted. The eventual 1/x intensity is scale invariant, but that fact alone is not a replacement for the exact geometric Gamma marking used in the proof.

### 5. Every fixed joint count moment

Let p_(n,j)=P(Y_j/(2q)∈[a,b]). The same three ranges, now without coefficient ratio, give Σa_jp_(n,j)≤C_(a,b). Independent marks on distinct selected components and the factorial extraction give

    E(M_n)_r = Σ_(j₁+…+j_r≤n)
                  (h_(n−Σj_i)/h_n)∏a_(j_i)p_(n,j_i).

Repeated sizes are allowed and are already handled by selecting distinct components via falling factorials. For Σj_i≤n/2, the ratio bound and the preceding weighted sum give a uniform constant C C_(a,b)^r. If Σj_i>n/2, some j_i≥n/(2r). Since q=o(n), that mark's probability of landing below 2bq is at most e^(−c_r n) for all sufficiently large n. The remaining sum is bounded by C√n times a fixed power of Σ_(j≤n)a_j=O(log n), hence is o(1). This includes the boundary residual h₀/h_n of order √n. Thus all fixed ordinary moments of the marked count are bounded. A finite union of compact intervals is bounded by its compact hull, so the same statement holds there.

On the event 1/2≤T/(2n)≤2, a normalized count in [a,b] is bounded by the marked count in [a/2,2b]. The complement has Gamma Chernoff probability O(e^(−c n)); the normalized count is at most K≤n, making its r-th moment contribution at most n^rO(e^(−c n)). Hence all normalized compact-window moments are uniformly bounded. A higher moment gives uniform integrability for every fixed power. Products of window-count powers are bounded by a power of the count on the finite union. The limiting Poisson process has no atoms at the fixed interval boundaries; count convergence plus this uniform integrability proves all fixed joint ordinary moments.

Total variation convergence alone would not suffice for these unbounded statistics. The paper has supplied a separate integrability argument rather than making that invalid inference.

## Conditional geometric reconstruction and exact imports to check

The probability argument above is independently complete for the stated marked assembly model. Its geometric application is conditional on the following precise published interfaces, which have not yet been read independently at this early stage.

1. **Fixed-genus geometric law and height/area convention.** DL Theorems1.4/3.2 must concern exactly the unbounded-height m=∞ square-tiled principal quadratic law, including the isomorphism-class/automorphism-weighted correspondence, normalized horizontal cylinder areas, and finite count bound K≤3g−3. The full positive graph mixture, not just convergence of a ranked leading component, is needed.

2. **Uniform one-vertex coefficient.** DL Lemma6.4 and Eq6.1, at vertex genus g−k and 2k markings, must give positive monomials x_i^(2j_i−1)/(2j_i)! with Σj_i=n and a relative coefficient 1+o(1), uniformly over all such compositions and all k≤k_g=floor((3/5)log(2n)). It is particularly necessary to inspect the actual numerical/quantified range for the number of marked points; O(log g) should not be substituted for a smaller explicit allowed range.

3. **Prefactor and common kernel.** With the graph automorphism factor 2^k k!, the claimed A_(g,k) is

       (6g−5−2k)! 2^(3k−3) /
       ((g−k)!(3g−3−k)!3^(g−k)).

   Changing width w_i to area x_i=h_iw_i multiplies the monomial measure by h_i^(−2j_i). Summing integer heights supplies ζ(2j_i). The simplex integral supplies ∏Γ(2j_i)/Γ(2n), so (2j_i)! cancels to 1/(2j_i), yielding exactly a_(j_i). Conditional area law is Dirichlet(2j₁,…,2j_k). The prefactor D=A/2^k has ratio

       D_(g,k+1)/D_(g,k)
        =12(g−k)(3g−3−k)/((6g−5−2k)(6g−6−2k)).

   This follows by direct factorial cancellation. For k=O(log g), numerator/denominator differ by O(g(k+1)+k²), while the denominator is Θ(g²). Thus log ratio=O((k+1)/g), and D_(g,k)/D_(g,1)=1+O((log g)²/g). Any missing graph labeling factor depending exponentially on k would change the assembly parameter, so this exact interface cannot be treated as cosmetic.

4. **Quantified good-event and total-count control.** DGZZ Theorems1.7/1.12 must apply to this precise surface law at fixed t=11/10<8/7 and give E t^K=O(n^((t−1)/2)). Markov then gives P(K>k_g)=O(n^(−η)), with η=(3/5)log(11/10)−1/20>1/220: the inequality log(11/10)>1/11 proves the stated lower bound. Summing the exponential Markov tail after a sufficiently large multiple of log n gives E K^r=O((log n)^r) for every fixed r. This does not follow from unquantified K/log n concentration alone.

5. **Multivertex suppression at the used cutoff.** DGZZ Theorem5.2 must give the claimed relative bound O((log g)^25 g^(−1)2^k) in its actual stated low-k range. Here k_g≈0.6log g lies below log g/log(9/4)≈1.233log g, and 2^(k_g)=O(g^((3/5)log2)), whose exponent is less than one. The low-k multivertex error is polynomially small. Adding the upper-tail estimate yields a polynomial good-event failure bound. No extension of Theorem5.2 beyond its stated range is needed.

Given these verified interfaces, the geometric law conditioned on one vertex and K≤k_g has latent composition weights within a uniform factor 1+o(1) of the model conditioned on K≤k_g, and exactly the same conditional Dirichlet kernel. Normalizing positive weights preserves a uniform relative-density bound. Forgetting the latent variables gives total variation o(1). This is a whole-multiset comparison, not relative accuracy on arbitrarily rare events.

For any fixed moment statistic F_g bounded above by K^r, the bad contribution in either law satisfies

    E[K^r;bad]≤(E K^(2r))^(1/2)P(bad)^(1/2)=o(1).

On the good events the uniform density-ratio estimate applies to every nonnegative measurable F_g, including a genus-dependent scale, and its model expectation is bounded by the marked compact-window moment argument. Thus the relative o(1) error is multiplied by O(1), not by a possibly growing power of log n. Removing the model cutoff costs o(1) again. This completes geometric moment transfer once the cited interfaces are verified.

At each fixed sufficiently large g, window endpoints s_g a,s_g b lie below1. Graph-mixture components with at least two cylinders must have continuous simplex marginals, whereas the one-cylinder atom is at1. Hence the fixed-N limiting law gives count convergence on these windows by its null boundaries. K≤3g−3 makes all count moments bounded at that fixed genus. N→∞ may therefore be taken first, and only afterward the proved g-limit. No uniform N-versus-g estimate or diagonal sampling has been smuggled in.

## Early status and falsification plan

The self-contained probability chain has no central gap identified: it handles all q→∞, q=o(n), full Gamma normalization and every fixed joint moment, and it correctly separates total variation from unbounded-moment transfer. The geometric claim remains provisional until exact published positive-mixture, coefficient-range, prefactor and surface-moment interfaces are inspected. Those substantial geometric results are imports, not re-proved by finite tests.

Useful diagnostics would independently enumerate small positive assemblies with generic rational weights, verify selected-component identities and marked factorial moments against a separate enumeration, check the exact D ratio and cutoff exponent inequalities, and inspect meaningful tail bounds. They must not be promoted to all-genus geometry or arbitrary-rate convergence proofs. Primary announcement bodies and original problem wording must also be read after this seal; a microscopic fixed-window theorem and the tail of a limiting density do not alone supply a growing-window estimate. No priority or publication conclusion is yet made.

Completion estimate: **40% of the bounded independent analytic review**, measuring completed work rather than probability of correctness. External primary bodies and sibling/current-root opinions remain unread.
