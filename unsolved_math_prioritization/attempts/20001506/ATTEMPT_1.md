# Turn 1: canonical cyclic covers and homological growth

Date: 2026-10-03. This is new mathematical work beyond the supplied prior report. The original quasi-isometry conjecture is not solved.

## Target and route

Use the exact map phi(a)=b, phi(b)=c, phi(c)=ab, phi(d)=ea, phi(e)=ed, with alpha its restriction to F(a,b,c). Can a computable homological distinction of their mapping tori force a quasi-isometry distinction?

With columns denoting images, the abelianization matrix is

    M = [0 0 1 1 0; 1 0 1 0 0; 0 1 0 0 0; 0 0 0 0 1; 0 0 0 1 1].

Its diagonal blocks are A=[0 0 1;1 0 1;0 1 0] and B=[0 1;1 1]. Thus

    det(xI-A)=x^3-x-1,
    det(xI-M)=(x^3-x-1)(x^2-x-1).

## Exact results

For every positive n, write Gamma_n=F3 semidirect_{alpha^n} Z and G_n=F5 semidirect_{phi^n} Z. These are the index-n covers defined by the displayed height maps. Abelianizing the presentations gives

    H1(Gamma_n;Z)=Z plus coker(A^n-I),
    H1(G_n;Z)=Z plus coker(M^n-I).

No eigenvalue of either A or B has modulus one. For A, the cubic has exactly one real root rho>1: both local extrema are negative, and the other two roots are conjugate with product 1/rho, hence modulus rho^(-1/2)<1. For B, the roots are tau=(1+sqrt(5))/2 and -1/tau. Therefore both cokernels are finite, and b1(Gamma_n)=b1(G_n)=1 for every n.

In particular det(A-I)=-det(I-A)=1 and |det(M-I)|=1, so H1(Gamma;Z)=H1(G;Z)=Z, with no torsion. Every epimorphism to Z is the displayed height map or its negative. The two groups have canonical cyclic towers as abstract groups, although no claim of quasi-isometric canonicity follows.

The torsion orders obey the exact identity

    |Tor H1(G_n)| / |Tor H1(Gamma_n)| = |det(B^n-I)|
      = |(tau^n-1)((-tau^(-1))^n-1)|.

For n=1,...,8 the ratios are 1,1,4,5,11,16,29,45. Their logarithmic exponential growth rates are log(rho) and log(rho)+log(tau), respectively. This follows directly by factoring the determinants over the complex roots; all non-dominant factors tend in absolute value to one.

A further consequence is useful for a periodic-conjugacy search: if phi^n(w) is conjugate to w, then the abelianization of w lies in ker(M^n-I), which is zero. Hence every nontrivial periodic conjugacy class, if one exists, belongs to [F5,F5]. The analogous statement holds for alpha.

## Why this does not finish the target

The computed towers are canonical under isomorphism, not known to be transported by an arbitrary quasi-isometry. Neither first homology nor these torsion-growth sequences are, by this calculation, quasi-isometry invariants. Both groups even have the same first Betti number in every displayed cyclic cover. Thus the attempted homological route supplies an exact obstruction/filter but no QI proof.

## Verification

The dependency-free verify.py recomputes the matrices, verifies the inverse of phi in both directions, checks characteristic-polynomial evaluations and all torsion ratios for n=1,...,20 using exact integer determinants. checks_turn1.json records the finite checks; the all-n assertions are proved above, not extrapolated from them. Prior work already contained the inverse and transition blocks; their replay here is a control, not a claim of novelty or a separate turn.
