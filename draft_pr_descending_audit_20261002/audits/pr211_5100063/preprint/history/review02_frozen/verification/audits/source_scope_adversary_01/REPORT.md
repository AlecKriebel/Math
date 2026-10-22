# Source-first adversarial audit — PR211 / 5100063 / k904,a

Audit date: 2026-10-15 UTC. Parent-supplied frozen head: `9d7b623203b525386da3d9d91548c79e7445a11c`. Native submitted artifact count independently checked: 19. Proof SHA256: `9640ed4bc6c6b0b56f0235c0e28513e9c3ca94c53cb75d2cb2eecee5b45b075e`.

## Disposition and strongest verified result

**The candidate matches the actual primary-source target and its nondegenerate confocal-ellipse domain. No source-object substitution or source-scope counterexample was found.** Stachel's cited canonical-coordinate theorem applies to that domain and to all coprime turning numbers in the chosen orientation. Real tangent intersections and original-focus inversions are well-defined; the proof/checkers use straight-edge signed areas of the correct outer vertices.

This is a source/scope disposition, **not a blanket mathematical PASS or publication authority**. I read the entire proof but did not independently certify its complete complex pole/divisor argument or every local identity; those are the other mathematical approach families' remit. No full historical-priority search was undertaken. The overall research/publication goal remains incomplete.

The most useful clarifications are:

1. The actual v11 row is k904,a, Table 10, printed p.12, with date **10/20**, odd N, and a question mark in the proof column. The imported report's 4–5/2020 dating and implication of an identical published table are inaccurate historical leads. The candidate's `SOURCES.md`, `WIP.md`, proof and current status correctly reject the published-table equivalence.
2. The published *Fifty New Invariants* companion genuinely omits the paired inversive area product: its actual Table 9 on printed p.350 contains only inverse-distance sums, inverse-distance-product sums, an inversive perimeter, and an angle sum. This conclusion is based on table contents, not only numbering or title.
3. The source table says odd N without explicitly imposing least period. The candidate states odd **least** period. This is readily reconciled by the repetition argument below; it is a wording/completeness clarification, not an identified obstruction.
4. `PUBLICATION_STATUS.md` says claimed_solved and records an earlier independent AI PASS, while `metadata.json` still says `complete_candidate_pending_independent_review` and `full_resolution_claimed=candidate_pending_review`, and the proof/README still say review pending. The status file explicitly calls the older pending text historical, so this is an artifact-level status mismatch rather than mathematical evidence. A later status reconciliation should identify which machine-readable record is current; this audit changes none of them.

## Independence and chronology

I began only with `source_record.json` and `prior_imported_report.json`, treating them as leads. I then verified the three supplied primary PDF hashes, read the relevant source sections, and inspected the critical rendered pages. `SOURCE_SCOPE.md` was frozen at **10:19:45 UTC**, before reading any candidate proof or inherited review. The entire `PROOF.md`, source/status/WIP metadata, and checker code were read only afterward. My direct source-geometry diagnostics were authored and run independently of the submitted checkers. The inherited `independent_review/INDEPENDENT_REVIEW.md` was read last, after my scope findings, own checks, and checker-code assessment; its PASS is not a premise of this report.

No other-shard chats or results were consulted. No person was contacted. No Git, index, ref, queue, database, provider, PR, tracker, paper, or deposit state was changed. All authored outputs are confined to this shard.

## Primary source verification

Read arXiv:2004.12497v11, 29 October 2020, introduction, Section 2, table-column conventions, Section 3.9 in full, Table 10 and nearby notes, plus Appendix A notation. Visually inspected printed pp.3 and 9–12. The introduction specifies a **confocal ellipse pair**; Section 2 specifies billiard axes a>b>0 and signed cross-product areas. Figure 1 fixes the outer polygon as the consecutive intersections of billiard tangents. Section 3.9 applies primed dagger notation to inversions of those outer vertices about the original foci and separately introduces the outer-locus foci and double-dagger notation. These definitions disambiguate k904,a from both k903,a and k906.

Read the journal companion's introduction, definitions, numbering table, Section 3.9 and actual Table 9; visually inspected printed p.350. Its absence of this product is a coverage fact only. It is not evidence that the conjecture has been proved, remains open today, or has no prior proof.

Read Stachel, *On the motion of billiards in ellipses*, European J. Math. 8 (2022), 1602–1622, introduction, canonical-coordinate construction and Theorem 4.3/equation (4.9); visually inspected printed p.1614. Its main domain is explicitly an ellipse caustic. All three PDF pins match the parent-supplied values, recorded in `SOURCE_SCOPE.md` and `INPUT_VERIFICATION.json`. PDFs, extracted source text and page images remain private and excluded from the authored manifest.

## Exact source target

Let E be x²/a²+y²/b²=1 with a>b>0 and f±=(±c,0), c²=a²−b². Let C be a strictly inner nondegenerate confocal ellipse, equivalently with squared axes a²−λ,b²−λ for 0<λ<b². For a fixed periodic Poncelet family and ordered billiard vertices P_i, let Q_i=T_(P_i)E ∩ T_(P_(i+1))E. Set

    W_(±,i) = f± + (Q_i−f±)/|Q_i−f±|²,
    S± = (1/2) Σ_i det(W_(±,i), W_(±,i+1)).

The source claim is constancy of S+S− along the odd-period family. Straight segments join consecutive W vertices. One does not invert entire edges to arcs, use unsigned union-region areas, replace Q_i by P_i, or replace f± by the outer-locus's own foci. The candidate and both submitted checker codes implement this exact Cartesian object. Subtracting the fixed focus from every inverted vertex in their area routines is legitimate: the extra terms telescope in a closed shoelace sum.

## Domain, winding, reversal, repetitions and boundaries

The source's explicit a>b>0 and confocal ellipse pair exclude circles and hyperbolic caustics. The ordinary regular billiard construction requires a strictly nested nondegenerate caustic; boundary, focal-segment and collapsed limits are not regular families covered here. A theorem restricted to this domain has not silently narrowed the actual primary source. The imported dataset's shorter phrase 'fixed confocal caustic' should be read with the primary source's ellipse-pair definition.

The source gives no explicit convexity restriction. The candidate expressly includes primitive star trajectories and therefore safely covers every admissible coprime odd winding number, rather than relying on the source's largely convex illustrations. Reversal negates each signed area and preserves their product. Cyclic reindexing preserves each area.

For a repeated odd N-cycle with least period n and repetition count r=N/n, both n and r are odd. The ordered outer vertices and inversions repeat r times, so S±^(N)=r S±^(n), and the product is r² S+^(n)S−^(n). Consequently the candidate's primitive odd theorem, if its universal proof is certified, extends immediately to this reading of the source's unrestricted odd N. Repetition never makes an even least period odd. The inherited reviewer independently mentions the same reduction, but the reduction here follows directly from the source's area definition.

Circle extension: for a circular billiard and concentric circular caustic, a fixed step angle gives a regular or star polygon that moves by rigid rotation. Its outer vertices and their central unit inversions also move by rigid rotation, so both signed areas are constant. This justifies the candidate's separate circle remark; its k>0 meromorphic proof need not cover k=0. No hyperbolic or degenerate extension is asserted here.

For real well-definedness, distinct parallel tangents to a central ellipse touch antipodal points. Their connecting diameter passes through the interior of the inner elliptical caustic and cannot be a tangent side. Thus regular consecutive billiard tangents intersect finitely. Their intersection is exterior to E, whereas the two original foci are strictly inside E; no original-focus inversion is undefined. This is a real-domain argument only and does not dispose of complex poles.

## Applicability of Stachel's actual theorem

Stachel Theorem 4.3 uses a caustic with axes (a_c,b_c), eccentricity modulus m=d/a_c, and canonical coordinate (−a_e sn u,b_e cn u). Its billiard step is 2Δu, with b_c=b_e cn(Δu), and its periodic formula is Δu=2τK/N with gcd(N,τ)=1 and a_e=a_c dn(Δu)/cn(Δu), b_e=b_c/cn(Δu). This is precisely candidate equation (2), with Stachel's modulus m renamed k and (a_c,b_c) renamed (alpha,beta). The numerical-library parameter is k².

There is no hidden restriction to winding one. Choosing the orientation with 0<τ<N/2 gives 0<v=2τK/N<K. Conversely, in any fixed nested confocal ellipse pair, beta/b is in (0,1), so the strictly decreasing real cn on (0,K) determines the relevant v uniquely. Confocality then gives the displayed major-axis relation. Closure forces the canonical shift to be 4Kτ/N, with coprimality exactly the least-period condition. Thus all source families in the stated regular domain have the required input. The use of Stachel is credited and does not assume this particular area-product conclusion.

## Independent finite checks and submitted-checker limits

`source_geometry_check.py` uses Stachel only to generate original billiard vertices. It then independently computes Cartesian line tangency to the original caustic, the reflection law, intersections of the actual billiard tangent lines, Euclidean inversions about f± derived from the original axes, and signed areas. It never uses the candidate's reduced edge expression, its pole locations, cyclic reflection or divisor argument.

Result: **10,530 finite assertions/diagnostics passed over 42 families**, with k=0.03,0.55,0.97; all coprime τ for N=3,5,7,9,11; three phases per family; alpha=1.37; 80-digit arithmetic and threshold 1e−60. Maximum scaled residual was 3.8384550079e−79. The checks include source caustic tangency, billiard reflection, finite outer intersections exterior to E, defined original-focus inversions, phase-product constancy, reversal, and threefold odd repetition. These are uncertified numerical diagnostics, not interval certificates or an all-N proof.

The default and bundled Python environments lacked mpmath. I reused the already installed mpmath 1.3.0 package from a preexisting local environment, with bytecode writing disabled; no package or external code was downloaded. Execution details and Python version are recorded in `INPUT_VERIFICATION.json`.

The author checker is self-writing, so I inspected it read-only rather than run it in the frozen input. Its numerical geometry really does intersect original billiard tangents and invert about the original foci. Its recorded 102,770 exact assertions consist of eight symbolic/Laurent controls plus eleven finite lattice assertions per 9,342 sampled coprime rotations. The independent checker similarly implements direct tangent geometry, source inversion and reversed order, with exact symbolic checks and finite lattice controls. Its reported 8,438 exact assertions and 5,412 numerical diagnostics are described as supporting the universal proof, not certifying it by enumeration. I did not rerun either submitted checker or independently certify all their algebra here. Their recorded counts are therefore inherited recorded results, clearly distinguished from my own 10,530 diagnostics.

## Remaining gaps and release limits

No source-scope blocker remains within this shard. A short explicit repetition corollary would make the candidate's least-period formulation fully transparent relative to the source's 'odd N'. The metadata/status mismatch and inaccurate imported historical dating should be preserved as provenance or clearly reconciled, rather than silently treated as current evidence.

The exact open mathematical gate for this audit program is independent completion of the local identity and complete meromorphic pole/divisor audits, including the N=3 critical fiber and quotient-lattice argument. This source audit does not supply that certification. A full priority/literature clearance is also not supplied, and absence of a row from the shorter journal companion proves nothing about later status. No neighboring PR theorem has been assumed.

Checkpoint: assigned source/scope audit **100% complete**; overall research/publication goal **incomplete and not estimated here**. Authored-only hashes and byte sizes are in `AUTHORED_MANIFEST.json`. Primary reading copies and renders are excluded.
