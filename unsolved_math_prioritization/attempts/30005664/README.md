# Critical Dirac potentials: audited scoped results

**Original problem 30005664 / OWR-14297742-004 remains unsolved after 5/5 substantive approaches. Independent AI audit PASS for the five explicitly limited propositions. No mathematical correction to either freeze was required.**

**The sharp constant 4m/p is a gap for the closed scalar upper-component Schur form at the fixed two-dimensional candidate. It is not a spectral gap of the full Dirac operator.** Its sharpness witness reconstructs an L² lower component exactly when p>3. For 2<p≤3 the scalar-form sharpness statement remains valid, but that witness does not produce an L² full spinor. Even for p>3 the reconstructed pair is not a threshold eigenspinor. Read [audit §6](audit/AUDIT.md#6-sharpness-and-the-full-spinor-distinction).

## Scope and source credit

The package proves an all-dimensional Clifford construction with an H¹ threshold state, exact norm minimization on one specified width branch, a Pohozaev identity in a stated dilation-differentiable class, boundary concentration at p=d, and the fixed-potential two-dimensional angular factorization. The finite-width candidate requires integer d≥2, finite p>d and m>0; its norm to power p contains m^(p−d).

Dolbeault, Gontier, Pizzichillo and Van Den Bosch already give the d=2,3 candidate and its upper bound in [§5.4 of their paper](https://arxiv.org/abs/2210.03091v2). No first-discovery claim is made. The remaining result is the uniform reverse inequality a_*≥A with the appropriate equality/attainment statement. Fixed-potential positivity and one-branch minimization do not establish radial or global optimality.

- [Authored proofs](author/PROOF.md) and [five substantive approaches](author/APPROACHES.md)
- [Complete independent audit](audit/AUDIT.md), including domain closure and infinitely many angular modes
- [Current verdict, precise limitations and publication metadata](VERDICT.json)
- [Author source checks](author/SOURCE_VERIFICATION.json) and [independent source review](audit/SOURCE_REVIEW.json)

This is AI-assisted, unrefereed work with independent AI review. It is not human peer review or formal proof-assistant certification; no novelty, journal acceptance or full solution is claimed. Source inspection is bounded evidence, not a universal current-open-status certificate.

## Reproduce

Use Python 3 with SymPy 1.14.0:

```sh
python3 -B verify_publication.py
python3 -O -B verify_publication.py
```

The portable verifier checks the exact recursive inventory, all SHA-256 hashes and byte counts, both untouched ZIPs and all 18 extracted-file matches, both frozen manifests, and byte-identical author and independent checker output. Frozen checkers always execute in isolated non-optimized Python children, with assertions enabled, even if the wrapper is launched with -O or PYTHONOPTIMIZE. The wrapper works from an unrelated working directory after relocation. The 957 author controls and 992 independent controls supplement the analytic proofs.

Add `--queue /path/to/unsolved_math_prioritization/QUEUE.md` to verify the full queue hash and the exact two-cell change. Only this row's Status and Turns become unsolved and 5/5. Every other byte, including Findings, chat links and the existing stale embedded header, remains unchanged. No queue generator is run.

Optional complete input verification needs all six arguments: `--author-zip`, `--catalog`, `--problems`, `--research-results`, `--dataset-manifest` and `--source-directory`. The final directory must contain the five PDFs named in [audit/README.md](audit/README.md). These external inputs are intentionally absent from this publication. Without them, that stage reports NOT_RUN, not PASS; the frozen input-verification record is historical evidence.

The original author and audit files and their safe ZIPs are preserved byte-for-byte. Historical pending-audit/no-remote-write statements remain creation-time records; the later PASS and this publication wrapper supersede them without rewriting history. Source PDFs, source extracts, images, raw corpora and private coordination files are excluded. This is a draft research checkpoint, with no merge, release, DOI deposit or outreach.
