# Property-(s) elements need not form an additive subgroup

**Status:** complete counterexample candidate; separate adversarial review pending. Two substantive approach families recorded. AI-assisted research draft, not human peer reviewed. Historical priority is unestablished.

## 1. Answer to the exact question

The answer is **no**, even for a left brace with abelian additive group. On

\[
B=\mathbb Z\times\mathbb Z/4\mathbb Z
\]

use coordinatewise addition and define

\[
(n,c)\circ(m,d)=
\bigl(n+\varepsilon(c)m,\ c+d+2cd\pmod4\bigr),
\tag{1}
\]

where

\[
\varepsilon(0)=\varepsilon(1)=1,\qquad
\varepsilon(2)=\varepsilon(3)=-1.
\tag{2}
\]

This is a skew left brace. The element x=(0,1) has property (s), with both indices in the definition equal to two. Its additive double x+x=(0,2) does not have property (s): its right fixed subgroup has infinite additive index. Consequently the set of property-(s) elements is not even an additive subgroup and cannot be an ideal.

In fact the property-(s) set in this example is exactly

\[
\mathcal S=\mathbb Z\times\{0,1\}.
\tag{3}
\]

Here {0,1} is a subgroup for the second coordinate's multiplicative operation, but not for addition modulo four. The brace is not two-sided, so the example does not contradict the known positive two-sided abelian-type result.

## 2. Source scope and conventions

The original is Question 1 in Ilaria Colazzo's contribution, *Derived-indecomposable solutions and skew braces whose elements have a finite number of conjugates*, Oberwolfach Report 9/2023, printed p.543. It asks about an arbitrary skew brace B. Although the surrounding contribution begins with finite Yang--Baxter solutions, the question itself does **not** restrict B to be finite or two-sided. Restricting B to be finite would make the property automatic and the question trivial.

We use precisely its definitions:

\[
a*b=-a+a\circ b-b,\quad
\operatorname{Fix}^{r}(x)=\{b:x*b=0\},\quad
\operatorname{Fix}^{l}(x)=\{b:b*x=0\}.
\]

Property (s) means finiteness of

\[
[(B,+):\operatorname{Fix}^{r}(x)\cap C_x^+],\qquad
[(B,\circ):\operatorname{Fix}^{l}(x)\cap C_x^\circ].
\tag{4}
\]

The published primary treatment, Colazzo--Ferrara--Trombetti, *On derived-indecomposable solutions of the Yang--Baxter equation*, Publ. Mat. 69 (2025), 171--193, Definition 3.7, uses exactly (4). Its Proposition 3.10 proves the ideal assertion for two-sided braces and explicitly leaves the general question unresolved there. Our example has an abelian additive group, but fails the right distributive law.

## 3. Verification of the infinite brace

### 3.1. The four-element multiplicative group

On C=Z/4Z put

\[
c\diamond d=c+d+2cd\pmod4.
\]

Its complete table is

| diamond | 0 | 1 | 2 | 3 |
|---|---:|---:|---:|---:|
| 0 | 0 | 1 | 2 | 3 |
| 1 | 1 | 0 | 3 | 2 |
| 2 | 2 | 3 | 0 | 1 |
| 3 | 3 | 2 | 1 | 0 |

It is the Klein four group, with identity zero and c diamond c=0. Equivalently, writing c=u+2v with u,v in {0,1}, the operation is coordinatewise addition of these two bits modulo two. In particular epsilon(c)=(-1)^v is a group homomorphism from (C,diamond) to {1,-1}.

Thus (1) is the group law of the semidirect product Z semidirect_epsilon (C,diamond). It is associative, with identity (0,0) and inverse

\[
(n,c)^{-1}_{\circ}=(-\varepsilon(c)n,c).
\tag{5}
\]

These formulas hold for every integer n, not merely in finite quotients or a bounded range. The additive law is the abelian group law on Z times C.

### 3.2. The lambda maps and left distributivity

For a=(n,c), b=(m,d), direct substitution gives

\[
\lambda_{(n,c)}(m,d)=-a+a\circ b
 =\bigl(\varepsilon(c)m,(1+2c)d\pmod4\bigr)
 =\bigl(\varepsilon(c)m,(-1)^c d\pmod4\bigr).
\tag{6}
\]

Each map in (6) is an automorphism of the additive group: both factors are multiplication by a sign. Therefore

\[
a\circ(b+e)=a+\lambda_a(b+e)
 =(a\circ b)-a+(a\circ e)
\]

for all a,b,e. Together with the two verified group structures this is exactly the skew left brace axiom. One can also directly check lambda_(a circle b)=lambda_a lambda_b: both epsilon(c) and (-1)^c are characters of (C,diamond).

The general semidirect-product construction is standard; for example Cascella--Properzi--Van Antwerpen state it in Definition 2.11 of their 2026 postprint. The four-element brace c circle d=c+d+2cd is already Colazzo--Ferrara--Trombetti's Example 3.8. The present proof verifies the operations directly, so neither the semidirect-product theorem nor any recent preprint theorem is an unproved dependency.

## 4. The two exact property-(s) calculations

The star product obtained from (6) is

\[
(n,c)*(m,d)
 =\bigl((\varepsilon(c)-1)m,2cd\pmod4\bigr).
\tag{7}
\]

### The element x=(0,1)

By (7), for every (m,d),

\[
x*(m,d)=(0,2d),\qquad (m,d)*x=(0,2d).
\]

Hence both fixed sets, as subsets of B, are

\[
H=\mathbb Z\times\{0,2\}.
\]

All additive centralizers are B because addition is abelian. The element x is also central in the multiplicative group: epsilon(1)=1 and diamond is commutative, so

\[
x\circ(m,d)=(m,1\diamond d)=(m,d)\circ x.
\]

The additive index of H is two. Its multiplicative index is also two: the map (m,d) -> d modulo two is a surjective homomorphism from (B,circle) to Z/2Z with kernel H, since c diamond d has the same parity as c+d. Therefore both indices in (4) are exactly two, and x has property (s).

### Its additive double y=(0,2)

By (7),

\[
y*(m,d)=(-2m,0).
\]

Since m is an integer, this vanishes precisely when m=0. Thus

\[
\operatorname{Fix}^{r}(y)=\{0\}\times C.
\]

The additive centralizer is still all of B. The quotient of the additive group by this subgroup is Z, so its index is infinite. In particular y fails the first finiteness condition in (4).

This is a proof of infinite index, not a numerical extrapolation: the additive cosets represented by (m,0), m in Z, are pairwise distinct. Since x has property (s) but x+x does not, the original ideal assertion is false. ∎

## 5. The full set and the excluded two-sided hypothesis

For completeness, equation (7) shows that no element with c=2 or c=3 has property (s), because its right fixed subgroup forces m=0 and therefore has infinite additive index.

For c=0 or c=1, the first index is one or two, respectively. Let z=(n,c) with c in {0,1}. Comparing g circle z and z circle g, for g=(m,d), shows that g centralizes z multiplicatively exactly when epsilon(d)n=n. Also

\[
g*z=((\varepsilon(d)-1)n,2dc\pmod4).
\]

Consequently the two indices are:

| Element z | Additive index in (4) | Multiplicative index in (4) |
|---|---:|---:|
| (0,0) | 1 | 1 |
| (n,0), n nonzero | 1 | 2 |
| (0,1) | 2 | 2 |
| (n,1), n nonzero | 2 | 4 |

For the final case the second subgroup is Z times {0}, the kernel of the multiplicative projection onto the Klein group. This verifies (3) directly. The set is a normal subgroup of the multiplicative group, being the inverse image of the subgroup {0,1} of the abelian Klein quotient, but is not an additive subgroup. Even lambda-invariance fails: lambda_x(x)=(0,3) lies outside the set.

To check that the known positive theorem has not been contradicted, put u=v=(0,1) and w=(1,0). Then

\[
(u+v)\circ w=(-1,2),\qquad
(u\circ w)-w+(v\circ w)=(1,2).
\]

The right skew distributive law fails. This is a left brace of abelian type, not a two-sided brace.

## 6. Current literature and precise credit

The 2025 paper's positive two-sided result and its finite four-element example are credited above. The 2026 Cascella--Properzi--Van Antwerpen postprint distinguishes finite lambda-orbits and finite additive conjugacy from property (s), and supplies the standard semidirect construction. Di Matteo--Ferrara, *Finite-index problems in skew braces*, arXiv:2607.20222v1, Theorem 5.2 and Corollary 5.4, assert and prove a related elementwise characterization by finite additive and multiplicative conjugacy classes and finite lambda-orbit. That characterization is consistent with this example, but it is not the original ideal-closure question and is not needed for this counterexample.

The July paper is a preprint; its presence is not described as peer review. The September arXiv version of the Cascella--Properzi--Van Antwerpen paper is labelled a postprint. The downloaded primary arguments and exact versions are recorded in the source manifest. No claim is made to have independently recertified every result in those papers.

A bounded current-source search did not identify this exact counterexample or a prior resolution of the original ideal question. That does not establish novelty. The result here is the direct infinite-brace construction and exact index calculation, not the invention of the four-element brace or of semidirect products.

The verifier checks the finite component, symbolic integer-coordinate identities, bounded exact group/brace controls and the reported fixed-set conditions. Finite quotients are not used to infer failure of property (s): in any finite quotient all the relevant indices are finite. The infinite-coset argument in Section 4 is the essential certificate.

## Sources

1. I. Colazzo, *Derived-indecomposable solutions and skew braces whose elements have a finite number of conjugates*, Oberwolfach Report 9/2023, pp.543--544, Question 1 and preceding definitions. [Full primary report](https://ems.press/content/serial-article-files/47003).
2. I. Colazzo, M. Ferrara and M. Trombetti, *On derived-indecomposable solutions of the Yang--Baxter equation*, Publ. Mat. 69 (2025), 171--193; Definition 3.7, Example 3.8, Proposition 3.10 and the following open-status statement. [Full published primary PDF](https://mat.uab.es/pubmat/fitxers/download/FileType%3Apdf/FolderName%3Av69%281%29/FileName%3A6912508.pdf).
3. R. Cascella, S. Properzi and A. Van Antwerpen, *Finiteness conditions on skew braces and solutions of the Yang--Baxter equation*, arXiv:2603.06177v2, 14 September 2026, labelled postprint; Definition 2.11 and Sections 4--5. [Primary version record](https://arxiv.org/abs/2603.06177v2).
4. M. Di Matteo and M. Ferrara, *Finite-index problems in skew braces*, arXiv:2607.20222v1, 22 July 2026, Proposition 5.1, Theorem 5.2 and Corollary 5.4. [Primary preprint](https://arxiv.org/abs/2607.20222v1).
