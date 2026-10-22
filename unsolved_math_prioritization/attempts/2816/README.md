# Minimal foliations: accepted scoped partial results

**Rank 911 / ID 2816 / KP-3.18 remains unsolved, with 3 of 5 approaches used.**
The exact original author freeze was independently accepted without correction.
This is AI-assisted research and an independent AI audit, not human peer review.
There is no novelty or priority claim.

Start with [the exact acceptance](independent_audit/ACCEPTANCE.md),
[the proof](author/PROOF.md), [the mathematical audit](independent_audit/MATHEMATICAL_AUDIT.md),
and [the source review](independent_audit/SOURCE_REVIEW.md).

The four scoped propositions exclude the constant principal-curvature equality
case, establish a curvature balance and strict crossing for smooth minimal
foliations on each closed ambient component, establish strict crossing for
compact members of an actual embedded minimal product family, and obstruct
closed descent of the standard vertical-plane foliation of hyperbolic space.
The original question does not assume the additional smoothness or product-family
hypotheses. These results do not resolve general minimal-foliation existence.

The `author/` and `independent_audit/` directories preserve all 27 frozen members
byte for byte. The two ZIPs, two external manifests, and author validation receipt
are preserved in `frozen/`. Historical author labels saying review is pending
remain untouched; the separately dated exact acceptance records the completed
review. `STATUS.json` is the canonical publication status.

## Reproduction

Tested with Python 3.12.14 and SymPy 1.14.0. From any working directory:

    python /path/to/2816/verify_publication.py

The new wrapper rejects missing, extra, changed, or nonregular files; authenticates
five immutable inputs and all archive members before executing scripts; checks
the exact acceptance and unsolved status; then reconstructs isolated inputs and
repeats the 63-case independent harness under ordinary Python, `-O`, and `-OO`.
Each harness itself covers all three modes, 139 author algebra checks, 512
independent finite checks, 16 author-integrity mutations per mode, and three
trusted-input mutation controls. The wrapper also reproduces all 42 audit
verifier self-tests. `--integrity-only` skips execution after byte/scope checks.

Authenticate the wrapper and public manifest against independently delivered
commit and byte hashes. A locally editable manifest alone cannot prove authenticity.
The finite controls do not certify the geometric statements or settle the problem.
`VALIDATION_RESULTS.json` records publication-wrapper adversarial tests.

`INPUT_VERIFICATION.json` records a fresh complete-corpus/full-pair and six-PDF
pin check plus fresh matching text extractions. It does not claim remote source
redownloads. The source review retains its bounded search and access limitations.
No source PDFs, extracted source text, dataset records, or private coordination
material are included.

This checkpoint is a draft pull request only. There is no merge, release, DOI,
deployment, or outside outreach. Local passing checks are not GitHub CI.
