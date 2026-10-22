# PR201 — independent whole-package adversarial review 02

**Verdict: CLEANPASS.** No substantive mathematical, attribution, scope, reproducibility, PDF, custody-consistency, or archive-integrity defect was found in the exact final package identified below. No repair is requested. This clears the package as an attributed alternative presentation of the exact Ferudun theorem; it does not establish theorem/method novelty, first disclosure, derivational independence, conventional human peer review, or formal verification. Publication authority remains with Root.

## Exact reviewed object and independence

- Target: `publication_package_v2` beside this review folder.
- `PACKAGE_SEAL.json`: **90105 bytes**, SHA256 **89bbfc82c0ae2b80fca046671681f94cef28f130d01df4a3b52036efd7a95ad5**.
- The timed independent plan was frozen at **2026-10-16T06:52:23Z**, before reading the manuscript or any favorable verdict. The entire proof was then reconstructed independently in `INDEPENDENT_DERIVATION.md`, including the local AA-prime argument. Primary literature, rather than earlier audit verdicts, was used for the mathematical/source comparison.
- No earlier whole-package report was read. Earlier favorable audit reports were inventoried and hashed as historical payload only. Original PR metadata and turn receipts were subsequently read for chronology/effort; favorable summaries appearing there did not support this mathematical verdict.
- The planned time windows were upper estimates, not a mandatory waiting period; the actual UTC events and completion estimates are in `RESEARCH_LOG.md` and machine receipts.

## Mathematical claim and proof audit

The theorem has the correct quantifiers: fix a noncircular ellipse `a>b>0`, a proper nondegenerate confocal inner ellipse `0<lambda<b²`, and exact least Poncelet period `N=2m` with odd `m>=3`; then for every fixed finite real point M the signed outer-tangent area times the signed pedal-on-boundary-tangents area is phase independent. It does not assert a constant uniform across different M or different caustics. Primitive star traversals and their reversals are covered. The feet lie on whole tangent lines, and zero/negative signed pedal area is allowed.

I independently verified each central step:

1. The four E/C intersections are finite, distinct, transverse, and nonzero in both coordinates. The tangent-incidence double cover is smooth connected genus one. Both deck involutions act by -1 on differentials, so their composition is a translation. Least period forces its exact global order, rather than merely producing an N-entry list.
2. Central inversion and `T^m` agree by the faithful finite orientation-preserving action on either real directed component, a metric circle; equality extends analytically to X. This argument continues to coprime stars. Consequently the cyclic quotient is unramified genus one.
3. Original coordinate poles lie at the four flags over two original infinities. Central pairing reduces their quotient support to at most two points. Consecutive original vertices cannot both be infinite. A is nonconstant because it is strictly positive for the real orientation having the caustic on the left and is odd under reversal. Genus one rules out a single simple pole, proving exactly two distinct simple poles and the two-dimensional space `L(D)=span{1,A}`.
4. The complex dot product is correctly bilinear. The foot map is regular at original infinity because the leading normal is nonisotropic for a>b. The four finite isotropic contacts are exactly the common E/C tangent contacts; d has simple zeros, and the explicit nonzero C(P)-1 value proves projection unramified there.
5. At a common-tangent flag, the odd-m congruence moves it to original infinity. The sigma-fixed shifts in its orbit are exactly 0 and m; the two flags at every contact then give the complete singular foot index list **0,1,m,m+1**. For m=3 and all larger odd m, the only adjacent pairs are (0,1) and (m,m+1), including the cyclic wrap check. The residues in each pair are scalar multiples of the same contact normal, so the double-pole determinant coefficient vanishes even if a special M kills a residue. Equal residue magnitudes are not assumed. Unramified descent gives `B_M in L(D)`.
6. Reversal holds with M fixed and removes the additive constant from `B_M=c_M A+d_M`. No division by an area is used. Zero c_M and negative signed values cause no exception.
7. I rederived the credited AA-prime law locally: W is the E-pole of the caustic chord, its only coordinate poles are the two origin-through complex tangents to C, the chord projection is unramified, and no adjacent W poles occur. Odd-m shifts put the original-infinity support at sigma-fixed representatives and the W-infinity support at tau-fixed representatives. An even-order orbit cannot contain both kinds because that would require `2j=1 mod N`. The corresponding finite palindromic vertex/chord lists have signed area zero. These zeros remove every possible simple pole of AA-prime, making it constant on the compact quotient. This verification does not rely on an unexamined generic-pole assertion from the credited paper.
8. Real outer intersections are finite; real projection denominators are positive. The manuscript's positioning observation also correctly uses a nonzero real AA-prime product: in normalized ellipse angle coordinates, every forward increment lies in (0,pi), and the outer tangent intersections have midpoint-angle increments in (0,pi), making their oriented shoelace summands positive even for stars.

The exact remaining mathematical gap is **none found**. This statement means the written argument survived this audit, not that an automated check establishes infallibility. The universal conclusion rests on the analytic proof, not sampled periods or symbolic control counts.

## Fresh falsification and reproduction

`reproduction_receipt.json` records fresh runs of all five portable exact suites in ordinary Python and `-O`. Both return PASS and reproduce their retained expectations. The runner's manifest checks use explicit exceptions. It ignores only UTC/optimization/elapsed-time metadata in JSON, and byte-compares text. Both `--guard-false` runs fail as required.

A separate newly authored control, `independent_exact.py`, rederives geometry from the boundary tangent equations and projection definition. It passes **407** enforced checks in each mode, with identical mathematical output. These include the isotropic/infinity algebra, complete modular shift/adjacency tests for selected m as finite cross-checks, arbitrary parallel-residue cancellation, the exact general-M N6 polynomial, signed reversal, and both printed repeated-triangle constants. For the latter two triangles it also checks unit specular reflection and strict caustic contacts inside each segment. This supplements, rather than replaces, the universal modular reasoning in the written derivation.

The new falsification command changes the target coefficient from 40 to 41. The false claimed identity `A'B_M=41*(1+|M|²/9)` is rejected with nonzero status in ordinary and optimized Python. Thus testing is not limited to an unconditional guard that says “false.” See `false_identity_receipt.json`.

`selected_physical.py` reuses the read-only portable direct-contact/second-intersection physical implementation, not the flag proof, for selected new executions:

| a,b | least N, winding | purpose |
|---|---:|---|
| 2,1 | 10,3 | signed star with negative exterior pedal area and a zero crossing |
| 1.0001,1 | 14,5 | approach to excluded circular boundary |
| 5,1 | 22,9 | caustic lambda about 0.999999995706, close to excluded degeneration |

All target phase-product spreads are below about 1.25e-66; the largest closure error is about 2.16e-65. For the N10 star the zero radius is about 4.0799382974793983; the sampled zero residuals are below 3.2e-72, with positive/negative pedal values on its two sides. Reversal negates both signed factors. The six-entry winding-two triangle control has large phase variation for noncentral M, as expected for its least period three. Ordinary and optimized selected outputs agree after removing only UTC/optimization fields. These are finite, noninterval diagnostics, explicitly not a universal proof.

The original assertion-based scripts are not silently promoted to `-O` evidence; the manuscript and README disclose their limitation. I did not needlessly rerun the full historical 56-case numerical suite. I inspected all six portable code files and the runner; their explicit conditions and direct formulas are consistent with the advertised controls.

One initial replay failed because I supplied a relative PYTHONPATH while the child changed working directory. This was my orchestration error, not a package defect. The failure is preserved, and all successful reruns use the absolute shared read-only dependency directory. No dependencies were installed/copied. Every Python command used `-B`.

## Primary sources and honest positioning

The decisive cached primary texts were read directly; their identities and reading locations are in `literature_receipt.json`. Ferudun v1.0 gives the same Theorem 1, arbitrary real M, signed areas, least-period convention, stars, six-period formula, and repeated-triangle warning. The full v1.0/v1.1 source diff preserves that result and adds a separate centered extension. The overlap in central pairing, isotropic projection poles, parallel residues and reversal is substantial and is expressly acknowledged in the current note. The quotient two-pole presentation is a useful alternative organization, and the note does not claim those mechanisms new. Its explicit observation that proportionality follows from the product theorem and nonzero AA-prime correctly avoids repackaging an equivalent consequence as theorem novelty.

Chavez-Caliz's journal text supplies the flag framework and the original/outer product for even concentric Poncelet families. The note credits it and independently supplies the target-parity local verification. RGK arXiv v11 page 6/Table 4 indeed lists k303,a with N=2mod4 and all M, without literally printing “least period”; the current wording corrects that distinction. Steiner XV–XVI records the classical pedal-area radial/circular-level mechanism. I used its cached OCR with that limitation and independently derived the modern central-pairing formula; I do not elevate a generic finite curvature centroid statement in zero-coefficient cases.

The fresh primary public GitHub, Zenodo and DataCite API checks in `primary_records.json` confirm exactly the chronology fields printed in the note: PR creation at 2026-10-01T05:18:49Z; Ferudun v1.0 creation 16:56:14.316216Z/registration 16:56:15Z and v1.1 creation 18:12:36.529602Z/registration 18:12:37Z. They also confirm the original PR head listed in custody. These heterogeneous record fields do **not** prove first visibility or derivational independence; the paper, README and metadata correctly refrain from drawing that inference. No wider exhaustive priority search is certified here.

The extensive AI assistance, one recorded original substantive turn/QUEUE1/5, unverified model/effort, October16 additions, unrefereed status, and lack of conventional independent human peer review/proof-assistant certification are disclosed. Historical pending-stage artifacts and the source-literal correction are clearly explained in README. They are preserved for accountability without being presented as current publication-operation state. The honest positioning is suitable for the intended attributed research note.

## Whole payload, custody and PDF

`check_package.py` validates the exact seal, all **237** nonseal outer files, all **233** materials files, all **232** materials-manifest pins, three intended upload pins, and metadata equality across seal/materials/deposit. ZIP CRC passes; the ZIP has exactly **233 unique regular entries**, no unsafe path or symlink, and every entry equals its extracted material byte-for-byte. It contains all **24** original submission files. Their sizes, SHA256 hashes and independently recomputed native `blob <length>\0<data>` SHA1 identities match custody, totaling **54661** original bytes. This is custody consistency; I did not issue Git commands or independently re-extract the old tree in this read-only review.

`check_history_links.py` revalidates **142** mathematical-gate and **43** priority-gate safe-file pins, including self-exclusion. It also verifies that all six portable scripts differ from the retained original scripts only by their individually disclosed local runtime path removals (or are byte-identical), with source, portable and expected-source pins matching. The prior portable replay receipt is transparently described as predating the archive-only repair, and the new manifest/seal, not that old receipt, authenticates the final 233-entry coverage.

The standalone and archived LaTeX sources are identical. I read the complete source and extracted PDF text and rendered/visually inspected **all six actual PDF pages**. Equations, scope, attribution, bibliography and disclosures are legible; no clipping, missing glyph, missing section, placeholder or material source/PDF mismatch was observed. PDF metadata reports six letter-sized pages, no encryption, forms or JavaScript. Rendering used about 1.8 MB and the six temporary images were removed after inspection; only my own temporary renders were deleted. No rebuilt PDF or bit-reproducible typesetting claim is made.

The archive has no third-party fulltext PDFs/images, dependency implementations, browser artifacts or nested external source archives. Authored bibliographic/custody receipts and original historical source records remain. This review retains only authored scripts, reports, selected bibliographic/public-record fields, check results and diagnostics; no new third-party fulltext/dependency/raw external/private payload is copied into its safe manifest.

## Reproduce this review's checks

With Python3.14 and the given shared dependency directory on an **absolute** PYTHONPATH, from A:

```
python3.14 -B whole_package_adversary_02/check_package.py
python3.14 -B whole_package_adversary_02/check_history_links.py
python3.14 -B whole_package_adversary_02/reproduce.py
python3.14 -B whole_package_adversary_02/independent_exact.py
python3.14 -B -O whole_package_adversary_02/independent_exact.py
python3.14 -B whole_package_adversary_02/run_false_identity.py
python3.14 -B whole_package_adversary_02/selected_physical.py
python3.14 -B -O whole_package_adversary_02/selected_physical.py
```

The two direct `independent_exact.py --false-identity` commands, with and without `-O`, must fail; their wrapper succeeds only when both fail. `check_primary_records.py` is optional and re-reads public APIs; it retains selected public metadata only. Exact paths/commands and actual statuses are preserved in receipts. `SAFE_AUTHORED_MANIFEST.json` authenticates this review's retained authored outputs and excludes itself.

No package/original/global file, Git/ref/index/branch, PR, release/DOI, spreadsheet, UI or publication state was changed. No outside individual was contacted. This review is complete; strongest verified result is the stated universal theorem supported by its reconstructed analytic proof and the package's successful reproducibility/integrity checks.
