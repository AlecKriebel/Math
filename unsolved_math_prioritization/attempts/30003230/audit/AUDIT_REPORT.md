# Independent adversarial audit: problem 30003230

Audit date: 2026-10-05 UTC. Rank: 732. General result: unresolved, five routes completed. No solution, counterexample, novelty, or exhaustive current-openness claim is certified.

## Verdict

- **Authored mathematics and stated scope: PASS.**
- **Frozen packet integrity and deterministic arithmetic: PASS.**
- **Original source provenance record: REVISE_REQUIRED**, for one URL/byte-identity mismatch.
- **Original frozen packet read together with the controlling SOURCE_METADATA_CORRECTION.json overlay: PASS, scoped as above.** The overlay supplied in this audit discharges the sole mandatory correction without changing the authored freeze or any mathematical claim.

The original packet alone must not be described as an unqualified provenance pass. Any composite delivery relying on this corrected pass must retain the correction overlay and identify it as controlling for the OWR source record.

## Bound input

Eight-file authored release; the manifest itself lists the other seven files.

- ZIP: STRINGY_DIVISORIAL_30003230_SAFE_PACKET.zip
- ZIP bytes: 17356
- ZIP SHA-256: b6c69b1639fd31f5a8ed675fa7ddaac6e097cf669419ff8222315af9dba86710
- MANIFEST.json bytes: 1003
- MANIFEST.json SHA-256: 5d6dfeea07270a9a307fc7e21a623cd427826c0f9eb638ffcb389ea9c6e324f2

All files were read. All listed file hashes and sizes match. Archive members match the release byte for byte. Authored files were not edited.

## Mandatory correction C1: distinguish the OWR PDF versions

The first source entry in SOURCE_AUDIT.json attributes a 661526-byte PDF, SHA-256 46d20f91d170342f50942e330f6adfefc09b793905cfc42abc87649b6c1af769, to the MFO download URL. Fresh retrieval from that exact URL instead gives:

- [MFO PDF](https://publications.mfo.de/bitstream/handle/mfo/3550/OWR_2016_46.pdf?isAllowed=y&sequence=1)
- 626588 bytes
- SHA-256 7e95eece7a092107d1f2f3f07831aca55705715cadd4b8d739cd4e1f6341843d

The stored 661526-byte object is independently reproduced exactly from the download link on the [EMS publisher landing page](https://ems.press/journals/owr/articles/14754):

- [EMS PDF](https://ems.press/content/serial-article-files/46651?nt=1)
- 661526 bytes
- SHA-256 46d20f91d170342f50942e330f6adfefc09b793905cfc42abc87649b6c1af769

The overlay corrects the existing source URL to EMS and separately records MFO's distinct bytes. It does not claim that the MFO URL reproduced the EMS object. Both are genuine 68-page report PDFs. The relevant printed pages 2684-2686 were inspected. Whitespace-normalized extracted text agrees exactly on printed pages 2684 and 2686. Printed page 2685 was visually compared; its substantive definitions and formulas agree despite layout and extraction-order differences. This is a provenance correction, not a mathematical revision or a claim that the entire PDFs are identical.

## Target and source scope

The projective complex normal Q-Gorenstein log-terminal domain is retained from the invariant's surrounding definition. OWR Conjecture 4 is the divisorial question, and the MFO and EMS copies agree on it. Batyrev-Gagliardi's version-2 Conjecture 1.5 is the same target. The additive algebraic invariant and its resolution independence are explicit inputs; arbitrary-product multiplicativity is not assumed. Their Theorem 3.6 has a finite-orbit equivariant resolution hypothesis, and Theorem 1.8 supplies the spherical special case. Neither is an unrestricted theorem. [Batyrev-Gagliardi v2](https://arxiv.org/html/1610.03842v2)

Fresh byte retrieval exactly reproduces the other three reported PDF hashes and the dataset-response hash. The dataset statement is 125 UTF-8 bytes with SHA-256 44af69f0ad0c8eb55d3b4a8120b3f78560101ee51145291bd2c2478f186a0901; its identifier, row index, and lack of truncation agree. The endpoint is not revision pinned. No raw row or source text is in this audit's safe release.

Satriano-Usatine's seven-dimensional example concerns a negative off-diagonal stringy Hodge coefficient. It supplies no divisorial algebraic-Euler comparison here. The packet correctly excludes that substitution. [Satriano-Usatine v2](https://arxiv.org/pdf/2607.19184v2)

## Proof-by-proof review

### Route 1: smooth centers and a single smooth exceptional divisor — PASS

The blowup decomposition restricts to algebraic cycle-class subspaces: the maps and inverse projections are given by algebraic correspondences. Consequently summing algebraic Betti numbers gives the claimed positive codimension-minus-one multiple. This uses neither the Hodge conjecture nor an unproved general positivity assertion. Nonempty smooth projective centers have positive algebraic Euler number. Codimension one is properly excluded.

For the single-divisor formula, the source itself is a log resolution under the stated smoothness and entire-exceptional-locus hypotheses. The negativity-lemma argument has the correct sign: a negative canonical coefficient would make the nonzero effective exceptional divisor relatively nef, which is impossible; coefficient zero contradicts relative anticanonical ampleness. Thus the coefficient is strictly positive. The formula is not extended to singular divisors or sources.

The genus example correctly separates algebraic and topological Euler numbers. Odd cohomology does not enter the smooth projective algebraic invariant.

### Route 2: toric subdivisions — PASS

On a simplicial complete fan the shed decomposes into lattice simplices, so the determinant sum is the normalized volume. Replacing a column by the primitive inserted ray gives the stated rational-coefficient determinant identity, including lattice index and orientation. Positivity is tied to the Mori sign of the canonical coefficient. Crepant subdivisions give equality and some non-Mori subdivisions reverse the inequality. Primitive positive weighted blowups of a fixed point of projective space give the stated geometric family. This is attributed special-case work, not a new general result.

### Route 3: canonical projective surfaces — PASS

The crucial map is a morphism, not merely a birational rational map. The composite of the minimal resolution of X with f is a resolution of X', possibly also modifying its smooth locus. The universal property of the minimal resolution of a normal surface gives S -> S'. This property applies to arbitrary resolutions; no minimal-model choice on the birational class is being substituted. An independent reference is Theorem 0.4.1 of [Cossec-Dolgachev-Liedtke, Enriques Surfaces I](https://sites.lsa.umich.edu/idolga/wp-content/uploads/sites/1334/2024/08/EnriquesOne.pdf), printed p. 66.

Canonical surface singularities have crepant minimal resolutions, so the two stringy invariants equal the algebraic Euler invariants of their respective smooth projective resolutions. This is exactly the surface fact recalled in [Carvajal-Rojas-Yasuda, Example 2.17](https://ems.press/content/serial-article-files/50862?nt=1). The proper birational map of smooth surfaces factors only in the required blowup direction by [Stacks, Lemma 54.17.1](https://stacks.math.columbia.edu/tag/0C5Q). Each point blowup adds one. If the count were zero, compatible canonical pullbacks would force K_X=f* K_X', contradicting its intersection with a contracted curve. Strictness is therefore justified. No klt-but-noncanonical or higher-dimensional extension follows.

### Route 4: common-resolution positivity and obstruction — PASS

Discrepancy order makes the rational brackets nonnegative. Strictness still needs a positive stratum involving a changed discrepancy. The finite-orbit source provides this; an arbitrary resolution does not. The iterated point-blowup example has the correct log discrepancies (1,2,...,2) versus (2,3,...,3), central open value 2-m, and total difference one. The negative central stratum is genuine. The -7/20 formal example is also arithmetically correct and is clearly excluded as a geometric counterexample.

### Route 5: graph derivative criterion — PASS

Writing x_i=1/A_i gives the independent expression F=2 sum_i x_i + sum_edges (x_i x_j-x_i-x_j). Its coefficient in x_i is exactly 2-d_i+sum_neighbors x_j. Increasing discrepancies decreases reciprocal coordinates. Replacing coordinates one at a time gives an exact telescoping proof of the same sufficient criterion as the author's derivative proof: intermediate neighbor reciprocals are at least 1/B_j, and every changed coordinate has strictly positive coefficient. At least one strict change therefore makes the total drop strict. Negative derivatives at unchanged coordinates are irrelevant because their directional multiplier is zero.

Degree-at-most-two graphs, including a two-vertex double-edge cycle, have a strictly positive coefficient for every positive vector. The B_j<=1 region has lower bound two even at branching vertices. Edge multiplicity is counted correctly, and the no-triple-point hypothesis is needed for the displayed surface formula. Neither positivity on the whole orthant nor a common-resolution discrepancy bound of one is imported.

The star adjunction equations, Schur-complement condition, source discrepancies, and center sign are consistent. Independent Cramer's-rule solutions reproduce the 1650 attempted and 17 eligible numerical cases, with minimum gap one. Such computations do not establish geometric realization, projectivity, or all klt surface cases.

## Independent computation and adversarial controls

A separate standard-library verifier does not import or execute the author's functions to compute its mathematical tests. It uses reciprocal-coordinate polynomials, exact coordinate differences, permutation determinants, and Cramer's rule. Author scripts are separately replayed only for reproducibility.

- 53895 independent checks, deterministic in ordinary and optimized Python.
- All 1099 simple graphs on one through five labeled vertices tested; 4396 sufficient-region instances, including 3176 with negative open-stratum coefficients.
- 11 further cycle/multiedge cases and a case with a negative margin at an unchanged coordinate.
- 1403 primitive positive weight tuples using weights one through six, plus 819 nonunimodular cone cases.
- 49 local SNC blowup-invariance identities and 101 genuine iterated-blowup cancellation checks.
- 12 explicit false-shortcut controls, including failure of strictness with zero margin and failure of strict lexicographic order after evaluation at one.
- The author's 2427 checks and 10 false shortcuts reproduce byte-for-byte in ordinary, optimized, and relocated execution.
- 14 file-tamper rejections and six missing/extra-file rejections, all on temporary copies.

No Python assert statements occur in the author's checkers, so optimized execution does not disable their checks. These counts measure checks, not independent theorems or geometric realizations. The arithmetic output's PASS status concerns its own stated finite scope and does not override provenance correction C1.

## Limits and delivery boundary

Historical repository searches, conversation searches, and the earlier queue state were not reconstructed. No exhaustive literature search or universal current-openness certification is made. The retained conclusion is that this packet does not solve or disprove the unrestricted problem.

The audit release contains authored audit prose and code plus public verification metadata only. Source PDFs, extracts, dataset rows, rendered source pages, private sources, and coordination materials are excluded. No remote write or publication was performed. The frozen author release and ZIP remain unchanged.
