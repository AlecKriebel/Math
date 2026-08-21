# Paper II theorem and evidence map

Date: 2026-08-20 (America/Los_Angeles)

## Headline and claim boundary

The paper proves

\[
R_{\rm sim}\ge 1.5028569127905696\ldots>3/2.
\]

The construction is one graph sequence selected independently of fitness.
For every fixed fitness in the open interval, both update rules amplify for
all sufficiently large population indices.  The algebraic endpoint is exact
among fixed positive parameters in the paper's displayed first-order dilute
pair--pendant response model, not for all growing weighted graphs.  The
unrestricted exact threshold and any finite universal upper bound remain open.

## Proof architecture

1. Define both update rules, complete-graph baselines, and the quantifier order
   in `R_sim`.
2. Construct a large clique with dilute hub pendants and dilute internally
   heavy two-vertex satellites, connected by a uniformly selected dyadic cut.
3. Derive the weak-cut limiting trace exactly from the finite-state chain.
4. Prove compact-uniform center establishment, full cleanup, and reciprocal-
   invasion estimates at the gain scale `q/C`.
5. Derive the exact pair-gate macro chain and control the post-gate sweep.
6. Obtain the two leading response functions and optimize their common
   positivity interval.
7. Isolate the sextic root and prove tangency, fixed-parameter response
   optimality, and a specialization with entirely rational edge weights
   crossing `3/2`.
8. Separate exact computational audits from the analytic asymptotic proof and
   state the unrestricted open problem.

## Evidence map

| Claim | Analytic source | Exact replay boundary |
|---|---|---|
| finite orbit lumping | manuscript orbit argument | `verify_hybrid_lumping.py` checks all 512 labelled states and 108 fibres on the audit instance |
| finite weak-cut trace | manuscript block-matrix/Schur proof | no machine proof; finite algebra is stated and proved in text |
| center estimates and reciprocal invasion | manuscript stopped comparisons | no numerical diagnostic is a proof dependency |
| pair and pendant coefficients | trace equations | `verify_hybrid_coefficients.py` |
| sextic, tangency, and fixed-parameter response optimization | quadratic minimization | `verify_leading_algebra.py` and the coefficient audit |
| cross-section integration | manuscript theorem proof | `verify_paper_claims.py` |
| novelty and provenance | manuscript bibliography and release note | `LITERATURE_AUDIT.md` and submission provenance note |

## Freeze gates

- [ ] Final hostile mathematical review reports no theorem, rate, scale, or
      quantifier defect.
- [ ] Exact development replay and submission static audit exit zero.
- [ ] Deterministic archive is byte-identical across two generations.
- [ ] Fresh extraction passes its internal manifest and pinned exact replay.
- [ ] PDF rebuilt from the extraction is byte-identical with the frozen PDF.
- [ ] Every rendered page receives visual review after the last manuscript
      edit.
- [ ] Human author supplies only the private postal-address field, rechecks
      live venue rules, chooses licenses, and performs any submission.
