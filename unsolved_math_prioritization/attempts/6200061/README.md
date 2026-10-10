# Kleiner conformal dimension: marked-realization obstruction

**Problem 6200061 / AMR-061-0061, rank 810: unsolved, 5/5 routes.** Independent audit: **ACCEPTED_PARTIAL_NOT_SOLVED**. No correction to the frozen partial-result proof was required. There is no full-resolution or novelty claim, human peer review, or proof-assistant certification.

## Exact scope

The original target asks whether the Ahlfors-regular conformal dimension A(G) equals the equivariant visual conformal dimension E(G), and whether a geometric visual model attains A(G) when the gauge minimum exists. Both general questions remain unresolved here.

The accepted partial result concerns a **specific marked metric**. For each closed orientable hyperbolic surface group, pull the chordal circle metric back by h(x)=x|x|, with h(infinity)=infinity. This metric is quasisymmetric to the standard metric, Ahlfors 1-regular and minimizing. An actual Fuchsian group element can be written g(x)=ax+a-1 with a>1 after conjugation; it is not Lipschitz for the pulled-back metric. Every isometry acts bilipschitz on a visual boundary, so an equivariant bilipschitz realization of this marked metric is impossible.

This does **not** refute existential attainment: the ordinary round visual metric already attains A=E=1 for surface groups. The illustrative multiplier 2 is not asserted to occur in every lattice. Proper-geodesic model hypotheses and the distinction between a fixed marking and abstract round-circle isometry are essential.

Read [the proof](author/PROOF.md), [all five routes](author/APPROACHES.md), [independent audit](audit/AUDIT_REPORT.md), and [verdict](VERDICT.json). Other accepted observations include the bounded-additive-defect invariant metric lemma, consistent entropy/visual-parameter rescaling, free-group equality with unattained zero infimum, and real-hyperbolic lattice equality. They do not supply a general geometric realization theorem.

## Verification and its limits

The author and independent audit contain exact algebraic certificates and finite rational regressions. The positive Bernstein certificate proves its stated polynomial inequality on the entire interval. The 80 dyadic samples, 84 cylinder records, 155 multiplier tests, and 4,080 power-map triples are regression evidence, not formal geometric proofs.

The independent suite runs 22 rejection cases in both Python modes, plus the author's 12 rejection cases in both modes. Three deliberately rehashed changes to mathematical prose, plausible corpus hashes and source titles pass the standalone author verifier. They fail the externally pinned archive identity. The mathematical and source audit is therefore essential; executable PASS does not verify arbitrary prose or refresh literature.

Run from any working directory, using Python's standard library:

    python3 /path/to/6200061/verify_package.py
    python3 -O /path/to/6200061/verify_package.py
    python3 /path/to/6200061/run_package_controls.py

For an externally retained publication manifest pin and exact queue comparison:

    python3 verify_package.py --expected-manifest SHA256 --queue-base BASE_QUEUE --queue-updated BRANCH_QUEUE

The wrapper verifies exact inventories, symlinks, the author/audit manifest pins, immutable archive bytes and each unpacked member, scope fields and the independent checking suite. The publication manifest excludes only itself; authenticate it with the Git commit or external publication receipt. Hashes are not signatures and do not protect against replacement of every trust anchor and verifier.

Complete corpus identity can be checked separately with the audit script's optional --corpora CATALOG_JSON PROBLEMS_JSON REPORTS_JSON. These inputs are deliberately not distributed. A run without them reports NOT_RUN for fresh complete-corpus verification; historical checked metadata remains in the immutable audit.

## Sources and preservation

The problem is due to Bruce Kleiner and recorded in [Kapovich's survey](https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf), page 17. Hume-Mackay-Tessera's [Poincare profiles of groups and spaces](https://ems.press/journals/rmi/articles/16795) was published in **2020**; the retained author PDF is dated **May 29, 2019**. The source audit does not claim every PDF was freshly downloaded, and the full Bonk-Schramm original was not independently inspected. The [2025 Hume-Mackay preprint](https://arxiv.org/abs/2511.10469) addresses a different profile exponent. The bounded literature and repository searches are not exhaustive absence or priority proofs. The catalogue webpage was inaccessible during preparation, so no current rendered webpage status is claimed.

Both safe ZIPs and every author/audit file remain byte-identical to their freezes. Their historical no-publication statements describe preparation stages. Public source titles, URLs, hashes, sizes and inspection metadata are retained; source PDFs, extracts, raw corpora, private sources and coordination are excluded.

Only the selected queue row's Status and Turns change to unsolved and 5/5; every other queue byte, including the existing header, is preserved. There are no additional proof-search turns. Draft review only; no merge, release, DOI or outreach.
