# Elite-pool path relinking: verifier-backed partial report

**Status:** `REPRODUCIBLE COMPUTATIONAL OBSERVATION — INTERRUPTED`

The frozen portfolio completed **10 of 22 directional jobs** and exactly **100,000 of 220,000 registered repair moves**. It then stopped at its registered disk-safety gate: after job 10, the runner observed fewer than the required `200000000` free bytes. No resume or overwrite was attempted.

## Method and preregistration

The audited 22-member start pool was used rather than the 22 conflict-block finals. The starts have complement-normalized locally aligned pair distances from 0 to 300, while all 231 final-pool pairs align at distance 0 and therefore form one isomorphism/complement class.

The frozen operator is genuinely two-parent: after complement normalization and a deterministic vertex alignment, it makes 48 objective-guided moves along the directional parent-disagreement path, then applies a 10,000-step exact incremental single-edge repair. Conflict color and overlap topology are not used in child generation, scoring, repair, or retention.

The registration audit passed all 21 pinned hashes, exact coverage of the 22 starts by 11 disjoint pairs, unique seeds, registered budgets, output absence, and the prelaunch disk gate. At launch, `245379072` free bytes exceeded the required `220000000`.

## Exact completed coverage

| Pair | Catalog lines | Direction | Seed | Steps | Final |
|---:|:---:|:---:|---:|---:|:---:|
| 1 | 144–253 | A→B | 2026083101 | 10,000 | E=2, C5=2, I5=0 |
| 1 | 144–253 | B→A | 2026083102 | 10,000 | E=2, C5=2, I5=0 |
| 2 | 1–2 | A→B | 2026083103 | 10,000 | E=2, C5=2, I5=0 |
| 2 | 1–2 | B→A | 2026083104 | 10,000 | E=2, C5=2, I5=0 |
| 3 | 152–177 | A→B | 2026083105 | 10,000 | E=2, C5=0, I5=2 |
| 3 | 152–177 | B→A | 2026083106 | 10,000 | E=2, C5=0, I5=2 |
| 4 | 316–326 | A→B | 2026083107 | 10,000 | E=2, C5=2, I5=0 |
| 4 | 316–326 | B→A | 2026083108 | 10,000 | E=2, C5=2, I5=0 |
| 5 | 4–131 | A→B | 2026083109 | 10,000 | E=2, C5=2, I5=0 |
| 5 | 4–131 | B→A | 2026083110 | 10,000 | E=2, C5=2, I5=0 |

Seeds 2026083111–2026083122 and pairs 6–11 were not executed.

## Outcomes

- E=0: **0/10**; E=1: **0/10**; E=2: **10/10**.
- E2 conflict-color split: **8 C5-only / 2 I5-only**.
- All ten E2 finals retained the known topology: two same-color conflicts with four shared vertices. No completed final had mixed colors or overlap at most three.
- The ten raw final graph6 files are distinct. Their 45 labeled pair distances range from 288 to 480, with median 439.
- The 48-move children had objective 158–175. Repairs ended 0–5 edges from the nearer aligned parent, so these trials returned to the parent basin rather than retaining an interior crossover state.
- Retained production artifacts total `104656` bytes, below the `20000000`-byte cap.

Neither preregistered hypothesis is adjudicated because only 10/22 jobs completed. All ten completed children repaired to E=2, but none produced the registered strict plateau departure.

## Verification and bindings

Every retained final was accepted during production by:

1. direct Python enumeration of all five-sets,
2. the separately compiled C++ graph/complement verifier, and
3. the independent path/crossover structural audit.

For this report, both graph verifiers were freshly rerun on all ten finals and reproduced the stored verifier JSON byte-for-byte; all ten stored structural audits remained accepted. The exact retained directory set and all 60 retained artifact hashes were also rechecked.

Key bindings:

- plan: `c9bdffd941e0d55ea15128d86b09113c7aa304e94ba9295af9babeca66224c7c`
- registration audit: `765be463a134c0e8b8b37bf5ccf8b01aa3ce588167c1e9cb16b06cdd5bf898ba`
- partial summary: `9aa63223f94c1972becb955f0a60d767464999de39ba87cc8062ecf989fcbf44`
- runner: `64cd3c9cc07f85b5e3505e04e9ae3bfa6060f8fb305f9a4bab7f676514373ff1`
- search source: `45a84256333c14be1eeea6cabb90ec839dd6a65ba56ddf5140281ac9aa698eb4`
- search binary: `d2f6f1eed61c5baa91cc909eb72701528af4ffe41d3161fe3b349923698179da`
- structural verifier: `34c6e8c1632f633a04e004b1547b5b99daacf930e8e95f8a6c905eccf51c1340`
- Python graph verifier: `fb8f5bee76f98a37a080970cd0548b88825f6f0f49f1144db20a3524ce5878b5`
- C++ graph verifier: `2ba9e189bc56b4d7c439b26317ade8eec60589c58e294bd26d7f35f4bd631f89`

The partial summary records every retained file path and SHA-256 digest.

## Claim boundary

**This run found no E=0 graph and therefore supplies no Ramsey construction. It left 12 registered jobs unexecuted and explored only a finite heuristic budget, so it supplies no proof—and no evidence—of nonexistence.**
