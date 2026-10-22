# The two matching Yoneda algebra

## Claim and dependencies

Let X=S_(2,2) be the smooth resolved Slodowy slice, let A and B be its two Springer-fiber components, and put E_A=i_*K_A^(1/2), E_B=j_*K_B^(1/2). Over C, the ordinary cohomologically graded Yoneda algebra Ext*(E_A⊕E_B,E_A⊕E_B) is isomorphic to the usual two-matching arc algebra. In particular it agrees, up to an abstract graded algebra isomorphism, with the opposite-sign repaired 12-dimensional convolution described in the earlier packet.

This is a k=2 statement, not the all-k conjecture. It uses the published pairwise-module theorem of Mladenov, the established Springer geometry, and proper-support Serre duality. The elementary algebra argument below supplies the mixed-product step; it does not assume it from pairwise formality. No historical novelty is claimed.

## Geometry and graded spaces

For a nilpotent N on C4 with ker N=im N=W of dimension 2, the two components of the Springer fiber are

A={F2=W}≅P1×P1,
B={F3=N⁻¹(F1)}≅P(O(1)⊕O(−1))=F2.

They intersect cleanly in C≅P1. It is the diagonal in A and the section of self-intersection −2 in B. These facts, including the line-convention for projectivization, are proved in the original frozen packet and checked in its independent audit.

Let x,y be the two standard degree-2 classes on A. On B let h be the base class and s the negative-section class. Then

H*(A)=C[x,y]/(x²,y²),
H*(B)=C[h,s]/(h²,s²+2hs).

Set p=h, q=−s−h. Then p²=q²=0 and pq spans H4(B). All of x,y,p,q restrict to the same positive generator t on C.

The half-canonical bundles exist. On A one can use O(−1,−1); on B the class −s−2h squares to the canonical class −2s−4h. The orientation local system of the pair is trivial because C=P1 has no nontrivial two-torsion line bundle or rank-one order-two local system.

The established Ext-space computation gives diagonal graded dimensions (1,0,2,0,1), and off-diagonal dimensions 1 in degrees 1 and 3 and zero elsewhere. The individual self-Ext rings are the above cohomology rings.

## What the module theorem contributes

Mladenov, Theorem 0.1.12 and Remark 0.1.13(2), apply to compact Kähler Lagrangians in a holomorphic symplectic variety with a smooth intersection and square roots of their canonical bundles. They identify Hom-derived-from-one-to-the-other as a module over either self-derived-endomorphism algebra with the corresponding cohomology restriction module. The variety X need not be compact. A and B are smooth projective Lagrangians, and their clean intersection is C, so the hypotheses apply here.

The needed consequence is deliberately weak: for M=Ext*(E_B,E_A), either degree-2 square-zero generator of either diagonal ring acts nontrivially from M1 to M3. This follows from the displayed restriction maps. We do not require the two one-sided isomorphisms supplied by the theorem to come with any simultaneous or canonical compatibility. Independent scaling of generators in the two diagonal rings is permitted.

Analytic and algebraic Ext agree for these algebraic coherent sheaves with proper support: local sheaf Ext commutes with analytification, and the resulting coherent cohomology is supported on the proper intersection, where GAGA applies. Thus the analytic form of the theorem gives the required algebraic Ext-module assertion.

## An elementary two-object algebra lemma

Let E be a nonnegatively graded associative C-algebra with orthogonal idempotents e_A,e_B summing to 1. Write E_XY=e_X E e_Y, so multiplication E_XY×E_YZ→E_XZ is in left-to-right block order. Suppose:

1. E_AA=C[x,y]/(x²,y²) and E_BB=C[p,q]/(p²,q²), with all four generators in degree 2.
2. E_AB and E_BA each have one-dimensional pieces in degrees 1 and 3 only.
3. On E_AB, the actions of each of x,y,p,q from degree 1 to degree 3 are nonzero.
4. The two composition pairings E_AB^1×E_BA^3→E_AA^4 and E_AB^3×E_BA^1→E_AA^4 are nonzero.

Then E is isomorphic to the usual two-object arc algebra, by an isomorphism preserving the grading and the two idempotents.

### Proof

Choose u≠0 in E_AB^1 and w≠0 in E_AB^3. Rescale x,y,p,q independently so that

xu=yu=up=uq=w.

Rescaling either square-zero generator preserves the presentation of its diagonal ring. Define a=xy and b=pq; these are nonzero top-degree elements. Choose arbitrary nonzero v∈E_BA^1 and z∈E_BA^3. Write

uz=αa, wv=βa, vw=γb, zu=δb.

Assumption 4 gives α≠0 and β≠0. Temporarily write

vx=s_x z, vy=s_y z, pv=r_p z, qv=r_q z.

Write uv=c_x x+c_y y. Associating x(uv)=(xu)v and y(uv)=(yu)v gives c_y=c_x=β. Thus

uv=β(x+y).

Associating (uv)x=u(vx) and (uv)y=u(vy) gives

s_x=s_y=β/α.

Similarly (up)v=u(pv) and (uq)v=u(qv) give

r_p=r_q=β/α=:r.

Write vu=d_p p+d_q q. Associating (vu)p=v(up) and (vu)q=v(uq) gives d_p=d_q=γ. Hence

vu=γ(p+q).

Now (uv)u=u(vu) says 2βw=2γw. Since the field has characteristic zero and w≠0, γ=β. Finally (pv)u=p(vu) says rδb=γb. Since r=β/α and γ=β, it follows that δ=α.

Replace v by v0=β⁻¹v and z by z0=α⁻¹z. The multiplication now has

vx=vy=pv=qv=z,
xu=yu=up=uq=w,
uv=x+y, vu=p+q,
uz=wv=a, vw=zu=b,

where v,z denote the new normalized generators. All unspecified products follow from idempotents, the diagonal relations, or the fact that degrees above 4 vanish. In particular, w z and z w vanish. This is exactly the standard Frobenius multiplication/comultiplication table for two crossingless matchings: the two diagonal rings are tensor squares of C[t]/(t²), the off-diagonal rings are C[t]/(t²) shifted by one, and Δ(1)=t⊗1+1⊗t, Δ(t)=t⊗t. This proves the lemma.

## Applying the lemma to coherent sheaves

Take E_XY=Ext*(E_Y,E_X). This block order is chosen so that the usual right-to-left composition of maps becomes multiplication in the indicated corners.

The self-Ext rings and graded dimensions give assumptions 1 and 2. Apply the module theorem to the ordered pair (B,A) and to the action at each endpoint; the nonzero restriction values of x,y,p,q give assumption 3 after independent identifications of the two diagonal rings.

Finally, X is smooth symplectic of complex dimension 4, hence K_X≅O_X. Both sheaves have proper support and are perfect on X. Proper-support Serre duality yields perfect pairings

Ext^r(E_B,E_A) × Ext^(4−r)(E_A,E_B) → Ext^4(E_A,E_A) → C.

For r=1 and r=3 the factors are one-dimensional. Their nonzero generators therefore have nonzero compositions, proving assumption 4. One can justify the proper-support version by extending the sheaves to a smooth projective compactification: their supports stay away from the boundary, so Ext and the canonical-bundle restriction are unchanged, and ordinary Serre duality applies.

The lemma proves the claimed graded-algebra isomorphism for k=2.

## Why this does not settle k greater than 2

The proof uses an exceptional small-dimensional feature: each mixed degree-1/degree-3 space is one-dimensional, and multiplication by either diagonal degree-2 generator reaches the top mixed piece. Associativity then compares two scalar multiples of one w and forces equality. For larger k, mixed spaces have several independent cohomology classes and products between three distinct objects cannot be reconstructed from these two nonzero duality pairings. The separate higher-rank constraint computation gives an explicit place where dimension and bimodule balance alone leave two possible product directions.

## Primary references

- C. Stroppel and B. Webster, 2-block Springer fibers: convolution algebras and coherent sheaves, Comment. Math. Helv. 87 (2012), Theorems 40 and 45, https://doi.org/10.4171/CMH/261.
- B. Mladenov, Formality of differential graded algebras and complex Lagrangian submanifolds, Selecta Mathematica 30 (2024), article 8, Theorem 0.1.12 and Remark 0.1.13, https://doi.org/10.1007/s00029-023-00894-3.
