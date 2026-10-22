# Independent construction and simplicity adversary

**Decision: PASS for the assigned mathematical scope. No repair required.**

Target: PR 1121 / problem 30004311, exact stated PR head
`f86b108ac1bc024302648eee9f47f74e26c810ec`. The reviewed proof is 14,213 bytes,
SHA-256 `68c040d5bfe5d536e6f33f0f319a2d721bac5c562ec60f802fc516f293205b75`.
The shared checkout is a different `main` head, so this review is bound to the
frozen proof bytes; it does not claim that the workspace HEAD equals the PR head.
No Git, index, ref, PR, or publication mutations were performed.

This adversary independently checks the direct operations, characteristic-five
logarithm/exponential, group-coordinate map, left-brace laws, simplicity for
**every** ideal, metabelianity, and abelianness of **all** multiplicative Sylow
subgroups. I read the accompanying audit but did not treat its acceptance or
historical computation claims as evidence. The independent implementation uses
the displayed definitions, imports no author implementation, and uses only the
Python standard library. Neither a priority assessment nor a separate audit of
the full asymmetric-product obstruction is included in this assignment.

## 1. Exact claim and possible failure points

The direct construction is

\[
B=x\mathbb F_5[x]/(x^5)\times V\times\mathbb F_2,
\qquad V=\{v\in\mathbb F_2^5:\sum v_i=0\},
\]

with componentwise addition and the proof's displayed circle law. The claim is
that this is a nontrivial simple left brace of order 20,000, and its
multiplicative group is

\[
(\mathbb F_5^3\rtimes_\tau C_2)\times(V\rtimes_M C_5),
\qquad \tau(k_1,k_2,k_3)=(-k_1,k_2,-k_3).
\]

The dangerous points are: truncating logarithms in characteristic five; using a
quadratic rather than linear binary coordinate; a possible missing coupling in
the direct-product identification; assuming a left ideal is a two-sided ideal;
and proving simplicity only for selected coordinate subgroups. The arguments
below resolve each of these points without such assumptions.

## 2. Logarithm, exponential, and binary ingredients

Every element of the ring has positive polynomial degree, so every product of
five ring elements vanishes. The commutative identities

\[
L(E(t))=t,\quad E(L(r))=r,\quad
L(r+u+ru)=L(r)+L(u)
\]

are identities of formal polynomials modulo total degree at least five. Their
degree-at-most-four coefficients have denominators involving only 2 and 3.
Consequently they reduce in characteristic five; no term with a denominator
divisible by five is required. This argument is valid for arbitrary ring
elements, not just monomials. The implementation separately checks both inverse
identities on 625 elements and the homomorphism identity on all 390,625 ordered
pairs.

In characteristic five the polynomial coefficients are

\[
L(r)=r+2r^2+2r^3+r^4,\qquad
E(t)=t+3t^2+t^3+4t^4.
\]

Extracting the fourth coefficient gives

\[
\eta(r)=a_4-a_1a_3-a_2^2/2+a_1^2a_2-a_1^4/4.
\]

It is a homomorphism for the ring circle group. Substitution \(x\mapsto-x\)
commutes with both polynomials and fixes their fourth coefficient. In
particular, \(\eta\) is not the raw fourth coefficient of \(r\).

On the even-weight subspace, the integer weight formula proves
\(Q(v+w)=Q(v)+Q(w)+\beta(v,w)\). The dot product is alternating because
every vector has even weight. If a vector is orthogonal to every
\(e_i+e_j\), all its coordinates agree; the only nonzero constant vector has
odd weight. Thus the restricted form is nondegenerate. Rotation preserves
weight and dot product. A rotation-fixed vector is constant, so \(M-1\) is
invertible on \(V\). These observations cover zero vectors and all nonzero
vectors without an irreducibility assumption.

## 3. Group law and brace compatibility on all inputs

Use coordinates \(L(r)=(k_1,k_2,k_3,s)\) and \(e=z+Q(v)\). Their inverse is
\(r=E(k_1x+k_2x^2+k_3x^3+s x^4)\), \(z=e+Q(v)\), so the coordinate map
is bijective. For arbitrary two inputs, logarithm equivariance gives

\[
L(r\circ\sigma^e(u))=L(r)+\sigma^eL(u).
\]

Hence the first three coefficients become \(k+\tau^e h\), while the fourth
becomes \(s+t\). The quadratic identity and rotation invariance give

\[
z+Z+\beta(v,M^sw)+Q(v+M^sw)
=z+Q(v)+Z+Q(w)=e+f.
\]

The remaining coordinate is \(v+M^sw\). Thus the complete transformed product
is

\[
(k,e,v,s)(h,f,w,t)
=(k+\tau^e h,e+f,v+M^sw,s+t).
\]

The two actions have orders dividing two and five, respectively. This is the
ordinary product of two semidirect-product group laws, proving associativity,
identity, and inverses universally. No assertion about all triples is inferred
from generator tests. Finite factor checks cover every relevant ring pair and
binary coordinate case; the additional 360,000 basis-pair checks are only
cross-checks.

Subtracting the first input in the additive group gives

\[
\lambda_{(r,v,z)}(u,w,Z)
=((1+r)\sigma^{z+Q(v)}u,M^{\eta(r)}w,
 Z+\beta(v,M^{\eta(r)}w)).
\]

This is additive. Its ring matrix is a unit triangular multiplication matrix
times the diagonal matrix for the involution, with diagonal
\(((-1)^e,1,(-1)^e,1)\). Its determinant is one. Its binary block is triangular
with invertible diagonal blocks \(M^s\) and 1. Thus every lambda map is an
additive automorphism. Together with the group law and
\(a\circ b=a+\lambda_a(b)\), this proves the full left-brace identity. The
checker tests all 1,250 possible ring matrices, all their 781,250 input images,
and all 80 binary blocks on every input and every ordered additive pair.

## 4. Simplicity for arbitrary ideals

Here an ideal is an additive subgroup invariant under all lambda maps and
normal in the multiplicative group. Both ideal operations used in the proof
are valid. Lambda invariance gives \(\lambda_g(i)-i\in I\). To verify
\(i*g\in I\) directly, put \(j=g^{-1}\circ i\circ g\in I\). Then

\[
i+\lambda_i(g)=i\circ g=g\circ j=g+\lambda_g(j),
\qquad i*g=\lambda_g(j)-i\in I.
\]

This uses normality explicitly and does not assume the second inference for a
mere left ideal.

For a nonzero element \((r,v,z)\in I\) with \(r\ne0\), its additive double
is \((2r,0,0)\ne0\). Multiplication by two is invertible on the 5-part and
kills the 2-part. If its lowest nonzero ring term is \(cx^j\), then
\(\lambda_{(x^{4-j},0,0)}-1\) isolates exactly \(cx^4\) for \(j<4\);
for \(j=4\) it is already isolated. Scaling gives
\(a=(x^4,0,0)\in I\). Higher terms cannot survive the multiplication, which
is why there is no cancellation assumption here.

If instead the initial nonzero element is \((0,v,z)\), either it is
\(b=(0,0,1)\), or nondegeneracy provides \(w\) with \(\beta(w,v)=1\).
Then \((\lambda_{(0,w,0)}-1)(0,v,z)=b\). The involution on the ring block
does not interfere because the input ring component is zero.

From \(b\), the star product \(b*(x,0,0)=(3x,0,0)\) produces \(x\) by
additive scaling. From \(a\), the products
\(a*(0,w,0)=(0,(M-1)w,0)\) produce every pure \(V\) vector. A binary shear
then produces \(b\). Finally \((\lambda_{(x,0,0)}-1)(x^j,0,0)\) produces
\((x^{j+1},0,0)\). Every nonzero ideal therefore contains all four ring basis
vectors, all four \(V\) basis vectors, and the last binary basis vector, hence
is all of \(B\).

This is a proof for every nonzero ideal, including mixed additive subgroups.
No decomposition of an ideal into coordinate subspaces is assumed. The
independent membership engine reproduces a derivation from every one of the
19,999 nonzero elements. Every scaling, lambda difference, and star step checks
that its required source is already known; every final derivation checks all
nine additive basis vectors. Its 259,889 steps happen to match one historical
count, but that match is not used as evidence. The trace hash is recorded in
the result file and regenerated from actual evaluated inference records.

## 5. Multiplicative hypotheses and witnesses

For abelian groups \(A,H\), the derived subgroup of \(A\rtimes H\) is the
subgroup generated by \((h-1)a\): those differences are actual commutators,
and quotienting by them makes the group abelian. Apply this independently to
the two factors. The image of \(\tau-1\) is the two-dimensional first/third
coordinate space. The image of \(M-1\) is all of \(V\). Consequently

\[
[G,G]\cong C_5^2\times C_2^4,\qquad |[G,G]|=400,
\]

and it is abelian. Both actions are nontrivial, so \(G\) is nonabelian and
metabelian.

Inside the direct product, \(K\times C_5\) has order 625 and
\(C_2\times V\) has order 32. They are abelian subgroups of the full prime
powers in 20,000, hence are Sylow subgroups. Sylow conjugacy transports
abelianness to every Sylow subgroup. Their normality is neither necessary nor
claimed. Under the coordinate map these are the actual primary subbraces
\(P_5=R\times0\times0\) and \(P_2=0\times V\times\mathbb F_2\).

The ring restriction gives \(x*x=x^2\ne0\), so the brace is nontrivial.
It also gives the checked witness \((x*x)*x=x^3\ne0\); classification of
two-trivial-factor products is outside this review's assigned boundary.

## 6. Falsification controls and finite scope

Four targeted changes are independently rejected:

1. Replacing \(\eta\) with the raw fourth coefficient breaks associativity
   for \(a=x\), \(b=x^3\), \(c=(0,e_0+e_1,0)\). The two binary outputs
   are \(e_1+e_2\) and \(e_0+e_1\).
2. Omitting \(Q\) from \(e\) breaks associativity for binary inputs
   \((0,e_0+e_1,0)\), \((0,e_0+e_2,0)\), followed by \(x\). The ring
   outputs are \(-x\) and \(x\).
3. Omitting \(\sigma\) leaves a valid brace but destroys simplicity:
   projection onto the ring brace is an additive and multiplicative
   homomorphism, with nonzero proper kernel \(P_2\) of order 32.
4. Omitting \(M\) likewise leaves a valid brace with a projection to the
   binary brace \((v,z)\circ(w,Z)=(v+w,z+Z+\beta(v,w))\); its kernel
   \(P_5\) has order 625. The binary group is identified with componentwise
   addition by \((v,z)\mapsto(v,z+Q(v))\).

For the last two changes, the group-coordinate proof remains valid with the
relevant action replaced by the identity, and lambda additivity remains
valid. Thus these are actual nonsimple braces rather than possibly invalid
operations. The universal projection identities prove the ideal assertions;
the finite generator closure checks are supplementary.

The results are deliberately factored. There is no exhaustive computation of
\(20,000^3\) triples, no enumeration of every additive subgroup, no imported
certificate treated as mathematics, and no claim about scholarly novelty.
The strongest result within this review is a full analytic proof of the
construction and every-ideal simplicity, backed by exact independent checks.
There is no remaining gap in that assigned scope. The final receipt binds the
proof, authored checker, both execution results, report, and research log.
