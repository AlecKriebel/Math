# Independent audit of prescribed boundary zero sets

Problem **2305029 / AMR-022-5029**, rank **1035**, Hayman Problem **5.29**.  
Audit date: **2026-10-08 UTC**.  
Verdict: **ACCEPT the prior affirmative solution, conditional on the explicitly imported published theorem.**  
Substantive new research turns: **0**. Mathematical correction required: **none found**.

This report independently reviews the seven-file acceptance packet, its mathematical deduction, source conventions, and finite integrity controls. It does not claim a new solution, an independent proof of every imported result, or a computational certificate for an analytic existence theorem. The original seven files were preserved byte for byte.

## Exact scope and direct deduction

The target quantifies over every arc-length-null relative G_delta set E in the unit circle T. It requires a bounded holomorphic function in the open unit disk D, not identically zero, whose boundary limits exist at every point and vanish on E. It requires inclusion of E in the boundary zero set, not equality. Arc length and its normalized version have the same null sets.

Danielyan's published page 813 defines Fatou points through radial limits. Theorem 1 supplies an H-infinity function with positive real part in D, radial limits everywhere, and radial zero set exactly the prescribed null G_delta. [D]

Set F = E in that theorem. Its set hypotheses match the target without strengthening. Its function belongs to the requested space; Re f(0) > 0 proves nontriviality. Equality of zero sets implies the required inclusion. For E empty, the constant function 1 independently handles the target.

No closedness, countability, or logarithmic-capacity condition is used. A null G_delta can be dense and uncountable. For example, choose dense open sets of successively smaller arc length and intersect them. Their intersection is comeager and, by Baire's theorem, dense, while the measure bounds make it null; it cannot be countable because countable sets are meager in T. Thus restricting to closed sets would discard genuine cases.

Hayman–Lingham's own Update 5.29, immediately following the problem on printed page 95 / PDF page 96, credits an affirmative solution. Reference 181 identifies the 2016 published article. The earlier imported assessment that the problem remained open in the 2018 source is therefore contradicted by that source itself. [H]

## Primary proof and dependency audit

The complete short primary proof was read, including Kolesnikov's imported Lemma 2. The compact-uniform series estimate is summable. At prescribed points, positivity lets finite partial sums force divergence of the real part. Elsewhere, nested neighborhoods give uniformly summable radial tails. The reciprocal has a denominator with real part bounded below by 1, so its finite complementary limits remain nonzero. These steps introduce no hidden closed-set restriction. [D]

Acceptance imports Danielyan's Theorem 1. Inspection of its proof does not independently establish Kolesnikov's lemma. The primary bibliographic record for that dependency was checked, but its complete proof was not reconstructed. [K] The separate normal-family argument below uses Montel's theorem and the identity theorem, also as standard imported results.

The subsequent corollaries and the paper's application to nonexistence sets of radial limits are not needed for this acceptance. No claim about their independent verification is made.

## Independent boundary convention verification

For bounded holomorphic functions, a finite radial limit at a boundary point implies the same finite nontangential limit there. The acceptance packet's argument is valid; the following rederivation spells out its sequential step.

Rotate the boundary point to 1 and define F(w) = f((w-1)/(w+1)) on the right half-plane. The radial assumption gives F(t) -> L for positive real t -> infinity. For any positive sequence t_n -> infinity, the functions F_n(w) = F(t_n w) are uniformly bounded. Montel's theorem gives a locally uniformly convergent subsubsequence from every subsequence. Any such limit equals L on all positive real w, since t_n w -> infinity there. The identity theorem forces that limit to be identically L. Consequently the entire sequence F_n tends locally uniformly to L: a failure on a compact set would provide a subsequence with a fixed positive discrepancy, contradicting its convergent subsubsequence.

Now suppose z_n -> 1 with |1-z_n| <= C(1-|z_n|). Put w_n = (1+z_n)/(1-z_n) and t_n = Re w_n. Direct algebra gives

    t_n = (1-|z_n|^2)/|1-z_n|^2
        >= (1+|z_n|)/(C|1-z_n|) -> infinity,

    |Im w_n|/t_n = 2|Im z_n|/(1-|z_n|^2)
                 <= 2C/(1+|z_n|).

Thus w_n/t_n lies on a fixed compact vertical segment with real part 1 for all sufficiently large n. Local uniform convergence implies

    f(z_n) = F_n(w_n/t_n) -> L.

Every nontangential sequence has this property. The converse is immediate because a radius is nontangential. Boundedness supplies the common normal-family bound; the proof does not assert the same implication for arbitrary unbounded holomorphic functions.

### Unrestricted limits are a different target

Neither the source convention nor this audit substitutes unrestricted approach limits for nontangential limits. That distinction matters. If a function on D has a finite unrestricted limit at every boundary point, its boundary extension is continuous: for boundary points zeta_j -> zeta, choose interior points z_j -> zeta_j with |z_j-zeta_j| < 1/j and |f(z_j)-f*(zeta_j)| < 1/j. Then z_j -> zeta and the unrestricted limit at zeta forces f*(zeta_j) -> f*(zeta).

For a bounded holomorphic function with those limits, this gives a continuous extension to the closed disk. Vanishing on a dense E would force zero on the whole boundary and hence zero throughout D by the maximum principle. Dense null G_delta sets exist as above. Therefore the unrestricted interpretation would change the problem and cannot be silently inferred from a Fatou-point statement. The accepted radial/nontangential interpretation is essential and source-grounded.

## Independently established byte inventory

The trusted original manifest SHA-256 is

    cf5f178a46b580701522ce59ff4707c4179963ec5d2f8848a759261b1d974206

`INPUT_INVENTORY.json` independently records all seven original filenames, sizes, and hashes, including the manifest itself. The sum of the original sizes is 17,709 bytes. The manifest contains six payload entries; those six plus the manifest are the exact reviewed packet. `verify_independent.py` embeds the seven reviewed identities and the original manifest pin, checks a fixed inventory, and never executes the original verifier. The strict checker is the authoritative release interface for this audited inventory; the original checker is retained unchanged as historical evidence.

`SOURCE_AUDIT.json` records the three independently recalculated source-PDF hashes and exact public locations. These byte checks used the already-retrieved streams. Fresh public-page checks corroborated the source records; this audit does not claim a second network retrieval of the PDF bytes. Existing rendered pages were inspected after web screenshot requests returned cache misses. Source PDFs, extracted source text, page images, and input records are excluded from the public audit.

A bounded current correction search located no correction to the target theorem. This is a limited negative search result, not proof of an exhaustive absence of corrections. The positive acceptance evidence is the exact published theorem and the problem collection's own affirmative update.

## Verifier trust boundaries

The original verifier checks the caller's external manifest hash before trusting file identities. Under the reviewed pin, altered manifest or payload bytes and inventory changes are rejected. No correctness check uses Python `assert`, so optimization does not remove these checks.

It is a generic manifest verifier, not a validator for every mathematical or metadata claim. Deliberately replacing the external pin changes what the caller trusts. With such replacement pins, the audit observed acceptance of a boolean schema value, duplicate JSON keys interpreted by Python's parser, wrong or missing problem IDs, and an empty inventory. These are documented semantic limits, not successful tampering under the original trusted pin. The authentic manifest has none of these forms.

The original verifier also follows a symlink for MANIFEST.json and optional source PDFs, while rejecting payload symlinks. Byte identity can still be established through such a link. The independent checker imposes the stricter rule that every expected packet member, including the manifest, and every optional PDF must be a regular nonsymlink file. Packet and source roots must themselves be nonsymlink directories. All packet JSON is parsed with duplicate-key and nonfinite-number rejection, including exponent overflow. Manifest schema version, problem ID and byte counts require actual integers, not booleans or floats; exact root and row field sets and the complete reviewed inventory are enforced. Source-identity records also have exact row fields and types. It fixes the reviewed inventory rather than accepting caller-repinned alternatives.

Neither checker can authenticate its own executable code merely by running it. A reader must obtain the checker and its externally delivered audit-manifest hash through a trusted publication or handoff, or independently inspect its short code and constants. A compromised interpreter, filesystem, or hash implementation is outside the guarantee. Tests use stable offline inputs; no general defense against hostile concurrent filesystem mutation is claimed. Hard links to the same ordinary file bytes are permitted.

No correction to the original mathematical report or original verifier is required for its stated externally pinned byte-identity use. The strict independent checker is an additive audit tool, not a silently modified original. Broad interpretations of “malformed manifest rejection” should be read in light of the concrete parser limits just documented.

## Reproducibility outcomes

The final run met **337 expected outcomes** with Python 3.12.14, as a non-root POSIX user. `AUDIT_TEST_RESULTS.json` contains each test name, mode, expected exit, actual exit, and sanitized output. Expected rejection tests count as successful controls; these are not 337 mathematical proof tests.

Coverage includes:

- Original and independent checkers under normal Python, `-O`, and `-OO`.
- A packet with files mode 0444 and directory mode 0555, plus an unrelated read-only working directory. Actual attempts to append and create files both raised PermissionError before the checkers were run.
- Missing, wrong, and uppercase external pins; same-size report, verifier, and manifest mutations; truncation; missing payload; unknown PDF, hidden file, and directory; file replaced by directory; payload and manifest symlinks.
- Deliberately re-pinned invalid JSON, root shape, missing/unsupported schema, duplicate filenames, traversal/absolute/self-manifest names, negative/string sizes, invalid digest, null rows, null file list, and the accepted semantic boundary cases described above.
- Direct structural-helper tests in all three Python modes, independently reaching duplicate/nested-duplicate, NaN/infinity/exponent-overflow, exact integer-type, row-field, inventory, source-name, and source-schema checks without weakening the production pin gate.
- Packet-root and source-root symlinks, rejected by the strict checker.
- All three optional source identities; source mutation, truncation, absence, and symlink behavior.
- Before/after identity checks proving that all original packet files and the three supplied source PDFs remained unchanged. No verifier wrote into the read-only working directory.

An initial harness development run passed the source directory as a relative path while changing the subprocess working directory. That setup error was corrected by resolving the input directory before launching subprocesses; the published results are the complete final rerun. This was a harness configuration issue, not a theorem or original-verifier failure.

The test harness mutates only disposable copies and creates no publication or queue changes. Its optional source tests need separately obtained PDFs; the source-free public slice contains none.

## Publication allowlist

The complete audit public slice consists only of:

1. `AUDIT_REPORT.md`
2. `AUDIT_TEST_RESULTS.json`
3. `INPUT_INVENTORY.json`
4. `REPRODUCIBILITY.md`
5. `SOURCE_AUDIT.json`
6. `run_audit_tests.py`
7. `verify_independent.py`
8. `MANIFEST.json`

Only these eight ordinary files are proposed for publication. The seven original packet files may be published separately, unchanged, under their existing allowlist. No source text, PDFs, datasets, private coordination records, or environment-specific paths belong in either audit publication slice. The audit manifest covers the seven audit payload files; its own hash is delivered separately. This audit itself performed no publication, queue mutation, outreach, or child delegation.

## References

[D] Arthur A. Danielyan, *Rubel's problem on bounded analytic functions*, Annales Academiae Scientiarum Fennicae Mathematica 41 (2016), 813–816. DOI: https://doi.org/10.5186/aasfm.2016.4151 . Published PDF: https://www.acadsci.fi/mathematica/Vol41/vol41pp813-816.pdf . Versioned preprint: https://arxiv.org/abs/1606.03116v1 .

[H] Walter K. Hayman and Eleanor F. Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2, 21 September 2018, Problem and Update 5.29, printed p. 95, reference 181. https://arxiv.org/abs/1809.07200v2 .

[K] S. V. Kolesnikov, *On sets of nonexistence of radial limits of bounded analytic functions*, Russian Academy of Sciences Sbornik Mathematics 81:2 (1995), 477–485. DOI: https://doi.org/10.1070/SM1995v081n02ABEH003547 . Primary record: https://www.mathnet.ru/php/archive.phtml?jrnid=sm&option_lang=eng&paperid=892&wshow=paper .
