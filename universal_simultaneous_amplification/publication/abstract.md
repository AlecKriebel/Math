# Abstract draft

> **DRAFT — NOT SUBMITTED.** Prepared for possible submission to PLOS
> Computational Biology. The human author must approve the final text and
> paste it into the submission portal.

**Manuscript title:** *No universal death–birth amplifier on a finite weighted
population structure*

**Word count:** 164 words by the Markdown plain-text extraction used for this
package (the LaTeX-source extraction reports 159 because it handles math tokens
differently).

We ask whether a finite loopless weighted population structure can strictly
increase uniformly initialized single-mutant fixation probability, relative
to the same-order complete graph, under death–birth updating for every mutant
fitness (r>1). For complete directed support we derive the first (1/r)
correction exactly. Its excess loss is a sum of squares over incoming weight
columns; equality holds precisely when every incoming column is constant, in
which case the entire process is the complete-graph baseline. Combining this
with the known transience theorem for strongly connected noncomplete supports
and a source-component bound for non-strong supports proves that no finite
directed weighting amplifies dB fixation for every (r>1). For undirected
graphs we also give the exact incomplete-support strong limit. Finally, we
classify positive weighted triangles and two maximally symmetric nontrivial
families on four vertices at every beneficial fitness: every nonuniform member
is a strict dB suppressor. These fixed-graph results do not settle the reversed
asymptotic order in which the population threshold may depend on fitness.

## Provenance and human checks

- This text matches the abstract currently in `paper/main.tex`, with only
  typographic conversion from LaTeX to Markdown.
- The all-(r) obstruction, equality class, low-dimensional classifications,
  and quantifier limitation are all marked **PROVED** or **OPEN**, as
  appropriate, in `CLAIMS_LEDGER.md`.
- **Human action:** confirm the current portal word limit and approve any final
  house-style edits before submission.
