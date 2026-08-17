# Reproducibility

## Corrected full release replay

From the corrected project root:

```bash
bash release/one_command_replay.sh
```

The command verifies all frozen source hashes; regenerates `data/current_profile_exact.json`; rebuilds the finite table, printed certificate tables, simulations, and figures; runs the generalized principal-minor theorem and all network-specific exact verifiers; compiles the manuscript, supplement, and external-audit documents; rebuilds every public and submission bundle; and writes the immutable release manifest.

The successful log must contain:

```text
NUMERICAL_PROVENANCE_PASS
MATRIX_THEOREM_GENERALIZATION_PASS
STABLE_DOMAIN_SCOPE_PASS
SCC_EXHAUSTION_PASS
OMISSION_MINOR_PASS
SYMBOLIC_CERTIFICATE_VISIBILITY_PASS
TABLE_REGENERATION_PASS
FIGURE_REGENERATION_PASS
SUBMISSION_BUNDLE_FRESHNESS_PASS
ALL_FINAL_RELEASE_REPLAY_CHECKS_PASS
```

## Portable public replay

```bash
cd public/repository
bash replay.sh
```

This replay has no dependency on the private source archives. It rebuilds all current-profile values and all-dimensional proof certificates from the portable sources. `FINAL_RELEASE_QUICK=1 bash replay.sh` is a smoke-test mode; the release qualification uses the full command.

## Single source of numerical truth

`data/current_profile_exact.json` is regenerated from the indexed reactions and current improved diffusion profile. Table 1, normal-form predictions, simulation metadata, figures, finite examples, and public demonstrations derive from this file. The mandatory regression is

```text
eta_3 = 143636/7451873
```

## Software environment

Python dependencies are in `requirements.txt`. PDF builds require `pdflatex`, `biber`, TikZ, `biblatex`, AMS packages, and Poppler utilities. Numerical integrations are deterministic cosine-Galerkin illustrations and are not used in any proof.
