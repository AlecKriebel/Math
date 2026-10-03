# Attempt 1: construct every irreducible character, and locate the counting gap

## Scope and notation

Let Gamma=(V,E) be a finite simple graph, with n vertices and m edges. Fix an ordering of V. For an odd prime power q, put U=F_q^V and W=F_q^E. Define the alternating bilinear map beta:U x U -> W by

beta(v,v')_{jk}=v_j v'_k-v_k v'_j, for {j,k} in E, j<k.

Give U x W the multiplication

(v,w)(v',w')=(v+v',w+w'+beta(v,v')/2).

Bilinearity proves associativity directly. Inverses are (-v,-w); commutators are (0,beta(v,v')); and (v,w)^a=(av,aw) for integers a. Thus, when q=p is prime, this is the class-at-most-two, exponent-dividing-p graph group in the primary question. Indeed its indicated vertex generators have the required relations, generate W through their edge commutators, and generate the whole group. Conversely those relations collect every word into at most p^(n+m) normal forms, proving that the presentation and this model agree. Isolated vertices and the edgeless case are included; “class two” is not asserted when the group is abelian.

Write B_Gamma(y) for the n by n alternating matrix having entry y_{jk} in position (j,k) for an edge j<k and zero at nonedges. Set

N_i(Gamma;q)=#{y in F_q^E : rank B_Gamma(y)=2i}.

The subscript i is HALF the matrix rank throughout this packet.

## Complete character construction

Fix a nontrivial additive character psi:F_q -> C^*. For lambda in W^*, let b_lambda=lambda o beta, and write R_lambda=rad(b_lambda). Suppose rank b_lambda=2i. Choose a symplectic decomposition

U=R_lambda direct-sum X direct-sum Y,

where X and Y have dimension i and b_lambda((x,y),(x',y'))=x dot y'-y dot x'. This decomposition follows by repeatedly choosing a pair with nonzero pairing, rescaling it to pairing 1, splitting its two-dimensional nondegenerate span orthogonally, and continuing. The radical is the remaining zero-form subspace.

For each mu in R_lambda^*, define a representation on complex-valued functions f on F_q^i by

[rho_{lambda,mu}(r+x+y,w)f](t)
 =psi(mu(r)+lambda(w)+y dot t+(x dot y)/2) f(t+x).

Multiplying two such operators produces the extra term x dot y', which is exactly the sum of the half-commutator term and the cross terms in (x+x') dot (y+y')/2. This proves the representation identity, including the signs. The trace of a nontrivial translation is zero. When x=0 but y is nonzero, summing psi(y dot t) over t also gives zero. Consequently its character is

chi_{lambda,mu}(v,w) = q^i psi(mu(v)+lambda(w)), if v is in R_lambda,
                       0, otherwise.                              (1)

Here mu(v) is used only when v belongs to R_lambda. Its character norm is

(1/q^(n+m)) q^(n-2i+m) q^(2i)=1.

Thus rho is irreducible. Characters with different lambda are orthogonal by summation over w; for equal lambda and different mu they are orthogonal by summation over R_lambda. All additive characters of an F_q vector space arise uniquely as psi composed with an F_q-linear functional: the map is injective because every nonzero functional is onto F_q, and both sets have the same cardinality. This justifies the indexing, also for nonprime q.

There are q^(n-2i) choices of mu for a fixed rank-2i lambda. The sum of the squared degrees of the constructed, pairwise inequivalent irreducibles is

sum_lambda q^(n-2i(lambda)) q^(2i(lambda)) = q^(n+m).

The usual decomposition of the regular complex representation now proves completeness. This uses only the basic finite-group facts that a character of norm one is irreducible and that the sum of squared irreducible degrees is the group order.

Therefore

ch(Gamma,i;q)=q^(n-2i) N_i(Gamma;q).                        (2)

In particular, N_0=1 and ch(Gamma,0;q)=q^n. The central subgroup W need not be the full centre; the construction deliberately keeps isolated-vertex directions in U, so no factor is lost.

## What this attempt does and does not settle

Formula (1) supplies every character for a specified finite field. Formula (2) gives the precise factor in the rank-count reduction already present in the primary source and in Rossmann's 2022 paper, §1.6. Neither is a resolution of the source's intended symbolic dependence on p: N_i still counts a rank stratum whose dependence on the field is unknown in general. An exhaustive finite-field algorithm is not being substituted for that question. No novelty is claimed for this standard class-two character construction.
