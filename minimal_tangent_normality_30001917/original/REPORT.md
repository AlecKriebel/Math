# Credited negative resolution of VMRT normality

## Result and exact question

The assertion associated with problem 30001917 / OWR-11139-010 is false in its source-level scope. This is a reconciliation with published mathematics, not a new counterexample.

In Jun-Muk Hwang's contribution to [Oberwolfach Report 47/2011](https://ems.press/content/serial-article-files/46361), printed pages 2690–2692, the ambient space is a complex projective manifold $X$. A component $K$ of its rational-curve space is called minimal dominating when the curves through a general $x\in X$ form a nonempty complete family. This is the locally unsplit condition; the definition does not demand least degree among all covering families. The normality assertion concerns the whole reduced tangent image $C_x\subset\mathbb P(T_xX)$ for general ambient $x$, not just normality at a general point of $C_x$. The discussion emphasizes $\dim K_x=\dim X-2$, and a subsequent classification theorem assumes normality. That conditional theorem is not invalidated here.

To avoid ambiguity, write $\widetilde K_x$ for the normalized space of members through $x$, $\nu_x:\widetilde K_x\to C_x$ for the tangent map to its reduced image, and $j:C_x\hookrightarrow\mathbb P(T_xX)$ for inclusion. The original report suppresses this normalization distinction. [Hwang–Mok, Theorem 1 and Corollary 1](https://hkumath.hku.hk/~nmok/IMR2004-011.pdf), together with the tangent-map finiteness theorem cited there, identifies $\nu_x$ as normalization and $\widetilde K_x$ as smooth for general $x$. Both examples below have irreducible $\widetilde K_x$ and irreducible $C_x$; reducibility is not the obstruction.

## The elementary normalization implication

Let $\nu:Y\to Z$ be a finite birational morphism of integral complex varieties, with $Y$ normal. Then $\nu$ is the normalization. Indeed, over an affine open $\operatorname{Spec} A\subset Z$, its inverse image is $\operatorname{Spec} B$, where $A\subset B\subset\operatorname{Frac}(A)$, $B$ is integral over $A$, and $B$ is integrally closed. Every element integral over $A$ is integral over $B$ and so belongs to $B$. Conversely every element of $B$ is integral over $A$. Thus $B$ is exactly the integral closure of $A$.

If $Z$ were normal, this gives $A=B$ on every such open, hence $\nu$ would be an isomorphism. Consequently either of the following disproves normality:

1. $\nu$ is not an isomorphism, for example because it is not injective.
2. If $Y$ is smooth and $Z\hookrightarrow M$ is a closed embedding into a smooth ambient variety, the composite $Y\to M$ has a noninjective differential somewhere. Were $\nu$ an isomorphism, that composite would be a closed embedding with injective differential everywhere.

The second implication does not assert that every singular variety is nonnormal. It uses the finite birational map from a smooth normalization.

## Counterexample within the codimension one setting

The published input is [Casagrande–Druel, Example 1.6, Proposition 1.7, Theorems 1.9–1.10 and Example 5.8](https://druel.perso.math.cnrs.fr/textes/minimal.pdf). Specialize their parameters to $n=3,a=2,d=4$. Let $A\subset\mathbb P^2$ be a smooth quartic. In $Y=\mathbb P_{\mathbb P^2}(\mathcal O\oplus\mathcal O(2))$, let $\pi:Y\to\mathbb P^2$ be the bundle projection and choose the section $G_+$ with normal bundle $\mathcal O(2)$, and put

\[
X=\operatorname{Bl}_{G_+\cap\pi^{-1}(A)}Y.
\]

Their results give a smooth Fano threefold of Picard number three and an irreducible locally unsplit dominating component $V$ with anticanonical degree three. For general $x\in X$, its normalized family $\widetilde V_x$ is a smooth connected genus-seven curve. The reduced tangent image $C_x\subset\mathbb P(T_xX)=\mathbb P^2$ is an irreducible sextic, and $\widetilde V_x\to C_x$ is its normalization. Remark 5.4 explicitly says this component is not degree-minimal for any ample polarization. That does not exclude it from the report's definition.

Here is the complete deduction of the requested negative answer from these published inputs. Smoothness of $X$, irreducibility of $V$, dominance, and properness of the general-point family are precisely the report's hypotheses. The family has dimension one at $x$, so it also satisfies $\dim V_x=3-2$. An integral plane curve of degree six has arithmetic genus

\[
p_a(C_x)=\frac{(6-1)(6-2)}2=10.
\]

For completeness, this follows from $0\to\mathcal O_{\mathbb P^2}(-6)\to\mathcal O_{\mathbb P^2}\to\mathcal O_{C_x}\to0$ and $\chi(\mathcal O_{\mathbb P^2}(t))=(t+1)(t+2)/2$. Thus $\chi(\mathcal O_{C_x})=1-10=-9$, while the smooth normalization has Euler characteristic $1-7=-6$. Isomorphic proper curves have equal Euler characteristics, so the normalization cannot be an isomorphism. The preceding lemma proves that $C_x$ is not normal.

More precisely, the cokernel $Q=\nu_{x*}\mathcal O_{\widetilde V_x}/\mathcal O_{C_x}$ has finite support, and finiteness of $\nu_x$ gives

\[
\operatorname{length} Q
=\chi(\mathcal O_{\widetilde V_x})-\chi(\mathcal O_{C_x})=3.
\]

This is a positive, exact normalization defect. It does not, by itself, count singular points or prove that there are three nodes. In this example the tangent normalization map is immersive but not injective; failure of immersion is unnecessary for the negative answer.

## Counterexample with actual degree minimality and Picard number one

The stronger alternative uses [Hwang–Kim, Theorem 1.3, Propositions 6.3–6.7 and its proof on page 191](https://content.algebraicgeometry.nl/2015-2/2015-2-008.pdf). Set $n=6,d=3$. For general weighted-homogeneous $f(u_1,\ldots,u_6,w)$ of degree six, with weights $1,\ldots,1,2$, take

\[
X^f=\{z^2=f(u_1,\ldots,u_6,w)\}
\subset\mathbb P(1,1,1,1,1,1,2,3).
\]

Their results give a smooth Fano sixfold with $\operatorname{Pic}(X^f)=\mathbb ZL$, $ -K_{X^f}=5L$, and a single dominating family of $L$-degree-one rational curves. It is unsplit and genuinely degree-minimal. For general $x$, $\widetilde K_x$ is smooth, projective and irreducible of dimension three, while its tangent morphism to $\mathbb P(T_xX^f)$ is not immersive. Irreducibility is explicitly established in their proof for $n>d$. The hypotheses $d\ge3$ odd, $n>d$, and $n\ge2d$ all hold here. The general-point quantifier is essential.

Apply the normalization implication to $\nu_x:\widetilde K_x\to C_x$. If $C_x$ were normal, this finite birational morphism would be an isomorphism, forcing the composite into projective tangent space to have injective differential everywhere. The published failure of immersion contradicts this. Hence this irreducible VMRT is also nonnormal. Its dimension is three in $\mathbb P^5$, so this second example has codimension two; it is the first example above that directly covers the report's codimension-one focus.

## Attribution and limits

Both negative constructions are credited prior results, published in 2015. The Casagrande–Druel paper has an arXiv submission history beginning in December 2012; the version inspected here is the 2015 author-hosted journal article. This packet supplies a scope check and the elementary implication from their results to nonnormality. It does not claim to reprove their geometric existence theorems, to choose a fully numerical general polynomial, or to establish new mathematical novelty.

There is no remaining gap in rejecting the universal assertion, conditional on the cited published theorems. Classification of the families or varieties for which normality does hold is outside this disposition. The number of new mathematical research attempts is zero: literature retrieval, hypothesis verification, arithmetic checks and packaging do not count as turns.

## Bibliography

- Jun-Muk Hwang, “Varieties of minimal rational tangents of codimension 1,” contribution in *Complex Algebraic Geometry*, Oberwolfach Report 47/2011, printed pp. 2690–2692. [Report DOI](https://doi.org/10.4171/owr/2011/47).
- Cinzia Casagrande and Stéphane Druel, “Locally unsplit families of rational curves of large anticanonical degree on Fano manifolds,” *International Mathematics Research Notices* 2015, no. 21, 10756–10800. [DOI](https://doi.org/10.1093/imrn/rnv011), [author-hosted full article](https://druel.perso.math.cnrs.fr/textes/minimal.pdf), [arXiv history](https://arxiv.org/abs/1212.5083).
- Jun-Muk Hwang and Hosung Kim, “Varieties of minimal rational tangents on Veronese double cones,” *Algebraic Geometry* 2 (2015), no. 2, 176–192. [DOI](https://doi.org/10.14231/AG-2015-008), [journal PDF](https://content.algebraicgeometry.nl/2015-2/2015-2-008.pdf).
- Jun-Muk Hwang and Ngaiming Mok, “Birationality of the tangent map for minimal rational curves,” *Asian Journal of Mathematics* 8 (2004), no. 1. [DOI](https://doi.org/10.4310/AJM.2004.v8.n1.a6), [author-hosted full text](https://hkumath.hku.hk/~nmok/IMR2004-011.pdf).
