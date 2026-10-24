# A common-centralizer metric filter for candidate eligibility

October24,2026 UTC. Supporting deduction from the standard minset and flat-torus theorems, following the mechanism in Delage2602.08759v3, §§2.2 and3. **No originality or complete Kourovka solution is claimed.** This filter rejects ineligible non-CAT(0) candidates; it is not an obstruction to virtual RAAG embedding for a genuine CAT(0) group. Fresh review is pending.

## Exact family and success criterion

Let F=F(x_1,...,x_r), r≥1, let k≥0, and let w_1,...,w_k∈F. Consider

    G=<F,t,c_1,...,c_k | [t,x_j]=1, c_i^-1 t c_i=t w_i>.

This is a finite-rank free-by-cyclic group: rewriting the latter relations gives t c_i t^-1=c_i w_i, while t fixes every x_j. The displayed substitution fixes F and sends c_i to c_i w_i, an automorphism of the free group on the r+k displayed fiber generators (inverse sends c_i to c_i w_i^-1). Thus the base F×<t> and its rank-two free abelian subgroups <u,t>, u∈F nontrivial, genuinely inject. The empty family k=0 and the case of all trivial w_i give the RAAG F_(r+k)×Z; these are not excluded.

Assume G has a **proper action by semisimple isometries** on a CAT(0) space. In particular this applies to an eligible geometric CAT(0) action in the Notebook. We derive necessary conditions only. A negative virtual-specialness claim for21.124 cannot use a group failing these conditions as its CAT(0) example.

## One common signed translation character

Because t has infinite order and the action is proper and semisimple, it is hyperbolic. Write its length as ell>0 and its minset as C×R, with t acting by (identity,+ell). Every element of F centralizes t, so preserves this splitting and acts by an isometry of C and a translation of R. The signed R-displacement is therefore a single homomorphism

    lambda:F→R.

For each nontrivial u∈F, its induced isometry of C is semisimple with **strictly positive** translation length d(u). To justify strictness, restrict the proper semisimple action to <u,t>≅Z². The flat-torus theorem gives a Euclidean plane on which u,t act by an injective lattice of translations. If d(u)=0, their translation vectors would be parallel; an independent rank-two group cannot act properly by translations on a line. Equivalently the associated transverse translation vector in that plane is nonzero. This step uses the independence of u and t, not just u≠1.

Conjugate elements have equal translation length. The defining relation makes t w_i conjugate to t. The product metric on C×R therefore gives, for every nontrivial twist word,

    d(w_i)^2+(ell+lambda(w_i))^2=ell^2.

In particular,

    -2ell < lambda(w_i) < 0.                 (1)

The same character lambda must work for **all** twist words simultaneously. It factors through F_ab≅Z^r. Thus their nonzero abelianization vectors must lie in one common strict open halfspace. This is necessary, not sufficient.

## Exact certificates excluding CAT(0)

If there are nonnegative real coefficients z_i, not all zero, supported on nontrivial w_i, with

    sum_i z_i [w_i]_ab=0,

then applying lambda contradicts(1). Nonnegative rational or integer coefficients provide particularly simple checkable certificates. A single nontrivial word in F' is the one-term case. This recovers the prior Delage commutator-twist exclusion and extends the same standard mechanism to simultaneous twists. Words equal to the identity must be omitted: a trivial twist imposes no strict inequality.

For example, the twists x_1,x_2,(x_1 x_2)^-1 have a positive dependence with coefficients(1,1,1). Their mapping torus cannot admit a proper semisimple CAT(0) action. The twists x_1,x_1^-1 give coefficients(1,1). These are eligibility exclusions, not counterexamples to the Notebook.

## A further commensurable-twist restriction

Suppose two nontrivial twist words have the form

    w_i=h_i u^n_i h_i^-1,
    w_j=h_j u^n_j h_j^-1,

with u∈F nontrivial, h_i,h_j∈F, and signed nonzero integers n_i,n_j. Since lambda is a homomorphism and the C-actions are conjugate, their displacement data are

    lambda(w_i)=n_i lambda(u),
    d(w_i)=|n_i| d(u),

and similarly for j. Set D=d(u)^2+lambda(u)^2>0. Expanding the common norm equation and dividing by the signed nonzero exponent gives

    n_i D+2ell lambda(u)=0,
    n_j D+2ell lambda(u)=0.

Hence **n_i=n_j**. Distinct oriented powers in the same F-conjugacy family cannot occur among the twists of an eligible action. No choice of powers of t or alteration of the ambient CAT(0) space removes this necessary length equality for the original group.

The standard Gersten pair w_1=x_1,w_2=x_1² violates this restriction. It passes the weaker halfspace test (choose lambda(x_1)<0), explicitly showing that the halfspace test alone is insufficient. This is a rederivation of a familiar non-CAT(0) obstruction, not a new solution.

## Limits and precise remaining gap

The filter assumes a common fixed free subgroup F centralized by t. It cannot be applied to the abelianization of an arbitrary larger free fiber that is **not** fixed by t. For example, when an automorphism fixes a and sends b to b a^k, the fixed subgroup containing a and b a b^-1 has a different abelianization from F(a,b). The word [a,b]=a(b a b^-1)^-1 can be nonzero in the fixed subgroup's abelianization although it is zero in F(a,b)_ab. Confusing these would wrongly reject the genuine CAT(0) examples in Delage's §4.

Satisfying these metric constraints supplies no RAAG embedding and does not certify CAT(0) by itself. A construction must still provide a geometric action, and a negative solution must still exclude every finite-index RAAG embedding. No such full conclusion follows here.

Primary source for the established geometric input and rank-three antecedent: L.Delage, *Which F3-by-Zs are CAT(0)?*, arXiv:2602.08759v3, §§2.2,2.3 and Proposition3.1, https://arxiv.org/html/2602.08759v3 . Delage cites Bridson–Haefliger for the general minset/flat-torus facts. This note does not claim the simultaneous elementary consequences have no prior appearance.
