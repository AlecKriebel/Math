## Accepted prior arbitrary-residue counterexample

The complete prose proof of Shouqiao Wang, *A Proposed Solution to Erdős
Problem 486*, is accepted after mathematical audit. One fixed infinite set
of positive moduli, with fixed arbitrary residue sets, has survivors B with

    liminf L_B(x) <= 177/200 < 49/50 <= limsup L_B(x),
    L_B(x) = (1/log x) sum_{1<=m<x, m in B} 1/m.

Source: [ten-page Wang manuscript](https://multiscalar.ai/results/erdos-486/paper.pdf),
350612 bytes, SHA-256
`01ce6f1d22b0c9208cc45ecaa15039f0ee13ea75c334908ca65f371c365b9048`.
This is acceptance of an identified prior theorem, with no novelty claim.
The arbitrary-residue result does not settle singleton-residue EP25.

The result applies to the original inclusive-activation formulation in
[Erdős, Some unsolved problems (1961), I.26, printed pp.235–236](https://users.renyi.hu/~p_erdos/1961-22.pdf).
For every installed endpoint/modulus pair, q<m<2q. Hence every installed
residue is nonzero, and strict q<m and inclusive q<=m activation produce
exactly the same survivor set at every positive integer. The general
primitive-set bridge is also verified but is unnecessary for this example.

## Complete analytical audit and focused independent check

AUDIT.md retains the full global proof analysis: finite periodic recovery,
arithmetic skeleton, endpoint abundance, deterministic collision removal,
conditional fresh bits, entropy bounds, simultaneous finite-block selection,
summable footprints, separated epochs, fixed data for all cutoffs,
recovery/deletion subsequences, and the exact original-formulation bridge.
No unresolved mathematical gap was found in the pinned prose theorem.

FOCUSED_AUDIT.md independently retains the full deletion-lemma derivation
and exact activation bridge. It establishes individual conditional candidate
probabilities after collision removal and uses a union bound, without
asserting independence across candidates. Its accepted scope is focused;
it does not claim a second independent audit of every global-theorem step.

An optional explicit finite-threshold computation and finite toy parameters
and numerical computational witnesses are omitted; historical-check wording
is clarified. These are editorial changes only. All general mathematical
derivations, theorem constants and proof-level limitations remain. No new
mathematical proof attempt or publication-stage mathematical test was made.

## Formal evidence and review boundaries

Acceptance means independent internal AI review of the specified written
arguments. This AI-assisted work is unrefereed. No external human peer
review, journal acceptance or local proof-assistant certification is claimed.
Historical exact arithmetic and finite-mechanism checks passed normal/-O/-OO
with byte-identical results where recorded; they support the written proofs
and do not prove infinite statements.

The retained formal statements were text-read, but no local Lean build,
replay, full formal dependency audit or axiom computation was performed.
The retained author commit is `d28713ac8245ca86a686b8c67370a8d19d81b242`;
the external replay report concerns `61325b10bbdc29f4fb5e0618b414b9f2189333ad`.
Identity between those source trees was not established. The inspected
formal implementation uses a four-color biased construction; the accepted
prose proof uses fair bits and a central-subset window. Statement readback
is not a claim of a line-for-line formalization of this prose construction.

The external report's replay and standard-axiom claims are not locally
reproduced evidence. Its strict/inclusive bridge was explicitly not
formalized there. This acceptance rests on the written proof and the
independently proved exact activation bridge.

## Sources and publication boundary

SOURCES.json retains public titles/URLs, byte/hash pins, version identifiers
and accurately scoped historical inspection. The primary audit text-read
all ten manuscript pages and the full retained TeX; manuscript pages 6 and 9
and original Erdős printed pages 235–236 were visually inspected. No fresh
publication-stage source inspection, current tracker status or exhaustive
novelty/community-resolution claim is made.

Exactly eight authored-prose/public-verification-metadata files are added
under attempts/2141. Copied source bodies/PDFs, code, datasets, raw
certificates, numerical computational witnesses, private sources and private
coordination are excluded. Analytic constants and their written derivations
remain. This is not an executable reproduction package. Original sealed
audits, QUEUE.md and all unrelated repository content remain unchanged.
Preparation verifies exact bytes, editorial scope and native addition-only
structure; it executes no third-party code.

## Exact public-file identities

- `ACCEPTANCE.json`: 2,098 bytes; SHA-256 `7f2174bfc5322642a84c4df5e9d3a94c5d70f36cc7b155acac6d0cd8b127fd70`.
- `ACCEPTANCE.md`: 4,844 bytes; SHA-256 `66a6b14404c7edec8accb7779bb6c417bb6b4e270e8b1c7126d09fdb3a0aa341`.
- `AUDIT.md`: 20,404 bytes; SHA-256 `9379a98395e748856eb3ea778ea9134303577a24c9feef390efd4c934acb3035`.
- `FOCUSED_AUDIT.md`: 13,657 bytes; SHA-256 `57efd48cd81d7444631f7f2baf7f60059e602844ac6edce649b1eece94cf8359`.
- `MANIFEST.json`: 1,589 bytes; SHA-256 `5825dd34a45b21e6ab07fcb57adbb6f029f5464845872903ceeb4093a2e1e1c1`.
- `README.md`: 3,543 bytes; SHA-256 `e2c533894a61d9879b50da4b6353a3196e0f1cf9a28543640864a571ac35a457`.
- `SOURCES.json`: 5,388 bytes; SHA-256 `3c6e6d4ca43dc7c23a8a2eae42f4e6c9fdac5c71a35d40705729598005a26062`.
- `VERIFICATION.json`: 2,287 bytes; SHA-256 `445c473d2fd9b22f4946edd43fdd934430fd7fb04efb2e1b41318ab592747ce4`.

MANIFEST.json lists all eight members and hashes the other seven; this body independently pins its digest.

