# Independent derivation before source verification

Audit begun 2026-10-21T04:53:01Z. Only the pinned proof `original/PUBLIC_TURN_2.md` and `original/source_record.json` were read before this note. No prior or fresh review has been read.

## Lemma A: direct check

Let X be smooth projective integral over an algebraically closed field and H nef with e=H^2>=2, represented by an integral Cartier curve C. If pg>0 the product of any nonzero canonical section and the square of a defining section of C gives the required nonzero section. In the pg=0 case, duality gives H^2(O_X)=0, which should imply smoothness of Pic^0 through the obstruction space for line-bundle deformation. Thus q=h^1(O_X)=dim Alb(X), subject to primary-reference confirmation.

The normalized curve's Jacobian maps to Alb(X). If its image B is proper, the quotient morphism b:X->Alb(X)/B is constant on C. For an ample M on the quotient, N=b^*M is nef and N.H=0. Hodge index and nefness force N numerically trivial. A nonconstant projective morphism has a curve on which the pullback of an ample line bundle has positive degree, even when the curve map is inseparable: the degree is the finite map degree times the positive ample degree. Therefore b is constant. The universal property/generation of the Albanese then forces B=Alb(X). This gives q<=g(C_normalization)<=pa(C).

Adjunction gives KH=2pa(C)-2-e. Riemann--Roch gives chi(K+2H)=1-q+KH+2e=e+2pa(C)-1-q>=e+pa(C)-1>=1. Serre duality gives h^2(K+2H)=h^0(-2H)=0 because H is nef and H.(-2H)=-2e<0. No sign discrepancy is apparent.

## Lemma B: first independent check

Normalization of a projective integral surface is finite and projective. A projective resolution of its normal surface can be chosen to be an isomorphism over the regular locus, so every exceptional curve maps into the finite singular locus of the normalization; its image in S is finite. A general plane can avoid these finitely many points. Its scheme-theoretic inverse image on X is an effective Cartier divisor. If the plane section E is integral, its generic point is regular on S, and no exceptional curve lies above it, then the pullback has a unique codimension-one component, multiplicity one. A Cartier divisor on a smooth surface is Cohen--Macaulay and has no embedded associated points, so generic reducedness implies reducedness. This appears to establish integrality without smooth Bertini for X's pulled-back system.

Restriction from the resolution injects q_*omega_X into omega_Y because Y is normal and omega_Y is the reflexive extension of its regular-locus canonical bundle. Finite duality should identify nu_*omega_Y with Hom(nu_*O_Y,omega_S). For the rank-one finite birational extension A subset B in its fraction field, Hom_A(B,A) identifies with the conductor. For a hypersurface S, omega_S=O_S(e-4). Therefore a section from Lemma A gives a nonzero section of the conductor twisted by e-2.

At a height-one singular point of S, its one-dimensional local domain is not regular and so is not normal (normal local domains of dimension one are DVRs). A conductor element that is a unit would imply normalization equality locally. Thus the conductor is contained in every height-one singular prime and its sections vanish along every reduced singular curve. The polynomial lift uses H^1(P^3,O(-2))=0 and is nonzero because the section on S is nonzero.

## Adversarial targets requiring source-level verification

- Formal smoothness of the Picard scheme from H^2(O)=0 in arbitrary characteristic and exact relation q=dim Alb.
- Integral general plane section and complete avoidance of images of resolution exceptions.
- Existence/projectivity of surface resolution in arbitrary characteristic, and reflexive canonical sheaf on normal surface.
- Finite canonical duality without any separability or normality assumption on S.
- Whether the conductor argument proves scheme-theoretic vanishing on each reduced singular curve, including purely inseparable normalization along its generic point.
- Boundary controls: e=1, smooth quadrics, cones, ruled surfaces, pg=0 with nonreduced Picard in characteristic p, nef H having zero intersection with some exceptional curves, and nonnormal surfaces.

Current best guess: the chain is sound, with several references and explanatory local steps still to verify. Audit completion estimate: 20%.
