# Final hostile synthesis for v1.2.5

**Audit date:** 2026-08-27
**Scope completed:** 100% of the requested synthesis
**Artifacts read in full:** `math_audit.md`, `code_audit.md`,
`literature_layout_audit.md`, `root_audit_evidence.md`, and the complete draft
`REFEREE_REPORT.md`

## Bottom line

I could not falsify a theorem, witness, rank claim, continuous-time claim,
topology description, grafting argument, or operative computation. The two
clean-room mathematical reconstructions, literal ordinary-state pruning, and
the successful hostile mutations leave no evidential basis for a major
revision or rejection.

The draft's overall **MINOR REVISION** disposition is defensible, but its
allocation of what is mandatory is slightly too strict. My reconciled
recommendation is:

- **Required before submission:** cite Ardiyansyah (2021) and distinguish its
  restricted level-two variety/distinguishability results from the present
  pointwise three-leaf collision.
- **Advisory, not submission-blocking:** qualify the Version 2-to-3 wording
  with “formal lemma and corresponding corollary.” This is worthwhile
  precision, but the current abstract and acknowledgment are not materially
  false.
- **Advisory package hardening:** reject duplicate JSON object names and, if a
  closed schema is desired, close operative schemas. Neither behavior
  invalidates the supplied certificates or their evidence.

Thus the paper warrants a **narrow, nonmathematical MINOR REVISION**, sustained
by the omitted close citation alone. After that citation is added, I would
recommend acceptance; the history and parser edits may be made at the same
time but should not independently delay submission.

## Attempt to falsify the draft disposition

The strongest avenues in the five audit artifacts were: (i) a possible false
history of the cited Version 3; (ii) an omitted prior level-two result; (iii)
ambiguous raw JSON and open schemas; (iv) the source-side `2`-sub-blob
definition; and (v) possible overreliance on self-consistent certificates.
None produces a mathematical counterexample.

The finite evidence is unusually redundant. Independent scripts that do not
import packet verifiers or read packet certificates reconstruct the compact
K2P and quartic K3P collisions, exact probabilities, literal pruning, selected
rank minors, and the K3P tangent. A second independent reconstruction covers
the algebraic continuous-time K2P witness and associated sign checks. The
canonical replay passes in ordinary and optimized modes. Hostile probes reject
18 K3P semantic/source corruptions, all nine compact-K2P stored transition-row
corruptions, and four packet-boundary mutations. No passing unique-key
mutation was found that makes an advertised operative graph, parameter,
coordinate, probability, determinant, or tangent meaning false.

The remaining raw-JSON passes are real parser behaviors but not such
mathematical false positives: in both duplicate-name examples, Python's parsed
operative value is the later canonical value, while the earlier bogus spelling
is shadowed. This creates an ambiguous raw serialization, not a false parsed
certificate. Newly added open-schema fields are inert and are not used to
establish a manuscript conclusion.

## Adjudication of the three disputed items

### A. Stale Version 3 page-11 sentence — advisory precision

**Adjudication: advisory, not a required correction.**

The primary record is internally inconsistent in a narrow way. Version 3:

- removes the formal arbitrary-level K2P Lemma 5.6;
- makes the corresponding global corollary JC-only;
- explains why the K2P induction fails under leaf reordering; and
- explicitly asks the high-level K2P/K3P question as open.

Against those operative changes, one Section 4.1 roadmap sentence on PDF page
11 still announces a JC-and-K2P arbitrary-level generalization in Section 5.
The latter is plainly stale because Section 5 does not contain the announced
K2P theorem and the abstract and final discussion contradict it.

The collision manuscript's detailed introduction already says exactly that
the **formal** lemma and K2P part of the corollary were removed. Its abstract's
plural “K2P claims withdrawn” has a natural and accurate referent in those two
formal claims. The acknowledgment's statement that Version 3 “correct[ed] the
Version 2 K2P statement” is also a fair description of removing the formal
result, explaining its obstruction, and reopening the question. A surviving
editorial remnant does not make either sentence materially false.

Adding “formal lemma and corresponding global-corollary claim” would eliminate
all room for a hyperliteral objection and is good editorial practice. The
draft referee report may recommend it, but calling it a condition of
submission overstates the defect. A footnote about the stale roadmap sentence
is optional and would be excessive unless the author wants a documentary
version history.

### B. Ardiyansyah (2021) — required minor citation

**Adjudication: required before submission, with no priority conflict.**

Ardiyansyah's *Distinguishing Level-2 Phylogenetic Networks Using
Phylogenetic Invariants* (arXiv:2104.12479) is not merely tangential. It treats
simple and semisimple level-two network models using the same algebraic/Fourier
framework under JC, K2P, and K3P, catalogs small orientable simple strict
level-two topologies, and proves restricted variety noncontainment or
distinguishability results. Its “nice” class contains no simple strict
level-two network on two or three leaves, so it neither proves nor anticipates
the present stochastic-interior tree--theta collision.

That limitation protects the present novelty but does not remove the duty to
cite it. The manuscript contains a compact literature map that moves from
level-one algebraic results to current level-two work; omitting the closest
earlier level-two Kimura/Fourier study makes that map materially incomplete.
A single sentence and bibliography entry suffice. The report should avoid
implying that Ardiyansyah studied the present pointwise tree--theta
intersection; it should state the restricted generic/variety scope and the
three-leaf exclusion.

This is the only issue I would require before submission, and it warrants a
minor rather than advisory classification because citation of directly
relevant prior work is a basic scholarly obligation even when there is no
priority overlap.

### C. Duplicate keys and open schemas — advisory hardening

**Adjudication: advisory, not required for the scientific submission.**

The code audit establishes all relevant facts:

1. All five supplied JSON certificates have unique object names under a strict
   duplicate-detecting parse.
2. The K3P verifier rejects the former duplicate-vertex/list-to-map escape and
   canonically binds vertices, arcs, endpoints, vectors, reticulation
   descriptors, suppression sources, Jacobian descriptors, and tangent data.
3. Ordinary `json.loads` accepts an earlier bogus duplicate name followed by a
   later canonical name. Two such raw K3P serializations pass because the
   operative parsed value is canonical.
4. The two K2P files accept unknown top-level fields, and some K3P nested
   objects accept unknown inert fields. No accepted extra field alters a
   mathematical computation.
5. The full packet replay checks the manifest before execution and rejects any
   changed certificate byte relative to the supplied manifest.

These facts do not support mandatory re-engineering for v1.2.5. Duplicate
object names are invalid or at least non-interoperable under the intended JSON
profile, but none occurs in the evidence being submitted. Open schemas are not
false verification unless the package promises that every unknown field is
operative or rejected; it does not. The K3P inventory explicitly treats
unlisted descriptive fields as informational, and the K2P inventory does not
advertise a closed schema.

The manifest is an internal-consistency boundary, not an authentication
boundary: because it is unsigned and co-distributed with the files, it cannot
defeat malicious repackaging with a rewritten manifest. The packet states
this limitation correctly. This caveat prevents overstating “manifest
protection,” but it still leaves the exact reviewed bytes well identified and
does not convert the parser behavior into a theorem risk.

A strict `object_pairs_hook` is a cheap and sensible future improvement.
Closing operative schemas and reserving an explicit metadata namespace would
also improve assurance. They are not conditions of accepting the mathematics
or the current reproducibility artifact.

## Omitted or overstated points in the draft report

### Overstatement 1: “no verifier false positive” is too absolute

The executive assessment says there was no “verifier false positive,” while
the code audit records two accepted duplicate-name serializations and three
accepted open-schema additions. Later sections explain why they do not affect
the supplied evidence, so this is a wording inconsistency rather than a hidden
finding. The defensible formulation is: **no false positive affecting an
operative parsed value, any supplied unique-key certificate, or a mathematical
claim was found.**

Likewise, “independent hostile tests reject every earlier K3P semantic escape,
additional graph/schema/descriptor contradictions” is sound for the former
v1.2.4 escapes and the unique-key semantic mutations, but should not be read as
claiming that every malformed raw JSON serialization is rejected.

### Overstatement 2: two required history/literature edits

The final report says submission should wait for both the history
qualification and the Ardiyansyah citation. Only the latter is necessary on
the evidence. Downgrading the history qualification to an advisory does not
alter the report's `MINOR REVISION` outcome.

### No omitted substantive defect

The draft appropriately records the source-side `2`-sub-blob ambiguity,
untagged-PDF accessibility limitation, unsigned provenance, existential nature
of the K3P continuous-time branch, and proof-level rather than finite nature of
the all-taxon theorem. The code audit's missing literal assertions for one
printed determinant bracket and the three six-order fractions are also
correctly treated as optional source-coupling improvements because independent
exact calculations verify the printed values.

I found no omitted fatal, major, mathematical-minor, topology, or layout issue.
The bibliography omission is the sole required scholarly repair.

## Final recommendation

**MINOR REVISION**, narrowly confined to adding and accurately contextualizing
Ardiyansyah (2021). The exact results, proof, topology, verifier repairs,
certificates, and publication PDFs are otherwise ready. The Version 3 wording
and strict-JSON/schema changes are advisable refinements, not acceptance
conditions. After the citation is added and the manuscript/packet is rebuilt
consistently, recommend **ACCEPT**.
