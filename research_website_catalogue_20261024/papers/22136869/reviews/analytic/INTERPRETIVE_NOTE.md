**RECLASSIFIED 2026-10-25T01:26:17.270649+00:00: no substantive defect is established by this counterexample under the strongest plausible contextual reading.** Equation(17) fixes B with equal nontrivial coordinates. Under that restriction, M_CC=4d²/5 and M_TT=5e²/9 imply e/d=6/5. The counterexample below refutes only general factorization under the displayed U,V,S,T ansatz. Full analytic review has resumed; the earlier stopping disposition below is retained as historical reasoning, not the current verdict.

# Interim interpretation note: Zenodo 22136869

**Disposition: DEFER — an exact, noncentral mathematical overclaim is confirmed.** On published page 12, the derivation paragraph after Theorem 12 says that its positive ansatz and τ=1/3 force e/d=6/5. They do not: an exact strict-interior example with e/d=1 satisfies the same core tree-factorization condition. The ratio is free under that condition unless a further constraint is imposed.

This finding **does not refute the paper's selected e/d=6/5 witness, Theorem 12, or the main collision, rank, implicit-function, and grafting theorems**. It refutes the unqualified necessity claim in the explanatory derivation. If the author intended a more restrictive normalized factorization, that restriction is not stated in the displayed ansatz/necessity sentence. No repair or replacement publication construction was attempted. Per the defect protocol, the remaining global certificate review was stopped rather than declared passed.

## Exact publication binding

The reviewed work is *Exact Tree–Theta-Trinet Collisions under the Kimura 2- and 3-Parameter Models*, https://doi.org/10.5281/zenodo.22136869, spreadsheet row43.

The Zenodo metadata `version` field is **1.2.6**. The published filename and package presentation identify **v1.2.7**. Both labels are preserved; the review is bound to the bytes below rather than silently resolving that discrepancy.

| Asset | SHA256 |
|---|---|
| Main published PDF, 20pp, 178,692 bytes | `7f1ecd0e70504736146eb8f2d4ebfb43980fd1feef50cf39bbe7e751ad5afa8f` |
| Published ZIP, 443,027 bytes | `7c603e15f6afb7546f618b88bbefdc52ee264b656399f6656fc742aeabb786c7` |
| `combined-paper-clarified.tex` | `e4876619a27cdd7e91e051c89b0827da418d6d201a40400c2bc3c31e2f1f9a9a` |
| Displayed-tree clarification PDF, 2pp | `14855c3cddf1aea47f2d8e014ab9ea2618a8f3fa76cf08a4ebb468dcf68f1c57` |
| Technical-summary PDF, 2pp | `4864396b878ecdd6cbfb0b92df960fb9344e015866eaaa61ee2979cfc66e4637` |

Fresh acquisition was performed by the scope agent; sources were read-only throughout. The queue-bound original PDF was independently size/MD5/SHA checked before reading, then rebound to the fresh Zenodo receipt. The ZIP's internal main PDF is byte-identical to the separately published main PDF. `source_pins.json` pins all acquired assets; it is explicitly an inventory of hashes, not a claim that every asset was read.

The defect was authenticated in the actual rendered published page12, not only extracted text. It occurs immediately after Theorem12 and before Section8. The matching TeX is lines414–422, particularly lines418–420. The mathematical necessity asserted there is

`τ=1/3 and positive core factorization ⇒ κ=3/√5, b²=1/√5, e/d=6/5`.

Only the last asserted necessity is challenged here.

## Exact counterexample

Let h be the positive root of 5h⁴−1, so 2/3<h<7/10. In the paper's stated ansatz take

`τ=1/3, b=h, κ=3h², d=e=1/4`.

Then e/d=1≠6/5, while κ=3/√5 and b²=1/√5 still hold. The edge vectors are

```
U = (1, h/3, h, 1/3)
V = (1, h, h/3, 1/3)
S = (1, 3h²/4, 1/4, 1/4)
T = (1, 1/4, 3h²/4, 1/4).
```

Define

```
P = (1, (5h³+h)/4, (5h³+h)/4, h²)
B = (1, h²/2, h²/2, 5h²/12).
```

Substitution into the paper's four-switching formula (7) gives, exactly in Q(h),

`M[y,z] = P[y+z] B[y] B[z]`

for every one of the sixteen pairs y,z in Z₂². Thus this is the asserted core tree factorization under the displayed positive ansatz, with a different ratio. The P vector is unchanged from the paper's equation(17); B's T-coordinate changes. A requirement that B retain three equal nontrivial coordinates would be an extra restriction, not a consequence of general core factorization.

For explicit admissible tree and network parameters, use the paper's common K=(1,1/2,1/2,1/2), inheritance probabilities 1/2, and the stated ten-arc rooted topology. The effective first pendant is K⊙K. The comparison tree edges are α=K⊙K⊙P and β=γ=K⊙B. Every nontrivial eigenvalue of these network/effective/tree edges lies strictly between zero and one, and all four transition-row entries are strictly positive. These signs were certified by rational interval bounds using 2/3<h<7/10, not floating-point signs.

The independent code also literally deletes the unselected parent arc at each reticulation, obtains Fourier labels from the retained graph's descendant leaves, and compares all64 Fourier coordinates to the comparison tree. It then inverts the transform in all64 ordinary patterns and checks positivity and total mass one. These checks confirm that this is not an extraneous algebraic root outside the paper's strict stochastic parameter domain.

## Why the ratio cannot be forced by the stated condition

There is a simple structural reason. The T-character coordinates of both S and T are the same variable e. Rescaling that variable by a positive factor c multiplies each core coordinate M[y,z] by c once for each of y,z equal to the T character. It is absorbed by the same rescaling of B_T in any factorization P[y+z]B[y]B[z]. For sufficiently small changes, all strict stochastic inequalities persist. General factorization alone therefore cannot fix e/d.

An independent symbolic calculation gives the same diagnosis. Write r=e/d, set τ=1/3, and use the C/G symmetry of this ansatz. Two factorization conditions are

```
M_CT² − M_AC² M_TT
  = b² d⁴ r² (5κ²−9)/81,

M_CG² M_TT − M_AT² M_CC²
  = d⁶ r² [5b⁴κ⁴ +54b⁴κ² +405b⁴
           −48b²κ³ +432b²κ −81κ⁴ +18κ² −81]/11664.
```

Since d,r>0, the r² factors impose no condition on r. The concrete counterexample above verifies every coordinate directly, so the conclusion does not depend on accepting these two conditions as a complete characterization.

## Independent evidence and reproducibility

`counterexample_ratio.py` imports no submitted code, certificates, or historical findings. It was written from the actual manuscript equations before any supplied verifier implementation was read. It uses exact SymPy algebraic-field arithmetic and rational interval arithmetic. The completed run passes **225 exact assertions**, including:

- the symbolic cancellation of the proposed ratio constraint;
- the non-6/5 ratio and all16 core factorization identities;
- strict edge/effective-edge/tree eigenvalue and transition-probability bounds;
- all64 graph-derived Fourier equalities;
- all64 positive ordinary pattern probabilities and exact normalization.

Run with the existing project environment:

```
/Users/alec/Documents/Math/.venv/bin/python -E -B \
  /Users/alec/Documents/Math/research_website_catalogue_20261024/papers/22136869/reviews/analytic/counterexample_ratio.py
```

The script writes `counterexample_ratio_results.json`, including all assertion labels, symbolic equations, rational transition bounds, runtime versions, UTC timestamp and its own source hash. It is a falsification artifact for the narrow necessity assertion. It is not a proposed repair of the paper or a full replay of the published theorem certificates.

## Reading coverage, proof map, and exact stopping point

Read all20 main PDF pages and both2-page reader supplements. Reconstructed the intended chain: group-based mixture and root suppression; compact K2P core factorization; cubic continuous-time witness; full rank and local-fiber geometry; quartic K3P factorization and parameter/observable symmetry distinction; analytic inward direction into the edgewise continuous-time chamber; removal of the three K2P fixed loci; Zariski dominance; and the injective/equivariant common-subtree argument. Selected matching main-source passages, especially the defect and adjacent claims, were inspected. Reading a proof chain is not being presented as complete verification of its large algebraic certificates.

The general inference mechanisms appeared coherent on this reading: a surjective differential gives a local submersion; tree recovery is smooth in the positive chamber; tangent positivity plus the analytic implicit-function theorem would move the two saturated margins inward if its stated exact matrix data are correct; and attaching identical conditionally independent kernels preserves a three-interface distribution. The distinction between a K3P network parameter and an observably genuine K3P distribution is made correctly in the statements. None of these observations certify the un-replayed determinant or tangent data.

The exact rank-9/rank-15 determinants, cubic continuous-time certificate, displayed-child sign audit, complete source-convention check, analytic tangent certificate, mutation suite, and four-leaf replay were **not completed after the stopping defect**. Supplied verifier implementations and JSON certificate bodies were not read or executed. Dedicated historical review/disposition documents, archived verification reports, and sibling reports were not opened. Consequently this report must not be used as a pass for the remaining theorem chain.

Fresh primary PDFs for Brits et al. v2/v3 and Ardiyansyah were acquired and hashed in `primary_sources.json`. The Brits v2 binary-network definition and restricted stochastic/eigenvalue/inheritance parameter definition were checked against the concrete counterexample. The exact broader versioned theorem/novelty comparison and all other literature interfaces were not completed after the stopping defect. Downloading a source is not counted as having read all of it. The defect is established directly from the paper's own displayed ansatz and exact arithmetic and does not depend on a literature priority judgment.

## Independence and limits

No current sibling findings or dedicated historical verdicts were read before this conclusion. The main paper's p19 acknowledgments incidentally say that external mathematicians examined or confirmed an earlier clarified counterexample; this opinion text was encountered during the required full manuscript read and was not used as evidence. The two reader supplements also assert that their verification suites pass; those assertions were not substituted for current execution. Filenames of archival/disposition documents were seen during a source inventory, but their contents were not opened.

The review is complete as a **bounded defect disposition**, not as full validation of all published claims. The strongest verified conclusion is the exact failure of the unqualified e/d necessity statement, with an admissible counterexample. The exact remaining gap is the unreplayed remainder of the paper's main certificate chain; its truth or falsity is undecided by this stopped review. No source repair, alternative rooting search, publication mutation, external outreach, Git, website, or spreadsheet action was performed.
