# Author turn 5: exact transverse saddle certificate

**Final author outcome: original unresolved 5/5.** The explicit branched-cover fixed point from Turn 4 has four hyperbolic transverse multipliers. Its stable relative elliptic surface therefore does not extend to a stable six-dimensional neighborhood by the proposed local mechanism. This is a statement about the tested fixed point. It proves neither ergodicity of the closed pseudo-Anosov nor impossibility of another nonergodicity construction.

## 1. Exact presentation of the degree-three cover

Retain the base automorphism φ(a)=ab, φ(b)=bab and the degree-three cover of Turn 4. For the Schreier calculation, use the right sheet action j·a=j+1 and j·b=−j modulo 3, starting at sheet 0. This is the right-coset convention corresponding to the same dihedral cover; the explicit rewrite rules below eliminate any ambiguity about permutation order. Choose spanning-tree paths 1,a,a². A free basis of the punctured-cover group H is

 h1=a³, h2=b, h3=ab a^(−2), h4=a²b a^(−1).

The lift of c³, c=[a,b], rewrites as

 r=h3 h4^(−1) h1 h2 h1^(−1) h3^(−1) h4 h2^(−1).

Filling gives the closed genus-two presentation <h1,h2,h3,h4 | r=1>. This follows from the actual connected three-sheeted once-punctured cover and its unique boundary; it is not inferred merely from the appearance of a length-eight word.

For reproducibility, positive a at sheet 2 contributes h1 and otherwise contributes no generator; positive b at sheets 0,1,2 contributes h2,h3,h4 respectively. Negative edges contribute the inverse generator of the positive edge at their terminal sheet. Update the sheet after each letter. Applying these rules to φ³(hj) gives four explicit free words, stored in TURN_5_COCHAIN_CERTIFICATE.json. Their lengths are 29,16,6,25. The checker verifies by free reduction that substituting back gives the original base words, that the induced automorphism preserves r exactly, and that its rewritten inverse is an inverse on each generator. No quotient word-problem oracle is assumed.

## 2. Algebraic coefficient field and the fixed representation

Let ξ be the negative root of p(X)=X⁴−3X³+2X²+2X−1 in the interval from Turn 4, and put η=ξ/(ξ−1). All the following coefficients lie in K=Q(ξ), with the indicated real embedding. Let A=ρ(a), B=ρ(b) be the unit quaternions realizing the exact trace triple (ξ,η,ξ). Their commutator has trace −1 and its cube is I in SU(2), not merely I after passing to the adjoint group. Thus the representation genuinely descends to the filled cover.

Write u=Im A and v=Im B. Use the real basis (u,v,u×v) of the Lie algebra. It is a basis because the commutator is nontrivial. Set

 U=1−ξ²/4, V=1−η²/4, W=ξη/4−ξ/2.

Its Gram matrix is diag-block [[U,W],[W,V]] together with the entry UV−W². In this basis,

 Ad_A = [[1,2W,ξW],[0,ξ²/2−1,−ξU],[0,ξ,ξ²/2−1]],

 Ad_B = [[η²/2−1,0,ηV],[2W,1,−ηW],[−η,0,η²/2−1]].

These follow directly from quaternion conjugation. The exact character fixed-point condition provides a conjugating rotation O taking Im A to Im(AB) and Im B to Im(BAB). Its first two columns are

 (η/2,ξ/2,1)^T and (1,ξ,0)^T,

and its third is the cross product of those two vectors in the above basis. The cross-product rules are

 e1×e2=e3, e1×e3=W e1−U e2, e2×e3=V e1−W e2.

The checker verifies O's Gram orthogonality, positive determinant, and its two adjoint intertwining identities exactly in K. The vector formulas and equality of the scalar parts show that it intertwines the actual quaternions, rather than only their images modulo sign. It lifts to a unit quaternion S with ρ∘φ=Ad_S∘ρ. The choice of sign of S has no effect on the tangent calculation. For φ³ the normalization back to ρ is O^(−3).

## 3. The tangent quotient, not just an unconstrained Jacobian

For a one-parameter deformation, use the left logarithmic cocycle z(g)=dρ(g)ρ(g)^(−1). It obeys

 z(gh)=z(g)+Ad_(ρ(g))z(h),
 z(g^(−1))=−Ad_(ρ(g)^(−1))z(g).

The four generator values form a 12-dimensional cochain space C1. Differentiating r produces a 3×12 matrix D. Infinitesimal conjugation gives the 12×3 matrix B whose j-th block is I−Ad_(ρ(hj)). Let L be the 12×12 derivative obtained by differentiating the four rewritten φ³ images and then multiplying every output block by O^(−3).

The portable certificate gives every entry of B,D,L,O^(−3) as four rational coefficients in the basis 1,ξ,ξ²,ξ³. The exact checker establishes

 DB=0,   DL=O^(−3)D,   LB=B O^(−3),
 rank D=3,   rank B=3.

Thus the actual closed-character tangent space is ker D / im B, of dimension 6. At this irreducible smooth point it is the standard twisted H1 tangent space. This explicitly removes both the relation constraints and the conjugation directions; a spectrum of the raw 12-dimensional matrix would not answer the question.

The characteristic polynomial of the induced six-dimensional map is therefore

 χ_H1(t)=det(tI_12−L)/det(tI_3−O^(−3))².

One factor removes the infinitesimal conjugations and the other the relation-normal quotient. The two chain-map identities and ranks above justify both factors, including multiplicities. Exact polynomial division has zero remainder.

## 4. The normal quartic and its rigorous root location

Put s=√13 with its positive real value. The characteristic polynomial simplifies to

 χ_H1(t)=(t²−(80−22s)t+1) N(t),

 N(t)=t⁴−a t³+b t²−a t+1,
 a=(53−5s)/2,   b=(705−163s)/2.

The first factor is the cube of the relative derivative: if its original trace is τ=2−s, then τ³−3τ=80−22s. The relative tangent plane injects and is symplectic by Turn 4. Its symplectic orthogonal is consequently an invariant four-plane, and N is the characteristic polynomial there. The reciprocal form is a consistency check, not a substitute for this identification.

All four roots of N are positive real numbers off the unit circle. To prove this without numerical eigenvalues, put r=t+t^(−1). Then N(t)/t²=r²−ar+(b−2). Its discriminant is

 Δ=(387s−1237)/2.

The rational interval 18/5<s<361/100 proves Δ>0, a>4, and

 (r²−ar+b−2)|_(r=2)=b−2a+2=(603−153s)/2>0.

The vertex a/2 lies to the right of 2 and the quadratic has two distinct real roots. Since its value at 2 is positive, both roots lie strictly to the right of 2. Each then gives two distinct positive reciprocal solutions of t²−rt+1=0, one below 1 and one above 1. The two r roots are different, so all four t roots are distinct. There are two contracting and two expanding real normal directions.

Meanwhile −2<80−22s<2, and the original relative multiplier is not a root of unity. Thus the known tangent pair remains elliptic after cubing. The ambient fixed point is an elliptic-center saddle, not an elliptic fixed point in six dimensions.

## 5. What this establishes and what it does not

The expanding directions yield a nontrivial local strong unstable manifold, so the fixed point is not Lyapunov stable in the full smooth character space. The relative stable neighborhoods lie on a normally saddle-type invariant surface and remain of zero ambient Goldman volume. In particular the two-dimensional Rüssmann stability theorem cannot justify an ambient stable neighborhood at this point, and the ordinary elliptic-fixed-point higher-dimensional KAM route fails its first spectral hypothesis here.

This does not prove that the same pseudo-Anosov acts ergodically. It does not exclude other periodic points, invariant sets elsewhere, different branched covers, or other measurable nonergodicity mechanisms. The fifth turn did not close the original full-volume target. It supplies an exact intrinsic linearization of this particular candidate point, rather than confusing the failure of a chosen formula with a global no-go theorem.

## 6. Reproducibility and final scope

The self-contained SymPy checker recomputes the Schreier words, inverse automorphisms, adjoint matrices, relation and conjugation maps, chain identities, ranks, characteristic-polynomial divisions, and root inequalities over exact rational/algebraic arithmetic. It reproduces the 25,144-byte cochain certificate byte-for-byte and passes 89 grouped exact assertions. A matrix equality is counted as one assertion, not inflated to the number of entries. The decisive hyperbolicity conclusion uses rational inequalities, with no floating-point spectrum or uncertified numerical KAM claim.

The consolidated result remains **unsolved 5/5**. The exact source-angle simplification and its specific stabilizer obstruction from Turn 3 are independent of this alternate dynamical route, and still require the separate source/convention audit. All historical turn files are preserved. No full source criticism, solution promotion or PR precedes independent review.
