# Second independent adversarial review

## Disposition

**Accept the forward counterexample mathematically, and accept the complete two-part answer after the separate converse-scope clarification.** This is one independent review; the surrounding project must separately satisfy its two-review gate. No claim of publication, established novelty, formal proof-assistant verification, or author-approved correction to the literature is made.

The proposed CM eightfold exists, is simple, has all powers Hodge-Lefschetz, and has a geometrically simple characteristic-five reduction with endomorphism field E. The reduction has non-Lefschetz codimension-two Tate classes. Independent finite enumeration sharpens the obstruction to a four-dimensional quotient: Tate H^4(2) has dimension 32 and its divisor-generated part has dimension 28, over every Q_l with l different from 5.

The only correction required for the literal two-part response is to exhibit a class of A, rather than relying exclusively on a class of pairs (A,prime), in the converse. `CONVERSE_SCOPE.patch` adds CM elliptic curves, for which the consequent holds at every prime, and keeps the stronger prime-dependent theorem clearly separated. It also adds Conrad's independently checked source for the local formula. The mathematical construction and the author's finite certificate are unchanged.

## Independence and evidence

The frozen proof, exact OWR contribution, relevant source theorems, and all geometric steps were independently assessed. The first audit was not consulted. After the core assessment began, the coordinating reviewer asked about the converse quantifier issue; that issue was checked against the original OWR text and resolved by an independently supplied elementary proof.

`INDEPENDENT_LEMMAS.md` records the actual derivations, including the local coset orientation, every-extension endomorphism argument, rational descent, and the literal converse. `independent_check.py` uses root permutations, prime cosets, an independent determinant expansion, and exhaustive exterior-basis enumeration. It does not load or import author code. It also exhausts compatible CM types, strengthening the published-conflict diagnosis.

The reviewed original is pinned by these hashes:

- Author ZIP: 32f5ec9f310f62566906cf6b0ff4a1e8cef5a6e9442ecb995c91525a1fb9879e; 14,326 bytes.
- Author external manifest: 24d868b99bd75c586313062c107bb6d6b1f2f5d5efb939f17d1401e1da6c8212.
- Author bootstrap: 897a75796bef8d980a0c12808a21ddd9a71cefa7dbf54bd6cf12c8f14ad2d6a5.

## Mandatory literature gate

The unrestricted statement of Angle ranks Remark 3.5 conflicts with the construction. No stated ordinary or special-lift hypothesis was found. The local averaging formula is valid, but it does not imply equal centered ranks. The rank computation and geometric realization establish a genuine counterexample to that inference, rather than merely an unexplained numerical inconsistency. In this precise sense this review discharges the mathematical conflict gate.

The final cited CCO proposition and the original Dodson PDF remain uninspected. This is a source-access limitation, explicitly retained in the report and metadata. It does not leave a necessary proof theorem unsupported: the formula and actual hypotheses were checked in Milne's two works and Conrad's original notes. Do not describe the original CCO or Dodson passages as verified, and do not call this a published erratum.

## Execution acceptance

The externally pinned original bootstrap passed 26 independently replayed controls: normal and optimized clean launches from hostile working directories and PYTHONPATH, relocation, rejection of injected import/startup modules, cache directories, changed entrypoints, changed proofs, root/member/manifest symlinks, an internal manifest, a changed external manifest, and an unrecognized entrypoint selector. No hostile marker executed in these trusted runs. The first harness attempt hit copied read-only file permissions before mutation; only disposable copies were made writable, and the complete controls were replayed successfully.

The trust claim is bounded. It assumes the pinned bootstrap, a trusted Python interpreter and standard library, and no concurrent replacement after hashing. It is not a sandbox against an attacker who controls the interpreter, OS, or same-user races. The bootstrap verifies extracted-member bytes and strict inventory before execution; its manifest's ZIP record is independently checked by this review rather than interpreted as a self-authenticating archive guarantee.

`AUTHOR_ACCEPTANCE.json` records all original-packet controls. `PATCH_ACCEPTANCE.json` records fresh application of the correction to a copy, byte matching, a separately pinned corrected packet, normal/optimized replays, independent-checker results, and final immutable-original verification. A changed proof is not passed off as the original freeze.

## Safe scope

The review bundle contains authored mathematical analysis, the authored patch, an independent finite checker, acceptance results, and bounded public-source metadata. It contains no third-party PDF/text, raw datasets, private sources, or private coordination files. This review performed no repository publication or external communication.
