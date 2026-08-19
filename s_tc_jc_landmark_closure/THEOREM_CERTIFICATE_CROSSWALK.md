# Theorem-to-certificate crosswalk

Status: **v1.1.5 certificate bundle prepared; Zenodo DOI pending**

The authoritative computer-assisted proof object is
`stc_jc_sharp_boundary_atlas_certificates_v1.1.5.tar.gz`. All paths below are
relative to its extracted root. The broad development snapshot and historical
audit reports are provenance only and are not theorem dependencies.

| Article claim | Minimal exact evidence | Replay |
|---|---|---|
| Fixed mixed-graph convention, primitive supports, cut recovery, and full incidence-scaling bridge fibre | `primary/certificates/{core_universe,support_universe}.json`, `reviews/root_probe/`, `independent/bridge_cut/` | `bash verify.sh full` |
| Theorem 6.3: complete three- and four-outgoing directed relation universes | `atlas/ATLAS_INDEX.csv.gz`, bounded relation streams in `primary/certificates/`, four-outgoing gate and restoration streams indexed there | `bash verify.sh full` and `regenerate-all` |
| Restoration, arbitrary subdivisions, and coherent one-/two-port probes | `hard_cover_*` and `compact_probe_*` streams; `reviews/direct_anchor_probe_closure/certificates/` | `bash verify.sh full` and `regenerate-all` |
| Ordinary triangle common germ | `primary/certificates/jc_triangle_redirection_active.json`, `reviews/triangle_redirection_cleanroom/` | `bash verify.sh full` |
| Omega and Theta sharpness families | `omega_audit/independent/`, `s_tc_jc_sharp_boundary/reproducibility/` | `bash verify.sh full` |
| Bundle integrity, relation totality, deterministic regeneration, and mutation sensitivity | `ACTIVE_MANIFEST.json`, `SHA256SUMS`, `atlas/ATLAS_INDEX.csv.gz`, `expected_outputs/`, `verifiers/package_mutation_tests.py` | all three modes |

The per-relation index has 10,466 three-outgoing rows and 192 four-outgoing
survivor rows. Every row names its certificate, transport (when applicable),
and verifier. The archive excludes referee prose, research logs, superseded
claims, manuscripts, and release-engineering workspaces.

## Explicit exclusions

No active theorem uses a reciprocal-only bridge chart, a hidden cleanup-fibre
rooting convention, a weak-class gadget as a move in the strong class,
target-only counts, equality of complete stochastic images under ordinary
triangle redirection, physical bridge-parameter recovery, or K2P/K3P claims.
