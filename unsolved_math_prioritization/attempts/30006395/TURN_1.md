# Turn 1: exact Cayley-forest second moment and a high-mean-degree regime

**Partial result; original transition remains unresolved.** Author turn 1, 2026-10-01. This concerns the **unknown uniform labelled-tree mixture**, not a typical template revealed to the detector. Classical Cayley/Prüfer enumeration, likelihood ratios, and the second-moment method are credited; no novelty claim is made. Separate review is still required.

## 1. Experiment and conclusions

Let P=P_(n,c) be G(n,p), p=c/n, and let Q=Q_(n,k,c) be obtained by selecting a uniform k-subset S, selecting a uniform labelled Cayley tree on S, forcing its k−1 edges, and including every other edge independently with probability p. A test sees G and the parameters, but not S or the tree. Assume 2≤k≤n and 0<p<1. Write L=dQ/dP and (x)_v=x(x−1)...(x−v+1).

We establish:

1. An exact finite-n forest expansion for E_P L², equation (6) below.
2. If 2k≤n, a uniform upper bound E_P L²≤exp(S_(n,k,c)), equations (10)–(11).
3. For every fixed c>e (Euler's number), TV(P,Q)→0 when k=o(sqrt(n)), and strong detection is impossible when k=O(sqrt(n)). The elementary edge-count test gives strong detection when k=omega(sqrt(n)). Thus this fixed-c regime has the full square-root strong-detection scale.
4. At c=e, TV(P,Q)→0 for k=o(n^(4/9)), and strong detection is impossible for k=O(n^(4/9)). This is a lower bound only, not an asserted critical detection threshold.
5. A uniform second-moment bound near c=e is given in Section 6. It does not supply a matching test or establish that e is the true transition location.

The unresolved original question includes the intervening mean-degree regime, the optimal low-c unknown-tree scale, the true location/form of the transition, and any sharp critical window. A divergent second moment below e would not prove detectability. Nor do mixture lower bounds establish the source's stronger, revealed-template impossibility statement.

## 2. Likelihood and classical forest containment

Let Z_k(G) count pairs (S,T) where |S|=k and T is a spanning tree on S whose edges occur in G; extra edges are allowed. Cayley's formula gives

    L(G)=Z_k(G)/[binom(n,k) k^(k−2) p^(k−1)].       (1)

Indeed, conditioning on a planted pair contributes p^(−k+1) times its edge-presence indicator, and averaging proves (1). This is the standard fixed-template copy-count likelihood principle (Massoulié–Stephan–Towsley, Lemma 5), averaged over Cayley shapes; it is not a new likelihood-ratio method.

For a fixed forest F with v nonisolated vertices, r nontrivial components of sizes s_1,...,s_r≥2, and m=v−r edges, a uniform Cayley tree on a fixed k-set containing F has containment probability

    k^(−m) product_j s_j.                           (2)

Here k−v isolated vertices are also forest components, contributing factors 1. For completeness, contract all components. Choosing connecting edges of a component tree weights an edge ij by s_i s_j. The Prüfer-code identity

    sum_(component trees) product_i s_i^(degree_i)
        =(product_i s_i)(sum_i s_i)^(q−2)

counts all tree extensions, with q=k−m components. Dividing the extension count k^(k−m−2) product_i s_i by k^(k−2) yields (2). When q=1, the forest itself is already a spanning tree and the same probability follows directly.

For the uniformly embedded random planted tree, the probability that its k-set contains the support of F is (k)_v/(n)_v. Therefore

    Pr(F⊆planted tree)=[(k)_v/(n)_v] k^(−m) product_j s_j.  (3)

This is a containment calculation, not a probability of F being an induced subgraph or an isolated component.

## 3. Exact second moment

Take independent planted trees T,T' with their independent random k-sets. Independence of the null edges gives

    E_P L²=E_(T,T') p^(−|E(T)∩E(T')|).             (4)

Let z=p^(−1)−1≥0. Expand the product over common edges:

    E_P L²=sum_(forests F on [n]) z^|E(F)| Pr(F⊆T)². (5)

The empty forest contributes 1. Forests have no explicitly listed isolated vertices in this sum, so their support is uniquely specified by their edges.

For an ordered list s_1,...,s_r≥2 with total v≤k, the number of labelled forests of these component sizes, summed with a factor 1/r! over ordered lists, is

    (n)_v/r! product_j [s_j^(s_j−2)/s_j!].

Combining this enumeration with (3) gives the exact identity

    E_P L² = 1 + sum_(r≥1) (1/r!)
      sum_(s_1,...,s_r≥2; v=sum s_j≤k)
        [(k)_v²/(n)_v] k^(−2(v−r)) z^(v−r)
        product_j [s_j^s_j/s_j!].                 (6)

Equivalently one can sum over component multiplicities and replace 1/r! by the corresponding product of 1/m_s!. The finite checker compares both forest enumeration and direct pairs of independently embedded Cayley trees to (6).

## 4. A factorized upper bound, with finite-population corrections

Put

    t=k²/n, rho=z/n=(1−c/n)/c,
    R_(n,k)(v)=[(k)_v/k^v]² [n^v/(n)_v].          (7)

Then a summand of (6) is

    R_(n,k)(v) t^r product_j [rho^(s_j−1) s_j^s_j/s_j!]/r!. (8)

For 2k≤n and v≤k, log(1−x)≤−x and −log(1−x)≤x/(1−x) imply

    log R_(n,k)(v)
      ≤ −v(v−1)/k + v(v−1)/[2(n−v+1)]
      ≤ −v(v−1)/(2k).                              (9)

No replacement of a large falling factorial by an asymptotic equivalent has been made. In particular R≤1. Also v(v−1)≥sum_j s_j(s_j−1), so (9) can be allocated component by component. Dropping only the total-support restriction v≤k and then applying the exponential formula gives

    E_P L² ≤ exp(S_(n,k,c)),                        (10)
    S_(n,k,c)=(k²/n) sum_(s=2)^k
       rho^(s−1) [s^s/s!] exp(−s(s−1)/(2k)).        (11)

All summands are nonnegative, so enlarging the index set is legitimate. This bound is not a claim that component sizes are independent in the original overlap distribution; the interactions were bounded explicitly by (9).

Since E_P L=1, the chi-square divergence is E_P L²−1, and

    TV(P,Q)≤(1/2)sqrt(exp(S_(n,k,c))−1).            (12)

If S stays bounded, E_P L² stays bounded. Cauchy–Schwarz then gives Q(A)≤sqrt(E_P L² P(A)); hence an event with P(A)→0 cannot have Q(A)→1. This excludes strong detection even if (12) itself is not small.

## 5. Fixed c>e and the point c=e

For fixed c>e, rho≤1/c and the Gaussian factor may be discarded. Define

    A(c)=sum_(s≥2) c^(1−s) s^s/s! < infinity.       (13)

Its convergence follows immediately from Stirling's formula. The elementary factorial bound s!≥(s/e)^s also gives A(c)≤e²/(c−e). Thus

    S_(n,k,c)≤A(c) k²/n.                           (14)

Equations (12)–(14) prove TV→0 for k=o(sqrt(n)) and bounded second moment, hence no strong detection, for k=O(sqrt(n)). If k/sqrt(n) fails to diverge, the bounded-ratio subsequence already excludes a full-sequence strong-detection assertion.

Conversely, let M=binom(n,2) and m=k−1. Under P the edge count has law Bin(M,p); under Q it has law m+Bin(M−m,p), regardless of the unknown shape. Their means differ by m(1−p). Thresholding halfway between the two means and using Chebyshev gives sum of errors at most

    8 M p / [m²(1−p)] = O(n/k²)                   (15)

for fixed c. Thus k=omega(sqrt(n)) gives strong detection. This elementary count test is classical (and consistent with the broader connected-plant result of Massoulié–Stephan–Towsley); no new algorithmic claim is made.

At c=e, use the classical lower Stirling bound

    s!≥sqrt(2πs)(s/e)^s.

For s≥2, s(s−1)≥s²/2. Because x^(−1/2) exp(−x²/(4k)) decreases on (0,infinity), sum/integral comparison yields

    sum_(s=2)^k rho^(s−1) [s^s/s!] exp(−s(s−1)/(2k))
      ≤ e/sqrt(2π) integral_0^infinity x^(−1/2) exp(−x²/(4k)) dx
      = [e Gamma(1/4)/(2sqrt(π))] k^(1/4).          (16)

Consequently

    E_P L²≤exp(D k^(9/4)/n),
    D=e Gamma(1/4)/(2sqrt(π)).                      (17)

This proves the stated o(n^(4/9)) indistinguishability and O(n^(4/9)) strong-impossibility bounds. It provides no matching upper bound on detection at c=e. In particular the exponent 4/9 is a certified bound from this argument, not an established transition exponent.

## 6. Uniform near-e bounds

These optional bounds describe the present method, not a solved phase diagram.

For c>e, put eta=log(c/e)>0. Stirling and decreasing-integral comparison give

    A(c)≤[c/sqrt(2)] eta^(−1/2).                   (18)

Combined with (14), this yields indistinguishability whenever

    c k²/[n sqrt(log(c/e))] → 0,

subject to 2k≤n and c/n<1. This statement allows parameter sequences satisfying those conditions; it is explicitly separate from the original fixed-c question.

For any c>0, put eta_+=max(log(e/c),0). By

    eta_+ s ≤ s²/(8k)+2k eta_+²,

the same calculation gives

    S_(n,k,c)≤D_c k^(9/4)/n · exp(2k eta_+²),
    D_c=c Gamma(1/4)/(2^(3/4)sqrt(π)).             (19)

The finite-n factor rho≤1/c was used, so (19) remains valid for n>c and 2k≤n. Its implication is only an upper bound on chi-square divergence. For fixed c<e it gives logarithmic-scale lower bounds, not a polylogarithmic detection algorithm or a sharp critical c.

## 7. Exact remaining gap and next directions

The forest expansion and its upper bounds settle a high-c subregime of the **unrevealed mixture**, while leaving the original transition open. To complete the target one needs matching detection results below the actual boundary and a proof that any proposed boundary is sharp. A second-moment divergence does not supply either. Rare overlap configurations can dominate E_P L² even when total variation is small.

Subsequent turns should therefore challenge this obstruction directly: truncated likelihood/typical-tree conditioning, comparison with the supplied hairy-path endpoint, and exact asymptotics of the full moment rather than its factorized upper bound. These are distinct routes, not claims that the missing positive test has already been found.
