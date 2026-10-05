# Validation scope and replay

The default finite suite passes 900 explicit assertions. It computes exact rational and finite-field homology of the binary level posets for one through five levels, verifies the integral square/cone chain identity, checks all identity-zero monoid tables on up to three elements, checks 52 surjective homomorphisms between those tables, verifies the finite-group failure of naive center covariance, and tests the indicated endomorphism-operad arities for sets of sizes one and two.

The universal proofs are in `PROOF.md`. Field-rank tests alone would not certify integral homology; the cross-polytope boundary identification proves the integral statement. The suite does not compute the homotopy center in the problem, the free E2 algebra's full homology, or any general derived mapping space. The free-algebra argument is a mathematical proof, not a numerical simulation.

`RESULTS.json` is the deterministic default output of `python3 verify.py`.
`EXTERNAL_REPLAY.json` records the run with all three optional complete-corpus inputs. That run adds identity/hash assertions, for a total of 916 assertions. The external inputs are deliberately absent from the public packet, so reproducing that particular source check requires separately obtaining the matching authorized files. Default mathematical replay requires none of them.

Example optional invocation:

```sh
python3 verify.py --external-catalog /your/catalog.json --external-problems /your/problems.json --external-research /your/research_results.json
```

These local inputs are read only. Their contents are never copied into the output.

The frozen manifest lists exact relative filenames, sizes, and SHA-256 values. Its own trusted digest is supplied with the archive, outside the manifest. Run:

```sh
python3 verify.py --manifest MANIFEST.json --expected-manifest THE_SUPPLIED_DIGEST
```

This replay rejects a changed file, missing file, extra file, symbolic link, unlisted directory, unsafe manifest path, or wrong manifest digest. Integrity checks certify bytes relative to that trusted digest; they do not certify mathematics or author identity.

The packet was also replayed from a fresh relocated directory, with default output identical. Publication negative controls exercised changed and missing files, an extra file, an unlisted directory, and an incorrect trusted digest. Their results are recorded in the external freeze receipt. No source corpus or PDF is needed for those checks.

The primary report was checked against two byte-identical public PDF copies. Source inspections are limited to the locations listed in `SOURCE_VERIFICATION.json`; the packet makes no claim to have independently reproved every cited theorem. A separate adversarial mathematical audit is pending at this checkpoint.
