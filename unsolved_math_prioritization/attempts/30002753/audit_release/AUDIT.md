# Independent adversarial audit: 30002753 / OWR-13359-003

Date: 5 October 2026. Rank: 726. Original disposition: **unsolved, 5/5 approaches**.

## Verdict and controlling qualification

**PASS for the retained exact mathematical claims, with one non-blocking exploratory-precision qualification.** No correction to the exact proofs was found. This is not a solution of the requested asymptotic-order problem, a certification of a global optimizer, a novelty claim, or a claim of current global openness.

The saved floating-point n=3 optimizer candidate does **not** reproduce its displayed value to absolute tolerance 10^-9. Independent evaluation of its saved density and potential gives approximately **0.8816783124866347**, whereas the packet reports **0.8816783052209357**. The absolute difference is approximately **7.2657 × 10^-9**. The corresponding n=4 discrepancy is approximately **9.4606 × 10^-12**. Both retained numerical values are exploratory. They must not be represented as precision-certified bounds or global optima. Six-decimal reporting avoids suggesting the unsupported displayed precision.

The proof of **κ_3 < 9/10** uses a different, exactly specified rational density and integer potential. Its certificate was independently verified with exact arithmetic and rational bounds for log 2. It has no dependence on either optimizer value. The original frozen packet has been preserved byte-for-byte; this audit addendum controls interpretation of its exploratory digits.

## 1. Binding and independence

The audit is bound to exactly these original bytes:

- Original `MANIFEST.json`: SHA-256 `dbc674b5e74de6e98a077b3eb5fd6a5b38e6566a89c6b629f54d7d8c0db9b31e`.
- Original `transpositions_30002753_safe.tar.gz`: 18,329 bytes; SHA-256 `051c82bb55cc5cd3a967b128db8c560065000ec5db81753cdb78016ef2e3755c`.
- All ten original safe files match their manifest or the supplied manifest anchor. The archive has exactly those ten regular-file members, without symbolic links, hard links, duplicate paths, or unexpected entries, and each member equals the corresponding directory file byte-for-byte.

The author checker was replayed from `/tmp` without modifying it. It reports 113 arithmetic assertions and 872 distinct permutation states. Its arithmetic count intentionally precedes its additional manifest checks; the audit does not confuse these counts. The recorded author arithmetic output agrees with the replay after excluding the extra replay-only manifest-status field.

Independently written controls do not import or call either author script. The finite checker constructs the graph by pairwise Hamming distance two, rather than composing label transpositions, and evaluates the ordered-edge formulas with their 1/4 and 1/2 factors. It passes **187 exact assertions**, including **nine mathematical negative controls**, over the 872 states of S_2 through S_6. Supplemental symbolic work passes **19 identities/limits**. The symbolic checker uses SymPy 1.14.0; the finite checker and binding checker use only the Python standard library.

The audit was performed without additional auditors and without remote writes. Its safe release contains authored analysis, audit code/results, and public verification metadata only. Public-source PDFs and private visual renders remain outside the release. No raw problem records, source-text extracts, dataset contents, or private coordination files have been added.

## 2. Source identity and scope

The [OWR publisher report](https://ems.press/content/serial-article-files/46544), printed pages 3227–3229, identifies an entropy-geodesic-convexity question and asks for asymptotic order after giving the two established bounds. Page 3229 was independently rendered and visually inspected. The exact UnsolvedMath website statement was not independently read; the frozen packet's access limitation and catalog-to-primary-source qualification remain in force.

The [published Erbar–Maas–Tetali article](https://numdam.org/item/10.5802/afst.1464.pdf) supplies the precise Markov rates, logarithmic-mean metric, Hessian criterion (Theorem 2.2), established lower bound, and local obstruction (Lemma 5.2). The relevant definitions and Section 5 were independently inspected; printed page 798, including the local test's diagram, was visually checked.

The [published Fathi–Maas article](https://www.janmaas.org/wp-content/uploads/2016/06/2016-FM-AAP.pdf) uses Theorem **4.9** in Section 4.4. The [earlier arXiv version](https://arxiv.org/pdf/1501.00562v1) uses **4.8**. Both relevant statements use the required normalization and the existing lower bound; no theorem-number confusion remains.

All eight available public PDFs match the original public-source byte counts and SHA-256 metadata. This is a file-integrity check, not a claim to have independently reread every later paper. The independent content audit focused on the primary sources above. It did not repeat an exhaustive literature or repository-history census. No raw AI-solution or AI-progress corpus was inspected. Absence of such inspection cannot support an absence-of-prior-solutions claim.

## 3. Model, forms, and domain checks

Fix n ≥ 2, d = n(n−1)/2, q = 1/d, and μ = 1/n!. Each state has exactly d transposition neighbors. Thus the generator's total nonidentity jump rate is one. The graph is connected, its rate matrix is symmetric, and μ is reversible.

For positive a,b, the mean is θ(a,b) = (a−b)/(log a−log b), extended by θ(a,a)=a. Put z = log(a/b). Independent differentiation yields

θ_1 = 1/z − (a−b)/(a z²),

θ_2 = −1/z + (a−b)/(b z²).

Both derivatives extend to 1/2 on the diagonal. Euler's identity aθ_1+bθ_2=θ holds. In particular the formulas are not evaluated as a literal 0/0 at equal densities. The integral representation of θ proves strict positivity for positive inputs.

In ordered-edge form, A has factor 1/2 and the density part of B has factor 1/4. Passing to unordered edges doubles each symmetric summand and gives exactly the factors in the original proof. The gradient term has its stated minus sign. These factor and sign checks were tested against deliberate mutations.

For positive densities and nonconstant potentials, connectedness gives A>0. Multiplying a density by c>0 scales both A and B by c; positive unnormalized test densities therefore legitimately give the same quotient after normalization. Multiplying all rates by c scales A by c and B by c², hence the curvature quotient by c. Identity moves contribute zero to the generator. This verifies the lazy-chain and independently sampled-label conversions, and rules out an unnormalized-time substitution. No finite Rayleigh quotient is assigned to the singleton n=1 case.

The inference from the Hessian inequality to entropy-geodesic convexity uses the established theorem in the inspected primary article, including its treatment of the boundary of the density simplex. It is an explicitly cited theorem dependency, not an unproved new claim by the packet. Neither ordinary Ollivier/W_1 curvature nor a modified log-Sobolev constant can replace this variational quantity.

## 4. Uniform density, one-card lifting, and the asymptotic upper test

At density one, the density-derivative term vanishes. Reversibility gives A=−⟨ψ,Lψ⟩ and B=⟨Lψ,Lψ⟩. A one-card indicator, centered by 1/n, has eigenvalue −nq. Consequently κ_n ≤ nq = 2/(n−1). This is an upper test only.

For z(σ)=σ(1), each full state has exactly one edge moving the card from i to each distinct j. Within its own fiber it has d−(n−1) edges, all with zero lifted-potential difference. Therefore the projected off-diagonal rate is q, not 1/(n−1), and the stationary measure is 1/n. The full L of a lifted function is exactly the lift of the quotient L. Grouping weighted edge sums consequently proves equality of both A and B for any positive lifted density and potential. The finite audit checks this for multilevel quotient densities and nonindicator potentials, not just the special one-parameter test.

For density (t,1,…,1), t>0, and potential (1,0,…,0), the quotient action is

A = (n−1)q θ(t,1)/n > 0.

The density drifts are q(n−1)(1−t) in the special state and q(t−1) elsewhere. The potential's Laplacian difference across a contributing edge is −nq times its potential difference. Substituting gives exactly

R_n(t) = [n + (t+n−2−(n−1)/t)/log t] / [n(n−1)].

Thus κ_n ≤ R_n(t) for every t>0, t≠1. This formula, including t<1, is independently checked by exact directed-edge sums. At t=1 the singularity is removable, with R_n(1)=nq and derivative q(2−n)/4. For n≥3 the derivative is strictly negative, proving a strict improvement for sufficiently small positive t−1.

For the all-n limit, setting t=√n simplifies the expression further:

n R_n(√n) = n/(n−1) + 2(n−2+1/√n)/[(n−1)log n].

The second term tends to zero, since (n−2+1/√n)/(n−1) stays bounded and log n tends to infinity. Hence **limsup nκ_n ≤ 1**. Every test density is strictly positive for finite n≥2, and all denominators are nonzero. No exchange of an optimizer with a limit is used: the inequality holds separately at each n.

The known lower bound remains of order n^-2 and this upper bound remains of order n^-1. A better upper-test constant does not identify the order or establish one-card optimality.

## 5. Quotient comparison, parity, and the exact n=2 value

For a reversible equitable quotient with its pushforward stationary measure, lifted tests have the same two forms. The original chain's infimum is over a superset of those tests. Therefore the valid direction is κ_X ≤ κ_Y. A quotient lower bound does not reverse this direction.

The parity quotient has two equally weighted states and rate one in each direction. At density (a,b), its quotient is

B/A = 2 + (b−a)(θ_1−θ_2)/(2θ).

To verify the sign for all positive densities, write θ(a,b) as the integral of a^s b^(1−s), 0≤s≤1. The Hessian quadratic form of the integrand is

−s(1−s)a^s b^(1−s)(u/a−v/b)² ≤ 0.

Thus θ is concave. Gradient monotonicity applied to (a,b) and (b,a), together with symmetry, gives (a−b)(θ_1−θ_2)≤0. The displayed remainder is nonnegative; it vanishes when a=b. The restricted infimum is therefore exactly two.

For n=2 the parity quotient is the entire chain, so **κ_2=2**. For n≥3 even the uniform-density test is strictly below two. Thus the unrestricted reverse comparison is false. This is a concrete obstruction to the discarded proof route; it is not a counterexample to the original order question.

## 6. Diagonal/off-diagonal decomposition and the published local test

Retaining only the same edge's jump in each local density/potential drift gives the packet's B_on. For each edge the bracket is

2θ + (b−a)(θ_1−θ_2)/2 ≥ 2θ.

It follows that B_on≥2qA. The nonnegative total remaining contribution for the transposition graph is an established, credited result, not inferred from finite tests here. The inspected source distinguishes disjoint and overlapping pairs with their respective square-counting weights.

The source diagram's six vertices have three density-ε/potential-one vertices in one bipartition and density (1,ε²,ε²), potential (0,2,2) in the other. It is exactly the labeled K_3,3 test in the packet, up to graph relabeling.

For 0<ε<1, M=−log ε>0, independent ordered-edge computation gives

A = (1−ε)(1+2ε)/(6M),

B_on/A = (1+2εM−ε²)/(6εM),

B_off/A = (1+2εM−ε²)/[3M(1+2ε)],

B/A = (1+4ε)(1+2εM−ε²)/[6εM(1+2ε)].

These identities are verified symbolically for arbitrary positive ε with its stated domain and by exact finite rational/logarithmic controls. All denominators are positive and A>0 before passage to the limit. As ε→0, M→∞ and εM→0. The common numerator tends to one. Therefore B_off/A→0, while B_on/A and B/A diverge to positive infinity. In particular the action itself tends to zero, so reasoning only about unnormalized Hessian numerators would be invalid.

As a concrete negative control, ε=2^-31 gives B/A>10,000,000 and B_off/A<1/50. This rules out any numerical confusion between vanishing off-diagonal ratio and full-curvature sharpness. The local example neither settles κ_3 nor proves n^-2 asymptotic order.

## 7. Exact S3 witness, independently reconstructed

With lexicographic permutations (012),(021),(102),(120),(201),(210), take the exact density (1,1,16,16,1,1) and potential (5,−5,8,−8,5,−5). All density coordinates are positive and their mean is six. The normalized density is obtained by dividing by six, with no change of quotient.

An independent Hamming-distance graph construction gives the density drift

(5,5,−10,−10,5,5)

and potential drift

(−17/3,17/3,−22/3,22/3,−17/3,17/3).

There are four low-low edges, four mixed-density edges, and one high-high edge. Writing ℓ=log 2, the action is

A = 2248/9 + 15/(2ℓ).

Separately summing the two Hessian pieces yields

density-derivative part = −140/9 − 15/(4ℓ) + 675/(128ℓ²),

gradient part = 2104/9 + 25/(6ℓ).

Hence B = 1964/9 + 5/(12ℓ) + 675/(128ℓ²), exactly equal to the formula in the original proof. Their difference is

(9/10)A−B = [37888ℓ²+36480ℓ−30375]/(5760ℓ²).

The denominator is positive. The numerator is strictly increasing for ℓ>0. Integrating the positive geometric series on [0,1/3] gives ℓ>2/3; substituting 2/3 in the numerator gives 97057/9>0. This proves the strict bound without any floating-point premise.

The independent finite checker also encloses log 2 between rational partial-series/tail bounds and encloses B/A between **0.881815 and 0.881816**, strictly below 0.9. This is the distinct exact test underlying the retained claim, not the saved optimizer candidate near 0.8816783. The witness does not attain the established lower bound 2/3 and is not claimed to minimize the full problem.

## 8. Matrix formulation and numerical limitations

For a fixed positive density the matrix of A is a weighted graph Laplacian. The density contribution is half the corresponding Laplacian weighted by θ_1Lρ_x+θ_2Lρ_y. Since L is symmetric, the gradient contribution is −(AL+LA)/2. This verifies the packet's matrix identity. All matrices annihilate constant vectors. Fixing one potential coordinate to zero represents the quotient by constants; connectedness and positive edge means make the restricted action matrix positive definite.

These assertions were checked coefficient-by-coefficient on all 21 pairs of S3 coordinate basis directions, independently of the author optimizer. A generalized eigenvalue at one positive density therefore is a legitimate fixed-density numerical calculation. It says nothing by itself about global density optimality.

The numerical code's near-diagonal formulas are truncated Taylor expansions, while the other branch evaluates quotient-rule expressions in machine precision. No interval-error bounds or global optimizer certificate are supplied. The saved candidates were independently re-evaluated using Decimal at 80 and 120 digits; the two reevaluations agree within 10^-70. The optimizer itself was not rerun. This high-precision agreement is a numerical stability observation, not a new interval certificate. The discrepancy in Section 1 must remain visible in any summary claiming reproducibility.

## 9. Five approaches and final disposition

The five counted approaches remain distinct: uniform-density spectral tests; nonuniform one-card tests; quotient/parity comparison; local Bochner geometry; and finite full-Hessian search with exact witness extraction. Source retrieval and audit controls are not additional mathematical attempts.

Each failed route has the correct missing step: spectral calculations omit nonuniform densities; one-card upper tests do not lower-bound the full infimum; quotient lower bounds have the wrong direction; a vanishing off-diagonal ratio does not control the full Hessian above; and finite numerical optimization does not settle a global or all-n problem.

**Keep status unsolved at 5/5.** The safe retained results are the exact upper-test formula, limsup nκ_n≤1, κ_2=2, the exact κ_3<9/10 certificate, quotient-direction obstruction, and the evaluated local diagonal/off-diagonal/full ratios. No matching all-n order, exact constant for n≥3, prior-resolution conclusion, or novelty assertion is certified by this audit.
