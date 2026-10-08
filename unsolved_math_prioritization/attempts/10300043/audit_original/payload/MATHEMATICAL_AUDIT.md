# Independent audit of short geodesics and taut foliations

Problem 10300043 / AMR-102-0043, rank 1008. Review date: 2026-10-08 UTC.

## Disposition

**Accept the original author_v1 packet as an unsolved investigation with five scoped approaches.** The complete authored proof was read, all seven numbered propositions were reviewed, and the stated source scopes were checked directly. No mathematical correction is required. The original proof, metadata, bootstrap, manifest, and archive remain unchanged.

This accepts the deductions under their stated hypotheses. It does not accept a solution of Calegari Question 10.5, a geodesic counterexample, a uniform length gap, a novelty claim, an exhaustive current literature status, or machine verification of the topology. The original author metadata saying that independent review was pending remains historical; this separate report supplies the later disposition without rewriting that freeze.

## Authenticated review object

- Original proof: 21,275 bytes; SHA-256 e095f3cbfb4876a19d01be1558307267031c1eee4af08fcda8ace38e39077f5e.
- Original manifest: 1,648 bytes; SHA-256 24e4e0b001028a38091b1293b490e36227fda8d2ee73f726ef316f2eb0fe4c96.
- Original bootstrap: 3,752 bytes; SHA-256 10efdf3b3290b84365e6cad3e84822f322aa5e7f6778e2551addb2ab9329076c.
- Original ZIP: 24,197 bytes; SHA-256 b2d5c49b421e530bdf3863d12ddb753ff9884f4f217ed1c244120b9c38c70fe1.

All 13 ZIP members were compared byte-for-byte with the actual freeze. The manifest's members were separately rehashed before author code was executed. This audit treats those externally supplied original pins as the trust boundary; it does not claim protection against coordinated replacement of every trust anchor or concurrent hostile filesystem modification.

## Exact target and source scope

Calegari's printed Question 10.5 on page 24 distinguishes isotopy from a separate homotopy question and asks for a threshold uniform across the ambient manifold and the specified taut foliation. Its wording itself adds no closedness or coorientation qualifier. The proof announces its narrower closed, orientable, cooriented category and does not silently remove those restrictions. The question page and introductory definitions were checked in the retained primary source. [Calegari 2002](https://arxiv.org/pdf/math/0209081v1)

For the isotopy discussion, both primitiveness and embeddedness are explicit. A primitive class need not have an embedded geodesic in general. The primitive-root step below concerns free homotopy classes; it is not a proof of embeddedness. Leafwise homotopy representatives are allowed to be circle maps and need not be simple curves in a leaf. These conventions agree with the scope of the cited loop criterion rather than enlarging it into a knot theorem.

Kano's article globally assumes a closed oriented manifold and transverse orientation. Immediately before Proposition 6.1, it expressly removes the leafwise-hyperbolicity assumption for that proposition. The fixed-leaf and strict-motion alternatives, and the following statement about two-sided branching, were checked on printed page 14 in text and an image. This supports the author's exact use of the criterion. [Kano 2012](https://arxiv.org/pdf/1203.2413v1)

In Calegari's Gromov-norm paper, the length in Section 3.2 is a homotopy/foliation subdivision invariant, not ambient geodesic length. Lemma 3.2.2 and its proof on pages 17-18 provide the claimed obstruction in the presence of two-sided branching. They supply no sequence of ambient geodesic lengths approaching zero. The relevant definition, statement, proof, and page images were checked. [Calegari 2001 version](https://arxiv.org/pdf/math/0007120v2)

Breslin's Theorem 1 attributes a fiber-genus-dependent unlinking result to Otal in closed hyperbolic mapping tori. The relevant geodesics are simple. Breslin's own Theorem 4 has a strongly irreducible Heegaard surface as input, not a prescribed foliation leaf. The statement on page 1, the Heegaard statement, and the area-method discussion were checked. No genus-independent threshold follows merely by taking all genera in the stated theorem. [Breslin 2011](https://arxiv.org/pdf/0912.3496v2)

The full original Otal proof was not available for this review and is not certified. The author's provenance remains “Otal, as stated in Breslin.” An independent attempt to open the [Otal chapter DOI](https://doi.org/10.1017/CBO9780511542817.005) through the web tool failed. The earlier publisher-abstract/definition inspection is retained as the author's reported provenance, not relabeled as a new successful inspection by this reviewer.

The public arXiv records for all four retained PDFs were independently opened and their title/version histories checked. All four PDF hashes, both whole-corpus hashes, and the unique selected problem/report binding replayed successfully. Each retained text-extraction hash was independently checked; fresh pdftotext -layout extractions reproduced all four hashes. Source bytes, extracted text, screenshots, and corpus contents are excluded from this audit deliverable.

## Proposition 1.1 and the primitive root step

**Accepted.** Equality and the two strict comparability alternatives exhaust the complement of the author's “bad” condition by the credited criterion. The deck action preserves transverse orientation, so conjugating transports a witness. The witness for an inverse can be moved from lambda to g lambda, reversing the direction. This covers equality as well as strict comparisons.

For powers, if h fixes a leaf, every power fixes it. If h moves a leaf strictly upward, iteration of the order-preserving action gives an increasing chain; transitivity compares its endpoints. The downward case is identical, and inversion supplies negative powers. Thus non-badness passes from an element to every nonzero power; the stated badness implication passes from a power to its root. No converse is used.

The fixed-leaf construction produces a path from x to gx inside one connected lifted leaf and hence a leafwise loop downstairs. It does not promise an embedded loop. The transverse direction retains its source attribution; finite order controls do not replace that geometric input.

In a closed hyperbolic manifold, nonidentity elements are loxodromic and their cyclic axis stabilizers have primitive generators. If g=h^n, translation length is |n| times that of h. Consequently a bad class has a bad primitive root of no greater length. This uses the standard torsion-free discrete hyperbolic group setting and is valid for conjugacy classes even if their geodesic images are not embedded.

The warning against deriving badness of all powers is appropriate. The independent test includes an abstract antichain permutation whose square fixes every point. It is only a countercontrol for unrestricted order reasoning; it is not presented as a constructed taut foliation or hyperbolic counterexample.

## Proposition 1.2 and quantifier discipline

**Accepted.** In the declared category, D is an extended nonnegative infimum over primitive bad classes. If D is positive and finite, D/2 is a valid threshold; if the set is empty, every positive threshold works. A shorter nonprimitive bad class would have a still shorter bad primitive root and contradict the definition of D. Conversely, any valid positive threshold is a lower bound for every primitive bad length.

The proof establishes an equivalence, not positivity of D. A positive systole on one fixed compact manifold only produces a vacuous below-systole threshold on that manifold. Covering a chosen geodesic preserves its local metric; a closed lift may require an iterate and then has a positive integer multiple of its length. Neither operation gives the missing universal estimate. Two-sided branching supplies a qualitative class obstruction but no shrinking-length family.

The R-covered special case is correct because every pair of leaves is comparable. The more general one-sided-branching statement is attributed to the cited literature. None of these homotopy facts controls knot type.

## Proposition 2.1 on normalized periods

**Accepted.** For the stated smooth bundle with connected fiber, alpha=p*(dt) is a global, nowhere-zero, normalized closed form. Compactness makes its norm supremum finite, and nonvanishing makes it positive. The line-integral estimate applies after a rectifiable loop is reparametrized in the usual absolutely continuous manner. The resulting integer period must vanish under the strict length bound. Equality at the bound would not suffice, and an arbitrary nonintegral period would invalidate this inference.

The pullback bundle over the real line is smoothly trivial, and a zero-degree loop lifts as a closed loop there. Projection to a fiber supplies a homotopy. For nonzero degree n, replacing the lifted height coordinate by a linear function preserves the endpoints. The fiber-coordinate path can be smoothed in its relative path class and made constant near the endpoints. In a mapping-torus trivialization, those endpoint germs match under monodromy, so the quotient loop is smooth and its alpha-value has constant nonzero sign.

The final embedding statement is justified by the density of embeddings of a compact one-manifold in a three-manifold under sufficiently small generic C1 perturbations. Transversality is open in that topology. It is not an embedded leafwise statement for the zero-degree case and is not an isotopy statement about an initially specified knot.

## Proposition 2.2 on the norm under isotopy

**Accepted.** The t-derivative of the displayed shear is 1+a chi eta' sin(nx), with a strictly positive lower bound independent of n. For each fixed (x,y), this is an increasing interval diffeomorphism fixed near both ends. Keeping x and y unchanged yields a global box diffeomorphism, and identity near the boundary allows extension to M. Scaling a by the isotopy parameter keeps the same positive derivative bound.

At the chosen center, where the cutoffs are identically one and x=0, the pulled-back form is dt+an dx. The reverse triangle inequality for the fixed covector norm gives at least an|dx|-|dt|, which diverges. This directly validates the claimed unbounded norm without an assumption that the metric is Euclidean in the box.

The pullback foliation varies within the ambient-isotopy class of the original foliation. Transporting a tangential or transverse representative by the diffeomorphism preserves the property, and the diffeomorphism itself is isotopic to the identity. Thus the same knot isotopy classes have the alternatives. The literal fixed plane field need not remain unchanged. This is the sense expressly used in the proof. The calculation degrades one particular sufficient bound; it does not disprove an optimal uniform bound.

## Proposition 3.1 on the meridional calibration

**Accepted.** In normal Cartesian coordinates, eta=((cosh r-1)/r^2)(x dy-y dx). The scalar factor has the convergent even series sum over j>=0 of r^(2j)/(2j+2)!, including value 1/2 at the axis. Hence eta is genuinely smooth there. Both this radial coefficient and x dy-y dx are invariant under rotations, while the form is independent of z. It therefore descends under every stated loxodromic twist and translation.

Away from the axis, omega equals the wedge of the unit radial and angular covectors. Its comass is exactly one; the smooth extension and normal-plane value retain that property at the axis. Stokes' theorem applies to the compact oriented source surface, even when its map is nonembedded or has critical points. Each signed standard meridian contributes 2 pi(cosh R-1). The pointwise comass inequality bounds the pulled-back integral by parametrized area with multiplicity, producing the claimed absolute-value bound.

For k nonzero, the conditional upper radius inequality is an algebraic rearrangement followed by monotonicity of cosh on nonnegative radii. It requires an independently supplied area upper bound B. The author supplies none for an arbitrary taut foliation and does not assume tube intersection creates the required meridional boundary surface.

The zero-twist longitudinal annulus has area integral_0^R integral_0^ell cosh(r) dz dr = ell sinh R. Its angular differential vanishes, so omega restricts to zero. It does not meet the meridional-boundary hypothesis. The example correctly prevents transferring the disk bound to a longitudinal annulus.

## Proposition 4.1 and stability of the filling core

**Accepted.** A foliated collar identification, rather than only a slope match, ensures the disk extension is smooth across the gluing torus. The disk-foliation defining form dt evaluates nontrivially on the core tangent. This produces the promised embedded transversal and therefore the transverse alternative for any knot already ambient-isotopic to that core.

Every newly attached disk meets the gluing boundary, so a leaf containing it also has an exterior portion. Under the stated additional hypothesis, a closed transversal contained in N meets that portion and remains transverse after extension. This proves tautness in the explicitly specified every-leaf formulation. No weaker assertion that a boundary-ended transverse arc can always close is used. Other boundary components or coorientation conventions do not supply hidden conclusions.

The stability observation is also correct: positivity on the compact core has a positive minimum, and sufficiently small C0 change of the defining form preserves it. Integrability remains a separate premise. The proposition does not prove existence for arbitrary filling slopes, hyperbolicity of any filling, or isotopy between a hyperbolic geodesic and the topological core without that additional assumption.

## Proposition 5.1 on small nongeodesic trefoils

**Accepted.** A fixed compact coordinate ball supplies a uniform upper comparison of Riemannian and Euclidean norms. Scaling a smooth local trefoil therefore makes its length arbitrarily small without changing its local knot type. It is nullhomotopic in the ambient manifold because the ball is contractible.

For a transverse circle, the globally defined form alpha evaluates continuously with a fixed nonzero sign on its tangent. Its integral cannot vanish. The nullhomotopic knot has zero period, and isotopy preserves that period, ruling out every transverse representative.

If the knot were isotopic to a simple curve in a fiber, fiber injectivity on fundamental groups would make that curve nullhomotopic in the fiber. The surface disk theorem for simple nullhomotopic circles supplies an embedded disk. Pulling the disk back along the ambient isotopy and lifting it to the universal cover gives an embedded spanning disk for a lift of the small trefoil in R3. An embedded smooth spanning disk makes its boundary an unknot, contradicting the local trefoil type.

The displayed braid-relation group maps onto the nonabelian group S3 with the indicated two transpositions. The standard trefoil Wirtinger identification and the cyclic unknot complement group justify the nontriviality conclusion. The independent exact permutation check verifies the relation, noncommutation, and generation; it does not mechanically prove the Wirtinger theorem or disk theorem.

Finally, a nonconstant nullhomotopic closed geodesic would lift to a closed geodesic in H3, which is impossible. Thus every small trefoil in this construction is outside the geodesic target. The distinction is essential and is maintained throughout the packet.

## Independent execution and negative controls

The author's 84-case control suite was replayed successfully. An independently written suite contributed 111 scenario results: accepted baseline and source/corpus replay plus rejected payload, inventory, bootstrap, manifest, JSON-claims, source, and missing-corpus corruptions, each in normal, -O, and -OO modes. The independent suite itself was run in all three optimization modes, with byte-identical JSON results.

The actual frozen files, not merely writable copies carrying a read-only label, were used for the baseline. Effective UID was 1000. All 13 frozen files rejected O_WRONLY opens, and both frozen directories rejected file creation. Actual file modes were 0444 and directory modes 0555. Execution occurred with the actual read-only freeze as the working directory. Whole-tree byte and mode snapshots were unchanged afterward. This is verified operating-system permission protection for the tested non-root process; it is not a claim of a read-only mount, protection against the owner deliberately changing modes, or concurrent-adversary isolation.

Exact controls include all 242 labelled partial orders of sizes one through four, 419 automorphisms, 5,028 root implications, 1,495 conjugacy checks, integer-period strictness and integrality controls, rational hyperbolic identities and radius inequalities, a comass inequality, rational rotation invariance, smooth-axis series coefficients, shear positivity, and the trefoil quotient. Their labels explicitly restrict them to finite algebraic diagnostics. The manual arguments above, together with credited standard and published inputs, are what justify the mathematical disposition.

## Remaining blockers to a solution

1. No uniform positive D and no sequence of bad primitive classes with geodesic lengths tending to zero is constructed.
2. No theorem converts these homotopy deductions into the requested knot isotopies for an arbitrary prescribed foliation.
3. No foliation-independent area budget or meridional spanning-surface existence theorem is established.
4. No filling construction preserves the necessary bad leaf-space action while producing arbitrarily short geodesic cores.
5. The manifold and foliation restrictions are not removed, and the credited genus-dependent bundle theorem is not upgraded to a universal one.

The five methods are mathematically distinct and support the recorded five-approach accounting. This review does not independently reconstruct a historical conversation-turn log or repeat every repository duplicate-search query. The packet's bounded search and retrieval narratives remain explicitly provenance claims, not proofs that no earlier attempt or later literature resolution exists.

No correction patch or corrected author manifest is needed. Acceptance is limited to the unchanged, externally pinned author_v1 packet and the scoped conclusions detailed here.
