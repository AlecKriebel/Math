# Source, edition and prior-attempt audit

## Exact target and conventions

Numeric ID5100007, code AMR-050-0007, queue rank217. The pinned dataset record asks for constancy of the product of distances from the **outer tangent-intersection polygon's vertices** to one original ellipse focus, for period divisible by4. Its full record and exact-key imported prior report are retained as `source_record.json` and `prior_imported_report.json`. Imported third-party triage is not a prior Alec/campaign attempt and is not proof evidence.

The source editions were independently downloaded and the full table pages visually inspected:

- Reznik-Garcia-Koiller, *Eighty New Invariants*, arXiv2004.12497v11, October29,2020. Table2 printedp5 has k115 = product |P'_i-f1|, N=0mod4, proof column '?'. The product uses ordinary Euclidean distances, and the introductory conic pair is two confocal ellipses. https://arxiv.org/abs/2004.12497v11
- Published *Fifty New Invariants*, Arnold Mathematical Journal7(2021),341-355, DOI10.1007/s40598-021-00174-y. Table2 printedp345 retains that **same k115 formula and parity**, also '?'. https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf
- Edition changes matter nearby: arXiv k111 is A'A'' for evenN; published k111 is A'A''/A^2 for oddN. The ratio A'/A'' moves from arXiv k113 to published k112, while the even focal-distance sum moves from arXiv k121 to published k113. None changes k115. The preceding k114 remains the original-vertex product for N=2mod4 in both tables.
- P' means intersections of **tangents to the outer billiard ellipse at consecutive orbit vertices**, not caustic contact points, focal pedals or antipedals. The inner polygon P'' and its areas do not enter this target. All source polygon areas are signed. The source's internal angles differ from Stachel's exterior-angle notation elsewhere, but neither convention is used in the proof.
- The theorem explicitly uses least period, equivalently gcd(N,tau)=1 in the canonical parametrization. Primitive star orbits are included. Repeated smaller-period words do not acquire the primitive parity merely because their traversal length is renamed N. Hyperbolic/degenerate caustics are outside the source's introductory confocal-ellipse scope.

## Published proof inputs

Stachel, *On the motion of billiards in ellipses*, European Journal of Mathematics8(2022),1602-1622, DOI10.1007/s40879-021-00524-2. Published Theorem4.3/equation4.9 provide canonical parameters, caustic-eccentricity modulus, shift2v, primitive turning number and semiaxes. The full published PDF was retrieved from the author's university repository. Its catalogue incorrectly calls the journal European Journal of Applied Mathematics, but the PDF and publisher identify European Journal of Mathematics; the latter attribution is used.

- Publisher: https://doi.org/10.1007/s40879-021-00524-2
- Full version of record: https://repositum.tuwien.at/bitstream/20.500.12708/136087/1/Stachel-2022-European%20Journal%20of%20Applied%20Mathematics-vor.pdf
- Author preprint: https://arxiv.org/abs/2105.03624v2, Theorem2/equation4.10
- Jacobi periods/poles/quarter shifts: https://dlmf.nist.gov/22.4 . Addition/double-angle identities: https://dlmf.nist.gov/22.8 . Derivatives: https://dlmf.nist.gov/22.13 . The proof uses the correct standard sn/cn shifts, not the adjacent dn-shift sign typo in the preprint.
- Classical complex pole-cancellation method: Akopyan-Schwartz-Tabachnikov, *Billiards in ellipses revisited*, https://arxiv.org/abs/2001.02934 . This is methodological prior art, not an asserted exact k115 theorem.

The preceding campaign result [PR149](https://github.com/AlecKriebel/Math/pull/149), head dde6ebe550ed7fe2e2fc8a1ff06fb13105be97ae, is the distinct k114 target. Its complete proof and review were read. The cyclic-norm strategy is credited; its theorem is not assumed to prove the present outer-product statement. The present proof derives its own outer locus, factorization, divisor and exceptional N4 case.

## Prior-Alec/campaign gate

October1,2026: all-state PR searches by numericID5100007, codeAMR-050-0007 and k115 returned no matching PR. Branch search5100007 returned none. The default-branch commit history for `unsolved_math_prioritization/attempts/5100007` returned empty. Available local all-ref path history returned no attempt; the checkout is a recovered partial clone, so this alone is not a comprehensive remote-history proof. Combined live connector searches supplied the operational gate. `review_v2/related_target_groups.json` contains no target-ID match. The current row was queued0/5. No prior campaign attempt was located; no counter reset is performed.

## Literature-status limits

The exact source tables and Stachel's subsequent canonical theorem were recovered; focused searches for k115 and outer focal-distance products did not identify an exact prior all-period proof. This is bounded literature triage, not proof of novelty or a claim that no unpublished/uncatalogued proof exists. The dataset's old OPEN-TRIAGE conclusion is treated as historical input only. No external person was contacted.

Downloaded full PDFs and their renderings are local reading copies outside the attempt package. No downloaded software was run. Proof verification uses locally authored code and preinstalled standard scientific libraries.
