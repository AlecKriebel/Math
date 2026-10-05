# Source-only claim and independent falsification plan

Freeze UTC: 2026-10-04T23:02:15.189587+00:00

Complete extracted contents read: arxiv_v11.txt lines 1–814 and published_021_0174.txt lines 1–739. Native source PDFs and abstract page are retained with capture metadata. No candidate documents, candidate scripts, inherited reviews or numerical results have yet been accessed.

## Primary-source correspondence

- Reznik, Garcia, Koiller, arXiv:2004.12497v11 (29 October 2020), *Eighty New Invariants in the Elliptic Billiard*, pp. 1–4 definitions/context, §§3.3–3.4 pp. 4/6 pedal definitions, §3.7 pp.7–8, Table 7 p.9, §4 p.13 experimental family constancy, Appendix A p.15.
- Reznik, Garcia, Koiller, *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, Arnold Mathematical Journal 7 (2021), 341–355, DOI 10.1007/s40598-021-00174-y, pp.341–344 definitions/context, §§3.3–3.4 pp.344/346 pedal definitions, §3.7 and Table 7 p.349, §4 pp.351–353, Appendix pp.353–354.
- The literal area-ratio equality row is arXiv k606 but journal k607. In arXiv, k607 is instead an antipedal focal area ratio for N divisible by 4. Journal k606 is a product of outer focal pedal areas for odd N. These identifiers cannot be interchanged without edition qualifiers.

## Geometric setting and exact hypotheses

The source EB is a pair of confocal ellipses, outer ellipse x²/a²+y²/b²=1 with a>b>0, inner elliptic caustic with positive semiaxes and the same foci f1,f2=(±sqrt(a²−b²),0). For each permitted N-periodic closed billiard trajectory P_i (i mod N), let P' be the outer/tangential polygon whose side lines are the outer-ellipse tangents at P_i. Let Q_{j,i} be the perpendicular foot from f_j to orbit side P_iP_{i+1}, and Q'_{j,i} the foot to the corresponding tangent side of P'. All areas are signed shoelace sums in cyclic order, not sums of unsigned regions.

The primary target is the Table 7 display

    A1/A2 = A1'/A2',  all N, value unknown, proof unknown.

Here the barred quantities in arXiv and unbarred quantities in the journal mean the same focal pedal areas. “All N” should be read for the paper's defined confocal-ellipse periodic families and where the ratios exist. The paper does not provide a minimum N or a nonzero-denominator lemma in this row; N=2 and collapsed caustics may require formulation care if one tries to include them. No hyperbolic caustic, circular outer billiard (a=b), focal separatrix or degenerate limiting caustic is included by the literal initial geometric hypotheses. Their possible extension must be labeled as extra work, not an original mandatory case.

## What is actually asked: two distinguishable layers

E: For every allowed member of every allowed N-family, the displayed two ratios are equal whenever denominators are nonzero.

C: For a fixed allowed family (ellipse and caustic fixed), those equal ratio values are independent of phase.

E is unambiguous in the display. C is strongly implied by the global interpretation of every table entry as a conserved quantity, arXiv p.2's explicit selection criterion of constancy over the moving family, and both editions' Table 1 discussion and §4 numerical method. It is not separately written as an equation in the row. Therefore a proof of E alone cannot be called proof of the whole source invariant without testing C; if C fails, report that the source's constancy framing needs correction while E can remain valid.

The journal's end of §3.7 additionally anticipates analogous antipedal ratio/product invariants but says they were not checked. That is not a replacement statement of the focal *pedal* equality. Neither source has a concluding mathematical section revising the target; the final substantive section is the experimental method and video list.

## Independent analysis and controls before candidate access

1. Attempt an exact N=3 phase comparison, using symmetric triangle orientations on a major-axis endpoint and a minor-axis endpoint of the same a=2,b=1 ellipse. Establish reflection law and common elliptic caustic before comparing focal pedal signed areas. If C varies while E survives, freeze an exact counterexample to constancy.
2. Use direct feet q=f−((f−p)·n)n with unit normal n to every line; compute signed shoelace areas. Construct outer feet from outer-ellipse tangents rather than relying on any candidate indexing.
3. Independently derive a relation between orbit and outer pedal feet by reflecting a focus across incident billiard lines. Seek a uniform similarity or common area scaling, checking that the cyclic index is consistent for both foci. Do not assume E in the derivation.
4. Check orientation reversal, cyclic relabeling, focus swap, and even-period central symmetry. Check zero denominators and cross-multiplied extension separately from ratios.
5. A real conic boundary audit will distinguish literal ellipse-pair scope from broader physically valid ellipse-billiard hyperbolic trajectories. Any lack of the latter cannot by itself falsify literal source fidelity.
6. Only after recording independent analysis/control outcomes read every submitted candidate document and implementation, then compare strongest proved statement separately against E and C. Do not accept inherited verdicts as evidence.

Progress estimate: 25% of this source-fidelity audit, not percentage toward solving the mathematical problem.
