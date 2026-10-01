# Local strong Lefschetzness and the zeroth symmetric component: a top-Hessian obstruction

**30004526 / OWR-2654827-002. Scoped characteristic-zero partial result; original question unresolved, 2/5 approaches.** No novelty or human peer-review claim.

## 1. Exact source and the meaning of Q(0)

[OWR31/2020, printed pp.1540–1542, Question4](https://publications.mfo.de/bitstream/handle/mfo/3804/OWR_2020_31.pdf?isAllowed=y&sequence=4) concerns a **local, possibly nongraded Artinian Gorenstein algebra** (A,m). Its associated graded algebra A*=gr_m A has the symmetric-decomposition filtration by ideals C(a), with Q(a)=C(a)/C(a+1). The unadorned Q(0) in the question is A*/C(1). It is not a chosen Jordan block; nor is it an arbitrary central-simple module associated to a principal ideal. The report discusses those related decompositions separately.

The accompanying contribution, pp.1549–1550, defines local strong Lefschetzness by the existence of ell in m whose nilpotent multiplication operator has Jordan partition P_ell=H(A)^vee, the conjugate of the Hilbert sequence sorted into a partition. This is often called **strong Lefschetz Jordan type**. One must allow nonlinear ell and a nonsymmetric local Hilbert function. Replacing A by an already standard-graded Gorenstein algebra makes Q(0)=A and misses the genuine question.

[Iarrobino–Macias Marques, *Reducibility of a family of local Artinian Gorenstein algebras*](https://arxiv.org/abs/2112.14664), Definition1.3 and Question2.32(b), restates the implication A strong Lefschetz => Q_A(0) strong Lefschetz as open in that work. Its question about A versus A* is distinct. That source attributes the October2020 workshop question to Johanna Steinmeyer. A targeted primary-source search did not establish a full later resolution; this is not an exhaustive present-day openness assertion.

All new deductions below are over an infinite field k of characteristic zero. This restriction makes ordinary differentiation equivalent, after factorial rescaling, to the divided-power contraction convention of the source. No assertion for arbitrary positive characteristic is made.

Let R=k[[x_1,...,x_r]], S=k[X_1,...,X_r], and let

$$A=R/\operatorname{Ann}(F),\qquad F=F_j+F_{j-1}+\cdots,\quad F_j\ne0,$$

where x_i acts by partial differentiation. The socle degree is j. Macaulay duality gives a vector-space isomorphism A -> M=R·F, a -> a(D)F, intertwining multiplication by ell with ell(D) on M. The primary symmetric-decomposition identity is

$$B:=Q_A(0)\simeq R/\operatorname{Ann}(F_j).\tag{1}$$

In particular B is standard-graded Gorenstein and H(B)_i<=H(A)_i. Write H(A)=(1,h_1,...,h_(j-1),1), and s=dim B_1=dim B_(j-1). The source's inverse-system theory and Hessian/Lefschetz framework are credited; the calculations here are explicit restricted consequences.

## 2. An exact rank formula that permits nonlinear Lefschetz elements

**Proposition.** Suppose j>=3 and ell in m has ell^j!=0. Write a representative ell=L+terms of order at least2, where L=sum c_i x_i. Then

$$\operatorname{rank}(m_\ell^{j-2}:A\to A)=2+\operatorname{rank}\operatorname{Hess}(F_j)(c).\tag{2}$$

The Hessian may be computed in all ambient variables; dummy variables contribute zero rows and columns. Neither lower-degree terms of F nor higher-order terms of ell can repair a deficit in this rank.

**Proof.** Since ell^j acts on F only through L^j acting on F_j,

$$\ell(D)^jF=j!F_j(c)\ne0.$$

Put T=ell(D)^(j-2) on M. The space M is spanned by F and all its partial derivatives.

- TF has degree2, with nonzero leading quadratic D_L^(j-2)F_j. It is nonzero because applying D_L² to it gives j!F_j(c).
- For each first partial D_iF, T(D_iF) has degree at most1. Its linear term is

$$D_L^{j-2}D_iF_j=(j-2)!\sum_k (\partial_i\partial_kF_j)(c)X_k.$$

Thus these linear terms span a space of dimension d=rank Hess(F_j)(c).
- Images of partials of order at least2 are constants or zero. The nonzero constant T(D_L²F)=j!F_j(c) belongs to the image.

Modulo constants, the first-partial images therefore contribute exactly d dimensions. The single degree-two image adds one independent dimension, and constants add one. These exhaust the image, giving d+2. Higher terms in ell only change lower-degree parts of the displayed vectors, so the argument covers every ell in m, not just a linear form. QED.

## 3. A necessary Hilbert/Hessian equality

Let m_H=min(h_1,...,h_(j-1)). For any positive interior Hilbert values,

$$\sum_{p\in H(A)^\vee}\max(p-(j-2),0)=m_H+2.\tag{3}$$

Indeed the first column of the conjugate diagram has length j+1 and contributes3. Every other column has length at most j-1, since h_0=h_j=1. Such a column contributes1 exactly when every interior entry is at least its column index. There are m_H-1 such columns.

Combining (2) and (3) proves:

**Corollary.** If (A,ell) is strong Lefschetz in the source's local Jordan sense, then F_j(c)!=0 and

$$\operatorname{rank}\operatorname{Hess}(F_j)(c)=m_H.\tag{4}$$

In particular, if all interior values H(A)_i are at least s, then m_H=s because h_(j-1)=s. In that case the top Hessian must have full essential-variable rank s. The multiplication map L^(j-2):B_1 -> B_(j-1) is then an isomorphism, by the standard apolar pairing/Hessian identity.

The equality h_(j-1)=s follows directly from inverse systems: m^(j-1)A is represented by the span of partial derivatives of F of orders at least j-1. Its degree-one parts are exactly the order-(j-1) derivatives of F_j, a space of dimension s, and its constants have dimension1. Quotienting m^j gives s.

This controls the **first** Hessian only. It does not prove all higher-degree Lefschetz maps for B. If H(A) dips below s in an interior degree, (4) allows a smaller Hessian rank; that case is also not excluded.

## 4. Complete equivalence in socle degree three

For j=3, write H(A)=(1,r,s,1), with r>=s, and H(B)=(1,s,s,1). The restricted question has a negative answer:

$$A\text{ has strong Lefschetz Jordan type}\quad\Longleftrightarrow\quad B=Q_A(0)\text{ is strong Lefschetz}.\tag{5}$$

**Proof.** Here m_H=s. If A is strong Lefschetz, (4) forces a nonsingular essential Hessian and F_3(c)!=0. These are exactly the degree1-to2 and degree0-to3 Lefschetz conditions for the graded cubic Gorenstein algebra B; the remaining maps follow from them and duality.

Conversely, choose a linear form L that is strong Lefschetz on B. Then F_3(c)!=0 and its Hessian rank is s. Formula(2) gives rank m_L=s+2 on A. Also rank m_L²=2: the image of F has a nonzero linear part, all first-partial images are constants, and L³F!=0 supplies a nonzero constant. Rank m_L³=1 and m_L⁴=0. Consequently the Jordan partition is

$$(4,\underbrace{2,\ldots,2}_{s-1},\underbrace{1,\ldots,1}_{r-s})=H(A)^\vee.$$

This is exactly local strong Lefschetzness. QED.

This low-socle reduction is consistent with, and should be credited alongside, [Elias–Rossi's classification of short Gorenstein local rings](https://arxiv.org/abs/0911.3565). In particular their canonical-graded and cubic-classification results are prior structure theorems, not campaign discoveries. The direct proof above does not need to assume a normal form or invoke the classification as a black box.

## 5. A whole quartic Perazzo deformation family is excluded

Consider the ordinary quartic

$$G=XU^3+YU^2V+ZV^3.$$

For every polynomial F=G+F_3+F_2+F_1+F_0, even allowing additional variables in the lower-degree summands, the associated local apolar algebra cannot be strong Lefschetz.

The homogeneous apolar Hilbert function of G is

$$H(R/\operatorname{Ann}G)=(1,5,6,5,1).$$

Here is a direct calculation: the five first derivatives U³,U²V,V³,3XU²+2YUV,YU²+3ZV² are independent. The second derivatives span six independent quadrics, which can be chosen as

$$U^2,\ UV,\ V^2,\ 6XU+2YV,\ 2YU,\ 6ZV.$$

The third derivatives span all five essential linear variables, and the fourth derivatives span constants. Thus the stated Hilbert function follows without a numerical rank tolerance.

The Hessian has a zero3-by3 block in the X,Y,Z coordinates. Its block form is [[0_(3x3),C],[C^T,D]], with only two U,V coordinates in the second block. Its rank is at most4 for every point: its image is contained in im(C) in the first three coordinates, of dimension at most2, together with the final two coordinates. In fact its generic rank is4, but only the upper bound is needed.

For any such lower-degree deformation F, the quotient relation(1) gives H(A)_1>=5 and H(A)_2>=6; also H(A)_3=5. Hence m_H=5. Equation(4) would require Hessian rank5, contradicting the rank-at-most4 bound. Extra variables in lower terms only append zero rows to the top Hessian and cannot change this argument. This rules out a tempting construction family; it is not a counterexample to the original implication.

## 6. Exact gap and outcome

Route1 derived the top-Hessian rank formula, its Hilbert minimum constraint, and the complete cubic equivalence. Route2 tested the natural quartic Perazzo-leading-form mechanism and upgraded the observed obstruction to the all-lower-deformations proof above. Both routes stop before the general problem: higher Hessians, interior Hilbert dips, and other leading forms may behave differently.

No local AG algebra with A strong Lefschetz and Q_A(0) not strong Lefschetz has been constructed, and the implication has not been proved for arbitrary socle degree. Positive-characteristic variants are not settled. Recommended status **unsolved, 2/5**. Exact finite inverse-system and partition checks are supporting diagnostics; the all-parameter statements rest on the written rank proofs.
