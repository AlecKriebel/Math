# Primary replay work log

All times below are Pacific time on 2026-08-24 unless stated otherwise.

## 20:55 — immutable-input and upstream-verifier audit

Scope was fixed to the 28 primary items in `input_frozen/specification/AUTONOMOUS_FINAL_PROGRAM.txt`. Supplied cloud scripts were executed unchanged before replacement work. The first run exposed missing Python packages; after the project-local environment was installed, every supplied primary script was run unchanged again. All nine exited nonzero for evidence or path reasons:

| Supplied script | Exact first-replay finding |
|---|---|
| `verify_model_domain_and_bridge.py` | All internal symbolic assertions reached the final write, which failed at hard-coded `/mnt/data/...`. |
| `verify_k3p_cut_transfer.py` | The required `jc_pointwise_cut_certificate_frozen.json` is absent. |
| `verify_tree_sunlet_separator.py` | `k3p_three_port_models.py` is absent. |
| `verify_three_port_geometry.py` | `k3p_three_port_models.py` is absent. |
| `verify_compiler_specialization.py` | The cloud K2P atlas/universe path is absent. |
| `verify_rooting_censuses.py` | `k3p_graph_map.py` and `rooting_census.py` are absent. |
| `verify_fourteen_orbits.py` | Its package-relative lock path is wrong locally and the cloud universe is absent. |
| `certify_sharpness_krawczyk.py` | Its original dependency stack and `sharpness_relative_root.json` are absent. |
| `verify_sharpness_extension.py` | Its package-relative certificate path is wrong locally. |

Decision: do not create replacement certificates by copying the stored conclusions. Rebuild from literal graphs and algebra where possible; otherwise leave the corresponding gate blocked.

Best-guess completion toward the primary-replay goal: **15%**.

## 21:28 — primitive exact replacements

Implemented project-local exact arithmetic that starts from the frozen formulas and literal graph records:

- inverse Fourier, principal-domain, CT-exponent, subdivision, and root-movement identities;
- three-sunlet maps in all orientations, six tree circuits, the eight-term quartic, its gradient, and exact Jacobian minors;
- the tree–double-theta collision over `Q[h]/(5h^4-1)`, including a newly selected nonzero rank-15 minor, tree rank 9, principal-domain interval bounds, and the 23-dimensional local-locus calculation;
- independent admissible-rooting enumeration for `W`, `Wprime`, and the collision graph;
- three-sector incidence anchor matrices and triple-sector product maps;
- all six source-rank minors, nine quartics, five directed-rank factorizations/minors, and two sink-swap quartics from literal four-port graph maps.

The double-theta replay certifies the exact rank-15 collision. It does **not** claim to regenerate the unstored tangent vector for the separate strict-CT perturbation; the gate report says so explicitly.

Best-guess completion: **82%**.

## 21:40 — orbit transport correction and adversarial cross-check

The historical H21 rejection was reproduced exactly. Its test used the rooted completion rather than the standard root-suppressed semi-directed mixed factor and interpreted target automorphisms in the wrong coordinate frame.

The project-local primary implementation now independently:

- root-suppresses every literal completion;
- retains arrowheads at reticulation endpoints;
- reconstructs all source and target mixed automorphism groups;
- reconstructs every required double coset in the correct relation-family frame;
- matches all 38 raw members across 14 canonical orbits; and
- verifies all 64-coordinate Fourier transports as exact literal-edge polynomial identities.

The separately implemented clean-room verifier was then executed as an adversarial cross-check. It passed all 14 orbits, 38 raw members, and two sink swaps. The primary replay does not substitute that clean-room Boolean for its own calculation.

Best-guess completion: **90%**.

## 21:50 — full one-command replay checkpoint

Command:

```text
bash reproducibility/verify_primary.sh
```

Result:

```text
PRIMARY_GATE_STATUS BLOCKED
PRIMARY_GATE_COUNTS pass=27 blocked=1 fail=0
```

The command executed the independent exact-rational Krawczyk replay and the independent topology/all-n replay, bound their executable and certificate hashes, and verified that the `sharpness/` tree was byte-for-byte unchanged. It likewise executed the corrected clean-room cross-check and verified that `clean_room/` was unchanged.

- Wall time: **35.16 seconds**.
- `/usr/bin/time -l` maximum resident set size: **94,109,696 bytes**.
- Internal Python peak-memory reading: **70,205,440 bytes**.
- Active transcript: `reproducibility/logs/primary_20260825T045030Z.log`.
- Machine report: `reproducibility/primary_gate_report.json`.

The only blocked item is primary item 6, pointwise cut recovery. The frozen K3P transfer record binds a JC primitive certificate with SHA-256

```text
b627df5b2dc8cf1eb21c2e08c974f9e54f5a0399043e4dd96ea95dc73c2c3350
```

but no file with that hash exists under `input_frozen/`. The missing object is not cosmetic: the supplied verifier expects 177 endpoint records and 453 single-blob records, including their exact sign certificates. Only aggregate counters and the absent-file hash remain. The JC manuscript explains the theorem but explicitly delegates the finite primitive cases to its exact package, so prose is not a substitute for those records.

Current strongest verified result: **27 of 28 primary gates pass; 1 is honestly blocked; 0 fail.**

Best-guess completion toward a fully passing primary gate: **96.4%**. Completion can reach 100% only by supplying the exact hash-bound JC certificate or regenerating its records from the missing primitive graph universe and then replaying all signs—not by copying the expected counters.

## 21:56 — deterministic final replay

Removed run-dependent timestamps, elapsed times, and live memory readings from the tracked machine report; those measurements remain in ignored per-run transcripts. The final replay again returned **27 PASS, 1 BLOCKED, 0 FAIL**, with no family errors. The input lock and all three auxiliary cross-checks passed, and both protected `clean_room/` and `sharpness/` trees remained byte-for-byte unchanged.

- Final replay wall time: **35.53 seconds**.
- Final replay maximum resident set size: **94,224,384 bytes**.
- Final replay transcript: `reproducibility/logs/primary_20260825T045606Z.log`.
- Stable report SHA-256: `8bdc4b6cea2eb895331295dd5cdc7f13a19f8d53f0ee89eb60e9394481525a04`.

No theorem promotion was made for item 6. The exact missing primitive certificate remains the sole gate to a fully passing primary replay.
