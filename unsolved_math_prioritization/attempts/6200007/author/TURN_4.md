# Attempt 4: a finite-annulus cusp obstruction

The principal scoped result of this packet is Theorem 4.5 below. It obstructs
the finite-orbit annulus construction even though the exhibited action itself
has a classical hyperbolic realization. Its mechanism is closely related to
Azemar's finite-boundary analysis [A22, Lemma 3.10 and Proposition 3.11]. No
claim of historical novelty is made.

Use the annulus and chain conventions in Attempt 2. Let A be a symmetric
G-invariant annulus system with finitely many G-orbits for a convergence
action on a compact metrizable Z. A point p is conical if some sequence of
distinct group elements h_n and distinct u,v satisfy h_n p->v and
h_n x->u locally uniformly for x outside p.

## Lemma 4.1: uniform finiteness for two separated pairs

Suppose B_1,C_1,B_2,C_2 are compact subsets with B_i disjoint from C_i for
i=1,2. Only finitely many annuli of A have negative half meeting both B_1,C_1
and positive half meeting both B_2,C_2.

Proof. Otherwise take distinct such annuli. Passing to a subsequence writes
them as g_n A_0 for one fixed annulus and distinct g_n. Use a convergence
subsequence with repeller r and attractor s. If r is outside A_0-, that
compact half is mapped uniformly into arbitrarily small neighborhoods of s,
which cannot meet both disjoint compact B_1 and C_1. Therefore r belongs to
A_0-. The same argument puts r in A_0+, a contradiction. Empty compact sets
make the assertion immediate. Finitely many annulus types are handled by
pigeonhole. This is the mechanism of [B98, Lemma 7.2] and [A22, Lemma 3.2].

## Lemma 4.2: separating a nonconical point has bounded depth

If a,b,p are distinct and p is nonconical, there are only finitely many
annuli A_i satisfying {a,b}<A_i<{p}. In particular (a,b|p)<infinity.

Proof. Infinitely many such annuli provide distinct g_n and a fixed annulus
A_0 with a,b in g_n int(A_0-) and p in g_n int(A_0+). Apply convergence to
g_n^{-1}, with repeller r and attractor u. At least one of a,b differs from
r, so u belongs to the closed set A_0-. If p!=r, then g_n^{-1}p->u would
also put u in A_0+, impossible. Hence r=p. Pass to a further subsequence
so g_n^{-1}p->v in A_0+. Now u!=v and the sequence witnesses that p is
conical, again a contradiction. Chain lengths are bounded by the number of
separating annuli, because strict chains contain no repeated annulus.

## Lemma 4.3: a common bounded sequence at every nonconical point

Let p be nonconical, fix distinct a,b outside p, and let t_n->p avoid a,b,p.
For x=(a,b,p) and y_n=(a,t_n,p), the triple quasimetric satisfies

sup_n rho(x,y_n)<infinity.

Proof. Seven of the nine pair-pair crossratios are zero because the pairs
intersect. The remaining two are

(a,b|t_n,p) and (b,p|a,t_n).

The first is at most (a,b|p), finite by Lemma 4.2. Choose a closed
neighborhood V of p disjoint from a and b; eventually t_n is in V. Lemma
4.1 with B_1={b}, C_1={p}, B_2={a}, C_2=V bounds the number of annuli that
could occur in a chain for the second term, uniformly for these n. The
finitely many initial n have finite crossratios by the same lemma applied
to singleton pairs. This proves the bound.

The triples y_n converge topologically to p in the customary triple-space
compactification (two coordinates tend to p), but stay bounded in rho.
Moreover the same sequence is bounded for each of any finite collection of
such systems. A finite sum or maximum of their quasimetrics therefore still
has this defect.

## Lemma 4.4: a parabolic element has a bounded orbit in this model

Suppose h fixes a nonconical p and h^n z->p and h^{-n}z->p for every z!=p.
Assume h has infinite order. Then its orbit of x=(a,b,p) is rho-bounded.

Proof. For all sufficiently large positive n, z_n=(a,h^n a,p) is a distinct
triple, and Lemma 4.3 bounds rho(x,z_n). By invariance,

rho(z_n,h^n x)=rho(h^{-n}z_n,x)
             =rho((h^{-n}a,a,p),x).

Permuting a triple does not change rho. Lemma 4.3 again bounds this expression
since h^{-n}a->p. The additive triangle inequality for rho bounds
rho(x,h^n x). The finitely many remaining positive n and zero can be absorbed
in the bound. Negative n give the same distances by symmetry and invariance.

Here the fact that rho is a hyperbolic path quasimetric is the established
[B98, Propositions 7.5, 6.5, 4.2 and Lemma 4.3]. For completeness, the
finiteness ingredient (A1) is Lemma 4.1. To see the uniform crossing bound
(A2), assume (a_n,b_n|c_n,d_n)->infinity and (a_n,c_n|b_n,d_n)>0. Normalize
one annulus separating the latter pairs to one of the finitely many fixed
types. After taking limits, a,c lie in its negative half and b,d in its
positive half. Thus a!=b and c!=d. The former chains now contradict Lemma
4.1, using fixed disjoint compact neighborhoods for each of those two pairs.
This also explains exactly why finiteness of the number of orbits matters.

## Theorem 4.5: finite-orbit annulus models fail for the modular boundary

Let G=PSL_2(Z) act on Z=RP^1 by fractional linear transformations. For any
symmetric invariant annulus system with finitely many G-orbits, construct
its triple quasimetric rho and a graph Gamma as in Lemma 2.1. Then there is
no G-equivariant homeomorphism Z -> boundary(Gamma).

Nevertheless the action meets the question's hypotheses and has an exact
isometric realization on the hyperbolic plane. Thus this theorem is not a
counterexample to Kapovich's question.

Proof of the hypotheses. An infinite sequence of distinct elements has
integer determinant-one representatives M_n with norm tending to infinity,
after passing to a subsequence. Normalizing by their maximum entry norm and
taking a subsequence gives a nonzero rank-one matrix B. Projectively M_n
converges uniformly on compact sets outside ker(B) to im(B): the normalized
linear maps converge uniformly, and their projective denominators are
bounded away from zero on each such compact set. This proves
the convergence property and hence properness on triples. The action is
minimal: T(x)=x+1 has T^n x->infinity for every finite x. Every orbit closure
therefore contains infinity, and invariance then makes it contain
G infinity=Q union {infinity}, a dense subset of RP^1.

Proof that infinity is not conical. Suppose g_n infinity->alpha and
g_n x->beta for every finite x, with alpha!=beta. Normalize determinant-one
integer matrices as above. Their rank-one limit must have image beta and
kernel infinity; otherwise g_n infinity would also tend to beta. Write the
two columns as u_n,v_n. Kernel infinity means u_n/||M_n||->0, whereas
v_n/||M_n|| tends to a nonzero vector. In particular ||v_n||->infinity and
||u_n||>=1. Since det(u_n,v_n)=1,

|det(u_n,v_n)|/(||u_n|| ||v_n||) <= 1/||v_n|| -> 0.

The left side is the sine of the projective angle between g_n infinity and
g_n 0. Their limits must therefore agree, contrary to alpha!=beta.

Now h=T fixes infinity, with both h^n and h^{-n} collapsing its complement
toward infinity. Lemma 4.4 shows that h has a bounded rho-orbit, hence a
bounded graph orbit by Lemma 2.1. Say d_Gamma(o,h^n o)<=D for every integer n.

For an isometry of a hyperbolic space, changing the base point by at most D
changes boundary Gromov products by at most D, with the usual equivalent
boundary-product conventions differing only by a fixed hyperbolicity error.
This follows first for interior points directly from the triangle inequality,
then for the boundary by taking the defining limits. Thus the whole family
h^n acts equicontinuously on the boundary in its Gromov-product uniformity.
If there were a homeomorphism from the compact space RP^1 onto that boundary,
this would be uniform equicontinuity in any compatible compact metric on
RP^1, and the same would hold for the inverse powers.

But h^n 0=n and h^n 1=n+1 both tend to infinity in RP^1. Inverse-power
equicontinuity would force 0=1, exactly as in Lemma 3.1. This contradiction
proves the claimed failure of every finite-orbit annulus graph.

Finally the original action does extend isometrically to the upper half-plane
with its usual hyperbolic metric. For g(z)=(az+b)/(cz+d), det(g)=1 gives

Im g(z)=Im z/|cz+d|^2,
|g(z)-g(w)|=|z-w|/(|cz+d| |cw+d|).

Substitution in cosh d(z,w)=1+|z-w|^2/(2 Im z Im w) proves isometry. The
hyperbolic plane is a geodesic Gromov-hyperbolic space with boundary RP^1.
This is the promised positive control.

## Scope of the result

Theorem 4.5 excludes this specific family of interior geometries, including
any finite enlargement of the annulus-type list. It excludes neither
infinitely many annulus orbits nor other constructions, and proves no
non-realizability statement about a general convergence action.

Checkpoint: approximately 15% toward the universal target. A concrete
failure mechanism has been proved; the original general question remains
unresolved.
