# Acceptance report: Erdős Problem 1038 / database 2449

## Bounded disposition

Accepted: the independently reconstructed strict upper bound

    inf measure{x in R: |f(x)|<1} < 1.834430475762662,

where f ranges over nonconstant monic real polynomials with all roots, counted with multiplicity, in [-1,1]. More precisely the proof shows the infimum is at most Lambda(q) for the exact rational q=0.02571553686652745032257637166391965344, and establishes a rational upper enclosure for Lambda(q) strictly below both 1.83443047576266171109075363512901884952989750747 and 1.834430475762662.

The construction is reproduced from Shouqiao Wang's proposed resolution, which credits the one-cut family to Terence Tao. This audit claims neither a new family nor a new resolution. The fixed q is not claimed to be stationary or optimal.

Not accepted: the full proposed exact infimum, a matching global lower bound, uniqueness of a globally minimizing parameter, the proposed digits of that global minimum, or nonattainment of that infimum by finite polynomials. No counterexample to the proposal was found. The public manuscript and result page are described according to the inspected snapshot as proposed.

## Complete proof chain for the accepted upper bound

1. Exact rational logarithm intervals prove 0<A<s<1 for A=log(H)/log(q), H=2q/(1+q)^2 and s=(1-q)/(1+q), and prove the geometric parameter domain.
2. The derivative and endpoint analysis establishes a unique nontrivial root of F in each required branch. Exact rational endpoint signs then certify the two explicit root brackets. Monotonicity of u+1/u yields the rational length enclosure and strict upper comparisons.
3. An atom at -1 plus an explicit nonnegative arcsine-weighted density is a probability supported in [-1,1]. Fourier/Poisson calculations identify its potential and its constant platform.
4. The Cauchy-transform derivative, monotonicity, and endpoint values exclude additional negative components. Perturbing A upward makes the platform strictly positive and gives exactly two potential zeros. The two crossings and negative-set length converge to the fixed-candidate values.
5. Equal empirical probabilities approximate each positive-platform measure, including its possibly irrational atom weight. Truncation of the logarithmic kernel proves L1 potential convergence. The two-point zero set implies convergence of negative-set lengths. The associated monic polynomials have admissible roots, and a diagonal choice gives lengths tending to Lambda(q).

The positive-platform step is essential. Weak convergence alone at a zero platform does not justify upper convergence of sublevel lengths. The proof supplies this step rather than assuming it. It guarantees that some finite admissible polynomials have length below the stated rounded bound, without a claimed explicit degree.

## Established supremum and external mathematical inputs

The supremum 2sqrt(2), with equality for (x^2-1)^m, is retained by specialization of Theorem 2.1 in [Tao's note](https://terrytao.wordpress.com/wp-content/uploads/2025/12/erdos-1038-2.pdf). The statement and specialization were checked; the theorem's full proof and scalar numerical inputs were not independently reproduced. Direct evaluation of those polynomial examples confirms their stated measure, including the irrelevant omitted point x=0.

The lower-bound analytic audit also retains the proposal's cited circle rearrangement and Pringsheim theorems as external inputs. Reviewing their use does not certify the unresolved numerical portions of the proposal.

## Two mandatory unresolved certificate gates

Certificate 6.1 must independently establish a gap-free derivative/convexity cover, including both singular ends, a unique stationary point, and rigorous enclosures for q_s, q_star and the global minimum L. The audit preserves all six source domain pieces, endpoint limits, soft-chart deflation, derivative tests, and interval-Newton requirements.

Certificate 7.1 must independently establish valid nonnegative references, correct simple main crossings, positive adjoint data and the strict block inequality for every nonempty quantile interval throughout k>=29/20. The audit preserves the affine, constant-edge, refined-terminal and final-terminal ranges, their overlap obligations, stated margins, Fourier tails, and dependence on the global minimum from Certificate 6.1. This is the remaining numerical basis required for the proposed matching lower bound and strictness/nonattainment.

The source verifier uses intended interval-enclosure tests, not merely sampled optimization. It was statically inspected but not executed; its old unused machinery was not entirely reviewed line by line. The linked Lean project was not executed and no Lean acceptance is asserted.

Independent acceptance requires pinned interpreter and package versions; review of proof-relevant conversions, all remainders and endpoint construction; justified fixed decimal padding (including 1e-85 and 1e-65) at the actual working precisions; completed logs; a gap-free coverage check; and explicit comparisons between the printed enclosures and theorem decimals. A PASS banner or padding constant alone is insufficient.

## Exact scope of the one-sided comparator bridge

The independent candidate proves Lambda(q)<LSTAR_HI. Conditional on Certificate 6.1 proving L is the global minimum, it follows that L<=Lambda(q)<LSTAR_HI. The block margin decreases with the target L, so a valid interval check over the hardcoded target interval includes its upper endpoint and suffices for every smaller L. This resolves the needed one-sided linkage only.

No claim is made that L>=LSTAR_LO, that L lies in the full hardcoded interval, that its proposed digits are validated, or that any affine interval run passed. Both certificate gates remain open.

## Arithmetic verification and publication boundary

The independent checker uses exact rational arithmetic and positive geometric-series logarithm remainders. After an implementation-only replacement of proposal regeneration by recorded rational centers, and assertions by explicit exception checks, the exact input values, acceptance inequalities and output were unchanged. The final checker passed in normal, -O and -OO modes during the audit and again during preparation, with byte-identical 2820-byte output, SHA256 b8fb956611313159f8e03f87fef65e0c8cadeb03f2117a9ed7cc4b159b6885bf.

The public proof appendix gives exact q, root endpoints, rational interval rules, logarithm remainder formulas, sign enclosures, length-comparison formulas and elementary-range positive margins. These are mathematical witnesses. Raw program output and executable checker code are excluded. Thus the report supports independent arithmetic rederivation, not an advertised turnkey public code replay. Hashes and three-mode execution receipts establish bounded integrity and implementation robustness, not the theorem by themselves.

The complete mathematical audit and all original proof sections are retained, subject only to report-reference edits and the added witness appendix. Mathematical content was not removed. The report includes public-source metadata rather than copied PDFs, extracted source text or rendered source pages. PDF hashes and inspection history are inherited from the completed audit; preparation freshly reverified the pinned audit artifacts and the locally available source verifier bytes, without re-downloading the PDFs.

## Next acceptance step

Independently reproduce and map Certificates 6.1 and 7.1 to the pinned manuscript and verifier, retaining the one-sided comparator bridge and all conversion/coverage obligations. Until those obligations are met, the bounded upper-bound reproduction remains the accepted result and the proposed full resolution remains verification-dependent.
