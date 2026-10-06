# 30003713: known reductions and the remaining functor-decomposition gap

**Disposition:** unresolved in this investigation. The reduction below and the cited low-degree answers are known; they are not a new full solution. Originally prepared2026-09-30; historical model/reasoning labels are documentary self-attribution. Current independent AI verification is unrefereed, with no human peer review or proof-assistant certificate asserted.

## 1. Exact target and current literature

The [original OWR2018/2 report](https://ems.press/content/serial-article-files/46724), p.118, Question13 by Dan Petersen, asks for the homology of
\[
\mathfrak h=L(V)\otimes(\mathbb C\oplus E),\qquad E^2=0,
\]
for arbitrary finite-dimensional complex \(E,V\). It explicitly asks for a sum of polynomial functors in the two variables. The dataset's word “preferably” understates this requirement. Reporting an unevaluated Chevalley–Eilenberg complex or naming its kernels does not supply the requested decomposition.

The same question was posted by [Petersen in 2017](https://mathoverflow.net/questions/273196/homology-of-an-interesting-lie-algebra). The discussion already gives the adjoint-coefficient reformulation and the two-term tensor-algebra resolution; Petersen explicitly says that computing the resulting groups is the difficulty. Tosteson identifies the adjoint case with Whitehouse/cyclic-Lie modules. This is direct prior evidence against treating the elementary spectral-sequence collapse as a new answer.

Relevant later primary work includes:

- [Gadish–Hainaut, *Configuration spaces on a wedge of spheres and Hochschild–Pirashvili homology*](https://ahl.centre-mersenne.org/item/10.5802/ahl.213.pdf), *Annales Henri Lebesgue* 7 (2024), 841–902. Section1.3 describes complete decomposition through10 particles and additional infinite families, rather than an all-degree general decomposition. Section4.4 and the later work below explain the connection to the coefficient problem here.
- [Powell, *On fundamental structure underlying Lie algebra homology with coefficients tensor products of the adjoint representation*](https://arxiv.org/abs/2309.07607), 2023. Its main structure is a differential graded category built from a two-term complex; the abstract is not an assertion of a complete irreducible decomposition.
- [Powell, *Lie algebra homology with coefficients tensor products of the adjoint representation in relative polynomial degree2*](https://arxiv.org/abs/2507.03453v4), revised December2025 and [published March2026](https://doi.org/10.1080/10586458.2025.2608243). Theorem1 gives a complete answer in relative polynomial degree2. Proposition3.3 gives the preceding diagonal, and Example3.1 records the cyclic-Lie adjoint case. These are genuine advances, but their stated range is not the all-degree target.

The original OWR passage, the 2017 discussion, Gadish–Hainaut's computational-scope statement, and Powell's introduction, exact theorem, conventions, and relevant examples were inspected. No exact all-degree solution was located. No claim of exhaustive literature coverage is made.

The workshop/report volume is2018, while EMS states publication5January2019; the dataset's2019 citation is not inherently a date error. Current EMS PDF bytes differ from the absent historical checksum-bound PDF, although the literal target has been freshly read and visually checked. The exact Powell mathematical body checked is author arXivv4 of16December2025; its final published PDF was not independently compared. These source and historical execution limits are recorded in CURRENT_SOURCE_QUALIFICATION.md.

## 2. A canonical reduction, with its limitations explicit

Put \(L=L(V)\) and \(M=E\otimes L\). Then
\[
\mathfrak h=L\ltimes M,
\]
where \(M\) is abelian and \(L\) acts through its adjoint action on the second tensor factor.

The Chevalley–Eilenberg chains split by the number \(r\) of ideal factors. Since \([M,M]=0\), the differential preserves this number, and the weight-\(r\) summand is the coefficient complex
\[
C_*(L;\Lambda^rM)[r].
\]
This is an actual direct-sum decomposition of complexes, not merely a collapsed spectral sequence with an unexamined extension problem.

The enveloping algebra of the free Lie algebra is \(T(V)\). For the trivial **right** module use the right-free resolution
\[
0\longrightarrow V\otimes T(V)\xrightarrow{\ v\otimes a\mapsto va\ }T(V)\longrightarrow\mathbb C\longrightarrow0.
\]
Each nonempty tensor word has a unique first letter and tail, so multiplication bijects the source onto the augmentation ideal and is right linear. Tensoring over \(T(V)\) with a **left** coefficient module \(N\) therefore computes its homology by \(V\otimes N\to N\), \(v\otimes n\mapsto v\cdot n\). The separate left-free resolution \(T(V)\otimes V\) uses the last letter; it cannot simply be tensored with another left module. This establishes the convention for arbitrary coefficient modules, including the graded infinite-dimensional modules below. In our case write
\[
\delta_r:V\otimes\Lambda^r(E\otimes L)\longrightarrow\Lambda^r(E\otimes L),
\]
\[
\delta_r\bigl(v\otimes\bigwedge_{i=1}^r(e_i\otimes x_i)\bigr)
=\sum_{i=1}^r(e_1\otimes x_1)\wedge\cdots\wedge(e_i\otimes[v,x_i])\wedge\cdots\wedge(e_r\otimes x_r).
\]
Consequently
\[
H_n(\mathfrak h)\cong\operatorname{coker}\delta_n\oplus\ker\delta_{n-1},
\tag{1}
\]
with the second term omitted for \(n=0\). The two displayed terms have distinct polynomial degrees \(n\) and \(n-1\) in \(E\), so their distinction is canonical.

The Cauchy identity gives
\[
\Lambda^r(E\otimes L)\cong
\bigoplus_{\lambda\vdash r}S_\lambda(E)\otimes S_{\lambda'}(L).
\]
It reduces the unanswered part to evaluating, in every homogeneous degree of \(V\), the kernel and cokernel of
\[
V\otimes S_{\lambda'}(L(V))\longrightarrow S_{\lambda'}(L(V)).
\tag{2}
\]
Writing (1) or (2) is not a computation of those multiplicities. It repeats the prior reformulation.

## 3. Completely checked elementary layers

In homological degrees zero and one,
\[
H_0(\mathfrak h)=\mathbb C,\qquad
H_1(\mathfrak h)=(\mathbb C\oplus E)\otimes V.
\]
The second equality follows directly from abelianization.

The component of **polynomial degree one in \(E\)** is also known in all degrees of \(V\):
\[
H_1(\mathfrak h)_{E[1]}=E\otimes V,\qquad
H_2(\mathfrak h)_{E[1]}=E\otimes\operatorname{CycLie}(V),
\]
and \(H_n(\mathfrak h)_{E[1]}=0\) for \(n\ge3\). This is the adjoint-coefficient case, credited above. It must not be confused with the entire case \(\dim E=1\), which still has all polynomial weights in \(E\).

For \(d\ge2\), the cyclic-Lie character is
\[
\operatorname{ch}\operatorname{CycLie}_d
=p_1\ell_{d-1}-\ell_d,
\qquad
\ell_d=\frac1d\sum_{a\mid d}\mu(a)p_a^{d/a}.
\]
Equivalently it is the kernel in
\[
0\longrightarrow\operatorname{CycLie}_d(V)
\longrightarrow V\otimes L_{d-1}(V)
\xrightarrow{[\ ,\ ]}L_d(V)\longrightarrow0.
\]
The bracket map is onto because the free Lie algebra is generated by \(V\). The first components are \(\operatorname{Sym}^2V\), \(\Lambda^3V\), and \(S_{(2,2)}V\) in degrees2,3,4, respectively. Exact small-dimensional ranks were checked in `verify.py`; these are sanity checks of a known formula.

Boundary cases are consistent: \(E=0\) gives the usual homology of a free Lie algebra; \(V=0\) gives only \(H_0=\mathbb C\); for \(\dim V=1\), the whole algebra is abelian and
\[
H_n(\mathfrak h)=\Lambda^n\bigl((\mathbb C\oplus E)\otimes V\bigr).
\]

## 4. Translating Powell's recent theorem to the exact current algebra

The complete cited proof is used with an explicit auxiliary restriction: v4 Lemma5.2 is false at n=2, but its Theorem1 induction uses only n=r−1>=3 and has a separate r=3 base. The valid used-range proof and exact boundary counterexample are in CURRENT_POWELL_RANGE_QUALIFICATION.md. Every displayed formula below is unchanged.

This section records consequences of the cited theorem, not a new computation.

Let \(H_{r+1}(\mathfrak h)_{E[r],V[d]}\) denote the summand of polynomial degrees \(r\) in \(E\) and \(d\) in \(V\). It is the degree-\(d\) part of \(H_1(L;\Lambda^r(E\otimes L))\). Since taking symmetric-group coinvariants is exact in characteristic zero,
\[
H_1(L;\Lambda^r(E\otimes L))
\cong
\bigl(E^{\otimes r}\otimes H_1(L;L^{\otimes r})\otimes\operatorname{sgn}_r\bigr)_{S_r}.
\tag{3}
\]
The permutation action here is simultaneous on the tensor factors; it is important to retain the sign representation from the exterior power.

Powell's Proposition3.3 yields, for \(r\ge1\),
\[
H_{r+1}(\mathfrak h)_{E[r],V[d]}=0\quad(d\le r),
\]
\[
H_{r+1}(\mathfrak h)_{E[r],V[r+1]}
\cong\Lambda^rE\otimes\operatorname{Sym}^{r+1}V.
\tag{4}
\]
His Theorem1 yields, for \(r>1\),
\[
H_{r+1}(\mathfrak h)_{E[r],V[r+2]}
\cong
\operatorname{Sym}^rE\otimes\Lambda^{r+2}V
\ \oplus\ 
\Lambda^rE\otimes S_{(r,1,1)}V.
\tag{5}
\]
For \(r=1\), the corresponding answer is \(E\otimes\Lambda^3V\), with no second summand. These formulas are compatible with the elementary adjoint layer. The rational-coefficient theorem base-changes to \(\mathbb C\), since tensoring with \(\mathbb C\) is exact.

Equations (4)–(5) do not determine the components with unrestricted \(d-r\). That is exactly where the general Schur-kernel calculation persists. An Euler-characteristic identity gives only the difference between the kernel and cokernel characters, not the two actual representations separately.

## 5. Stopping point

The attempted route reaches a known equivalent coefficient-homology problem, and the cited papers inspected here evaluate specified diagonals or families; this investigation has not evaluated the unrestricted decomposition. No new mechanism was found to resolve the remaining ranks and multiplicities. This investigation therefore stops after one substantive attempt, with a precise **unresolved** outcome rather than a candidate full solution.

A meaningful reopening would require an all-degree calculation of (2), or a different structural model whose homology is actually evaluated in polynomial-functor terms. Renaming the kernels, assuming that virtual character cancellations cannot occur, or presenting a bounded-degree computation as a general answer would not meet the source target.
