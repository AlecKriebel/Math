# Source and mathematical audit

Target: 30004909 / OWR-8415356-020. Checked 9 October 2026.

## Source match

The complete Végh contribution on printed p. 2946 / PDF page 54 of [Oberwolfach Report 53/2021](https://ems.press/content/serial-article-files/46931) was visually inspected. The next titled contribution begins immediately below it, so the statement is not missing a continuation. The source requires nonnegative, monotone, submodular set functions, zero empty-set value, and singleton value one. It asks for one matroid rank on the same ground set with the two-sided comparison r(S)/alpha <= f(S) <= alpha r(S), for every subset.

No element weights, scalar multiplier of the rank, expanded ground set, or other restriction on the input function appears in that contribution. The sentence naming the rank function uses f while its displayed formula uses r; the report consistently calls the rank r. The source says “constant” without separately writing “for every finite V.” This audit explicitly uses the dimension-independent interpretation of that question, which is also the universal-constant target.

The corpus's clean inequality dropped the denominator alpha on its left side. The submitted argument does not exploit that transcription error: it disproves the weaker, correctly sourced two-sided comparison itself. The full theorem's quantifiers and normalized input class are explicitly restated in REPORT.md.

The official PDF has 613,600 bytes and SHA-256 80b960c10c23bc89b6a74a2b7e1957a65c52fa5f16b15bf5c4aa82602ad16ef7. The report was reused from a same-day verified retrieval and its page was independently inspected here. The official PDF endpoint was also opened again during this audit. A DOI-tool opening failed; the official publisher PDF was accessible. No later correction of this passage was located in the bounded search.

## Adversarial proof checks

- All input hypotheses hold for sqrt-cardinality, with a direct all-pairs proof of submodularity, including empty sums.
- Singletons exclude every loop, exclude rank zero when n >= 1, and force alpha >= 1. Division by sqrt(R) is therefore legitimate.
- A basis exists because the ground set is finite. It is permitted to depend on the proposed approximating matroid, since the comparison is required on every subset.
- At a basis the lower, rather than upper, comparison bounds the total rank by alpha squared. At the full set the upper comparison forces unbounded total value. The direction of both inequalities is correct.
- The full-set cardinality and basis cardinality refer to one unchanged ground set. No sampling, algorithmic oracle assumption, or randomization is used.
- The contradiction uses n > alpha^6 for any proposed fixed alpha, so it refutes a uniform constant rather than only one chosen numerical factor.
- Uniform-matroid sharpness is restricted to the square-root family. The rational family prevents mistaking its exponent for an optimal lower bound over all submodular functions.
- The rational family is a nonnegative convex combination of rank-one uniform rank and free rank. The case m = 1 is included. Its proof avoids dividing by m - alpha and therefore has no missing sign case.
- The proof is an existence obstruction for one ordinary matroid rank. It does not establish anything about an unspecified alternative intended formulation.

## Prior-work and attribution limits

Editorial selection: repository/corpus-history and deduplication details are omitted from this proof-only edition. All mathematical checks, original-source observations, literature-search limits and the disposition are retained. The audit is therefore a narrowly edited edition, not a byte-identical copy.

This is one approach, 1/5, using a single basis/full-set method with two input families. No fresh budget is asserted for any other problem.

The literature check used the exact contribution title, Végh's name, matroid-rank/submodular approximation terms, square-root-cardinality variants, and the n^(1/6) exponent. The primary Goemans-Harvey-Iwata-Mirrokni paper concerns an oracle-learning problem with a different output class. Search results about sums of ranks or approximation under matroid constraints were not treated as solutions of this question. No exact attribution for the displayed elementary obstruction was found; no claim of originality or publication priority follows.

## Disposition

Accept the self-contained negative result for the displayed, dimension-independent, same-ground-set ordinary-matroid-rank formulation. Retain the explicit source correction and bounded-priority qualification. The mathematical proof is complete; external publication and QUEUE changes were outside this audit's scope.
