# Independent acceptance: problem 30001669

## Verdict

**Accepted as `already_solved`: the proposed universal assertion is false by a published 2015 result.** This is a credited prior resolution, not a new solution. One mathematical approach was used: identifying and specializing the published existence theorem. This audit and its regression checks are verification of that approach, not additional solution attempts.

The reviewed author archive has 10,114 bytes and SHA-256 `15bb36b2d492b2ace008a6b851b31a3893ec0a559ccc3853a2d709f58f3ed96f`; its manifest pin is `d1d79514b2851823f47345677bfa66f53152f1922562b1040f7dd8882028c620`. The unchanged archive is included as `AUTHOR_SAFE_FREEZE.zip`. No correction to its mathematical conclusion is required.

## Exact question and applicable prior result

The official Oberwolfach report places Noga Alon's question on printed page 74. Its arrows point from the witness to every member of a subset of at most 100 vertices. It asks about all finite directed graphs and cycles of length at most 100. Thus the relevant condition is a common in-neighbor, not a common out-neighbor or a dominating set for the whole graph. [1]

Anbalagan, Huang, Lovett, Norin, Vetta and Wu define `(k,l)`-digraphs on printed page 80 and prove their finite existence in Theorem 11, page 83. The definition uses the same arrow orientation and all subset sizes up to `l`. Substitution `(k,l)=(101,100)` satisfies Alon's premise and excludes his conclusion. [2]

The publisher identifies this as a conference-proceedings publication dated 13 August 2015, not merely an unpublished manuscript. The cited preprint identifier is arXiv:1504.03602. A bounded search found no correction withdrawing the relevant result; that is not an exhaustive literature-clearance claim. [2,3]

## Independent proof-boundary analysis

The following checks make the specialization precise rather than relying on an abstract or title.

1. **Finite base and orientation.** The published construction is on a finite cyclic group. Its relation has the form `x -> y` when `x-y` belongs to a chosen set `Y`. The difference-cover identity yields, for any two targets `a,b`, elements `r,s` with `a-b=r-s`; then `a+s=b+r` points to both. This is exactly the needed direction. Repeated targets also handle a singleton.
2. **Base girth.** For the relevant construction choose `K=9900!`. A zero sum of `j` elements of `Y`, where `1 <= j <= 9900`, would repeat to a zero sum of `K` elements because `j` divides `K`. The additive construction excludes the latter. Consequently the base has no positive closed walk shorter than 9901, in particular no loops. This verifies the factorial divisibility step in the inspected proof, conditional on its stated additive-number-theory input.
3. **Positive power.** Use arcs arising from walks of lengths 1 through 99. The source's phrase about walks of bounded length must be read with the positive-length, loopless-power convention here. Adding length-zero walks would create loops and destroy the girth statement; the author packet explicitly disallows this. This convention is sufficient for the construction, so the source's shorthand does not invalidate its application.
4. **Strict cycle bound.** A directed cycle with `t <= 100` arcs in the power lifts to a nonempty closed base walk with length between `t` and `99t`. Its length is at most 9900, strictly below 9901. Every nonempty closed directed walk contains a directed cycle: select a shortest nonempty closed segment, which has no internal repetition. This contradicts base girth. Equality at 9900 would not suffice if the base bound were incorrectly weakened to 9900.
5. **Every subset size.** For `2 <= m <= 100`, first dominate two targets in the base, then successively dominate the previous witness together with the next target. The final witness reaches each target by a positive walk of length at most `m-1 <= 99`. Thus the proof works directly for each subset size, even though the displayed final paragraph of the published proof writes `|S|=l`. A singleton already has a predecessor in the base. The empty subset has any vertex as a witness because the finite group is nonempty. No unjustified exact-size padding is needed.
6. **Simple, loopless digraph.** The relation is a set of ordered pairs, so parallel arcs are unnecessary. Girth at least 101 excludes loops and opposite arc pairs. A witness is necessarily outside the subset it dominates: otherwise one of the required arcs would be a loop. These examples therefore remain counterexamples under the stricter ordinary simple-loopless interpretation.
7. **Existence of a cycle.** Every singleton has an in-neighbor. Following predecessors in a finite nonempty graph eventually repeats a vertex and produces a directed cycle. The example has long cycles; the claim does not exploit an acyclic graph with a vacuous girth convention.

I inspected both text and rendered pixels of the original question and the definition, additive construction, and Theorems 10–11. Fresh downloads of both official PDFs reproduce the author-recorded hashes and byte counts. Haight's underlying existence result is a cited dependency, not newly proved or independently reconstructed here. These elementary boundary checks are authored audit reasoning; no source passage or PDF is reproduced in this archive.

## Corpus reconciliation

All three complete input files reproduce the supplied byte counts, SHA-256 values and record counts. The uniquely matching record has problem identifier 30001669, number OWR-4791-028 and rank 832. The statement is 241 UTF-8 bytes with SHA-256 `2117b75dcc957ad67a89583a8434249e2f924eca4e28d39ed1641a5602e26fda`.

The research-results mapping genuinely has no entry for that problem number. The review fingerprint was recomputed from the complete record paired with `{}`, using Python's default JSON options and `sort_keys=True`: 3,626 bytes, SHA-256 `d155d5ff1ec1c49ab26c0c03207cd027a66c48aedc993a29fe538d941b2b4bc4`. Both values match the catalog and the frozen packet. An absent research report does not erase the literature assessment inside the main record; that assessment was reviewed and its open-status conclusion is superseded by the published counterexample theorem. Only hashes, byte counts and match results are reproduced here.

## Execution and adversarial review

Both author scripts were read before execution and matched their frozen pins. Their harness ran under normal Python and `-O`, including normal and optimized replays of original and relocated packages. Both harness outputs equal the packaged `VERIFICATION.json` byte for byte. All eight author integrity mutations and eight semantic mutations were rejected in both modes.

The independent harness separately runs four verifier replays, 14 integrity mutations and 24 re-manifested semantic mutations in both Python modes, plus wrong-external-pin tests, 100 strict lifting inequalities, 99 recursive subset-size checks and six synthetic graph fixtures. The fixtures check direction, empty-set nonvacuity, positive-walk behavior and girth; none is presented as an actual 100-dominating adjacency certificate. Normal and optimized independent harness outputs agree byte for byte.

`verify_audit.py` checks this audit's externally pinned exact flat inventory and hashes, the unchanged author archive, its member inventory and payload hashes, and key acceptance fields. Run with the audit manifest hash from the external receipt:

    python -B verify_audit.py --manifest-sha256 EXTERNAL_AUDIT_MANIFEST_SHA256
    python -B -O verify_audit.py --manifest-sha256 EXTERNAL_AUDIT_MANIFEST_SHA256
    python -B independent_checks.py

These checks validate frozen files, selected semantics and regression tests. They are not a formal proof of the published theorem or an exhaustive adjacency/subset enumeration. Replacing an externally trusted manifest pin changes the trust boundary; neither checker claims to validate arbitrary new scholarly metadata solely because it was re-manifested.

## Scope and publication boundary

There is no unresolved mathematical objection to classifying this problem as already solved negatively. There is no novel-resolution credit or newly enumerated counterexample. No external publication, repository mutation or communication was performed during this audit.

The safe archive contains authored audit/acceptance/checking material, public verification metadata, and the unchanged authored safe packet. It excludes source PDFs, page images, source extracts, input datasets, records, research reports, private sources and coordination material.

## Public references

1. *Combinatorics*, Oberwolfach Reports 8 (2011), no. 1, pp. 5–83; Noga Alon's problem at p. 74. DOI: https://doi.org/10.4171/OWR/2011/01 . Official PDF: https://ems.press/content/serial-article-files/46314?nt=1 .
2. Yogesh Anbalagan, Hao Huang, Shachar Lovett, Sergey Norin, Adrian Vetta, and Hehui Wu, *Large Supports are Required for Well-Supported Nash Equilibria*, APPROX/RANDOM 2015, LIPIcs 40, pp. 78–84. Definition p. 80; construction pp. 82–83; Theorem 11 p. 83. https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.APPROX-RANDOM.2015.78 .
3. The authors' preprint record: https://arxiv.org/abs/1504.03602 .
