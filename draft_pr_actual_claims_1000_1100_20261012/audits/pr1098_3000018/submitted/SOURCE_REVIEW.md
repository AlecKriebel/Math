# Source review and exact complexity-model boundary

## Credited prior result and original question

Matthew Farrell and Lionel Levine, *CoEulerian graphs*, Proceedings of the
American Mathematical Society 144 (2016), 2847–2860,
[DOI 10.1090/proc/12952](https://doi.org/10.1090/proc/12952), establishes
NP membership for the larger directed-multigraph halting language in
Section 3. The inspected [arXiv version 3](https://arxiv.org/pdf/1502.04690v3)
states the nonnegative strongly connected conservative graph language on
PDF page 2, gives NP membership on page 10, and explicitly leaves the simple
directed case as a question in Section 3.1 and Table 1 on page 13.

The [Egres problem page](https://oldlemon.cs.elte.hu/egres/open/Complexity_of_the_halting_problem_for_simple_digraphs)
asks whether chip-firing halting is NP-complete for simple digraphs and
attributes the question to Farrell and Levine. Its archived Open Problems
label and displayed last modification of 5 December 2016 are historical
observations, not evidence of preexisting present-day openness.

The maximal stable-capacity observation, total chips at most E-N for a
halting simple input, is also prior work in Farrell–Levine, PDF page 2.
Neither membership nor this observation is claimed as new here.

## Exact accepted conclusion

The report proves NP-completeness under polynomial-time many-one reductions
for halting of nonnegative binary-encoded configurations on finite loopless
simple strongly connected directed graphs. The graph is conservative and
has no dissipative sink. Its main convention permits antiparallel arcs.
The separately accepted appendix proves the same result on the oriented
subclass, forbidding antiparallel arcs. In both constructions, deleting the
specified root leaves a depth-at-most-one acyclic graph, and all initial
chip counts, including their total, are polynomially bounded in the SAT
input length. The construction therefore also gives hardness for unary
chip encoding.

Hardness is an explicit reduction from 3-SAT. A modular bank encodes an
arbitrary nonempty residue predicate by polynomially many distinct simple
counter vertices. Variable and clause banks enforce Boolean assignments
and clause satisfaction through the Chinese remainder theorem. Only the
individual variable primes and products of at most three such primes are
expanded; the global CRT period is never expanded in the output or simulated
by the reduction. A legal checkpoint schedule and least action prove the
two-way equivalence. Section 7 gives a self-contained specialization of
Farrell–Levine's NP certificate method, including the necessary additive
one slack in its path bound.

This is separate from binary directed-multigraph reachability for problem
3000016. Expanding exponentially large binary arc multiplicities would
not prove the simple-graph theorem. The graphs here are generally
non-Eulerian, so no Eulerian-multigraph halting problem is resolved.

## Recorded source inspection and search limits

The independent audit records reuse of previously independently retrieved
Farrell–Levine PDF bytes, with reverified size and SHA-256 hash matching the
proof-review record: 218,260 bytes and
`efe2b90f98723c10490785e14797ffd9f99dacecc2ac2500a31ed7a6e3f24cb1`.
The versioned arXiv abstract and PDF were opened afresh during that audit.
Text inspection covered Sections 3 and 3.1; PDF pages 2, 10 and 13 were
visually inspected through successful rendering of the recorded PDF.
Failed web screenshot attempts are not counted as visual inspection.

The proof-review record reported an Egres access error; the later independent
audit recorded successful text access to the exact question and attribution.
These are distinct historical observations. Public source metadata retains
their chronology, the recorded archived page hashes and sizes, and bounded
search descriptions without reproducing any source body.

The audit's bounded searches on 10 October 2026 identified no competing
exact resolution among checked results. This does not certify novelty,
priority, exhaustive literature coverage, or preexisting current openness.
Acceptance rests on the written proof, not the negative search. The work is
AI-assisted and unrefereed; the separate mathematical audit is not external
human peer review, journal acceptance, or formal proof-assistant certification.

Edition preparation claims no new scholarly-source retrieval, source-file
rehash, source inspection, literature search, or mathematical test rerun.
The report and appendix are complete analytic arguments independent of
every omitted executable. Only aggregate supporting test results and public
bibliographic or verification metadata accompany them.
