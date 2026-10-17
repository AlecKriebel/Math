# Quantum-symmetrizer adjudication: two different coefficient statements

13 October 2026. Authored mathematical verification and qualification.

## Result and scope

For the four-point permutation solution

\[
 X=\mathbb Z/4,\qquad r(x,y)=(y,x+1),
\]

over every field of characteristic different from 2, the following statements have complete elementary proofs below.

1. The image complex of the signed quantum symmetrizer is **not** a bimodule resolution of its structure algebra. There are two independent degree-2 homology classes of weight 3. This independently verifies the core of Ferudun's Theorem 1.3(a), an existing unrefereed claim, and gives a negative answer to the precisely formulated Farinati--García Galofre Question 44.
2. With the character sending every generator to **0**, no chain quotient through which the quantum symmetrizer factors can make the comparison a quasi-isomorphism. The obstruction is a missing class in Hochschild homology in degree and weight 3; dually the cohomology comparison is noninjective. This independently verifies the core of Ferudun's Theorem 1.3(b).
3. With the character sending every generator to **1**, the **same four-point example does admit an explicit chain quotient on which the comparison is a quasi-isomorphism**. The quotient kills just the line spanned by the all-sum tensor in each degree at least 2. This is an all-degree statement, proved below, rather than an extrapolation from finite computations. It does not claim to be a quotient by an algebra ideal or a coefficient-independent bimodule construction.

Thus the zero-character obstruction must not be reported as ruling out every constant-character quotient. Statement 3 does not refute the scope-qualified assertions in Ferudun's paper: its Remark 3.3 and concluding section explicitly discuss only one quotient for the constant character and leave other quotients unexamined. It does qualify any broader reading of the headline.

The original brief OWR problem still has a **source-scope hold** if the intended task is the universal constant-character suitable-quotient question. Neither a universal positive construction nor a constant-character counterexample for all allowed quotients is established here. There is no novelty claim for Statements 1 or 2; both are credited to Ferudun. Statement 3 is an independently derived qualification, with no claim that it is new to the literature.

## 1. Primary-source contract

Lebed's Problem 2 on printed p. 3237 asks: “Is the quantum symmetriser QS bijective for general solutions?” The preceding paragraph concerns a relation between braided and Hochschild cohomology, and the following paragraph cites involutive and idempotent positive cases. It does not specify coefficients, characteristic, quotient, degree, or permitted solution class. [Original OWR report, pp. 3237--3238](https://ems.press/content/serial-article-files/46831?nt=1).

The relevant conventions are as follows.

- The signed braiding is **\(-r\)**, so \(QS_2=1-r\), not \(1+r\). On chains the map goes from braided to Hochschild chains; precomposition reverses the direction on cochains. Farinati--García Galofre (FGG), Definition 31 and Theorem 32, p. 18, and Corollaries 42--43, p. 22, identify the image with the Nichols-image complex. Question 44, p. 22, asks whether that particular image is a bimodule resolution. [FGG, arXiv v2](https://arxiv.org/abs/1508.07970v2), [journal DOI](https://doi.org/10.1016/j.jpaa.2016.04.010).
- Lebed's linear bimodule definition permits noninvertible generator actions. The idempotent result is a quasi-isomorphism for a specified critical quotient, with matching arbitrary bimodule coefficients; it is not a raw tensor-space bijectivity theorem. See Definition 3.1 and Theorem 2, pp. 8--10, and Theorems 5--6, pp. 19--20. [Lebed, idempotent braidings, arXiv v1](https://arxiv.org/abs/1607.08081v1), [journal DOI](https://doi.org/10.1142/S0218196717500229).
- The discussion in *Plactic monoids: a braided approach*, §6, p. 17, distinguishes the cochain map from its induced cohomology map. Section 7, p. 18, distinguishes the ordinary character \(\epsilon_1\), often omitted in notation, from the zero character \(\epsilon_0\). This is evidence against silently identifying the two readings of the OWR problem. [Lebed, Plactic, arXiv v1](https://arxiv.org/abs/1612.05768v1), [journal DOI](https://doi.org/10.1016/j.jalgebra.2020.08.010).
- Ferudun's manuscript is dated 1 October 2026 and publicly labels itself unrefereed and AI-assisted. Theorem 1.3 is the pre-existing four-point claim; Remark 3.3 and §7 limit the constant-character conclusion to the image quotient. [Author landing page](https://eulersolve.org/papers/owr-17294-017/), [Zenodo record](https://zenodo.org/records/23072076), [DOI](https://doi.org/10.5281/zenodo.23072076).

The elementary arguments below do not use finite-dimensional Nichols algebras, Koszulness, the full computational census, or a global-dimension theorem. In particular, they avoid relying on an uncorrected version of Jespers--Kubat--Van Antwerpen. A separate use of that shortcut must retain the hypotheses and corrected statement of [arXiv:1812.02026v2](https://arxiv.org/abs/1812.02026v2) and its [corrigendum](https://doi.org/10.1090/tran/8057). No independent acceptance of that proof or of Ferudun's full census is asserted here.

## 2. Definitions and comparison complex

Let \(k\) be a field, \(V=kX\), and

\[
 R=\operatorname{im}(1-r)\subseteq V^{\otimes2},\qquad
 A=T(V)/(R)=kM(X,r).
\]

The word-length grading is called **weight**. It is distinct from chain degree. The relation space is homogeneous of weight 2, and \(A_0=k\), \(A_1=V\). Write \(\bar A=A_{>0}\).

For a permutation \(w\in S_n\), use any reduced positive braid lift \(T_w^r\). The braid equation ensures independence of the reduced expression. Set

\[
 Q_n=\sum_{w\in S_n}(-1)^{\ell(w)}T_w^r,
 \qquad B_n=\operatorname{im}Q_n\subseteq V^{\otimes n}.
\]

Here \(B_0=k\), \(B_1=V\), and \(B_2=R\). This realizes the degree pieces of the Nichols algebra as quantum-shuffle image spaces; ordinary concatenation is not asserted to be their multiplication.

Define

\[
 K_n=\bigcap_{j=0}^{n-2}V^{\otimes j}\otimes R\otimes V^{\otimes(n-j-2)}.
\]

Every parabolic factorization of \(S_n\) into minimal coset representatives and a subgroup gives a corresponding factorization of \(Q_n\). Factoring with the subgroup generated by a single adjacent transposition shows \(B_n\subseteq K_n\). Factoring with the subgroups on the first or last \(n-1\) positions shows

\[
 B_n\subseteq (B_{n-1}\otimes V)\cap(V\otimes B_{n-1}).
\]

In the normalized two-sided bar complex, set \(C_n=A\otimes B_n\otimes A\). Its differential is

\[
 d(a\otimes v_1\cdots v_n\otimes b)
 =av_1\otimes v_2\cdots v_n\otimes b
 +(-1)^n a\otimes v_1\cdots v_{n-1}\otimes v_nb,
 \tag{2.1}
\]

interpreted linearly. Inner bar terms vanish since adjacent multiplication kills \(R\); the preceding inclusions ensure that the endpoints lie in \(C_{n-1}\). This is precisely the image complex in FGG's Question 44. The augmented comparison is \(C\to A\).

## 3. Four-point solution and Fourier block

The map \(r(x,y)=(y,x+1)\) has inverse \((x,y)\mapsto(y-1,x)\). Its two nondegeneracy maps are permutations. Both sides of the braid equation send \((x,y,z)\) to \((z,y+1,x+2)\). Moreover \(r^2(x,y)=(x+1,y+1)\), so it is neither involutive nor idempotent.

Assume now \(\operatorname{char}k\ne2\), and extend scalars, if necessary, to a field \(L\) containing \(i\) with \(i^2=-1\). Such an \(i\) has order 4. Put

\[
 u_j=\sum_{a=0}^3 i^{-ja}x_a\quad(j\in\mathbb Z/4),\qquad t=u_0.
\]

The Fourier transform is invertible because 4 is invertible. With \(F(x_a)=x_{a+1}\), one has \(Fu_j=i^ju_j\), hence

\[
 r(u_a\otimes u_b)=i^a u_b\otimes u_a. \tag{3.1}
\]

All relations and symmetrizers preserve the multiplicity of each Fourier letter. In particular their spaces split by these multidegrees.

The relations \(u_0u_1=u_1u_0\) and \(u_1u_0=i u_0u_1\) imply \(u_0u_1=u_1u_0=0\) in \(A_L\). Similarly \((1-i)u_1^2=0\), so \(u_1^2=0\). The scalar \(1-i\) is invertible. Consequently all three words

\[
 w_1=u_1u_1u_0,\quad w_2=u_1u_0u_1,\quad w_3=u_0u_1u_1
\]

belong to \(K_{3,L}\). Here and below these words denote tensors when considered in \(V^{\otimes3}\), rather than their zero products in \(A\).

Let \(W=\langle w_1,w_2,w_3\rangle\). Summing the six signed braid lifts, equivalently using

\[
 Q_3=1-r_1-r_2+r_1r_2+r_2r_1-r_1r_2r_1,
\]

gives, with images as columns,

\[
 Q_3|_W=
 \begin{pmatrix}
 1-i&-1+i&1-i\\
 -1-i&2&-1+i\\
 -1+i&-1-i&1-i
 \end{pmatrix}. \tag{3.2}
\]

The row vector \(\ell=(i,1+i,1)\) annihilates this matrix, while \(\ell(w_3)=1\). Multidegree preservation implies \(B_{3,L}\cap W=Q_3(W)\). Therefore

\[
 w_3\in K_{3,L}\setminus B_{3,L}. \tag{3.3}
\]

This short calculation is the essential obstruction from Ferudun's proof. It is valid over every field of characteristic different from 2, not just over the complex numbers. All matrix identities are polynomial identities in \(i\) modulo \(i^2+1\).

## 4. The bimodule-resolution obstruction

For \(v=v_1v_2v_3\in V_L^{\otimes3}\), define

\[
 \theta(v)=v_1\otimes v_2v_3\otimes1,
 \qquad \rho(v)=1\otimes v_1v_2\otimes v_3.
\]

For \(v\in K_{3,L}\), these belong to the two direct weight-3 summands of \(C_{2,L}\). For \(w_3\) in (3.3), put

\[
 z=\theta(w_3)-\rho(w_3)
 =u_0\otimes u_1u_1\otimes1-1\otimes u_0u_1\otimes u_1.
\]

The adjacent pairs are elements of \(R_L=B_{2,L}\), so \(z\in C_{2,L}\). Formula (2.1) gives cancellation of the middle terms; the other two terms vanish because \(u_0u_1=u_1^2=0\) in \(A_L\). Thus \(dz=0\).

Any degree-3 chain of weight 3 is \(1\otimes b\otimes1\), with \(b\in B_{3,L}\), and its boundary is \(\theta(b)-\rho(b)\). The two terms live in distinct outer-weight summands. Since \(A_1=V\), \(\theta\) is injective. Hence an equality \(z=d(1\otimes b\otimes1)\) would force \(b=w_3\), contrary to (3.3). A boundary of other weight cannot help because the differential preserves weight. Thus \([z]\ne0\in H_2(C_L)\).

Replacing \(i\) by \(-i\) gives a second class \(\bar z\), with \(u_3\) instead of \(u_1\). They have distinct Fourier multidegrees and are linearly independent. Let

\[
 a=x_0-x_2,\qquad b=x_1-x_3,\qquad t=x_0+x_1+x_2+x_3.
\]

The following tensors are defined over \(k\), without adjoining \(i\):

\[
 v_{\rm re}=t\otimes(a\otimes a-b\otimes b),\qquad
 v_{\rm im}=-t\otimes(a\otimes b+b\otimes a).
\]

Set \(z_{\rm re}=\theta(v_{\rm re})-\rho(v_{\rm re})\) and
\(z_{\rm im}=\theta(v_{\rm im})-\rho(v_{\rm im})\). Extension of scalars gives

\[
 z=z_{\rm re}+i z_{\rm im},\qquad
 \bar z=z_{\rm re}-i z_{\rm im}.
\]

Field extension commutes with homology and is faithful. Since \(2i\ne0\), the two classes \([z_{\rm re}],[z_{\rm im}]\) are independent already over \(k\). This proves Statement 1 without any global-dimension or Koszul argument.

## 5. Zero-character obstruction for every factoring chain quotient

Let \(\epsilon_0:A\to k\) kill every positive-weight element, and let \(k_0\) have left and right action through \(\epsilon_0\). This is a unital bimodule: the algebra unit acts as 1, although each generator acts as 0.

The normalized Hochschild chain complex with these coefficients has spaces \(\bar A^{\otimes n}\). The endpoint terms vanish, leaving the internal multiplication terms. In degree and weight 3 the chain space is \(V^{\otimes3}\). Its outgoing differential has components in the distinct summands \(A_2\otimes V\) and \(V\otimes A_2\). Its kernel is therefore

\[
 (R\otimes V)\cap(V\otimes R)=K_3.
\]

There is no degree-4 chain of weight 3. Consequently

\[
 HH_3(A;k_0)_{\text{weight }3}=K_3. \tag{5.1}
\]

Every braided face contains one generator action, so the braided differential with coefficients \(k_0\) is zero. Its degree-3 comparison map has image \(B_3\). Scalar extension and (3.3) show that \(B_3\ne K_3\) over \(k\).

Let \(Y\to C_*(A;k_0)\) be any chain map whose degree-3 image lies in \(B_3\subseteq V^{\otimes3}\). Its image on homology cannot contain the missing class of (5.1). This applies in particular to every quotient of the braided chain complex through which the original quantum symmetrizer factors, and to every subcomplex with its restricted comparison. Thus no such quotient yields a quasi-isomorphism.

For the cohomological statement, choose a linear functional \(g\) on \(V^{\otimes3}\) that vanishes on \(B_3\) but not on \(K_3\), and extend it by zero on all other weights in \(\bar A^{\otimes3}\). It is a Hochschild cocycle: the degree-4 domain has no weight-3 summand. It is not a coboundary, because every coboundary vanishes on cycles in \(K_3\). But \(gQ_3=0\). The induced comparison from Hochschild cohomology to braided cohomology, or to any subcomplex containing its image, is therefore noninjective. This proves Statement 2 with the correct cochain direction.

## 6. Constant-character quotient that does work

Keep the same four-point solution and \(\operatorname{char}k\ne2\). Let \(\epsilon_1(x_a)=1\) and let \(k_1\) have this character on both sides. Let \(D_n=V^{\otimes n}\) be the braided chain complex with these coefficients and the left-minus-right convention of Lebed's Theorem 2.

### 6.1 All-degree contraction of the other Fourier blocks

Work first over \(L\) as in §3. Write \(\lambda_j=i^j\). Then
\(\epsilon_1(u_j)=4\) for \(j=0\) and zero otherwise. Moving a letter to the left endpoint by the braiding contributes the product of the eigenvalues of the preceding letters; moving a zero-index Fourier letter to the right contributes 1. Thus

\[
 d(u_{j_1}\cdots u_{j_n})
 =4\sum_{s:j_s=0}(-1)^{s-1}
 \left(\prod_{h<s}\lambda_{j_h}-1\right)
 u_{j_1}\cdots\widehat{u_{j_s}}\cdots u_{j_n}.
 \tag{6.1}
\]

In particular, the differential removes only \(u_0\) letters. It preserves the ordered list of nonzero-index letters. Fix a nonempty such list \(b_1,\ldots,b_m\in\{1,2,3\}\). A word in its block is uniquely described by

\[
 u_0^{a_0}u_{b_1}u_0^{a_1}u_{b_2}\cdots u_{b_m}u_0^{a_m}.
\]

These powers mean tensor runs. Put \(\Lambda_j=\lambda_{b_1}\cdots\lambda_{b_j}\) and \(c_j=4(\Lambda_j-1)\). The contribution deleting from gap \(j\) is zero when \(a_j\) is even, and when it is odd is

\[
 (-1)^{a_0+\cdots+a_{j-1}+j}c_j
 \times\text{the word with }a_j\text{ reduced by 1}.
\]

The initial gap has \(c_0=0\), while \(c_1=4(\lambda_{b_1}-1)\ne0\). Define a degree-raising map \(h\) by

\[
 h(w)=
 \begin{cases}
 \displaystyle\frac{(-1)^{a_0+1}}{c_1}
 \times\text{the word with }a_1\text{ increased by 1},&a_1\text{ even},\\
 0,&a_1\text{ odd}.
 \end{cases}\tag{6.2}
\]

Deleting in gap 1 gives \(d_1h+hd_1=1\): for even \(a_1\), the first composite is the identity, and for odd \(a_1\), the second is the identity. For each later gap, insertion in gap 1 reverses the deletion sign, so \(d_jh+hd_j=0\). The initial-gap contribution is zero. Hence \(dh+hd=1\) on every nonempty-skeleton block.

The remaining block consists of the tensors \(t^{\otimes n}=u_0^{\otimes n}\); its differential is zero. We have proved, in all degrees,

\[
 H_n(D_L)=L\,[t^{\otimes n}].
\]

The tensors are defined over \(k\), and faithful scalar extension shows that already
\(H_n(D)=k\,[t^{\otimes n}]\). No rational-only rack-homology theorem is needed for this step.

### 6.2 The quotient and the factoring map

Let \(S\subset D\) be the subcomplex

\[
 S_0=S_1=0,\qquad S_n=k\,t^{\otimes n}\quad(n\ge2).
\]

Its differential is zero. Since \(r(t\otimes t)=t\otimes t\), every signed braid lift acts on \(t^{\otimes n}\) by its permutation sign. For \(n\ge2\) the sum of these signs is zero. Thus \(Q_n(S_n)=0\), and QS factors through the chain quotient

\[
 Y=D/S.
\]

The inclusion \(S\to D\) induces an isomorphism on homology in every degree at least 2 and is zero in degrees 0 and 1. The long exact sequence, or the contraction above, gives

\[
 H_n(Y)=\begin{cases}k,&n=0,1,\\0,&n\ge2.\end{cases}\tag{6.3}
\]

### 6.3 Hochschild homology for this character

Over \(L\), the relations \(t u_j=u_jt\) and \(u_jt=\lambda_j t u_j\), with \(j\ne0\), imply \(tu_j=u_jt=0\). Let \(J\) be the ideal generated by \(u_1,u_2,u_3\). Then \(tJ=Jt=0\), and

\[
 A_L=L[t]\oplus J
\]

as vector spaces. Indeed mixed words vanish, and the map sending \(t\) to a polynomial indeterminate and all other \(u_j\) to zero proves the polynomial summand has no additional relations and intersects \(J\) trivially.

The central element \(t-4\) acts injectively: on \(L[t]\) it is ordinary multiplication by the nonzero polynomial \(t-4\), and on \(J\) it is multiplication by the nonzero scalar \(-4\). Its cokernel is \(L_1\), since setting \(t=4\) forces every \(u_j\), \(j\ne0\), to vanish. All maps are defined over \(k\), so exactness descends and gives a free resolution

\[
 0\longrightarrow A\xrightarrow{\;t-4\;}A
 \xrightarrow{\epsilon_1}k_1\longrightarrow0.\tag{6.4}
\]

For a character bimodule with the same character on both sides, the Hochschild chain complex is the two-sided bar complex computing \(\operatorname{Tor}^A_*(k_1,k_1)\): their formulas agree term by term. Tensoring (6.4) with \(k_1\) gives zero differential. Therefore

\[
 HH_n(A;k_1)=\begin{cases}k,&n=0,1,\\0,&n\ge2.\end{cases}\tag{6.5}
\]

Finally, QS is the identity in degrees 0 and 1. Its degree-1 image of \([t]\) is nonzero: the \(\epsilon_1\)-derivation sending every generator \(x_a\) to 1 respects the homogeneous quadratic relations and evaluates to 4 on \(t\). As 4 is nonzero, this is a Hochschild 1-cocycle detecting \([t]\). Equations (6.3)--(6.5) prove that

\[
 Y\xrightarrow{QS}C_*(A;k_1)
\]

is a quasi-isomorphism in all degrees. Taking vector-space duals also gives the corresponding cohomological quasi-isomorphism in the reversed direction.

This is an ordinary chain-complex quotient after choosing \(k_1\). No claim is made that \(S\) is an algebra ideal, a Hopf ideal, a coefficient-independent sub-bimodule, or the Nichols kernel. Such additional requirements would be different targets.

## 7. Reproducible finite checks and their limits

The accompanying authored `check_claim.py` was written independently from the definitions above. No program from Ferudun's source archive was executed or imported. It uses exact integer/rational matrices through preinstalled SymPy and a separately implemented exact \(\mathbb Q(i)\) arithmetic class; there is no floating-point rank calculation.

The recorded run in `check_results.json` verifies:

- all 64 Yang--Baxter triples, bijectivity and both nondegeneracy conditions;
- monoid dimensions \(\dim A_2=2\), \(\dim A_3=1\), by union-find on the defining relations;
- \(\operatorname{rank}_{\mathbb Q}Q_2=14\), \(\operatorname{rank}_{\mathbb Q}Q_3=47\), and \(\dim_{\mathbb Q}K_3=49\);
- adjoining \(v_{\rm re},v_{\rm im}\) to the image columns of \(Q_3\) raises their rank from 47 to 49;
- \(\dim C_{2,\text{weight }3}=112\), \(\operatorname{rank}d_2=63\), \(\operatorname{rank}d_3=47\), hence exactly two weight-3 classes in \(H_2(C)\) over \(\mathbb Q\);
- the independently generated Fourier matrix (3.2) and its left annihilator;
- \(d^2=0\) and the contraction identity on all 5,461 Fourier words in degrees 0 through 6;
- QS chain-map compatibility for all 340 Fourier words in degrees 1 through 4, and annihilation of the all-sum tensor in degrees 2 through 6.

The finite checks corroborate the proofs but do not establish their all-degree or all-characteristic quantifiers. Those are supplied by the symbolic arguments in §§3--6. The exact dimensions 47, 49 and 2 above are asserted over \(\mathbb Q\); no extrapolation of all those dimensions to every odd characteristic is made.

## 8. Acceptance boundary

**Proposed for independent mathematical acceptance:** Statements 1--3 with exactly the field, character, quotient and map conventions stated here.

**Not established:** a universal solution to the constant-character suitable-quotient question; the intended omitted conventions of the original OWR question; a new proof of every theorem in Ferudun's manuscript; a complete literature or priority result; a classification of all solutions; or any theorem in characteristic 2.

The logical distinction is substantive: failure of a particular image complex does not rule out larger factoring chain quotients for a fixed coefficient module, and a zero-character obstruction cannot be silently transferred to the constant character. The explicit positive construction in §6 demonstrates that distinction within the very same example.
