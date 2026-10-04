# Source and prior-work gate

Checked 2026-10-04 UTC. Rank 558, ID 30001242, code OWR-3472-013.

## Catalogue identity and retrieval

https://www.unsolvedmath.com/problems/30001242 returned HTTP 403 on direct
retrieval; web retrieval also failed. The denial was not bypassed.

The exact matching record was recovered from the public Ulam AI dataset,
pinned at revision 372682f27c1b0d3d39e75fa63ad7932c7a2e1bde:

https://huggingface.co/datasets/ulamai/UnsolvedMath/blob/372682f27c1b0d3d39e75fa63ad7932c7a2e1bde/problems.json

The existing local 15,458-record file has SHA-256
37067f43734b76ee886b032469836767c34d892de14397ce6aa71da01500e252,
matching the LFS object hash from a fresh read of the pinned public tree
endpoint. It is a provenance/identity source, not mathematical authority.
Neither the corpus nor the extracted catalogue record is published here.

The record asks whether the containment R_m0 in (f_1,...,f_n) has a generic
bound depending only on the dimension d and the prescribed degrees a_i,
for arbitrary standard-graded k-algebras. Its August 2026 generated
literature label says “open.” That label is rejected on primary evidence.

## Primary question and answer in context

Helena Fischbacher-Weitz, joint with Holger Brenner, “Generic bounds for
tight closure,” in *Kommutative Algebra*, Oberwolfach Report 22/2009,
pp. 1211–1214:

- https://ems.press/journals/owr/articles/3472
- https://ems.press/content/serial-article-files/46222
- https://doi.org/10.4171/OWR/2009/22

The entire contribution was read. Its printed p. 1212 (PDF page 56,
zero-based index 55) introduces ordinary membership as a question and
immediately states that the answer requires ring-dependent data, using
parameter ideals in hypersurfaces. The page was also rendered and visually
checked. This is an introductory contrast, not an unanswered conjecture.
The primary setup has n >= d; our d = n = 2 counterexample respects it.

## Companion paper and version check

H. Brenner and H. Fischbacher-Weitz, *Generic bounds for Frobenius closure
and tight closure*, https://arxiv.org/abs/0810.4518v3 .
The current arXiv landing page identifies v3, 30 July 2009, as the latest
version. Its p. 1 explicitly gives the same negative ordinary-membership
answer. This page was read and visually checked.

Read beyond the abstract: introduction and Theorem 2; Definition 2.3;
Construction 2.2 and Lemma 2.4 with proof; Lemma 1.1 with proof; Remark 3.1;
Lemmas 3.2–3.3 with their complete proofs; Theorem 3.4 with its complete
proof; and Remarks 3.5–3.9. In particular Theorem 3.4(c) is ring-dependent.
The closure theorems are context, not dependencies of our counterexample.
No claim is made to re-prove all external references in those arguments.

The paper uses d+1 for ring dimension where the report uses d. Our proof
uses actual dimension two throughout; no shift is imported accidentally.

Publication metadata was verified through the DOI registrant's Crossref
record: *American Journal of Mathematics* 133 (2011), no. 4, 889–912,
https://doi.org/10.1353/ajm.2011.0032 . The publisher page was blocked by
robots, so the publisher PDF was not inspected. The claimed prior
resolution relies on the fully accessible 2009 sources, not an unverified
equivalence of versions.

## Actual repository prior-attempt checks

Read-only checks in AlecKriebel/Math, not merely the queue label:

- PR searches, all states, for `30001242`, `OWR-3472-013`, and the exact
  title: zero results.
- Branch search for `30001242`: zero results, no continuation cursor.
- The default-branch path
  `unsolved_math_prioritization/attempts/30001242`: HTTP 404.
- Commit history for that path: empty list.
- Default-branch code search for `30001242`: no results. This is not treated
  as conclusive because search indexing is incomplete.
- A broader PR phrase search produced only unrelated targets, not a prior
  attempt at this item.
- QUEUE.md blob 59dba610d333684751e889818d21f66aba29cec9 lists the matching
  rank as queued, 0/5. It supplies order, not evidence of no prior work.
- Main was observed at 642e59ea2f6ad2e72920c4e6f57f23c600bfac35. An attempted
  complete recursive-tree inventory failed with a transport error; no
  completeness claim is made for that failed check.

Conclusion: no prior repository attempt found by these actual checks;
the mathematical negative resolution is explicitly prior literature.
Searches for the exact title and combinations of generic degree bounds,
ideal membership, and Brenner confirmed this source chain rather than
an unresolved uniform ordinary-membership assertion.

## Disposition

`already_solved`, one substantive author turn. The proof is self-contained
apart from elementary polynomial-ring and integral-extension facts. It
refutes the requested ring-independent bound in genuine integral-domain
parameter examples, not a weakened or underspecified substitute.

Only original explanation, bibliography, metadata/hashes, and independent
finite controls belong in the public packet. Local source PDFs, extracted
paper text, source-page images, full dataset data, and private context are
excluded. No remote write is authorized by this file itself.
