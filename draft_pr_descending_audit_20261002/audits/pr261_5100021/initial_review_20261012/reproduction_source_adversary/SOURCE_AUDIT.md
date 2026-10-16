# Independent source-target audit for PR 261 / 5100021

Audit fixed head: `7b7fcd63d5ea83df3a4c29853c4ba34b93d16f07`.
This document reports the fresh 2026-10-12 source review; historical review verdicts are not evidence.

## Original imported statement and prior report authentication

The complete original imported statement and complete eight-field prior OPEN-TRIAGE report were read from the cache through a read-only SQLite URI. The catalog metadata revision is exactly `37e53eabe540fb458758e198be61634bd02ee008`, matching `TARGET.json`. The exact unnormalized UTF-8 statement has SHA-256 `6b0e8ed57a00deaeb2b265627bc1146e625e89db5fd9d2ff0f0453d371a7df15` and is byte-for-byte the target's `exact_target` string. The complete report, canonically encoded with `json.dumps(report, sort_keys=True)` using default separators/ASCII escaping, has SHA-256 `a2571a93645c4df7ce94e27215aaece0bdbc05ca9384d131bfcb75bedd77cccb`, matching the pinned prior-report hash. This distinction matters: hashing the SQLite's original unsorted report serialization gives a different hash, without changing the authenticated complete parsed report.

`ORIGINAL_SOURCE_AUTHENTICATION.json` records the exact hash encodings, all field names, revision and file hash. The complete imported payload/report and raw serializations are retained in local `sources/ORIGINAL_IMPORTED_FULL.json`, excluded from publication in line with the submitted source-manifest policy. There is no missing full-record gap. The statement asks solely for the focal product `A_M A_M*` at N≡0mod4, while the prior report classifies it OPEN-TRIAGE, reports the old source table's unknown proof status, records a bounded old literature search, and proposes a possible reduction to original/outer area invariants. Those are historical hypotheses; none is used as proof evidence.

## Primary statement and constructions

Both the [arXiv v11](https://arxiv.org/pdf/2004.12497v11) and [published edition](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf) agree on Table 5, row `k403,b`: the quantity is the **unprimed** pedal area times the **unprimed** antipedal area, the period column is `N≡0 mod4`, and the point column is either focus. The table's value and proof columns were unknown in these editions. The table is on v11 physical page 7 and published physical page 8 (journal p348).

The original-pedal definition is in §3.3: feet of Euclidean perpendiculars from the fixed point to the **original orbit's sides**, with the polygon ordered by trajectory order. The antipedal definition is §3.5: intersections of consecutive lines through original vertices perpendicular to the corresponding focus-to-vertex vectors. The source calls these “rays”; its figure and signed self-intersecting polygon convention make supporting-line intersections the intended geometric construction. Primed outer constructions belong to different rows. No inversion of the original vertices occurs in this target.

The published preliminaries (physical p3, journal p343) explicitly use `a>b>0` and signed shoelace areas. The introduction defines the elliptic billiard here as a pair of confocal **ellipses**; the inner ellipse is the caustic. The antipedal section's footnote permits self-intersections. Circles, hyperbolic caustics, the collapsed caustic segment, and grazing zero-gap endpoints are outside this source setting. Primitive elliptic stars are legitimate families of the same setting and are not excluded by the target row.

There is a minor notation slip in the prose of §3.5, where the antipedal area is rendered without its star. The table and symbol glossary distinguish the original pedal `A_m` from original antipedal `A_m*`; the target is unambiguous when the complete definitions are read.

Relevant pages were extracted and **visually inspected** under the PDF skill: both Table 5 editions, published preliminaries, and published antipedal definition. The locally retained PDFs have the exact submitted source-manifest SHA-256 hashes, listed in `sources/DOWNLOADS.json`. Full PDFs, extracted full text, and page images are kept locally and excluded from Git publication by this folder's `.gitignore`.

## Important period qualification

The **literal Table 5 row does not explicitly say “least period”**. Neither the imported statement nor the imported prior report expands this convention. Consequently, a source audit should not say that the original row itself expressly imposes least period. Treating `N` as the primitive orbit's genuine period is a defensible conventional interpretation, supported by the standard canonical description with `gcd(N,τ)=1` in [Stachel, Theorem 4.3(2)](https://repositum.tuwien.at/bitstream/20.500.12708/136087/1/Stachel-2022-European%20Journal%20of%20Applied%20Mathematics-vor.pdf), physical p13 / journal p1614. That convention must nevertheless be stated explicitly when claiming a complete resolution.

The qualification is mathematically essential. The independently authored `exact_repeated_period.py` constructs two **primitive six-bounce** orbits in outer axes `a=3/2,b=1`, with strict confocal caustic squared axes `189/100,16/25` (`λ=9/25`). Each phase passes exact outer-incidence, caustic-discriminant and reflected-ray checks. Repeating each six-vertex list twice produces a listed `N=12` polygon, but its focal pedal–antipedal products are respectively

`27648/625` and `27783/625`, differing by `-27/125`.

This is an exact counterexample to an unrestricted padded-list reading, **not** to the pinned primitive target. The artifact records every vertex and residual, and the direct area calculations show that repetition doubles each signed area.

## Current literature and priority limitations

A bounded fresh primary-source search found [Alper Ferudun, Focal Pedal-Antipedal Area Products in Elliptic Billiards](https://eulersolve.org/papers/amr-050-0021/), with a landing-page/manuscript date of 1 October 2026 and DOI `10.5281/zenodo.23079799`. The [six-page manuscript](https://eulersolve.org/papers/amr-050-0021/paper.pdf?v=34ff068237a7) claims the same scoped target using a velocity-product telescope, quarter-period permutation, and the known even original/outer area-product theorem. It explicitly qualifies the genuine-period convention and the repeated-N6 limitation.

That external manuscript is an **unrefereed claim** whose proof was not independently audited by this agent. Its presence prevents a clean inference from the old table's question mark to a presently open or novel result. It is context for priority/literature assessment, not independent evidence for this PR's proof. The original imported report's earlier “no proof found” statement is now stale as an account of available claims.

Search queries, exact URLs, limitations and a local-download HTTP403 diagnostic are recorded in `sources/CURRENT_SEARCH.json`. The original and Stachel primary PDFs are retained locally. The search is bounded and does not certify exhaustive novelty or priority. No external individual was contacted.

## Source conclusion

The pinned **primitive, strict elliptical-caustic** target uses the correct original focal constructions and signed areas. Its scope is consistent with the source's geometric setting after making the genuine-period convention explicit. The least-period phrase must be presented as a qualification/interpretation, rather than a verbatim condition in Table 5. A stronger assertion for every periodic list whose length is divisible by four is false by the exact artifact above.
