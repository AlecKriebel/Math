# Weak Artin–Schreier condition: exact orbit-field reductions

**Status: accepted scoped partial result after independent AI mathematical audit.** This note does not establish the weak-to-strong bridge.

## Setting

Let k be algebraically closed of characteristic p>0. Let sigma be a k-automorphism of k[[t]] of exact order N=p^n, n>=2. Suppose sigma(t) belongs to a cyclic Artin–Schreier extension E/k(t) of degree p inside k((t)). Put t_i=sigma^i(t), indexed modulo N, and L=k(t_i: i in Z). All assertions below concern this weak hypothesis alone. In particular, sigma(E)=E is NOT assumed.

## Theorem 1. The orbit extension is Galois of p-power degree
There is an integer 1<=r<=N-1 such that:
(a) [L:k(t_i)]=p^r for every i;
(b) for every interval [a,b] of length ell=b-a+1<=r+1, the field K[a,b]=k(t_a,...,t_b) has degree p^(ell-1) over every k(t_j) with a<=j<=b;
(c) L/K[a,b] is Galois for every such nonempty interval;
(d) in particular, L/k(t_i) is Galois of degree p^r;
(e) k(t_i,t_(i+1)) is cyclic Galois of degree p over EACH of its two rational coordinate subfields.

### Proof
First, t_1 is not in k(t_0). If it were, sigma restricted to k(t_0) would be an automorphism: the finite-order inclusion sigma(k(t_0)) subset k(t_0) must be equality. Its order is still N because it acts on the generator t_0, contradicting the fact that a p-power torsion element of PGL_2(k) has order at most p. Therefore E=k(t_0,t_1).

Let F_m=k(t_0,...,t_m). The extension F_m/F_(m-1) is obtained by base-changing the cyclic degree-p extension sigma^(m-1)(E)/k(t_(m-1)). It is therefore trivial or cyclic of degree p. If F_m=F_(m-1), then sigma(F_(m-1))=k(t_1,...,t_m) is contained in F_(m-1); since sigma has finite order, this inclusion is equality. Consequently F_(m-1)=L and all subsequent steps are trivial. Define r so that the first r steps have degree p and F_r=L. Then [L:k(t_0)]=p^r. Since sigma acts on L, [L:k(t_i)]=p^r for every i. A shift of an interval gives its forward degree p^(ell-1), and comparison of its index in L with [L:k(t_j)]=p^r gives the same degree over each coordinate field within that interval. This proves (a) and (b).

An elementary intersection calculation will be used for descent. Whenever ell<=r-1, let A=K[a-1,b], B=K[a,b+1], and C=K[a,b], where b-a+1=ell. Both A/C and B/C have degree p, while their compositum K[a-1,b+1] has degree p^2 over C by (b). Hence A and B are distinct and A intersect B=C: an intermediate field of the prime-degree extension A/C is either C or A, and the second case would force A=B.

For every interval of length r, L/K[a,b] is cyclic of degree p, by shifting the last nontrivial forward step. Suppose inductively that L/K[a,b] is Galois for every interval of length ell+1, with ell<r. For C, A, B as in the preceding paragraph, Gal(L/A) and Gal(L/B) are finite groups of automorphisms fixing C. The subgroup they generate remains finite because it lies in Aut(L/C), whose order is at most [L:C]. Its fixed field is A intersect B=C. Artin's fixed-field theorem therefore proves L/C Galois. Descending to ell=1 proves (c) and (d).

Finally, k(t_i,t_(i+1)) has degree p over each coordinate field by (b). As a degree-p intermediate extension of the Galois p-extension L/k(t_j), it is Galois: its corresponding subgroup has index p in a finite p-group and is normal. Its group is cyclic of order p. This proves (e).

**Important logical distinction.** Equal degrees of the two projections alone do NOT prove that the reverse projection is Galois when p>2. The descent above is needed for that conclusion.

## Corollary 2. Geometric and group description
Let X have function field L, and let x be the place induced by L subset k((t)). The valuation of t at x is 1, so t is a local parameter; sigma fixes x and acts there with its original order N. For H_i=Gal(L/k(t_i)), |H_i|=p^r, the quotient X/H_i is rational, and H_i acts freely at x. For ell<=r+1,
  |H_a intersect ... intersect H_b|=p^(r-ell+1).
In particular neighboring H_i meet in index p, while any r+1 consecutive H_i have trivial intersection.

The neighboring pair field E_i=k(t_i,t_(i+1)) is the function field of a curve with two distinct cyclic-p rational quotients. It has genus at most (p-1)^2. The quotients are distinct, since equality of their rational fixed fields would make t_(i+1) a rational function of t_i and contradict the order assumption. The two quotient groups act freely at the distinguished place of E_i.

These statements do not imply that the H_i are equal, that sigma(E_i)=E_i, or that r=1. The desired weak-to-strong bridge is exactly the assertion r=1.

## Corollary 3. Genus bound for the whole orbit field
  g(L) <= 1 + p^r (r(p-1)-1).
Indeed, put g_m=g(F_m). Apply Castelnuovo–Severi to the generating subfields F_(m-1) and k(t_m) of F_m. Their respective indices in F_m are p and p^m, and the second subfield is rational. Thus
  g_m <= p g_(m-1) + (p-1)(p^m-1),   g_0=0.
Induction yields g_m <= 1+p^m(m(p-1)-1), including the stated bound at m=r.

## Corollary 4. Ramification obstruction to a small orbit field
For every nonidentity sigma^j,
  v_x(t_j-t_0) <= 2p^r.
The function t_j-t_0 is nonzero, and its pole divisor has degree at most deg(t_j)+deg(t_0)=2p^r. Its order of vanishing at x is bounded by the total degree of its zero divisor.

Write b_(n-1) for the final lower break of <sigma>, so v_x(sigma^(p^(n-1))(t)-t)=b_(n-1)+1. The standard cyclic p^n lower-break bound is
  b_(n-1) >= (p^(2n-1)+1)/(p+1).
For completeness, upper breaks u_j satisfy u_0>=1 and u_j>=p u_(j-1). Hence the successive increments in the Hasse–Arf expression for lower breaks are at least (p-1)p^(j-1), giving the displayed bound. These ramification facts are also stated in Section 3.D of Bleher–Chinburg–Poonen–Symonds, [Automorphisms of Harbater–Katz–Gabber curves](https://doi.org/10.1007/s00208-016-1490-2), Section 3.D.
Therefore
  (p^(2n-1)+1)/(p+1) + 1 <= 2p^r.
In particular r>=2n-2 for p>=3, and r>=2n-3 for p=2. For r=1 this already forces (p,n)=(2,2), but it does not rule out r>1.

## Remaining gap

These are structural reductions, not a proof of weak implies strong and not a counterexample. In particular, the strong whole-orbit classification cannot be applied until r=1 is established independently.

## Scope of the source citation

The cited paper supplies the standard ramification inequalities used in Corollary 4. The orbit-field argument in Theorem 1 is proved above; no weak-to-strong implication is being attributed to the cited classification. The weak hypothesis enters through the single adjacent cyclic Artin–Schreier extension, whereas the strong hypothesis would already require that the entire orbit lie in that extension.
