# Second independent audit of the order-12 frontier manuscript

## Verdict

**`ACCEPT_FROZEN_MANUSCRIPT_WITH_EXPLICIT_PRESUBMISSION_PLACEHOLDERS`.**

No mathematical, scope, certificate, reproduction, bibliography, build, or
rendering defect was found in the exact frozen manuscript.  The mathematical
draft is accepted within its stated finite and published-premise boundary.
It is not ready for external submission until the human user supplies the
author metadata and a permanent archive identifier.

This verdict binds:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `paper/order12_frontier/main.tex` | 48,398 | `5437afac6f3c3e5ee291e7389939bc6708d20521524bce700eba26e051fbf0b5` |
| `paper/order12_frontier/references.bib` | 4,534 | `8471090ae03babda7794aea6bbcbc6fbcb36ffa8a859a86005bbb0b7ae2f9ec6` |
| `paper/order12_frontier/main.bbl` | 2,484 | `f9789755c4ec0c83b1e2493f5301e7d4d4dfaa4398810aa9e28d22148da4849a` |
| `paper/order12_frontier/main.pdf` | 130,406 | `1084efc8372a5615dca68bc0f80a4fad88557ebfed8930a655126246de5cd8fc` |

The machine-readable evidence is
`reviews/order12_frontier_manuscript_second/evidence.json`, 6,042 bytes,
SHA-256
`2d158338fea8160373d69501bb8ee6aa95526b27d1095c7a4c82df6aaabb990b`.
The audit log is
`reviews/order12_frontier_manuscript_second/RESEARCH_LOG.md`, 1,711 bytes,
SHA-256
`2e154a57fcedc6f1b4d978c48c5638b541b55c901803900dee94d1d679bdaeb7`.
This review was performed independently and does not rely on the stalled
first manuscript review's conclusion.

## Mathematical and scope audit

The manuscript matches the accepted claim boundaries:

- C-035 excludes every order-12 graph with common parameter \(3\), including
  disconnected graphs.
- C-047 excludes connected order-12 graphs with common parameter \(4\).
- C-049 proves \(n\geq\lceil5k/2\rceil\) for a minimum counterexample and
  excludes order-12 parameter \(5\), explicitly conditional on the published
  through-order-11 premise.
- C-050 combines exactly \(k=3,4,5\) and concludes order at least 13 only
  relative to MacGillivray--Mynhardt--Virgile Observation 5.6.
- C-051 gives the unrestricted
  \(\gamma,\alpha,\gamma^\infty\) independent-antineighborhood projection and
  uses minimum-counterexample minimality, not a deletion identity, for the
  \(\theta\) conclusion.

The abstract, main theorem, proof assembly, evidentiary-boundary remark, and
limitations section repeatedly say that the campaign did not reproduce the
all-graph enumerations at orders 10 and 11, that the universal conjecture
remains open, and that no claim is made at order 13 or above.  There is no
scope inflation from finite verification to universal resolution.

The model is consistently the one-guard model: attacks occur only at
unoccupied vertices, exactly one adjacent guard moves, and the successor is
a selected dominating state.  With \(H=\overline G\), the manuscript
correctly uses \(\theta(G)=\chi(H)\), represents a \(G\)-edge by a negative
\(H\)-edge literal, and uses positive \(H\)-edge disjunctions to obstruct
proper colorings.  No complement sign or all-guards variant error was found.

## Certificates and reproduction

The three parameter-three formula/proof censuses and all six hashes match the
accepted C-035 artifacts.  The documented C-035 full-replay command matches
the current command-line interface.

For parameter four, the parent and DoubleLex variable, clause, literal, byte,
and SHA-256 values match the exact manifests.  The normalized RUP hash,
228,381,671-byte LRAT hash, and 64,288,636-byte compressed-LRAT hash all
match the accepted certificate packages.  The documented publication
verifier command was rerun and returned:

```text
VERIFIED_EXACT_DOUBLELEX_CNF_UNSAT_ONLY
verified_marker_count = 1
```

The manuscript keeps exact-CNF UNSAT separate from the reviewed graph
transfer.  Its certificate claims therefore match their actual scopes.

## Prior art, attribution, and disclosure

The structural theorem is presented as an unrestricted, family-level
generalization of Taletskii's planar lemma, not as a wholly new
antineighborhood idea.  The unavailable 2018
Klostermeyer--Krop--MacGillivray manuscript and unresolved priority are
explicitly disclosed.  The manuscript also discloses substantial autonomous
AI assistance, separate adversarial reviews, independent proof checking,
the continuing need for human inspection, and human responsibility for any
submission.

The corrected bibliography entry renders exactly:

```text
Warren A. Hunt, Jr.
```

No attribution or bibliography defect was found.

## Build and visual audit

Using Tectonic 0.16.9, I ran the documented deterministic command twice in
separate clean temporary directories:

```text
SOURCE_DATE_EPOCH=1785074656 \
  tectonic --keep-logs --keep-intermediates main.tex
```

Both builds exited zero.  Their BBL and PDF files were byte-identical to one
another and exactly matched the four frozen hashes above.  The retained and
fresh logs contain no TeX/BibTeX warning, overfull or underfull box,
undefined citation/reference, or multiply defined label.

I rendered all 17 frozen PDF pages at 144 DPI.  Contact sheets covering pages
1--4, 5--8, 9--12, and 13--16 were independently inspected, and page 17 was
inspected separately at its full 1224-by-1584 render resolution.  There is
no clipped or overlapping text, margin overflow, malformed table, broken
glyph, replacement character, or missing page number.  The title, theorem
displays, long hashes, verbatim commands, data-availability text, disclosures,
and bibliography are legible.

## Exact ledger

- Blocking mathematical defects: **0**
- Blocking scope defects: **0**
- Blocking certificate or reproduction defects: **0**
- Blocking bibliography or attribution defects: **0**
- Blocking deterministic-build defects: **0**
- Blocking rendering defects: **0**
- Nonblocking editorial defects: **0**
- Explicit pre-submission gates: **2**

The two pre-submission gates are intentional placeholders:

1. replace `Author metadata to be supplied before submission` with
   human-supplied author metadata; and
2. insert a permanent public archive identifier in Data availability.

These placeholders do not weaken the frozen mathematical result, but they
must be resolved before arXiv or journal submission.
