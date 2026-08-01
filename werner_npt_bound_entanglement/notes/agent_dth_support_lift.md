# Audit of the five-replica support constraint

## Status

The support constraint proposed for the holomorphic five-replica lift
cannot exist as stated. This is not a normalization problem.

Let \(V\) be a complex Hilbert space of dimension at least three and
write

\[
w=\sum_{i,j}W_{ij}e_i\otimes e_j\in\wedge ^2V,
\qquad W^{\mathsf T}=-W .
\]

On

\[
\mathscr X=\operatorname{Sym}^2(\wedge ^2V)\otimes V
\]

put

\[
\eta(w,z)=w_{12}\otimes w_{34}\otimes z_5.
\]

There is no nonzero complex-linear, or even real-linear, map on this
space satisfying

\[
\mathcal C_{\rm supp}\eta(w,z)
=\kappa\,w\otimes(W^\dagger z),\qquad \kappa\ne0,       \tag{1}
\]

under any fixed linear tensor identification. More strongly, after
the first Pluecker equation is imposed, the physical monomials with
\(W^\dagger z=0\) span the whole holomorphic source. Consequently no
nonzero linear map on this source can even have all physical support
monomials in its kernel.

The exact five-replica object encoding the support equation is instead
the **Hermitian cross-Jucys form**

\[
\boxed{\quad
J_5=F_{15}+F_{25}+F_{35}+F_{45}.
\quad}                                                   \tag{2}
\]

It obeys

\[
\boxed{\quad
\langle\eta(w,z),J_5\eta(w,z)\rangle
=4\|w\|^2\|W^\dagger z\|^2.
\quad}                                                   \tag{3}
\]

Thus support is a zero-expectation condition on physical monomials,
not a linear-kernel condition on \(\mathscr X\). The common-kernel
space proposed in the cloud handoff therefore does not define the
complete DTH-constrained five-replica relaxation.

There is a genuine linear contraction after replacing one holomorphic
bivector copy by a conjugate copy. On

\[
\widehat{\mathscr X}
=\overline{\wedge ^2V}_{12}\otimes
  \wedge ^2V_{34}\otimes V_5
\]

the map

\[
\widehat{\mathcal C}_{\rm supp}
  (\bar w_{12}\otimes w_{34}\otimes z_5)
=w_{34}\otimes(W^\dagger z)_{\bar V}                  \tag{4}
\]

is complex-linear and equivariant. This is a mixed-conjugate, or
star-moment, lift; it is not the all-covariant \(S_5\) Schur--Weyl
lift used for the first Pluecker obstruction.

The dependency-free exact checker is
\`verification/agent_dth_support_lift.py\`.

## 1. The phase obstruction

Replace \(w\) by \(iw\). The proposed source vector changes by

\[
\eta(iw,z)=(iw)\otimes(iw)\otimes z=-\eta(w,z).         \tag{5}
\]

On the proposed target, however,

\[
(iw)\otimes((iW)^\dagger z)
=(iw)\otimes(-iW^\dagger z)
=w\otimes W^\dagger z.                                 \tag{6}
\]

A real-linear map sends the left side of (5) to the negative of its
value on \(\eta(w,z)\), whereas (6) is unchanged. Choosing \(w,z\)
with \(W^\dagger z\ne0\) contradicts (1). This proves the no-go even
before covariance is considered.

Equivalently, the source has phase bidegree \(w^2z\), while the target
written in (1) has phase bidegree \(w\bar w z\). A fixed reshuffling,
transpose, Hodge map, or tensor identification cannot change that
bidegree.

## 2. The exact Hermitian support identity

For a two-tensor \(w\), its first reduced operator is

\[
\rho_1(w)=WW^\dagger .                                  \tag{7}
\]

Its second reduced operator is \(W^{\mathsf T}\bar W\). Skew
symmetry gives

\[
W^{\mathsf T}\bar W=-W\bar W=WW^\dagger,               \tag{8}
\]

because \(W^\dagger=-\bar W\). The swap identity therefore gives

\[
\begin{aligned}
\langle\eta,F_{15}\eta\rangle
&=\|w\|^2\langle z,WW^\dagger z\rangle,\\
\langle\eta,F_{25}\eta\rangle
&=\|w\|^2\langle z,WW^\dagger z\rangle .                \tag{9}
\end{aligned}
\]

The same calculation on replicas \(3,4\) proves (3). Notice that
(3) uses only skew symmetry; decomposability of \(w\) is not needed.

For \(V=(\mathbb C^3)^{\otimes3}\), each \(F_{a5}\) in (2) is the
global swap

\[
F_{a5}=\prod_{r=1}^3F_{a5}^{(r)}.                      \tag{10}
\]

Hence \(J_5\) is exactly covariant under local \(U(3)^3\) and under
physical-site permutations. It is Hermitian and commutes with the
first-four replica symmetries. It is not positive on the full lifted
linear space.

## 3. Why support is not a linear kernel

Let \(P_{12}^-P_{34}^-P_{(12)(34)}^+\) impose pair antisymmetry and
pair-exchange symmetry, and let \(\mathcal A_4\) antisymmetrize the
first four replicas. Put

\[
\mathscr K=\ker\mathcal A_4\cap
\operatorname{Sym}^2(\wedge ^2V)\otimes V .            \tag{11}
\]

The first four replicas in \(\mathscr K\) have Young symmetry
\((2,2)\). Adding replica five has exactly the two symmetry types

\[
(3,2),\qquad(2,2,1).                                    \tag{12}
\]

On these two summands \(J_5\) has eigenvalues respectively \(+2\)
and \(-2\). Equivalently, in the group algebra restricted to
\(\mathscr K\),

\[
J_5^2=4I,
\qquad
P_+=\frac{2I+J_5}{4},
\quad
P_-=\frac{2I-J_5}{4}.                                  \tag{13}
\]

One can check (13) directly in the group algebra: impose the two pair
antisymmetries and pair-exchange symmetry, subtract the full
four-fold antisymmetrizer, and expand \(J_5^2-4I\). The verifier does
exactly this in the regular representation of \(S_5\), so the identity
does not depend on a chosen physical dimension.

Take an orthonormal triple \(e_1,e_2,e_3\), set

\[
w=e_1\wedge e_2,\qquad z=e_3.                           \tag{14}
\]

This is a physical support monomial. By (3), its \(J_5\)-expectation
is zero. Equations (13) then give

\[
\|P_+\eta\|^2=\|P_-\eta\|^2=\frac12\|\eta\|^2,          \tag{15}
\]

so both components are nonzero. The unitary orbit of each nonzero
component spans its irreducible symmetry type in (12). Therefore the
unitary orbit of the single support monomial (14) spans all of
\(\mathscr K\). Since the support condition is unitary invariant,
all vectors in that orbit are again support monomials. This proves

\[
\boxed{\quad
\operatorname{span}_{\mathbb C}\{
  \eta(w,z):w\text{ decomposable},\ W^\dagger z=0
\}=\mathscr K.
\quad}                                                   \tag{16}
\]

Multiplying \(z\) by arbitrary phases shows that the real span is the
underlying real space of \(\mathscr K\) as well. Thus a real- or
complex-linear map annihilating every physical support monomial must
vanish identically on the first-Pluecker source.

This also explains geometrically what goes wrong with a kernel
compression. On a physical support monomial the positive and negative
\(J_5\) branches balance:

\[
\langle J_5\rangle
=2\|P_+\eta\|^2-2\|P_-\eta\|^2=0.                     \tag{17}
\]

Neither branch vanishes.

## 4. Correct mixed-conjugate contraction

Regard \(\bar w\) as an independent vector in
\(\overline{\wedge ^2V}\). Contract its first index with \(z\):

\[
\bar w_{12}\otimes z_5
\longmapsto
\sum_j\left(\sum_i\bar W_{ij}z_i\right)\bar e_j.
                                                                \tag{18}
\]

The coefficient in parentheses is exactly
\((W^\dagger z)_j\). Leaving the second bivector as a spectator gives
(4), with normalization one in the coefficient convention used
above. Contracting the second index instead changes only the overall
sign because \(W^{\mathsf T}=-W\).

Under a unitary \(U\),

\[
\bar w\mapsto(\bar U\otimes\bar U)\bar w,
\quad z\mapsto Uz,
\quad W^\dagger z\mapsto\bar U(W^\dagger z).            \tag{19}
\]

Thus the natural target is
\(\wedge ^2V\otimes\bar V\), and (4) is equivariant. For
\(V=(\mathbb C^3)^{\otimes3}\), the evaluation in (18) is the product
of the three local \(\bar{\mathbb C}^3\otimes\mathbb C^3\) evaluation
maps, so local \(U(3)^3\) covariance and physical-site permutation
covariance are exact.

The price is unavoidable: the five replica slots no longer all carry
the same covariant representation. Full \(S_5\) permutation symmetry
is replaced by mixed covariant/contravariant contraction algebra.

## 5. The known obstruction vector

In the exact point--point--edge realization of the cloud vector
\(\xi\), direct integer arithmetic gives

\[
\|\xi\|^2=64,
\qquad
\langle\xi,J_5\xi\rangle=-40,
\qquad
J_5^2\xi=4\xi.                                         \tag{20}
\]

Consequently

\[
\|P_+\xi\|^2=22,
\qquad
\|P_-\xi\|^2=42.                                       \tag{21}
\]

Thus \(\xi\) fails the physical support equation already at the exact
Hermitian level. It cannot be assigned a value
\(\mathcal C_{\rm supp}\xi\) for the proposed holomorphic kernel map,
because that map does not exist. The correct statement is that its
support localizing functional equals \(-40\), whereas every physical
monomial has a nonnegative value and every physical DTH monomial has
value zero.

## 6. Consequence for the next finite decision

The proposed space

\[
\ker\mathcal A_4\cap\ker\mathcal C_{\rm supp}
\cap\ker\mathcal C_\Omega
\]

is not a valid holomorphic first-level model of the DTH variety.
There are two exact repairs:

1. retain the holomorphic five-replica source and impose the Hermitian
   star-polynomial equation
   \(\langle\eta,J_5\eta\rangle=0\), together with appropriate
   Hermitian localizing multipliers; or
2. pass to the mixed-conjugate lift (4), where support is a genuine
   linear contraction, and redo the symmetry reduction in the mixed
   tensor algebra.

The Omega equation is holomorphic and can still have a linear map on
the original source. The obstruction found here is specific to the
Hermitian support incidence \(W^\dagger z=0\).

