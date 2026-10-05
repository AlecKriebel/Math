# Random-graph biclique partitions: audited prior negative result

Problem 30002468 / OWR-12861-019, queue rank 721. Disposition: `already_solved`,
one substantive proof/verification attempt of five. This AI-assisted, unrefereed
research record explains a consequence of an existing published theorem. It
claims neither new mathematics nor historical priority for recognizing that
consequence. Identifying and auditing the exact prior-result consequence is
complete; this is not a claim of a new discovery.

## Controlling reading of the frozen packets

The `author/` and `independent_audit/` directories preserve every reviewed byte.
The independent verdict is ACCEPT_PRIOR_NEGATIVE_WITH_NONBLOCKING_CLARIFICATIONS.
Historical statements that review was pending or that no remote writes had
occurred describe their freeze times. This guide records the completed review
and assembled publication without changing that history.

Read the words “fewer than 2^k” in author/PROOF.md as **at most 2^k**. There are
exactly 2^k ordered side assignments when empty sides are allowed. The displayed
union-bound inequality already uses the correct bound. Allowing empty sides
can change the finite value of beta, including on an edgeless graph; both
conventions satisfy the same asymptotic bound and the same strict refutation.
No equality of their finite beta values is asserted.

## Exact result and credit

For G_n = G(n,1/2), let bp denote the minimum number of edge-disjoint complete
bipartite subgraphs partitioning all edges. Pieces may share vertices and need
not be induced; stars and single edges are permitted. Let beta denote the
largest order of an induced complete bipartite subgraph. This beta is neither
the independence number nor the order of an arbitrary non-induced biclique.

Theorem 1.1 of Noga Alon, Tom Bohman and Hao Huang,
[More on the bipartite decomposition of random graphs](https://doi.org/10.1002/jgt.22010),
Journal of Graph Theory 84 (2017), 45–52, supplies an absolute c > 0 such that
bp(G_n) <= n - (2+2c) log_2 n with high probability. The result already appears
in the [2014 preprint](https://arxiv.org/abs/1409.6165).

The authored first-moment argument proves beta(G_n) < (2+c) log_2 n with high
probability. Intersecting the two events requires no independence and yields
bp(G_n) < n - beta(G_n) + 1 with high probability. Thus the probability of the
revised conjectured equality tends to zero. This settles the complete revised
equality in Alon's [2014 OWR contribution](https://ems.press/journals/owr/articles/12861),
printed page 80, rather than substituting the older n-alpha question.

This does not determine an exact finite-n or second-order formula, establish a
matching lower bound, or resolve other fixed p or sparse/critical regimes.

## Source and proof boundaries

Fresh independent primary-PDF retrievals and rendered-page inspection matched
the author-hosted theorem, the arXiv v1 theorem and the OWR question. The pinned
public statement-audit bytes match; that editorial record's source_checked=false
is preserved and is not treated as primary verification. Public hashes, byte
counts, URLs and inspection scope appear in the frozen metadata.

The exact numeric website returned HTTP 403 and its live content was not
inspected. The raw prior AI report remains uninspected. Repository-history
searches provide bounded evidence, not a universal claim that no differently
named attempt exists. The published theorem's proof scope was reviewed, not
formally proved or independently reconstructed in full. In ABH Claim 3.1 the
probabilistic use concerns compatible restricted patterns; unspecified edges
between the two exclusive vertex sets integrate to one. It is not a count of
fully specified union graphs. The independent audit records this caveat.

All 1,100 labelled graphs on zero through five vertices were independently
checked, together with 14,964 hereditary checks, 1,100 exact deterministic-bound
checks, 1,100 explicit star constructions, 20 expectation identities and 320
exact rounding/exponent controls. Three authored and five independent negative
controls distinguish the relevant definitions. These finite tests supplement
the written asymptotic proof; they do not prove a random-graph limit or the
external theorem. Hash checks establish byte identity, not mathematical truth.

## Portable verification

Only Python 3 and its standard library are needed, without network access.
Use the externally supplied SHA-256 of PUBLICATION_MANIFEST.json:

    python3 -B /path/to/30002468/verify_publication.py /path/to/30002468 EXPECTED_MANIFEST_SHA256 --replay
    python3 -B /path/to/30002468/test_publication_integrity.py /path/to/30002468 EXPECTED_MANIFEST_SHA256

The publication verifier uses explicit checks, binds both frozen manifests and
the audit report, rejects extra/missing/changed files and unsafe paths, and
replays in a temporary relocated directory. The frozen suites use assertions:
optimized Python is explicitly rejected, and subprocesses run with assertions
enabled and ignore PYTHONOPTIMIZE. Actual mutations test integrity rejection;
an optimized invocation is also required to fail. These are local reproducible
checks. No reported repository CI checks means no CI pass.

Only authored proof, audit, code/results and public verification metadata are
included. Source PDFs, extracted source text, images, raw dataset records,
private sources, private personal data and private coordination are excluded.
The queue edit changes only this row's Status, Turns and formerly blank Findings;
all other existing bytes, including Chat/DOI fields and the stale embedded
header, remain unchanged. No queue regeneration is used.
