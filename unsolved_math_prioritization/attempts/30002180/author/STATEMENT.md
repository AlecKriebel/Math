# Exact scope and conventions

The matching source is Simone Diverio's contribution, “Rational curves on Calabi-Yau threefolds and a conjecture of Oguiso,” in Oberwolfach Report 43/2012. Printed p. 2612 fixes X to be compact projective over C and introduces a Kähler metric; printed p. 2613 gives the jet definition and question. The surrounding discussion highlights threefolds, but the displayed jet question is not explicitly restricted to dimension three. We study the ordinary positive-dimensional interpretation, n=dim_C X >=1.

Build X_0=X and V_0=T_X. For j>=1 let X_j=P(V_{j-1}), using the convention that P parametrizes lines, and let pi_j:X_j→X_{j-1}. The tautological line is L_j=O_{X_j}(-1)⊂pi_j^*V_{j-1}. Define V_j=(d pi_j)^(-1)(L_j)⊂T_{X_j}. Thus rank V_j=n while dim X_j=n+j(n-1). Write L_j^*=O_{X_j}(1), u_j=c1(L_j^*), and pi_{j,0} for the composite projection.

Let J_k X be curve k-jets and G_k invertible changes of the curve parameter. The regular locus X_k^reg identifies with J_k^reg X/G_k, where the first derivative is nonzero. The excluded boundary is X_k^sing=X_k\X_k^reg; it is not a singularity of the smooth manifold X_k.

The hypothesis is a singular Hermitian metric h on L_k, locally represented with the usual quasi-plurisubharmonic weight convention, whose degeneration locus Sigma_h lies in X_k^sing. For the dual curvature current alpha=Theta_{h^-1}(L_k^*), normalized to represent c1(L_k^*), there are epsilon>0 and a smooth Hermitian form omega_k such that

alpha(xi,bar xi)>=epsilon omega_k(xi,bar xi) for xi in V_k,

in the distributional sense. This is negative curvature of L_k, equivalently positive curvature of its dual on V_k. Negativity on all of T_{X_k} is the different, stronger **total** jet condition. Neither smoothness of h nor its origin from a base Kähler metric is assumed. Local boundedness away from Sigma_h is sufficient for the restriction arguments used below.

Target: prove c1(T_X)_R≠0 in H^2(X,R). This is not a demand for a nowhere-zero curvature form, a sign for every canonical intersection, canonical bigness, or canonical ampleness. A nonzero torsion integral c1 still maps to zero over R and must not be mistaken for the desired nonvanishing; on a compact manifold, nonzero real c1 is equivalent to the integral class being non-torsion. Since c1(K_X)=-c1(T_X), a nonzero real canonical class would suffice. Every argument that assumes ampleness or bigness labels that added hypothesis. We never equate the tower class u_k with a pullback of c1(T_X).

Projectivity implies compact Kählerness here. Some retained lemmas work for compact Kähler manifolds, and the torus lemma works for compact complex tori, but these extensions do not change the original scope. No proper directed subbundle V⊊T_X is substituted in the target.
