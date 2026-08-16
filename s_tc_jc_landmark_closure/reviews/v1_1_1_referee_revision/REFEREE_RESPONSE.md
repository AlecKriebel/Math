# Response to the targeted adversarial referee report

Status: **REVISED AND ADVERSARIALLY REVIEWED — release requires exact clean replay**

This response records the disposition of every recommendation in the
2026-08-16 report.  The revision preserves the theorem's scope; no central
claim was weakened or broadened.

| Referee item | Disposition | Revision |
|---|---|---|
| Componentwise all-zero bridge normalization | **ACCEPTED — mandatory** | Section 5 now normalizes every component tensor by `P_v(0,...,0)=1`, defines the incidence-saturated locus from normalized tensors, and uses normalized subtree contractions to fix the zero sector. Supplement P3 states the same condition. |
| Finite target-completion union | **ACCEPTED — mandatory** | Section 6.1 now names the finite semialgebraic images `Y_tau`, applies the finite-cover lemma, and fixes one full-dimensional decorated relation before invoking the bounded theorem. |
| Physical analytic sections | **ACCEPTED** | Lemma 5.3 now invokes the constant-rank theorem on the chosen smooth physical image branch and distinguishes the ambient tensor locus, physical locus, projective image, and analytic slice. |
| Image-tangent rank in Lemma 6.2 | **ACCEPTED** | The descriptor is renamed `delta_R`; the proof explicitly identifies the source-image tangent space with `Im D phi_full` and restricts `DR` to it. |
| Fourier marginalization reminder | **ALREADY PRESENT** | The cut proof already states at its first load-bearing use that omitted characters are set to zero and the marginal is a literal row/column submatrix. No duplicate sentence was added. |
| Definition of complete factor | **ACCEPTED** | The term is defined before the local model uses it. |
| Repair-table indexing | **ACCEPTED** | The text now states that indices start at zero and follow each displayed segment list. |
| Exclusivity wording in Theorem 6.3 | **ACCEPTED** | The theorem now says the certificate assigns each relation to one category; it no longer asserts abstract logical exclusivity of the category properties. |
| Triangle-context sentence and quantifier | **ACCEPTED** | Lemma 6.5 now uses a physical context-parameter chart, a displayed contraction map, and “each selected orientation.” |
| Bridge-scale gluing precision | **ACCEPTED** | Lemma 6.6 now separates edgewise scale choice from the tree's no-holonomy role. |
| Genericity notation and dimension handoff | **ACCEPTED** | The proof defines `Z_N(N')` explicitly and states the real semialgebraic dimension/relative-interior implication before forming `E_top(N)`. |
| Omega determinant rows | **ACCEPTED** | The main text and supplement identify rows `(A,B,C,D,E,F)` and columns `(a_0,...,a_4,a_7)`. |
| Theta local coordinates | **ACCEPTED** | The overlap proof now states why `(A,...,H)` are coordinates on the positive smooth branch and why rank eight yields a shared relative neighborhood. |
| Add “generic” to title | **ACCEPTED** | The manuscript, supplement, metadata, and active consistency checks now use “Sharp Generic-Identifiability Boundary.” |
| Copy the full P1–P8 map into the article | **NOT ADOPTED — optional** | The article already gives a compact four-layer proof overview, while the supplement carries the detailed P1–P8 map. Duplicating it would add length without closing a proof gap. |
| Enlarge or split Figure 2 | **PARTLY ACCEPTED** | Splitting is unnecessary. All four theta labels were moved downward and the rebuilt page was inspected at full size; the overlap is removed. |
| “Independent replay” terminology | **ACCEPTED** | Reader-facing language now prefers “separately implemented replay,” preserving the explicit statement that no independent human review is claimed. |
| Dedicated repository, licenses, persistent deposit | **DEFERRED — human/release choice** | The active package remains self-contained in the versioned project folder. No license or persistent identifier was selected or invented; those choices remain on the human checklist. |

The regression script `verify_referee_regressions.py` fails if the bridge
normalization, finite-cover selection, descriptor distinction, category
wording, or Figure 2 spacing is reverted.  It strips TeX comments, measures
graph-to-label clearance, synchronizes embedded PDF and submission titles,
and rejects eight targeted mutations.  It also records the explicit
constant-scalar counterexample excluded by component normalization.

A second mathematical review identified and corrected one overstatement in
the generalized finite-cover lemma: the full-dimensional object is
$U\cap Y_\tau$, not necessarily the ambient target image $Y_\tau$ itself.
It also prompted an explicit smooth-image preimage condition in the marginal
rank proof.  A separate release review found no new mathematical issue and
correctly required a fresh v1.1.1 rebuild, visual audit, metadata seal, tag,
and clean replay after these last source edits.
