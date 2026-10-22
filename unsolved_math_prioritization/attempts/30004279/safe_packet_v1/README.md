# Problem 30004279: partial research packet

Original target: Henriques's 2019 conjecture on nonisomorphic conformal nets whose associated bicommutant categories are tensor equivalent.

## Result

Unresolved after five substantive approach units. No full candidate, new counterexample to the original target, verified prior resolution, or novelty claim.

The retained work establishes necessary conditions and rules out shortcuts:

- Equal Drinfeld centers alone do not reconstruct a bicommutant category, even in the holomorphic setting.
- Holomorphic central-charge-8 tensor powers give nonisomorphic nets with equal representation categories, but their full soliton-category equivalence is still missing.
- The Henriques–Penneys Morita theorem requires a fusion-commutant realization that has not been supplied for those nets.
- An ambient-factor isomorphism works only if it also preserves the precise normal-extension predicate defining solitons.
- Proper solitons form an uncountable family; matching object labels or fusion rules leaves essential-surjectivity and tensor-coherence gaps.

Read PROOFS.md for statements, complete retained deductions, explicit external inputs, and exact residual gaps. Read SOURCE_VERIFICATION.md before interpreting the scope of the search.

## Verification

Python 3 standard library only:

    python verify.py
    python verify.py --output /tmp/bicommutant-checks.json
    cmp checks.json /tmp/bicommutant-checks.json

The checker has 47 exact assertions for E8 lattice arithmetic, S3 characters, and a Z/2 associator obstruction, with negative controls. It does not verify operator-algebraic theorems, build a conformal net, or certify an equivalence. A byte-for-byte replay passed. No numerical search is being substituted for proof.

## Source and review limits

Original OWR contribution and seven relevant papers were retrieved privately and inspected at the named sections. The exact live target page returned HTTP 403. Raw dataset statements and prior AI reports were not available to this worker and were not inspected. A September 2026 thesis was found but its full PDF was inaccessible; its abstract does not settle the target. No global openness or exhaustive-literature claim is made.

This packet contains only authored notes, source-verification metadata, code, exact check output, status/log, and a manifest. It excludes source PDFs, extracted text, images, raw dataset records, and private coordination material. No remote writes, queue changes, or publication were performed. Fresh independent mathematical audit and the parent publication gate are still required.
