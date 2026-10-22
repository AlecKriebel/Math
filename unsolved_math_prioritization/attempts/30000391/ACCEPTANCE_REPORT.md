# Acceptance report for affine incidence matching

Problem 30000391, priority rank 1223; audit date 2026-10-10 UTC.

## Accepted result

Accept the positive finite-dimensional affine-spanning problem as settled by Farley's published 2022 Theorem 11. The affine-flat reduction is complete and preserves the target's exact direction, injectivity and incidence requirement. Arbitrary infinite point sets are covered in ZFC, without CH or a regular-cardinality restriction.

Record zero new mathematical proof turns. The disposition is a literature-based closure with an authored applicability certificate and an audit, not a new solution of Björner's conjecture.

## Scope qualification

The accepted self-contained statement must say that d is a positive integer. The original wording does not explicitly exclude d=0, and the literal d=0 instance with P=R^0 is false because there is no incident hyperplane. This is a boundary normalization, not a limitation on the infinite-cardinality result. Retain the explicit affine-spanning hypothesis. Do not claim infinite-dimensional, choice-free, measurable-matching, bijective-matching or disjoint-maximal-chain results.

## Checks passed

1. Original pages 51-52 and all inherited hypotheses inspected.
2. Farley's full nine-page primary article read; theorem number, incidence convention and finite-rank scope verified.
3. Closure lattice, rank d+1, singleton atoms and semimodularity established directly.
4. Coatom to P-spanned-hyperplane bijection proved, including the injectivity back-transfer.
5. Infinite-cardinality and degeneracy checks completed; d=1 settled and d=0 exception disclosed.
6. Internal proof checked at Lemmas 1 and 9, Proposition 10 and Theorem 11, including countable closure at singular cofinality and both final geometric cases.
7. Imported transversal-obstruction statement compatibility checked directly in the 1983 primary paper.
8. Three source PDF byte counts and SHA256 values verified against retained files.

## Acceptance limits

This is a complete applicability audit and an internal audit of the displayed Farley argument relative to its named external inputs. It is not an independent proof from set-theoretic foundations or a recursive re-proof of every cited theorem. The matching theorem, the old finite/rank-three/regular-cardinality results, and the general transversal results retain their literature attribution. No formal proof assistant or computational proof of the unrestricted theorem is claimed. Hash checks attest to source identity only, not mathematical truth.

No internal obstruction to the positive-dimensional application was found. The precise open issue from the 2006 problem is covered by the existing general theorem, so further original attack on this problem is unnecessary under the accepted scope.

## Suggested concise disposition

Closed by prior result for positive finite d: Farley, Australas. J. Combin. 82(3) (2022), Theorem 11. The affine closure lattice has rank d+1 and identifies its atoms with P and its coatoms with P-spanned hyperplanes. Full applicability checked; internal proof audited with explicit external-dependency limits. Literal d=0 excluded and documented. New proof turns: 0.

## Publication documents

- [APPLICABILITY_CERTIFICATE.md](APPLICABILITY_CERTIFICATE.md): complete affine-lattice reduction and scope analysis.
- [INTERNAL_PROOF_AUDIT.md](INTERNAL_PROOF_AUDIT.md): complete internal mathematical checks and the named external-dependency boundary.
- [SOURCE_LEDGER.md](SOURCE_LEDGER.md) and [SOURCE_LEDGER.json](SOURCE_LEDGER.json): public scholarly-source identities and the originating audit's retrieval and inspection history.
- [README.md](README.md), [STATUS.json](STATUS.json) and [MANIFEST.json](MANIFEST.json): scope, attribution, zero new proof-search turns, navigation and edition identity.
