# Ueno-type varieties: corrected, audited partial results

**ID 30002829, OWR-13500-010, rank 727. Unsolved after 5/5 approaches.**

This is a provisional AI-assisted research checkpoint, not a solution or an
expert-reviewed theorem. The original questions are rationality of the
fourfold X_{4,6} and unirationality of the fivefold X_{5,6} over C. Both remain
unanswered by this packet. Rationality of X_{5,6} is a separate, stronger
unanswered question. Fourfold unirationality is a prior result.

## Mandatory reading and authority

1. Read [CONTROLLING_CORRECTIONS.md](audit/CONTROLLING_CORRECTIONS.md).
   Its domain and dominant-component replacements are mathematically
   authoritative over the frozen author text, not cosmetic qualifications.
2. Read the [independent audit](audit/AUDIT.md).
3. Read the [five original approaches](author/PROOF_ATTEMPTS.md) only with
   those corrections. All original author and audit files are preserved byte
   for byte, so their historical pending-audit, no-remote-write and local
   exhausted-budget labels describe their respective creation stages.
   [release_status.json](release_status.json) controls this checkpoint's
   disposition: unsolved, 5/5 approaches; none of the exact targets solved.

The old model-side nonvanishing product admits T=0 and is insufficient.
On the unique dominant component use the nonempty corrected open

    Omega_n: B_n U D q(q+2)(q(q+2)-U) != 0,

where U=w_2^3-1, V=w_3^3-1, D=s^2 U-V,
q=2(V-sU)/D, B_4=st(s-1)(t-1)(s-t), and
B_5=B_4 r(r-1)(s-r)(t-r), with projective coordinate z=1.
The original side is the inverse image of this open with x_1 y_1 != 0.
The correction proves both inverse compositions, gives a surviving domain
witness, and checks the downstream arguments on the intended function field.

The full unsaturated fivefold intersection has genuine vertical components,
including s=0, w_3^3=1 and s=1, w_3^3=w_2^3. No global integrality assertion
for that intersection is retained. Only the dominant component and the
geometrically integral generic fiber are used.

## Retained conclusions and boundaries

- Corrected invariant-field/birational reductions in dimensions four and five.
- Fixed-base nonrationality of the fourfold's cubic surface, alongside its
  prior unirationality theorem.
- A smooth geometrically integral generic (3,3) surface of general type for
  the fivefold projection, and genus-one generic fibers for another fourfold
  projection. These are relative obstructions only; they do not establish
  nonrationality or nonunirationality of either total space over C.
- A conditional curve-family descent argument whose characteristic-zero
  generic counting and incidence hypotheses remain unproved.

No novelty, global-current-openness, or stable-rationality conclusion is
claimed. The exact live problem pages and full raw imported statement/prior
AI records were not inspected; recorded descriptor hashes are not recomputed
raw-record hashes. The source-grounded formulation and these limits are
documented in [author metadata](author/source_verification.json) and
[audit metadata](audit/source_bindings.json). Only metadata and authored
research are included, not source PDFs, extracts, images or raw datasets.

Neighbor ID 30002830 has method-specific partial overlap with the fourfold
objective. It is not classified as a duplicate, solved, fully covered or
exhausted. Its queue row and attempt budget are unchanged.

## Reproduce

With Python 3 and SymPy 1.14.0, from this directory or any working directory:

    python /path/to/30002829/verify_release.py

The wrapper checks the full release allowlist, byte counts, SHA-256 bindings,
frozen manifests, controlling corrections, 32 author checks and 115
independent checks (including 11 negative controls). It compares regenerated
JSON with the frozen results and refuses optimized Python or
PYTHONOPTIMIZE settings that disable assertions. No source downloads or
working-tree writes are performed. Checks supplement the written proofs;
counts are not a formal proof certificate or peer review.

The queue patch changes only this row's Status to unsolved and Turns to 5/5.
Findings, Chat, DOI, all other rows, and every other existing queue byte are
preserved. No queue regeneration is part of this checkpoint.
