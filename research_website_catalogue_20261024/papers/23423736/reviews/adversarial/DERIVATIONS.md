# Checkable universal proof and adversarial boundaries

This final derivation retains the full original target. Its main all-field mechanism was sealed in INITIAL_RECONSTRUCTION.md before foreign bodies, supplied code/results and peer opinions. The normal/optimized finite diagnostics are implementation checks of these identities, not their universal justification.

## Exact quotient, not a quotient of an unknown quotient

Write F4=k⟨x1,x2,x3,x4⟩, F2=k⟨X,Y⟩ and e(x1)=e(x3)=X,e(x2)=e(x4)=Y. The kernel of e is the two-sided ideal L=(x3−x1,x4−x2): the induced map F4/L→F2 has the inverse X↦x1+L,Y↦x2+L. For the literal six target relations, direct expansion gives e(f1)=⋯=e(f4)=0 and e(f5)=e(f6)=Q=βX²−XY+YX−βY². Therefore

R/I=F4/(J+L)≅F2/e(J)=k⟨X,Y⟩/(Q)=A.

In particular no unproved assertion about the source algebra's noetherianity, dimension or birational geometry is needed to identify this kernel. The primary printed relations, including the x4 factors in f5/f6, were authenticated separately against OWR1361 and published RS1202.

## Universal basis and domain using operators

Assume β²≠1. Set U=X−Y,V=Y and

a=(1−β)/(1+β),   b=−β/(1+β).

The change of generators is unitriangular in every characteristic and Q=βU²+(β−1)UV+(β+1)VU. Thus A has the single relation VU=aUV+bU². A replacement of VU by either UV or UU strictly decreases fixed-length lexicographic order V>U. Consequently the words U^i V^j span A. No confluence assumption is being used.

To prove their independence without relying on section-ring dimensions, use k[u,z]. Define σ0(u)=a u,σ0(z)=z and

δ(u^n z^j)=b[n]_a u^(n+1)z^j,   [n]_a=Σ_(r=0)^(n−1) a^r,   [0]_a=0.

The identity [n+m]_a=[n]_a+a^n[m]_a proves δ(fg)=δ(f)g+σ0(f)δ(g) for monomials and hence all polynomials. This definition uses no division by a−1. The operators U0(f)=u f and V0(f)=δ(f)+zσ0(f) satisfy

V0 U0(f)=b u² f+a uδ(f)+a uzσ0(f)=a U0 V0(f)+b U0²(f).

Thus there is a representation of A on k[u,z]. Since V0^j(1)=z^j, the normal monomial U0^i V0^j sends1 to u^i z^j. These images are linearly independent, so the spanning normal monomials form a basis of A. In total degree n the basis has n+1 elements.

For a polynomial q(U), induction on its monomials gives

Vq(U)=q(aU)V+δ(q)(U).

Iterating, the highest V-degree term of V^j q(U) is q(a^jU)V^j. If P=Σ_(r≤j)p_r(U)V^r and Q'=Σ_(s≤l)q_s(U)V^s have nonzero top coefficients, the coefficient of V^(j+l) in PQ' is p_j(U)q_l(a^jU). It is nonzero because a≠0 and k[U] is a domain. Therefore A is a domain for arbitrary elements, not merely for homogeneous ones. This supplies an independent all-field basis/domain route beyond the manuscript's section-dimension sandwich.

Characteristic2 causes no exception: then a=1 and δ is a scalar multiple of u²∂/∂u. The finite geometric sum still defines δ even at roots of unity and at a=1. Neither diagonalization nor a formal division by2 is used.

## The actual positive-pullback THCR

Let S=k[s,t] and θ(s)=s+βt,θ(t)=βs+t. Its determinant is1−β², so θ is a graded automorphism. Put f⋆g=f θ^m(g) for homogeneous f of degree m. Then

(f⋆g)⋆h=fθ^m(g)θ^(m+n)(h)=f⋆(g⋆h).

The degree-zero1 is a unit. Highest homogeneous components show that B=(S,⋆) is a domain. Further, S_n⋆S1 spans S_n θ^n(S1)=S_(n+1), so s,t generate B in degree 1. Expanding the four quadratic products proves βs⋆s−s⋆t+t⋆s−βt⋆t=0. Hence A surjects onto B. Both have graded dimensions n+1, by the independent normal basis above and ordinary polynomial sections respectively. This surjection is therefore an isomorphism in every degree and globally.

The invertible matrix [[1,β],[β,1]] induces the genuine projective automorphism σ[s:t]=[s+βt:βs+t] over any field. Pulling back a linear coordinate section gives θ, not θ^−1. Compatible identifications of L_n=⊗_(i=0)^(n−1)σ^(i*)O(1) with O(n) turn the declared section product f⊗(σ^m)*g into exactly fθ^m(g). Choosing the displayed linear lift is legitimate; rescaling a lift by λ changes these graded identifications by powers λ^(n(n−1)/2) and does not change the THCR isomorphism class. Global sections here are homogeneous polynomials as a scheme construction, not functions on the finite set of k-rational points.

Finally L_n≅O(n). Serre vanishing on projective space makes O(1) σ-ample for this invariant polarization. Equivalently on P1, a coherent sheaf has a finite surjection from a sum of O(−d_i), and H1(O(n−d_i)) vanishes for n sufficiently large; dimension1 removes any H2 obstruction. No algebraic closure, rational-point density or infinite-order dynamical hypothesis is needed for this elementary case. The positive-pullback multiplication and σ-ampleness convention are explicitly confirmed in the actual RZ-v2 primary, section 3, printed page7.

## Nontrivial prime and growth

The defining ideal J of R is homogeneous and generated in degree 2, so J∩F4_1=0. In particular x3−x1≠0 in R, including characteristic2. The homogeneous two-sided ideal I lies in R+. Its exact quotient sends x1 to the nonzero section s, so x1∉I and I⊊R+. Thus0≠I⊊R+. Since R/I≅B is a domain, I is completely prime, hence ordinary two-sided prime and graded prime.

The quotient dimensions n+1 give Hilbert series Σ(n+1)z^n=(1−z)^−2 and cumulative growth (n+1)(n+2)/2. With degree-one finite generation, GK dimension is exactly2. It is a positive-dimensional projective-curve image, not an augmentation or a finite-dimensional image.

## Boundaries and source categories

At β=0 the quotient is k[X,Y] and σ=id. At β=1 the relation is (X+Y)(X−Y); at β=−1 it is−(X−Y)(X+Y). The factors are nonzero in A1 because the ideal is generated in degree 2, so these excluded quotients have zero divisors. In characteristic2 the factors coincide and give a nonzero square-zero linear class. The condition β²≠1 is therefore substantive.

In characteristic≠2, P=X+Y,N=X−Y gives the classical quantum-plane relation PN=((1−β)/(1+β))NP. This is an independent sign check, not the all-characteristic proof. In characteristic2 that diagonalization degenerates; the unitriangular/operator proof remains valid.

Algebraically independent α,β over the prime subfield satisfy β²≠1. For the journal's geometric parameters, c=(ϑ−1)/(ϑ+1),d=(ρ−1)/(ρ+1) are invertible birational substitutions in characteristic≠2. In characteristic2 both fractions collapse to1 where defined, so the note properly does not identify independent c,d there with the generic geometric family or transfer its noetherianity/GK results. The full all-field result concerns the literal six-relation presentation. A lower-dimensional quotient does not contradict the separate same-graded-quotient-ring obstruction for a surface algebra. The negative answers concern the actual broad printed prime/no-map assertions, which impose no injective/birational/image-dimension condition.

No remaining in-scope mathematical gap was found. The primary/priority limits remain part of the conclusion: classical machinery is credited, no global prime classification or historical firstness is certified, and no new repair or narrowed target has been substituted.
