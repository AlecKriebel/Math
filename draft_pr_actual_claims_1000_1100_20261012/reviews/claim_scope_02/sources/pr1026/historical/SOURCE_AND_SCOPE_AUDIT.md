# Source and scope audit

Checked 9 October 2026. Bounded primary-source search found no full all-genus
proof or counterexample. This is a search result, not a guarantee of current
openness or novelty. No GitHub or queue changes are part of this packet.

## Original and follow-up statement interfaces

1. **OWR 39/2010, p.2324, Conjecture 1.** The original calls the interior
   locus \(G^{(g)}\). It includes decomposable ppav and asks pure codimension
   \(g\). It explicitly gives emptiness for \(g=1,2\), products of three
   elliptic curves for \(g=3\), elliptic curve times the genus-three theta-null
   divisor for \(g=4\), and the union of the intermediate-Jacobian closure
   and elliptic curve times the genus-four theta-null divisor for \(g=5\).
   Source: https://ems.press/content/serial-article-files/46295

2. **Grushevsky–Hulek, arXiv:1103.1857v2 (10 January 2012), §2,
   pp.10–13, Conjecture 2.2.** The interior locus is renamed \(I^{(g)}\).
   The conjecture adds reducedness of its gradient scheme. The separate
   compactified gradient zero locus appears later. The class formula is
   explicitly conditional on the expected codimension; it cannot prove the
   hypothesis. Remark 2.1 distinguishes initial set-theoretic descriptions
   from the additional reducedness argument in low genus.
   Source: https://arxiv.org/abs/1103.1857v2

3. **Grushevsky–Salvati Manni, arXiv:0805.4148v1.** The corresponding locus
   is \((\partial\theta)_{\rm null}\). Theorem 6 already identifies the
   elliptic-factor/theta-null component. Proposition 12 and Theorem 13
   provide a rank-one-boundary dimension induction with an explicit
   boundary-meeting hypothesis. The packet does not silently drop it.
   Source: https://arxiv.org/abs/0805.4148

4. **Grushevsky–Hulek, arXiv:1103.1858v2 (21 April 2011).** Theorem 1.2
   establishes the empty cases and pure codimension for \(3\leq g\leq5\).
   Theorem 1.3 excludes certain extra boundary components through
   codimension five. These bounds are not an unrestricted classification
   of all higher-rank boundary strata.
   Source: https://arxiv.org/abs/1103.1858v2

5. **Hulek's problem sheet.** Problem 1.2 restates the interior conjecture;
   Problem 2.2 concerns a stronger compactified equality. They are distinct.
   The genus-five formula is taken from the exact OWR/arXiv texts rather
   than this sheet's text extraction. The curve-moduli restriction has a
   different ambient codimension.
   Source: https://homepages.math.uic.edu/~coskun/Problemsession_Hulek.pdf

## A newer partial claim requiring precise handling

Grushevsky–Salvati Manni, *Moduli of abelian varieties near the locus of
products of elliptic curves*, arXiv:2307.05238v2, dated 12 July 2023, has a
relevant Theorem 5 on p.3. Its second assertion concerns components
**containing the diagonal** and includes local smoothness. Its introduction
uses broader informal wording. The exact theorem is not a global resolution;
containing the full diagonal must not be replaced by an arbitrary component
or a single arbitrary intersection point. The arXiv record lists v2 as a
TeX-only correction of v1. No later version or journal acceptance was
verified in this search.

The local argument in this packet independently proves only the explicit
generic three-odd-factor statement of Proposition 4.1. It does not certify
the full Theorem 5 or its smoothness assertion.

Source: https://arxiv.org/abs/2307.05238v2

### Lemma 23: precise limitation of the stated criterion

In v2, p.20, Lemma 23 considers an irreducible affine scheme
\(X=\operatorname{Spec}\mathbb C[x_1,\ldots,x_N]/(F_1,\ldots,F_k)\),
a point \(x\in X\), and the maximal ideal \(M_x\) of the ambient local
ring. It defines \(N(h)\) using algebraic independence of equation images
modulo \(M_x^h\), then claims \(\dim X\leq N-N(h)\). The following
distinction matters:

- **Literal quotient-ring reading.** Since each \(F_i(x)=0\), its image in
  the Artinian quotient is nilpotent and hence algebraic over \(\mathbb C\).
  No individual image is algebraically independent. Consequently this
  reading gives \(N(h)=0\) and no useful dimension bound. This is a
  vacuity observation, not a counterexample to the literal inequality.
- **Polynomial-truncation reading.** If one instead counts independent
  polynomial jet representatives, independence does not control the
  height of their common zero ideal. For example \(F_1=u\), \(F_2=uv\)
  are algebraically independent in \(\mathbb C[u,v]\), but
  \((u,uv)=(u)\) defines an irreducible reduced line of dimension one.
  The claimed bound with \(N=2,N(h)=2\) would incorrectly give zero.
  Independence follows because the monomials \(u^a(uv)^b=u^{a+b}v^b\)
  have distinct exponent pairs. The example also works for these
  polynomials viewed as formal power series.

Thus that algebraic-independence criterion is not used here. Proposition
24 cites the lemma in the local dimension argument. The analytic slice
proof in this packet instead controls the actual common zero set with
uniform convergent remainder estimates. Its coefficient agrees with the
source's notation: the source defines
\(\phi=f''/f\) and \(\psi=f''''/f-\phi^2\), so its
\(\psi-2\phi^2\) equals the packet's \(\gamma-3\beta^2\).
**No counterexample to the theta conjecture or to the asserted local
dimension conclusion follows from the lemma issue.**

## Search boundary

The original exact report, the two Grushevsky–Hulek papers, the
Grushevsky–Salvati Manni high-multiplicity paper, Hulek's problem sheet,
the 2023 diagonal preprint, its current arXiv version record, and the
author's public paper list were inspected. Searches included the exact
odd-two-torsion/pure-codimension phrases, recent-year restrictions, and
the 2023 preprint identifier with correction terms. The author list is
https://www.math.stonybrook.edu/~sam/papers.html .

The 2023 preprint is an important additional partial result. Its presence
does not establish that every global component is accessible to the
diagonal calculation. Search snippets, secondary summaries, and conditional
class formulas were not promoted to full theorems.
