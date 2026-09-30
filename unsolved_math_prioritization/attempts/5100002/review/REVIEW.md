# Independent adversarial review: 5100002 / k108

**Verdict: PASS_COMPLETE_COUNTEREXAMPLE_TO_PRINTED_K108. No mandatory mathematical correction.**

The submitted pair of convex primitive six-period orbits disproves the exact quotient and period condition printed in both the original and published source tables. This is a complete answer to that literal target. It does not establish a corrected invariant for any period class, an official erratum, historical priority, or human peer review.

Reviewed mathematical snapshot: SHA-256 **5553f899b1098a321fe2164c3ba0d6eed87bc2424dc8021dee50e01fc14dc4ab**.

The review independently checked the source images and geometry, replayed all **291** submitted assertions byte for byte, and passed **272** additional exact assertions using only rational arithmetic in scaled coordinates. The independent code does not import the submitted checker.

## 1. Source question and conventions

I inspected the full available primary PDFs, with particular attention to the introduction, preliminary definitions, §3.1 and the rendered Table 2. The table in [arXiv:2004.12497v11](https://arxiv.org/abs/2004.12497v11), printed p.5, and [the published Arnold Mathematical Journal paper](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), printed p.345, agree:
\[
k_{103}=A'/A,\qquad
k_{105}=\prod_i\sin(\theta_i/2),\qquad
k_{108}=k_{103}/k_{105},\quad N\equiv2\pmod4.
\]
The quotient sign and congruence are visible in both rendered tables. They are not PDF-text extraction artifacts. The tables' individual odd-period assertions about \(k_{103}\) and \(k_{105}\) do not restrict the definition of those numerical quantities to odd polygons; the k108 row explicitly proposes their quotient for the even period class.

The source defines \(A\) as the signed area of the orbit polygon and \(A'\) as the signed area of its outer polygon, formed from consecutive tangents to the billiard ellipse at the bounce points. This is distinct from the caustic-contact polygon. Equation (1) gives the signed cross-product area convention.

The usual internal polygon angles are the appropriate \(\theta_i\). The examples independently satisfy the source's k101 normalization
\[
\sum_i\cos\theta_i=JL-N=-26/9.
\]
Using supplementary exterior turning angles would instead change the cosine sum's sign and would not match that source convention. This rules out silently repairing the quotient by changing the angles.

The source assumes a strictly nested confocal ellipse pair and its one-parameter Poncelet billiard family. It imposes no exclusion of convex primitive hexagons or axis-symmetric members of such a family.

## 2. Exact geometric reconstruction

Both outer and inner ellipses are nondegenerate:
\[
E:x^2/4+y^2=1,\qquad
E_c:x^2/(32/9)+y^2/(5/9)=1.
\]
The two squared semiaxes decrease by the common amount \(4/9\), strictly between zero and \(b^2=1\). Thus the focal distance is unchanged and the caustic is strictly inside the billiard ellipse.

I recomputed all sides from the submitted vertex lists. Every vertex lies on \(E\). The six vertices in each list are distinct; all nonincident vertices lie strictly to the left of every directed edge. Hence the lists define positively oriented, strictly convex, simple hexagons.

For each side parameterized as \(p+t v\), restriction of the caustic quadratic gives \(at^2+bt+c\) with discriminant zero. Its double-root parameter is strictly between zero and one. In cyclic order, these parameters are
\[
P_H:(1/3,1/2,2/3,1/3,1/2,2/3),
\]
\[
P_V:(2/3,1/2,1/3,2/3,1/2,1/3).
\]
Thus the contact points lie on the actual finite chords, not only their supporting lines. The origin, and hence the caustic interior, lies to the left of each oriented supporting line.

At every vertex I verified the full specular law
\[
e_+=e_--2\frac{\langle e_-,n\rangle}{\langle n,n\rangle}n,
\qquad n=(x/4,y),
\]
with unit incoming and outgoing vectors. The incoming and outgoing normal components are \(1/3\) and \(-1/3\), respectively. Closure includes the last-to-first edge and its two endpoint reflections.

The six distinct bounce points imply least billiard period six: a smaller period would repeat a bounce point and its direction within that list. Neither orbit is a repeated three-period cycle. They are also different geometric polygons: \(P_H\) contains the points \((\pm2,0)\), while \(P_V\) does not.

Both orbits follow the same directed tangent branch, with the caustic on the left. The usual Poncelet porism for this fixed pair, already part of the original problem's setting, places them in the same six-period family as the starting point varies. Their common directly computed perimeter is \(28/3\), and their common Joachimsthal constant is \(1/3\). There is no comparison between different caustics or period families.

## 3. Outer polygons and angle products

I solved all six pairs of consecutive outer-ellipse tangent equations afresh. Their determinants are nonzero and their intersection points agree with the submitted outer polygons. Each bounce point lies strictly inside the corresponding finite outer-polygon side. This also checks that an accidental alternate tangent-intersection convention is not being used.

Signed shoelace areas give
\[
\begin{array}{c|ccc}
 & A&A'&A'/A\\ \hline
P_H&20\sqrt5/9&16\sqrt5/5&36/25\\
P_V&32\sqrt2/9&5\sqrt2&45/32.
\end{array}
\]
All areas are positive. Reversing both polygon orientations would change both area signs and leave their quotient unchanged.

The internal cosines independently recomputed from the unit edges are
\[
P_H:\quad -1/9\text{ twice},\quad -2/3\text{ four times},
\]
\[
P_V:\quad -7/9\text{ twice},\quad -1/3\text{ four times}.
\]
Every angle is strictly between zero and \(\pi\). Therefore the positive half-angle formula is unambiguous, and
\[
\prod_i\sin(\theta_i/2)=125/324\quad(P_H),\qquad
32/81\quad(P_V).
\]
All denominators in the proposed quotient are nonzero.

It follows directly that
\[
k_{108}(P_H)=11664/3125,\qquad
k_{108}(P_V)=3645/1024,
\]
and
\[
k_{108}(P_H)-k_{108}(P_V)=553311/3200000>0.
\]
An admissible pair at primitive period \(6\equiv2\pmod4\) is sufficient to refute the universal printed assertion.

## 4. Independent controls and reproducibility

The submitted checker and receipt were copied into author_replay/ and rerun without editing the author directory. The resulting receipt is byte-identical to the frozen receipt; all 291 assertions pass.

The independent checker uses rational coordinate systems \((u,\sqrt5\,v)\) and \((\sqrt2\,u,v)\), with Euclidean metrics \(\operatorname{diag}(1,5)\) and \(\operatorname{diag}(2,1)\). This removes the quadratic radicals while preserving exact physical geometry. It reconstructs the line-restricted caustic discriminants, contact parameters, unit velocities, reflections, tangent intersections, scaled areas and half-angle-product squares. All required square roots of the final rational squares are checked with integer square roots. Its 272 assertions pass.

This independent implementation uses neither SymPy nor any submitted routine. The original author verification requires SymPy 1.14.0; the independent verification requires only Python's standard library.

The ancillary area-product and product-of-invariants equalities are retained only as consistency checks on these two examples. They do not prove a repaired all-period theorem.

## 5. Publication recommendation

Recommend **claimed_solved, 1/5** for the literal k108 target, with wording such as “counterexample to the printed k108 quotient.” Preserve:

- Both primary source table references and the explicit quotient/parity statement
- The convex, primitive, nondegenerate six-period geometry and same-caustic qualification
- The distinction between internal and exterior angles, and between outer tangents and caustic contacts
- Credit for the previously checked six-bounce geometry and the distinct neighbouring investigations
- The absence of any corrected general invariant, official source correction or first-discovery claim

A bounded search did not locate a published correction of this exact row. That negative search is not a priority certificate. This is a separate adversarial AI review, not human peer review.

The frozen mathematical snapshot needs no correction. All source scope and mathematical claims in the submitted counterexample are covered by this verdict.

