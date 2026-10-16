# A compact counterexample to the anti-invariant integrability implication

Problem **30004549 / OWR-2654829-012**, queue rank **940**. Status:
**claimed_solved**, cumulative author turns **4/5**. This is AI-authored,
unrefereed work. Novelty has not been established.

## Result and credit

The [unchanged proof](author/R3_counterexample_candidate.md) constructs a smooth
nonintegrable almost-complex structure on the compact connected product of
the genus-two curve `y^2=z^6-1` with an elliptic curve. Three independent real
de Rham classes have closed anti-invariant representatives, so `h_J^- >= 3`.
Compactly supported exact perturbations preserve all three classes, and an
explicit nonzero Nijenhuis component establishes nonintegrability.

This gives a negative resolution of the integrability clause in the stated
smooth compact four-dimensional scope. The generic-vanishing clause is the
prior theorem of **Qiang Tan, Hongyu Wang, Ying Zhang, and Peng Zhu**,
*On Cohomology of Almost Complex 4-Manifolds*,
[arXiv:1112.0768v3](https://arxiv.org/abs/1112.0768),
[DOI 10.1007/s12220-014-9477-2](https://doi.org/10.1007/s12220-014-9477-2).
No new proof of that theorem is claimed. Neither an exact value of `h_J^-`
nor fixed-symplectic-form compatibility is claimed.

The target is Conjecture 2.5 of
[Draghici-Li-Zhang](https://arxiv.org/abs/1104.2511) and OWR 33/2020,
printed page 1687. The [MFO PDF](https://publications.mfo.de/bitstream/handle/mfo/3805/OWR_2020_33.pdf?isAllowed=y&sequence=4)
and [publisher PDF](https://ems.press/content/serial-article-files/46869?nt=1)
were separate retrievals with different sizes and hashes. Each retrieval is
recorded separately; they are not asserted to be byte-identical. The withdrawn
[Lejmi-Upmeier manuscript](https://arxiv.org/abs/1507.00282) is not used.

## Exact accepted object

The proof is **9,997 bytes**, SHA-256
`50a267656e6a5412a2e14208ada5aec203df4c5385be63b831029188cb1cf39e`.
Both fresh independent AI audits accepted these exact bytes without a
mathematical correction:

- [Audit A](audit_a/INDEPENDENT_ACCEPTANCE_A.md), 10,890 bytes, SHA-256
  `a4e8a88320d30cafe7fe5c95fa95f97fab999baa5dba1241c3e7919fb6b20988`.
- [Audit B](audit_b/INDEPENDENT_ACCEPTANCE_REPORT.md), 12,527 bytes, SHA-256
  `05a1a99f0c825be6a623b0ad827008fb68a442f38f7908593bdef6ce4c612568`.

See the [scope and credit cover](author/PUBLIC_SCOPE_CREDIT.md) for the
historical candidate label, the current 4/5 count (one earlier turn plus three
resumed turns), and the clarification that `C` in the displayed elliptic
quotient denotes the complex plane. The proof, audits, and their manifests
are preserved verbatim. There is no correction patch or silent acceptance
rebinding. The finished construction stops before a fifth author turn.

## Reproduction

Use Python 3.10 or later. Integrity verification and its negative tests use
only the standard library. Symbolic replays require SymPy 1.14.0, as pinned in
`requirements.txt`. From this directory:

```sh
python verify_publication.py --self-test --run-checkers
python -O verify_publication.py --self-test --run-checkers
python -I verify_publication.py --self-test --run-checkers
```

The verifier authenticates every listed payload file before execution and
checks the complete file inventory, SHA-256, byte counts, Git blob hashes,
the seven-member author archive, the archive's extracted mirrors, all original
manifests, and the exact accepted proof and review pins. It rejects deliberate
file, manifest, path, and archive mutations. Each of the three independent
source-free symbolic scripts is replayed under normal, optimized, and isolated
Python. Frozen review scripts contain assertions; the driver explicitly
compiles them with `optimize=0`, including under `python -O`, and tests that a
false assertion is rejected. Running a frozen review script directly with
`python -O` would disable its assertions and is not an equivalent test.

[Recorded replay results](VERIFICATION_RESULTS.json) are finite symbolic
checks only. They do not certify the global geometric argument, smooth
patching, cohomological independence, current literature, or novelty. The
written proof and audits address the global mathematical steps. Independent
AI review is not human peer review, formal proof-assistant verification, or
journal acceptance.

The manifest and its checksum are integrity aids, not digital signatures.
Authenticate this package against a separately verified Git commit or manifest
hash. The manifest does not list itself or its checksum sidecar; both are
separately bound by the Git commit. No copied source PDFs, extracted source
text, corpus contents, or private coordination material are included.

## Queue scope

The accompanying queue patch changes only rank 940's Status, Turns, and
Findings cells. It preserves all unrelated bytes, including the pre-existing
header and links, and does not regenerate the queue or modify lifecycle state
files. The public status is a scoped AI research claim, with the prior theorem
credited explicitly, rather than a claim of novelty or formal certification.
