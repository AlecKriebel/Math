# k817 as a credited area-product corollary

**5100060 / AMR-050-0060. Full candidate after one substantive author turn. Independent review and validation of the frozen antipedal input are required before publication. No novelty claim.**

## 1. Exact theorem and domain

Let E be x²/a²+y²/b²=1, a>b>0, with foci F=(±c,0), c²=a²-b². Fix a strictly nested nondegenerate confocal elliptical caustic. Let P_i be a family of primitive billiard orbits of least period N divisible by four, in traversal order, with any coprime turning number 0<tau<N/2. This includes the admissible primitive stars.

For a fixed original focus F define the unit focal-inverse vertices and antipedal side lines by

    I_i = F+(P_i-F)/|P_i-F|²,
    L_i = {X:(P_i-F)·(X-P_i)=0},
    U_i = L_i intersection L_(i+1).                 (1)

Let A, V_F and B_F be the signed shoelace areas of P, I and U, respectively. The theorem is

    V_F B_F is independent of the orbit phase.      (2)

This is precisely arXiv:2004.12497v11 Table 9, k817, A_j^dagger A_(j,ant), N=0 modulo 4. The published companion omits the row; its differently numbered inverse table is not the target. Areas use straight edges between the listed vertices, not curved images of original edges or unsigned filled regions.

All objects in (1) are finite. The ordinary focal distance on the ellipse is at least a-c>0, so inversion has no real pole. Two consecutive antipedal normals would be dependent only if the original chord passed through F. That chord is tangent to the strict elliptical caustic, and F is strictly inside it, which is impossible. Thus each antipedal intersection exists uniquely in the affine plane.

## 2. Exact inputs, with hypotheses matched

The two complete input proofs are included unchanged and pinned in INPUTS.md.

**Input A: original/inverse product.** The independently reviewed proof in PR207, SHA256 d92e9a82674b1562e0b980c78088fc48319f9fc3d9d46ec55a1a46c893e372b8, proves that under exactly these strict confocal, primitive N-divisible-by-four and unit original-focus conventions,

    A(w) V_F(w)=C_F,                                (3)

where C_F is constant. The proof includes primitive stars and treats N=4 separately when the generic pole formula changes. Neither an outer polygon nor the circular image of a whole side is substituted.

**Input B: even focal antipedal proportionality.** Sections 3–5 of the frozen k404 proof, SHA256 b8edd78d03dac33a7be77837649eef7a8558900b3499774725174836fa54d462, establish for every primitive even period under the same ellipse/caustic hypotheses that

    B_F(w)=kappa_F A(w).                            (4)

The proof first obtains the actual focal antipedal intersection formula, then bounds its area poles by order two. Reflection, reversal and the imaginary anti-period force an odd Laurent expansion at the relevant pole, leaving only simple poles. Residue matching on the quotient torus identifies the area with a scalar multiple of the original-area cyclic dn trace. Its coefficient is allowed to be zero.

This is the general-even part of that proof. Its subsequent specialization to a focal pedal ratio for N=2 modulo 4 is not used here. Normalizing the caustic major semiaxis in its derivation preserves (4), since both B_F and A scale by the same factor.

## 3. The corollary, without an unjustified division

Multiply (4) by V_F and apply (3):

    V_F(w) B_F(w)
      = kappa_F A(w) V_F(w)
      = kappa_F C_F.                              (5)

This proves (2) for every real phase. No inverse area or antipedal area is divided by. Therefore zero antipedal areas, including an identically zero numerator family if it occurs, are harmless; no nonzero-area hypothesis is added to the source product.

Central inversion cyclically permutes a primitive even orbit and interchanges the foci. It preserves signed area in two dimensions and is equivariant with both constructions (1). Thus V_(F+)=V_(F-) and B_(F+)=B_(F-), so the two products have the same constant.

Reversing traversal negates both derived signed areas, preserving their product. Repeating an already admissible primitive orbit r times multiplies each signed area by r and the product by r², which is still constant along that repeated family. Merely taking a repetition whose indexing length is divisible by four does not place its underlying primitive orbit in the theorem.

## 4. Unit inversion, a four-period control, and limits

The unit-circle normalization in (1) is essential for numerical values. If the inversion radius is changed to rho, V_F is multiplied by rho⁴ while B_F is unchanged, so the product value is multiplied by rho⁴. Constancy remains, but the source uses rho=1.

As an exact N=4 check, use the axial parallelogram

    (0,b), (-a,0), (0,-b), (a,0).

Direct line intersections give B_F=4ab. The focal-inverse signed area is 2/(ab), the same elementary computation behind the credited N=4 inverse-product value A V_F=4. Thus (5) has value 8 for this N=4 family. This is a normalization check for the corollary, not a substitute for the all-period inputs.

The proof covers only the source's strict noncircular confocal ellipse ensemble. No hyperbolic or degenerate caustic, arbitrary inversion center, outer-locus focus, centroid, polar-area, or dual-area statement is asserted. The numerical diagnostics and exact finite checks corroborate the objects and normalization. The mathematical proof of the full product is the hypothesis-matched deduction (3)–(5), with both full input proofs available for independent examination.
