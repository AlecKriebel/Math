# Published-paper impact assessment: rows 39, 43, 45, 51

Checkpoint: 2026-10-07 08:02:58 PDT. Bounded assessment complete: **100%**. No external individual contacted; no git operation, spreadsheet mutation, or proof-certification claim. Read workspace AGENTS.md, inventory entries, final manuscript introductions/theorems/contribution statements, relevant priority records, and exact source-archive members. This is an importance/credit assessment assuming correctness, not a fresh full proof audit. Scores are judgment calls with roughly ±0.5 uncertainty.

**A** = importance of the paper's mathematical conclusions if correct and newly established; **B** = this paper's actual incremental contribution after credited upstream results, established reductions, and the author's prior public disclosures. A high A does not confer the upstream breakthrough on the follow-on author. Archive checks below prevent scoring abandoned ambitions as the published paper.

| Row | Published paper | Recommended A | Recommended B | Interpretation |
| --- | --- | ---: | ---: | --- |
| 39 | Two consequences of group-algebra and planar Fourier certificates: wreath products and triangle bounds | **7.5** combined | **4.5** | Wreath counterexample 7.5; planar triangle-program equality 7.0; the imported exact two-point bound itself would be 8.0. Two unrelated consequences do not add their scores. |
| 43 | L2-acyclicity and cost for a rank-100 amalgam | **8.5** | **5.0** | Resolves a central measured-equivalence-relation comparison question if novel; the added direct invariant proof is useful but classical and specific. |
| 45 | Reduced C*-algebras of the Thompson family: an attributed consequence of nonamenability | **8.0** | **4.0** | Significant classical examples, but all decisive simplicity and trace reductions preexist. |
| 51 | A sharp dyadic threshold in a characteristic-two random-cone construction | **5.0** for its actual main new theorem | **4.5** | Exact calibration of one fixed construction; do not score as an independently discovered Kaplansky counterexample. Its inherited scalar-idempotent conclusion considered alone, hypothetically new, would be approximately 9.0. |

## Row 39: two independent topics in one note

**Actual claims.** There are finitely generated Hopfian groups A,H, with A=C2, such that the standard restricted regular wreath product A wr H is not Hopfian. Its particular surjective noninjective endomorphism fixes H, splits, and has explicitly identified kernel R(1-ba), R=F2[H]. Separately, for the precise real-Schwartz two-point and triangle Fourier programs defined in the paper, L2=2/sqrt(3) and P2=4/3. The triangle objective is unrooted; the AIM formulation's square root equals L2. This answers only the planar numerical subcase, without a triangle optimizer or an all-dimensional conversion theorem.

**Lay explanation.** Two groups can each resist being collapsed onto a smaller copy of themselves, yet putting copies of one at the positions of the other can destroy that property. In an unrelated circle-packing calculation, a more elaborate three-point Fourier optimization reaches exactly the same sharp planar bound as the two-point method.

**Importance.** The wreath component answers Kourovka 21.22 and Bradford–Fournier-Facio Question 1.14 for the standard regular restricted action. It is a meaningful specialist negative answer: **A 7.5**. It should not inherit the full importance of the original group-ring direct-finiteness counterexample. The planar result pins down a specific optimization program; **triangle A 7.0**. The statement L2=2/sqrt(3) is itself an important sharpness theorem about Cohn–Elkies, **A 8.0**, but the new planar function supplying it is wholly imported. This paper neither newly proves that triangular packing is densest nor settles the full AIM problem. For a single combined row use **A 7.5**, with these components visible, rather than rewarding the accidental combination of subjects.

**New versus inherited.** OpenAI supplies the one-sided-inverse defect and sharp planar Schwartz certificate. Bradford–Fournier-Facio already characterize wreath Hopficity in terms of direct finiteness; the finitely generated Hopfian embedding is established. Cohn–de Laat–Salmon already supply the product-program comparison; lattice Poisson summation is standard. The paper's added value is explicit deductions, conventions, reconstructed proof bookkeeping, and independent validation artifacts, including substantial finite planar checks. Those are credible verification/exposition contributions rather than a new research mechanism: **B 4.5**. Both the paper and its final attribution audit explicitly decline independent-breakthrough and first-priority claims.

Primary prior sources: [Bradford–Fournier-Facio, published institutional record](https://www.repository.cam.ac.uk/handle/1810/376427), [Cohn–de Laat–Salmon, Proposition 4.7](https://arxiv.org/html/2206.15373), and the paper's exact pinned OpenAI inputs. Product comparison is an infimum comparison; a naive product g(x)g(y) need not satisfy the triangle sign conditions.

## Row 43: cost versus L2-Betti numbers

**Actual claim.** For Gamma=F(a,b1,...,b99)*_J(J x Z), J generated by b1,...,b99 and w=ab1ab2...ab99a, the displayed 101-generator/100-relator presentation is a finite two-dimensional K(Gamma,1), and every L2-Betti number is zero. Every essentially free p.m.p. action has the same vanishing invariants. Its free ergodic Bernoulli relation has cost at least 1+1/(100*2^61), whereas the infimum cost over its free actions is one. Consequently the relation-level cost–Betti inequality is strict, while group-infimum equality survives. Infimum one does not assert attainment by an action.

**Lay explanation.** A standard measure of how many connections are needed to describe a random group action can be strictly larger than the group's homological measure predicts. The paper also directly checks that all of this group's L2-homological invariants vanish, without relying on those cost estimates.

**Importance.** A correct new strict example would answer Gaboriau's longstanding cost versus L2-Betti question and would be a major result in measured group theory/orbit equivalence: **A 8.5**. It is broader than an isolated numerical example, but not a major-area revolution deserving 10. The explicit cellular acyclicity computation by itself is a much narrower theorem, around **A 5.5**. The size of the positive rational gap is incidental: any positive gap supplies the qualitative counterexample.

**New versus inherited.** The actual group, actions, and positive Bernoulli cost lower bound are OpenAI's fixed-price construction. Gaboriau supplies comparison and action invariance. The general fixed-price-to-cost–Betti implication is explicitly in [Popa–Shlyakhtenko–Vaes, Remark 6.6](https://arxiv.org/html/1811.06929#S6), and the author's earlier public triage already states the first-Betti limit deduction. The follow-on adds a complete elementary regular-tree/Fox-boundary proof, verifying the exact presentation's asphericity and all-degree vanishing independently of both cost bounds. Its priority audit correctly observes that standard amalgam classifying-space arguments plus the previous first-degree result would already yield all-degree vanishing; the tree convolution fact is also a known special case of analytic zero-divisor theory. Thus this is substantive concrete alternative-proof content, not a new general invariant method or independent fixed-price discovery: **B 5.0**.

[Gaboriau's own FAQ](https://perso.ens-lyon.fr/gaboriau/Travaux-Publi/FAQ.pdf) identifies the relation-level equality as an open question and distinguishes it from fixed price. This supports the high hypothetical theorem score while the paper's explicit dependency record supports the lower incremental-paper score.

## Row 45: the Thompson reduced C*-algebras

**Actual claim.** Reduced group C*-algebras of standard F, T, the full abstract Aut(F), and abstract Comm(F) are simple and each has only its canonical tracial state. Also every countable subgroup of circle homeomorphisms containing the specified standard circle action of F has those properties. This concerns reduced algebras, full automorphism groups, and a particular action-containment hypothesis; it is not a theorem about the full group C*-algebra or every abstract embedding of F.

**Lay explanation.** The operator algebras built from four famous Thompson groups have no nontrivial proper closed ideals and admit only one normalized trace. These properties follow once the new nonamenability result for F is inserted into previously published equivalences.

**Importance.** These are important test examples in C*-simplicity and group dynamics. Taken as genuinely new conclusions, the four-group package merits **A 8.0**, with F and T doing most of the work. The corresponding longstanding F nonamenability breakthrough is important in its own right but is not this author's new proof. Unique trace for T was already unconditional and adds no newly solved problem.

**New versus inherited.** [Le Boudec–Matte Bon, Theorem 4.1 and Corollaries 4.2/4.4](https://www.numdam.org/item/10.24033/asens.2361.pdf) already state the precise simplicity equivalences and overgroup consequence. BKKO already gives the amenable-radical/unique-trace theorem. OpenAI supplies the only new decisive nonamenability input. The paper collects those consequences, checks countability/group identifications, and supplies audits and scope clarification. There is no new criterion, proof mechanism, or independent nonamenability proof: **B 4.0**, an accurate technical consequence note. Its archive explicitly states that dependence on OpenAI's input is unchanged.

## Row 51: the actual threshold paper, not the earlier idempotent ambition

**Actual main contribution.** In the October 4 construction's unchanged seven-extra-letter projective-plane model, q=32 is the least dyadic q>=4 for which the squared turn matrix has spectral radius below one, independent of allowed inverse pairing. An invariant three-class quotient and exact positive rational vectors certify decay at 32 and exponential growth at 4,8,16. Propagating all affected probabilistic/geometric estimates yields the same existential random-cone construction on a 532-edge rose rather than 8260. The lower-order obstruction is to this specified word-mass decay criterion, not to other constructions or proof estimates.

**Additional asserted consequence.** Classical HNN embedding carries the example to a two-generator finitely presented torsion-free H with a finite two-dimensional classifying complex. For every characteristic-two field K, K[H] has a scalar idempotent e other than 0,1 and a nonzero cyclic projective right module P=eK[H] with K[H] isomorphic to K[H] direct-sum P and [P]=0. These consequences are inherited and were already disclosed in the author's triage. They do not assert K0(K[H])=0, characteristic zero, odd characteristic, or a reduced C*-projection counterexample.

**Lay explanation.** The paper proves how small one particular group-ring construction can make its projective-plane parameter while retaining its key decay estimate. This reduces the size of that recipe, while the dramatic counterexample to familiar group-ring expectations comes from the earlier credited construction.

**Importance and credit.** The exact threshold is independently checkable and a legitimate narrow refinement. Its novelty consists of calibration plus complete propagation of parameter changes, without a new method or broader theorem. **A 5.0; B 4.5**. The 532-edge count is not globally optimal in generator number: the classical embedding already produces a two-generator host, and one-generator torsion-free groups cannot support the idempotent. A scalar characteristic-two torsion-free idempotent example considered hypothetically new would warrant about **A 9.0**, but that is emphatically not the incremental discovery in this published note. Scoring this row as a fresh Kaplansky solution would erase the paper's own title, scope, and prior disclosure.

Evidence: final main.tex Sections 1, 2, 3, and Priority; notes/EXTENSION_PRIORITY_ATTACK.md; public triage commit f27318d83bd7000ef817957a9a4b3087de28d198. The mathematical background is [Öinert's primary paper](https://arxiv.org/abs/1904.04847v3), but the exact calibration is supported by the local final theorem and certificate package rather than a literature firstness claim.

## Source-archive custody and version reconciliation

Each archive main source was read with Python zipfile and compared byte-for-byte to the local final source. All four are equal. These are the final archives associated with the inventory/published records; row 39's publication README and receipts explicitly identify the revised ZIP as uploaded, with the old ZIP merely retained historically.

| Row | Archive and main member | SHA-256 of final TeX |
| --- | --- | --- |
| 39 | publication/wreath-planar-verification-v1.0.0-revised.zip → publication/preprint.tex | 27a41032c4812d4b7263bd0a4fc398de2109c12185545f9d25ae8ae1a05787fe |
| 43 | publication/cost-betti-source-and-verification.zip → main.tex | 7475979d063f5ad6e9e85f09fca5eca6f1beb83a83f654bc9011854dc8c4182a |
| 45 | upload-kit/thompson-cstar-source.zip → main.tex | 5a95378741e1a371056251df4d6a492c16169d349ecc02ddb1b0d3ecd791fe92 |
| 51 | source-and-audit.zip → main.tex | a2d6f9dce6b65e23c0a325619ada4a50ba1fcbeb02fda555c0e9debb13b3b5b6 |

No discrepancy between published-source claims and current final manuscript was found. Row 51's versions/duplicate-core-candidate2 and versions/refinement1 are superseded and were not substituted for the final threshold paper. No conventional human peer review or reproduced full upstream Lean validation is claimed by these papers; that affects evidentiary status, while the requested A scores explicitly assume correctness. These scores do not turn automated review into journal acceptance or universal novelty certification.
