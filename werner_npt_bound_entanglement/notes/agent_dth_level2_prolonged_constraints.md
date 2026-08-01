# Exact prolonged DTH constraints at degree three

## Scope

This note records the density-level equations needed after the positive
fixed-marginal test.  It distinguishes the holomorphic Omega quotient from
the conjugate-linear support equation and proves that both descend through
the seven-to-five marginal without a normalization factor.

Let

\[
H=(\mathbb C^3)^{\otimes3},\qquad A=\wedge^2H.
\]

For (w=\operatorname{vec}W\in A), use the normalized skew-matrix
convention

\[
W=\frac{u_0u_1^{\mathsf T}-u_1u_0^{\mathsf T}}{\sqrt2}.
\]

Define the two polarized contractions

\[
q(w,z)=\operatorname{Tr}(D_zW),
\qquad
s(\bar w,z)=W^\dagger z.
\]

The first is bilinear in ((w,z)).  The second is linear in
((\bar w,z)), which is why it belongs on a partial-transpose face rather
than in the holomorphic ket kernel.

## Anchored degree-three maps

On the ordered tensor products define

\[
\mathcal C_{\Omega,3}
 (w_1\otimes w_2\otimes w_3\otimes z)
=q(w_1,z)\,w_2\otimes w_3,
\tag{1}
\]

and

\[
\mathcal C_{S,3}
 (\bar w_1\otimes w_2\otimes w_3\otimes z)
=w_2\otimes w_3\otimes s(\bar w_1,z).
\tag{2}
\]

On the pair-symmetric degree-three Grassmann source, anchoring any of the
three bivector copies gives a unitarily equivalent map and the same kernel.
Equivalently one may average the three anchored maps after canonically
identifying their output factors.  On a physical monomial the formulas are

\[
\mathcal C_{\Omega,3}(w^{\otimes3}\otimes z)
=q(w,z)w^{\otimes2},
\]

\[
\mathcal C_{S,3}(\bar w\otimes w^{\otimes2}\otimes z)
=w^{\otimes2}\otimes W^\dagger z.
\]

Thus both vanish under the minimal DTH equations.

## Correct moment equations

Let (T\succeq0) be a degree-three moment.  The holomorphic equation is

\[
\boxed{
\mathcal C_{\Omega,3}T\mathcal C_{\Omega,3}^\dagger=0.
}
\tag{3}
\]

Positivity makes (3) equivalent to

\[
\operatorname{ran}T\subseteq\ker\mathcal C_{\Omega,3}.
\]

For support, take the partial transpose on the anchored bivector factor.
The correct equation is

\[
\boxed{
T^{\Gamma_{A_1}}\succeq0,
\qquad
\mathcal C_{S,3}T^{\Gamma_{A_1}}
 \mathcal C_{S,3}^\dagger=0.
}
\tag{4}
\]

Equivalently,

\[
\operatorname{ran}T^{\Gamma_{A_1}}
 \subseteq\ker\mathcal C_{S,3}.
\]

Putting (2) directly on the holomorphic range of (T) would be incorrect:
it would replace (W^\dagger z) by a different bilinear contraction.

Every physical DTH moment

\[
T=\sum_jp_j
 |w_j^{\otimes3}\otimes z_j\rangle
 \langle w_j^{\otimes3}\otimes z_j|
\]

satisfies (3)--(4) term by term.

## Exact descent to five replicas

Let

\[
R=\operatorname{Tr}_{A_3}T,
\]

with the final (z) factor retained.  Let

\[
\mathcal C_{\Omega,2}(w_1\otimes w_2\otimes z)
=q(w_1,z)w_2,
\]

\[
\mathcal C_{S,2}(\bar w_1\otimes w_2\otimes z)
=w_2\otimes s(\bar w_1,z).
\]

For every operator (T), direct contraction of the third bivector indices
gives

\[
\boxed{
\operatorname{Tr}_{A_3}
 \left(\mathcal C_{\Omega,3}T
 \mathcal C_{\Omega,3}^\dagger\right)
=
\mathcal C_{\Omega,2}R\mathcal C_{\Omega,2}^\dagger.
}
\tag{5}
\]

Partial trace and partial transpose act on disjoint factors, so

\[
\operatorname{Tr}_{A_3}(T^{\Gamma_{A_1}})
=R^{\Gamma_{A_1}}.
\]

The same index contraction yields

\[
\boxed{
\operatorname{Tr}_{A_3}
 \left(\mathcal C_{S,3}T^{\Gamma_{A_1}}
 \mathcal C_{S,3}^\dagger\right)
=
\mathcal C_{S,2}R^{\Gamma_{A_1}}
 \mathcal C_{S,2}^\dagger.
}
\tag{6}
\]

Equations (5)--(6) prove that the prolonged constraints automatically imply
the established five-replica constraints on the marginal.  There is no
extra scalar factor: the contracted bivector inner product is exactly the
one already present in the partial trace.

## Grouped PPT cut census

The grouped degree-three factors are

\[
A_1:A_2:A_3:H_z.
\]

A physical moment is fully separable across these four factors, hence PPT
across every grouped cut.  Pair symmetry and the equivalence of a cut with
its complement under full transpose reduce the nontrivial cuts to three
representatives:

\[
\boxed{
\Gamma_A,\qquad \Gamma_{H_z},\qquad \Gamma_{A_1A_2}.
}
\tag{7}

All one-(A) cuts are pair-conjugate; an (A+H_z) cut is complementary to
a two-(A) cut; a two-(A+H_z) cut is complementary to a one-(A) cut;
and the three-(A) cut is complementary to the (H_z) cut.

## Consequence for the hierarchy

The logical order of tests is now exact:

1. solve the PSD fixed-marginal problem on the post-Omega source;
2. if feasible, impose (4) on the one-(A) partial-transpose face;
3. then impose the two remaining grouped PPT representatives in (7).

Infeasibility at any stage is a valid convex-hull obstruction.  Feasibility
at any finite relaxation is not a physical DTH witness.
