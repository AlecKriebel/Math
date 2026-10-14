# Separating meridian twists do not generate the full handlebody Johnson kernel in genus at least three

Inspection and proof date: 14 October 2026.

## Result and scope

Let (V_g) be a fixed oriented handlebody with closed boundary (S_g). Write (H_g\leq\operatorname{Mod}(S_g)), (I_g=\ker(\operatorname{Mod}(S_g)\to\operatorname{Sp}(H_1(S_g;\mathbb Z)))), (K_g=\langle T_c:c\text{ separates }S_g\rangle), and
\[
HI_g=H_g\cap I_g,\qquad HK_g=H_g\cap K_g.
\]
Let (\rho:H_g\to\operatorname{Out}(F_g)) be the handlebody fundamental-group action, and let
\[
M_g^{\rm sep}=\langle T_d:d\text{ bounds a disk in }V_g\text{ and separates }S_g\rangle.
\]

**Proposition.** For every (g\geq3), there is an explicitly specified commutator (f\in[HI_g,HI_g]\leq HK_g) such that (\rho(f)) has infinite order. Consequently
\[
M_g^{\rm sep}\ \leq\ HK_g\cap\ker\rho\ <\ HK_g,
\qquad [HK_g:M_g^{\rm sep}]=\infty.
\]
Indeed, even (HK_g\cap\ker\rho) has infinite index in (HK_g).

This disproves the separating-meridian generator proposal for the **full** (HK_g), in every genus (g\geq3). The target cannot be replaced by the smaller intersection with the Luft/twist kernel. This argument makes no genus-two generator claim and does not answer Birman's open-ended request for some useful generators of (HK_g). No novelty claim is made.

## 1. The precise map and the required lifting statement

Put
\[
IA_g=\ker(\operatorname{Aut}(F_g)\to\operatorname{GL}_g(\mathbb Z)),\qquad
OA_g=\ker(\operatorname{Out}(F_g)\to\operatorname{GL}_g(\mathbb Z)).
\]
Inner automorphisms act trivially on abelianization. Thus the quotient map (\pi:\operatorname{Aut}(F_g)\to\operatorname{Out}(F_g)) restricts to a surjection (IA_g\to OA_g).

Choose a disk (D\subset S_g) and a basepoint (p\in\partial D). Use (H_g^D,I_g^D,HI_g^D) for disk-fixed groups. These are Omori's (H_{g,1},I_{g,1},IH_{g,1}); his subscript does **not** mean merely point-fixed. Omori's §2.1, p.4, equation (2.1), explicitly gives
\[
\eta:HI_g^D\twoheadrightarrow IA_g.
\]
The preceding calculation identifies a genus-one homotopical bounding-pair map (u=T_{C_1}T_{C_2}^{-1}\in HI_g^D), with curves and free basis shown in Figures 1 and 3, whose image is
\[
\eta(u)(x_1)=x_2x_1x_2^{-1},\qquad\eta(u)(x_k)=x_k\quad(k\ne1).
\]
The proof of surjectivity uses the normality of (HI_g^D\) in (H_g^D\), the surjectivity (H_g^D\to\operatorname{Aut}(F_g)), and normal generation of (IA_g) by this partial conjugation. We use this primary statement, not an inference from generation of the larger handlebody group. [Omori, §§1 and 2.1, pp.1–4](https://arxiv.org/pdf/1607.06553v1).

Let (q:H_g^D\to H_g) forget the disk. The inclusion (S_g\setminus\operatorname{int}D\to S_g) induces an isomorphism on integral first homology, so (q(HI_g^D)\subseteq HI_g). By their definitions the actions satisfy
\[
\rho\circ q=\pi\circ\eta.
\]
For any (a\in OA_g), choose (A\in IA_g) with (\pi(A)=a), then choose (\widetilde a\in HI_g^D) with (\eta(\widetilde a)=A). Its closed image belongs to (HI_g) and maps to (a). Therefore
\[
\rho(HI_g)=OA_g.
\]
The opposite inclusion follows because trivial action on (H_1(S_g;\mathbb Z)) implies trivial action on its quotient (H_1(V_g;\mathbb Z)).

Notice what was **not** assumed: injectivity of the forgetful map, an identification of Aut and Out kernels, or surjectivity of the restriction (q:HI_g^D\to HI_g). The displayed commutative relation and homology isomorphism already prove the needed assertion.

### Independent constructive verification by meridian correction

There is also an integral symplectic proof of the lifting statement. The standard surjection (H_g\twoheadrightarrow\operatorname{Out}(F_g)) is recorded with geometric Nielsen-generator lifts in [Hensel, Theorem 6.3, p.21](https://www.math.lmu.de/~hensel/papers/hno4.pdf). Choose any lift (h\in H_g) of (a\in OA_g).

Take a meridian disk system with boundary classes (a_1,\ldots,a_g), and complete it to a symplectic basis (a_1,\ldots,a_g,b_1,\ldots,b_g) of surface homology. The kernel (L) of (H_1(S_g;\mathbb Z)\to H_1(V_g;\mathbb Z)) is the span of the (a_i). Since (h) preserves (L) and is the identity on the quotient, its matrix has block form
\[
h_* = \begin{pmatrix}P&Q\\0&I\end{pmatrix}.
\]
The equation (h_*^{\mathsf T}Jh_*=J), with (J=\left(\begin{smallmatrix}0&I\\-I&0\end{smallmatrix}\right)), gives (P=I) and (Q^{\mathsf T}=Q).

For each primitive meridian class (v\in L) used below, choose the direction of the disk twist (D(v)) so that its homology matrix is
\[
D(v)_*=U(vv^{\mathsf T}),\qquad U(R)=\begin{pmatrix}I&R\\0&I\end{pmatrix}.
\]
The standard Dehn-twist transvection formula gives this matrix; if right twists give the opposite sign under one's convention, use their inverses. Required curves exist: (v=e_i) is a standard disk boundary, and (v=e_i+e_j) is the oriented boundary of a band sum of the (i\)-th and (j\)-th meridian disks along a boundary arc. The band sum is an embedded disk and its boundary has the stated homology class.

The matrices (U(R)) add their (R)-blocks under multiplication. Moreover,
\[
(e_i+e_j)(e_i+e_j)^{\mathsf T}-e_ie_i^{\mathsf T}-e_je_j^{\mathsf T}
=E_{ij}+E_{ji}.
\]
Thus all integral symmetric matrices are realized by products of these disk twists. More explicitly, for (Q=(q_{ij})\), a correction is
\[
\delta=
\prod_i D(e_i)^{-q_{ii}}
\prod_{i<j}\bigl(D(e_i+e_j)D(e_i)^{-1}D(e_j)^{-1}\bigr)^{-q_{ij}},
\]
where any fixed order is used. Its homology matrix is (U(-Q)), even though the actual disk twists need not commute. Every factor has trivial outer action: a disk twist inserts disk-boundary loops into transverse loops, and these inserted loops are nullhomotopic in (V_g). Hence (\rho(\delta)=1), (\rho(\delta h)=a), and ((\delta h)_*=I). This proves the lift is in (HI_g) without using Omori's stronger generator theorem.

## 2. Explicit partial conjugations and handlebody lifts

Fix (g\geq3), with free basis (x_1,\ldots,x_g). Define
\[
A(x_1)=x_2x_1x_2^{-1},\quad A(x_i)=x_i\ (i\ne1),
\]
\[
B(x_2)=x_3x_2x_3^{-1},\quad B(x_i)=x_i\ (i\ne2).
\]
These are automorphisms: their inverses replace the indicated conjugator by its inverse. Both act trivially on abelianization, so (A,B\in IA_g).

For a concrete disk-fixed lift take (u=T_{C_1}T_{C_2}^{-1}) from Omori's figures. Let (P\in\operatorname{Aut}(F_g)) be the basis cycle (x_1\mapsto x_2\mapsto x_3\mapsto x_1), fixing the other basis elements. Choose a disk-fixed handlebody lift (r) of (P). Such a lift exists by the verified surjection (H_g^D\to\operatorname{Aut}(F_g)); geometrically this is a permutation of the three marked handles, with based paths chosen as in Figure 3. Then set
\[
v=rur^{-1}.
\]
Normality of the surface Torelli kernel gives (v\in HI_g^D), and (\eta(v)=PAP^{-1}=B). If a geometric handle permutation is initially chosen with different based paths, choose a lift of the exact (P) through the same verified Aut surjection; no equality of merely outer representatives is being assumed.

The closed lifts are (a=q(u),b=q(v)\in HI_g). We define
\[
f=[a,b]=aba^{-1}b^{-1}.
\]
Any other exact lifts of (A,B) yield the same outer image for their commutator, so the subsequent obstruction is independent of the permissible lift choices.

## 3. Why this commutator lies in the surface Johnson kernel

For a closed surface of genus (g\geq3), let (H=H_1(S_g;\mathbb Z)), and use the integral Johnson homomorphism
\[
\tau_g:I_g\longrightarrow\Lambda^3 H/\kappa(H),\qquad \kappa(x)=x\wedge\omega,
\]
where \(\omega\) is the symplectic class. Johnson's kernel theorem identifies \(\ker\tau_g\) with the subgroup generated by separating twists. An independent proof in the exact closed model is [Putman, *The Johnson homomorphism and its kernel*, arXiv:0904.0467v4, §1 pp.2–3, Theorem A with the subsurface equal to the whole surface; §2.4 p.12](https://arxiv.org/pdf/0904.0467v4).

The codomain is abelian. Consequently \([I_g,I_g]\subseteq K_g\). Since \(a,b\in HI_g\), their commutator is in \(H_g\) and in \([I_g,I_g]\), proving
\[
f\in [HI_g,HI_g]\subseteq H_g\cap K_g=HK_g.
\]
This is an integral kernel statement, not a rational-homology or finite-index substitute.

## 4. Exact free-group calculation and non-innerness

Composition is right-to-left: \(AB\) applies \(B\) first. Put
\[
\Phi=[A,B]=ABA^{-1}B^{-1},\qquad w=x_3x_2^{-1}x_3^{-1}x_2.
\]
Applying the four maps gives
\[
\Phi(x_1)=x_3x_2^{-1}x_3^{-1}x_2x_1x_2^{-1}x_3x_2x_3^{-1}=wx_1w^{-1},
\]
\[
\Phi(x_i)=x_i\qquad(2\leq i\leq g).
\]
For example, \(B^{-1}(x_1)=x_1\), then \(A^{-1}(x_1)=x_2^{-1}x_1x_2\); applying \(B\) and then \(A\) yields precisely the displayed word. For \(x_2\), the four stages are \(x_3^{-1}x_2x_3\), the same word, \(x_2\), and \(x_2\).

The word \(w\) is nonempty and cyclically reduced, contains no \(x_1^{\pm1}\), and is fixed by \(\Phi\). Hence, for every integer \(n\),
\[
\Phi^n(x_1)=w^nx_1w^{-n},\qquad \Phi^n(x_i)=x_i\ (i\geq2).
\]
For \(n\ne0\), the first word is freely reduced of length \(8|n|+1>1\), so \(\Phi^n\ne1\).

Suppose \(\Phi^n\) were conjugation by a word \(z\). As it fixes both \(x_2\) and \(x_3\), the word \(z\) would belong to
\[
C_{F_g}(x_2)\cap C_{F_g}(x_3)=\langle x_2\rangle\cap\langle x_3\rangle=\{1\}.
\]
Here the centralizer of a free basis element is its cyclic subgroup, directly from reduced normal forms in the free product \(\langle x_i\rangle*F(\{x_j:j\ne i\})\). A nonidentity power of \(x_2\) cannot equal a power of \(x_3\) by uniqueness of reduced words. Thus \(z=1\), contradicting \(\Phi^n\ne1\). Every nonzero power of \(\Phi\) is non-inner.

The action diagram now gives \(\rho(f)=[\Phi]\in\operatorname{Out}(F_g)\), an element of infinite order.

## 5. Failure of the candidate family, including the finite-index version

Every meridian twist has trivial \(\rho\)-image. Every separating meridian twist also lies in \(K_g\) by definition. Thus \(M_g^{\rm sep}\subseteq HK_g\cap\ker\rho\). But \(f^n\notin\ker\rho\) for \(n\ne0\). The cosets \(f^n(HK_g\cap\ker\rho)\), and therefore \(f^nM_g^{\rm sep}\), are pairwise distinct. This proves the proposition and its infinite-index strengthening.

For completeness, if \(\Gamma\leq H_g\) has finite index, some positive power \(f^m\) lies in \(\Gamma\). Its outer image still has infinite order. If \(K(\Gamma)\) is generated by the powers of separating meridian twists which belong to \(\Gamma\), then \(K(\Gamma)\subseteq\ker\rho\), and the cosets \(f^{mk}K(\Gamma)\) in \(\Gamma\cap HK_g\) are pairwise distinct. Hence
\[
[\Gamma\cap HK_g:K(\Gamma)]=\infty\qquad(g\geq3).
\]

## 6. Precisely what this says about the dated proposal

Holden's [arXiv:2607.07587v1, §1.4 p.3 and §7 p.12](https://arxiv.org/pdf/2607.07587v1) defines \(HK_g\) as the full \(H_g\cap K_g\) and labels separating-meridian generation as **Conjecture 7.1**. Under those definitions the proposition above is a counterexample for every \(g\geq3\), in particular throughout the surrounding applications' range \(g\geq4\). The paper's §2.3 separately records the meridian-twist kernel of the Out action.

The further finite-index calculation shows that the hypothesis of that version's Theorem D cannot occur in this model and genus range. It does **not** disprove the conditional implication in Theorem D. Likewise, an explicitly conjecture-dependent corollary must not be described as an unconditional theorem refuted here.

No claim is made about revised versions, publication status beyond the cited version, the author's intended alternative formulation, or novelty of the obstruction. The argument rules out one proposed family; it does not provide a replacement generator family for \(HK_g\), and it leaves genus two separately unresolved in this report.

## 7. Verification record

- Disk-fixed notation, HBP curves, free basis, explicit partial-conjugation lift, and equation (2.1): checked in Omori's retained complete PDF and fresh arXiv PDF view; Figures 1 and 3 and p.4 were visually inspected.
- Closed Johnson target and separating-twist kernel: checked in Putman's arXiv v4 PDF, pp.2–3 and §2.4; the author-hosted PDF gives the same relevant statements.
- Closed handlebody action and geometric Nielsen lifts: checked in Hensel's retained PDF, §6, especially Theorems 6.3–6.4.
- Holden's conjectural status and full-intersection definition: checked against the retained source-scope adjudication and current v1 HTML/PDF presentation.
- `verify_free_group.py` checks exact free reduction, inverse automorphisms, the commutator convention, all images, and powers \(-12\) through \(12\), in ranks \(3\) through \(12\). All checks pass. These finite checks are supplementary; Sections 3–5 are the proof for all \(g\geq3\) and all nonzero powers.
- This is a separately audited mathematical obstruction, complementary to the generating families in this reader.
