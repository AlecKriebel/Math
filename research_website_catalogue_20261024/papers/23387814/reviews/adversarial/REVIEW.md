# Independent adversarial review — Zenodo 23387814

Completed 2026-10-25T02:06:59.447408+00:00; assigned task 100%.

**Verdict: SUPPORTED AT THE STATED SCOPE.** No substantive defect was found. The construction does give smooth minimal complex projective surfaces, integral ample polarizations and special points contradicting the exact arbitrary-point lower bound, for every integer d>=7. The proof uses standard algebraic-geometric existence and ampleness theorems, not only numerical controls. This is an independent AI review, not human peer review or formal proof-assistant certification, and it does not establish historical firstness.

## Bound edition and coverage

The actual [Zenodo23387814](https://zenodo.org/records/23387814) PDF is `seshadri_counterexample.pdf`, all **five pages** read, printed **October14,2026**, Zenodo version1.0. SHA-256: `8f50f329fac5b30ffea3d98f82e36ec71af0d3d5df44e38a21f992eb45aa4c48`. The actual `verification_package.zip` SHA-256 is `6af7c815f863d44ba4b24708d5ae70bec4d5e0fd55789114083a605c08a27a20`. Both public assets were independently checked against size/MD5/SHA receipts at intake and completion. All **102** safely extracted files were rehashed at both checkpoints and remain unchanged. There is no additional embedded reader PDF.

Coverage includes the exact question, theorem, explicit singular member and entire-pencil existence argument, blowup and ampleness, smooth connected integral cover, canonical formula/minimality, split-fibre multiplicity/intersections, exact inequality and all stated limitations, followed by disclosure and references. `DERIVATION.md` reconstructs every mathematical stage and boundary. The published mathematical helpers were read only after a recorded independent reconstruction/control checkpoint.

## Exact primary target

The target is epsilon(S,L;x)>=1/(2+|K_S^2|^(1/4)), with **2 outside the fourth root**, a minimal smooth complex projective surface, an ample integral line bundle, and an **arbitrary point**, without a Picard-rank restriction. This was checked directly in [Szemberg's 2007 final question](https://arxiv.org/abs/0711.0584v1), [OWR2009 Conjecture2, printed p.1124](https://doi.org/10.4171/OWR/2009/21), and [Primer Question6.1.6, v2 p.17](https://arxiv.org/abs/0810.0728v2). The OWR equation and surrounding hypotheses were visually inspected, not inferred from imperfect OCR or a catalogue transcription.

The proposed example satisfies this target. It does not refute the neighboring very-general-point result, a Picard-rank-one result, or a canonical-polarization bound. The special point is permitted. The surfaces vary with d, so no assertion about the infimum over all polarizations and points of one fixed surface follows.

## Geometric attacks and outcomes

| Potential failure | Independent resolution |
|---|---|
| Reducible singular member or unseen projective singularity | The equation is primitive linear in Z, so Gauss's lemma proves integrality. The first partials exclude all singular points except [0:0:1], and the tangent polynomial has d−1 distinct factors. The multiplicity is exactly d−1. |
| Only a generic pencil member is integral | The full reducible/nonreduced locus has codimension at least d−1. Its join with the chosen integral member is proper for d>=3. A companion outside the join makes **every** pencil member integral and reduced. |
| Simultaneous genericity conditions incompatible | Smoothness, avoiding the marked singular point, and transversality are nonempty opens for the complete degree-d system. Their intersection with the nonempty join complement exists in the irreducible parameter space. The proof works at d=7 and does not borrow an unproved finite threshold from an asymptotic source. |
| Basepoint multiplicities or hidden exceptional fibre components | At a transverse basepoint, the two defining forms are local coordinates. Each pencil member is simple there, one blowup resolves the map, and every exceptional curve is a section. Bezout gives d^2 distinct basepoints away from the singular point. |
| A=2F+E_1 not ample | The full curve argument distinguishes the section, all horizontal curves, and vertical curves. The last class consists of whole integral reduced fibres, of degree one against A. Together with A^2=3, Nakai–Moishezon applies. |
| Cover singular over a bad fibre | The four branch fibres are smooth and avoid the marked one. Away from them, the cover is etale even where the original fibration has singular fibres. At branch fibres it is locally t=v^2 in smooth coordinates. Thus the entire covering surface is smooth. |
| Disconnected or reducible fibre product | Proper connected fibres over connected B prove connectedness; smoothness then gives integrality. Odd branch valuations also exclude a split quadratic extension over C(Y). Projectivity and finite flat degree two are preserved by the base change. |
| Incorrect canonical correction or overlooked (−1)-curve | The half-branch bundle is 2F, giving K_S=pi^*(K_Y+2F). N=(d−3)H+F has positive degree on every exceptional curve and every other integral curve, with N^2>0 for d>=4. Hence K_S is ample and adjunction excludes rational (−1)-curves. |
| Degree-two rather than degree-one curve upstairs | Because this is a base change and the special base value is unbranched, its inverse image is C x {b_1,b_2}, two disjoint copies of C. One chosen component has L.C'=1 and unchanged multiplicity d−1. A generic etale curve cover need not split, but that invalid inference is not used. |
| Wrong radical/domain or threshold | For d>=4, fourth powers preserve the positive comparison and reduce it to (d−3)^3>6(d−1). The margin starts positive at d=7 and increases. d=4,5,6 fail for this witness as explicitly stated. |

At d=7 the verified identities are K_S^2=144, L^2=6 and L.C'/mult_x(C')=1/6. Since 144<4^4, 1/6 is strictly less than 1/(2+144^(1/4)). Only an upper bound on epsilon is required; an exact value is not claimed.

The preimage of an old exceptional section is a genus-one curve of self-intersection −2 and canonical degree2, not a rational exceptional curve. The marked fibre can have rational normalization while positive arithmetic genus, so it does not contradict the adjunction argument for minimality. These checks address plausible but incorrect objections to the construction.

## Fresh independent evidence

`fresh_controls.py` was written and executed before reading any supplied helper. It imports no supplied code and uses exact integer/Fraction arithmetic. It passed **5,387** assertions, including:

- Degree cases d=3 through40: sparse polynomial Euler identities, exact multiplicity, squarefree tangent gcds, reducible-locus dimension formulas and proper-join bounds.
- Full blowup-lattice calculations of F, A, K_Y, N and cover degrees, including individual exceptional intersections and the single-fibre quotient. A topological Euler/Noether consistency check is recorded separately as a consistency check, not an existence proof.
- **1,999** exact integer inequality parameters, including d=10^20 and10^100, checking the forward-difference formula and strict threshold without floating-point radicals.
- Negative construction controls: F+E has zero degree on E; using only two branch fibres gives zero canonical degree on the lifted section; omitting the cover retains K_Y.E=−1; d=6 fails the strict comparison; branching at the singular fibre has vanishing gradient, while the smooth-fibre local cover has a nonzero derivative.

Finite checks do not certify the existence of a generic companion g, Bertini/transversality, Nakai–Moishezon, connectedness, or priority. Those logical steps are reconstructed in `DERIVATION.md`. The construction is explicit in its singular curve and numerical family, while its companion is chosen from a proved nonempty open set; no single fully enumerated companion polynomial was computed or needed for the existential theorem.

## Fresh replay of supplied mathematical support

After the independence checkpoint, four standalone mathematical helpers were read completely and copied byte-for-byte into an ignored isolated replay directory. Their hashes and original paths are in `published_helper_bindings.json`. They were run with the existing project Python runtime, confirmed **SymPy1.14.0/mpmath1.3.0**, in normal mode with assertions enabled. All exited zero:

- `reviews/geometry01/geometry_controls.py`: **1,183** exact controls, including rank-two cover algebra, split special fibre, local smoothness/branch failure and cover intersection lattice.
- `reviews/pencil01/fresh_controls.py`: **28,945** exact controls, including primitive-polynomial and singular-chart computations, parametrization, dimensions, jet/transverse-basepoint models and threshold controls.
- Original author `verify_formulas.py`: **97** degree cases d=4 through100.
- Original author `verify_intersections.py`: **27** degree cases d=4 through30.

The new outputs are saved in the four `published_*_replay.json` files. They are results of this execution, not adopted archived totals. Full package wrappers, historical audit prose, historical audit checkers and stored replay outputs were not run/read, and no full-package semantic audit is claimed. The helpers themselves explicitly limit their finite computations; they cannot establish the geometric existence proof or historical priority.

## Primary interfaces and attribution boundaries

`primary_sources.json` binds the actual primary PDFs, hashes, URLs and precise reading scopes. Raw files and acquisition receipts only were shared from the scope agent; no review conclusions were exchanged.

- The exact target was checked in Szemberg, OWR and the Primer as above.
- [Ein–Lazarsfeld, Example3.1](https://www.numdam.org/item/AST_1993__218__177_0.pdf) directly records Miranda's integral pencil and section polarization. Its introduction also distinguishes special small-constant points from the general-point lower bound.
- [Bauer, Proposition3.3](https://arxiv.org/abs/math/9903072v1) gives the related blowup construction and an asymptotic d=m+1 use. The candidate independently supplies the finite-degree integral pencil, so it does not silently convert that asymptotic assertion into d=7 existence.
- [Bauer–Szemberg, Proposition2.1](https://arxiv.org/abs/1011.0979v1) explicitly uses the integral polarization E+2C on a nonminimal pencil blowup. This ingredient is prior work.
- [Fuentes Garcia, Section2](https://arxiv.org/abs/math/0511547v2) gives the reduced ramification and canonical line-bundle formulas for a cyclic cover of a smooth surface branched over a smooth reduced divisor. Four disjoint smooth fibres meet these hypotheses. No unrelated rank-one or very-general-point lower bound from that source is imported.
- [Bauer–Szemberg's canonical-polarization paper](https://arxiv.org/abs/0801.3245v1) was checked only at its introductory lower-bound discussion; no complete example audit or firstness inference is claimed.

Standard characteristic-zero Bertini/transversality, intersection theory, Nakai–Moishezon and finite ample pullback are essential inputs. Their hypotheses were checked in the reconstructed proof. The bounded primary reading is not a full literature search and does not resolve the manuscript's stated priority gaps.

## Independence and action boundary

No current sibling mathematical report, historical dedicated verdict, acceptance document, audit prose or status body was read. Source manifests exposed only file names and hashes. Required manuscript section5 and its AI disclosure contain historical internal-review assertions, and required helper docstrings describe earlier independence; these were incidentally encountered and not adopted as evidence. Original support files were only hashed for inventory except for the selected mathematical helper bodies.

All authored results and logs are confined to `reviews/adversarial`. No website, spreadsheet, Git, Zenodo, publishing, repair or external outreach action was performed. No substantive defect warrants deferral from this independent gate; the parent retains the overall publication decision after all gates.
