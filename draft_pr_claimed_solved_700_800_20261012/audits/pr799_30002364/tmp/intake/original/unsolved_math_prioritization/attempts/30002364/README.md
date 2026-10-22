# CM reduction: an eightfold counterexample candidate

Problem 30002364 / OWR-12495-004, queue rank 841. Dated 6 October 2026.

**Current disposition: complete two-part candidate accepted by two independent AI mathematical audits; unrefereed.** The queue label `claimed_solved` records this project assessment, not human peer review, formal verification, a novelty finding, or an accepted correction by the cited authors. All five substantive approaches are exhausted and preserved in the original status record.

## Result and limits

The forward construction gives a simple CM eightfold over the algebraic numbers whose every power has only divisor-generated Hodge classes, but whose geometrically simple reduction in characteristic 5 has non-Lefschetz codimension-two Tate classes. Its CM field is the degree-16 Galois field E = L(i), where L is the splitting field of X^4 - 6X^2 + 3, with group D4 × C2. The centered Hodge and slope ranks are 8 and 4; geometric End^0 of the reduction remains E. The two audits independently find Tate H^4(2) dimension 32 and divisor-product dimension 28, over every Q_l with l ≠ 5.

The literal existential converse has an elementary affirmative variety class: CM elliptic curves, uniformly at every reduction, since the characteristic-zero conclusion already holds for every power. This is not a new converse theorem. The separately stated complete-splitting result concerns specified (variety, prime) pairs and is attributed to Sugiyama. No unrestricted pointwise converse is asserted.

Non-Lefschetz does not mean nonalgebraic. This is not a counterexample to the Hodge or Tate conjecture, and it makes no claim about numerical equivalence.

## Read the operative argument and reviews

- [Scope-corrected proof](corrected/PROOF.md)
- [First independent mathematical audit](audit_one/MATHEMATICAL_AUDIT.md) and [exact-byte acceptance](audit_one/ACCEPTANCE.json)
- [Second independent review](audit_two/REVIEW.md), [independent lemmas](audit_two/INDEPENDENT_LEMMAS.md), and [patch acceptance](audit_two/PATCH_ACCEPTANCE.json)
- [Aggregate current verdict](VERDICT.json)
- [Exact original-to-corrected patch](audit_two/CONVERSE_SCOPE.patch)

The original five-file author archive is preserved verbatim. The corrected archive changes only PROOF.md: the literal converse class and the independently inspected Conrad citation. The other author files, plus pre-audit language preserved in the proof, are historical records. This README and VERDICT.json record the aggregate disposition after both reviews. The two audit archives and all original external manifests, bootstraps, and receipts are also preserved verbatim.

## Literature conflict and source limitations

The authored argument and both AI audits explicitly challenge the unrestricted lift equivalence in Dupuy–Kedlaya–Zureick-Brown, *Angle ranks of abelian varieties*, Remark 3.5 ([arXiv version](https://arxiv.org/abs/2112.02455v3), [journal](https://doi.org/10.1007/s00208-023-02633-7)). Local averaging preserves neither the centered orbit rank (8 versus 4) nor the corresponding weight-inclusive dimensions (9 versus 5). The construction retains absolute simplicity and is not supersingular; no ordinary or distinguished-lift hypothesis was found in the inspected statement. This is an authored correction claim, not an author-approved or published erratum. No claim of priority or established novelty is made.

The final Chai–Conrad–Oort Proposition 2.1.4.2 and original Dodson PDF were not retrieved. The necessary averaging formula and its hypotheses were independently checked in [Milne's CM notes](https://www.jmilne.org/math/CourseNotes/CM.pdf), [Milne 2001](https://www.jmilne.org/math/articles/2001aP.pdf), and [Conrad's original notes](https://math.stanford.edu/~conrad/vigregroup/vigre04/stformula.pdf). Their text and PDFs are not redistributed.

## Reproduce the finite acceptance checks

Use trusted Python 3 and the external manifest and wrapper SHA-256 pins from the exact-head PR acceptance receipt. The hashes must be obtained independently of an untrusted checkout. Before executing the wrapper, verify its exact bytes against WRAPPER_SHA256 with a trusted local hash utility, and reject any symlink in its path. The self-check is not a substitute for this independent pre-execution check. From any working directory:

    python -I -S -B /absolute/path/verify_publication.py /absolute/path/package MANIFEST_SHA256 WRAPPER_SHA256 --execute
    python -I -S -B -O /absolute/path/verify_publication.py /absolute/path/package MANIFEST_SHA256 WRAPPER_SHA256 --execute
    python -I -S -B /absolute/path/test_publication.py /absolute/path/package MANIFEST_SHA256 WRAPPER_SHA256

The operative launcher authenticates itself, its external manifest pin, the strict complete file/directory inventory, all four immutable archives, all 30 extracted members, and both exact corrected-proof acceptances before executing any packet code. It rejects symlinks, caches, extra files, missing files, changed code, changed metadata, or changed archives. Each finite checker then runs as an isolated subprocess with `-I -S -B`, with `-O` in optimized mode. Tests also replay the frozen bootstraps and first auditor's original 23-case harnesses; those historical launchers retain their original `-I -S` child semantics. They are not silently changed to claim a stronger original launch mode.

The publication tests exercise normal/optimized launches, relocation to paths with spaces, hostile working directories/PYTHONPATH, mutation rejection, and actual zero-fuzz patch application, checking all five reconstructed files against the corrected archive. [Stored results](PUBLICATION_TEST_RESULTS.json) are finite execution evidence, not a mechanized geometric proof. Authenticate the test script before running it, using the operative launcher without `--execute`.

The trust boundary assumes the external pins, a trusted interpreter and standard library, and no concurrent filesystem replacement after hashing. This is an integrity check, not a sandbox against a compromised OS or same-user races.

## Publication scope

Only authored mathematics, code, audits, acceptance records, immutable safe archives, and bounded public verification metadata are included. No copied scholarly source text/PDF, dataset contents, private source, personal data, or private coordination file is distributed. The queue changes only row 841's Status, Turns, and Findings; all other queue bytes are preserved. No merge, release, DOI, or outreach is part of this publication.
