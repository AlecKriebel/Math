# Independent acceptance of the median inequality two pass reader

## Decision and exact scope

**Accepted as a historical two-pass partial-results checkpoint.** The unrestricted normalized-supremum conjecture remains unresolved. The reader supplies valid affirmative subclasses, exact diagnostics against stronger false reformulations, and limitations of particular proof methods. It supplies neither a genuine uniformly negative counterexample nor a general proof. No theorem-level correction is required by this review.

This acceptance concerns the reader identified by public manifest SHA-256

`a0d04d609ebf1bc146a23a36e67d14142e226a18a309fee47eb80e03b5dea4b7`.

That manifest covers 24 public files besides itself: all eight proof reports, all four mathematical audits, six exact certificate records, the reader introduction, reproduction and validation notes, and the three-file angular-mollification change record. The review covers every included file. The checkpoint records exactly the first two documented shared substantive passes on problem 3700039, row 1762 / AMR-036-0039. Auditing, reproduction, and this acceptance do not add a substantive research pass. The lifetime count of earlier attempts remains unknown. This document makes no claim about later research or historical novelty.

## Source attribution and the target

The primary source is A. Eremenko, [Conjectured inequality for subharmonic functions](https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf), dated 4 April 2015. The two-page note was checked for the normalization, the supremum assertion, the separately stronger small-radius assertion, and the credit for the homogeneous and harmonic cases. Its power-growth assumption describes an application; it is not a hypothesis of the general question. On 13 October 2026 the author's [problem index](https://www.math.purdue.edu/~eremenko/uns1.html) still linked this question without a resolution annotation. This is a bounded source observation, not proof of worldwide openness.

The reader consistently uses the intended pointwise middle value of three whole-plane subharmonic functions satisfying u_j(0)=0. Its angular integral I(r) uses dtheta, without the factor 1/(2*pi), and B(r) is the largest of their circle maxima. The source does not specify zero denominators.

The chosen convention is stated accurately: for a nonzero triple evaluate I/B only on D={r>0:B(r)>0}; treat the globally zero triple separately as zero equality. The first theorem proves D=(R_0,infinity), with B=0 exactly on joint zero disks. Assigning zero to every 0/0 is a weaker extension on nontrivial flat-disk triples, and equivalence has not been claimed or proved. A genuine negative example under the chosen convention needs one epsilon>0 bounding I/B above by -epsilon on every radius in D. Neither an isolated negative circle nor a negative unnormalized integral at every finite radius is enough.

## First pass claims

### Denominators and the sharp circle bound

The denominator classification uses local upper bounds, upper semicontinuity, the submean and strong maximum principles, and harmonic comparison on annuli. These establish finiteness, nonnegativity, monotonicity, continuity, the zero left limit, and the zero-disk characterization without assuming continuity of the original subharmonic representatives.

Circle integrability follows because local upper bounds control the positive part and submean excludes an infinite negative part. For ordered values a<=b<=c<=B, the inequality a+b+c<=2b+B yields I/B>=-pi; the upper bound 2*pi is immediate and attained. The Fejer construction gives genuine harmonic polynomial triples, correctly normalized positive convolution, and a degree-9999 fixed-radius witness. The exponential-series computation and strict relative error 189/20000<1/100 were independently reconstructed. The witness proves sharpness of the fixed-radius lower bound while remaining inside the credited harmonic affirmative class.

### Exact harmonic diagnostic and finite jets

The three root-of-unity harmonic functions have B(r)=r+r^2. Direct symbolic evaluation of the sine primitive at the actual ordering-sector endpoints reproduces all three integral regimes, both junctions, and both normalized endpoint limits. The integral is strictly negative at each positive radius, while its normalized supremum is zero and is not attained. The preserved separate clamp control in the theory audit remains an additional check, not a substitution of examples.

The leading-jet theorem retains its uniform expansion and nonzero common leading-order hypotheses. Positive rescaling gives subharmonic homogeneous polynomial limits, the credited half-period argument gives a nonnegative median integral, and the leading maximum is positive. Hence a smooth counterexample would have every component flat at zero. This necessary condition does not resolve the flat case.

### Spiral, rotating-separable, compact-potential, and periodic reductions

The common spiral proof has the correct conjugated angular operator, positive half-period Green kernel, common shift and positive weight, median monotonicity, and removable origin. Different exponents or angular drifts are outside its conclusion.

The rotating-separable angular lemma treats both complex characteristic roots and real same-sign roots. The common amplitude is positive on the whole logarithmic line and tends to zero at its left endpoint, ensuring F''>0 somewhere. The clarified proof first averages over rotations with a positive angular mollifier, obtains a C^2 subharmonic function away from zero, and only then selects the radius. Uniform convergence justifies the median limit. This removes any need to restrict an arbitrary distribution to a fixed-radius slice. The supplied original, clarification, and exact mathematical patch preserve the theorem's hypotheses and conclusion; both patch directions have been executed and checked.

For compact positive logarithmic potentials, the absolute logarithmic moment makes normalization at zero finite. The uniform far-field expansion and highest harmonic-degree comparison give the stated affirmative result. Noncompact mass, infinite mass, and nonpolynomial harmonic contributions remain outside that proof.

The log-periodic reduction has the correct multiplier, noninteger nonresonance condition, and uniform negative criterion. Continuity and compactness convert an all-phase strictly negative median into a genuinely negative normalized supremum. Finite sampling does not establish that premise.

## Second pass claims

### Positive smoothing and the two flat frontiers

The coefficient estimate |c_n|<=b follows from the nonnegative function b-U, rather than from a nonexistent pointwise lower bound. The exact weighted-square sum gives K_N=N(N+1)(N+2)/6. Positive Fejer convolution defines an actual positive measure on the logarithmic-radius axis at each angle; it does not require an arbitrary distributional slice. The integrated angular-curvature correction has second derivative of the correct sign and a zero left limit. Convexity then supplies the lower bound, with both integration constants controlled.

The resulting estimate is

I(exp t)/b(t)>=-2*pi*K_N*A(t)/b(t)-E_N(t).

The factor 2*pi and the sum of all three unnormalized L1 errors are necessary. At an infinitely flat origin, record-scale maximization gives A(tau)/b(tau)<=1/M^2, with N fixed before M increases. At a flat-disk boundary, A(t)/b(t)<=(t-t_0)^2/2 gives the stronger one-sided liminf under the stated angular compactness. Neither argument assumes homogeneous dilation limits.

The equivalence between the stated asymptotic Fejer-error condition and relative L1 compactness uses bounded normalized profiles, contraction, finite-dimensional approximation, and continuity on compact intervals away from the frontier. It is an additional hypothesis. The smooth oscillatory flat examples genuinely violate it: the single-component fixed-N error tends to 4/5, the identical-triple sum tends to 12/5, and their median quotient is the positive value 8*pi/5. The independent positive Laplacian margins are exactly 27/16 and 10011/4096. The cutoff and convex radial correction preserve smoothness and whole-plane subharmonicity.

The exact-growth example has B(r)=r^2 and a positive median. Its logarithmic angular amplitude varies, which is incompatible with a fixed angular profile under common scaling and rotation. It disproves an automatic tangent-shape inference, not the conjecture. These results retain their continuity assumptions and do not cover arbitrary discontinuous representatives.

### Periodic symmetry, high frequency, and finite-point obstruction

The temporal scalar inverse has a positive kernel and the correct shift orientation. It proves nonnegative angular means. A common sign-reversing angular shift therefore gives the claimed nonnegative median at every phase, even with otherwise independent phase modulation. The theorem does not assert admissibility of arbitrary coefficient choices.

The high-phase-frequency theorem fixes noninteger rho and each nonzero nonnegative finite Fourier forcing. Its strictly positive half-period margin and the bound on nonzero temporal modes give the stated threshold. The threshold depends on the forcing; it is not uniform over changing forcings, nor a result about intermediate frequencies. The zero-forcing and temporal-constant boundaries remain correctly distinguished.

The finite-point obstruction uses an invertible elliptic periodic operator, a logarithmic singularity with coefficient 1/(2*pi*omega), and a positive approximate unit concentrated at one chosen evaluation point. Its value there tends to negative infinity while the finitely many other distinct evaluations stay bounded. Merging repeated points preserves positive weights. This disproves a universal fixed positive finite sum of torus point evaluations on the whole cone. It leaves integral averaging, profile-dependent pairings, symmetry subclasses, and global arguments open.

## Exact certificate reconstruction and adversarial controls

A fresh reconstruction starts from the real temporal form P=A(theta)+B(theta)cos(s)+C(theta)sin(s). Symbolic Laurent expansion reconstructs every coefficient of P^2; exact complex inversion reconstructs every solution coefficient. Every coefficient and both phase slices match the reader, including the drift sign and conjugate symmetry.

The [independent reader certificate](independent_reader_checks.json) records a distinct 960-node rational calculation. It uses 30 and 11 alternating arctangent terms in Machin's identity; a degree-28 cosine and degree-27 sine polynomial; downward rounding to denominator 10^20; and common trigonometric error at most 4^29/29! plus half the proved pi interval width plus 10^(-20). Reduced arguments lie in [-pi,pi]. Rotations by thirds are exact index shifts. The median is evaluated by sum minus minimum minus maximum.

The derivative bound is 2*sum_(n=1)^2 n*(|Re(a_n)|+|Im(a_n)|). The median inherits that Lipschitz constant. Integrating distance to the central grid node on each cell bounds the angular mean error by D*pi/(2*N). All sign decisions are exact rational comparisons. Outward rounding gives

- -222245404751/500000000000 < M(0)/(2*pi) < -365366363637/1000000000000 < -1/3;
- 1 < 1256823133751/1000000000000 < M(pi)/(2*pi) < 128287323839/100000000000.

The checker also reconstructs the harmonic primitive formulas, the exponential sum, the general Fejer weighted-square identity, both flat-example margins, and the one-component/triple error distinction. Its 36 recorded checks are accompanied by nine rejected invalid controls: altered constant coefficient, omitted Fourier mode, reversed drift, wrong angular normalization, swapped phase slices, reversed interval endpoints, equality at a strict threshold, an insufficient 12-node sign certificate, and classification of a positive constant as negative. A constant one is independently recovered with exact mean one. The coarse-grid enclosure demonstrably crosses zero.

The existing 600-node full audit, 1536-node reader reconstruction, and delivered-artifact checks were also regenerated, including their original negative controls. The 600-node record reproduces every delivered exact rational quantity. The reader regeneration reproduces all delivered public certificate bytes. Normal and optimized executions agree. These finite calculations authenticate the specified algebra and enclosures; the analytic arguments above remain indispensable, and no all-phase negative conclusion follows from two checked phases.

## Editorial completeness and public scope

All eight full authored proof reports and all four full mathematical audits are present. The exact original-to-reader comparisons retain the mathematical content: other than the explicit angular-mollification clarification, differences are local navigation, removal of operational instructions, and removal or compression of exploratory search details outside acceptance. No missing proof is replaced by an asserted validation flag. All 51 rendered relative document links resolve within the reader tree.

The public manifest closes the included file inventory and names only included public objects. The public tree contains authored mathematical prose, exact authored certificates, the mathematical clarification record, and public scholarly citations. It contains no executable program, copied source document, third-party dataset, private coordination record, credential, or hash of a withheld object. File integrity and source attribution have been checked separately from the mathematical claims.

**Final disposition:** the reader is suitable as the specified historical two-pass checkpoint. The unrestricted normalized-supremum conjecture and the general periodic some-phase question remain unresolved. The denominator convention, attribution, extra compactness hypotheses, fixed-forcing limitation, and distinctions between counterexamples to a proof strategy and counterexamples to the conjecture must travel with any summary of these results.
