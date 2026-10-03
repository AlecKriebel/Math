# Source and prior-attempt gate

Checked 2026-10-03, starting at 08:20 UTC.

## Exact source

- Numeric record: 30003813; code OWR-16164-005; rank 439.
- Requested page:
  https://www.unsolvedmath.com/problems/30003813
  The direct web read returned an internal fetch error.
- The authorized fallback is `ulamai/UnsolvedMath`, immutable revision
  `37e53eabe540fb458758e198be61634bd02ee008`.
- SHA-256 of the complete cached `problems.json`:
  `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`.
- SHA-256 of the complete cached `research_results.json`:
  `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`.
- Both hashes were independently recomputed before selecting the record.
  The imported prior-report entry under this exact code is absent.
  The problem record's imported assessment says that the record contained
  only a placeholder sentence. That assessment conflicts with the corrected
  statement and the directly checked source, so it is not used as evidence.

The full official OWR report was obtained and checked as text. The target
page was also rendered and visually inspected: printed page 1410, PDF page
30. The source is the concluding paragraph of the Josuat-Vergès abstract,
joint with Ayyer and Ramassamy, entitled *Enumeration of cyclic orders and
consecutive coordinates polytopes*, printed pp. 1408-1410.

The report is Oberwolfach Reports 15 (2018), issue 2, pp. 1381-1464, DOI
10.4171/OWR/2018/23. The workshop was held 13-19 May 2018; the publisher
lists publication on 12 April 2019. The upstream title's parenthetical 2019
does not change the workshop year.

- [Official source](https://publications.mfo.de/bitstream/handle/mfo/3645/OWR_2018_23.pdf?isAllowed=y&sequence=1)
- [Publisher metadata](https://ems.press/journals/owr/articles/16164)
- [Immutable fallback](https://huggingface.co/datasets/ulamai/UnsolvedMath/tree/37e53eabe540fb458758e198be61634bd02ee008)

The exact final source sentence is quoted in `PROOF.md`; the mathematical
definition and all quantifiers are restated there. The source asks for the
combinatorics of h-star, with no explicit restriction to a cyclic-order
statistic. The narrower cyclic-order-specific interpretation remains outside
the present claim.

## Current literature and attribution

The following primary sources were inspected, not inferred from titles:

1. Stanley (1986), *Two poset polytopes*, Definition 1.1, Corollary 1.3,
   Theorem 4.1, and Section 5.
   https://math.mit.edu/~rstan/pubs/pubfiles/66.pdf
2. Coons and Sullivant (2023), *The h-star polynomial of the order polytope of the
   zig-zag poset*, Section 1.4, especially Theorem 16 on PDF page 8.
   This restates Stanley's natural-label P-partition formula from
   Enumerative Combinatorics, volume 1, Theorem 3.15.8. The theorem page was
   also visually inspected.
   https://www.combinatorics.org/ojs/index.php/eljc/article/download/v30i2p44/pdf/
3. Ayyer, Josuat-Vergès and Ramassamy (2020), *Extensions of partial cyclic
   orders and consecutive coordinate polytopes*, Theorems 2.5 and 2.9 and
   Remark 2.6, printed pp. 279-281.
   https://ahl.centre-mersenne.org/item/10.5802/ahl.33.pdf

AJR's signed family has the opposite sign convention and a dimension shift.
Its Theorem 2.5 concerns volume and integrality. Its Theorem 2.9 is for the
upper-bound consecutive-sum family, so it is not treated as a theorem about
the signed-family h-star polynomial. Coons-Sullivant's swap theorem is also
not silently generalized to arbitrary sign words.

Searches included the exact problem title, the report identifier, signed
adjacent-sum polytopes, sign sequences and Ehrhart polynomials, and the
authors' consecutive-coordinate-polytope papers. No directly checked
publication was found explicitly closing this exact OWR problem. This is a
bounded literature search and cannot prove absence. The candidate is
credited as an elementary application of Stanley's classical theory, not a
novel discovery or a confirmed historical prior resolution.

## Prior attempts and related targets

Repository checks used `AlecKriebel/Math` main at
`ae20170da67ad1d891f9852ca3ed6df74a869513`.

- `unsolved_math_prioritization/QUEUE.md` gives rank 439, queued, 0/5.
- The complete recursive queue subtree was returned without truncation
  (9,376 entries); it contains no path matching the ID, code, or signed
  adjacency name.
- The complete recursive `problems` subtree has 315 entries and no match.
- The 112-entry repository-root tree has no matching named research folder.
- The returned current `state.json` and `history.jsonl` contain no occurrence
  of the numeric ID or problem code.
- GitHub issue/PR searches for the exact ID and for adjacency returned no
  matches; a commit search for the exact ID returned no matches.
- The repository's related-target group file does not list this ID.
- The imported problem collection was checked for adjacent-polytope titles
  and the same report DOI. No duplicate of this exact statement was found
  in those matches; the other report questions have different targets.

These checks found no user-authored prior attempt. Imported source and
literature-triage records were not counted as such attempts.

Root and queue-specific `AGENTS.md` and the queue README were read. This
packet was kept in a dedicated local folder. At the source-gate stage, no queue program, public checkpoint, outreach,
release, or remote mutation had been performed.

## Scope and success test

For every n >= 1 and all 2^(n-1) sign words, prove that each coefficient of
h-star counts an explicitly defined finite set of permutations. Account for
all lattice-boundary points, m=0, natural labeling, and both sign conventions.
A self-contained proof plus exact independently replayable checks meets the
literal mathematical target, subject to independent review.

The source gate itself consumed no author attempt. The subsequent explicit
reflection, descent-class formula, and proof are recorded as substantive
author attempt 1/5.
