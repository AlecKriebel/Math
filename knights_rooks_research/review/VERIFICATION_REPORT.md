# Independent verification report

17 September 2026 UTC / 16 September 2026 US Pacific.

**Verdict: verified; no mathematical or computational issue requiring correction
was found. The supplied package can be published with its exact stated scope.**
This is an independent AI-assisted audit of the supplied work, not external
human peer review or a proof-assistant formalization.

## Exact result

Let K and R be finite, nonempty, disjoint subsets of the ordinary integer grid,
containing only knights and rooks, respectively. Rook attacks terminate at the
first occupied square in each orthogonal direction. If each rook attacks exactly
two knights and no rooks, some knight attacks at most three rooks. Knight-to-knight
attacks need not be forbidden.

The theorem therefore rules out the N=4, R=2 cell in the Knights and Rooks table
of [Friedman's February 2007 Math Magic page](https://erich-friedman.github.io/mathmagic/0207.html).
It does not resolve the other open cells on that page. The source still displayed
`?` for this cell on this audit date; that fact does not establish priority.

## Independent routes and evidence

| Route | Mechanism | Evidence and status | Remaining gap |
|---|---|---|---|
| Geometric proof | Rightmost knight, forced rooks/blocking knights, empty rays, final degree contradiction | Every coordinate and implication checked independently; valid | None for the stated finite model |
| Necessary local relaxation | Restrict to 28 squares while retaining only necessary constraints | All distinguished knight neighborhoods complete in the nonempty half-plane; outside continuation cannot invalidate retained restrictions | None for the reduction |
| Independent Boolean audit | Reconstruct clauses from coordinates, residual-clause proof check, fresh unit propagation | Exact multiset match for 174 variables / 699 clauses; 728 gadget truth assignments; supplied 151-step certificate and new 222-step certificate both verify | None for the encoded obstruction |
| Computational reproduction | Replay tests, regenerate certificate, third attack reconstruction, integrity checks | 20 tests pass; all 74 original file digests match; stored calibrations and reports reproduced | Earlier exploratory solver runs were not rerun and are not needed |
| Public presentation | Compare original source, manuscript variants, PDF and website claims | Six PDF pages visually checked; exact cell, finite scope, and internal AI audit limitations stated | Historical priority and external peer review remain unestablished |

The reviewers worked separately before their findings were integrated. Their
reports explain the deductions rather than asking the reader to trust a verdict:

- [Geometric referee report](geometric_referee.md).
- [Encoding referee report](encoding_report.md).
- [Reproduction referee report](reproduction_referee.md).
- [Publication context](PUBLICATION_CONTEXT.md).

The main proof stands independently of every program. Its key force is that a
rook already seeing two knights must have its other rays entirely empty: any
additional nearest piece would be a third knight or an impermissible rook. No
reciprocal incidence-count assumption, fixed board size, extra piece type,
checkerboard restriction, or assumed global reflection symmetry enters the proof.
Finiteness justifies choosing an extremal knight; translated/rotated placements,
disconnected components, and ties for the extremal coordinate cause no gap.
Empty placements, toroidal boards, and unrestricted infinite configurations are
outside the claimed model.

## Reproducible checks

From the `knights_rooks_research` directory, using Python 3.9 or newer:

```sh
python3 src/run_all.py
python3 review/encoding_independent.py
python3 review/reproduction_artifacts.py
python3 src/verify_unsat.py certificates/local_relaxation.cnf review/encoding_fresh_proof.json
```

The first command is the original standard-library suite. The encoding audit
imports no package code. It independently reconstructs all clauses, verifies each
Boolean gadget, checks the original certificate, derives another proof with a
different inference order, and rejects 153 corrupted certificate variants.
The additional reproduction script compares stored data with independently
reconstructed attacks and regenerated artifacts. Review scripts may update their
own result files; original supplied files remain unchanged.

Original certificate: 3 nodes, 1 split, 151 unit steps, 2 conflicts.
New independent certificate: 3 nodes, 1 split, 222 unit steps, 2 conflicts.
The fresh proof is also accepted by the original checker.

CNF SHA-256:
`991d45763d7e62b35ddedc7af5040cf93ef5e83b9b7b02340bbdb53da6930f10`.

PDF SHA-256:
`b36f1b9632553b9cf415fe6a6c230bd10b0165a9a6240480e70c90a87b46a640`.

## Preservation and publication decision

No correction to the supplied mathematics, code, data, or PDF was necessary.
All original package bytes are preserved. `MANIFEST.sha256` continues to cover
only the original 74 files, excluding itself. This report, the other review
materials, and `RESEARCH_LOG.md` document the later verification separately.
Historical references to the original conversation and unpublished status should
be read in that original-session context.

Publication is authorized to the existing AlecKriebel/Math repository on main,
with a new top-level `knights_rooks_research` folder and a GitHub Pages entry at
`papers/knights-rooks-n4-r2/`. No GitHub release or immutable DOI snapshot is
needed for this publication. No individual was contacted on the project's behalf.

The final public-scope review requested the word "nonempty" in the short website
statements. It was added before publication. The full theorem already stated this
hypothesis; this was a public-summary clarification, not a proof correction.
