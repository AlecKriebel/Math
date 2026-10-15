# Independent source, reproduction, and geometry audit of PR 259 / 5100026

Frozen family findings: 2026-10-12T11:49:08.567841+00:00. Estimated family completion: 100% of this independent source/reproduction audit.

## Conclusion and exact scope

The submitted all-period proof supports the stated theorem for genuine least even periods N >= 4 in a strict nested confocal **elliptical** caustic, including primitive stars, using the original ellipse's fixed foci and the arithmetic mean of antipedal vertices. No fatal mathematical defect was found in that theorem. Real outer and antipedal intersections are finite; the centroid is independent of phase, on the original focal axis, negated on changing the focus, and zero for N=4. The two focal centroids being negatives does **not** say that either one lies opposite to its chosen focus.

The source-to-theorem qualification must remain explicit: neither the imported statement nor the k407 tables literally says “least” or “primitive.” They say even N. The source's genuine-polygon interpretation is supported by its discussion of opposite vertices of even N-periodics, while Stachel's parametrization explicitly requires gcd(N,tau)=1. If arbitrary repeated vertex lists are admitted, doubling an odd orbit yields an even-length list outside the theorem and does not restore invariance. This family supplies a reproducible numerical boundary control, not an exact algebraic certificate for that broader literal reading. Root is separately considering an exact certificate; no result from that family has been read or used here.

No novelty, priority, publication, or final project-status verdict is given.

## Independence and authenticated input

`INDEPENDENT_PLAN.md` was frozen at 11:37:36 UTC before reading proof, scripts, source gate, or historical/new review conclusions. During later pin authentication, historical verdict labels embedded in the review/publication manifests were incidentally visible. The historical narrative review and every other new audit-family conclusion remained unread. The mathematical analysis below was performed from the submitted proof, primary sources, scripts, and newly written controls.

All 26 files in parent `INTAKE.json` match independent byte counts, SHA-256, and reconstructed Git blob SHA-1. All file pins in FROZEN_MANIFEST, PUBLICATION_MANIFEST, and REVIEW_MANIFEST match. Reviewed-proof and reviewed-author-manifest body pins, every historical HASH_AND_REPLAY_RECEIPT file/body pin, and decoded BLOB-capture payloads also match. Every intake request stdout/stderr hash has a matching retained capture. See `AUTHENTICATION.json` and its reproducible driver `authenticate_and_replay.py`.

This audit binds to original submitted/current PR head `0524ed734ee8185681d030af98088259134a6af7`; it does not authenticate any later changes. There were no Git, index, ref, provider, queue, shared-log, or submitted-file mutations.

The imported input is record 5100026 / AMR-050-0026 in `ulamai/UnsolvedMath` revision `37e53eabe540fb458758e198be61634bd02ee008`. The local complete `problems.json` is 68,931,837 bytes with SHA-256 `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`. The pinned remote resolver independently returned the same `x-repo-commit`, `x-linked-size`, and `x-linked-etag`. The exact imported statement hash is `c5d8b6bb6353994b902f5c9db0db51eb15630aba13def49b1507f9a2ca9594b6`, matching the catalog. The source path/revision gap left by the author's terse source manifest is thus filled in this audit's reading evidence. No database was copied into a publication artifact.

All three source PDFs downloaded independently match the author's full SHA-256 pins:

| Source | Bytes | SHA-256 |
|---|---:|---|
| arXiv 2004.12497v11 | 3,389,610 | c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da |
| final Reznik–Garcia–Koiller | 1,836,579 | c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42 |
| Stachel published paper | 726,042 | 9121028d7295435740cebb25ec60abe1a0dcc4e96686c226b1b6533bd49515d8 |

The Stachel publisher download and TU Wien repository copy have identical bytes. Full imported/source reading material, derived text, rendered source pages, and transport headers remain in `reading_private/`, explicitly excluded from publication. `SOURCE_PINS.json` and `record_source_pins.py` preserve the check.

## Source alignment

The [v11 paper](https://arxiv.org/pdf/2004.12497v11) is titled *Eighty New Invariants in the Elliptic Billiard*. Its p7 Table 5 visibly assigns k407 to the primed-star vertex centroid, even N, and M=f1 or f2. Section 3.5 separates vertex and signed area centroids and assigns primes to the outer polygon. The preliminary focus definitions concern the original billiard ellipse; the geometry is a confocal ellipse pair. Figure 3 confirms the tangent outer polygon and original foci. The paper's later statement that opposite vertices of an even N-periodic reflect through the origin supports the genuine-period convention, but is not an explicit definition excluding repeated lists.

The [final paper](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, printed pp347–348, has the same definition and k407 row. I visually inspected both complete pages and v11 p7, rather than relying on extracted superscript order. The row requests the arithmetic vertex centroid; k406 has separate area-centroid content. Source wording about rays is interpreted as their perpendicular supporting lines, consistent with the figure and imported record. Neither edition supplies an all-period value formula for k407. Neither edition literally uses least/primitive in this row.

The packet includes `SOURCE_TITLE_CORRECTION.md`, preserving and correcting the frozen SOURCES item's mistaken use of *Fifty* for v11. The v11 PDF title itself omits “N-Periodics”; the exact bibliographic form above is safest. This naming issue does not affect the k407 mapping or geometry.

[Stachel's published paper](https://link.springer.com/article/10.1007/s40879-021-00524-2), visually inspected at printed p1614, Theorem 4.3 and (4.9), supplies exactly the parametrization used: caustic eccentricity as Jacobi modulus, canonical step twice the auxiliary shift, auxiliary shift 2 tau K/N, gcd(N,tau)=1, and the stated dn/cn and 1/cn semiaxis formulas. Restricting the shift to (0,K) selects the orientation representative; reversal covers the complementary orientation. This is a credited input, not a new result in the packet.

[DLMF 22.4](https://dlmf.nist.gov/22.4) independently confirms the period/pole/zero tables and the three half-period signs used in the proof, including dn's real period 2K. [DLMF 22.8](https://dlmf.nist.gov/22.8) confirms the addition formulas. These consulted web references were not represented as frozen PDFs.

## Exact replays and environment

Every program was copied unchanged into its own scratch directory. Each ran without modifying any submitted file or frozen receipt. Raw stdout, stderr, command, timestamp, duration, source hash, runtime path, and expected/output hashes are retained in `replays/` and `REPLAY_RECEIPTS.json`. No normalization, rounding, or output editing was performed.

| Unmodified program | Mode | Assertions/diagnostics | Result | Frozen output |
|---|---|---:|---|---|
| verify_exact.py | exact algebra and finite indices | 40,797 | exit 0 | byte-identical |
| verify_numeric.py | 110-digit non-interval geometry | 47,931, 93 primitive families | exit 0 | byte-identical |
| independent_review/independent_exact.py | exact homogeneous/rational geometry | 12,906 | exit 0 | byte-identical |
| independent_review/independent_numeric.py | 125-digit non-interval geometry | 4,083, 18 primitive families | exit 0 | byte-identical |

Runtime: bundled Python 3.12.14, SymPy 1.14.0, mpmath 1.3.0. Only the vendored library directory from a prior case was added to PYTHONPATH; no earlier review helper implementation was imported. Default Homebrew Python 3.14.6 and default bundled Python 3.12.14 both fail to import SymPy; these failures and full traces are preserved in `SOURCE_PINS.json`. A plain default-python replay is therefore not self-contained. Reproduction is successful with the explicitly recorded dependencies. `RUNTIME.json` records paths and versions.

## Whole-proof audit and checker coverage

I inspected every section of PROOF.md and every assertion in the four programs.

1. **Domain and canonical data.** Scaling the caustic major semiaxis to one preserves the Euclidean statement. For 0<k<1 and 0<v<K, a=d/c>1, b=k'/c>k', and a²-b²=k². Stachel gives the complete elliptic-caustic orbit mechanism. Least even N makes tau odd, so shifting N/2 vertices adds an odd multiple of 2K. The claimed antipodal pairing follows. The finite integer tests corroborate this arithmetic; the all-N argument is gcd arithmetic, not enumeration.
2. **Actual outer geometry.** Substituting the derived R(u) into the two original tangent equations verifies both incidences. It does not quietly construct a new confocal billiard from the outer locus. The normal-line equation through R is (R-M)·(U-M)=(R-M)·(R-M), equivalent to (R-M)·(U-R)=0. The exact checker verifies the tangent and determinant identities algebraically under the Jacobi square relations. Its numerator reductions cannot establish denominator nonvanishing; that comes from the proof's separate real-domain inequalities.
3. **Real finiteness.** For the positive original focus, the determinant factors as 2Bsd D(a+k sn u)/D0. All factors are positive for real u, with D0>0 and a-k>0. The negative focus follows centrally. Original tangent intersection determinants are nonzero on the same strict domain. Hence real construction and arithmetic denominator N are valid throughout the family, including stars. This does not extend to degenerate/hyperbolic caustics or diameter two-orbits.
4. **Complex singularities.** On the common 4K,4iK' torus, the only determinant-zero/pole mechanisms are the four listed classes. At simple dn zeros the endpoints coincide and the Cramer numerators vanish. At midpoint Jacobi poles the endpoints are regular and the determinant has a nonzero finite limit. At a+k sn u=0, the shared original tangent passes through the original focus with isotropic normal; both quadratic right sides vanish. That zero is simple and separate from an endpoint pole except when sn²v=1/(1+k'), precisely v=K/2. Under gcd(N,tau)=1 this is only N=4. The endpoint-pole cases have at most simple poles after Cramer's rule. The classification is sufficient to exhaust the meromorphic determinant; the programs only sample corroborating complex neighborhoods and cannot by themselves certify exhaustion.
5. **All-period cyclic cancellation.** A real step orbit meets exactly two pole slots, j and j+N/2. The pole-reflection identity gives neighbors Q and -Q. The leading equations independently determine a residue by L·V=L·L and (Q-M)·V=0. With the opposite leading vector -L, the four incident residues cancel by the two elementary pair identities. Four edges are distinct for N>=6, and there are no higher-order Laurent terms from the local classification. Holomorphicity on the compact torus then proves both coordinates constant. The supplied exact programs verify general residue algebra but do not prove the analytic assumptions; those are present in the argument.
6. **Symmetry and N=4.** Reflection in the focal axis maps the family to reversed cyclic order, so a phase-independent centroid has zero transverse coordinate. Central reflection changes M to -M and negates the centroid. For v=K/2 the outer locus is a circle and four antipodal vertices form a rectangle. The original ellipse support relation h²-m²=l²-n²=b² makes the explicitly computed rectangle centroid zero. The generic rectangle identity is exact; the independent reviewer script additionally verifies genuine rational ellipse contacts and reflection, so it is not merely an arbitrary rectangle substituted for an orbit. The separate circle argument is valid by opposite pairing and independent consecutive real normals.

The strongest verified proof result is the complete scoped theorem above. No unsupported equivalent theorem is substituted for the phase-invariance step. The main analytic work is the singularity classification plus four-edge residue cancellation; the finite checkers are labeled consistently as corroboration.

## Newly written independent dynamics and falsifiable controls

`direct_reflection_controls.py` constructs original vertices independently from Euclidean caustic tangency and specular reflection. Jacobi functions select only the known closed-family ellipse axes. A starting point is chosen by ordinary ellipse angle; a tangent point on the caustic is solved trigonometrically; each next bounce comes from the second intersection of its ray with the original ellipse; its direction is then reflected in the ellipse normal. Outer and antipedal vertices are independently solved by mpmath LU. No submitted code or former audit helper is imported.

At 180 digits, 1,649 assertions pass over 10 primitive families and three ordinary starting angles each. Cases include N=4,6,8,10,14,18,30, multiple stars, k=10^-15, and k=1-10^-15. Segment discriminants independently confirm tangency to the fixed caustic; closure, winding, and distinct vertices confirm the intended least periods. All real antipedal determinants are nonzero in samples. The worst normalized phase discrepancy is 6.88e-172 and worst normalized closure error 9.93e-172. The extreme k=1-10^-15 example has a sampled determinant as small as about 1.10e-7, so a fixed double-precision threshold would be inappropriate. These are high-precision diagnostics, **not interval certificates**.

The controls quantify distinct wrong claims:

| Control | Parameters | Euclidean phase gap |
|---|---|---:|
| use outer-locus own focus | k=.63, genuine N=6, tau=1 | 0.0001020311366648138488 |
| replace vertex centroid by area centroid | same family | 0.0029568767946750728893 |
| duplicate an odd orbit into an even-length list | k=.63, least N=3, tau=1, repeated list length 6 | 0.7760997829639318802 |

The repeated odd list preserves its odd orbit's arithmetic mean exactly as an algebraic property of repetition; the diagnostic checks the equality and shows the underlying mean changes with phase. The independent circle model also gives zero.

My original plan included an unnecessarily stronger hypothesis that the positive-focus centroid points to the negative half-axis for every N>4. That hypothesis is falsified by stars: k=.63, least N=8, tau=3 gives x approximately +1.780146638544216. The supplied proof never claims that sign; its focus-negation claim passes. This correction is retained as an audit decision rather than silently removing the stronger hypothesis.

## Remaining gap and handoff

For the submitted strict elliptic, original-focus, arithmetic-centroid, genuine even-period theorem: no mathematical gap was identified by this family. For an unrestricted literal statement admitting arbitrary even-length repeated odd lists: the proof does not cover it, and the numerical control rejects it; retain an explicit least-period/source-convention qualification. Source priority and novelty have deliberately not been audited. Default environment dependencies and non-interval numerical diagnostics are the main reproducibility limitations.

Private reading copies must not be included in any public packet. This family has made no publication or outside-individual communication. Final manifest hashes all checkable family artifacts and separately lists excluded private reading evidence.
