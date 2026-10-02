# Source gate: positive association of bipartite proper-coloring marginals

Target 30003338 / OWR-15206-017, queue rank 328. Checked 2026-10-02. No substantive author turn has yet been consumed.

## Exact source and success test

Peled and Kahn's problem (5), printed p. 76 of the Combinatorics workshop report, DOI 10.4171/OWR/2017/1, asks whether the indicator set of one fixed color on one bipartition class of a uniformly random proper q-coloring is positively associated, for every finite bipartite graph and every integer q ≥ 3. The entire problem and surrounding page were read and inspected visually. The next paragraph's separate correlation-decay question is not part of this imported target. Original report: https://publications.mfo.de/bitstream/handle/mfo/3565/OWR_2017_01.pdf .

A full positive answer must cover all increasing real functions of the fixed-color indicator vector, not only pairwise correlations, singleton versus all-one events, or a graph subclass. A full negative answer requires one finite bipartite graph, one q ≥ 3, and two explicit increasing functions/events with an exact negative covariance. Failure of an FKG lattice condition alone does not suffice.

## Existing mathematical information, credited

Peled–Spinka, *Three lectures on random proper colorings of Z^d*, arXiv:2001.11566v2, May 2022, pp. 48–49, repeats this exact open problem. It states that singleton versus arbitrary all-one conjunction is positively correlated by a Kempe-chain argument. Its Figure 13 gives a nine-vertex “dreidel” graph whose q=3 fixed-color marginal fails the FKG lattice condition: conditioning the named vertex u on v having the fixed color gives 23/56, which decreases to 9/22 when w also has that color. The figure was visually checked. This is a known obstruction to the naive lattice-condition route, not a counterexample to the requested positive association. The same source reports negative correlation for two color-equality events; those are different observables. https://arxiv.org/pdf/2001.11566v2 .

Ferreira–Sokal, *Antiferromagnetic Potts Models on the Square Lattice: A High-Precision Monte Carlo Study*, arXiv:cond-mat/9811345, Appendix A, derives same-bipartition two-point positivity using an embedded Ising model; equation (A.15) was read. It is not a full fixed-color association theorem. https://arxiv.org/pdf/cond-mat/9811345 .

Kahn's 2022 *A note on positive association*, arXiv:2210.08653, concerns increasing functions of independent variables and distinctions among positive-association classes; its main statement was read. It does not resolve the bipartite-coloring question. Targeted searches as of 2026-10-02 found no later primary resolution. This is a bounded literature check, not a novelty guarantee.

## Provenance and prior-attempt audit

The requested https://www.unsolvedmath.com/problems/30003338 was attempted and was inaccessible. The fallback is the pinned dataset revision 37e53eabe540fb458758e198be61634bd02ee008. Both imported source files were byte-size/SHA256 verified. The full problem record was read; no research-results key matching the exact ID or report code 15206 was present. The record's short dated literature triage was read, but does not replace the above primary-source checks.

Live all-state exact-ID PR and branch searches were empty. Additional PR searches for positive association, proper colorings, and Peled/Kahn were empty. Exact-ID default-branch code search returned only desk-review metadata. Main has no target entry in state.json or related_target_groups.json, and the target attempt path has no commit history. A recovered local repository with 311 branches and 2,851 commits contains no matching target path or title/ID proof commit. Catalog and assessment give queued 0/5, eligible, no holds, with review hash b186c228ae6ff2c586fe0dde5a98293028d261003fcb07a15983a3cc43fb413a. No previous substantive author attempt was found.

Source PDFs, extracted full texts, images and imported records remain local-only. Public checkpoints will contain authored mathematical notes, source locators and hashes, scripts, exact controls and turn records. Completion estimate 5%, subjective; source review is not a substantive proof turn. The next author turn will test the exact marginal and increasing-event inequalities while respecting the known failure of the stronger lattice route.
