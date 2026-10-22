# Post-seal cross-check: matching theorem and publication framing

## Outcome

**PASS for the exact orientation-preserving target as a theorem already recorded in the matching public note.** No mathematical gap was found in the checked main proof of that restricted scope. A new note should cite Ferudun's Theorem 1.1 and present its compact-core argument as an alternative proof of that recorded theorem. It should make no firstness, new-existence, new-mechanism, or current-openness claim.

This is a new supplement. The initial adversary package (10 authored files plus its manifest) and the direct/historical family's initial package (9 authored files plus its manifest) authenticated byte-for-byte before comparison. Their sealed contents were not edited. The latter's full REPORT.md, VERDICT.json and relevant source-inspection receipts were then read. This comparison does not retroactively change either family's independence before its initial seal.

## Authenticated matching source and exact scope

Alper Ferudun, *Unbounded Multiplicity in the Dilatation Spectrum of Every Term of the Johnson Filtration: An Observation on a Question of Farb*, unrefereed preprint, version 1.0, DOI [10.5281/zenodo.23301731](https://doi.org/10.5281/zenodo.23301731), is the matching source. The current [Zenodo record](https://zenodo.org/records/23301731) and [publisher page](https://eulersolve.org/papers/amr-109-0082/) identify the same work.

Three independently retained copies—the present family's publisher download, the direct family's Zenodo download, and the root's Zenodo download—have identical SHA-256:
`f04bac1ae0f63f083777008c50442fa97fc9edc3659b35b789343e017a73d0ed`, 167507 bytes, 13 pages. Their MD5 matches the archival record's file checksum, `730ce1f845948a1645613e45dfe24e25`. The direct family's raw Zenodo JSON and root's public_record.json are also byte-identical.

Theorem 1.1 on physical PDF 2 explicitly quantifies every closed genus g>=2, every k>=1 and every N>=1, with equal dilatation and ambient mapping-class nonconjugacy. Its stronger extended-group/up-to-inversion wording includes the submitted orientation-preserving k>=3 claim. Its indexing paragraph identifies I(k) with ker(Mod(S) -> Out(pi/gamma_(k+1)(pi))), exactly the candidate's zero-based surface-group convention.

Section 7 fixes g,k and its rank-two subgroup before increasing the trace-family size. It counts all pseudo-Anosovs, permits proper powers, and allows the common value to vary. Therefore this is an exact scope match, not a least-dilatation result, an intrinsic-subgroup count, varying-genus construction, simple-loop theorem, or infinite-multiplicity claim at one prescribed value.

## Adversarial check of the orientation-preserving main proof

The actual PDF text on pages 1-9 was inspected in this supplement, with visual inspection of pages 2,6,7,8,9. Below, “passes” is an analytic judgment relative to the explicitly imported standard Teichmüller facts, not a formal proof-assistant certificate or human peer review. The stronger orientation-reversing Lemma 4.4(ii), optional quantitative remarks, primitivity questions and large finite examples are outside this commissioned validation.

### Geometry, genus and depth

The note supplies explicit half-translation square models in genera two and three, followed by connected sums at intersections whose four quadrants belong to distinct complementary disks (Lemmas 3.1/3.2 and Proposition 3.3, PDF 4-5). The displayed cycle counts give genus two for the eight-square seed and genus three for the twelve-square seed. The parity conditions ensure both cylinder cores separate; the no-bigon condition ensures minimal intersection. The connected-sum operation joins four pairs of distinct disks, leaves disks with at least six sides, preserves separation, and increases genus by two when the genus-two seed is added. This supplies every required closed genus without varying it later.

The cylinder shear matrices use opposite twist handedness compared with a convention that takes both Dehn twists positive. The generated mapping-class group is unchanged by replacing one generator with its inverse. Lemma 4.2's actual printed ping-pong arcs are |x|>=n/2 and |x|<=2/n; the text extraction loses fraction layout. The arcs are disjoint for n>2, and the inclusions hold. Since n>=4, the two-parabolic exception at n=2 never enters.

The centrality derivation and separating-twist proof on PDF 3 place the free group's gamma_d term in I(2d). With d=max(k,2), I(2d) is contained in I(k). The source proves a stronger containment than the submitted proof needs; there is no indexing mismatch.

### Whole stabilizer and the signed saddle lattice

Lemma 4.3, PDF 7, uses the additive span of signed saddle-connection holonomy vectors, not an assumed orientable homology plane on the original Torelli surface. Tile chart transitions have integral translation parts and derivative +/-I, so these vectors are integral. Continuing a horizontal or vertical edge from a singularity through regular corners cannot enter a disjoint regular cycle: directed continuation is injective and would give the first entered cycle edge two predecessors. Finiteness forces another singular endpoint. Nonzero horizontal and vertical saddle vectors give rank two.

Every affine map and its inverse permute saddle connections, hence preserve this same lattice exactly. For the orientation-preserving part, determinant one follows either from preservation of compact total area or from a positive lattice automorphism's determinant being a positive unit. Thus the *whole* affine derivative image lies in PSL(Lambda), isomorphic to PSL_2(Z), not just the group generated by the two twists.

This proves containment in a discrete arithmetic **ambient** group. No unsupported finite-index assertion about the twist subgroup or a Johnson term is needed. Containment alone should not be advertised as proving that an arbitrary subgroup is itself an arithmetic lattice.

Lemma 4.4(i) then uses the unique invariant Teichmüller disk: an ambient orientation-preserving conjugator between two of these affine pseudo-Anosovs must stabilize their common disk. The inspected Leininger stabilizer identification gives an affine representative, whose derivative lies in PSL(Lambda). Thus all ambient conjugators are accounted for. The finite kernel on the whole stabilizer does not enlarge the bound, because derivative faithfulness is required only on the selected free subgroup.

### Fixed rank-two subgroup and proper powers

Section 7 chooses a nontrivial nested commutator u_0 in fixed gamma_d(F_2) and its beta-conjugate v_0. Nontriviality follows from cyclic centralizers and zero abelianization. If they commuted, beta would normalize the maximal cyclic root group of u_0; equivalently beta^2 would centralize its root. Since beta is a free basis generator, its power's centralizer is <beta>. The zero abelianization of u_0 then gives the contradiction. The resulting pair is a free basis of a rank-two subgroup, by the standard free-subgroup and Hopficity facts.

Every nonidentity element of this fixed subgroup lies in the commutator subgroup of the two-parabolic free group. Its zero exponent sums exclude both cusp power-conjugacy families, so every such element has hyperbolic derivative and is pseudo-Anosov. This includes nonprimitive words and proper powers.

### Uniform tree fusion

Lemma 6.1 and Corollary 6.2 (PDF 8-9) are substantive ambient-fusion proofs. For a fixed finite generating set of G, let Y be the finite subtree spanned by a vertex and its generator images. The union of its G-translates is a connected invariant subtree T'. An infinite-order element has no vertex stabilizer, because all such stabilizers have bounded finite size; its minimizing axis lies in T', by nearest-point projection.

Fix a point x_0 on the axis of one ambient conjugacy representative g. If cgc^{-1} is in G, translate cx_0 by an element of G into Y. For each target vertex in Y there are at most s group elements sending x_0 there. Consequently one ambient class meets G in at most s|V(Y)| G-classes.

The modular Bass-Serre tree has vertex stabilizers of orders two and three, giving C=3|V(Y)|. This constant depends on the fixed subgroup and generating set, not on g's word length, its exponent, the trace value, or the later family size. The proof works for proper powers. No factor growing with translation length or with m is concealed.

For the orientation-preserving target, PSL(Lambda) fusion and Lemma 4.4(i) suffice: at least 2^m/C ambient classes survive. This check does not rely on the extra PGL/inversion estimates used for the stronger printed conclusion.

### Universal traces and normalization

The source's Lemma 5.2 is a reversal/substitution construction rather than a mere attribution to Horowitz. Its induction is universal in arbitrary X,Y in SL_2(C): reversal preserves trace; the two substitutions are related by reversal; and reversing the recursively constructed family permutes it. Nonconjugacy follows from cyclic sequences of y-gaps between x's: outer substitutions produce distinguishable patterns (1,0,k_i+2) and (0,1,k_i+2), which uniquely recover the earlier cyclic word. This proves the full arbitrary-m family, not only finite examples.

A projective representation of a free rank-two group lifts to SL_2(R) by choosing two generator lifts. The universal trace identity applies to these arbitrary lifts. Hyperbolicity gives |t|>2, and Leininger's normalization gives lambda+lambda^{-1}=|t|, hence lambda=(|t|+sqrt(t^2-4))/2. There is no missing square or factor two. Choosing m after the fixed subgroup and C proves the desired unbounded ambient multiplicity.

No source-author code or optional numerical demonstration was executed.

## Dates, current visibility and the permitted inference

The authenticated Zenodo record reports:

- publication date 2026-10-11, version 1.0;
- record created 2026-10-11T17:16:06.239749+00:00;
- record updated 2026-10-11T17:16:06.680413+00:00;
- current record status “published.”

The authenticated root GitHub responses report PR1241 created at 2026-10-11T06:34:11Z, and Git author/committer dates of 06:33:30Z for head 493a764dec034b7b645be76a284c4e6edc0583eb. The repository is public **at the API observation time**.

These observations do not authenticate historical repository visibility, the time the current bytes became public, original discovery order, or textual lineage. Git dates are not authenticated public-release timestamps. The fact that the PR-creation field is earlier than the Zenodo-creation field is not a priority verdict. Conversely, the note's currently recorded publication date does not by itself establish priority over the candidate.

The direct family's wording “public resolution ... before this October17 audit” should be read with that evidentiary qualification: an exact theorem is publicly accessible now, and the archival record reports an October11 creation/publication date; this supplement does not certify visibility at an earlier instant. No dependence, independence, earliest-result or misconduct conclusion is drawn.

## Citation and framing requirements

The known same-scope theorem must be cited in a new presentation. The bibliography should identify Ferudun, the exact title, unrefereed preprint/version/date, DOI, and Theorem 1.1. The introduction should state that this note presents a compact-core alternative proof of that recorded result. For example:

> The fixed-genus, fixed-depth unbounded-multiplicity theorem is recorded in Ferudun [Fer26, Theorem 1.1]. We give a proof using compact cores to control fusion of conjugacy classes in the ambient mapping class group.

The paper should retain the classical source credits needed by its own proof. A different fusion proof, or replacing the signed lattice/tree argument by compact-core geometry, does not justify describing the theorem's existence conclusion or the ambient-fusion mechanism as new. Neither a catalog's “open” label nor an unsuccessful search should appear as a current-openness premise. Chronology speculation is unnecessary to explain the mathematics.

The submitted preserved snapshot already disclaims novelty and firstness, so this is an updated citation/framing obligation for the new note, not a retrospective accusation about the snapshot. No new-note body was supplied to this supplement for line-by-line verification that these requirements have been implemented. Accordingly: mathematics/scope **PASS**; framing **PASS subject to the concrete citation and alternative-proof presentation above**, with implementation to be checked on the actual new note.

## Cross-check log and limits

- 2026-10-17T20:34:20Z: clock-verified start; authenticated both original seals and all 19 listed members. Completion estimate 10%.
- 2026-10-17T20:35:29Z: clock-verified main-proof checkpoint; PDF 1-9 text and critical displayed statements inspected, three-copy byte agreement and raw record/GitHub receipts checked. Completion estimate 80%.
- 2026-10-17T20:35:53Z: clock-verified conclusion; restricted main theorem passes, precise chronology limits and required paper framing fixed. Completion estimate 95%; authored supplement and final seal follow.

No new broad searches, unrelated records, other PRs, external communications, or external/Git mutations were undertaken. The original full-paper background proofs behind the named Teichmüller imports remain standard imports. This supplement validates the orientation-preserving theorem and its proof interfaces, not all stronger or optional claims in the 13-page source.


- 2026-10-17T20:37:07Z: clock-verified completion checkpoint. Both initial manifests and all19 members, plus every original permitted input receipt, still match. Source copies/checksums agree; all cross JSON parses. Assigned bounded supplement complete, estimate100%; only the explicitly listed new CROSS files are about to be sealed.
