# Edition notice for the source audit

The authored source analysis below is preserved from the independent audit of 9 October 2026. Its mathematical comparisons and limitations are unchanged. Only the original report fingerprint and inventory wording have been edited to match this proof-only edition. Public scholarly URLs, raw public PDF sizes and historical verification results remain; source PDFs, extracted text, local source paths and derived-source-text hashes are excluded.

This is a historical source-reading record. Edition preparation did not reretrieve or rehash the sources and does not make a new present-day literature-status claim. The original problem remains unresolved after approach 1.

---

# Independent source audit of Approach 1

Audit date: 2026-10-09 UTC.

Scope: source support and category/topology distinctions in `APPROACH1.md`, not a new construction or a literature-wide status determination.

## Verdict

**Pass.** The report accurately distinguishes continuously chosen topological extensions, homotopy density of PL embeddings, and local contractibility of fixed homeomorphism groups from a continuously chosen, exactly boundary-preserving PL extension. None of the checked statements closes its remaining moving-boundary gap. No source-driven correction to its unresolved conclusion is needed.

One optional clarification would improve completeness: Yagasaki also states genuinely PL-valued local extension results in Fact 4.2(3)-(4), but their input boundary maps take values in the **fixed** ambient boundary. They do not allow the image curve to move freely in the plane.

## Primary problem and topology

- [OWR 30/2020, Problem 14](https://ems.press/content/serial-article-files/46867), printed p. 1523 / PDF p. 55, asks for an assignment extending each injective PL map of a fixed triangle boundary to an injective PL map of the whole triangle, continuously in the boundary map. It separately notes individual extension existence.
- [Rote's public problem list](https://page.mi.fu-berlin.de/rote/Kram/Problems-Discrete-Geometry-2020.pdf), p. 4, gives the same statement. Both pages were checked in extracted text and visually.
- Neither statement explicitly defines a mapping-space topology. The report therefore correctly identifies uniform/compact-open topology as its chosen interpretation, rather than attributing a missing hypothesis to the problem statement. Uniform and compact-open topologies agree here because the domains are compact and the codomain is Euclidean. The uniform topology retains the prescribed boundary parameterization; it is not the quotient topology on unparameterized curves.
- The statements impose no fixed subdivision or bound on its size. The report's unrestricted finite-PL formulation respects this.

## Yagasaki (2000)

[Spaces of embeddings of compact polyhedra into 2-manifolds](https://arxiv.org/pdf/math/0010222), Theorems 1.1 and 1.2, the extension proof in Section 3, and Section 4 through Lemma 4.4 were checked in the full local preprint. The relevant formulas on pp. 10-12 were also checked visually.

1. Theorem 1.1 uses compact-open embedding spaces and takes values in a topological homeomorphism group. PL structures on the source/target do not change that codomain to its PL subgroup. The construction in Section 3 uses the earlier topological/conformal extension operators; its principal-bundle corollaries are likewise topological.
2. Theorem 1.2 describes the triple of topological, Lipschitz, and PL embedding spaces as an `(s, Sigma, sigma)`-manifold. It contains no compatibility statement with the restriction map from triangle embeddings to boundary embeddings.
3. Lemma 4.4 gives ANR and homotopy-density statements. In the notation `E_K(X,M)`, the maps equal the identity on one fixed subpolyhedron `K`. Its absorbing homotopy changes a general input embedding away from that fixed set. It does not supply a homotopy that preserves the whole varying trace of each extension on `partial T`.
4. Fact 4.2(4), an adjacent statement worth mentioning, has inputs in `E_PL(Y, partial M)`, with `Y` a fixed compact subpolyhedron of `partial M`, and outputs in `H_PL(M)` agreeing with those inputs on `Y`. For `M=T`, it extends reparameterizations into the fixed boundary `partial T`; it does not handle a nearby polygonal curve that leaves `partial T`. Changing `M` separately for every curve would require the missing parameter-dependent identification. Fact 4.2(3) has the same fixed-boundary restriction.

Thus the report does not overlook a stated PL selector for freely moving plane curves. The relevant distinction is fixed image boundary versus moving image boundary, in addition to topological versus PL output.

## Gauld (1976)

[Local contractibility of spaces of homeomorphisms](https://www.numdam.org/item/CM_1976__32_1_3_0/), printed pp. 3-11, was checked throughout, with the theorem on p. 3 and warning on p. 11 checked visually because extraction omits formulas.

Theorem (1) contracts a neighborhood of the identity in the self-homeomorphism group of a fixed finite polyhedron. It preserves PL input, and the endpoint of this particular contraction is the PL identity. The relative statements on p. 10 are also for fixed subsets or pairs. They do not construct an extension from arbitrarily varying prescribed boundary data.

The warning on p. 11 concerns the separate, localized Siebenmann-style construction, whose limiting embedding need not be PL. It does not contradict PL preservation of the main contraction. The report accurately keeps these two claims separate and uses the warning only to reject an unproved inference from PL intermediate stages to a PL limit.

## Dobbins (2021)

[Grassmannians and pseudosphere arrangements](https://jep.centre-mersenne.org/articles/10.5802/jep.171/), Theorem 3.1.7 and its explanation on printed pp. 1243-1244, give uniform convergence of conformal disk parameterizations normalized at three boundary points when the curves converge in Frechet distance and those points converge. This does not prescribe an arbitrary full boundary parameterization, and it does not assert finite PL output. The report's description is accurate. Uniform convergence of parameterized boundary maps is strong enough for the associated curve convergence, but that observation does not add the absent PL or exact-trace assertion.

## Verification record

The original source audit found that all five source PDFs exactly matched both byte count and SHA-256 recorded in the source manifest. These public PDF identities are retained in the sanitized `SOURCE_MANIFEST.json`:

| Source | Bytes | SHA-256 match |
|---|---:|---|
| OWR 30/2020 | 1,132,713 | Yes |
| Rote problem list | 198,165 | Yes |
| Yagasaki 2000 | 195,082 | Yes |
| Gauld 1976 | 711,749 | Yes |
| Dobbins 2021 | 1,215,501 | Yes |

No source was redownloaded, and no claim is made about later literature not covered by these documents. This audit did not alter the report, queue, or source files and did not publish anything.
