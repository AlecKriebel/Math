# Independent historical priority audit: PR311 / problem 30005303

**Verdict.** The negative answers to source Conjectures 2 and 3 already follow from an explicit published binary four-cycle probability law. Gandolfi–Lenarda Lemma 5.2 contains exactly the submitted TURN_1 law after a graph-preserving coordinate rotation. The publisher records publication on **13 April 2017**, before the 2022 problem statement. The older paper does not assert MTP2, but its actual table satisfies that hypothesis by the complete derivation below. This is a verified specialization of a primary example, not an inference from metadata or a negative search. The separate source Conjecture 1 closure claim is not settled historically by this finding. No equivalent prior closure theorem was established in this audit; that is an exact remaining historical gap, not evidence of novelty.

## Independence and scope

The authenticated original is Lauritzen, *Two open problems in graphical models of algebraic nature*, printed pp. 3125–3126 in [OWR 2022/55](https://ems.press/content/serial-article-files/46992), DOI 10.4171/OWR/2022/55. The retrieved publisher PDF is exactly 600619 bytes, SHA-256 `56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65`. Printed pp. 3125–3126 were visually inspected and references p. 3127 read.

Source-only criteria were frozen at actual UTC 2026-10-04T16:30:50.969209+00:00. The first independent historical conclusion, finding Kahle–Sullivant Example 6.5, was frozen at 16:35:56.009901+00:00. The older Gandolfi–Lenarda law was found and separately frozen at 16:39:43.581192+00:00, **before any candidate body read**. These original conclusions remain unchanged, including their then-unresolved date qualifications. Root's stated release gate is 16:37:57.234303+00:00; root reported having authenticated the initial frozen criteria and first conclusion before release. I did not read root's gate file or conclusions.

After explicit release, only the snapshot files `TURN_1.md`, `TURN_2.md`, `SOURCE_GATE.md`, and `SOURCE_RECHECK_2.md` under `audits/pr311_30005303/snapshot/unsolved_math_prioritization/attempts/30005303/` were read, first at 16:40:13.982971–16:40:13.983868+00:00. Exact bytes, hashes, modes and absolute paths appear in `released_candidate_input_manifest.json`. No candidate code, inherited priority gates/reviews, PUBLICATION_SUMMARY, root/sibling conclusion files, other-family artifacts or other candidate material were opened. One attempted later citation search used an incorrect nonexistent snapshot path and returned only a filesystem error; it read no body. A general web search incidentally returned an unrelated repository STATUS snippet; it was not opened or used. Primary source bodies and relevant search snippets are distinguished in the ledger. Third-party PDFs, text, renderings, search output and raw command captures remain private and excluded from publication by `.gitignore`.

## Exact comparison target

For a finite graph G on binary coordinates, source Conjecture 2 asks whether every **global** G-Markov MTP2 probability mass function, including zeros, has a product representation by finite real clique factors. Conjecture 3 replaces MTP2 by closure of the support under coordinatewise meet and join and is stronger. MTP2 implies that support closure. A valid negative answer therefore requires the same law to satisfy global Markov, all MTP2 inequalities and an obstruction to finite clique factorization. For real factors producing a nonnegative mass function, taking absolute values preserves the product, so signed factors do not remove the obstruction.

Null conditioning events impose no condition. Pairwise Markov is not a general substitute for global Markov at zeros. On C4 the only nontrivial separations are 1 from 3 by {2,4} and 2 from 4 by {1,3}, with their reversed ordered versions, so pairwise and global coincide there. Exact factorization and closure of factorizing laws are distinct; a balanced polynomial identity is necessary even for closure, whereas satisfying toric identities alone does not establish exact factorization at zeros. All-clique versus maximal-clique conventions agree after absorbing smaller factors, and C4 has only edges as maximal cliques.

Source Conjecture 1 instead asks closedness of the MTP2 Ising/edge-factorizing class. TURN_2 proposes the more precise identity F2(G) = closure A(G), with finite nonnegative unary/edge factors in F2, and strictly positive ferromagnetic exponential models in A. Literal edge-only isolated-coordinate conventions are treated in its §6. A Markov MTP2 law outside the factorizing class disproves Conjecture 2 without disproving Conjecture 1.

## Earliest confirmed qualifying published law

[Gandolfi and Lenarda, *A note on Gibbs and Markov random fields with constraints and their moments*](https://msp.org/memocs/2016/4-3/memocs-v4-n3-p13-p.pdf), DOI 10.2140/memocs.2016.4.407, Lemma 5.2, printed pp. 415–417, gives C4 with edges 12,23,34,41 and the law

\[
L=\{x\in\{0,1\}^4:x_3=x_4\},\qquad
p(x)=\begin{cases}2/9,&x=1111,\\1/9,&x\in L\setminus\{1111\},\\0,&x\notin L.\end{cases}
\]

It proves global Markov and failure of its Gibbs extension property; Example 6.3, printed p. 418, also identifies the constraint with edge 34. The [publisher article record](https://msp.org/memocs/2016/4-3/p13.xhtml) states publication 13 April 2017 and embeds `citation_publication_date=2017/04/13`. The volume is nominally 2016; the PDF says received 14 September 2016 and accepted 12 January 2017. None of those alternative dates is substituted for the verified publication date. This is the earliest qualifying example **confirmed here**, not a claim that every earlier publication has been exhausted.

The following additions are independent mathematical checks of the published table:

1. **Lattice support.** Equalities of coordinates are preserved by minimum and maximum, so L is a Boolean sublattice.
2. **MTP2, including zeros.** Use unnormalized weights w(1111)=2, w=1 elsewhere in L and w=0 off L. If either input is off L, w(x)w(y)=0. On L, comparable inputs give equality in the MTP2 inequality. Incomparable inputs cannot include the top element 1111, so their product is 1; their meet/join product is either 1 or 2. Thus every inequality holds. The independent verifier also checks all 256 ordered input pairs exactly.
3. **Global Markov.** Under conditioning on X2,X4, X3=X4 is constant, so X1 is independent of X3. Under conditioning on X1,X3, X4=X3 is constant, so X2 is independent of X4. These are all C4 separations. Positive conditioning events suffice and zero events are vacuous. Exact conditioning tables confirm every minor is zero.
4. **Finite signed factor obstruction and closure obstruction.** Any edge product, even with zero or signed finite entries, must satisfy

\[
p_{0000}p_{0111}p_{1011}p_{1100}
=p_{0011}p_{0100}p_{1000}p_{1111}.
\]

For each of the four edges, the two sides use the same multiset of edge configurations; multiply the factors without division. For this p, the products are 1/9^4 and 2/9^4, with difference −1/6561. The polynomial also vanishes on every limit of factorizing laws. Hence p is outside that closure, and in particular has no finite clique factorization.

These checks yield explicit negative answers to both source Conjectures 2 and 3 from a pre-source published probability table. It is fair to describe the MTP2 specialization as a derivation supplied by this audit, because the old paper does not label the law MTP2. It is not fair to describe the underlying qualifying witness as newly discovered in TURN_1.

## Exact relation to TURN_1 and the six-cycle extension

TURN_1 uses p(a,a,b,c)=2^(abc)/9, supported on X1=X2. Set

\[
(x^{new}_1,x^{new}_2,x^{new}_3,x^{new}_4)
=(x^{old}_3,x^{old}_4,x^{old}_1,x^{old}_2).
\]

This is a C4 rotation, preserves the ordered lattice and 1111, and moves old equality X3=X4 to new equality X1=X2. The two probability tables agree on **all 16 configurations**, including all zeros. The old obstruction becomes exactly

\[
p_{0000}p_{0011}p_{1101}p_{1110}
=p_{0001}p_{0010}p_{1100}p_{1111},
\]

the submitted quartic. Thus there is exact witness priority, stronger than merely knowing its invariant or a similar mechanism. TURN_1 already credits Geiger–Meek–Sturmfels for the invariant and makes no historical novelty claim; the actionable historical correction is to credit Gandolfi–Lenarda for the exact law and state the elementary MTP2 specialization explicitly.

TURN_1's C6 law p(a,a,b,b,c,c)=2^(abc)/9 is a duplicate-coordinate lift of the same three-bit core q(a,b,c), as checked on all eight core states. Its equality blocks are {1,2},{3,4},{5,6}; their quotient graph is a triangle. For any separator C, a block touched by C is constant conditionally. Untouched blocks remain internally connected, and any two untouched blocks are joined by a boundary edge. Hence they all occupy one component of C6 minus C. Separated sets A and B cannot both contain unfixed blocks, so at least one side is conditionally constant. This proves the full global Markov property, including separators involving only part of an equality block.

The six-cycle obstruction uses the four even-parity core states on one side and odd-parity states on the other:

\[
p_{000000}p_{001111}p_{110011}p_{111100}
=p_{000011}p_{001100}p_{110000}p_{111111}.
\]

Every edge projection multiset balances. The products are again 1/9^4 and 2/9^4. Lattice/MTP2 arguments are unchanged. Independent exhaustive verification checks 4096 MTP2 pairs and 252 ordered nontrivial separations with 6384 unique conditional 2×2 minors, all successful. The candidate's larger conditional-equality count uses a different enumeration convention; no inference of error follows from that count difference.

No primary preexisting C6-specific table was identified in the bounded searches recorded here. This does not establish its novelty. The exact deduction from an old core law establishes the scope of the extension; its contribution could be stated as a transparent C6 lift with attribution. It cannot make the universal negative answers newly resolved, because C4 already refuted them.

## Additional primary comparisons and false equivalences excluded

| Primary body actually checked | Actual scope | Priority implication and exact gap |
|---|---|---|
| [Geiger–Meek–Sturmfels 2006](https://math.berkeley.edu/~bernd/AOS0092.pdf), Theorems 3.1–3.2, printed p. 1470; Proposition 1 and (4.10), p. 1478; Examples 7–8, p. 1480 | Exact factorization requires toric membership and A-feasible support; closure requires toric membership. Proposition 1 supplies C4 quartics. Examples distinguish Markov, closure and factorization. | Established algebraic mechanism. Examples 7 and 8 both fail MTP2 under every one of the 16 coordinate flips; permutations preserve MTP2, so no flip/permutation recoding qualifies. These examples alone do not settle the source MTP2 claim. |
| [Kahle–Sullivant, arXiv 2411.03139v1](https://arxiv.org/pdf/2411.03139v1), Example 6.5, p. 13; Definition 2.4, p. 3; Theorem 6.1, p. 10 | Example 6.5 gives the exact C4 equality-block lattice L={∅,12,3,4,34,123,124,1234}, global Markov, and a violated quartic. Theorem 6.1 assumes **natural** lattice support. | Independent later explicit negative C3 example. Its bottom-heavy normalized weights 7,1,…,1 also satisfy MTP2 by the dual corner argument, so qualify for C2. The published numerical sentence overlaps the empty entry with “S∈L”; normalized reading excludes ∅. The example's general all-laws-on-L statement makes the comparison independent of repairing that typo. Theorem 6.1 is not a positive answer to general C3: atom {12} has rank 1 and cardinality 2. |
| [Fallat et al. 2017](https://discovery.ucl.ac.uk/id/eprint/10058843/1/Total-positivity-in-Markov-structures.pdf), Example 5.4; Theorem 6.1; Corollary 7.3; Theorem 7.5 | MTP2 can fail the intersection axiom. Faithfulness theorem assumes a graphoid. Factorization statements impose decomposability or strictly positive pair potentials. | These conditions cannot be silently imposed at the equality-block boundary. No general zero-inclusive factorization/closure answer follows. |
| [Lauritzen–Uhler–Zwiernik 2021](https://web.math.ku.dk/~lauritzen/papers/AOS2007.pdf), §4.4, printed p. 1448; Example 4.7; Lemma 4.9 and Corollary 4.10 | MTP2 intersections with an **extended** exponential family are compact; full support results have positive-margin conditions. | The extended family already includes limits by definition. Its compactness does not identify finite edge-factorization at boundary points. No equivalence to TURN_2's boundary identity was established. |
| [Kolmogorov–Rother 2007, author-hosted manuscript](https://www.microsoft.com/en-us/research/wp-content/uploads/2007/01/PAMI07-QPBO.pdf), §§2.1–2.2, manuscript pp. 4–7 | Binary submodular energies admit nonnegative normal forms, a cut representation, and flow as an energy reparameterization. | Confirms the classical tool expressly attributed by TURN_2. The checked statement is not a zero-inclusive MTP2 finite-factor compactness theorem. |

The [primary arXiv history](https://arxiv.org/abs/2411.03139) dates Kahle–Sullivant v1 to 5 November 2024 at 14:31:16 UTC; the PDF displays 6 November. Metadata saying a later journal version was accepted was not treated as a read journal theorem or as its publication date.

Citation chains additionally reached Moussouris 1974, Matúš–Studený 1995 and Onural 2016. Moussouris's publisher abstract/metadata were accessible but its original full body was not; the precise binary law used in GMS was checked from that primary GMS paper. A supposed DML fulltext link resolved to a different-title paper and was rejected. Matúš–Studený's author-hosted primary body and example catalogue were inspected; no fully specialized binary MTP2 witness was established. Onural's primary body was inspected, but its constraint/clique scope cannot be specialized into the exact fixed-G target as a positive result; Gandolfi–Lenarda explicitly treats that distinction. These are limitations, not blanket claims that the works contain no relevant result.

## Reproduction, disposition and remaining gap

`verify_laws.py` is independently written verification code, with no candidate code read. It enumerates the full state spaces, tests all meet/join inequalities, enumerates every disjoint (A,B,C) separation while summing over leftover coordinates, checks all conditional 2×2 minors in integer arithmetic, and checks every edge-projection multiset. Fractions are exact. The output is deterministic. Two fresh executions produced identical 65252 bytes, SHA-256 `2f70112c513b0f9098b1c2813a465c0c1f939bb09c037a892dfd0ad7656a0357`. Reproduce with `python3 verify_laws.py --output NEW_OUTPUT.json`; it refuses to overwrite existing outputs. The command streams contain the actual execution timestamps and exit statuses.

The strongest verified historical result is exact pre-2022 priority for the C4 witness and hence already available negative answers to Conjectures 2 and 3. The strongest verified extension result is the candidate C6 law's valid lift and exact obstruction, with prior C6-specific publication history unresolved. The C1 identity needs its own proof audit and historical comparison: this report does not independently certify the entire TURN_2 proof or infer newness from its searches. Consequently a statement that the packet gives a full mathematical answer can be evaluated by combining an independently valid C1 proof with already known negative answers; a statement of entirely new full resolution would fail this priority distinction. The released files explicitly disclaim historical novelty, and this report does not allege intent or plagiarism.

Concrete attribution required before promotion: cite Gandolfi–Lenarda Lemma 5.2 for the exact C4 table; present the MTP2 specialization and rotation; cite Kahle–Sullivant Example 6.5 for the later explicit lattice-support failure; retain GMS credit for the quartic; state C6 as a lift unless its independent prior history is established; separate any prospective C1 contribution from the old negative answer. No publication, merge, Git mutation or external communication was performed.

The final input/output manifest records actual measured modes before and after the final chmod, real seal times, hashes before and after, and preservation of all earlier frozen bytes. The research log records nonmonotone completion estimates; completion means this bounded independent audit and its artifacts are finished, not that all possible prior literature has been exhausted.
