# Audited partial analysis: 30001033

Mathematical disposition: **unsolved after five approaches**. No complete solution or novelty claim is made.

The `package/` directory preserves the original 12-file freeze byte for byte. The `audit/` directory preserves the separate independent audit and its checkers. The audit accepts every mathematical partial and identifies no required mathematical correction. These are historical snapshots: statements within them about pending review or preparation-time remote activity describe their original stage.

The strongest partials are the abelianization C4 × C12, exponent-two positive-index lower-central factors, all-index periodic leading-image lower bounds, and exact target indices at i=2 and i=3. The unresolved issue is vanishing of the excess kernels K_i for every i≥4.

## Release checks

Both independent mathematical checkers were rerun against this exact layout and their outputs matched byte for byte. The packaged controls also reproduced exactly, and all eight tests passed. The original package and audit checksum manifests remain valid.

Run from this directory:

```sh
python3 -B verify_release.py --negative-test
python3 -B audit/independent_checks.py
python3 -B audit/independent_finite_images.py
python3 -B package/test_controls.py
```

The release manifest covers only the safe mathematical package, the full audit and checks, and this release documentation. It excludes source PDFs, imported corpus data, private coordination, and repository-wide inventories. The negative integrity test alters a proof byte in memory and must be rejected.

## Queue scope

The only existing repository file changed is `unsolved_math_prioritization/QUEUE.md`. Only problem 30001033's Status and Turns cells are changed to `unsolved` and `5`. Its other cells, every other row, and the existing header are preserved byte for byte. No Findings cell or machine-state file is changed, and no queue-generation command is run. The audit's general administrative caution does not expand this explicitly limited release scope.

This is a draft pull-request checkpoint. It does not merge changes or create a release.
