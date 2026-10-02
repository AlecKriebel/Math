# A positive prior-construction certificate for the literal problem

Reconstructed on 2026-10-02 after the source-first seal. This is an audit certificate, not a new paper or a novelty claim. No sibling proof was read before this reconstruction. The inherited root sine-curve exposure and the later disclosed cosine-curve hypothesis are recorded in `INITIAL_RECONSTRUCTION.md`.

## Published primary construction

Lei Ni, Wei Zhang, and Yijian Zhang, *On questions of Pogorelov and Toponogov*, arXiv:2606.29231v1, submitted 28 June 2026, Section2, printed pp2–3, explicitly construct the entire graph

$$V(x,y)=(x,y,x^4-y^4)$$

with unit Gauss map

$$n(x,y)=\frac{(-4x^3,4y^3,1)}{\sqrt{16x^6+16y^6+1}},$$

and closed asymptotic curves

$$\gamma_a(t)=(a\cos t,a\sin t,a^4(\cos^4t-\sin^4t)),\qquad a>0.$$

These formulas and the asymptotic calculation are explicit in the primary source; no unavailable theorem is needed. The fresh PDF is 329660 bytes, SHA256 `0ec8ff7da6224ece69f2beee6e71a39697a2fbc4a0aacb01b384755e69f9bbd2`. The source does not explicitly mention Ghomi2019 Problem1.4 or claim its binormal/linking conclusion. The following checks establish that its construction already gives a negative answer to that precise literal question, by immediate algebra and the definition of linking. This is a credited consequence of a prior construction, not evidence that the original author had already stated this exact consequence.

## Exact full-target specialization

Choose a=1. Then

$$\gamma(t)=(\cos t,\sin t,\cos2t),\qquad b(t)=(-4\cos^3t,4\sin^3t,1),\qquad B(t)=b(t)/|b(t)|.$$

1. The curve is smooth and closed. Its planar projection is the once-covered unit circle, so it is an embedding and its derivative never vanishes. Direct differentiation gives $\gamma'\times\gamma''=b$. The third component is1, so curvature never vanishes. Thus the osculating planes are smooth and unambiguous, and B is their smooth unit normal, orthogonal to both first and second derivatives.

2. The field B is one-to-one on $\mathbb R/(2\pi\mathbb Z)$. Its third component is positive, and the coordinate ratios are $B_1/B_3=-4\cos^3t$ and $B_2/B_3=4\sin^3t$. The real cubic is injective. Equal B values therefore imply equal sine and cosine and hence the same point of the parameter circle. This even proves global injectivity of the graph's Gauss map, since the same ratios recover x and y.

3. The spherical binormal is smooth but has four critical points. We have $b'=(12\cos^2t\sin t,12\sin^2t\cos t,0)$. Since b has constant third component1, differentiating its normalization gives B'=0 exactly when b'=0, namely t=0,π/2,π,3π/2 modulo2π. These points are allowed by the literal continuous-binormal hypotheses. They exclude use of the nonzero-torsion/regular-Gauss-map hypotheses of the negatively curved surface question.

4. Let D be the oriented graph disk $\{(x,y,x^4-y^4):x^2+y^2\le1\}$, whose boundary is γ. For $0<\varepsilon<1/4$, set $q_\varepsilon(t)=\gamma(t)+\varepsilon B(t)$ and $\alpha(t)=\varepsilon/|b(t)|$. Write x=cos t and y=sin t. Its coordinates are $(x-4\alpha x^3,y+4\alpha y^3,x^4-y^4+\alpha)$. Because $0<4\alpha x^2<1$ whenever x≠0, $|x-4\alpha x^3|\le|x|$. Also $|y+4\alpha y^3|\ge|y|$. Hence

$$q_{\varepsilon,3}-q_{\varepsilon,1}^4+q_{\varepsilon,2}^4
=\alpha+[x^4-(x-4\alpha x^3)^4]+[(y+4\alpha y^3)^4-y^4]\ge\alpha>0.$$

Thus the push-off is disjoint from the entire graph, and in particular from D and its boundary, for every $0<\varepsilon<1/4$. Since γ is a compact smooth embedding and B is a smooth nowhere-zero normal field, its sufficiently small constant-length normal push-off is an embedding by the tubular-neighborhood theorem (equivalently openness of embeddings in the C1 topology). Choose ε below both1/4 and this positive embedding radius. The linking number is the oriented intersection number of this push-off with D, which is zero because there are no intersection points. This proves $\operatorname{Lk}(\gamma,\gamma+\varepsilon B)=0$ with no numerical or asymptotic-sign assumption. It is unnecessary to compute writhe or total torsion.

These four checks cover every literal target hypothesis and the stronger unit-binormal and embedded-center conventions. One valid example disproves the universal assertion. The example does not have nonvanishing torsion; it does not settle Nirenberg's negative-curvature problem or Ghomi–Raffaelli2025 Problem1.1.

## Relation to the audit's cosine candidate and older construction

For the parent candidate $\Gamma(t)=(\cos t,\sin t,\tfrac14\cos2t)$, the direct binormal is $(-\cos^3t,\sin^3t,1)$ normalized. It is the same prior family: in Ni–Zhang–Zhang choose $a=4^{-1/3}$ and scale ambient coordinates by1/a. Its z-coordinate becomes $a^3\cos2t=\tfrac14\cos2t$. Positive homotheties preserve binormal directions, injectivity, and linking. There is therefore no new construction at the chosen amplitude.

Thomas Banchoff's Brown teaching page, *Spherical Images of Space Curves*, §4.1 exercise2, explicitly gives $X(t)=(\cos t,\sin t,\cos(2t)/c)$ and asks for the values of c producing cusps in the binormal indicatrix. Its embedded applet data contains precisely this formula and c ranging from0.5 to4. The fresh page has SHA256 `d2c8f4693cbf7891d20ba3d4353f41583a2a55b0a582481cc26e839fc3f3e330`; the server returns Last-Modified2 February2009. That metadata is not an independently archived publication date, and the page does not print a binormal-injectivity or linking theorem. It is an additional positive attribution of the exact curve family, not the sole priority certificate. The dated2026 primary preprint and the explicit specialization above suffice for the already-solved audit disposition.

## Exact outcome convention

Recommend `already_solved`: the original unsolved question now has a directly verified negative answer obtained from a prior, dated, publicly available construction. This does not mean the question was never historically open, that the cited authors stated the same consequence, or that the strictly negative-curvature surface problem is resolved. Preserve the original partial attempt and its historical reviews; supersede current unresolved-status/remaining-gap language globally with this credited consequence after a fresh full-candidate adversarial gate. No new discovery paper, DOI, or publication tracker entry is warranted under the user's workflow.
