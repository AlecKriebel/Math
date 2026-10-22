# Independent audit of the immersed leaf approximation obstruction

Target: rank 670, ID 10300062, AMR-102-0062. Audit date: 2026-10-04 UTC.

## Verdict

**Accept the stated coherent compact-domain obstruction as a valid scoped partial result. Retain an unresolved disposition for the original question.** No fatal mathematical error was found in Theorem 4 or the auxiliary arguments. The frozen packet already states the essential limits correctly. This audit does not establish current literature status, novelty, or a full solution.

The result concerns closed surfaces whose immersions are injective on fundamental groups, and a specified compact-domain coherence requirement. These conventions must remain visible wherever the result is described. The image-set control does not resolve the source's intended topology. A restriction to hyperbolic ambient manifolds remains outside this construction.

The exact author input is bound by SHA-256 `1f64af140ad77607cfd4a0ea61ed418853f9af99740387632b6f30545050b1f6` for the 1,648-byte root manifest. All eight listed payload files match. Originals were preserved. Code replays were run in disposable copies.

## Primary source and category check

Calegari's [2002 arXiv source](https://arxiv.org/abs/math/0209081), Definition 1.1 and printed page 31, was inspected, including the visual page. Question 14.2 has no explicit hyperbolicity restriction. It specifies compact essential surfaces and describes images of expanding balls. It does not formally define the convergence topology, the metric for these balls, or incompressibility for immersed surfaces. Closedness is supported by the adjacent doubling and cycle discussion, but is not an explicit definition in the question. The packet's closed, fundamental-group-injective, induced-metric conventions are therefore adopted interpretations. Tautness is explicitly defined using one transverse circle meeting every leaf; the construction meets that definition. The abstract lists the 2003 proceedings publication; the audit used the arXiv version.

Banagl's [author manuscript](https://www.mathi.uni-heidelberg.de/~banagl/pdfdocs/flatbundles.pdf), Section 6, printed pages 17-18, confirms the Fuchsian boundary suspension's identification with the tangent circle bundle and its genus-two Euler number of -2. Both official PDFs were independently downloaded successfully and matched the author's recorded bytes and hashes. Bibliographic and retrieval metadata appear in `source_verification.json`; no source text or PDF is distributed here.

## Mathematical dependency review

### Uniform closeness and the group obstruction

Lemma 1 is valid. The ambient manifold is closed, so its injectivity radius is positive. Uniformly close maps from the same compact patch are homotopic by short geodesics. Basepoints introduce only conjugacy, which does not affect injectivity. If the composed map through a surface induces an injection, the map from the patch to that surface must also induce an injection. No embedding, immersion, or group injectivity of the second map is needed for this lemma itself.

The choice of patch is important: the leaf contains an embedded once-punctured torus whose inclusion in the ambient manifold is injective on fundamental groups. Thus the obstruction uses an actual copy of the rank-two free group, rather than just two loops that fail to commute inside the patch but might commute in the ambient manifold.

### Central extension and finite index

Lemma 2 is valid for an oriented circle bundle over an oriented closed base of genus at least two with nonzero Euler number.

1. The fiber injects into the total fundamental group because the base has zero second homotopy group. Orientation makes this infinite cyclic kernel central.
2. A closed orientable surface group of genus at least two has trivial center. Its intersection with the fiber is consequently trivial, so projection embeds it in the base surface group. This step does not assume that every subgroup of the total group is centerless.
3. The cover corresponding to the projected subgroup is aspherical. Its ordinary second integral homology is therefore the second group homology, which is infinite cyclic for a closed orientable surface group. An infinite-sheeted cover of the closed base is a connected noncompact surface and has zero ordinary second homology. Hence the cover is finite-sheeted. Compactly supported homology is not being used.
4. In that finite cover, the embedded group gives a right inverse to the pulled-back central extension. A splitting forces the Euler class to vanish. The packet's construction of a map from the aspherical base, followed by a homotopy of its projection to the identity, correctly justifies this without equating an arbitrary group splitting directly with a literal section.
5. Euler number instead multiplies by the positive covering degree and remains nonzero. This is the required contradiction.

The passage to all finite ambient covers is also valid: a prohibited surface subgroup in a finite-index subgroup would still be a prohibited subgroup of the original group. No assumption about how a finite cover changes the Seifert presentation is required.

### Nonorientable and immersed surfaces

For a nonorientable closed surface of genus k at least three, the orientation double cover has orientable genus k-1 at least two. Injectivity would restrict to its subgroup, contradicting Lemma 2. The remaining sphere, projective plane, torus, and Klein bottle groups are virtually abelian. Including low-complexity surfaces that are not normally called essential only enlarges the tested class and strengthens the obstruction.

Self-intersections of an immersed approximant do not affect this argument. For a disconnected approximant, a connected patch maps into a single component. One-sidedness creates no additional exception under the stated fundamental-group-injectivity convention. Disk-incompressibility for immersed surfaces is not silently substituted for that convention.

Closedness is essential to the proof: compact surfaces with boundary can have nonabelian free fundamental groups. The classification used in Corollary 3 would be false for that larger category. The audit makes no negative assertion for approximants with boundary.

### Smooth suspension, Euler number, and tautness

The genus-three to genus-two homomorphism is the map of a degree-one handle pinch. Its surface relator is correct. Composing with the Fuchsian boundary representation gives a smooth orientation-preserving action on the circle. The diagonal action on the product with the universal cover is free and properly discontinuous because its first factor is a deck action. Its quotient is a closed smooth circle bundle.

Horizontal tangent planes are invariant since the circle action in each deck transformation is independent of the base point. They therefore descend to a smooth foliation. Circle orientation gives its transverse orientation. Bundle naturality, or the classifying-space description of the representation, gives Euler number -2. The pinch map itself need only be continuous; smoothness of the suspension does not depend on differentiating it.

For every point of the circle, its stabilizer contains the kernel of the pinch homomorphism, hence the once-punctured-torus subgroup. The corresponding leaf is the universal cover of the base divided by that stabilizer. It covers the whole base, so one circle fiber meets every leaf transversely. Over the collapsed handle, a component of the covering maps homeomorphically to the handle. Normality of the kernel also handles changes of basepoint or conjugate handle subgroups.

The retraction sending the first two handle generators to x,y and the next pair to y,x respects the genus-three relator, because the two commutators are inverses. It proves injection of the patch group directly. Composing the patch inclusion with projection to the base then proves ambient injectivity; this does not rely on an unproved immersed loop theorem.

A compact leaf would be a finite-sheeted cover of the genus-three base and would supply a forbidden closed surface subgroup. Thus the leaves are noncompact. Leafwise completeness with the induced metric is consistent with the smooth compact ambient construction; it can also be seen by completeness of the leafwise geodesic flow on the compact unit tangent bundle of the tangent distribution. Only the compact patch is needed for the obstruction.

### Conclusion and nonvacuity

Subgroups of virtually abelian groups are virtually abelian, whereas the rank-two free group is not. In a finite-index subgroup of that free group, positive powers of the two free generators occur and cannot commute. Lemma 1 therefore excludes sufficiently close factorizations through every permitted closed surface. This proves Theorem 4 in its exact stated scope.

The existence of vertical essential tori also checks out. The bundle restricted to an essential base circle is trivial, and the induced total group is the preimage of an injective infinite cyclic subgroup of the base, giving an injective rank-two abelian subgroup. Thus the obstruction is not merely absence of every closed essential surface.

## Convergence and auxiliary results

The degree-n torus immersion is fundamental-group-injective and has the asserted pullback metric. Choosing representatives in the coordinate square makes every point of the target torus the image of a domain point within distance at most pi times the square root of two. Thus for integer n at least five the radius-n ball has exactly the entire target torus as its image. A coherent approximate right inverse would induce an integral right inverse to the diagonal matrix with entries n and 1; its first diagonal entry would require n times an integer to equal 1. This is impossible for n greater than one.

This control disproves an automatic inference from image convergence of a given sequence to coherent lifts for that sequence. It does not provide a leaf for which every weakly approximating sequence fails coherence: in this example the identity torus is an alternative coherent sequence. Nor does it prove existence of weak image approximation in the nonzero-Euler example. The packet correctly uses it as a warning about a missing implication, not as a solution of the original existential question.

The irrational-plane positive example is valid. Rational independence of 1, square root of 2, and square root of 3 excludes any nonzero fixed integral vector perpendicular to the limit normal. The subsequence argument then forces the lattice systoles to infinity. The chosen radii tend to infinity while staying below the injectivity radii and making angular error times radius tend to zero. Nonprimitive normals do not cause a problem: the perpendicular plane's integral lattice is saturated and gives an embedded torus.

The folded-double kernel has the asserted nonzero abelianization. The invariant-measure obstruction is valid: a locally finite transverse measure restricts to a finite measure on the compact complete circle transversal; holonomy transfers any nonzero mass to this transversal. A hyperbolic circle transformation forces finite invariant mass onto its fixed points, and two disjoint fixed-point pairs rule out a common invariant probability. Finally, the positive-form area estimate has the necessary orientation and null-homology assumptions. No bound on a distant closing region follows from it.

## Replay and release findings

The author's `verify.py` passed in an isolated copy and regenerated `verification_results.json` byte for byte. The author's inventory check passed for the clean freeze. Independent character-based word reduction checked the pinch, retraction, fold, and 4,096 pairs of positive powers; deliberately wrong retraction and fold orientations were rejected. Euler pullback and torus-cover divisibility were independently sampled through degree 1,000. These are finite guardrails, not proofs of the topological or asymptotic statements.

One minor packaging defect was found in the original inventory checker. Its exclusion by basename ignores an unlisted nested file named `MANIFEST.json`. The original checker also has no external hash binding for its root manifest. Negative controls reproduce both behaviors; neither affects the clean, exact input audited here. `verify_binding.py` supplies a read-only supplementary check that pins the root manifest's hash and size, excludes only that root file from the payload inventory, and rejects symlinks, duplicate entries, missing files, extra files, and byte changes. It uses explicit exceptions rather than Python assertions.

The full public-dataset fallback files were independently rehashed against a fresh read of the public repository manifest. Both matched, and both complete target records matched the extracted copies. The exact whitespace-normalized target statement had only the requested numeric ID. `dataset_binding.json` records only public hashes, counts, and match results. This confirms provenance; the upstream report's broad literature assertions do not establish a theorem or a current open-status certificate.

## Disposition and portable replay

No correction to the mathematical proof is required for its expressly limited theorem. Keep the original packet unchanged and carry this audit, particularly its source/category distinctions and stronger binding verifier, as a supplement. Keep the original-question outcome unresolved. The five approach families are substantively distinct; whether they fulfill a five-turn campaign ledger is an accounting decision beyond this mathematical audit.

With Python 3.10 or newer, run from this directory:

    python3 -B verify_binding.py ../packet
    python3 -B replay_controls.py ../packet
    python3 -B verify_audit_manifest.py

The audit directory contains authored review text, code, and public verification metadata only. It contains no source PDFs, source text, datasets, private paths, or coordination records. No remote writes, submissions, or external communications were performed.
