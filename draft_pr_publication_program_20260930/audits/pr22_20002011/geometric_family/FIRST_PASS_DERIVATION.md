# Independent geometric first pass

Audit scope: PR 22, head `5dff69d1f25ac585a87bd8c71bc9d9c136e8c13c`, literal AIM Conjecture 1 / Problem 30, records 20002011 and 20002052. This is validation of the author's single existing attempt, not a new attempt at a repaired conjecture.

Before this derivation was sealed, I read only the frozen `SOURCE_STATUS.md`, the two exact source records, the snapshot inventory, applicable instructions, and the original AIM document. I did not open original verification scripts or outputs, historical reviews, parent reconstruction, or sibling mathematics. The candidate contains assertions about old checks and prior literature; those assertions have not supplied evidence for this first pass.

## Exact criterion

The original AIM document is the version dated 15 October 2003. Printed pp. 16–17 define a primitive by a functional first variation valid at every background metric and every conformal direction. Conjecture 1 on p. 17 requires a decomposition of natural top-degree forms into constant times the standard Q density, a pointwise conformal invariant density, and the conformal gradient of an integral of a natural local density. Problem 30 on p. 28 repeats the same statement. Printed p. 18 distinguishes a weaker decomposition with an arbitrary exact divergence and restricts the intended polynomial weight class by derivative count plus twice curvature count equal to dimension. The two records are one target.

Success in this family means proving that the displayed universal density satisfies that exact hypothesis on a genuine smooth closed six-manifold, but violates a necessary condition for the exact conclusion. It does not mean resolving any formally self-adjoint replacement or claiming a new counterexample priority. The published-priority assertion requires a later primary-source check.

## Necessity of symmetry

Use the affine coordinates `u` on a fixed conformal class, `g_u = exp(2u) g`. If a twice differentiable functional has first derivative `dF_u(v) = integral v H_{g_u}`, its second mixed derivatives in two fixed smooth directions give

`integral phi D H(psi) = integral psi D H(phi)`.

Here `D H` differentiates the entire top form, including volume. Smooth natural finite-order local densities define such twice differentiable functionals on the compact manifold. Thus every allowed local conformal gradient has a symmetric linearization. A pointwise conformally invariant density has zero derivative. The critical Q density has the formally self-adjoint critical operator as its derivative, as the original document explicitly states. In the conformally flat torus class there is also a direct check: relative to the global flat background its standard Q density is a constant multiple of the Euclidean third Laplacian of `u`, so its linearization is symmetric. Addition of a pointwise invariant does not affect this conclusion. Hence the asserted sum must have symmetric linearization.

This is a statement about the one-form `v -> integral v H` on conformal classes, not the scalar functional `integral H`. The latter can be identically zero even when the former has nonzero exterior derivative.

## Full density variation

In dimension six set `B = |P|_g^2`, `Delta = div grad`, `J = R/10`, `P = (Ric - J g)/4`, and `S = (Delta B) dV`. Constant rescaling sends `B` to scale to the power -4, `Delta B` to scale to the power -6, and `dV` to scale to the power 6. The density is polynomial and parity even: expanding the Laplacian gives complete contractions of `P Delta P` and `nabla P nabla P`, with curvature count two and derivative count two. Its integral is zero on every closed oriented six-manifold by Stokes' theorem. In particular its integral is conformally invariant.

For a conformal direction `psi`, differentiation gives `dot P_ij = - Hess_ij psi`, `dot B = -4 psi B - 2 P^{ij} Hess_ij psi`, and

`dot(Delta b) = -2 psi Delta b + 4 <dpsi,db> + Delta dot b`.

Volume contributes `+6 psi Delta B`. Expanding `Delta(psi B)` cancels every zeroth-order `psi Delta B` term and leaves

`D psi = -4 div(B grad psi) - 2 Delta T psi`, where `T psi = P^{ij} Hess_ij psi`.

The first operator is symmetric. Two integrations by parts give `T* h = nabla_j nabla_i(P^{ij} h)`, so

`D - D* = -2 (Delta T - T* Delta)`.

No boundary terms are omitted: the manifold below is closed, and all test functions are smooth global functions.

## Closed-manifold realization and jets

Take the torus `R^6 / (2 pi Z)^6` with its flat metric. In a coordinate ball of radius `b < pi`, choose a smooth radial cutoff `chi` that is identically one on a ball of radius `a`, with `0 < a < b`, and zero outside radius `b`. For example, with `h(t)=exp(-1/t)` for `t>0` and zero for `t<=0`, use

`chi(r) = h(b^2-r^2) / (h(b^2-r^2) + h(r^2-a^2))`.

The denominator is positive everywhere. Extend `f = chi(r) x1 x2 x3` by zero outside this chart, and choose `psi = f`. Both are globally smooth periodic functions. The metric `g = exp(2f) g_flat` is smooth, positive definite, globally conformal to flat, and defined on a closed oriented manifold. On a neighborhood of `p=0`, `f=psi=x1 x2 x3`.

For a conformal Euclidean metric the exact Schouten formula is

`P_ij = -f_ij + f_i f_j - (|df|_0^2/2) delta_ij`.

At zero, the zero-, first-, and second-order jets of `f` vanish. Consequently `g_ij=delta_ij`, first and second derivatives of `g` vanish, the Christoffel symbols and their first derivatives vanish, and the curvature vanishes there. Raising indices and passing from partial to covariant derivatives therefore produces no hidden terms in the jets being used. In particular,

`P(0)=0`, `nabla_k P_ij(0)=-f_ijk(0)`, and `nabla_k Hess_ij psi(0)=psi_ijk(0)`.

Potential connection terms in the third derivative of `psi` are a Christoffel coefficient times its second derivative or a first derivative of a Christoffel coefficient times its first derivative; all vanish at zero. Terms involving a second derivative of a Christoffel coefficient in higher jets are multiplied by a vanished lower jet whenever relevant to the present product calculation. This calculation never substitutes arbitrary covariant fourth derivatives by commuting them.

The cubic is harmonic in the Euclidean coordinates. The trace formula is `J = exp(-2f)(-Delta_0 f - 2|df|_0^2)`, so `J` vanishes to order four at zero and `dJ(0)=0`. Contracted Bianchi gives `div P(0)=0`. Also `psi(0)=dpsi(0)=Hess psi(0)=Delta psi(0)=0`.

The product-rule expansion of `Delta(P^{ij} Hess_ij psi)` at zero has only the cross term surviving:

`Delta T psi(0) = 2 sum_ijk (-f_ijk) psi_ijk = -12`.

There are six ordered permutations of the three distinct indices and each third derivative equals one. The double-divergence expansion of `T*(Delta psi)` contains `P Hess(Delta psi)`, twice `div P` paired with `d(Delta psi)`, and `div div P` times `Delta psi`. All vanish at zero. The symmetric term `div(B grad psi)` also vanishes because `B(0)=dB(0)=0`. Hence

`D psi(0)=24`, `D* psi(0)=0`, and `(D-D*)psi(0)=24`.

This is a local calculation of a global smooth operator; it yields a genuine integral obstruction. Write `w=(D-D*)psi`. It is a smooth nonzero global function. Choosing the further smooth conformal direction `phi=w` gives the particularly direct witness

`integral phi D psi - integral psi D phi = integral w^2 dV > 0`.

Alternatively, continuity gives a positive neighborhood and any nonzero nonnegative bump function supported there gives the candidate's stated witness. The first construction does not require estimating the neighborhood. No local-to-global extension assertion is being assumed without a cutoff.

## Boundary controls and first-pass conclusion

The obstruction uses neither a manifold boundary, a noncompact domain, an orientation-odd invariant, a noncritical weight, nor a nonpolynomial invariant. Changing the Laplacian sign changes the sign of the obstruction and not its nonvanishing. The six-dimensional example disproves a universal conjecture over even dimensions; it does not assert failure in dimension two or four. `integral S=0` only means `D*1=0`; it does not imply `D=D*`. The arbitrary-divergence version accommodates `S` by using this very divergence and is not contradicted.

First-pass mathematical conclusion: the displayed construction is an exact counterexample to the literal original statement, with no mathematical gap found in this geometric family. Published prior status and finite verification results remain to be checked after this seal. Their agreement cannot retroactively supply the universal derivation above.
