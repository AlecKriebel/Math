# Sources, definitions, attribution, and limits

Checked 2026-10-03 UTC.

## Primary statement

The requested entry is https://www.unsolvedmath.com/problems/30005832 , OWR-14298166-010. A direct request returned HTTP 403. The catalogue fallback supplied the identifier, title and source, but its status assessment was not treated as mathematical evidence.

The official MFO report was then retrieved and read directly:

https://publications.mfo.de/bitstream/handle/mfo/4161/OWR_2024_15.pdf?sequence=4

The question is in Aaron Potechin's contribution, joint with Aaron Zhang, printed p. 927, following the explanation of total coefficient size on p. 926. It asks for natural examples where fractions give large savings for Nullstellensatz and/or Sherali–Adams. The following discussion mentions proof support size as another comparison and gives pigeonhole lower bounds. Neither a numerical meaning of “greatly” nor a formal definition of “natural” is supplied. This is why the present packet does not silently interpret an explicit polynomial factor as a certified complete resolution of the intended question.

The official report DOI is https://doi.org/10.4171/OWR/2024/15 . Direct DOI fetching failed in the research tool, while the official MFO PDF succeeded. The wording and surrounding context were checked against that PDF, not against a search snippet. Extracted snippet typography for exponents in the pigeonhole theorem is unreliable; no new pigeonhole claim is derived from it here.

## Exact coefficient measure and known example

Potechin–Zhang's 2024 paper was retrieved at

https://drops.dagstuhl.de/storage/00lipics/lipics-vol297-icalp2024/LIPIcs.ICALP.2024.117/LIPIcs.ICALP.2024.117.pdf

DOI: https://doi.org/10.4230/LIPIcs.ICALP.2024.117 .

Relevant locations:

- Definitions 5–9 / Remark 10, printed pp. 117:4–117:5: twin variables, literal monomials, minimum coefficient mass, normalized monomial axioms and their weakenings. Boolean and twin corrections are not charged by this convention.
- Proposition 12, p. 117:6: the signed-function dual lower-bound criterion.
- Appendix A, p. 117:16: the published six-variable example, fractional mass at most 14 and proof support at least 17. The packet reconstructs it and supplies an exact family computation; the existing separation is explicitly credited.
- Introduction and concluding questions: the broad fractional-savings question persists in this paper. Its mere LP formulation and its small example are not a large-family naturalness theorem.

The paper's actual title is *Bounds on the Total Coefficient Size of Nullstellensatz Proofs of the Pigeonhole Principle*. The shorter catalogue label was not used as an exact title.

## Earlier full version and proof-system terminology

https://arxiv.org/abs/2205.03577 (v1, 7 May 2022) and https://arxiv.org/pdf/2205.03577 were checked directly.

Its Definition 16 calls the static equality-axiom plus nonnegative-monomial remainder formulation “resolution-like.” The 2024 article discusses Sherali–Adams in relation to these ideas. The present theorem's primary claim is Nullstellensatz. Its optional extension specifies the complete alternative syntax and mass itself; it does not rest on a blanket equivalence of all systems called Sherali–Adams.

## Established cardinality encoding

Eén–Sörensson, *Translating Pseudo-Boolean Constraints into SAT* (2006), Section 5.4, describes half/full-adder networks for pseudo-Boolean constraints. This supports credit for the encoding method, not first priority of any bound in this packet.

- Publisher DOI and bibliographic page: https://doi.org/10.3233/SAT190014
- Author-hosted URL: https://minisat.se/downloads/MiniSat%2B.pdf
- Readable university-hosted copy used after the author-hosted direct fetch returned 502: https://www.ccs.neu.edu/~pete/courses/Decision-Procedures/2007-Fall/readings/Een-Sorensson-Translating-Pseudo-Boolean-SAT.pdf

The title, authors, 2006 publication and Section 5.4 content were verified. Our fixed gate encoding uses all forbidden full tuples, so it is specified independently of any optimized clause encoding in an implementation.

## Bounded duplicate and priority checks

The live repository queue entry for this exact identifier was `queued`, `0/5` before this work. Read-only all-state PR searches for the exact identifier, fractional/coefficient wording and algebraic-proof wording did not locate a mathematically matching prior repository attempt. A related-word search returned unrelated coefficient and geometric-projection work, which was not treated as a duplicate. The cached catalogue search found only this entry with fractional coefficients plus either named proof system. This is a bounded check, not a claim that no external researcher has considered the construction.

Public searches included the exact coefficient-measure phrase with fractional, cardinality, adder and logarithmic terms, as well as 2025/2026 variants. They found the Potechin–Zhang work and established SAT-encoding literature; no exact earlier occurrence of the displayed adder bound was verified. Search absence does not establish novelty, and no “first” claim is made. The broader current status has not been exhaustively certified.

## Verification and publication boundary

The dependency-free checker uses only integers and exact rational arithmetic. It verifies local truth tables and ordinary polynomial identities, generated full certificates through 256 inputs, all small circuit inputs through eight bits, lower-bound avoiding witnesses, the published-gadget replication dual against every weakening through seven variables, and exact large-parameter formulas. There are 5,757 passing assertions. Its large-parameter controls do not enumerate or solve large formulas.

The public packet contains authored mathematics, the checker and its output. Source PDFs, extracted full texts, imported catalogue records, server response bodies and research-only numerical exploration are intentionally not part of the public packet. The exact frozen version should receive independent adversarial review before any publication.
