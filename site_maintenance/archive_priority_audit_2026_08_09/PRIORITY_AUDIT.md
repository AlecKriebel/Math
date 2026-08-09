# Refreshed priority audit for archived Discoveries 03, 05, and 06

Audit date: **9 August 2026**.

This is a documented, source-bounded audit. It is not a guarantee of
worldwide priority and does not independently validate any mathematical
claim. Private, unindexed, deleted, or simultaneously released work may be
missing.

## Scope and method

The audit compared the three Discovery entries formerly shown in the public
Archive and provenance section against:

- the exact Git history and original public-release timestamps in this
  repository;
- the primary predecessor commits already identified in the July audits;
- refreshed exact-phrase and variant searches across arXiv, Zenodo, GitHub,
  and the open web; and
- current archival records for later work that supersedes a quantitative
  headline without changing priority at the original release date.

The audit distinguishes an **earlier predecessor** from a **later
superseding result**. Those are not the same priority conclusion.

## Findings

| Artifact | Original release | Earlier same or stronger public result? | Current status |
|---|---|---|---|
| Discovery 03, 22/44-variable construction | 21 July 2026, 14:42:57 UTC | Yes for component claims: Cassidy had the equivalent six-variable symmetric transport; Thompson had the executed rank-compression principle; Mikhail Szh had the stronger full-family monodromy theorem. No earlier source was found for the residual executed 22/44-variable certificate. | Component novelty corrected; whole artifact superseded internally by Discovery 07. |
| Discovery 05, `SIC(21)` | 22 July 2026, 02:59:33 UTC | No earlier explicit `SIC(n)` witness for `n <= 21` was located. | Superseded internally by Discovery 07's `SIC(14)` and externally, later, by van Rijn's `SIC(3)`. |
| Discovery 06, 14-variable unipotent map and `SIC(14)` | 22 July 2026, 14:26:12 UTC | No earlier source for the exact map, fiber, and every-exponent formula was located. | Superseded internally by Discovery 07; its SIC dimension headline was externally superseded later by van Rijn's `SIC(3)`. |

## Primary predecessor records for Discovery 03

- Eliott Cassidy,
  [commit `40e1e20f`](https://github.com/eliottcassidy2000/math/commit/40e1e20f9ee113245f8e4e4b22ecd798fa1ffbfc),
  authored **20 July 2026, 14:46:10 UTC**. The commit message and artifact
  record an executed six-variable de Bondt--van den Essen/Meng transport,
  symmetric Jacobian, and the same lifted three-point fiber.
- William Thompson,
  [commit `45a7616f`](https://github.com/wtho704/explicit-cubic-homogeneous-jacobian-counterexample/commit/45a7616fdf5a20c065564f2676190093722696b9),
  authored **21 July 2026, 03:29:42 UTC**. It gives an executed 24-variable
  cubic-homogeneous rank-compressed reduction.
- Mikhail Szh,
  [commit `f8a6d679`](https://github.com/MikhailSzh/weighted-lift-galois/commit/f8a6d6794febb551050d73b8cf6ffab9da52d047),
  authored **21 July 2026, 04:03:36 UTC**. It proves the stronger full
  `S_n` monodromy statement for Gallagher's weighted-lift family.

All three predate the applicable Kriebel releases. The individual Discovery
03 audit and public paper had already corrected these points; the refresh
reconfirmed them.

## Later external supersession of the SIC dimension records

Roy van Rijn's *A Four-Term Counterexample to the Special Image Conjecture in
Three Pairs* was deposited on Zenodo on **28 July 2026 at 01:06:41 UTC**:

- [archival record](https://zenodo.org/records/21634058)
- [DOI `10.5281/zenodo.21634058`](https://doi.org/10.5281/zenodo.21634058)

The paper proves `SIC(3)` false with

```text
f = tau (t-y) (w z + v t),    g = y,
```

and gives a nonzero closed formula for the multiplier obstruction at every
positive exponent. Because this appeared after Discoveries 05 and 06, it is
not prior art against their original timestamps. It does, however, supersede
their dimension-21 and dimension-14 quantitative headlines.

## Bottom line

- Discovery 03 contains externally preempted components, already corrected,
  and no refreshed evidence of an earlier residual 22/44-variable
  certificate.
- Discoveries 05 and 06 were not found to duplicate an earlier explicit SIC
  result at their release times.
- All three are technical precursors rather than current papers.
- The current public-facing records now say explicitly where supersession is
  internal, where it is external, and whether the external result was earlier
  or later.
