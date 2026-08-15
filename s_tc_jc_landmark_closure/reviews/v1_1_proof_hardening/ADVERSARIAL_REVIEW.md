# Independent adversarial mathematical review

Reviewed checkpoint: `a121b4a8`

## Verdict before the repair pass

**No unresolved blocker and no counterexample were found.**  Outcome A was
judged mathematically supportable after one bounded repair pass.  The reviewer
identified two repairable mathematical handoff gaps and two exposition gaps;
all other mandated criticisms were rejected.

The reviewer was read-only and did not edit the manuscript or verifier.

## Findings preserved from the review

### F1 — compression-to-certificate handoff

Classification: **repaired mathematical gap**.

The noncut-compression lemma proves the correct direction and retains a full
repair, every sink child, and two actual taxa of each colour.  What was not
said in the manuscript was why its restriction of as many as eight ports was
covered by the four-active-port strict-minor certificate.

The exact bounded repair is:

1. use the compressed two-colour completion;
2. invoke the exact zero-survivor switching record to choose a switching that
   does not display the split;
3. apply the ordinary tree quartet criterion inside that switching to select
   two actual taxa of each colour whose quartet is still wrong;
4. retain all other repair and sink roles as zero-character completion ports;
5. use the certified universe of 72 four-active tensors and 204 strict wrong-
   split minors; the chosen minor is a submatrix of the original flattening.

The supporting certificate is
`independent/bridge_cut/cut_certificate.json`; the mathematical bridge was
already recorded in `independent/bridge_cut/PROOF.md` but needed insertion in
the article.

### F2 — zero-sum descriptor normalization

Classification: **repaired mathematical gap**.

The constant-rank proof is valid, including simultaneous nonvanishing of a
selected-rank minor and a generic full-model rank minor.  The false local
sentence was that distinct unnormalized rooted descendant-mask rows always
give distinct selected coordinates.  On zero-sum assignments, a selected
mask and its complement induce the same JC exponent; the clean-room fixture
realizes, for example, masks `3` and `12`.

The repair is to group physical edges by equality of their complete zero-sum
JC indicator signature, including split complements.  Every resulting class
maps to its effective selected coordinate by a positive product
`(x_1,...,x_s) -> product x_i`, which is onto and submersive on the open cube.
The constant-rank conclusion then follows exactly as written.

### F3 — omitted Theta reproducibility data

Classification: **repaired exposition gap**.

The article and supplement gave the common orbit vector and complete target
point but omitted the source physical parameter point and the definitions of
the source and target gauge variables in the two Jacobian determinants.  The
scoped frozen Theta derivation contains both.  They must be printed in the
unified supplement.

### F4 — decorated bridge-tree cross-reference

Classification: **repaired exposition gap**.

The global proof attributed equality of the decorated bridge trees directly
to the pointwise cut theorem.  Cut equality is established there, while the
ordinary/nontrivial component decoration is established in the immediately
following bridge-tree corollary using the trinet polynomial and the minimum
theta boundary count.  The global proof must cite that corollary.

## Mandatory review questions

| Question | Adversarial conclusion |
|---|---|
| Noncut compression direction | Correct; F1 concerned only its four-active certificate handoff. |
| Marginal open image | Correct after F2's zero-sum descriptor normalization. |
| Four directed theta cores | Structurally exhaustive; criticism rejected. |
| Endpoint normalization | Consistent with the displayed identities; criticism rejected. |
| Provenance of `f_1,...,f_4` | The stated blocks, rows, and columns regenerate the four determinants; criticism rejected. |
| Local product chart | Extraction and contraction are local analytic inverses on the stated physical locus; criticism rejected. |
| Simultaneous physical gluing | One common small effective scale keeps both physical bridge multipliers in `(0,1)`; criticism rejected. |
| Theta self-containment | Needed F3; no mathematical Theta defect found. |
| Omega class and nondegeneracy | Correctly in `W_TC \ S_TC`, strict, triangle-free, and rank nine; criticism rejected. |
| Literature comparison | No material overclaim found. |
| One-sided theorem | Correctly source-relative and not called a preorder a priori; criticism rejected. |
| Outcome Q leakage | None found; criticism rejected. |

## Additional load-bearing checks

The reviewer also rejected criticisms of the no-omnian equivalence, root
reduction, exact incidence-scaling bridge kernel and freeness, the finite
decorated-relation theorem boundary, coherent probes, the proper algebraic
exceptional set, and localization without a continuous target-parameter
selection.

## Release condition

The review authorized Outcome A only after one repair pass implementing
F1--F4 and replaying the relevant exact and mutation checks.  It did not
authorize any theorem or scope expansion.
