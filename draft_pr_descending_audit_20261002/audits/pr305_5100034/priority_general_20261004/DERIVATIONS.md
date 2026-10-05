# Checkable priority bridges and blocked routes

This file records deductions performed in the GENERAL-route audit. They are not assertions that an older author stated the resulting focal claim. The mathematical gate remains ROOT's gate. All assumptions below are real, Euclidean, strictly nested nondegenerate confocal noncircular ellipses unless an explicit generic polygon construction is used.

## 1. Old triangle results imply failure of phase constancy C

Querret, Annales de mathématiques pures et appliquées 14 (1823–1824), printed pp.280–285, derives on p.284 the triangle pedal-area relation in modern notation

\[
D_T(M)=\frac{[T]}{4R^2}\bigl(R^2-|M-O_T|^2\bigr).
\]

Here projections are on supporting lines, \([T]\) is oriented triangle area, and \(O_T,R\) are its circumcenter and circumradius. Sturm's independent proof, pp.286–293, expressly accounts for signs on p.287; pp.289–291 identify circumcenter, radial dependence, and the quarter-area maximum. Both originals were retrieved from Numdam and the decisive equations were checked in rendered facsimiles. These are not unsigned-only or interior-foot assumptions.

For foci \(F_\pm=(\pm c,0)\), let \(O_T=(x,y)\), \(D=R^2-x^2-y^2-c^2\). Then

\[
\frac{D_T(F_+)}{D_T(F_-)}=\frac{D+2cx}{D-2cx}.
\]

Fierobe, arXiv:1807.11903v5 (22 July 2019), §4, Lemma 4.1, p.9, proves that the two axis-vertex billiard triangles in one family have distinct circumcenters on the focal axis. Its proof is short and checkable: if centers coincide, symmetry makes the circumcircles equal; the noncircular ellipse and that circle would share six distinct points, violating Bézout's degree-four intersection bound. Central inversion maps the two triangles to each other, so their centers are \((x,0)\) and \((-x,0)\); distinctness gives \(x\ne0\).

Each focus is strictly inside the caustic, and the caustic lies inside every convex triangular billiard polygon. Thus the foci lie inside the triangle and its circumdisk, so \(D\pm2cx>0\). Since \(c>0\) and \(x\ne0\), the focal ratio is positive and different from 1. Inversion preserves signed area under compatible counterclockwise indexing, swaps the foci, and changes this ratio to its reciprocal. Hence the original focal ratio is not phase constant, for every noncircular elliptic triangular family.

This is a short explicit implication of pre-2020 primary theorems. The literature search has not located an older explicit statement of this particular C counterclaim, nor the submitted exact numerical triangle. These are distinct historical questions. Since C includes all primitive N, its N=3 failure is decisive. No E or M theorem is needed for this implication.

### Direct consistency check of the classical formula

For any cyclic list of oriented support lines \(n_i\cdot X=h_i\), with unit normals \(n_i\), the feet of M are \(q_i=M+(h_i-M\cdot n_i)n_i\). Translation terms telescope, giving

\[
D(M)=\frac12\sum_i (h_i-M\cdot n_i)(h_{i+1}-M\cdot n_{i+1})\det(n_i,n_{i+1}).
\]

Writing \(n_i=(\cos\psi_i,\sin\psi_i)\), the anisotropic quadratic terms vanish by the identities
\(\sin(\psi_{i+1}-\psi_i)\cos(\psi_i+\psi_{i+1})=(\sin2\psi_{i+1}-\sin2\psi_i)/2\) and its sine counterpart. Thus D is an isotropic quadratic polynomial. For triangles its zero circle is the circumcircle (Simson); at the circumcenter the feet are the side midpoints and have area \([T]/4\). This recovers the displayed signed formula independently and checks the sign convention.

## 2. What Steiner's polygon identity supplies, and what it does not

Steiner's collected original, *Gesammelte Werke*, vol.I (1881 reprint), “Einige geometrische Sätze”, printed pp.15–16, proves

\[
D_S(M)=\frac{[S]}2-\frac18\sum_i\sin(2\theta_i)|M-P_i|^2.
\]

Its original item is attributed in the collected volume to Crelle's Journal vol.I; the often repeated “1825” date is not authenticated here as the publication date of this item. The 1881 facsimile's printed p.15 and the crucial p.16 Eq.(5) were checked visually; p.16's bottom is obscured in the Google scan, but the equation and preceding proof are legible. Native archive OCR is separately sealed and is not substituted for the facsimile.

Equivalently, the preceding support-line formula writes \(D_S(M)=d_S+v_S\cdot M+\kappa_S|M|^2\). At F± put \(U_S=d_S+\kappa_S c^2\) and \(m_S=c(v_S)_x\), so \(D_S(F_\pm)=U_S\pm m_S\). For original P and tangent polygon T, with positive denominators, E is **equivalent to**

\[
m_P U_T=m_T U_P.
\]

Steiner gives the quadratic representation, but does not assert this relation between the two moving polygons. Introducing this relation as a “consequence” without proving it merely transfers the central problem. Route status: BLOCKED as a full-priority implication absent a published bridge. The same issue remains with weighted curvature centroids: ordinary vertex or lamina centroids are not the \(\sin2\theta_i\)-weighted Steiner centroid.

The continuous pedal-curve area formula in Reznik–Garcia–Stachel, arXiv:2009.02581, Proposition 2 Eq.(4), p.8, gives equal areas at the two foci of a whole ellipse. It is an integral over all tangent directions, whereas D above is a finite adjacent determinant sum over a closed billiard phase. Replacing the latter by the former is unsupported; the triangular counterexample directly falsifies that replacement.

## 3. Old elliptic master identity and its exact conditional implication for M

Khare–Lakshminarayan–Sukhatme, *Local Identities Involving Jacobi Elliptic Functions*, arXiv:math-ph/0306028 (10 June 2003), published Pramana 62 (2004), DOI 10.1007/BF02704435, §4.1 Eqs.(39)–(42), pp.12–13, proves the following general mechanism. A meromorphic f periodic under 2K and antiperiodic under 2iK′ is reconstructed from its principal parts as a sum of translated dn functions and derivatives. Its proof matches all poles/principal parts, uses compact-torus constancy of the difference, then uses antisymmetry to kill the constant. The cyclic predecessor, DOI 10.1063/1.1560856, J.Math.Phys.44 (2003), §2.1.1 Eq.(20), pp.5–7, does the same for equally shifted traces. These methods predate this target by decades.

For a rectangular torus with real period L and imaginary period 4iH, choose modulus \(\kappa\in(0,1)\) satisfying \(K'_\kappa/K_\kappa=2H/L\), and \(\lambda=2K_\kappa/L\). Suppose two nonzero traces A,B have that real period, obey f(w+2iH)=−f(w), and have only at most simple poles at \(w_0\) and \(w_0+2iH\) modulo the torus. Set z=λ(w−w0)+iK′κ. The old master identity then has one pole in its half-imaginary rectangle and order one, so both A and B are scalar multiples of the same translated dnκ(z). Equivalently, subtract a residue-matching multiple: its pole partner is matched by antisymmetry; the difference is holomorphic on the compact torus and antiperiodic, hence zero. This proves B=C0 A. Real positivity fixes C0>0; focus exchange gives the same C0 for the other focus.

In the accepted submitted calculation, H=K′, L=4K/N, and w0=K−v+iK′ modulo periods. The old theorem does **not** establish these focal hypotheses. The required geometric verification includes: (a) the correct phase displacement of original versus outer feet; (b) double original foot poles soften to simple area poles through local parity; (c) adjacent outer poles separated by the orbit step have collinear leading vectors, cancelling double area terms; (d) quotienting by the primitive orbit collapses all poles into that common pair; (e) both traces are nonzero and denominators are positive for every coprime star winding. Those are precisely the substantive application, rather than an automatic citation-level substitution. Therefore the generic theorem is METHOD PRIORITY, not a located full prior E/M proof.

For odd N, one must not blindly apply the cyclic type-IV identity in the original modulus: focal exchange is a real 2K shift, not generally a sign change. The quotient-torus rescaling above avoids that false hypothesis. For even N, central symmetry already gives A+=A− and B+=B−, hence E=1; it still does not imply phase independence of B/A.

## 4. The nearby area and distance invariants leave a precise gap

Akopyan–Schwartz–Tabachnikov Theorem 3 is the odd-N invariant area ratio \([P]/[T]\) of the original and outer tangent polygons. Chavez-Caliz Theorem 6 is the even-N constant product \([P][T]\) for concentric ellipses in general position. Both are affine constructions. Orthogonal projection is not covariant under a nonsimilarity affine map, so their circle normalizations do not transfer to focal pedals. Their statements do not supply the relation in §2 above.

Bialy–Tabachnikov Theorem 4.1 fixes the centroid and the sum of squared point-to-tangent distances. These involve single normal moments. The support-line formula shows pedal area instead involves adjacent products \(h_i h_{i+1}\sin(\psi_{i+1}-\psi_i)\) and their point-dependent versions. Lemma 4.2 fixes the product of the distances of the two foci to **one** caustic tangent; Theorem 4.3 fixes even-N products of focal distances. Neither is an identity for adjacent signed products or for their trace ratio. Route status: BLOCKED unless a materially new published adjacent-moment bridge is supplied.

Roitman–Garcia–Reznik Theorems 1–2 and Corollary 1 use Jacobi poles and Liouville to prove bicentric cosine-sum and limiting-pedal perimeter invariants and focus-inversive billiard perimeter invariants. They authenticate the established complex method, but their pedal is the bicentric polygon pedal and their claimed invariant is perimeter. Appendix A's polar/pedal identification does not identify the original/outer focal signed areas or their shared multiplier. Appendix videos 17–18 explicitly mark area observations as experimental and concern focus-inversives, a different construction.

Glutsyuk's string and area Poritsky results provide translation coordinates or characterize conics. Area Poritsky uses equal areas cut off between a smooth curve and a chord; “outer billiard” there is not the outer tangent polygon here. A proof that focal feet are sampled with the relevant area Poritsky parameter would be an additional central bridge. Route status: BLOCKED as a full-priority shortcut.
