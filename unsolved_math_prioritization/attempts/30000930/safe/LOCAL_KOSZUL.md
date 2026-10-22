# Direct local Koszul composition and its limit

This approach attempts to compute mixed products on explicit resolutions rather than reconstructing them from global module structures and duality.

Let R=C[z,w,x,y], A0=Spec R/(w,y), and B0=Spec R/(w,x). These are cleanly intersecting Lagrangian affine planes for the symplectic form dz∧dw+dx∧dy, and C0=A0∩B0 is the z-axis. This is an exact local model, not an asserted global splitting of the Springer neighborhood.

Use the Koszul resolution K_A in degrees −2,−1,0 with differentials

d_A^(−2)=(-y,w)^T, d_A^(−1)=(w,y),

and similarly K_B with

d_B^(−2)=(-x,w)^T, d_B^(−1)=(w,x).

After applying Hom(K_A,R/(w,x)), the differential is given by y in the remaining transverse direction. Its degree-1 and degree-2 cohomology are both C[z]. A generator of degree 1 lifts to the degree-1 closed map f:K_A→K_B whose only nonzero components are

f^(−1)=(0,1), f^(−2)=(-1,0)^T.

Indeed d_B f+f d_A=0, since the only potentially nonzero component is −w+w. Similarly a generator of Ext1(B0,A0) lifts to g with the identical two matrices, now in the reverse direction. Both degree-2 compositions are strictly zero:

g f=(0,1)(-1,0)^T=0,
f g=(0,1)(-1,0)^T=0.

The verifier checks the Koszul identities, both closed-map identities, and both zero compositions over an exact polynomial ring.

This is not a global vanishing theorem. The global k=2 calculation in K2_YONEDA.md forces the mixed degree-1 compositions to be nonzero in self-Ext2. There is no contradiction: in the self-Ext local-to-global filtration on a projective component A, the degree-2 group comes from H1(A,Ω_A^1), while the degree-0 sheaf-cohomology contribution H0(A,Ω_A^2) is zero. A product whose leading local associated-graded term vanishes can lie in a higher filtration piece. Local representatives and their chosen lifts need not glue with zero correction; Čech homotopies may contribute the nonzero global product.

Thus a naive multiplication of local sheaf-Ext generators misses precisely the global information needed. The attempted all-k proof by local Koszul products stops at the uncomputed gluing terms for triple compositions. We have not constructed a compatible global Čech resolution or proved these corrections agree with all weighted arc surgeries. This is a diagnostic partial calculation, not a false global counterexample.
