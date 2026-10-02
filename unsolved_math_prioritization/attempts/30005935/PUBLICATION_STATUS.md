# Reviewed disposition: 30005935 / OWR-14298374-004

**Original broad source bundle: unsolved, five of five substantive author turns completed.** Independent full scoped review passed with no mandatory mathematical revision. Read [the results](RESULT.md), [the exact source scope](SOURCE_SCOPE.md), and [the independent review](independent_review/ADVERSARIAL_REVIEW.md).

## A complete negative subquestion result

For the intended geometric-Brownian-then-heat splitting method, the claimed unconditional mean-square half-order behavior with g(v)=v^(5/4) is false. In one spatial dimension, for every nonzero nonnegative smooth compactly supported initial profile, every time step and every grid index at least two, the actual coupled mean-square error is infinite. The iterates nevertheless remain finite and positive almost surely.

The proof first establishes infinite numerical moments above one, then constructs the exact global nonnegative local mild solution and bounds it by an inverse BES6 process with sufficient finite moments. It does not infer an error by subtracting two infinite moments. A separate strict-local-martingale argument gives a finite linear-mass weak error bounded away from zero at every fixed final time.

## A compatible positive scoped theorem

The same unmodified one-dimensional scheme converges in probability and its continuously interpolated path laws satisfy an O([log(eM)]^(-2)) bound in bounded-Lipschitz distance. This bounded-test theorem coexists with the unbounded-test and strong-moment failures because uniform integrability fails.

The source's broader weak question does not fix a test class or dimension. No positive algebraic weak order, optimal logarithmic rate, higher-dimensional sup-norm theorem, or result for the separate space-time-white-noise model is claimed. The overall record therefore remains unsolved rather than promoting the entire bundle from the complete negative subquestion result.

## Provenance and verification

All 45 frozen author files are unchanged. All 10 frozen independent-review files are unchanged. The source's missing old-value factor in a displayed formula is reconciled explicitly with its stated substeps; no silent algorithm replacement is made. Source papers, standard stochastic analysis and the older positivity theorem's regularity limitation retain their recorded credit.

The five original control scripts pass byte-for-byte with 62,188 exact assertions. Independent review adds 31,770 symbolic/rational controls and an analytical audit of the kernel tails, comparison, random clock, Sobolev estimates and localization. These finite checks are not PDE simulations and do not replace the proofs. The broad-goal planning estimate retained from the author is 75%, with low confidence; it is not a correctness or novelty probability.

This is AI-assisted mathematical research and independent AI-assisted adversarial review, supported by primary-source retrieval, Python, exact rational arithmetic and SymPy. Historical priority and novelty are unverified. The publication is a draft research checkpoint, not a merge, journal acceptance or DOI release.
