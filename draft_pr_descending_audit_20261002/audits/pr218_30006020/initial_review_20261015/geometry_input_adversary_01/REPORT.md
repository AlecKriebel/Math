# Independent geometric and enumerative audit of PR218 / problem 30006020

**Status: PASS within the assigned mathematical-input scope.** I found no fatal error in the candidate's geometric reduction, exact composition law on the retained event, exceptional-probability estimates, or moment transfer. The main source-dependent claim is stronger than the published macroscopic Poisson-Dirichlet convergence, but it follows from the positive polynomial expansion and uniform correlator estimates. I reconstructed that implication rather than infer it from the published weak convergence theorem.

Audit target: submitted `unsolved_math_prioritization/attempts/30006020/CANDIDATE.md` at frozen PR head `dc457c741c779fbf90fbfdcdc73f750b3716f561`. This report concerns the claimed principal quadratic-stratum law in the iterated order of limits, first square count and then genus. It is not a priority or novelty determination.

Independence: before sealing this report I read the frozen candidate and freshly retrieved primary sources only. I did not read inherited `independent_review`, root reconstruction or conclusions, sibling reports, or old `FINAL_DISPOSITION`. All writes were inside this audit's assigned directory. No Git/index/ref mutation, provider write, outreach, paper, deposit, or tracker action was performed.

## Claim, assumptions, and success criteria

Fix genus g >= 2. Sample unlabelled holomorphic square-tiled half-translation surfaces with at most N unit squares, then let N tend to infinity. Restricting this fixed-genus sampling to the principal stratum Q(1^(4g-4)) has the same limiting cylinder-area law. Denote by nu_g the resulting unordered multiset of normalized areas of maximal horizontal cylinders. Every cylinder is counted once, regardless of its integer height. There is no primitive-cover condition.

Set n=3g-3 and a_j=zeta(2j)/(2j). The proposed model gives each ordered positive composition (j_1,...,j_k) of n mass

    (1 / (h_n k!)) product_i a_(j_i),
    h_n = [z^n] exp(sum_(j>=1) a_j z^j).

Given the composition, take the area vector to be Dirichlet(2j_1,...,2j_k), and then forget labels. The geometric success criterion is total-variation convergence of this full multiset law to nu_g. For moment transfer, an o(1) total-variation estimate alone is insufficient: the retained density comparison must be uniform, and moments of counts on the exceptional event must vanish.

Boundary checks include: k=1, equal part sizes and equal heights, the largest possible component count, highly unbalanced compositions, arbitrarily slow divergence of n*s_g, genus 2's special symmetry, fixed-genus window endpoints, and the distinctions among cylinder height, curve multiplicity, covering primitiveness, and zero labels.

## Primary evidence and custody

I independently retrieved the complete final published PDFs from these exact URLs:

- DL: Delecroix-Liu, JEMS 27 (2025), 5093-5131, DOI [10.4171/JEMS/1469](https://doi.org/10.4171/JEMS/1469), [publisher PDF](https://ems.press/content/serial-article-files/51451?nt=1). 39 PDF sheets. SHA-256 `03b84a6c19a8a9b25ad4c8991157f55247fe75e3297bad310aac7bcc85013a8b`.
- DGZZ: Delecroix-Goujard-Zograf-Zorich, Inventiones 230 (2022), 123-224, DOI [10.1007/s00222-022-01123-y](https://doi.org/10.1007/s00222-022-01123-y), [author-hosted published PDF](https://webusers.imj-prg.fr/~anton.zorich/Papers/Large_Genus_Asymptotic_Geometry_2022_Inventiones_published.pdf). 102 PDF sheets. SHA-256 `372586949b85e272a60b7a0dae2dc1c616cbfb94d0e661f40e5ba3bc8c621239`.

The PDFs, complete extracted text, and rendered evidence sheets are private and ignored by `.gitignore`. `SOURCE_RECEIPT.json` records their hashes. `retrieve_sources.py` reproduces the downloads and stops if either PDF changes. The authored manifest contains only authored deliverables and hashes of private evidence, never copies of the primary papers. Relevant equation sheets were visually inspected to resolve mathematical symbols and fractions damaged by text extraction.

The following location table identifies the exact input and conditions, without treating theorem labels as substitutes for checking the formulas.

| Input | Exact primary location | Condition used here |
|---|---|---|
| Uniform isomorphism-class surface sampling and normalized cylinder areas | DL pp. 5096-5097, Section 1.2.1 and Theorem 1.4; PDF sheets 4-5 | Fixed g, N tends to infinity; height <= m, including m=infinity |
| Exact graph, height, and area mixture | DL p. 5103, (2.2)-(2.4), Remark 2.5; p. 5106, (3.1)-(3.3); p. 5107, Theorem 3.2; PDF sheets 11,14,15 | Whole weighted stable-graph mixture; corrected graph automorphisms |
| One-vertex reduction | DL pp. 5104-5105, Theorem 2.7; p. 5109, (4.1)-(4.2), Theorem 4.1; PDF sheets 12-13,17 | k <= kappa*log(6g-6)/2 with kappa>1; here kappa=6/5 |
| Uniform coefficient and exact polynomial | DL p. 5116, (6.1)-(6.4); p. 5117, proof of Lemma 6.4; PDF sheets 24-25 | c_(g-k,k)(j_i-1) uniformly close to 1 for logarithmic k |
| Stronger uniform coefficient bound and mechanism | DGZZ pp. 156-158, Lemma 3.5, (3.6)-(3.8) and proof; PDF sheets 34-36 | 800*k^2 <= G for coefficient c_(G,k), uniformly in every admissible composition |
| Principal stratum and labels | DGZZ pp. 145-147, Section 2.2 and (2.1); PDF sheets 23-25 | Fixed-genus lower strata negligible in square-count limit; labelled-zero factor cancels in probabilities |
| Height/multiplicity dictionary | DGZZ pp. 146-147, Section 2.2; DL pp. 5096-5097 | Integer bands of squares are curve multiplicities |
| Cylinder-count correspondence | DGZZ p. 132, Theorem 1.7, (1.6); pp. 152-153, (2.20)-(2.21) and proof; PDF sheets 10,30-31 | Components counted without multiplicity = maximal cylinders |
| Generating function of actual K_g | DGZZ p. 137, Theorem 1.12, (1.16); p. 210 proof; PDF sheets 15,88 | Fixed t=11/10 lies strictly inside complex disk |t|<8/7 |
| Relative multivertex error | DGZZ p. 205, Theorem 5.2; pp. 207-209 proof, especially (5.7)-(5.8); PDF sheets 83,85-87 | k <= log(g)/log(9/4), a uniform range containing the proposed cutoff |

DGZZ's body in this supplied PDF does not print page numerals on every sheet. The journal locations above use the article's 123-224 pagination; PDF sheet numbers are unambiguous retrieval locators.

## Exact measure and conventions

DL defines Q_g(Z) as holomorphic square-tiled surfaces with the square labels forgotten. Theorem 1.4 takes an explicit uniform counting average on this set under the area and height cutoffs. Thus the required unlabelled sampling measure is directly present; there is no need to replace it by a cover model or to guess a lattice weighting.

The theorem first uses all holomorphic strata. DGZZ Section 2.2 supplies the fixed-genus principal-stratum reduction. The sentence in that section prints a limit in the symbol n where its surrounding count is ST_(g,n)(2N); the relevant limit is the square-count parameter N with g and the number of poles fixed. This is also forced by the dimension comparison underlying the count. In the present setting there are no poles. The candidate's principal-stratum scope is consistent with the exact source law.

DGZZ uses labelled simple zeros for its volume normalization, while DL's surface definition discards square labels. The fixed-genus zero-labelling multiplicity is common to normalized probabilities and does not alter the law used here. The normalized automorphism-weighted and unweighted descriptions agree on the generic fixed-genus stratum; special symmetry loci have smaller dimension. In genus 2 the generic hyperelliptic symmetry changes a common generic multiplicity, not the limiting normalized law. In any event, the audit's main chain uses DL's explicit uniform count directly, so it does not need an additional weighting-equivalence assertion.

The integer parameter m bounds the maximum cylinder height, equivalently the largest multiplicity of a component in the associated integral multicurve. m=infinity means summing every positive integer height independently. It does not mean restricting a square-tiled torus covering to primitive covers. Horizontal core curves of distinct maximal cylinders are distinct reduced multicurve components; height does not create extra cylinders. Rotation exchanges horizontal and vertical directions and preserves the sampling ensemble, so the vertical marginal agrees.

## Independent reconstruction of the latent law

Write Gamma_(g,k) for the one-vertex graph with vertex genus G=g-k and k loops. For the retained k range, G is a large nonnegative integer and the vertex is stable. Assign temporary labels 1,...,k to the loops.

The graph polynomial is

    F_(g,k)(x) = (product_i x_i)
                 V_(g-k,2k)(x_1,x_1,...,x_k,x_k).

Its degree is 6g-6-k. In each split pair of descendant degrees, put

    j_i = d_i^- + d_i^+ + 1.

The descendant dimension constraint is

    sum_i (d_i^-+d_i^+) = 3g-3-k,

so every j_i is positive and sum_i j_i=3g-3=n. Substituting the explicit definition of c_(G,k) into the Kontsevich polynomial gives the exact identity

    F_(g,k)(x) = A_(g,k) sum_(j_1+...+j_k=n)
                  ctilde_(g,k)(j) product_i x_i^(2j_i-1)/(2j_i)!,

    A_(g,k) = (6g-5-2k)! 2^(3k-3)
              / ((g-k)! (3g-3-k)! 3^(g-k)),
    ctilde_(g,k)(j) = c_(g-k,k)(j_1-1,...,j_k-1).

Every coefficient is positive. This is the pre-size-biased density expansion on DL p. 5117. One must use the exponent 2j_i-1 there; the subsequent size-biased marginal has an extra power and is a different object.

For a fixed height vector h, substituting x_i/h_i and multiplying by 1/h_i converts the ith monomial to

    x_i^(2j_i-1) / h_i^(2j_i).

Summing h_i from 1 to infinity produces zeta(2j_i), with no further coupling. A monomial integrates on the sum-one simplex, with the coordinate Lebesgue convention of DL, to

    product_i (2j_i-1)! / (2n-1)!.

Its normalized conditional area law is therefore exactly Dirichlet(2j_1,...,2j_k). The total shape is 2n=6g-6. Both 2j_i and 6g-6 survive direct normalization; replacing the total by 4g-4 would be an error. The candidate does not make that replacement.

The unweighted graph automorphism group has size 2^k k!: loop permutations and independent flips of the two half-edges. Let b_g=b_(g,infinity) in DL. The exact latent probability for this graph and composition, already integrated over heights and area vectors, is

    1 / ((2n)! b_g) * D_(g,k)/k!
        * ctilde_(g,k)(j) * product_i a_(j_i),

    D_(g,k) = A_(g,k)/2^k.

The remaining conditional kernel is the Dirichlet law just computed. The prefactor 1/((2n)! b_g) is independent of k and j. This also follows directly by applying the operator Z_infinity to F: each monomial contributes product_i zeta(2j_i)/(2j_i).

There is no missing second k!, no missing power of 2, and no additional multinomial factor for repeated j_i. The exponential formula uses ordered temporary slots and the single 1/k!. Repeated heights are handled by the orbit-stabilizer identity

    sum_(height orbits) f(h)/|Aut(Gamma,h)|
      = (1/|Aut(Gamma)|) sum_(ordered height vectors) f(h).

This is the corrected convention of DL Remark 2.5. In particular, one should not divide each ordered height vector by a weighted automorphism order separately.

## Uniformity for all compositions, including unbalanced ones

The relevant uniformity is not a claim only about typical or balanced j. It follows from a positive weighted-average identity. Put D_i=j_i-1 and G=g-k. Substitution of the normalized intersection-number formula into c gives

    c_(G,k)(D) = 2^(-(6G-6+5k))
        sum_(a_i+b_i=D_i) (1+epsilon(a_1,b_1,...,a_k,b_k))
             * product_i binom(2D_i+2, 2a_i+1).

The product weights sum to 2^(6G-6+5k), because the odd binomial coefficients of order 2D_i+2 sum to 2^(2D_i+1). Thus c is a convex average of the normalized correlators. Any uniform correlator error bound immediately holds uniformly for c, regardless of the relative sizes of D_i.

DGZZ Lemma 3.5 and its proof make this quantitative:

    sup_D |c_(G,k)(D)-1|
       <= C (k+2 log G)^2 / G,     provided 800 k^2 <= G,

for sufficiently large G. At

    k <= k_g = floor((3/5) log(6g-6)),

G=g-O(log g), and the condition holds eventually. Consequently

    sup_(k<=k_g,j) |ctilde_(g,k)(j)-1| = O((log g)^2/g).

This independently checks both the genus shift and the full-composition quantifier in DL (6.1)-(6.2). It is stronger than the candidate's stated o(1).

The exact successive prefactor ratio is

    D_(g,k+1)/D_(g,k)
       = 12(g-k)(3g-3-k)
         / ((6g-5-2k)(6g-6-2k)).

For k=O(log g), its logarithm is O((k+1)/g); summing gives

    sup_(k<=k_g) |D_(g,k)/D_(g,1)-1| = O((log g)^2/g).

The numerator and denominator differ by a polynomial of order g*k+g, not g^2, so this estimate is uniform over the chosen range. Finite exact checks below also confirm the ratio.

After normalizing the retained latent mass, the actual/model Radon-Nikodym derivative lies between 1-C*epsilon_g and 1+C*epsilon_g, with epsilon_g=O((log g)^2/g). Therefore, for every nonnegative measurable area statistic f,

    E_actual[f | one vertex, K<=k_g]
       = (1+O(epsilon_g)) E_model[f | K<=k_g].

The bound is uniform in f, including genus-dependent shrinking-window powers. Sorting or forgetting temporary labels cannot increase total variation.

## Exceptional probabilities and the actual K_g moments

The actual K_g is exactly the component count in DGZZ (1.6), by Theorem 1.7 and the exact surface/multicurve correspondence. It counts maximal cylinders without multiplying by height. DGZZ Theorem 1.12 gives, at the fixed allowed point t=11/10,

    E[t^K_g] = O((6g-6)^((t-1)/2)) = O(n^(1/20)).

No derivative at a moving point, coefficient extraction outside its stated domain, or uniformity in N and g is needed. Chernoff gives

    P(K_g>k_g) <= C n^(-eta),
    eta = (3/5) log(11/10)-1/20
        = 0.007186107882594953... > 1/220.

The floor and the constant factor 2 in 6g-6=2n affect only C. More generally,

    P(K_g>u) <= min(1, C n^(1/20) t^(-u)).

Splitting the tail-sum formula for E[K_g^r] at L log n, with L>(1/20)/log(t), proves

    E[K_g^r] = O((log n)^r)

for every fixed r. This is a genuine moment bound from a real point t>1; a central limit theorem would not suffice.

For k<=k_g, the first part of DGZZ Theorem 5.2 applies because

    3/5 < 1/log(9/4) = 1.23315... .

The total k-edge contribution divided by the one-vertex contribution is

    1 + O((log g)^25 g^(-1) 2^k).

Since all graph masses are nonnegative, it follows that the conditional multivertex probability is at most this relative excess. Uniformly through k_g it is

    O((log g)^25 g^(-1+(3/5) log 2)),
    1-(3/5) log 2 = 0.5841116916640328... .

Averaging over k<=k_g and adding the large-K tail proves

    P_actual(bad) = O(n^(-eta)).

The stronger-looking unrestricted statement printed later as DGZZ Corollary 5.3 is not required and was not used.

The same K estimates hold in the model. Its exact pgf is

    E_model[t^K] = [z^n]H(z)^t / h_n.

Here H(z)=(1-z)^(-1/2)B(z), where B is analytic for |z|<4 and B(1)=sqrt(2). Convolution with the binomial coefficients gives h_n~sqrt(2/pi)n^(-1/2), and the corresponding exponent t/2 yields E_model[t^K]=O(n^((t-1)/2)). Thus the model tail above k_g is O(n^(-eta)) and E_model[K^r]=O((log n)^r).

Combining retained-event density comparison with these exceptional probabilities proves Theorem A. In fact the checked quantitative inputs yield d_TV(nu_g,mu_n)=O(n^(-eta)) for this conservative fixed choice of t and cutoff, without asserting that this is an optimal rate.

## Why the moment transfer is strong enough

Let C be a count of cylinders in any finite union of compact positive rescaled-area windows. For every fixed r, C^r<=K^r, so Cauchy-Schwarz gives

    E_actual[C^r;bad]
       <= E_actual[K^(2r)]^(1/2) P_actual(bad)^(1/2)
       = O((log n)^r n^(-eta/2)) = o(1).

The model exceptional contribution has the same bound. On the good event the nonnegative-statistic density comparison applies directly to C^r; its error is multiplicative and uniform over shrinking windows. Therefore the transfer works as soon as the ideal-model compact-window rth moments remain bounded. It does not confuse total variation with uniform integrability.

I also checked the candidate's ideal-model argument for that boundedness. If q_n=n*s_g tends to infinity and q_n=o(n), factorial moments of the assembly have exact coefficient ratio h_(n-sum j_i)/h_n. The ratio is bounded for sum j_i<=n/2 and is at most O(sqrt(n)) globally. Marking part j with Gamma(2j,1), a selected j>=n/(2r) has exponentially small probability of entering a fixed q_n-scale compact window. This dominates the O(sqrt(n)) ratio and the remaining O((log n)^r) sums. Hence every fixed factorial moment of the unnormalized marked-window count is bounded.

The total Gamma variable has shape 2n. On 1/2<=T/(2n)<=2, the normalized-window count is bounded by a marked count in a fixed enlarged window. Outside this event, K<=n and the Gamma tail is exponentially small. Thus all normalized compact-window moments are bounded as claimed, and higher-moment bounds imply uniform integrability of every fixed moment.

For extremely slow q_n divergence, there is no hidden union bound over K approximately log n. The mean marking error is a sum over part sizes with weights O(1/j). Sizes j comparable to q_n contribute O(q_n^(-1/2)); smaller sizes have a factor O(log(q_n)) times exp(-c q_n), and larger sizes have exp(-c j). These bounds still vanish, for example, when q_n grows more slowly than log log n. The total Gamma normalization tends to 1 in probability and positive dilation is continuous in the vague topology, so no independence between T and the point process is needed.

These calculations support the candidate's mesoscopic limit and all fixed joint count moments. The requested g^(-1/2) window satisfies the assumptions. Its intensity integral is (log 2)/2, and exp(-(log 2)/2)=1/sqrt(2). At each sufficiently large fixed genus the relevant area-window endpoints are below 1; the one-cylinder atom at 1 cannot hit them, and the other mixtures have continuous simplex densities. This justifies applying the fixed-genus sampling limit to the window counts before sending g to infinity.

## Adversarial routes and source cautions

| Attempted falsification | Mechanism tested | Outcome and precise limit |
|---|---|---|
| Replace the whole law by the published PD weak limit | Weak product-topology convergence hides microscopic coordinates | Blocked as a proof route; candidate correctly uses the positive full-density expansion instead |
| Look for a shape-parameter or total-area mismatch | Reintegrate the exact pre-size-biased monomial | Dirichlet(2j), total 6g-6 verified; a 4g-4 substitution would fail |
| Introduce an extra factorial for labels or equal heights | Recompute graph orbit-stabilizer factors | Single 1/(2^k k!) verified; repeated j and height values do not add factors |
| Test only balanced compositions | Examine binomial-average identity and extreme j | Full uniformity verified, including j_1=n-k+1 and the other j_i=1 |
| Extend the relative multivertex bound to all k | Inspect proof (5.7)-(5.8) and later corollary | Unsupported outside its ranges; candidate stays safely inside the first range |
| Use TV alone for unbounded count powers | Compare bad-event contribution against K moments | Insufficient route blocked; pgf plus Cauchy-Schwarz supplies the required o(1) |
| Break Gamma marking at slow mesoscopic scales | Avoid concentration union over every part | Weighted mean and factorial-moment estimates remain valid |
| Impose primitive-cover or fixed-height interpretation | Trace m through the source dictionary | Rejected: m is cylinder height/curve multiplicity; m=infinity is exactly the required case |

Three source-exposition cautions should be kept separate from the candidate's mathematics:

1. DL Theorem 4.1 is printed as a relative expectation equivalence for every bounded h. Its conditioning proof immediately establishes additive control by ||h||_infinity times the exceptional probability; a literal relative equivalence for every h, including h supported on the discarded event, is too strong. The candidate derives the necessary conditional uniform density comparison separately and is not relying on that overstrong reading.
2. DL's proof of Theorem 2.7 prints in (2.8) a bound exp(-epsilon(kappa)*g) for a count whose mean grows like log g. The stated mod-Poisson mechanism gives polynomial decay in g at a fixed multiple of that mean. The candidate uses the valid explicit polynomial Chernoff estimate from DGZZ instead.
3. DL Theorem 3.3's prose describes labels by bijections of complementary components and curve components. Taken literally, this does not record independent half-edge flips of a loop, although its normalization invokes the full graph automorphism group. A one-loop graph already exposes the wording mismatch. The exact graph weights, corrected Remark 2.5, genus-two tables, and the polynomial formula all use the full 2^k k! factor consistently. The candidate uses those formulas, so this wording issue does not introduce an extra factor into its law.

DGZZ Corollary 5.3 also prints an unrestricted O((log g)^25/g) conditional separating probability, while the supporting proof contains factors depending on k and explicitly bounded ranges. I have not used that corollary to certify any assertion. This matters because simply checking that a cited theorem number exists would miss the usable hypothesis.

## Reproducible exact computations

Run `python3 exact_checks.py` in this directory. The script independently computes Witten intersection numbers using exact rational string, dilaton, and DVV recursion, rather than importing the candidate's coefficients or any inherited audit computation. It reconstructs each graph-polynomial coefficient from paired descendant degrees.

All 123 ordered positive compositions tested, with total genera 2 through 5 and 1<=k<=min(3,g), pass these exact checks:

- positivity of the graph coefficient;
- equality of the direct graph coefficient with the independent binomial-average formula for ctilde;
- equality of the graph-automorphism-integrated monomial weight with D_(g,k)/k! times ctilde times product 1/(2j_i), with zeta factors left formal;
- the successive D ratio whenever both k and k+1 are available.

The independent base checks include <tau_4>_2=1/1152, <tau_0 tau_2>_1=1/24, and <tau_1 tau_1>_1=1/24. In genus 2, the one-loop polynomial is x^5/48 and the two-loop polynomial is x^3*y+x*y^3, matching DL Table 1. Here ctilde is 3/4 for k=1 and 1 for k=2: it is correctly not asserted to equal 1 at finite genus.

For the genus-two one-vertex graph masses before common normalization, the script's formulas give

    k=1: (5/4) zeta(6),
    k=2: (3/2) zeta(2) zeta(4).

These independently check the factors most vulnerable to a silent 2^k or k! mistake. The computed large-g D_(g,k_g)/D_(g,1) values are approximately 0.99666305 at g=10^3, 0.9999826667 at g=10^6, and 0.9999999999227 at g=10^12. These floating values are illustrative checks; the logarithmic product estimate is the proof of uniform convergence. Full rational results and numerical constants are in `EXACT_CHECK_RESULTS.json`.

## Strongest verified result and exact remaining gap

Assuming the published exact surface/multicurve correspondence and uniform intersection-number estimates as credited geometric inputs, the candidate's entire-area-multiset total-variation model follows, with all constants and conditioning conventions checked. The fixed-t pgf and the valid low-k relative error are quantitatively strong enough for every fixed compact-window count moment. The elementary assembly and Gamma-marking estimates also survive the boundary-rate checks needed for all sequences s_g tending to zero with g*s_g tending to infinity.

There is no remaining mathematical gap identified in this assigned geometric/enumerative mechanism. I have not re-proved the foundational Masur-Veech correspondence or Aggarwal's intersection-number theorems from first principles; these remain substantial credited inputs, not new results of the candidate. Broad priority, the OWR problem's provenance and exact original wording, literature coverage beyond the two primary sources, and the overall repository release decision remain outside this independent audit.

Completion estimate for this assigned input audit: 100%. No external input was required or requested.
