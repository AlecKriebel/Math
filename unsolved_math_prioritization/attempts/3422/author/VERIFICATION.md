# Reproducibility and verification scope

Date: 2026-10-08. The mathematical outcome is a prior-literature classification, with source-inspection limits stated in REPORT.md and SOURCE_AUDIT.md.

## Executed checks

The checker uses the Python standard library and exact rational or integer arithmetic. Every guard uses explicit conditional failure; an AST check rejects Python assert statements. The same checks ran successfully under normal Python, -O and -OO as non-root UID 1000, with bytecode writing disabled, on a copy whose files were 0444 and directory 0555.

Each run included actual permission probes: creating a new file inside the packet was denied, and opening every existing packet file for writing was denied. The existing-file probes do not truncate or write any content. Pre/post SHA-256 inventories confirmed that the trial payload bytes did not change.

The supporting calculations cover:

- 18 strictly increasing piecewise-linear homeomorphisms and 126 dilation-parameter cases, with inverse identities, exact supremum scaling and point-track bounds checked at rational sample points and relevant breakpoints
- 405 exact periodic-shear cases, including a noncompactly supported example
- 254 interval compressions across seven standard-Cantor stages, with image intervals certified to lie inside omitted middle-third gaps
- 12 radial compression profiles, with inverse, monotonicity and boundary checks
- Binary distinct-generator commutator trees with 2,3,4,5,6,7,8 and 16 leaves, checking the canonical leading monomial coefficient and homogeneous degree
- Full truncated Magnus expansions for 2,3 and 4 leaves, including conjugation and inversion tests
- 100 homology-rank bookkeeping cases across ambient dimensions 3 through 12, explicitly distinguishing the nonvanishing H2 in dimension 3
- Payload file-set, byte-count and SHA-256 checks, plus guards preserving the imported Sher-theorem inspection limitation and the 0/5 prior-resolution status

## Negative and positive controls

- Non-strictly monotone PL input, an out-of-range dilation parameter, invalid Cantor depths, empty commutator trees and a zero generator are rejected.
- The incorrect opposite dilation scaling is detected by its displacement increase.
- The identity preserves a Cantor endpoint and is not treated as a displacement witness.
- The repeated-generator commutator [x,x] vanishes, while the distinct-generator commutator has a nonzero leading term. Thus written length alone is not accepted as a certificate.
- The dimension-three H2 term is retained rather than forcing the higher-dimensional vanishing formula into that dimension.
- A requested output path inside the packet is rejected under -OO, before any file is created.
- The writable development tree is rejected by --require-readonly under -O.
- Deliberately appending to REPORT.md in an independent copy is rejected under -OO by the pinned byte-count check.
- An explicitly external output file is successfully written, while default execution writes JSON only to stdout.

## Exact limits

These are finite checks of the supporting algebra and explicit formulas, not a computer proof about arbitrary wild Cantor embeddings. The general planar cover argument, Sher separation theorem, spun-Bing shrinkability, Alexander duality and Stallings theorem are not established by finite sampling. Their roles and inspection status are stated in the written report.

The final frozen payload and source-free archive have an external SHA-256/byte inventory. PAYLOAD_PINS.json pins every other payload file, including the checker. The external freeze receipt additionally pins PAYLOAD_PINS.json and the archive. Final normal/-O/-OO checks are rerun on that frozen payload, and the exact correction patch is replayed against the retained initial authored report.

No private corpus contents, source text, scholarly PDFs, local coordination logs, or raw source caches are included in the payload.
