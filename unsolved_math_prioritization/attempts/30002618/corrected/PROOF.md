# A residue–Gysin criterion for invariant-cycle exactness

## 1. Scope and conventions

Let V be a complete mixed-characteristic (0,p) discrete valuation ring, with perfect residue field k, uniformizer pi, and fraction field K. Put K0 = Frac W(k). Let X/V be a proper strictly semistable curve. Assume that its connected special fiber C has at least two smooth irreducible components C_v, that its nodes are k-rational, and that locally at a node the model is etale over xy = pi. Let E be a convergent F-isocrystal on the scheme C **without** a log structure. Equip C with the semistable log structure only to form its associated log coefficient and Hyodo–Kato cohomology.

All vector spaces below are over K, after extension of scalars from K0 where necessary. Write

    H = H^1_dR(X_K, E),
    S = H^1_rig(C, E) tensor_(K0) K,
    i: S -> H,
    N: H -> H.

The log-crystalline/de Rham comparison identifies this with the sequence in the question after scalar extension. Faithful flatness of K/K0 means that exactness can be tested here. We forget Frobenius in these linear-algebra statements: the Frobenius-compatible monodromy map has target Tate-twisted by (-1). In particular the assertions below do not claim that untwisted N is Frobenius equivariant.

Choose one orientation for each geometric edge of the dual graph. No edge is counted twice. Denote the corresponding node by P_e and its annular tube in X_K by X_e. Let X_v be the standard component wide open. Restriction and the isocrystal identifications at the node identify

    F_e = H^0_rig(P_e,E) tensor K = H^0_dR(X_e,E).

Put U_v = C_v minus its nodes. Use the usual comparison between H^1_rig(U_v,E) tensor K and H^1_dR(X_v,E).

The imported inputs are the component Gysin exact sequence of Chiarellotto–Le Stum [2, Proposition 2.1.4], and the comparison, Mayer–Vietoris, monodromy factorization, and zero-residue characterization in Chiarellotto–Coleman–Di Proietto–Iovita [1, Sections 2–4, Proposition 1, Lemmas 4 and 7]. These inputs are applied only with their proper/smooth-component and no-log coefficient hypotheses. On the proper smooth component C_v, the convergent coefficient is also overconvergent. Since C is connected with at least two components, each C_v meets a node; hence U_v is a nonempty affine open, as required by [2, Proposition 2.1.4].

## 2. The two finite-dimensional maps

Define

    C0(E) = direct sum_v H^0_rig(C_v,E) tensor K,
    C1(E) = direct sum_e F_e,
    C2(E) = direct sum_v H^2_rig(C_v,E) tensor K.

For an edge e directed from v to w, define

    (A a)_e = a_v|P_e - a_w|P_e.

The two restrictions are compared in the same node fiber F_e. The degree-zero Gysin isomorphism identifies these component sections with H^0_dR(X_v,E), so this is also the Mayer–Vietoris incidence map.

For a node incident to v, let

    g_(v,e): F_e -> H^2_rig(C_v,E) tensor K

be its Gysin map. Tate twists are suppressed only on underlying vector spaces. Set epsilon(v,e)=+1 at the tail and -1 at the head, and define

    (D r)_v = sum_(e incident to v) epsilon(v,e) g_(v,e)(r_e).

Thus D includes coefficient identifications and the component Gysin maps. In general D is **not** the transpose of A, and DA is not a chain-complex differential. In particular, DA is not assumed to vanish.

Let q: C1(E) -> coker(A) be the quotient. Mayer–Vietoris gives an injection

    j: coker(A) -> H.

For h in H, restrict to H^1_dR(X_v,E) and take the residue at each oriented annulus, using the outgoing annular orientation at the tail. This defines a K-linear map

    R: H -> C1(E).

Residues of exact connection forms vanish because E has a horizontal basis on each node annulus. Therefore this definition is independent of the hypercocycle representative. On a shared annulus, the representatives differ by an exact connection form, so the two outward residues have opposite signs in the common node fiber.

With these conventions, the known residue description says

    N = j q R,                 ker(R) = im(i).

A simultaneous change of the conventional sign of N does not change any assertion about its kernel.

## 3. Exactness defect theorem

**Theorem.** Under the hypotheses of Section 1, there is an isomorphism induced by R

    ker(N) / im(i)  ~=  im(A) intersect ker(D).

Consequently

    dim(ker(N) / im(i)) = rank(A) - rank(DA),

and the invariant-cycle sequence is exact if and only if rank(DA)=rank(A).

**Proof.** We first verify the non-formal identification im(R)=ker(D). For each v the Gysin sequence, after scalar extension, is exact at its node-fiber term:

    H^1_rig(U_v,E) tensor K
      -> direct sum_(e incident to v) F_e
      -> H^2_rig(C_v,E) tensor K.

The second arrow is the sum of the node Gysin maps. Given h in H, its component restrictions give the signed residues epsilon(v,e)R(h)_e. Exactness of this local sequence gives D R(h)=0.

Conversely take r in ker(D). At each component, local Gysin exactness supplies a cohomology class h_v in H^1_dR(X_v,E) whose outward residues are epsilon(v,e)r_e. On any common annulus the two local classes have equal residues when written with the same annular orientation. The residue map

    H^1_dR(X_e,E) -> F_e

is an isomorphism: E is trivial there and the ordinary annular de Rham cohomology is measured by residue. Hence the two restricted annular cohomology classes agree. The tuple (h_v) lies in the kernel of the Mayer–Vietoris difference map. Exactness of Mayer–Vietoris lifts it to h in H, and R(h)=r. Thus im(R)=ker(D).

Since j is injective, N(h)=0 if and only if qR(h)=0, equivalently R(h) belongs to im(A). Restricting R to ker(N) therefore has image im(A) intersect ker(D). Its kernel is ker(R)=im(i). The first isomorphism theorem gives the claimed isomorphism.

Finally, the restriction D|im(A) has image im(DA). Rank-nullity gives

    dim(im(A) intersect ker(D))
       = dim im(A) - dim im(DA)
       = rank(A) - rank(DA).

This proves every assertion. QED.

### Immediate consequences

1. If H^0_rig(C_v,E)=0 for every component, then A=0 and the sequence is exact.
2. The defect is additive under finite direct sums, because all spaces and maps in the formula are additive. Exactness therefore passes to a direct summand of an exact coefficient object.
3. For constant rank-r coefficients the maps are the scalar incidence matrix and its transpose, tensored with K^r. The rank equality follows from the ordinary graph Laplacian. One may prove it over the real numbers and extend the rational matrices to K. This reasoning does **not** apply to arbitrary p-adic coefficient matrices.

This theorem is a reduction to degree-zero/degree-two component data and node maps. It is not presented as a new intrinsic classification of all geometric or pure coefficient objects.

## 4. A complete cycle calculation under local triviality

Add the assumptions that the dual graph is an n-cycle, n>=3, and that the realization of E on every X_v is a trivial connection of rank r. This is an explicit additional restriction. It is not a consequence of being a convergent F-isocrystal. The component genera need not be zero.

Choose horizontal bases on consecutive component wide opens. Change those bases so the transition maps on the first n-1 edges are the identity. On the last edge the remaining identification is T in GL(W), W=K^r. The conjugacy class of T, up to inversion upon reversing the cycle, is the graph holonomy. The property proved below is unchanged by either operation.

In these bases, write a=(a_1,...,a_n) and r=(r_1,...,r_n). Then

    (Aa)_i = a_i-a_(i+1)        for i<n,
    (Aa)_n = a_n-T a_1.

For a trivial connection on a two-ended component wide open, the image of the two-residue map consists exactly of pairs whose sum is zero. This follows from the scalar component Gysin sequence: both rational-node Gysin maps are the degree-one point class; tensor with W. Consequently the residue-compatibility equations are

    r_i-r_(i-1)=0              for 2<=i<=n,
    r_1-T^(-1)r_n=0.

These equations can also be used directly instead of identifying C2(E). Thus

    ker(D) = { (t,...,t) : t in ker(T-I) }.

For completeness the use of scalar Gysin is justified by the local triviality assumption itself: a horizontal basis trivializes E on X_v, so its local de Rham complex is a direct sum of scalar complexes. The scalar residue theorem and its converse determine the residue image independently of any chosen basis in H^2_rig(C_v,E).

Now define

    L: W^n -> W/(I-T)W,
    L(r_1,...,r_n) = [r_1+...+r_n].

We claim ker(L)=im(A). Summing the displayed equations for A gives

    sum_i (Aa)_i = (I-T)a_1,

so im(A) is contained in ker(L). Conversely, if sum_i r_i=(I-T)a_1 for some a_1, set successively a_(i+1)=a_i-r_i for i<n. Then

    a_n-T a_1 = (I-T)a_1 - sum_(i<n)r_i = r_n,

so Aa=r. This proves the claim and also identifies coker(A) with W/(I-T)W.

For r=(t,...,t) in ker(D), L(r)=[nt]. Since the field has characteristic zero, n is invertible. Hence r lies in im(A) exactly when t belongs to im(T-I). Applying Section 3 proves:

**Cycle theorem.** Under the additional cycle/local-triviality hypotheses,

    ker(N)/im(i) ~= ker(T-I) intersect im(T-I),

and therefore

    defect(E) = dim ker((T-I)^2) - dim ker(T-I)
              = rank(T-I) - rank((T-I)^2).

The dimension identity follows from the surjective map

    T-I: ker((T-I)^2) -> ker(T-I) intersect im(T-I)

whose kernel is ker(T-I).

In Jordan form, the defect equals the number of Jordan blocks at eigenvalue 1 of size at least two, counted once per block. The statement does not require K to be algebraically closed: the generalized 1-eigenspace and its nilpotent Jordan decomposition are defined over K. Thus exactness holds precisely when eigenvalue 1 is semisimple, meaning that ker((T-I)^2)=ker(T-I). This condition is vacuous when 1 is not an eigenvalue. In particular:

- Rank-one coefficients satisfying these local hypotheses are exact.
- If T is unipotent, exactness holds if and only if T=I.
- A nontrivial Jordan block at an eigenvalue other than 1 contributes no defect.

These statements concern existing coefficient objects meeting the hypotheses. They do not assert that every arbitrarily prescribed matrix T admits a compatible Frobenius structure or isocrystal realization.

## 5. Symbolic checks and relation to the known example

For T=I, the right side of the cycle theorem vanishes.

For T equal to the 2x2 unipotent Jordan block with superdiagonal 1, put M=T-I. Then M has rank 1, M^2=0, and ker(M)=im(M) is the line generated by the first basis vector. The defect is exactly 1. For n=3, ker(A) has dimension 1, so rank(A)=5. The defect formula forces rank(DA)=4, agreeing with the rank of the coefficient-aware triangle Laplacian in [1, Appendix A]. This recovers a published failure mechanism; it is not a newly discovered counterexample.

For T=diag(1,2), M has rank 1 and M^2 has rank 1, so the defect is zero. For T a single size-three unipotent Jordan block, rank(M)=2 and rank(M^2)=1, so the defect is 1, not 2. For a direct sum of two size-two unipotent blocks, the defect is 2. These are exact symbolic consequences, not numerical evidence for the proof.

## References

[1] B. Chiarellotto, R. Coleman, V. Di Proietto, A. Iovita, *On a p-adic invariant cycles theorem*, J. reine angew. Math. 711 (2016), 55–74. DOI: https://doi.org/10.1515/crelle-2013-0117. Author-institution copy: https://www.research.unipd.it/handle/11577/3187169. Preprint: https://arxiv.org/abs/1207.7110.

[2] B. Chiarellotto, B. Le Stum, *F-isocristaux unipotents*, Compositio Mathematica 116 (1999), 81–110, Proposition 2.1.4. DOI: https://doi.org/10.1023/A:1000602824628.

[3] V. Di Proietto, *On a p-adic invariant cycles theorem*, contribution to *Algebraische Zahlentheorie*, Oberwolfach Reports 11 (2014), pp. 1790–1792, Questions 4 and 6. Report DOI: https://doi.org/10.4171/OWR/2014/32. Publisher: https://ems.press/journals/owr/articles/13102.
