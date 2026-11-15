# A two-tail obstruction to ambient conjugation in Dlab groups

Alec Kriebel · [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X)

17 October 2026 · Version 1.0.0 · Unrefereed preprint

[Zenodo record](https://zenodo.org/records/23441890) · [DOI](https://doi.org/10.5281/zenodo.23441890) · [Open PDF](paper.pdf) · [Download PDF](paper.pdf)

## Original abstract

Let $G=D_{\langle2\rangle}([0,1])$ be the compactly supported, locally right $2^{\mathbb Z}$-affine Dlab group. We construct an automorphism preserving both Dlab orders and give a proof that it cannot be implemented after any embedding in either of two explicitly defined groups: all locally right affine increasing interval homeomorphisms, and all locally right affine increasing real homeomorphisms that are affine on an initial ray. The ambient slopes are unrestricted, and the embedding need not preserve an order. Perfectness separates the supports of commuting local groups; a two-tail construction handles both possible orientations of their least action components. This extends a one-tail mechanism used in prior work. The definitions and affine-germ decomposition of the standard Dlab families place them in these ambient groups. Consequently the construction gives an affirmative answer to the corrected Kourovka Problem 21.149, including arbitrary positive-real slope groups and the full and reflected extended-real families.

## The idea in plain English

An automorphism changes the elements of a group while preserving how they compose. Conjugation implements such a change by moving to new coordinates: the same coordinate change is applied before and after every group element. An automorphism can fail to be conjugation inside its own group yet become conjugation in a larger group.

This paper constructs an automorphism of a Dlab group for which that larger-group route also fails in the stated ambient groups. The conclusion holds after every abstract injective embedding, including embeddings that do not preserve an order. The slopes allowed in the ambient group can be any positive real numbers.

The construction uses infinitely many small affine bumps approaching both ends of the source interval. A faithful action can arrange the relevant local regions in either of two orientations. One of the two tails then forces a proposed conjugating map to have a descending sequence of support components, which the ambient endpoint conditions forbid.

## The precise result

All maps are increasing, and group multiplication is ordinary composition. A map is **locally right affine** when, at every finite point $a$ other than a right endpoint, there are $\epsilon>0$ and $s>0$ such that

$$f(x)=f(a)+s(x-a)\qquad(a\le x\le a+\epsilon).$$

Let $\mathcal A_I$ be the group of these homeomorphisms of $[0,1]$, **including a right affine germ at $0$**. Let $\mathcal A_{\mathbb R}$ be the group of these homeomorphisms of $\mathbb R$ that also agree with $x\mapsto sx+t$, for some $s>0$, on an **initial ray at $-\infty$**. Positive ambient slopes are unrestricted. Infinitely many affine pieces and accumulation of pieces from the left are permitted.

The source group is

$$G=D_{\langle2\rangle}([0,1])=\{f\in\mathcal A_I:\text{ every right slope lies in }2^{\mathbb Z},\ f=\mathrm{id}\text{ near }0\text{ and }1\}.$$

**Theorem 2.** There is one automorphism $\alpha$ of $G$ preserving both Dlab bi-orders such that, for either $A=\mathcal A_I$ or $A=\mathcal A_{\mathbb R}$, every injective homomorphism $e:G\to A$ and every $u\in A$ satisfy

$$e(\alpha(f))\ne u^{-1}e(f)u\qquad\text{for some }f\in G.$$

The same automorphism works for both ambients and every subgroup of either ambient. The embedding is arbitrary as an abstract group embedding; no order on the ambient or order preservation by the embedding is assumed.

**Corollary 8.** Equip $G$ with either Dlab order. For any multiplicative subgroup $H\le\mathbb R_{>0}$, the automorphism cannot be implemented by conjugation after any embedding into any of the eight standard real Dlab families

$$D_H(I),\quad D_{H*}(I),\quad D_{*H}(I),\quad\overline D_H(I),\qquad D_H,\quad D_{H*},\quad D_{*H},\quad\overline D_H.$$

This includes the full and reflected extended-real families and gives an affirmative answer to the corrected ambient-conjugation formulation of Kourovka Notebook Problem 21.149. The standard real-line families retain their defining initial affine behavior at $-\infty$; a rank-one restriction on $H$ is not imposed.

### Why the initial affine ray matters

**Proposition 7.** Let $\mathcal B$ consist of all increasing real homeomorphisms that are locally right $2^{\mathbb Z}$-affine at every finite point and have support bounded above, with **no condition at $-\infty$**. For every automorphism $\beta$ of $G$, there are an embedding $E:G\to\mathcal B$ and $v\in\mathcal B$ such that

$$E(\beta(f))=v^{-1}E(f)v\qquad\text{for every }f\in G.$$

The countermodel is explicit. For $n\in\mathbb Z$, take $I_n=(-2^{-n},-2^{-n-1})$ and the increasing affine bijection $\phi_n:[0,1]\to\overline{I_n}$. Define

$$E(f)|_{I_n}=\phi_n\beta^n(f)\phi_n^{-1},\qquad v(x)=\begin{cases}x/2,&x<0,\\x,&x\ge0.\end{cases}$$

The maps $E(f)$ fix every cell endpoint and are the identity on $[0,\infty)$. The relation $v\phi_n=\phi_{n+1}$ gives the displayed conjugation identity. For nonidentity $f$, its copies act nontrivially in every cell while fixing cell endpoints arbitrarily far left, so $E(f)$ is not eventually affine on an initial ray. Thus $\mathcal B$ is a genuine boundary of the theorem and is not identified with the standard reflected Dlab family.

## Why the result holds

Dlab's classical algebraic simplicity theorem makes the source group and its interval copies perfect. The affine-germ centralizer argument then separates the action supports of commuting local groups. Simplicity supplies faithful local actions, and exact finite-tuple interpolation gives a single global orientation for their least action components.

A homeomorphism $h$ with bumps approaching both source endpoints defines $\alpha(f)=h^{-1}fh$. Its interior slopes are powers of two, and conjugation preserves each first nontrivial right slope, hence both Dlab orders. The map $h$ itself has no right affine germ at $0$ and is not in $\mathcal A_I$.

Any proposed ambient implementation must act nontrivially in every selected local region. Depending on the global orientation, the left or right source tail forces its support components to descend indefinitely. Right affine germs and the initial real affine ray rule out that behavior. The proof uses classical simplicity, order and affine-germ machinery; the finite rational construction checks supplement the mathematical proof.

## Scope and limitations

The right germ at $0$ in $\mathcal A_I$ and eventual affine formula at $-\infty$ in $\mathcal A_{\mathbb R}$ are essential hypotheses. The theorem concerns these explicit ambient groups and their subgroups. It does not assert an obstruction in every homeomorphism group; Proposition 7 supplies the precise larger-group countermodel.

The defining maps are locally affine from the right, with arbitrary real breakpoints. They need not have finitely many pieces on a compact interval. Fixed initial neighborhoods arising from perfectness may depend on the element; a common fixed neighborhood for a whole perfect subgroup is not assumed.

The contribution concerns the unrestricted ambient slopes, arbitrary embeddings, and the full eight-family conclusion. Historical first priority remains unestablished. No claim about the present open status of related questions is made.

## Status and AI use

This is an unrefereed preprint. AI tools were used extensively in discovery, development, writing and checking, including separate AI research and adversarial-review agents. These checks are not independent human peer review. No formal proof-assistant verification of this theorem is claimed.

## Read the paper

Read the complete six-page published paper below. The PDF is the unchanged version 1.0.0 archived on Zenodo.

<iframe src="paper.pdf" title="A two-tail obstruction to ambient conjugation in Dlab groups — complete six-page paper PDF" width="100%" height="760" loading="lazy"></iframe>

[Open the complete PDF](paper.pdf) · <a href="paper.pdf" download>Download the complete PDF</a> · [Zenodo original PDF](https://zenodo.org/records/23441890/files/paper.pdf)

## Supporting materials

The complete original [source and verification ZIP](source-and-verification.zip) includes the LaTeX source, exact-rational construction checker, supporting notes and source attributions. <a href="source-and-verification.zip" download>Download the original ZIP</a> · [Zenodo original ZIP](https://zenodo.org/records/23441890/files/source-and-verification.zip)

The paper, source, verification code and original accompanying research notes are licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Cited third-party publications and formalizations retain their own licenses.

## Collaborate on this result

Independent verification, a substantial mathematical extension, or work toward a journal submission would be welcome. Authorship would be considered in relation to actual contributions.

## Cite this paper

Alec Kriebel. *A two-tail obstruction to ambient conjugation in Dlab groups*. Version 1.0.0, 17 October 2026. Zenodo. [doi:10.5281/zenodo.23441890](https://doi.org/10.5281/zenodo.23441890).

[Download BibTeX](citation.bib)

## Background and prior work

* V. Dlab's [*On a family of simple ordered groups*](https://doi.org/10.1017/S1446788700006261) supplies the classical algebraic simplicity and order theorems, and the affine-germ centralizer background.
* A. V. Zenkov and N. Ya. Medvedev's [*On Dlab groups*](https://doi.org/10.1007/BF02671746) supplies the standard real-line families and the affine-germ decomposition retaining the initial-ray hypothesis.
* T. Gong, Y. Yang and M. R. Zeng's [earlier one-tail result](https://arxiv.org/abs/2609.18630v1) treats six rank-one families with order-preserving embeddings. Its support obstruction is an explicit antecedent of the construction here.
* The [Kourovka Notebook](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-1.pdf), Problem 21.149, states the corrected larger-group question. W. van Doorn, E. Judin, P. Monticone and D. Morrison discuss the [original non-inner formulation and its clarification](https://arxiv.org/abs/2607.17477v2). The associated [pinned Lean formalization](https://github.com/pitmonticone/Kourovka/blob/64a4fe59b1df1893a0a1a68641d6806ccaaa7150/Kourovka/Problem_21_149.lean) addresses that original formulation; its formal verification is not a certification of the ambient theorem on this page.

[All research](/research/)
