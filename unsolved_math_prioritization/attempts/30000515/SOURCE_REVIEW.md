# Source and hypothesis review

Target 30000515 / OWR-1276-008. Historically checked 10 October 2026 UTC during preparation of the authored note. The inspection and current-record statements below describe that review. Edition preparation rechecked identities and verification results without a new scholarly-source retrieval, source-text inspection or literature search. This review contains authored analysis and public references; source files and extraction/rendering products are excluded.

## Original statement

Miles Reid's contribution in Oberwolfach Report 27/2006 occupies printed pp.1645–1647, PDF pages 31–33. The exact hypothesis and conjecture are on printed p.1645. All three pages were read in extracted text and visually inspected. The hypothesis concerns every member of the pencil. The report gives the Picard-torsion conclusion and conjectures simple connectivity in addition to it. The following construction discussion is explicitly an approach to the general surface; its probabilistic dimension/irreducibility evidence is not a universal proof.

Public source: https://doi.org/10.4171/OWR/2006/27 . The bound source copy has 460456 bytes and SHA256 3ea3036d53b914e1ae4b1fc4944418a2113a9327d9bc78cac598b6baeebb629e.

The source's conjectural language is not used as a theorem or an exhaustive present-day status certificate.

## Exact mathematical dependencies

The partial proof uses Riemann–Roch and Serre duality for line bundles on a smooth projective surface, nefness of the canonical divisor on a minimal surface of general type, Hodge index and adjunction parity, the exponential and universal-coefficient sequences, finite-cover/projectivity comparison, Noether's inequality, and elementary finite-group arguments. These do not depend on finite-field experiments or unreproduced numerical algebra.

The weaker Noether bound K^2>=2chi-6 is stated in the introduction to Mendes Lopes–Pardini, arXiv:math/0512483v3, https://arxiv.org/abs/math/0512483 . Its use on a finite étale cover gives degree<=6. We deliberately avoid relying on the sharper degree<=5 classification. Perfectness then excludes every nontrivial group of the possible orders by the explicit order-by-order argument in PROOF.md.

The torsion-to-bicanonical-decomposition argument is already stated by Reid and appears in later Godeaux treatments. The converse is reconstructed directly by Hodge index on the smooth surface. The connection between numerical triviality and torsion for p_g=q=0 is also explicitly recalled in Chen–Shin, arXiv:2608.27317v1, §2. No novelty is claimed for these standard consequences.

## Schreyer–Stenger: known family versus all marked surfaces

1. “An 8-dimensional family of simply connected Godeaux surfaces,” arXiv:2009.05357v2, 26 January 2022, https://arxiv.org/abs/2009.05357v2 . The current arXiv landing page was checked and still identifies v2 as the latest version. The introduction, §§1,3,5–6, Corollary 5.2, Proposition 5.6 and the surrounding argument were inspected; the final summary page was also visually inspected. The marked construction assumes no fixed part and four distinct simple bicanonical base points. Corollary 5.2 proves a locally complete eight-dimensional simply connected family. Section 6 explicitly retains the issue of special lines leading to further smooth surfaces. This does not show that all marked torsion-free surfaces belong to that family.

2. “Marked Godeaux surfaces with special bicanonical fibers,” arXiv:2201.12065v1, https://arxiv.org/abs/2201.12065v1 ; published in Journal of Pure and Applied Algebra 228 (2024), 107765. The current arXiv landing page was checked and lists only v1. The introduction, Lemma 2.1 with proof, torsion-fiber characterization in Theorem 2.2, §4 and Summary were inspected. The Summary was visually inspected. The analysis includes special loci and finite-field experiments; it does not exclude all remaining special lines over C. The computational observations are not promoted to universal statements.

The first family's members with the stipulated marked minimal-surface hypotheses provide positive examples. Trivial torsion gives every-member 2-connectedness by Theorem 1 of PROOF.md. This verifies compatibility of the known positive family with the target; it does not imply that the family exhausts the target.

## Catanese–Pignatelli

“On simply connected Godeaux surfaces,” Complex Analysis and Algebraic Geometry (2000), 117–153, https://doi.org/10.1515/9783110806090-007 . The author's actual PDF was found at https://pignatelli.maths.unitn.it/papers/godeauxdg.pdf after the older Göttingen PostScript link returned 404. Text extraction from the author PDF has broken font encoding, so pages 1–10 were rendered and OCR was used to locate the relevant material; selected formulas were checked visually. The introduction distinguishes trivial torsion from simple connectivity and states a classification strategy, not a solution of the full topological problem. The title cannot be used as a universal theorem. Its bicanonical-curve analysis is reproduced in Schreyer–Stenger's Lemma 2.1, which was read directly in usable text.

## Recent counterexample leads checked

- Dias–Rito, “Z/2-Godeaux surfaces,” arXiv:2009.12645v3, 28 April 2026, https://arxiv.org/abs/2009.12645v3 ; Journal of Algebra 701 (2026), 340–357, https://doi.org/10.1016/j.jalgebra.2026.04.035 . The current arXiv version, abstract and introduction were read from the PDF. Its scope is precisely torsion Z/2, and its topological group conclusion is Z/2 for that class. If tau is the nonzero order-two class, Riemann–Roch gives D in |K+tau|, so 2D belongs to |2K| and D.D=1. This fails the every-member 2-connectedness hypothesis. It also cannot have a reduced four-point bicanonical base scheme when the pencil has no fixed part: at a base point the equation of the double member has zero linear term, so two pencil generators cannot generate the maximal ideal. Thus these are not counterexamples to the target. The publisher page's direct fetch returned 403; the final arXiv PDF was used instead.

- The established Z/3 and Z/5 marked families have opposite-torsion decompositions D_tau+D_-tau of intersection one. They too fail the every-member condition, even though they can have four simple base points.

- Rito, with appendix by Gleissner and Ruhland, “Computation of Singular Godeaux Surfaces and a New Explicit Fake Quadric,” arXiv:2509.08198v2, 10 July 2026, https://arxiv.org/abs/2509.08198v2 . The current record and PDF introduction were inspected. The Godeaux examples discussed there are in a Z/2 family. Their smooth minimal resolutions retain that torsion obstruction. The cover of a singular canonical model producing a fake quadric is not a finite étale cover of a smooth numerical Godeaux surface and cannot contradict the finite-cover bound proved here.

- Chen–Shin, “Numerical Godeaux Surfaces with many disjoint (-2)-curves and Applications,” arXiv:2608.27317v1, 27 August 2026, https://arxiv.org/abs/2608.27317v1 . The current record, introduction, main statements and §2 were read. The main bound concerns disjoint negative curves and does not state a universal topological simple-connectivity theorem.

- Franciosi–Rollenske, “Canonical rings of Gorenstein stable Godeaux surfaces,” arXiv:1611.06810v1, https://arxiv.org/abs/1611.06810 . Its introduction and TheoremA were read. It explains the algebraic/topological distinction but concerns stable surfaces and large torsion in its main theorem. The historical remark about an infinite topological group is not treated as a current global-openness certificate.

## Bounded status finding

Targeted searches covered the exact connectedness formulation, the original contribution and title, torsion-free marked Godeaux surfaces, the Schreyer–Stenger continuation, fundamental-group/Noether routes, and recent 2025–2026 Godeaux leads. The inspected sources did not supply a theorem covering all target surfaces or an explicit counterexample satisfying both hypotheses. This is a bounded negative finding, not an exhaustive literature certification. The proof's conclusions remain valid without assuming that the target is globally open.

## Precise residual gap

Every target surface is algebraically simply connected, but the current argument leaves an infinite topological fundamental group with no finite quotients possible. A proof could close this through finiteness/residual finiteness specific to this class, a complete smooth-deformation classification, or a uniform topological computation of the bicanonical fibration. None of those missing statements is assumed or established. The result must remain PARTIAL.
