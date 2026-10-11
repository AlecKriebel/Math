# Universal validation of the partial reduction

This verifies the known reduction and credited formulas. It does not constitute
a further substantive attempt to solve the unrestricted decomposition problem.
All vector spaces are ordinary even complex vector spaces; no graded Koszul
convention is silently imposed. Write L=Lie(V), I=E tensor L, h=L semidirect I.

Since E squared is zero, I is abelian. The chain-level decomposition of the
ordinary Chevalley–Eilenberg complex is

    C_n(h) = direct sum over p+q=n of Lambda^p L tensor Lambda^q I.

Place all L factors first. The bracket of two L factors reduces p by one. A
bracket of an L factor and an I factor replaces the I factor with its adjoint
action, again reducing p by one. A bracket of two I factors vanishes. Hence q
is preserved and, with the ordinary coefficient-complex signs, the weight q
subcomplex identifies with C_*(L; Lambda^q I) shifted by q. A harmless overall
sign under a different ordering is removed by a degreewise chain isomorphism.
This is a direct sum of actual complexes. No spectral sequence collapse or
extension claim is needed. Taking homology commutes with these vector-space
direct sums.

The universal enveloping algebra of L is T(V). Concatenation gives a free right
T(V)-module resolution of the trivial right module:

    0 -> V tensor T(V) -> T(V) -> C -> 0.

The first map is injective and identifies its source with the augmentation
ideal: each nonempty tensor word has exactly one first letter and remaining
tail. This proof also applies when V is zero. Tensoring this right resolution
with any left L-module N gives V tensor N -> N with map v tensor z -> v.z.
The opposite handed resolution is T(V) tensor V using the last letter. One
must use the appropriate handed resolution in the Tor computation; the
original notation suppresses this convention but the resulting map is correct.
Thus H_p(L;N)=0 for p>1, H_1 is the kernel, and H_0 is the cokernel.

For N_q=Lambda^q(E tensor L), let delta_q be the diagonal adjoint action. The
natural result is

    H_n(h) = coker(delta_n) direct sum ker(delta_(n-1)),

where the second term is omitted for n=0. The two pieces have E degrees n and
n-1. Their distinct weights make the split canonical and natural in E,V.
The action preserves total V bracket-length degree: the domain in total
degree d is V tensor (N_q)_(d-1), mapping to (N_q)_d. For finite-dimensional
E,V, each fixed q,d component is finite-dimensional. Infinite L and unbounded
V degree are handled by direct sums of these homogeneous components, without
assuming convergence, finite total dimension, or a completed tensor product.

Characteristic zero gives the exterior Cauchy rule

    N_q = direct sum over lambda partitions q of
          S_lambda(E) tensor S_(lambda transpose)(L).

It also makes taking S_q coinvariants exact by averaging. Therefore

    H_1(L;N_q) = (E^tensor q tensor H_1(L;L^tensor q)
                  tensor sign_q)_(S_q).

The sign is the ordinary exterior sign. A sign coefficient becomes trivial
after this additional twist and produces Sym^q E; a trivial coefficient
becomes sign and produces Lambda^q E. Applying the inspected Powell v4
Theorem 1 and Proposition 3.3 therefore gives exactly the original equations
(4) and (5). The separate q=1 branch contributes one E tensor Lambda^3 V,
not two. Flat extension of scalars from Q to C preserves kernels, cokernels,
and these finite-group constructions. Rational divided powers identify with
ordinary symmetric powers here; this statement would require change outside
characteristic zero.

The known cyclic-Lie layer also follows from the exact sequence

    0 -> CycLie_d(V) -> V tensor L_(d-1)(V) -> L_d(V) -> 0,

for d>=2. The bracket map is surjective by generation of L by V and repeated
Jacobi identities. Hence its character is the difference of the two actual
characters in that exact sequence. This justified subtraction does not allow
one to infer arbitrary delta_q kernels from an Euler difference. At E=0 the
free-Lie H_0=C, H_1=V boundary follows from the same resolution. At V=0 only
H_0=C remains. At dim V=1 the Lie algebra h is abelian and its homology is
Lambda^n((C direct sum E) tensor V), with the split dimensions
binomial(dim E,n)+binomial(dim E,n-1). The abelianization gives H_1(h)=(C
direct sum E) tensor V in all dimensions.

The complete target still requires evaluation of every kernel and cokernel of
V tensor S_mu(L(V)) -> S_mu(L(V)), naturally as Schur functors of V, for all
partitions mu and all degrees. Giving these maps, computing some diagonals,
or obtaining a virtual difference does not provide those evaluated
multiplicities. This exact remaining gap is what the original partial packet
states. Its formulas survive the universal proof above and the independent
finite falsifiers; neither proof nor falsifiers promote it to a full answer.
