# Source review and exact complexity-model boundary

## Source language and reduction type

Farrell and Levine, *CoEulerian graphs*, Proceedings of the American
Mathematical Society 144 (2016), 2847–2860, supplies the prior NP-completeness
of HALTING in Corollary 3.2. The inspected [arXiv version 3](https://arxiv.org/pdf/1502.04690v3)
states its source problem on PDF page 2 for nonnegative configurations on
strongly connected directed multigraphs encoded by adjacency matrices.
Loops are allowed. The complexity discussion on page 10 measures edge
multiplicities logarithmically; page 11 expressly uses a polynomial-time
Karp reduction. These facts make the complementary NONHALTING language an
appropriate coNP-hard source.

The report includes the necessary loop-removal relay construction, including
both directions for arbitrary legal executions and the one-vertex case.
It also includes optional signed-input normalization by added loops and
chips, preserving every legal word. This makes the handling of any signed
intermediate lattice representative explicit. The source hardness theorem
is credited prior work, not a theorem claimed as new here.

## Target membership and exact accepted conclusion

Hujter, Kiss, and Tóthmérész, *On the complexity of the chip-firing
reachability problem*, Proceedings of the American Mathematical Society 145
(2017), 3343–3356, [arXiv version 4](https://arxiv.org/pdf/1507.03209v4),
specifies loopless multigraphs with logarithmically encoded adjacency entries
on PDF page 2 and nonnegative configurations on page 3. Its Theorem 12,
pages 8–9, supplies coNP membership. Theorem 1 supplies the halting dichotomy.
Restriction to strongly connected valid inputs preserves membership because
validity is polynomial-time testable.

The report proves the explicit polynomial-time many-one equivalence
NONHALTING(G,x) if and only if REACHABLE(H,X,Y), with loopless strongly
connected binary-encoded directed multigraphs and nonnegative binary-encoded
initial and target configurations. Together with the credited membership
result, this yields coNP-completeness for that exact target language.
The construction does not establish hardness for simple graphs, unary edge
lists, bounded degrees, or bounded total chip count.

## Distinction from the earlier complexity barrier

Tóthmérész, *Rotor-routing reachability is easy, chip-firing reachability is
hard*, European Journal of Combinatorics 101 (2022), 103466,
[arXiv version 2](https://arxiv.org/pdf/2102.11970v2), Theorem 2.3, proves
that a polynomial-time reachability algorithm would collapse the polynomial
hierarchy to NP. Its proof uses recurrence and certificates for nonhalting.
That prior statement is not substituted for the explicit many-one reduction
in this report.

The [Egres question](https://lemon.cs.elte.hu/egres/open/Complexity_of_the_chip-firing_reachability_problem_for_general_digraphs)
asks for coNP-hardness of directed chip-firing reachability. The associated
[chip-firing conventions](https://lemon.cs.elte.hu/egres/open/Chip-firing)
allow signed configurations; hardness on the accepted nonnegative subclass
already suffices for that hardness question. CoNP-completeness is asserted
here for the stated nonnegative target language, without silently extending
the cited membership theorem to another formulation.

## Recorded review and limitations

Proof review and the independent audit inspected the primary definitions
and relevant proofs. The audit independently retrieved all three PDFs and
recorded matching byte counts and SHA-256 hashes. The recorded visual audit
pages are 2 and 11 for Farrell–Levine; 2, 3, 8 and 9 for Hujter–Kiss–Tóthmérész;
and 5 for Tóthmérész. [SOURCE_METADATA.json](SOURCE_METADATA.json) preserves
these public identities and observations.

The audit's bounded public searches on 2026-10-10, together with the
[author publication list](https://tmlilla.web.elte.hu/talks/papers.html),
found no competing many-one result. This is neither an exhaustive literature
search nor a priority certificate. The Egres page's historical open label
does not certify present-day openness.

Edition preparation checked metadata consistency but performed no new
scholarly-source retrieval, source-file rehash, page inspection, literature
search, or mathematical test rerun. Source PDFs, rendered pages, copied
source text, programs, and raw computational outputs are not distributed.
The written analytic proof is independent of every omitted executable.
