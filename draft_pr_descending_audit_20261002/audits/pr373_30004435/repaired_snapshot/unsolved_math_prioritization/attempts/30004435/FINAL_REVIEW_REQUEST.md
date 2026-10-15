# Independent full five-turn review request

Target30004435 / OWR-17474-009, Steif Question C, original printed632. Proposed result is unsolved5/5, with complete scoped entropy-free partials. Review all five proofs and the exact source, not only the computational receipts. The general source equality is known through entropy; the unresolved request is specifically a probability-only proof.

## High-risk points to audit

- Turn1: periodic phase versus invariant events; conditional D-stationarity; two-sided bridge denominator and uniform phase limits; completed-tail projection argument; ordered finite-window limits.
- Turn2: observability may merge hidden phases/classes; conditional empirical frequencies in both directions without reversibility; equal future profiles determine full laws using common D; word-length s−1 stabilization; stochastic-emission joint-state bound.
- Turn3: uniform-overlap and summable-continuity assumptions; forced agreement blocks and the stopping-time union bound; entire remote-future coupling rather than only a single coordinate; existence versus uniqueness; no unjustified bilateral-tail inference.
- Turn4: conull decisive-block definition; outside-only decoder measurability; exact summable boundary error; completed-field limit; radius moment is not automatic; inclusions do not equate two nontrivial subfields.
- Turn5: non-atomic disintegration, componentwise mixing with no uniform rate, joint L² profile recovery, countably many null sets, random law rather than redundant label; explicit irrational-rotation decoding in both directions and its nonmixing obstruction.

## Replay and source instructions

Run `python REPLAY_ALL.py` (stdlib only). Each TURN_n_CHECKS.json must match the corresponding script output byte-for-byte. The script also verifies historical and final artifact manifests. With `--sources PATH`, it verifies the PDF hashes in SOURCE_MANIFEST.json and TURN_3_SOURCE.json.

Read the original Steif contribution pp632–633, especially Question C. Read Al-Najjar–Shmaya2014 Theorem5.2 pp13–14 and Example6.1. Read Lemańczyk2020 thesis AppendixB.1 andB.3.2 pp111–115 for entropy/Pinsker and finite-Markov scope. Read Bressaud–Fernández–Galves1999 Sections4.1–4.4 for coupling credit; the packet's stated total-variation criterion has its own proof. The raw sources are research inputs, not files for public upload.

No theorem of unrestricted equality is claimed. A successful audit should bind exact frozen bytes and distinguish a scoped PASS from a resolution of the original method problem. Further author search has stopped at five turns; only additive source, review or packaging corrections should follow.
