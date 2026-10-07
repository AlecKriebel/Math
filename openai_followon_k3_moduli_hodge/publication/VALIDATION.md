# Validation basis and limits

The self-contained argument in this note is the rational correspondence
transfer. It is not an independent proof of the underlying mixed-K3 result.
No formal verification of the full theorem is claimed.

## Checkable transfer

For A in CH^a(V x W), the action shifts (p,p) to
(p+a-dim V,p+a-dim V). Composition with B in CH^b(W x V) has codimension
a+b-dim W. The Chow diagonal splitting gives a+b=dim V+dim W, so the
return cycle has codimension p. Exterior products of split maps compose
to the product diagonal. No Tate-sign convention is needed. Empty and
zero-dimensional varieties, zero targets, repeated bases and S^[0] and
S^[1] are explicit. The independent Bülles audit checks the exact theorem
scope and normalized non-fine/twisted construction.

## Upstream source-proof audit

The source ledger identifies the complete chain: relative immersed
realization and ordinary categorical recovery, semiregularity, exact
full-Clifford KS, auxiliary spin tensors, joint mixed Hodge-group invariants,
and the full CM-abelian Hodge theorem. Multiple auditors checked distinct
parts, against primary cited statements where pivotal. Early reports retain
the dependencies outside their individual scopes. An individual favorable
report does not certify the whole chain. Complete-package review and final
reconciliation are recorded separately with exact package hashes.

The relative analytic audit includes a detailed colored quasi-component
extension proof and actual reference-hypothesis matching, reciprocal corners,
ordinary child outputs, empty external words, Stokes, lattice/cost filtration,
ultraproduct/copy limits, saturation and proper Serre projection. It explicitly
excludes topology, ordinary HMS/generation and semiregularity, which require
the separate geometry/algebraic checks. The root arithmetic audit and the
independent theta/Satake audit together cover the initial CM proof slices;
fresh arithmetic falsification and package review assess their reconciliation.

## Reproducible finite checks

- Local spin Hom pairing over Q: full rank four, torus-line projection rank
  two. This verifies a matrix identity, not algebraicity of the spin tensor.
- Graph sign relations: all 11,894 simple-graph cases on up to four vertices
  with torus subsets/signs, plus 16 parallel-edge cases. The general argument
  is the path-product proof in the audited source, not finite enumeration.
- Realization algebraic parity checks: 32 branch parity, 1,600 product
  orientation parity, 79 block parity cases. These do not construct analytic
  determinant orientations or moduli spaces.

Exact scripts and expected outputs are in `checks/` in the source archive.
They use only Python's standard library and fail on any mismatch. The
reproduction runner verifies source hashes, executes them in a clean
directory and compiles the standalone paper. A successful runner certifies
these finite computations and the build, not the upstream Hodge theorem.

No conventional human peer review has occurred. The actual upstream Lean
scope is recorded in FORMAL_SCOPE.md; its Clifford identities neither
formalize algebraic cycles nor certify the main result.
