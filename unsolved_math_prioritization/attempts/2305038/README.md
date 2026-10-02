# Problem 2305038: reviewed alternative proofs, original goal unresolved

**Original-source disposition: unsolved, 5/5 substantive author turns exhausted.**

Hayman–Lingham Problem 5.38 asks for substantially simpler proofs of two known sharp comparisons for a function subordinate to a normalized univalent function. This package gives complete, independently audited alternative proofs under the classical nonnegative initial-derivative normalization. It does not establish substantial historical simplification or claim a new sharp inequality.

## Current proofs and audit

1. [Modulus comparison](MODULUS_PROOF_REVIEWED.md): the sharp radius is (3−√5)/2
2. [Derivative comparison and uniform disk-map bound](TURN_5.md): the sharp derivative radius is 3−2√2; the final proof removes the earlier parameter split
3. [Final independent audit](review/final/FINAL_ADVERSARIAL_REVIEW.md): mathematical PASS, qualitative source goal unverified
4. [Earlier complete four-turn audit](review/ADVERSARIAL_REVIEW.md): retained unchanged, with its harmless recovery-byte differences documented in the final audit
5. [Source scope](SOURCE_SCOPE.md), [final status](FINAL_STATUS.json), and [publication manifest](PUBLICATION_MANIFEST.json)

The corrected theorem assumes g=F∘φ, where F is normalized univalent on the unit disk, φ is a holomorphic disk self-map with φ(0)=0, and φ′(0) is real and nonnegative. The known conclusions are |g(z)|≤|F(z)| up to the modulus radius and |g′(z)|≤|F′(z)| up to the derivative radius. Both constants are sharp. A merely real, possibly negative, initial derivative does not suffice; the source normalization issue and counterexample are preserved in the research history.

## What remains unresolved

Correctness of these proofs does not certify the source's qualitative request. The original Shah papers and complete Campbell III proof have not been compared. Duren's 1977 survey already contains the odd-function modulus mechanism, and classical Schur/two-point methods underlie the derivative proof. The final presentation is shorter than this package's earlier derivative proof, but no historical novelty or first-resolution claim follows.

## Validation and preservation

All five author checkers were rerun, as were the independent controls. The fifth-turn audit derives an additional nonnegative 5×6 tensor-product Bernstein coefficient certificate independently from the squared inequality; it does not reuse the author's polynomial decomposition. Exact algebra checks are distinguished from numerical diagnostics and from the analytic proof.

The original thirty author files are preserved byte-for-byte from commit `dfa19a2d481fb9cce6a37453c789c1915dd82f49`; historical status text marked pending or 4/5 is left intact. `FINAL_STATUS.json` and the final audit give the current disposition. The original `TURN_4.md` is retained; the additive reviewed modulus copy changes only the identified argument-distance wording. All review histories and receipts remain available.

The first local review used three initially recovered files with an extra trailing newline. [The byte audit](review/final/RECOVERY_BYTE_AUDIT.json) records that harmless difference and the authoritative remote hashes; publication preserves the original remote bytes rather than changing history.

## Reproducing checks

Use Python 3 with SymPy and mpmath. Run author checkers on a disposable copy because some write their receipt beside the script. From this directory, the independent checks may be run as:

```sh
python review/independent_controls.py --proof-dir .
python review/final/independent_turn5_controls.py --proof-dir .
```

The first includes explicitly labeled high-precision diagnostics, which are not universal proofs. The second uses exact symbolic/rational identities. The mathematical arguments and all hypothesis checks are in the proof and audit documents.
