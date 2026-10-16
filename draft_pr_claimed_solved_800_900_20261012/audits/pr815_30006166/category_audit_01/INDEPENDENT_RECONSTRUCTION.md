# Independent reconstruction before prior verdicts

Timestamp: 2026-10-13 05:37:27 UTC. Exact candidate head supplied by parent: `5bee5139501a399da653f634147eab9433774ac7`.

Inputs read so far: `source/author/PROOF.md` and `source/author/SOURCES.json`, then a fresh primary CJMST web rendering. No prior review verdict has been read. This document records my independent derivation before any such reading.

## Exact claim and audit scope

For the restricted wreath product W=(direct sum over Z of Z) semidirect Z and chi:W->Z, the candidate claims a comeager set in all continuous Cantor actions with hyperfinite entire-space orbit relation. The proposed mechanism is existence of a continuous chi-equivariant profinite-integer height, followed by a Borel slab exhaustion. The topology/category family is the central focus of this independent audit.

## Category reconstruction

Let C be a compact perfect metrizable zero-dimensional space. Homeo(C), with uniform convergence of both maps and inverses, is Polish. Composition and inversion are continuous. Thus the equations alpha(gh)=alpha(g)alpha(h), for countably many pairs g,h in W, and alpha(e)=id cut out a closed Polish subspace in Homeo(C)^W. It is nonempty (the trivial action) and Baire.

For c:C->Z/m continuous, the equivariance conditions for a and t are clopen. The finite c-fibers are separated clopen sets, so the output label map c composed with a homeomorphism is locally constant in the uniform topology. A label inequality at one point is similarly stable. These generator conditions imply all W conditions by composition and inversion. For each finite target there are countably many continuous maps: countably many clopen sets, hence countably many finite fiber tuples.

For m dividing n, fix alpha with finite height c. The fiber product Y={(x,j):c(x)=j mod m} has the exact W action (x,j)->(alpha(g)x,j+chi(g)); all group laws and invariance of Y follow from alpha's equivariance. It is a nonempty Cantor space, including the case n=m. Choose an action neighborhood determined by a finite symmetric F, uniform errors, and a finite clopen Q of sufficiently small mesh. Refine Q, alpha(g)^(-1)Q for g in F, and c-fibers to P. For each nonempty P-atom A, Y_A is a finite union of nonempty Cantor spaces, hence a Cantor space homeomorphic to A. A piecewise homeomorphism h:A->Y_A preserves first-coordinate membership in A.

For beta=h^(-1)gamma h and x, write h(x)=(u,j). Then u,x share a P-atom, so alpha(g)u,alpha(g)x share a Q-atom. beta(g)x and alpha(g)u share a P-atom, and hence a Q-atom. This gives the demanded error without any false pointwise first-coordinate identity. Including inverses in F handles the inverse topology. The second coordinate d of h obeys d mod m=c and exact n-equivariance. This is an actual action approximation in every original-action neighborhood, rather than an approximate representation.

Consequently U(c;m,n)=(A\D(c,m)) union the D(d,n)'s with d mod m=c is open dense. Countable intersection over every c and every divisibility pair is comeager. For a fixed alpha in this intersection, its universal c conditions remain available when its successive c's are chosen adaptively. Starting at modulus 1 and lifting through factorial moduli constructs compatible finite maps. Their product is a continuous p:C->lim Z/n!, hence p:C->Zhat. Equivariance holds coordinatewise. Compact image, nonemptiness, and invariance under plus and minus 1 force surjectivity by density of the integers. No measurable dependence on alpha is required.

This establishes the proposed generic-factor theorem, subject only to the standard Cantor-space classification and Polish-homeomorphism facts; no gap has appeared in its internal construction.

## Bridge reconstruction and exact dependency checks still pending

At modulus m, the residue gives the Borel bijection B_m x {0,...,m-1}->X, (z,r)->t^r z, with B_m={p mod m=0}. A lamp move at level r becomes a_{-r} on B_m and an uncut t move changes r only. Thus the slab graph uses a finite-rank lamp action K_m=Z^m. If arbitrary K_m actions have finite Borel asymptotic dimension (not just free actions), a coloring transferred constantly along levels proves the slab metric has finite Borel asymptotic dimension. The dimensions may depend on m, which is harmless only if the compatible-union theorem really allows unbounded dimension.

For factorial m, cut positions are nested, so graph metrics decrease. On p^(-1)(Zhat\Z), every generator edge eventually appears: an edge permanently excluded at x would give p(x)=-1, and the regular set is invariant. This gives orbit-relation exhaustion by the slab metrics. The needed theorem must require bounded distances at one stage to stay bounded at the next, with no uniform dimension bound or reverse coarse control. Fresh full-statement verification is pending.

The exceptional invariant preimage of embedded Z has an integer height h and a normalizing q(x)=t^(-h(x))x in B=p^(-1)(0). The orbit relation pulls back E_N via q. A plain pullback of finite relations would have infinite classes. The displayed band |h|<=j fixes this: every q-fiber has exactly one point per integer height, and resulting finite classes have size at most (2j+1) times the original finite class size. This part is internally valid if the cited arbitrary-action hyperfiniteness of countable N is correct.

## Immediate attempted contradictions

Profinite factors prohibit t-periodic points and topological weak mixing, but genericity in all actions does not imply genericity in a closed minimal or measure-preserving subspace. A robust invariant clopen partition in an arbitrary action neighborhood can be replicated on each finer cyclic-height slice by the fiber-product construction. Compactness would obstruct an increasing exhaustion by finite relations with open edge membership; here only Borel finite relations are claimed. Neither gives a contradiction at present.

Strongest verified result at this checkpoint: the entire category/topology argument reconstructs correctly. Exact remaining gap: primary verification of the arbitrary-action finite-asymptotic-dimension and compatible-union inputs and of the original problem's quantifiers.

Audit completion estimate: 45%.
