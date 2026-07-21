# Full symmetric monodromy in a uniform subfamily of the Alpoge-Gallagher Keller maps

*Provisional research note - 20 July 2026*

*Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol.*

*First public release: __PUBLICATION_UTC__ (__PUBLICATION_PDT__).*

> **Verification disclaimer.** I am a complete amateur and cannot independently
> verify the mathematical claims in this note. This is an experiment in the
> limits of AI-assisted mathematics, not an established result. Every argument,
> computation, and novelty claim requires independent expert review.

## Abstract

Gallagher's weighted-lift construction, posted immediately after Alpoge's
announced counterexample to the Jacobian conjecture, produces a
three-dimensional Keller map of every generic degree \(n\ge3\). We isolate a
particularly simple uniform subfamily \(F_n:\mathbb C^3\to\mathbb C^3\) and
prove that the Galois closure of its function-field extension has full
symmetric group \(S_n\). Consequently these maps have no nonidentity rational
deck transformations. We also give, uniformly in \(n\), two rational points
with the same rational image. This is a structural refinement of the
Alpoge-Gallagher examples, not an independent construction of the underlying
counterexamples. The all-degree monodromy statement appears not to have been
recorded in the public follow-on analyses available on 20 July 2026.

## 1. The family

Fix an integer \(n\ge3\), and put

\[
u=1+xy,\qquad
\gamma=1-\frac{n}{n-1}xy+x^2z.
\]

Define \(F_n=(A_n,B_n,C_n)\) by

\[
A_n=\frac{(n-2)u+u^2-(n-1)u^n\gamma^{n-2}}
              {(n-2)x^2},
\]

\[
B_n=\frac{(n-2)+2u-nu^{n-1}\gamma^{n-2}}
              {(n-2)x},
\qquad C_n=x\gamma.
\tag{1}
\]

The displayed quotients by \(x^2\) and \(x\) cancel identically, as proved
below, so (1) is an honest polynomial map over \(\mathbb Q\).

### Theorem 1

For every \(n\ge3\):

1. \(F_n:\mathbb A^3_{\mathbb C}\to\mathbb A^3_{\mathbb C}\) is polynomial
   and \(\det JF_n=1\).
2. If \(K=\mathbb C(A_n,B_n,C_n)\) and
   \(L=\mathbb C(x,y,z)\), then \([L:K]=n\).
3. The Galois closure of \(L/K\) has group \(S_n\).
4. Every rational map \(\sigma:\mathbb A^3\dashrightarrow\mathbb A^3\)
   satisfying \(F_n\circ\sigma=F_n\) is the identity.

Thus there is an explicit noninjective Keller map in dimension three, of every
generic degree \(n\ge3\), with full symmetric monodromy and trivial rational
deck group.

## 2. Polynomiality and the Jacobian

Set \(v=xy\), \(\tau=x^2z\), and \(w=u\gamma\). Introduce

\[
p_n(w)=\frac{2w-nw^{n-1}}{n-2},\qquad
q_n(w)=\frac{w^2-(n-1)w^n}{n-2}.
\]

Then \(q_n'(w)=w p_n'(w)\), and (1) can be written

\[
\alpha=u+\frac{q_n(w)}{\gamma^2},\qquad
\beta=1+\frac{p_n(w)}{\gamma},\qquad
(A_n,B_n,C_n)=\left(\frac{\alpha}{x^2},
\frac{\beta}{x},x\gamma\right).
\tag{2}
\]

The expressions \(\alpha,\beta\) are polynomials in \(v,\tau\). Directly,
\(\beta(0,0)=0\), so \(\beta\in(v,\tau)\). Also
\(\alpha(0,0)=0\) and \(\partial\alpha/\partial v(0,0)=0\), so
\(\alpha\in(v^2,\tau)\). After \(v=xy\), \(\tau=x^2z\), this gives
\(\beta\in x\mathbb C[x,y,z]\) and
\(\alpha\in x^2\mathbb C[x,y,z]\), proving polynomiality.

For the determinant, make the output change

\[
P=B_nC_n=\gamma+p_n(w),\qquad
Q=A_nC_n^2=w\gamma+q_n(w),\qquad C=C_n.
\]

Its Jacobian with respect to \((A_n,B_n,C_n)\) is \(-C^3\). The input
changes \((x,y,z)\mapsto(x,v,\tau)\mapsto(x,w,\gamma)\) have product
Jacobian \(x^3\gamma\). Finally,

\[
\frac{\partial(P,Q)}{\partial(w,\gamma)}
=wp_n'(w)-q_n'(w)-\gamma=-\gamma.
\]

Including \(C=x\gamma\) gives
\(\partial(P,Q,C)/\partial(x,w,\gamma)=-\gamma^2\), hence

\[
\frac{\partial(P,Q,C)}{\partial(x,y,z)}=-x^3\gamma^3=-C^3.
\]

Comparison with the output change proves \(\det JF_n=1\).

## 3. The degree-n inverse equation

Let

\[
R_n(w)=\int_0^w p_n(s)\,ds=\frac{w^2-w^n}{n-2}.
\]

Since \(q_n=wp_n-R_n\), elimination of \(\gamma\) from \(P,Q\) yields

\[
R_n(w)=wP-Q.
\]

Equivalently, every generic preimage supplies a root of

\[
H_n(T)=T^n-T^2+(n-2)B_nC_nT-(n-2)A_nC_n^2.
\tag{3}
\]

Conversely, for a root \(w\) for which
\(\gamma=P-p_n(w)\ne0\), the source coordinates are recovered rationally:

\[
x=\frac{C}{\gamma},\quad
u=\frac{w}{\gamma},\quad
y=\frac{u-1}{x},\quad
z=\frac{\gamma-1+\frac{n}{n-1}(u-1)}{x^2}.
\tag{4}
\]

Put

\[
U=(n-2)B_nC_n,\qquad V=-(n-2)A_nC_n^2.
\]

The rational change of target coordinates is invertible at the level of
function fields:

\[
K=\mathbb C(A_n,B_n,C_n)=\mathbb C(U,V,C_n)
  =\mathbb C(U,V)(C_n).
\]

Indeed,
\(B_n=U/((n-2)C_n)\) and
\(A_n=-V/((n-2)C_n^2)\). Since \(A_n,B_n,C_n\) are algebraically independent
(the map is dominant), \(C_n\) is transcendental over \(\mathbb C(U,V)\).
The inverse equation (3) becomes

\[
h_n(T)=T^n-T^2+UT+V.
\tag{5}
\]

The polynomial (5) is irreducible in \(\mathbb C(U,V)[T]\): in
\(\mathbb C[U,V,T]\) it is primitive and linear in \(V\), and any
factorization would force a factor independent of \(V\) to divide the
coefficient \(1\) of \(V\). Irreducibility is preserved after the purely
transcendental base change
\(\mathbb C(U,V)\subset\mathbb C(U,V)(C_n)=K\), by Gauss's lemma.
Equations (3)-(4) therefore show that \(L=K(w)\) and \([L:K]=n\).

## 4. Full symmetric monodromy

We compute the Galois group of (5) over \(\mathbb C(U,V)\). Its affine
discriminant curve \(D_n\) is the image of

\[
t\longmapsto
\left(U,V\right)=
\left(2t-nt^{n-1},\ (n-1)t^n-t^2\right),
\tag{6}
\]

obtained by solving \(h_n(t)=h_n'(t)=0\). Thus \(D_n\) is irreducible.
At \(t=0\), the corresponding polynomial is

\[
h_n(T)=T^2(T^{n-2}-1),
\]

which has exactly one double root and all remaining roots simple. Moreover,
\(t=0\) is the unique parameter mapping to \((U,V)=(0,0)\): if \(t\ne0\)
and \(U=0\), then \(t^{n-2}=2/n\), which gives
\(V=t^2(n-2)/n\ne0\). The derivative of (6) at \(t=0\) has first coordinate
\(2\), so \((0,0)\) is a smooth point of \(D_n\). Having exactly one double root
and all other roots simple is a nonempty Zariski-open condition on the
irreducible discriminant curve (the complement is the locus of a triple root
or two distinct multiple roots). Hence the generic inertia along \(D_n\) is a
transposition.

The root incidence variety \(h_n(T)=0\) is isomorphic to
\(\mathbb A^2_{T,U}\), because \(V=-T^n+T^2-UT\). It is irreducible, so
the monodromy action on the \(n\) roots is transitive. Moreover, the monodromy
group is normally generated by the inertia around its finite branch divisor:
after quotienting the Galois closure by those inertia groups one obtains a
finite cover of \(\mathbb A^2_{U,V}\) unramified in codimension one; purity
makes it finite etale, and affine complex space has no nontrivial connected
finite etale covers. Since \(D_n\) is irreducible, these inertia generators
are conjugate transpositions.

A transitive permutation group generated by transpositions is the full
symmetric group: form the graph whose edges are the generating
transpositions; transitivity makes the graph connected, and edge
transpositions of a connected graph generate \(S_n\). Hence

\[
\operatorname{Gal}(h_n/\mathbb C(U,V))\cong S_n.
\tag{7}
\]

Let \(M/\mathbb C(U,V)\) be the splitting field. A finite algebraic extension
and a purely transcendental extension are linearly disjoint, so

\[
\operatorname{Gal}(M(C_n)/\mathbb C(U,V)(C_n))
\cong \operatorname{Gal}(M/\mathbb C(U,V))\cong S_n.
\]

Thus the base change from \(\mathbb C(U,V)\) to the actual target field
\(K=\mathbb C(U,V)(C_n)\) preserves the Galois group, and \(S_n\) is the
Galois closure group of \(L/K\).

## 5. Trivial rational deck group

Inside the \(S_n\)-Galois closure, \(L=K(w)\) is the fixed field of a point
stabilizer \(S_{n-1}\). Therefore

\[
\operatorname{Aut}_K(L)\cong
N_{S_n}(S_{n-1})/S_{n-1}=1,
\]

since a point stabilizer is self-normalizing for \(n\ge3\). Any dominant
rational map \(\sigma\) with \(F_n\circ\sigma=F_n\) induces a
\(K\)-endomorphism of the finite extension \(L/K\), hence a
\(K\)-automorphism. It must be the identity. A nondominant \(\sigma\) is
impossible because its composition with the dominant map \(F_n\) could not
equal \(F_n\). This proves Theorem 1(4).

## 6. A uniform rational collision certificate

Let

\[
s_n=\frac{4-2^n}{n-2}.
\]

At the target \((A,B,C)=(s_n,s_n,1)\), (3) becomes

\[
T^n-T^2+(4-2^n)(T-1),
\]

which has the two simple roots \(r=1,2\). Define

\[
g_r=s_n-p_n(r),
\]

and

\[
X_{n,r}=\left(
\frac1{g_r},\ r-g_r,\
g_r^2\left[g_r-1+\frac n{n-1}
\left(\frac r{g_r}-1\right)\right]
\right).
\tag{8}
\]

Here

\[
g_1=\frac{n+2-2^n}{n-2},\qquad g_2=2^{n-1},
\]

both nonzero for every \(n\ge3\). Reconstruction (4) gives the exact identity

\[
F_n(X_{n,1})=F_n(X_{n,2})=(s_n,s_n,1).
\tag{9}
\]

The points are distinct because their \(w\)-coordinates are 1 and 2. For
example, when \(n=3\),

\[
F_3(-1/3,4,-54)=F_3(1/4,-2,36)=(-4,-4,1),
\qquad \det JF_3=1.
\]

Thus every member comes with a short rational noninjectivity certificate, not
only an abstract generic-degree argument.

## 7. Scope and novelty audit

Alpoge announced the first explicit three-dimensional counterexample on 19
July 2026. Gallagher then posted a weighted-lift construction realizing every
generic degree \(n\ge3\). A contemporaneous MathOverflow post computed the
original cubic map's \(S_3\) Galois closure and trivial deck group. Another
follow-on calculation determined exact images for a different every-degree
family, including surjective noninjective examples.

The residual contribution isolated here is the single elementary subfamily
(1), its uniform rational collision (8), and especially the all-degree statement
\(\operatorname{Gal}=S_n\) with trivial rational deck group. Targeted searches
on 20 July 2026 did not locate that statement. Because this subject is moving
hour by hour, this paragraph is not a priority claim. Before public submission,
an expert should check the purity/monodromy paragraph and repeat a literature
search.

## References

1. O.-H. Keller, *Ganze Cremona-Transformationen*, Monatsh. Math. Phys. 47
   (1939), 299-306.
2. H. Bass, E. Connell, and D. Wright, *The Jacobian conjecture: reduction of
   degree and formal expansion of the inverse*, Bull. Amer. Math. Soc. 7
   (1982), 287-330.
3. L. Alpoge, announcement of an explicit counterexample, 19 July 2026.
4. A. Gallagher, *An infinite family of counterexamples to the Jacobian
   Conjecture in dimension three: every generic fiber degree n >= 3 occurs*,
   research note, 20 July 2026.
5. MathOverflow question 513387, *Galois structure of the new counterexample
   to the Jacobian conjecture*, 20 July 2026.
