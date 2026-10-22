# Source and prior-work gate

Checked 2026-10-03. Repository: AlecKriebel/Math. Numeric ID 11000020, AMR-109-0020, queue rank 421.

## Source and scope

The requested live URL https://www.unsolvedmath.com/problems/11000020 could not be retrieved by web tools. The existing local imported problem and prior report were read completely. The repository pins UnsolvedMath revision 37e53eabe540fb458758e198be61634bd02ee008. The complete 149 MB source corpus was not re-downloaded or rehashed in this gate, so the imported JSON is background rather than independent current-site verification.

The exact mathematical wording and its boundary were independently verified against the primary Farb book PDF page 30, printed page 23, both extracted text and a rendered image. The target is to find automorphism-theoretic properties selecting one point of M_g; its explicit example concerns maximal-order nilpotent full automorphism groups. The following Hurwitz paragraph introduces Question 2.20 and is not an extra part of Problem 2.19. The source's grammatical shorthand about an automorphism group being “the largest possible order” is normalized to its order being largest; no hypothesis is added.

Define the concrete yes/no subquestion by maximizing full Aut(X) over X with Aut(X) nilpotent. The broader source request is an open-ended programme. A negative answer to the example is not a classification of every possible canonical-point property.

## Prior author-campaign check

- Current main QUEUE row read: queued, 0/5, no linked prior attempt.
- All 439 live branch names were read using five pages of 100 and a final empty page. No branch name matches 11000020, canonical, or basepoint.
- All-state PR searches for 11000020, AMR-109-0020, and canonical/basepoints returned no match. A nilpotent PR search found only unrelated topics.
- Commit search for 11000020 returned no match. Default-branch code search returned no match, a weaker check because indexing can lag.
- Main attempts tree (39 directory entries, not truncated) has no 11000020 directory.
- Current history.jsonl and related_target_groups.json have no target match.
- The full recursive main tree call twice failed with Transport closed; this limitation is retained. The successful directory tree, full branch inventory, PR/commit searches, and current queue were used instead.

No earlier user author campaign was located. The local source-only folder predates this gate and contains no proof attempt. The imported OPEN-TRIAGE report is a third-party research aid, not a user attempt or proof certificate; its unsupported suggestion that nilpotent uniqueness remains open is superseded by the sources below.

## Literature findings and credit

1. MSSV 2002, arXiv:math/0205314v1, section 7.2 and Table 4, supplies full automorphism groups for four genus-9 curves of order 128. Original v1 and updated v2 were retrieved; v1 scope and table were visually checked. This refutes the explicit nilpotent uniqueness proposal once combined with the classical bound.
2. Zomorrodian's 1985 upper bound is recalled with exact original theorem numbers in Schweizer, arXiv:1701.00325, Theorem 2.2(c). The original AMS PDF returned HTTP 403. RESULT.md gives a direct reconstruction of the upper bound, so the maximality inference does not rely on pretending the original proof was inspected.
3. Reyes-Carocca, arXiv:2004.06506v2 (2021; published 2022), treats positive-dimensional nilpotent-action families. Those dimension-constrained maxima are not automatically genuswise absolute maxima. In particular, the genus-3 order-16 family does not contradict nilpotent uniqueness because an order-32 full group occurs.
4. Reyes-Carocca–Speziali, arXiv:2310.07520v2 (2025), Theorem 3.1 gives known positive canonical-point criteria for specified infinite genus classes. The exceptional genus 21 is present in the theorem and is preserved.

No historical priority is claimed for either the negative implication or the elementary bound reconstruction. No assertion of worldwide openness of the broader programme is made.

## Recommendation

Eligible for a credited source-correction packet, not a fresh novelty campaign on the nilpotent example. Count the mathematical reconstruction and verification as author turn 1, per the coordinating instruction. Freeze the complete certificate and perform a separate source/proof audit. A record-level disposition must preserve that the specific example is classically answered while the broad programme is not declared fully closed. No queue edit or PR has been made by this gate.
