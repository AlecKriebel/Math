# Mesoscopic cylinder areas in the principal quadratic stratum

**30006020 / OWR-14298589-005. Unreviewed full candidate, author turn 1.** The source's iterated sampling limit and principal-stratum scope are essential. No novelty or priority guarantee is made.

## 1. Exact statement

For each g≥2, sample square-tiled half-translation surfaces in the principal stratum Q(1^(4g−4)) with at most N unit squares, using the source's uniform measure on isomorphism classes (equivalently its automorphism-weighted measure in the N→∞ limit). First let N→∞. Let ν_g be the resulting law of the multiset of normalized areas of the maximal horizontal cylinders, each counted once. Their areas sum to one. Vertical cylinders have the same marginal law. There is no restriction to primitive torus covers, no cylinder-height cutoff, and no counting of repeated core curves as additional cylinders.

The following statements concern ν_g as g→∞. They do not assert a uniform joint N,g limit, a theorem for every individual surface, all directions at once, or other strata.

### Theorem A: an asymptotic model for the entire area multiset

Put n=3g−3 and a_j=ζ(2j)/(2j). Define

    H(z)=exp(sum_{j≥1} a_j z^j),  h_n=[z^n]H(z).

Choose an ordered positive composition j_1+...+j_k=n with probability

    (1/(h_n k!)) product_{i=1}^k a_(j_i).           (1)

The sum is over every k≥1 and every ordered composition, so (1) is normalized by the exponential formula. Given that composition, choose independent Gamma(2j_i,1) variables Y_i and form the unordered multiset

    {Y_i/(Y_1+...+Y_k):1≤i≤k}.                     (2)

Let μ_n be its law. Then d_TV(ν_g,μ_(3g−3))→0. This is a total-variation approximation of the whole area multiset, not just fixed macroscopic coordinates.

### Theorem B: every mesoscopic scale

Let s_g>0 satisfy s_g→0 and g s_g→∞. Then under ν_g the point process

    Ξ_g = sum_cylinders δ_(area/s_g)

converges vaguely in distribution on (0,∞) to a Poisson point process of intensity dx/(2x). For disjoint intervals [a_i,b_i] with 0<a_i<b_i<∞, their counts converge jointly to independent Poisson variables with means (1/2)log(b_i/a_i). Every fixed joint moment also converges.

In particular, for the source's window,

    C_g=#{cylinders:1/√g≤area≤2/√g},
    C_g ⇒ Poisson((log 2)/2),
    E C_g→(log 2)/2,  Var(C_g)→(log 2)/2.           (3)

Thus the count is typically of constant order, not of order √g or log g. Its limiting zero-count probability is 1/√2. Formula (3) is in the iterated limit N→∞ then g→∞.

## 2. Published inputs and conventions

We use two full primary papers, with final-edition numbering:

- [DL] Delecroix–Liu, JEMS 27 (2025), 5093–5131, DOI 10.4171/JEMS/1469: Theorem 1.4 identifies the limiting cylinder-area law; Theorem 3.2 describes its stable-graph polynomial mixture; Theorem 4.1 gives concentration on one-vertex graphs with O(log g) edges; equation (6.1), Lemma 6.4 and its proof give the uniform correlator coefficients and monomial expansion.
- [DGZZ] Delecroix–Goujard–Zograf–Zorich, Inventiones 230 (2022), 123–224, DOI 10.1007/s00222-022-01123-y: Theorem 1.12 gives the uniform probability-generating asymptotic for the number K_g of cylinders; Theorem 5.2 bounds the contribution of graphs with more than one vertex relative to one-vertex graphs in the low-k range.

These substantial geometric/enumerative results are credited inputs, not proved here. We derive the mesoscopic statements and the uniform-integrability transfer explicitly below.

The parameter called m in [DL] bounds multicurve multiplicities, equivalently cylinder heights in its surface correspondence. Here m=∞. It is unrelated to primitiveness of a square-tiled covering. The relevant mixture is the principal holomorphic quadratic law: lower-dimensional holomorphic strata do not change the fixed-genus N→∞ law. The original report states this same principal-stratum law as ν_(2,1^(4g−4)).

All uses of normalized area divide by the entire surface area. The Gamma total parameter in the exact [DL] formula is 6g−6=2n. The brief OWR report prints 4g−4 in its separate microscopic summary. We do not use that microscopic scaling assertion or silently identify those two factors; the proof here uses the exact published area formula, and the requested mesoscopic window is fixed as written in the question.

## 3. From stable graphs to a uniform composition mixture

Let Γ_(g,k) be the stable graph with one vertex of genus g−k and k loops. Restrict initially to

    k≤k_g=floor((3/5)log(2n)).                     (4)

For large g this is well below g, so the vertex genus is nonnegative. The graph automorphism factor is 2^k k!. The positive monomial expansion in the proof of [DL, Lemma 6.4] is

 F_(g,k)(x)=A_(g,k) sum_{j_i≥1, sum j_i=n}
       ctilde_(g,k)(j_1,...,j_k) product_i x_i^(2j_i−1)/(2j_i)!,

    A_(g,k)=(6g−5−2k)! 2^(3k−3)/
             ((g−k)!(3g−3−k)! 3^(g−k)).           (5)

The coefficients ctilde are positive. Equation (6.1) of [DL], applied with g−k in place of g, gives

    sup_{k≤k_g, sum j_i=n}|ctilde_(g,k)(j)-1|→0.     (6)

Summing unbounded heights gives ζ(2j_i) for each monomial. The simplex integral of product x_i^(2j_i−1) is product(2j_i−1)!/(2n−1)!. Thus, after integrating and dividing by 2^k k!, the unnormalized composition masses have the form

    common_factor(g) · D_(g,k)/k!
       ·ctilde_(g,k)(j) product_i a_(j_i),          (7)

where

    D_(g,k)=A_(g,k)/2^k
           =(6g−5−2k)! 2^(2k−3)/
             ((g−k)!(3g−3−k)! 3^(g−k)).

The common factor contains (2n−1)! and the total-volume normalization and does not depend on k or j. Conditional on the selected monomial, the area vector is exactly Dirichlet(2j_1,...,2j_k), equivalently (2).

The ratio of successive prefactors is

 D_(g,k+1)/D_(g,k)
   =12(g−k)(3g−3−k)/[(6g−5−2k)(6g−6−2k)].        (8)

Uniformly for k≤k_g=O(log g), its logarithm is O((k+1)/g). Summing these logarithms proves

    sup_{k≤k_g}|D_(g,k)/D_(g,1)-1|→0.              (9)

Equations (6) and (9) show that the conditional actual law on the one-vertex, k≤k_g event and the model law conditioned on k≤k_g have uniformly asymptotic Radon–Nikodym densities on the common latent space of compositions and Dirichlet vectors. The same holds after forgetting labels and sorting areas. In particular, for every nonnegative measurable statistic f,

 E_actual[f | good] = (1+O(ε_g)) E_model[f | K≤k_g], (10)

with ε_g→0 independent of f, whenever the expectations are finite. Uniformity in f is important for shrinking windows and for moments; pointwise weak convergence of macroscopic coordinates would not suffice.

## 4. Polynomially small exceptional probabilities and moment control

Write bad for either a non-one-vertex stable graph or K_g>k_g. We record enough quantitative control to transfer unbounded count moments later.

By [DGZZ, Theorem 1.12], for fixed t=11/10<8/7,

    E[t^(K_g)] = O(n^((t−1)/2)).                   (11)

Chernoff's inequality and (4) give

 P(K_g>k_g) ≤ C n^((t−1)/2−(3/5)log t)=O(n^-η),
    η=(3/5)log(11/10)-1/20>0.                     (12)

Indeed log(11/10)>1/11, so η>1/220. Rounding k_g only changes the constant. The same generating-function bound implies E[K_g^r]=O((log n)^r) for every fixed r: sum the exponentially decreasing Chernoff tail beyond a sufficiently large multiple of log n.

In the range k≤k_g, [DGZZ, Theorem 5.2] gives the relative excess of the total k-cylinder contribution above the one-vertex contribution as

    O((log g)^25 g^-1 2^k).                        (13)

We use only this low-k range, not an unrestricted interpretation of a subsequent corollary. Since k_g∼(3/5)log g, the bound is polynomially small after absorbing logarithms. Averaging the conditional bound over k≤k_g and combining with (12) yields

    P_actual(bad)=O(n^-c) for some c>0.            (14)

All these cylinder-count inputs transfer from the multicurve count in [DGZZ] by its exact surface correspondence [DGZZ, Theorem 1.7], consistent with [DL, Theorem 1.4].

The ideal composition model has the same bounds. Indeed

    E_model[t^K]=[z^n]H(z)^t/h_n,

and the coefficient estimate in the next section gives O(n^((t−1)/2)). Thus its K>k_g probability is polynomially small and all fixed K moments are O((log n)^r).

Equations (6), (9), (12), and (14) prove Theorem A by conditioning and then forgetting the latent variables. They also imply a stronger usable statement for moments: if f is a nonnegative r-th power of a count bounded by K, then

 E_actual[f;bad]
    ≤(E_actual[K^(2r)])^(1/2) P_actual(bad)^(1/2)=o(1), (15)

and the corresponding model tail also contributes o(1). This is why total variation alone is not being mistaken for convergence of expectations.

## 5. The composition model's coefficient estimates

Write

 H(z)=(1−z)^(-1/2) B(z),
 B(z)=product_{m≥2}(1−z/m²)^(-1/2).                (16)

To verify (16), expand ζ(2j) and interchange the absolutely convergent sums for |z|<1. The function B is analytic in |z|<4, with the branch chosen positive at zero. Its value B(1)=√2 follows from product_(m≥2)(1−1/m²)=1/2. These facts also appear in [DL, Lemma 6.7].

The binomial coefficients of (1−z)^(-1/2) are asymptotic to 1/√(π n). Convolution with the exponentially decreasing coefficients of B therefore gives

    h_n~sqrt(2/π) n^-1/2.                          (17)

This can be proved directly: on coefficient indices k=o(n), the binomial-coefficient ratio tends uniformly to one; the analytic B tail is exponentially small. The same argument applied to H(z)^t=(1−z)^(-t/2)B(z)^t gives

 [z^n]H(z)^t~2^(t/2) n^(t/2−1)/Γ(t/2)

for fixed t>0, justifying the model bounds in Section 4. It also follows from (17), including finitely many small indices, that constants c_1,c_2>0 satisfy

 c_1/sqrt(n+1)≤h_n≤c_2/sqrt(n+1),
 h_(n-r)/h_n≤C sqrt((n+1)/(n-r+1)), 0≤r≤n,        (18)

and h_(n-r)/h_n→1 uniformly whenever 0≤r≤o(n).

## 6. Mesoscopic cycles before Gamma marking

Set q_n=n s_g, so q_n→∞ and q_n=o(n). Let C_j be the number of parts of size j in the composition model. Its exact factorial-moment formula is

 E[product_j (C_j)_(r_j)]
     = h_(n−sum j r_j)/h_n · product_j a_j^(r_j),  (19)

when sum j r_j≤n, and is zero otherwise. Here (x)_r denotes the falling factorial. This follows simply by removing the selected parts from the exponential assembly.

For a fixed interval [a,b]⊂(0,∞),

 sum_{a q_n≤j≤b q_n} a_j→(1/2)log(b/a),           (20)

because ζ(2j)→1 exponentially and q_n→∞. In every fixed-order joint factorial moment of counts in bounded q_n-scale windows, the total selected size is O(q_n)=o(n). The ratio in (19) tends uniformly to one. Summing (19), therefore, gives the joint factorial moments of independent Poisson variables with the means in (20). The Poisson distribution is moment-determinate; the factorial-moment argument, or its probability-generating-function version, yields the joint count laws.

Consequently sum_i δ_(j_i/q_n) converges vaguely to PPP(dx/(2x)). This concerns windows bounded away from zero and infinity; there is no claim that a mesoscopic theorem applies at the microscopic or macroscopic endpoints.

## 7. Gamma smoothing at every mesoscopic rate

Conditional on the parts, attach independent Y_i~Gamma(2j_i,1). Let Z_n=sum_i δ_(Y_i/(2q_n)). We show that marking leaves the vague limit unchanged. A naive union bound over all K≈log n parts would impose an unnecessary growth condition on q_n; we avoid it.

Take a nonnegative compactly supported Lipschitz function f, supported in [a,b]⊂(0,∞). The expected difference between its integrals against the marked and unmarked processes is bounded by

 sum_{j=1}^n a_j h_(n-j)/h_n
       E|f(Y_j/(2q_n))-f(j/q_n)|.                 (21)

For a q_n/2≤j≤2bq_n, the coefficient ratio is bounded and

    E|Y_j/(2q_n)-j/q_n|≤sqrt(2j)/(2q_n).

The contribution of this range to (21) is O(q_n^-1/2), using a_j≤C/j.

For j<a q_n/2, the unmarked term is zero, and the Gamma upper-tail Chernoff bound gives

 P(Y_j≥2a q_n)≤exp(-a q_n)2^(2j)
              ≤exp(-a(1-log 2)q_n).

Its weighted sum is at most a constant times log(q_n+2) times that exponential. For j>2bq_n, the lower-tail bound gives

 P(Y_j≤2bq_n)≤exp(bq_n)(3/2)^(-2j)≤exp(-c j)

for an absolute c>0. Up to j=n/2 the coefficient ratio is bounded. Above n/2 it is O(√n) by (18), which is overwhelmed by the exponential tail. Thus (21) tends to zero for every q_n→∞ with q_n=o(n), however slowly q_n diverges.

The Laplace functionals against nonnegative compactly supported Lipschitz tests therefore have the same limit; these tests determine vague point-process convergence. Hence Z_n⇒PPP(dx/(2x)).

The total T_n=sum_iY_i has Gamma(2n,1) law, independently of the chosen composition as far as its marginal distribution is concerned. In particular T_n/(2n)→1 in probability. Since

    X_i/s_g=(Y_i/(2q_n))·(2n/T_n),

Slutsky's theorem and continuity of positive dilation in the vague topology give the point-process part of Theorem B for the ideal normalized model. No independence between the total and the point process is needed for this step.

## 8. Uniform moment bounds for marked and normalized counts

We supply the uniform-integrability step rather than infer it from convergence in law.

Let M_n count marked Y_i/(2q_n) in a fixed compact interval [a,b]⊂(0,∞), and put

    b_(n,j)=P(Gamma(2j,1)/(2q_n)∈[a,b]).

The same three-range estimates as above give

    sum_{j=1}^n a_j b_(n,j)≤C_(a,b)               (22)

uniformly in large n, without the coefficient ratio. For every fixed r, independent marking and (19) give

 E[(M_n)_r]=sum_{j_1+...+j_r≤n}
      h_(n−sum j_i)/h_n · product_i a_(j_i)b_(n,j_i). (23)

If sum j_i≤n/2, the ratio is bounded, so this part is at most C C_(a,b)^r. If sum j_i>n/2, one selected j_i≥n/(2r). Because q_n=o(n), its lower Gamma-tail probability is at most exp(-c_r n) for all sufficiently large n. The ratio is at most O(√n), the remaining sums of a_j are O(log n), and the exponentially small bound dominates these factors. This proves a uniform bound for every fixed factorial moment, and hence every ordinary moment, of M_n. The same proof works for a finite union of compact intervals.

On the event 1/2≤T_n/(2n)≤2, a normalized count in [a,b] is bounded by the unnormalized marked count in [a/2,2b]. The complementary event has exponentially small probability in n by the Gamma Chernoff bound. Since K≤n, its contribution to any fixed count moment is at most n^r exp(-c n)=o(1). Thus every fixed moment of every compact-window normalized count is uniformly bounded.

Weak count convergence to the Poisson limit, together with a uniform bound on a higher moment, now implies convergence of each fixed moment in the ideal model. In particular its first and second moments converge to those of the claimed Poisson law. This also proves joint moment convergence for finitely many disjoint intervals by bounding their mixed powers by a power of the total count on their union.

## 9. Transfer to the geometric law

For bounded point-process observables, Theorem A transfers the ideal distributional limit directly, even though s_g depends on g: total variation controls every measurable observation at each genus.

For a fixed count moment, split according to good and bad. The bad part is o(1) by (15). On the good part, the uniform density comparison (10) applies to the nonnegative moment statistic. Its ideal conditional expectation stays bounded by Section 8 and differs by o(1) from its unconditional expectation, since the ideal K-tail contribution vanishes as in Section 4. Therefore the actual moment converges to the same limit. This proves all assertions of Theorem B, including (3), with no hidden interchange of the limits N and g.

For each fixed large g, the endpoints of the requested area windows have no atoms under ν_g: the conditional laws with at least two cylinders have simplex densities, and the one-cylinder atom is at area one, outside these windows for large g. Hence the fixed-genus N→∞ convergence also applies to the window counts. Taking g→∞ afterward is exactly the source's sampling order.

## 10. Interpretation and exclusions

Theorem A supplies an explicit full-area-multiset asymptotic model in total variation. Theorem B fills the mesoscopic gap between areas comparable to 1/g and areas comparable to one, and provides the requested count law and mean. The macroscopic Poisson–Dirichlet law and the microscopic law cited in the source remain credited prior results, not new claims here.

No assertion is made for arbitrary strata, quartic differentials, primitive-cover ensembles, all directional cylinders on one surface, a diagonal N(g) sampling scheme, or scales with g s_g bounded or s_g bounded away from zero under the mesoscopic theorem. The full-multiset model remains a distributional approximation for the stated iterated principal-stratum ensemble. Any broader scope needs separate work.

### Primary references

[OWR] V. Delecroix, “What we do not know (yet) about square-tiled surfaces in large genus?”, Oberwolfach Report 41/2024, pp.2384–2387, Problem 2 p.2387. https://doi.org/10.4171/owr/2024/41

[DL] V. Delecroix, M. Liu, “Length partition of random multicurves on large genus hyperbolic surfaces,” J. Eur. Math. Soc. 27 (2025), 5093–5131. https://doi.org/10.4171/JEMS/1469 . Full publisher PDF: https://ems.press/content/serial-article-files/51451?nt=1

[DGZZ] V. Delecroix, É. Goujard, P. Zograf, A. Zorich, “Large genus asymptotic geometry of random square-tiled surfaces and of random multicurves,” Invent. Math. 230 (2022), 123–224. https://doi.org/10.1007/s00222-022-01123-y . Full publisher-version author-hosted PDF: https://webusers.imj-prg.fr/~anton.zorich/Papers/Large_Genus_Asymptotic_Geometry_2022_Inventiones_published.pdf
