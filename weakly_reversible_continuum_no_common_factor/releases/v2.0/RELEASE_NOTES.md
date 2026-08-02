# A four-parameter family of reversible mass-action equilibrium continua

Version 2.0.0 strengthens the frozen Version 1 theorem without altering its
immutable files. On the same reversible, one-linkage, three-species support,
the rate vectors preserving the displayed positive ellipse form an exact
four-dimensional rational linear space. Its strictly positive part is a
relatively open rational polyhedral cone, and the coordinate vector field is
geometrically gcd one on a nonempty Zariski-open subset of that family.

This release also adds:

- the complete `21 x 20` conic-remainder matrix of rank `16` and an exact
  four-parameter rate formula;
- a primitive positive integer specialization with largest rate `10296` and
  rate sum `52464`, proved simultaneously optimal for both objectives within
  this fixed support and conic-preserving integral family;
- exact radical decompositions for both displayed specializations;
- an exact transverse-stability classification for the frozen Version 1
  ellipse;
- global three-species minimality, a one-linkage rank-two obstruction, and a
  five-complex lower bound;
- four exact replay layers, including a substantively independent 993-line
  audit; and
- a conservative post-solution primary-source audit and specialist audit
  packet.

The continuum-preserving family has codimension sixteen in the ambient
twenty-dimensional rate space. The generic gcd-one statement is relative to
that constrained family; this release does not claim persistence under
arbitrary rate perturbations or global minimality of the ten-complex support.

## Reproduction

Download the complete archive, extract it, and run:

```sh
./reproduce.sh
```

The script creates a locked local Python environment and replays every exact
verifier. SHA-256 manifests accompany all release assets.

## Publication and citation

- Version: `2.0.0`
- Repository tag: `wr-continuum-v2.0.0`
- Publication date: 2 August 2026 UTC (1 August 2026 PDT)
- Version 1 DOI: `10.5281/zenodo.21753527`
- Repository-level Zenodo concept DOI: `10.5281/zenodo.21753404`

Publishing this GitHub release triggers the repository's automatic Zenodo
archive. The Version 2 DOI will be added here after Zenodo mints it. Because
the integration operates at monorepo scope, the concept DOI above groups
unrelated releases and is not a paper-specific all-versions identifier.

The DOI and repository tag establish a citable public disclosure date. They
are not peer review or a correctness certificate.

## Priority scope

Boros, Craciun, and Yu already supplied a positive-dimensional fixed-support
same-curve rate family, but every member retains a common scalar factor. In a
targeted primary-source audit through 1 August 2026, we found no earlier
weakly reversible fixed-support positive family preserving a compatibility-
class continuum while being generically free of a coordinate common factor
within that family. This is a conservative search report, not an exhaustive
worldwide priority claim.
