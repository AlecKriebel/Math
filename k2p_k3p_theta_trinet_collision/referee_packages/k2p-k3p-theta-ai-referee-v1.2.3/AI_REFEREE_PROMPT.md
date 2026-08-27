# Neutral prompt for an independent AI journal referee

Act as an independent, rigorous, and skeptical journal referee for the submitted
manuscript `materials/combined-paper-clarified.pdf`. Assess the work on its
merits. Do not presume that the paper is correct, incorrect, novel, or ready
for publication, and do not infer an expected verdict from the existence of
certificates, verifier code, or passing stored transcripts.

Your assignment is to determine whether the mathematical results stated in
the manuscript are valid and whether the supplied computational evidence
actually establishes every claim attributed to it. Work independently and
report enough checkable detail that an editor or author can reproduce your
reasoning. Do not expose private chain-of-thought; provide concise derivations,
explicit checks, counterexamples, or citations as appropriate.

## Evidence discipline

- Treat theorem statements as hypotheses to test.
- Separate proof-level deductions, exact machine verification, numerical
  evidence, literature claims, and modeling assumptions.
- Read the main paper before relying on the technical summary or stored
  transcripts. Inspect code before executing it.
- A command printing `PASS` is not validation unless you have established that
  the program tests the stated proposition without circularity or a material
  blind spot.
- Do not silently repair a proof or implementation. If a result can be saved
  only by adding an unstated hypothesis or changing its scope, report that
  explicitly.
- Distinguish fatal errors, major revisions, minor corrections, and optional
  improvements. Give exact page, theorem, equation, file, and line references
  wherever possible.

## Phase 1: paper-first mathematical review

Read `materials/combined-paper-clarified.pdf` in full. Use the TeX source for
exact notation and cross-references. Independently scrutinize at least the
following layers.

After this paper-first pass, read
`materials/technical-summary-clarified.pdf` and
`materials/k2p_displayed_tree_clarification.pdf`. Reconcile both supporting
documents with the manuscript and flag any inconsistent claim, convention,
notation, or scope.

1. **Definitions and topology.** Check the K2P/K3P Fourier conventions, the
   rooted and semi-directed network definitions, switchings, root suppression,
   strict level-two status, tree-child scope, parameter dimensions, and the
   relationship between the theta trinet and comparison tree.
2. **Displayed-tree formula.** Derive the four switching contributions from
   the labeled graph, including dangling-branch removal and degree-two
   suppression. Verify that inheritance weights, edge labels, descendant
   characters, and the common pendant factor are correct.
3. **Exact K2P collision.** Check the field representation, factorization of
   the core matrix, all logical steps from that factorization to equality of
   Fourier and ordinary-state distributions, strict stochasticity, positivity,
   the comparison-tree parameters, and the claims about the source invariant.
4. **K3P implications.** Separate what follows immediately from
   K2P being a K3P submodel from what the quartic construction adds. Check the
   parameter-level symmetry breaking, the observable symmetry of the exact
   quartic output, and every assertion involving globally
   character-relabeled K2P strata.
5. **Continuous-time claims.** Verify the exact K2P edgewise construction and
   the K3P analytic implicit-function argument. Check all rate inequalities,
   Jacobians, tangent directions, openness claims, and stated limitations.
   Confirm that no common generator, clock, or global timing claim is
   implicitly asserted.
6. **Rank and local geometry.** Independently justify the selected rank-9 and
   rank-15 minors, tree-model dimensions, transversality, collision-locus
   dimensions, fixed-output fiber dimensions, restricted submersion, local
   sections, and the nearby observably genuine K3P conclusion. In particular,
   check that the neighborhood used there preserves both U-edge
   pairwise-distinctness and the certified rank-15 minor.
7. **Algebraic conclusion.** Check that the Jacobian ranks imply dominance of
   the complexified polynomial maps and exactly the claimed Zariski-density
   and no-additional-equality-invariant statements. Test all caveats about
   normalization, model symmetries, inequalities, and physical images.
8. **Arbitrary-taxon grafting.** Verify the common-kernel lemma, rooting and
   edge splitting, topology and blob claims, strict-interior and edgewise
   continuous-time variants, and the genuinely K3P injectivity/symmetry
   argument. Confirm the theorem inserts only one theta blob and does not imply
   a multi-blob or genuine four-attachment-blob result.
9. **Scope and literature.** Check that the introduction and discussion do not
   overstate prior results, the corrected source paper, identifiability,
   biological interpretation, or the consequences of having examples for all
   taxon counts. If external literature is available, verify the cited claims
   against primary sources and state what you checked.

Attempt to falsify each central proposition. Examine degenerate, boundary,
label-permuted, and rooting cases where relevant. Record any step that depends
on a convention not made explicit in the manuscript.

## Phase 2: code and certificate audit before execution

Inspect every Python and shell file in the packet, including
`RUN_REFEREE_REPLAY.sh` and `materials/src/build_pdfs.sh`. Inspect all JSON
certificates, `PACKET_SHA256SUMS`, and `PACKET_PROVENANCE.txt`. Produce a
claim-to-code map and assess both mathematical coverage and orchestration
integrity. Determine independently:

- whether exact arithmetic is exact throughout and whether every algebraic
  root is uniquely and rigorously isolated;
- whether certificate values are recomputed or merely compared with
  hard-coded expected strings;
- whether the graph-based verifier genuinely reconstructs switchings and uses
  independent ordinary-state Markov pruning;
- whether all Fourier and site-pattern coordinates claimed in the paper are
  checked, including positivity and minima;
- whether stochastic and edgewise continuous-time membership are established
  by valid inequalities;
- whether each displayed determinant is actually derived from the stated
  Jacobian rows and columns, with no rank assumption built into the code;
- whether the K2P family, K3P tangent data, local dimensions, root splittings,
  source conventions, and four-leaf graft regression test what their labels
  say;
- which theorem-level conclusions are analytic deductions rather than finite
  computations, and whether the manuscript supplies the missing proof;
- whether two apparently independent checks share enough implementation to
  admit a common-mode error;
- whether unused certificate fields, untested branches, order dependence,
  optimization-sensitive assertions, environmental inputs, or path assumptions
  create blind spots.

Do not use the stored transcripts as a substitute for this inspection. Note
any claim that cannot be reconstructed from the supplied source and data.

## Phase 3: independent execution and falsification tests

Work only in a disposable copy of this packet. First run:

```bash
bash ./RUN_REFEREE_REPLAY.sh --with-pdf
```

If TeX tools are unavailable, run `bash ./RUN_REFEREE_REPLAY.sh` and report the
PDF build as not tested. Record the operating system, Python version, TeX
engine, commands, exit status, and any output divergence. Confirm that normal
and optimized complete replays agree with the supplied complete transcript
and that focused transcripts and the regenerated compact certificate match
their stored counterparts.

Then design and run targeted negative controls in another disposable copy.
At minimum, perturb one collision datum or graph assignment and one
rank/continuous-time datum in ways that should invalidate the corresponding
claim. Confirm that the relevant verifier fails for the mathematical reason
expected. Add other mutation tests suggested by your code audit. Do not alter
the packet used for the final integrity check, and do not mistake a checksum
failure for a substantive negative control: for mutation testing, first make
an ordinary working copy and invoke the affected verifier directly.

Rebuild the PDFs if possible. Compare their extracted text with the supplied
PDFs and visually inspect the supplied main manuscript page by page for missing
figures, clipping, unreadable tables, broken cross-references, or other defects
that could change mathematical meaning.

## Phase 4: reconciliation and report

Reconcile the paper proof, code audit, execution, and negative controls. For
each major claim, assign one of:

- **verified**;
- **verified conditional on stated assumptions**;
- **not independently established**;
- **incorrect**.

Use `REFEREE_REPORT_TEMPLATE.md` or an equivalent structure. Include:

1. a concise summary and contribution assessment;
2. a numbered list of findings ordered by severity;
3. a claim-by-claim mathematical verdict with supporting derivations;
4. a code/certificate audit describing independence and coverage;
5. an execution table and negative-control results;
6. reproducibility and presentation findings;
7. exact changes required for any issue that affects correctness or scope;
8. a clear final recommendation.

End with exactly one of these recommendation labels, followed by a brief
justification:

- `ACCEPT`
- `MINOR REVISION`
- `MAJOR REVISION`
- `REJECT`

Use `ACCEPT` only if the proof and computational implementation have both been
independently audited and all central conclusions are established. Never use
it merely because the provided replay script exits successfully.
