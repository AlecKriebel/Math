# Independent classical priority audit: PR967 / problem 2616

Submitted HEAD: `b356dec5cb01e5f536b9cfeece56ad08844c03cb`.
Family: `priority_classical_01`. Scope: classical mathematical priority only.

## Result

**Priority is not cleared. A complete classical specialization has been verified, with no mathematical gap in the deduction.** The exact submitted example is a direct consequence of the standard Mathias Boolean group topology together with Talagrand's finite-block filter criterion and the published finite-to-one lifting lemma in Medini, Repovš and Zdomskyy (2015), Section 3, Lemma 8. The full deduction, including countable resolvability and the exact quantifiers, is in `MATHEMATICAL_SPECIALIZATION.md`.

This finding is stronger than a search match or a result merely asserting non-H-separability. It supplies the exact countable Hausdorff group and the failure of every disjoint finite-block sequence from earlier source theorems. Under the protocol's criterion admitting a fully justified specialization of earlier theorems, this is a qualifying classical antecedent and prevents a novelty clearance. It does **not** establish that the cited authors explicitly announced a solution to Kourovka 15.80/21.107 or printed this particular combined corollary. I found no single earlier source inspected here that states the entire exact group counterexample in that language. The historical fact of an earlier explicit combined presentation remains distinct from the mathematically verified classical derivation.

A conservative date bound for all ingredients in that derivation is **14 December 2016**: Sipacheva's arXiv v1 explicitly provides the topology; Medini et al. v1 was submitted on **1 August 2015**; Talagrand's original theorem appeared in **1980**. Nothing in the deduction uses a selective, Ramsey, rapid, or P-point ultrafilter, or any hypothesis beyond ZFC. This is not a certificate of earliest priority.

## What was checked

The claim is interpreted with nonempty open sets and thresholds depending on the open set. Blocks need not cover the group. The exact obstruction is existence of a groupable dense subset (equivalently, for a countable space, groupability of the whole underlying space after distributing any leftover points into the blocks). It is not general failure of a varying-dense-set selection principle.

The decisive source theorem is not about free Boolean groups: a nonmeager filter remains nonmeager when pulled back, as a generated filter, along a finite-to-one map. Apply it to `max : [omega]^{<omega} \ {empty} -> omega`. The pulled-back filter is contained in the punctured neighborhood filter of the Mathias group. Thus that neighborhood filter is nonmeager. Talagrand's theorem excludes exactly the proposed finite blocks. The inclusion direction was checked explicitly; the large inverse-image fibers are not being confused with the smaller subgroups `[A]^{<omega}`.

I rendered and read the original Talagrand Theorem 21 and its proof at printed pp. 28–29 (PDF page 9). The theorem itself allows disjoint finite sets without demanding they cover the underlying set. The 2015 lifting lemma applies to arbitrary nonmeager free filters on countably infinite sets in the surjective case used here. Its proof, left to the reader in that source, has been independently reconstructed here. An adversarial check found that the unrestricted printed formulation needs a proper-pullback/range qualification; max is explicitly surjective, so this boundary does not affect the exact deduction.

## Other serious leads

- **Predecessor 15.80:** its box-product example is uncountable. The Zelenyuk Corollary 12.21 citation supplies absolute countable resolvability for other abelian groups; it does not itself provide a countable topology with the block obstruction. The route is not dismissed because the submitted group is Boolean. In fact infinite countable precompact groups admit expansive blocks, so absolute resolvability alone cannot establish the desired failure. The full 2011 book remained inaccessible; this is a live bibliographic coverage gap, not evidence against an antecedent elsewhere in it.
- **Soukup–Soukup–Spadaro 2012:** their very strong HFC example has no groupable dense subset, but is a space in a Cohen extension. Its group hull in the ambient Cantor cube is precompact and therefore has expansive blocks. The source does not give the required group counterexample through that transport.
- **Bella–Bonanzinga–Matveev 2009, Proposition 75:** H-separability implies groupability for an omega-resolvable dense countable subspace. This is the positive direction, with a stronger selection hypothesis. Its contrapositive does not turn an arbitrary non-H-separable group into the target counterexample.
- **Weak Fréchet, K-space and ultrafilter-space examples:** an obstruction for a particular nondense set of generators does not exclude finite blocks chosen from the entire group. Wang–He's countable free group example fails K-space on the embedded ultrafilter subspace; the missing implication to the present constant-space obstruction is explicit.
- **Protasov 2009 ultrafilter topologies:** the theorem concerns strongest left-invariant topologies. Joint continuity of multiplication and continuity of inversion are not supplied by that hypothesis. Maximal-space constructions also fail the dense-partition hypothesis. Neither is counted as an exact topological-group counterexample.

`LEAD_ADJUDICATION.md` records the mechanisms and exact remaining gaps, including a newly found 1999 monograph lead whose contents were not accessible.

## Coverage limits and release boundary

This was a substantial but bounded classical audit: searches used exact wording, groupability, H/GN selection, weak Fréchet and K-space language, Mathias/free Boolean topology, meager/feeble filters, Talagrand and finite-to-one maps, and Protasov/Zelenyuk references. Search absence has no firstness implication. The complete older Nyikos 1992 paper, the 1999 Protasov–Zelenyuk monograph and the full Zelenyuk 2011 book were not obtained. New official status and recent solution repositories are assigned to a separate family and were not imported here. I did not read that family's conclusions.

No acceptance, merge, publication, release, installation, Git/index/ref/config mutation, communication with people, or outreach draft occurred. All fetched primary bodies, extracts and renders are excluded from the public seal under `private_primary/`. Only authored findings, source metadata, query/access receipts and the seal checker are included. This report is not an entire-package clean review.
