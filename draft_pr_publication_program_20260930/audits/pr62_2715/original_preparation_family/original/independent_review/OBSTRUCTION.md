# Ribbon concordance with equal knot Floer homology: known cases and the exact gap

**Target:** 2715 / KP-1.56, proposed by Jennifer Hom.  
**Disposition:** unresolved in general; recommended `unsolved`, 1/5 substantive attempts.  
**Deliverable:** a credited affirmative case, an equivalent rank formulation, and a source-checked explanation of why the available functoriality and known equal-homology families do not resolve the general question. No new theorem of knot topology or novelty claim is made. Separate review is pending.

## 1. Exact source and direction convention

[K3, Problem 1.56, printed pp. 55–56](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf) asks whether two ribbon-concordant knots with isomorphic hat knot Floer homology must be isotopic. The surrounding text distinguishes this question from already-proved antisymmetry of ribbon concordance, from finiteness of descending chains, and from questions about fibering a particular concordance.

Write $J\le K$ when there is an upward annular movie from J to K containing births and saddles but no maxima; this is the direction in which knot Floer homology injects from J to K. Some authors describe the same relation with the opposite verbal “from/to” convention. All inequalities below use $J\le K$ as just defined.

Use the standard finite-dimensional, absolutely bigraded $\mathbb F_2$ vector space

$$\widehat{HFK}(K)=\bigoplus_{m,a}\widehat{HFK}_m(K,a).$$

The question is about the endpoint knot types. It does not require that a particular concordance be isotopic to a product annulus.

## 2. What split injectivity really yields

By [Zemke, Theorem 1.1 and its proof](https://annals.math.princeton.edu/wp-content/uploads/annals-v190-n3-p05-s.pdf), a decorated ribbon concordance C from J to K induces a bigrading-preserving map $F_C$ such that the reverse decorated concordance $\overline C$ satisfies

$$F_{\overline C}F_C=\mathrm{id}_{\widehat{HFK}(J)}.\tag{2.1}$$

In particular, each graded summand of $\widehat{HFK}(J)$ injects into the corresponding summand for K. If the two homologies are isomorphic, then $F_C$ is an isomorphism and $F_{\overline C}=F_C^{-1}$ on hat homology.

In fact, under the ribbon hypothesis, equality of **total dimensions** already implies this conclusion. The nonnegative differences

$$\dim\widehat{HFK}_m(K,a)-\dim\widehat{HFK}_m(J,a)$$

have sum zero, so they all vanish. Thus the full question is equivalent to asking whether

$$J<K\quad\Longrightarrow\quad
\dim\widehat{HFK}(J)<\dim\widehat{HFK}(K),\tag{2.2}$$

where $J<K$ means $J\le K$ with nonisotopic endpoints.

This equivalence does not prove (2.2). An isomorphism of the Floer maps does not supply a ribbon concordance in the reverse direction. Reversing the movie changes index-0 critical points into index-2 critical points, so $\overline C$ is an ordinary concordance but is not automatically ribbon. Therefore [Agol's antisymmetry theorem](https://doi.org/10.1090/cams/15) cannot be applied merely because $F_{\overline C}$ is an algebraic inverse.

Zemke's proof itself explicitly warns that $\overline C\circ C$ need not be isotopic to the product annulus although its Floer map is the identity. This is a direct warning against a geometric-triviality inference from (2.1), not a counterexample to the endpoint-isotopy question.

As a formal diagnostic, take the category with two objects 0 and 1, identities, and a single nonidentity morphism $0\to1$. It is a partial order. Sending both objects to $\mathbb F_2$ and the arrow to the identity linear map produces a functor that takes a noninvertible arrow to a split isomorphism. This is only a logical model showing that antisymmetry plus split functoriality is insufficient; it is not asserted to be realized by knots.

## 3. A known affirmative class

Call a knot residually nilpotent here when the **commutator subgroup of its knot group** is residually nilpotent. This is the terminology in [Boninger, Positive knots and ribbon concordance, Section 4](https://msp.org/pjm/2025/335-1/pjm-v335-n1-p04-p.pdf). It must not be confused with a statement about the lower central series of the entire knot group.

The precise imported result is Gordon's Lemma 3.4, restated as Boninger's Lemma 4.1:

> If $J\le K$, the knot K is residually nilpotent in this sense, and the Alexander polynomials have equal degree, then J and K are isotopic.

Here degree can be taken as the span of the Laurent polynomial, or equivalently the degree after multiplying by a monomial to give a nonzero constant term. The hypotheses and conclusion were read in the full published Boninger paper. The full 1981 Gordon article was not recovered; this package does not claim a line-by-line reproof of Gordon's group-theoretic argument.

The graded Euler characteristic identity is

$$\Delta_K(t)=\sum_{m,a}(-1)^m\dim_{\mathbb F_2}\widehat{HFK}_m(K,a)t^a.\tag{3.1}$$

It follows immediately that isomorphic bigraded knot Floer homology gives equal Alexander polynomials, hence equal degree. Combining (3.1) with the imported lemma proves the following credited consequence:

**Known affirmative case.** If $J\le K$, $\widehat{HFK}(J)\cong\widehat{HFK}(K)$ and the commutator subgroup of $\pi_1(S^3\setminus K)$ is residually nilpotent, then J and K are isotopic. Equality of total hat ranks suffices by Section 2.

Fibered knots belong to this class: their infinite cyclic covers are products of their fiber surfaces with the line, so their commutator subgroups are free groups, which are residually nilpotent. The fibered equal-genus case is also explicitly discussed by Zemke in Section 1.5. More generally Boninger's Theorem 4.2 credits Mayland–Murasugi with residual nilpotence for pseudoalternating knots whose Alexander polynomial has prime-power leading coefficient.

Consequently any counterexample to the general question must have a successor K outside this residually nilpotent class. Both endpoints must also be nonfibered: if either endpoint is fibered, equality of bigraded knot Floer homology and the standard fiberedness-detection theorem make the other fibered, and the preceding result applies. These are necessary exclusions, not evidence that a counterexample outside the class exists.

## 4. Why the standard equal-homology families are not counterexamples

The source specifically warns about the band-twist families of Hedden–Watson and Wang. Their exclusion can be made precise without guessing a ribbon movie.

In the accessible [Wang preprint](https://arxiv.org/abs/2006.01070), Theorem 1.3 states that the knots $K_n$ obtained by adding n full twists to a fixed nontrivial band joining a split two-component link have isomorphic bigraded hat knot Floer homology. This is the result cited as Theorem 1.2 in the published-source numbering used by K3.

Theorem 1.8 of that preprint gives

$$Kh(K_n;\mathbb F_2)\cong Kh(K_\#;\mathbb F_2)
\oplus h^{2n}q^{4n}H_b,\qquad H_b\ne0,\tag{4.1}$$

where $H_b$ is a finite-dimensional bigraded vector space independent of n. Therefore all total Khovanov dimensions are equal, but the bigraded vector spaces are different for distinct n. The latter also follows by canceling the fixed finite-dimensional summand and observing that a nonzero finite-support graded vector space cannot be invariant under a nonzero grading translation.

The split-injectivity theorem of Levine–Zemke for ribbon concordances, recalled directly in Wang's introduction, would turn any ribbon concordance between two members into a graded injection. Equal total dimensions would make it a graded isomorphism, contradicting (4.1). Thus distinct members of these familiar equal-HFK families are not ribbon concordant in either direction. Ordinary concordance is not a substitute for the missing ribbon hypothesis.

## 5. What the 2026 results add

The current [Baldwin–Hanselman–Sivek preprint, arXiv:2602.21109](https://arxiv.org/abs/2602.21109), Theorem 1.2, proves that any knot has only finitely many **fibered** predecessors. Corollary 1.3 gives finiteness of all predecessors when the successor is fibered. This does not prove that equal-HFK predecessors are unique for an arbitrary nonfibered successor. Its Introduction and Question 1.8 retain a nonfibered finiteness gap.

[Hom–Park, arXiv:2608.06625](https://arxiv.org/abs/2608.06625), proves, among other results, rigidity for ribbon-comparable cables of the same companion (Theorem 1.2). [Dunkerley, arXiv:2606.20802](https://arxiv.org/abs/2606.20802), proves ribbon minimality for particular detected knots, including examples outside a classical nilpotence class (Theorems 1.5–1.6). These are useful further special cases; their stated hypotheses do not cover a general pair in KP-1.56. This package checks their stated scope and relevant introduction, not every proof in these recent preprints.

## 6. A conditional quantitative consequence, not a completed argument

Every knot's total hat knot Floer rank is odd: reducing (3.1) at t=1 modulo 2 gives

$$\dim\widehat{HFK}(K)\equiv\Delta_K(1)=1\pmod2.$$

If KP-1.56 had an affirmative answer, each strict downward step in a ribbon chain would decrease this rank by at least 2. A chain starting at K would then have at most

$$\frac{\dim\widehat{HFK}(K)-1}{2}$$

strict steps. Unconditionally, split injectivity merely shows that the ranks eventually stabilize along any infinite descending chain. It does not prove that the knots stabilize. The conditional bound therefore restates a consequence of the missing equality case and must not be advertised as a proved termination theorem.

## 7. Exact remaining gap and stopping point

No geometric argument was found that forces endpoint isotopy from the Floer isomorphism when the successor's commutator subgroup is not covered by the known rigidity theorem. No valid pair of distinct ribbon-comparable knots with equal hat knot Floer homology was constructed. A proposed band-twist source of counterexamples is ruled out by the independent Khovanov obstruction.

The route stops here as unresolved, rather than converting algebraic invertibility into a reverse ribbon movie or treating finite predecessor sets as singletons. All positive knot-theoretic statements above retain their original attribution; the formal category and finite-dimensional checks are diagnostics, not new examples in knot topology.
