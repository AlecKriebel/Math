# Marked simultaneous reversal for free two-string-link exteriors

## Result and exact scope

**Theorem.** Let \(C=D^2\times[0,1]\), with its product orientation, and let \(p_1,p_2\) be distinct points of the real diameter of \(D^2\subset\mathbb C\). Let
\[
L_i:[0,1]\longrightarrow C,\qquad i=1,2,
\]
be disjoint smooth proper embeddings which are \(L_i(s)=(p_i,s)\) near their endpoints. They are ordered and oriented by increasing \(s\). They need not be monotone in the height coordinate away from the endpoints. Define
\[
r(z,t)=(\bar z,1-t),\qquad (\iota L)_i(s)=r(L_i(1-s)).
\]
If the actual fundamental group of the exterior of \(L_1\cup L_2\) is free of rank two, then there is a smooth ambient isotopy of \(C\), fixed on its boundary, taking each ordered, oriented strand \(L_i\) to \((\iota L)_i\). The isotopy may be taken fixed on a sufficiently small boundary collar.

This proves equivalence of ordinary unframed, ordered, fixed-endpoint string links. It neither assumes that free string links are braids nor makes a conclusion about preserving an independently specified framing. It does not extend automatically to three or more strands.

## 1. The actual exterior is a handlebody

Choose disjoint tubular neighborhoods \(N_i\cong D^2\times[0,1]\), standard near the endpoints, and put
\[
H=\overline{C\setminus(N_1\cup N_2)}.
\]
Here removal means removal of the relative interior, so the lateral annuli remain in \(\partial H\). Round all corners compatibly when working smoothly. The open complement deformation retracts to this exterior, hence has the same fundamental group. Its boundary is the four-holed outer sphere \(P\) with a lateral annulus \(A_i\) joining the two boundary circles belonging to strand \(i\). Thus \(\partial H\) is a connected closed genus-two surface.

The manifold \(H\) is irreducible. A smooth embedded sphere in its interior bounds a ball on the bounded side in the ambient ball \(C\), by smooth Schoenflies. Each connected \(N_i\) meets \(\partial C\) and is disjoint from the sphere, so it lies outside that bounded ball. Therefore this ball is contained in \(H\).

For completeness, the free-group-to-handlebody implication in this setting follows by compression, rather than from any assertion that a free tangle is trivial. Every subgroup of a free group is free. A closed positive-genus surface group is not free, so the fundamental group of any positive-genus boundary component of a compact manifold with free fundamental group cannot inject into that manifold's group. The Loop Theorem consequently supplies an essential compressing disk.

Cutting along a properly embedded disk preserves irreducibility: a sphere in a cut component bounds a ball in the original manifold; the cutting disk cannot enter that ball because it is connected, disjoint from the sphere, and has boundary on the original boundary. Cutting also makes each component's fundamental group a free factor of the original group, by van Kampen (reconstruction attaches one-handles along disks). Thus the component groups remain free. Continue compressing positive-genus boundary components. This terminates: the sum of \(3g-2\) over positive-genus boundary components strictly decreases under every essential compression.

Every final component is irreducible with only spherical boundary and hence is a ball. Indeed, push one boundary sphere into its collar; irreducibility fills it on the side away from the boundary collar, giving a ball bounded by the original boundary sphere. Reversing the cuts reconstructs \(H\) from balls by one-handles, so \(H\) is a handlebody. Its connected genus-two boundary identifies its genus as two.

The needed Schoenflies and Loop Theorem statements are in Hatcher's *Notes on Basic 3-Manifold Topology*, Theorem 1.1 and Theorem 3.1. No Poincare-conjecture input is required for this exterior argument.

## 2. Fix the complete boundary map before extending anything

Take each tubular chart
\[
q_i:D^2_\epsilon\times[0,1]\longrightarrow N_i
\]
to satisfy \(q_i(0,s)=L_i(s)\) and \(q_i(z,s)=(p_i+z,s)\) near both endpoints. Such a normal trivialization exists: the oriented normal bundle over an interval is trivial, and its two endpoint trivializations can be joined. An arbitrary integer twist in that choice is allowed.

Define a self-map \(\tau\) of \(\partial H=P\cup A_1\cup A_2\) by
\[
\tau|_P=r|_P,\qquad
\tau\big(q_i(z,s)\big)=q_i(\bar z,1-s),\quad |z|=\epsilon.
\]
These prescriptions agree exactly on the four seam circles. Because the charts are standard near the endpoints, they also agree on the nearby product germs. Equivariant corner rounding therefore makes \(\tau\) a smooth orientation-preserving involution of the closed boundary surface.

There are exactly six fixed points: two on the outer sphere, at the ends of the real diameter in the middle-height slice, and two on each lateral annulus, at \(s=1/2\) and \(z=\pm\epsilon\). The quotient is a sphere: the branched-cover Euler-characteristic formula gives
\[
-2=2\chi(\partial H/\tau)-6,
\]
so \(\chi(\partial H/\tau)=2\). Thus \(\tau\) is the genus-two hyperelliptic involution.

Equivalently, let \(H_0\) be the trivial two-string-link exterior with identical endpoint disks. The map \(\phi:\partial H_0\to\partial H\) which is the identity on \(P\) and uses \(q_i\) on the two annuli conjugates the standard half-turn \(r|_{\partial H_0}\) exactly to \(\tau\). This identification is only a boundary identification; no pattern-preserving diffeomorphism \(H_0\to H\) has been assumed.

## 3. Extension over the handlebody, with exact boundary values

The genus-two hyperelliptic mapping class is central in the orientation-preserving mapping class group, and the standard representative extends over the standard genus-two handlebody. Consequently **the particular map \(\tau\), not merely its unmarked action on a set of curves, extends over \(H\).** Here is the correction that makes this precise.

Choose an arbitrary orientation-preserving handlebody diffeomorphism \(f:H\to H_0\). On \(\partial H_0\), the involution \(f\tau f^{-1}\) is conjugate to the standard hyperelliptic involution by the boundary diffeomorphism \(f\phi\). Centrality gives
\[
[f\tau f^{-1}]=[r|_{\partial H_0}].
\]
Therefore the diffeomorphism \(F_0=f^{-1}rf:H\to H\) has boundary restriction \(\sigma\) isotopic to \(\tau\). Let \(\delta_s\), \(0\leq s\leq1\), be a smooth surface isotopy with \(\delta_0=\mathrm{id}\) and \(\delta_1=\tau\sigma^{-1}\). For a boundary collar \(c:\partial H\times[0,\eta]\to H\), extend this to
\[
K(c(x,u))=c(\delta_{\lambda(u)}(x),u),
\]
where \(\lambda=1\) near \(u=0\) and \(\lambda=0\) near \(u=\eta\), and take \(K\) to be the identity elsewhere. Then
\[
F=K\circ F_0\quad\hbox{satisfies}\quad F|_{\partial H}=\tau
\]
pointwise. Intermediate surface isotopies need not preserve \(P\) or the annuli. Only the final boundary map is used for gluing, and it is exact.

One can alternatively prove the extension using a complete meridian disk system. Haas--Susskind's Theorem 1 implies that a genus-two hyperelliptic map preserves every unoriented simple-curve isotopy class. In particular it preserves the disk-boundary classes; a simultaneous surface isotopy restores a disjoint complete disk system, the map then extends across those disks and the remaining ball, and a collar correction again restores the originally prescribed \(\tau\).

Bruno--Mecchia explicitly records both handlebody extension and commutation up to isotopy on p.272 of *On quotient orbifolds of hyperbolic 3-manifolds of genus two*. The argument above explains why using these unmarked mapping-class facts does not discard this problem's boundary markings.

## 4. Glue back the arc tubes without a framing or pure-braid error

On each whole tube, use the explicitly prescribed map
\[
J_i(q_i(z,s))=q_i(\bar z,1-s),\qquad |z|\leq\epsilon.
\]
It preserves the tube label, reverses its core parameter, is orientation-preserving in three dimensions, and agrees with \(\tau\) on its lateral annulus. It equals \(r\) exactly on both endpoint disks and their standard product neighborhoods.

Glue \(F\) to \(J_1,J_2\). Smooth collar straightening permits the extension \(F\) to be chosen with the prescribed collar germs on the annuli and the outer boundary: the local maps supplied by \(J_i\) and \(r\) are compatible near every corner because \(q_i\) is standard near both ends. Equivalently, first arrange equality of boundary values as above, then use uniqueness of smooth collars relative to their boundary to arrange equality of product germs before gluing. Only the exterior-side collar is altered. This yields a smooth orientation-preserving ball diffeomorphism \(h:C\to C\) satisfying
\[
h|_{\partial C}=r|_{\partial C},\qquad
h(L_i(s))=L_i(1-s).
\]
It may be chosen to equal \(r\) on a boundary collar. No claim that \(h\) itself is an involution is necessary.

Now put \(g=r\circ h\). Since \(r^2=\mathrm{id}\),
\[
g|_{\partial C}=\mathrm{id},\qquad
g(L_i(s))=r(L_i(1-s))=(\iota L)_i(s).
\]
Both labels and the upward orientation of the target parameterization are exact. There is no residual endpoint permutation, braid, meridional twist, or outer-boundary mapping class: the displayed equality \(g|_{\partial C}=\mathrm{id}\) rules these out at the ambient-boundary level. Choices of tube framing only changed the intermediate \(\tau\) by conjugation and the corresponding \(J_i\); the displayed endpoint and core identities still hold for every choice.

Finally, every smooth boundary-fixed diffeomorphism of a three-ball is smoothly isotopic to the identity relative to the boundary. This follows, more strongly, from contractibility of \(\mathrm{Diff}(D^3\,\mathrm{rel}\,\partial D^3)\), explicitly listed and proved equivalent to Hatcher's theorem in his 1983 paper, Appendix, p.604, statement (1). Standard collar straightening gives the same path-component assertion with a sufficiently small boundary collar fixed. Apply this to \(g\). Its ambient isotopy carries \(L\) to \(\iota L\) exactly in the marked string-link category.

If a long-link rather than a ball formulation is desired, extend that collar-fixed isotopy by the identity outside \(C\). Thus no outside-ball motion contributes any braid or endpoint identification.

## 5. Reversal convention and limits

The map \(r\) is a rigid half-turn about the real transverse axis through the middle of \(C\). In coordinates \((x,y,t)\), its derivative has determinant \((1)(-1)(-1)=+1\). It fixes each transverse endpoint coordinate \(p_i\), exchanges top and bottom for that same label, and the reversal of \(s\) restores upward orientation. It is not the half-turn in the projection plane that exchanges left and right labels, and it is not an orientation-reversing ambient mirror.

For long links with labeled standard lines \((i,0,t)\), simultaneously reverse all strand orientations and restore the upward convention by \((x,y,z)\mapsto(x,-y,-z)\). Rescaling the longitudinal interval produces exactly this \(r\). The application to Duzhin--Karev must use that label-preserving convention; its verification and the unframed finite-type invariant are separate from this geometric lemma.

The proof uses actual freeness of the exterior group, not merely equality of nilpotent quotients. Its genus-two step cannot be carried over without proof to higher genus, where the hyperelliptic class is not central. Deleting strands from a free exterior has not been used. The conclusion is about unframed embeddings, not a chosen ribbon normal field.

## Source evidence

1. Allen Hatcher, *Notes on Basic 3-Manifold Topology*, Theorem 1.1 (p.1), Theorem 3.1 (p.56), and the smooth-category conventions including tubular neighborhoods and isotopy extension (p.1). Author-hosted PDF: https://pi.math.cornell.edu/~hatcher/3M/3Mfds.pdf . These supply the standard three-manifold inputs; the compression argument above is supplied here.
2. Andrew Haas and Perry Susskind, *The geometry of the hyperelliptic involution in genus two*, Proceedings of the American Mathematical Society 105 (1989), 159--165, Theorem 1, p.159, proof pp.160--162. DOI: https://doi.org/10.1090/S0002-9939-1989-0930247-2 . The statement was inspected in indexed full-paper text at https://scispace.com/pdf/the-geometry-of-the-hyperelliptic-involution-in-genus-two-36fv449p4o.pdf . The publisher byte retrieval returned HTTP 403, and the mirror byte retrieval returned HTTP 202 with zero bytes, so no local PDF hash is asserted for this source. This is supplementary to the downloaded Bruno--Mecchia statement.
3. Annalisa Bruno and Mattia Mecchia, *On quotient orbifolds of hyperbolic 3-manifolds of genus two*, Rend. Istit. Mat. Univ. Trieste 46 (2014), 271--299, p.272. Journal PDF: https://rendiconti.dmi.units.it/volumi/46/014.pdf . It states both handlebody extension and centrality up to isotopy. Downloaded and inspected.
4. Allen E. Hatcher, *A proof of the Smale Conjecture, Diff(S^3) ≃ O(4)*, Annals of Mathematics 117 (1983), 553--607, Appendix p.604, statement (1). Author-hosted PDF: https://pi.math.cornell.edu/~hatcher/Papers/SmaleConjecture.pdf . Its extracted text has an incorrect character encoding; the precise assertion was verified visually on rendered PDF page 52, printed p.604.

## Verification verdict

The proposed geometric theorem is valid under the ordinary smooth, unframed string-link convention stated here. No marked-boundary or tube-framing obstruction remains. The important repair to a short proof is to distinguish an extendible mapping class from the exact boundary map and to insert the collar correction before tube gluing. Smooth isotopy of the three-ball is another genuine theorem input; an unqualified smooth Alexander trick would not suffice.
