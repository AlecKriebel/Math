# Hodge integrals for connected covers of a moving elliptic curve

## Result and attribution

This is a source-based resolution of Question 2 in Rahul Pandharipande's 2023 Oberwolfach report, not a claim of a new solution. The necessary higher-degree calculation was proved by Aitor Iribar López, Rahul Pandharipande, and Hsian-Hua Tseng in 2025. Below we extract the connected admissible-cover integral from their theorem, keeping the disconnected-cover correction explicit.

Work over the complex numbers, with rational Chow classes and automorphism-weighted stack integrals. Let H_{d,n} denote the compactified stack of **connected** degree-d admissible covers of a genus-one target with 2n ordered, simple branch points. Equivalently one may use its normalization by twisted stable maps. Its dimension is 2n, the source genus is n+1, and λ_j is the j-th Chern class of the source Hodge bundle. Define

\[
 I_{d,n}=\int_{H_{d,n}}\lambda_{n+1}\lambda_{n-1},\qquad
 F_d(u)=\sum_{n\ge1}I_{d,n}\frac{u^{2n-1}}{(2n-1)!}.
\]

For every d≥1 (with the empty branched degree-one stack understood),

\[
\boxed{I_{d,n}=\frac{|B_{2n}|}{48n}\bigl(\sigma_{2n+1}(d)-\sigma_1(d)\bigr).}\tag{1}
\]

Here B_{2n} are Bernoulli numbers and σ_a(d)=Σ_{k|d}k^a. Equivalently,

\[
\boxed{F_d(u)=\frac1{48}\sum_{k\mid d}
\left(k\cot\frac u2-k^2\cot\frac{ku}2\right).}\tag{2}
\]

The apparent pole at u=0 cancels term by term. With x=−q=e^{iu}, the requested rational function is

\[
\boxed{F_d(u)=-\frac{i}{24}U_d(q),\quad
 U_d(q)=\frac12\sum_{k\mid d}
 \left(k^2\frac{(-q)^k+1}{(-q)^k-1}
       -k\frac{(-q)+1}{(-q)-1}\right).}\tag{3}
\]

In particular F_2(u)=tan(u/2)/24, exactly the normalization printed in the question. Also

\[
 F_3(u)=\frac{i}{8}\frac{1-q^2}{q^2-q+1}.
\]

The word “connected” matters: the orbifold Gromov–Witten invariant on the symmetric product also contains disconnected covers. One cannot identify it with F_d by simply removing its equivariant prefactor.

## 1. Established input

Use the following two established theorems.

* [Iribar López–Pandharipande–Tseng, arXiv:2506.12438v2](https://arxiv.org/abs/2506.12438v2), Theorem 1 and equation (0.5), give
  \[
  \langle D\rangle^{\operatorname{Hilb}^d(\mathbb C^2)}_1
  =-\frac{(t_1+t_2)^2}{24t_1t_2}
  \left(T_d+\sum_{a=1}^{d-1}\sigma_{-1}(a)T_{d-a}\right),\tag{4}
  \]
  where T_0=T_1=0 and
  \[
  T_d=\sum_{\mu\vdash d}\sum_{k\in\mu}
   \left(\frac{k^2}{2}\frac{x^k+1}{x^k-1}
          -\frac{k}{2}\frac{x+1}{x-1}\right),\quad x=-q.\tag{5}
  \]
  The proof of this theorem is in Sections 2 and 3. It is unconditional; the nondegeneracy conjecture discussed later in that paper concerns reconstruction of other insertions, not (4).

* [Pandharipande–Tseng, Higher genus Gromov–Witten theory of Hilb^n(C²) and CohFTs associated to local curves](https://people.math.ethz.ch/~rahul/HilbC2-2025-August.pdf), Theorem 4, identifies the Hilbert-scheme and symmetric-product theories after −q=e^{iu}. For the transposition insertion τ=(2,1^{d−2}), and D=−|τ⟩, its phase is
  \[
  S_d(u):=\langle\tau\rangle^{\operatorname{Sym}^d(\mathbb C^2)}_1
  =i\langle D\rangle^{\operatorname{Hilb}^d(\mathbb C^2)}_1.\tag{6}
  \]
  Section 3.2 defines a term with b free simple branch points by division by b!, so b=2n−1 produces exactly the factorial in F_d. Section 0.6 checks the same convention in degree two. The complete correspondence proof is Section 11.1 of the August 2025 revision.

There is an acknowledged rationality gap in the originally published 2019 version of the second paper, repaired in its August 2025 revision. Equation (4) already gives rationality for the particular invariant used here; the analytic-continuation correspondence is the needed input, not an assumption of the earlier general rationality argument. See also footnote 7 in arXiv:2506.12438v2.

## 2. Hodge identities on the connected-cover stack

Let h be the pullback of λ_1 from the target moduli stack M̄_{1,1}; retain the first branch point when forgetting the others. Then h²=0. On every connected component C of a cover with arithmetic genus g, pullback of differentials gives a subbundle

\[
 0\longrightarrow \mathbb E_{\rm target}\longrightarrow
 \mathbb E_C\longrightarrow\mathbb F\longrightarrow0,
 \qquad\operatorname{rank}\mathbb F=g-1.\tag{7}
\]

This holds over the admissible-cover boundary as well: trace composed with pullback is multiplication by the positive degree, so in characteristic zero the inclusion is split. Hodge bundles are unchanged by stabilization of rational components. Since h²=0, (7) implies

\[
 \lambda_g=h\lambda_{g-1},\qquad h\lambda_g=0.\tag{8}
\]

Mumford's identity c(𝔼_C)c(𝔼_C^∨)=1 gives

\[
 \lambda_g^2=0,\qquad\lambda_{g-1}^2=2\lambda_g\lambda_{g-2}.
\]

Consequently λ_gλ_{g−1}=hλ_{g−1}²=2hλ_gλ_{g−2}=0.

Write s=t_1+t_2 and v=t_1t_2. The localization factor for a connected cover is

\[
 N_g=\frac{\prod_{j=1}^g(t_1-\alpha_j)(t_2-\alpha_j)}{v},\tag{9}
\]

where the α_j are Hodge Chern roots. Brackets below specify Chow codimension, not equivariant degree. For g≥2, put b_g=2g−2. The identities just proved imply

\[
 [N_g]_{>b_g}=0,\qquad
 [N_g]_{b_g}=\frac{s^2}{v}\lambda_g\lambda_{g-2},\qquad
 h[N_g]_{b_g-1}=-s\lambda_g\lambda_{g-2}.\tag{10}
\]

For the last equality, the full degree-b_g−1 term is

\[
 -\frac{t_1^3+t_2^3}{v}\lambda_g\lambda_{g-3}
 -s\lambda_{g-1}\lambda_{g-2}.
\]

Multiplication by h kills its first summand and converts the second using (8). Set λ_j=0 for j<0. This also covers g=2. For an unramified connected genus-one cover, its Hodge line is the target Hodge line and

\[
 N_1=1-\frac{s}{v}h.\tag{11}
\]

## 3. Extracting connected covers

Let Q mark the degree of the cover (Q is different from the quantum variable q). Set

\[
 P(Q)=\prod_{m\ge1}(1-Q^m)^{-1},\quad L(Q)=\log P(Q)
       =\sum_{m\ge1}\sigma_{-1}(m)Q^m.
\]

A connected unramified degree-m cover of a fixed elliptic curve has weighted count σ_1(m)/m=σ_{−1}(m). This follows by classifying index-m sublattices of Z²: there are σ_1(m), each with m deck transformations. Thus the generating series for arbitrary unramified covers is exp L=P. Weighting an arbitrary such cover also by its number of connected components gives P·L (differentiate exp(zL) at z=1).

We now compute the full localization integral S_d using (9). Each simple branch point belongs to exactly one connected component of the cover. If a connected component has b_j>0 simple branch points then b_j is even and its genus is 1+b_j/2. For a cover with B branch points in total, the base cover stack has dimension B. Thus only the total codimension-B part of the product of factors N_g contributes.

Suppose there are r≥2 branched components. By (10), their respective maximum codimensions are b_1,…,b_r, with sum B. Every maximum-degree term contains h. At most one unramified component can contribute positive codimension, since h²=0.

* If all unramified factors contribute codimension zero, all r branched factors must be at their maximum; their product contains h^r=0.
* If one unramified factor contributes codimension one, exactly one branched factor must drop by one; the remaining r−1 maximum terms, together with the unramified factor, again contain h^r=0.

All other distributions either have insufficient total codimension or contain h². Therefore only covers with exactly one branched component contribute. This argument applies on the compactified stack: component decompositions are locally constant for finite étale covers of the twisted target, and all the Hodge identities hold on the boundary.

Fix a branched component of degree m and genus n+1, together with an unramified cover of degree d−m with ℓ connected components. Formula (11) gives the combined unramified factor 1−ℓ(s/v)h. Using (10), the required codimension-2n term of the whole product is

\[
 \frac{s^2}{v}\lambda_{n+1}\lambda_{n-1}
 -\ell\frac{s}{v}h[N_{n+1}]_{2n-1}
 =\frac{s^2}{v}(1+\ell)\lambda_{n+1}\lambda_{n-1}.\tag{12}
\]

The unramified covers form a proper finite cover of the target moduli; its generic weighted degree is the fixed-target count above. Projection formula therefore supplies exactly those weights in (12), including boundary contributions. Quotienting permutations of equal unramified components gives the exponential-series automorphism factors already built into P and PL. All branch points belong to the unique branched component, so no additional binomial coefficient occurs.

After division by (2n−1)! and summation, we have proved

\[
 \sum_{d\ge1}S_d(u)Q^d
 =\frac{s^2}{v}P(Q)(1+L(Q))\sum_{d\ge1}F_d(u)Q^d.\tag{13}
\]

Inserting (4) and (6) into (13) and cancelling the invertible power series 1+L yields

\[
 \sum_{d\ge1}F_d(u)Q^d
 =-\frac{i}{24}\frac{\sum_{d\ge1}T_d(q)Q^d}{P(Q)}.\tag{14}
\]

## 4. Evaluating the trace and finishing the proof

For a partition μ, let m_k(μ) be the number of parts equal to k. Elementary partition enumeration gives

\[
 \sum_{d\ge0}Q^d\sum_{\mu\vdash d}m_k(\mu)
 =P(Q)\frac{Q^k}{1-Q^k}.
\]

Apply this identity to (5). With

\[
 a_k(q)=\frac{k^2}{2}\frac{x^k+1}{x^k-1}
       -\frac{k}{2}\frac{x+1}{x-1},\quad x=-q,
\]

we obtain

\[
 \frac{\sum_dT_dQ^d}{P(Q)}
 =\sum_{k\ge1}a_k\frac{Q^k}{1-Q^k}.
\]

Its coefficient of Q^d is Σ_{k|d}a_k, which proves (3) from (14). The identity cot(z/2)=i(e^{iz}+1)/(e^{iz}−1) proves (2).

Finally the convergent Laurent expansion near u=0, or its formal counterpart, is

\[
 \cot\frac u2=\frac2u-2\sum_{n\ge1}\frac{|B_{2n}|}{(2n)!}u^{2n-1}.
\]

The 2/u terms in k cot(u/2)−k²cot(ku/2) cancel. Comparing coefficients in (2) gives

\[
 [u^{2n-1}]F_d
 =\frac{|B_{2n}|}{24(2n)!}
   \bigl(\sigma_{2n+1}(d)-\sigma_1(d)\bigr).
\]

Multiplication by (2n−1)! proves (1). This completes the connected admissible-cover extraction, conditional only on the two established theorems explicitly stated in Section 1. No unproved reconstruction conjecture is used.

## Verification limits

`verify.py` checks exact rational identities, factorials, low-degree examples, the partition correction, and the Bernoulli expansion. It is not a formal proof of the geometric correspondence, trace theorem, or boundary-stack facts. Those are addressed by the argument and stated references above. This note is AI-assisted and unrefereed; no mathematical priority is claimed.
