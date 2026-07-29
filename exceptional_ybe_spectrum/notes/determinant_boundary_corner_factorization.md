# Determinant boundary corners are spectators

**Date:** 2026-07-29

**Scope:** arbitrary exceptional projection \(P\), with no Pauli,
irreducibility, leg-commutant, flip-symmetry, or tensor-factorization
assumption

**Status:** exact all-boundary factorization theorem and exact
dimension-six limitation model; no divisibility-by-four obstruction

## 1. Question and answer

Put \(d=2s\), let

\[
p_i=P_{i,i+1},
\qquad
\mathcal A_n=\operatorname{alg}^*(p_1,\ldots,p_{n-1})
\subseteq\operatorname{End}(V^{\otimes n}),
\]

and let

\[
e=\frac32p_1p_2p_1-\frac12p_1,
\qquad
f=\frac32(1-p_1)(1-p_2)(1-p_1)-\frac12(1-p_1)
\tag{1}
\]

be the three-site common-one and common-zero projections.  Both have rank
\(s^3\).  The four-site calculation already gives

\[
e p_3 e=\frac12e,\qquad
e\,e_{234}\,e=\frac14e,
\tag{2}
\]

and the analogous formulas for \(f\).

A tempting next step is to add one, two, or three boundary sites, combine
boundary \(H\)'s or \(R\)'s with shifted copies of \(e,f\), and close the
extra sites in the hope of obtaining two anticommuting operators or a
quaternionic structure on \(\operatorname{ran}e\).  The following theorem
shows that this entire boundary-word route cannot work.  In fact the
statement holds with any number of added boundary sites.

### Theorem 1.1 (determinant boundary-corner factorization)

For \(a=e\) or \(a=f\), and every \(m\geq0\),

\[
\boxed{
(a\otimes I_{V^{\otimes m}})
\mathcal A_{m+3}
(a\otimes I_{V^{\otimes m}})
=a\otimes\mathcal A_m,
}
\tag{3}
\]

where the copy of \(\mathcal A_m\) on the right acts on sites
\(4,\ldots,m+3\), and \(\mathcal A_0=\mathcal A_1=\mathbb C\).

Thus every closed Hecke boundary word has the form

\[
a\otimes x,\qquad x\in\mathcal A_m.
\tag{4}
\]

It is the identity on the determinant multiplicity
\(\operatorname{ran}a\).  In particular, applying any linear functional
to all \(m\) added sites, including their ordinary or normalized partial
trace, produces only

\[
\lambda a.
\tag{5}
\]

No two such closed boundary operations can supply a nondegenerate
complex Clifford action, alternating form, or quaternionic structure on
\(\operatorname{ran}a\).

### Proof

Automatic standardness and faithfulness identify every \(\mathcal A_n\)
with the semisimple Jones--Wenzl quotient \(H_n(3,6)\).

At three strands the two one-dimensional blocks selected by \(e\) and
\(f\) correspond to the two invertible summands in

\[
X^{\otimes3}\cong\mathbf1\oplus g\oplus2Y
\tag{6}
\]

in \(\mathcal C(\mathfrak{sl}_3,6)\), where \(g\) is an invertible simple
current of order three.  Fix one of these invertible endpoints
\(\gamma\in\{\mathbf1,g\}\).

The standard path-algebra description says

\[
a\mathcal A_{m+3}a
\cong
\bigoplus_\lambda
M_{N^{(m)}_{\lambda,\gamma}}(\mathbb C),
\tag{7}
\]

where \(N^{(m)}_{\lambda,\gamma}\) is the number of length-\(m\) paths in
the \(X\)-fusion graph from \(\gamma\) to \(\lambda\).  Multiplication by
the invertible object \(\gamma\) is a fusion-graph automorphism.
Consequently

\[
N^{(m)}_{\lambda,\gamma}
=N^{(m)}_{\gamma^{-1}\lambda,\mathbf1},
\tag{8}
\]

and hence

\[
\dim(a\mathcal A_{m+3}a)
=\sum_\lambda
\bigl(N^{(m)}_{\lambda,\gamma}\bigr)^2
=\dim\mathcal A_m.
\tag{9}
\]

On the other hand, \(a\) commutes with the disjoint generators
\(p_4,\ldots,p_{m+2}\).  Faithfulness of the \(m\)-strand
representation therefore gives an injective subalgebra

\[
a\otimes\mathcal A_m
\subseteq
a\mathcal A_{m+3}a
\tag{10}
\]

of dimension \(\dim\mathcal A_m\).  Equations (9)--(10) prove equality.
Equation (5) follows immediately from (3). \(\square\)

## 2. What happens on four, five, and six sites

The first three cases of (3) are especially transparent:

\[
\begin{array}{c|c|c}
\text{total sites}&a\mathcal A_na&
\text{right-hand spectator algebra}\\ \hline
4&\mathbb C a&\mathcal A_1\cong\mathbb C\\
5&a\otimes(\mathbb C\oplus\mathbb C)&
\mathcal A_2\cong\mathbb C\oplus\mathbb C\\
6&a\otimes
(\mathbb C\oplus M_2(\mathbb C)\oplus\mathbb C)&
\mathcal A_3.
\end{array}
\tag{11}
\]

At four sites, the boundary compression in (2) is therefore forced to
be scalar.  At five sites, the first non-scalar boundary corner merely
acts on the two newly added sites.  For example, writing
\(h_i=I-2p_i\), direct use of the cubic relation gives

\[
e\,p_3p_4p_3\,e
=\frac16e(1+p_4),
\tag{12}
\]

and hence

\[
\boxed{
e\,h_3h_4h_3\,e
=-\frac13e\,h_4.
}
\tag{13}
\]

The apparent boundary action is exactly a spectator action on sites
\(4,5\).

At six sites, the \(M_2\)-summand in (11) does contain a canonical
two-generator complex Clifford algebra.  Let \(p=p_4\), \(q=p_5\), and
let \(g_{\rm gen}\) be their generic two-projection central projection.
On that generic summand,

\[
Z=g_{\rm gen}(2p-I)g_{\rm gen},
\]

\[
X=\frac3{\sqrt2}g_{\rm gen}
\bigl(pq(1-p)+(1-p)qp\bigr)g_{\rm gen}
\tag{14}
\]

satisfy

\[
Z^2=X^2=g_{\rm gen},\qquad ZX=-XZ.
\tag{15}
\]

But Theorem 1.1 identifies these operators as

\[
e\otimes Z,\qquad e\otimes X.
\tag{16}
\]

They act on the new three-site path factor, not on
\(\operatorname{ran}e\).  Their \(M_2\)-module multiplicity in the
six-site representation is

\[
3s^6,
\tag{17}
\]

which may be odd.  The factor two is already the \(M_2\) path module; it
does not imply \(2\mid s\).

For \(s=3\), the determinant multiplicity is

\[
\dim\operatorname{ran}e=s^3=27,
\tag{18}
\]

while the six-site generic corner is a direct sum of \(3s^6=2187\)
two-dimensional modules.  All dimensions are integral and no
alternating form is imposed on the \(27\)-dimensional determinant
multiplicity.

## 3. Shifted determinant projections

Let \(E=e_{123}\) and \(F=e_{234}\).  The universal relation

\[
EFE=\frac14E,\qquad FEF=\frac14F
\tag{19}
\]

provides the canonical unitary

\[
2FE:\operatorname{ran}E\longrightarrow\operatorname{ran}F.
\tag{20}
\]

This is an open path between two different subspaces.  Closing it gives

\[
(2EF)(2FE)=E,
\tag{21}
\]

so the shortest loop is scalar.  Longer products of shifted \(e\)'s,
shifted \(f\)'s, and boundary \(P,H,R\) operators are elements of the
corners in Theorem 1.1.  When they begin and end at \(E\), they are
\(e\otimes x\).  Tracing or taking a matrix coefficient on all added
boundary sites again leaves only a scalar on \(\operatorname{ran}e\).

Thus shifted determinant paths do not evade the factorization theorem.
To turn (20) into an endomorphism, one would have to identify its source
and target by extra data.  Such an identification is not canonical and
is not part of the exceptional relations.

The same conclusion holds for opposite determinant signs.  Their
shortest shifted products vanish, and every closed same-sign word falls
under (3).

## 4. Reversal and antiunitaries

Tensor reversal is not an element of the Hecke boundary algebra.  If
\(J_n\) reverses tensor factors and \(P^{\rm op}=FPF\), then

\[
J_nP_{i,i+1}(P)J_n
=P_{n-i,n-i+1}(P^{\rm op}).
\tag{22}
\]

Consequently

\[
J_3e(P)J_3=e(P^{\rm op}),
\tag{23}
\]

not \(e(P)\) in general.  A reversal-based bilinear or antiunitary
structure on \(\operatorname{ran}e(P)\) therefore requires an additional
coherent equivalence \(P^{\rm op}\simeq P\).

This is a genuine missing hypothesis, not just a gap in the argument.
For the published exact \(d=4\) witness, the independent exact reversal
audit gives

\[
\operatorname{Tr}(eJ_3eJ_3)=1,\qquad
\|e-J_3eJ_3\|_{\rm HS}^2=14,
\tag{24}
\]

where \(\operatorname{rank}e=8\).  Bare reversal does not preserve the
determinant range.  The same witness is real, so its available
conjugation squares to \(+I\), not \(-I\).

Thus neither reversal nor complex conjugation supplies a universal
quaternionic structure.

## 5. Endpoint partial traces versus internal contractions

The normalized endpoint partial traces

\[
\mathbb E_n^R(x)=\frac1d\operatorname{Tr}_n(x),
\qquad
\mathbb E_n^L(x)=\frac1d\operatorname{Tr}_1(x)
\tag{25}
\]

map \(\mathcal A_n\) into \(\mathcal A_{n-1}\).  This follows from the
standard spanning relation

\[
\mathcal A_n
=\mathcal A_{n-1}
+\mathcal A_{n-1}p_{n-1}\mathcal A_{n-1}
\tag{26}
\]

and the scalar partial trace of \(P\).  Iterating endpoint traces around
a fixed three-site determinant interval gives an element of
\(\mathcal A_3\), whose \(e\)- or \(f\)-corner is one-dimensional.  This
is a second proof of the scalar-closure statement (5).

Internal contractions are different.  For example,
\(\operatorname{Tr}_2e\) acts on the nonadjacent endpoint sites and can
be nonscalar.  It is not an endomorphism of
\(\operatorname{ran}e\), and turning it into one requires an additional
tensor identification.  Theorem 1.1 therefore closes the natural
boundary-trace route, but it does not claim that every possible internal
contraction invariant is scalar.

## 6. Exact \(d=6\) abstract limitation model

The theorem already proves abstract compatibility for every odd \(s\).
For a completely explicit four-site check, set

\[
Q=
\begin{pmatrix}
1/3&\sqrt2/3\\
\sqrt2/3&2/3
\end{pmatrix}.
\tag{27}
\]

There are three simple four-strand blocks of dimensions \(3,2,3\).
On the first three-dimensional block put

\[
p_1=
\begin{pmatrix}0&0&0\\0&1&0\\0&0&0\end{pmatrix},
\qquad
p_2=0\oplus Q,
\qquad
p_3=vv^*,
\qquad
v=\frac1{\sqrt2}(1,0,1)^T.
\tag{28}
\]

On the second three-dimensional block use

\[
I-p_1,\qquad I-p_2,\qquad I-p_3,
\tag{29}
\]

and on the two-dimensional block use

\[
p_1=p_3=
\begin{pmatrix}1&0\\0&0\end{pmatrix},
\qquad p_2=Q.
\tag{30}
\]

Every \(p_i\) is a projection,

\[
p_ip_{i+1}p_i-p_{i+1}p_ip_{i+1}
=\frac13(p_i-p_{i+1}),
\qquad
[p_1,p_3]=0.
\tag{31}
\]

For \(s=3\), repeat each of the three blocks

\[
2s^4=162
\tag{32}
\]

times.  The resulting exact \(1296=6^4\)-dimensional abstract
four-strand model has

\[
\operatorname{rank}p_i=648,
\qquad
\operatorname{rank}e_{123}
=\operatorname{rank}f_{123}=162,
\tag{33}
\]

and exactly satisfies (2), (19), and the opposite-sign orthogonality
relations.

This is not a \(d=6\) tensor-local solution: no identification is asserted
under which the three generators become

\[
P\otimes I_{36},\qquad I_6\otimes P\otimes I_6,\qquad I_{36}\otimes P
\tag{34}
\]

for a single \(36\times36\) projection \(P\).  It is an exact limitation
model showing that all abstract four-site boundary relations, including
far commutativity, remain compatible with \(s=3\).

Together with the all-\(m\) corner factorization, it proves that adding
five- or six-site determinant boundary words cannot recover the missing
tensor-local obstruction.

## 7. Conclusion

The determinant projection does not conceal a parity-bearing boundary
action.  Its entire boundary corner is a spectator:

\[
\boxed{
a\mathcal A_{m+3}a=a\otimes\mathcal A_m.
}
\]

At six sites a complex Clifford algebra does appear, but it is exactly
the ordinary three-strand Clifford block on the added sites.  It acts as
the identity on the rank-\(s^3\) determinant multiplicity and therefore
cannot force that rank to be even.

A successful \(4\mid d\) proof must use an invariant not contained in
closed determinant boundary words.  The still-live possibilities are
the simultaneous spatial placement of the two shifted copies of \(P\),
an internal contraction retaining nonadjacent-site information, or a
new canonical identification between distinct shifted determinant
ranges.  None is supplied by the Hecke boundary algebra itself.

## 8. Exact replay

Run

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_determinant_boundary_corner_factorization.py
```

The verifier uses exact SymPy arithmetic.  It checks:

- the simple-current path-count bijection and corner dimensions through
  twelve added sites;
- the exact \(3,2,3\)-dimensional four-strand quotient blocks;
- the complete \(d=6\) abstract rank bookkeeping;
- all adjacent cubic and far-commutation relations in those blocks;
- the boundary compression, shifted angle-\(1/4\), and opposite-sign
  relations;
- the five-site boundary-word reduction (13);
- the six-site Clifford block and its odd-\(s\) multiplicity limitation.
