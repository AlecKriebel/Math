# Robustness research: five reviewed partial-result turns

**Current disposition: original unsolved, 5/5 substantive author turns.** The full unrestricted two-layer-network conjecture is not proved. The complete independent AI-assisted review passes the scoped results with the mandatory additive clarification below. No external peer-review or novelty certification is claimed.

## Required clarification

Read ADDITIVE_CHAINING_CLARIFICATION.md with TURN_4.md. The chaining base point and all nets in §2 must be deterministic and fixed before the data, specifically e_1 rather than the unrelated network-dependent empty-pattern vector of §1. Original35 frozen files are unchanged; the separately bound two-file addition makes this necessary distinction explicit.

## Results and limits

- Exact optimal Lipschitz interpolation law on the random circle and a geometric n²/log n lower floor
- Fixed-dimensional positive-density-chart birthday bounds, with dimension-dependent constants and explicitly global Gaussian scope
- Credited adaptive projection/rank mechanism on the actual sphere-restricted norm, with fixed-accuracy constants
- Log-free sqrt(n/k) sphere lower order for bias-free ReLU networks with independent hidden rows; dependent rows, hidden biases and overcomplete widths are excluded from this theorem
- Log-free sqrt(n/k) sphere lower order for rank-k quadratic-on-sphere functions, including quadratic-neuron biases and arbitrary width, with trace-zero balancing to remove radial constants; the fixed Lipschitz quadratic-core realization is a restricted subclass

See RESULT.md and review/ADVERSARIAL_REVIEW.md for full source and probability qualifications. The primary BLN results, classical tools and relevant later literature are credited. Historical checkpoint mentions of pending review are preserved; this additive README records the accepted present state.

## Reproduction

From this directory run `python review/verify_review.py --author .`. Python3 standard library only. It checks both author manifests, all37 corrected-head blob IDs and the review manifest, and reproduces329,914 author plus91,084 independent exact controls. These supplement the analytic probability proofs. Raw source PDFs/images and imported records are excluded. Optional `--sources sources` requires downloading the six exact source files recorded in SOURCE_MANIFEST.json; the ordinary public replay needs none.
