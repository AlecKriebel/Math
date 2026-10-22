# A fixed-area exceptional set for positive squared-pole sums

Problem 2307037 / AMR-022-7037, Hayman–Lingham Problem 7.37.

## Complete affirmative deduction

For every finite sum g(z) = sum_j lambda_j/(z-z_j)^2 with positive real weights summing to 1 and arbitrary complex poles, including repeated poles, there is one compact set S(g) of planar area exactly pi such that, simultaneously for every real R>1,

integral over { |z|<R } minus S(g) of |g(z)| dA <= 2pi log R + pi(log 2 + 1/e).

The target is an ordinary nonnegative Lebesgue integral. The set is chosen once, independently of R. No location, separation, overlap, connectedness or unit-disk restriction is imposed on the poles. The exterior-field argument covers every complementary component, including bounded holes. The leading coefficient 2pi is sharp; no optimality is asserted for the additive constant.

## Attribution and review

The proof is a complete deduction from the established Eremenko–Hamilton sharp Beurling-transform indicator estimate and the Levine–Peres quadrature/smash-sum theorem, together with the supplied localization argument. These imported results are credited, with exact assumptions and normalization checked in SOURCE_HYPOTHESES.md and AUDIT.md. Quadrature existence is not claimed as a new result.

The complete argument passed a separately tasked independent internal AI-assisted mathematical audit without required mathematical correction. The manuscript and audit are unrefereed. This is not human peer review or formal proof-assistant certification. No novelty, priority, exhaustive literature determination, or claim that the original question was globally open is made.

## Reading guide

- [PROOF.md](PROOF.md): complete analytic theorem, construction, all-radii bound and sharp logarithmic coefficient
- [SOURCE_HYPOTHESES.md](SOURCE_HYPOTHESES.md): imported assumptions and all complementary-component tests
- [AUDIT.md](AUDIT.md): complete independent mathematical audit and adversarial cases
- [AUTHOR_CHECKS.md](AUTHOR_CHECKS.md): author analytic checks and supplementary diagnostic history
- [ACCEPTANCE.json](ACCEPTANCE.json) and [STATUS.json](STATUS.json): exact accepted scope and original/distributed document identities
- [SOURCE_REVIEW.md](SOURCE_REVIEW.md), [SOURCE_DEPENDENCIES.json](SOURCE_DEPENDENCIES.json) and [SOURCE_METADATA.json](SOURCE_METADATA.json): source attribution, exact interfaces, public PDF identities and bounded inspection history
- [VERIFICATION_SUMMARY.md](VERIFICATION_SUMMARY.md): historical verification and its limits
- [MANIFEST.json](MANIFEST.json): exact public membership and SHA-256 identities

Only nonmathematical status, source-accounting and distribution wrappers were edited. Every mathematical section of the proof, source-hypothesis argument and audit remains. Audited original and distributed hashes are deliberately distinct. The source-dependency ledger is byte-identical to the accepted audit's ledger.

The analytic proof is standalone. Finite computations and integrity checks are supplementary, with no hidden software, dataset or generated-certificate dependency. Programs, raw outputs, generated certificates, datasets, copied source PDFs/text/images and private coordination are excluded from this edition.
