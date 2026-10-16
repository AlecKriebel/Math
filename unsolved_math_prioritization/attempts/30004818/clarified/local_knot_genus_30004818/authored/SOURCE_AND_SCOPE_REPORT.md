# Source and scope report: local-knot genus in orientable three-manifolds

Checked 7 October 2026. Problem 30004818, OWR-8415345-008. This report is source verification, not an author turn. The source check supports continuing proof work; it does not establish a resolution.

## Exact target

Ruppik's contribution to Oberwolfach Report 42/2021, pp. 2358–2360, asks whether the orientable analogue of the displayed nonorientable genus-saving example exists. The contribution explicitly stays in the smooth category. The relevant genus is the minimum genus of a compact connected orientable surface with one boundary component K, smoothly properly embedded in M×[0,1], with K local in M×{0}. It is not the Seifert genus, nonorientable genus, PL genus, or genus in an arbitrary four-manifold filling. Taking the unknot at the other end and capping it gives the same bounding-genus formulation. The example uses the sum of two same-handed trefoils: genus at most one in a nonorientable product versus classical genus two.

Source: https://doi.org/10.4171/owr/2021/42 ; publisher PDF https://ems.press/content/serial-article-files/46920 .

## Closed versus open manifolds

The short OWR question itself says an orientable three-manifold, without an explicit closedness qualifier. Celoria adopts closed, connected, oriented three-manifolds as a convention, while saying those restrictions are not essential. The collar discussion in Klug–Ruppik concerns compact manifold boundaries. We should not silently attribute Celoria's convention to the OWR question.

For the existential target this distinction is harmless, for a separate elementary reason. If a compact surface supplies a counterexample in the product of any smooth orientable three-manifold, choose a compact connected codimension-zero submanifold N of its interior containing both its projection and the local knot ball. Doubling N gives a closed connected oriented three-manifold D(N). The same surface lies in D(N)×I, so g_{D(N)×I}(K)≤g(F)<g_4(K). Thus it suffices to seek closed examples. This is an authored compactness reduction, not a quotation from a source. If an ambient manifold has boundary, properness with sole boundary K in its interior boundary-level ensures the surface avoids the side boundary; otherwise that altered relative problem must be specified separately.

## Baseline and lifting caveat

Klug–Ruppik §2 defines the precise bounding genus. Its discussion following Proposition 2.2 explicitly warns that the universal-cover proof for disks works for a higher-genus surface only when the surface's induced fundamental-group map is trivial. It records equality for local knots in connected sums of S¹×S², and for three-manifolds smoothly embedded in S⁴. Any strict example has g_4(K)≥2. Their compact-four-manifold sliceness statements must not be mistaken for higher-genus product statements.

Source: https://arxiv.org/abs/2009.03053 .

Boden–Nagel gives the smooth universal-cover compression result for a punctured closed oriented three-manifold, and uses contractibility of the slicing disk. The accessible arXiv manuscript numbers the general compression lemma 2.10; the later literature cites 2.11. The lemma, not a blanket higher-genus lifting assertion, is the usable input.

Source: https://arxiv.org/abs/1606.06404 ; https://doi.org/10.1090/proc/13667 .

## Celoria's role

Celoria's Definition 12 distinguishes genera in fillings from cobordism genera in Y×I, and distinguishes smooth, locally flat, and PL categories. For null-homologous knots, the standard comparison knot can be the unknot. Local knots are a special subclass of null-homologous knots; these notions cannot be exchanged. Celoria provides background, not a positive-genus resolution of this OWR question.

Source: https://doi.org/10.1112/topo.12051 ; https://arxiv.org/abs/1602.05476 (v4, 10 January 2018).

## Directly relevant 2026 result

Park–Wu–Yang, arXiv:2603.18619v1, submitted 19 March 2026, states the full local-knot question as open. Theorem 1.1 proves equality for a ν⁺-sharp classical knot in any rational homology three-sphere. Here ν⁺-sharp means max{ν⁺(K),ν⁺(−K)}=g_4(K). Although the paper uses a rational-slice-genus framework, it explicitly identifies that genus with the usual compact connected oriented bounding-surface genus for a local, hence null-homologous, knot. This is a genuine partial obstruction for our target, not a different rational quantity. Its hypotheses do not cover every classical knot or every orientable three-manifold.

Source: https://arxiv.org/abs/2603.18619 ; https://arxiv.org/html/2603.18619v1 . No later version or general resolution was identified in the bounded searches made for this check.

## Adjacent 2025 construction is not a solution

McDonald–Miller, arXiv:2511.15900v1, constructs genus-saving surfaces in punctured Spin(L(3,1)) and punctured T⁴. Their input is a tangle cobordism involving a generally nonlocal knot in a three-manifold, followed by a spinning/filling construction. The output is in a four-manifold filling, not a collar M×I. Their Proposition 2.12 also explains a cover-based obstruction when the surface's fundamental-group image in T⁴ has non-full rank. These constructions may inform later attempts but supply neither the required product surface nor an orientable local-knot counterexample.

Source: https://arxiv.org/abs/2511.15900 ; https://arxiv.org/html/2511.15900v1 .

The publicly listed Friedl–Kalelkar–Quintanilha–Shah project concerns Gordian distance/unknotting, not the same genus target. It was listed as in preparation on an author's public research page when checked; no private draft was sought or used.

Source: https://tanushreeshah.wordpress.com/research-mission/ .

## Status discipline

The retrieved sources support the statement that the full question remains unresolved in the checked primary literature, most explicitly in March 2026. Search non-detection is not proof that no later solution exists. This source report was prepared after the first substantive author approach. The later AUTHOR_COMPLETION_REPORT.md and AUTHORED_MANIFEST.json record five completed author approaches; the source check, normalization, and mathematical review do not add author turns. Approach 1 is in APPROACH_01_FINITE_IMAGE_COVERING.md. Raw downloaded papers are retained separately and are not publication material.
