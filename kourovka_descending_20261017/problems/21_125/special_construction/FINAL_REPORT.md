# Constructive algebraic family — terminal research report

**Target:** ordinary Hydra virtual specialness, Kourovka21.125(b), all ranks m≥5. **Outcome:** no complete construction and no counterexample. Discovery estimate: **5%**. Publication gate remains closed. These notes deliberately retain the distinction between specialness and compact specialness.

The original investigation explored three algebraic mechanisms rather than assuming that existing special analogues cover the ordinary groups.

| Mechanism | Checkable result | Exact remaining gap | Status |
|---|---|---|---|
| Cyclic-HNN embedding into a RAAG | A general marked Britton embedding lemma; explicit index-two rank2 embedding in A(P4) | A compatible finite-index marked embedding in every rank making the edge identifications realizable by RAAG conjugacy/vertex extensions. The supplied rank2 embedding does not automatically have those markings. | Blocked without a new marked construction |
| Finite-cover induction from the preceding rank | A finite quotient balancing/extension lemma imposes any chosen finite-index subgroup of H_r on all vertex stabilizers in a finite cover of H_(r+1) | A valid special-combination theorem or explicit global RAAG embedding for that cyclic graph of special groups. One edge family remains nonmalnormal in every finite cover. | Finite-cover step proved; specialness step open |
| Lift from Brady–Soroko special Hydra analogues | Explicit surjection to ordinary Hydra; two natural proposed sections fail by exact RAAG/Britton normal forms | A nontrivial section or a new finite-index embedding, whose existence cannot be inferred from the quotient | Blocked, no section candidate |
| Supporting finite quotient filter | All regular canonical covers with abelian original fiber image self-cross, proved symbolically for all ranks≥3 | Nonabelian fiber quotients and alternative cubulations are unrestricted by this result | Accepted pending fresh review; does not disprove specialness |

## Reproduction

Run `python3 check_algebraic_reductions.py` and `python3 check_finite_covers.py --max-rank 6` in this folder. Both require only the Python standard library. The first reproduces 8,000 exact Britton-reduced sample images, symbolic integer-fiber identities at ranks3–30, and an explicit order8 quotient extending balanced H2 edge orders to H3. The second constructs14 explicit regular finite filiform quotient covers and computes actual opposite-edge hyperplane equivalence classes. Rank2 has no self-crossing in these tested covers; this alone does not certify full specialness (self-osculation and inter-osculation are not checked). Every tested rank≥3 self-crosses.

Finite tests support the independent unbounded proofs in `ALGEBRAIC_REDUCTIONS.md` and `FIBER_ABELIAN_COVER_OBSTRUCTION.md`; they are not used to extrapolate a universal result. The proof notes state the exact extent of every claim. The special analogue relations were transcribed from the cached primary paper §5.1, and the ordinary square presentation from Dison–Riley pp.510–511.

No paper, publication package, Zenodo upload, tracker mutation, git operation, or external communication was performed by this family. The claimed small-rank injection is a rederivation, not a priority claim. The root should retain the overall research label **unsolved** unless another independent family resolves the full question. Fresh review findings must be incorporated before promoting the supporting lemmas in the shared ledger.
