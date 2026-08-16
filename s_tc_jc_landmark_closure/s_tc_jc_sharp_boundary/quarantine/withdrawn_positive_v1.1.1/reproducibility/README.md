# Reproducibility package

This version 1.1.1 archive accompanies *Generic Identifiability of Strongly Tree-Child
Level-2 Jukes--Cantor Networks*.

## Scope

The headline theorem concerns all binary standard semi-directed `S_TC`
level-2 networks under the open four-state Jukes--Cantor model, modulo ordinary
triangle redirection. The automatic triangle theorem, checked independently
in Python and C++, proves that every binary `W_TC` level-2 topology has at most
one triangle per blob. The underlying exact statistical release remains
hash-locked and is composed with this structural certificate. The structural
reconstruction output is a canonical class modulo triangle redirection, not an
input-specific list of every redirected stochastic model containing a fixed point.

## Commands

```bash
bash reproducibility/verify_quick.sh
bash reproducibility/verify_full.sh
```

The quick command verifies integrity, the automatic triangle theorem, the
hash-locked exact release, publication scope/count assertions, PDF build, and
component archives. The full command additionally regenerates the complete new automatic-triangle rooting universe in two independent implementations and validates every unchanged base algebra/statistical file against its preserved clean full-adversarial replay. `verify_regenerate_all.sh` is the slower from-scratch regeneration of every large signature stream, directed join, and relation universe.

## Environments

- `requirements.txt`: pinned Python packages used by the algebra generators.
- `environment.yml`: pinned Conda environment.
- `pyproject.toml`: package/tool metadata.
- C++17 and a LaTeX installation containing `latexmk`, TikZ, `biblatex`, and
  Biber are required for the full release replay.

See `RUNTIME.md` for measured resource use. SHA-256 manifests detect byte
changes only; exact regeneration and the written proof carry the mathematical
content.
