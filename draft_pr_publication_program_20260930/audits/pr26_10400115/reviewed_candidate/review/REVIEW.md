# Independent review: algebraic-coefficient braid representations

**Verdict: PASS for the stated partial results and precise obstruction to the attempted route.** The package does not solve the target for $n\geq4$, and the unresolved disposition must remain. No substantive mathematical correction is required.

**Target:** 10400115, Bigelow's Problem 6.7.  
**Reviewed document:** OBSTRUCTION.md.  
**SHA-256:** 8237a910fc2423e3d55ca09cd9bf0bc4300d588e9279b25fe78d41f0037a3995.  
**Date:** 30 September 2026. **Reviewer model:** gpt-6-astra, xhigh.

This is an independent AI mathematical and source review, not human peer review or formal verification. The elementary observations are not credited as new discoveries.

## Source fidelity and scope

The rendered page of [Ohtsuki's problem collection](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), printed p. 470, Problem 6.7, visibly has a bar over $\mathbb Q$. The question asks for a faithful representation by matrices over algebraic numbers without fixing its dimension. The adjoining remark identifies the higher-strand range and the algebraic-specialization issue. It also literally prints $\mathrm{GL}(2,\mathbb Z)$ for the three-strand case, so the package has not introduced that typographical error.

[Scherich's 2023 paper](https://msp.org/agt/2023/23-5/agt-v23-n5-p03-s.pdf), Theorem 1.1, proves discreteness of specified Salem-number specializations. Corollary 3.10 applies this conclusion to Lawrence–Krammer representations, and Example 3.11 exhibits a four-strand choice. Those statements make no injectivity conclusion. A discrete image can arise from a homomorphism with a kernel, so this literature does not supply the missing step. The review checked the theorem, its proof, the corollary and the example in the primary paper.

A bounded additional search did not locate a resolution of the exact higher-strand algebraic-coefficient target. This is consistent with the package's limited-search wording, and it is not a universal certification of the current literature.

## Restriction of scalars

The equivalence between finite-dimensional faithful representations over $\overline{\mathbb Q}$ and over $\mathbb Q$ is correct for finitely generated groups when the dimension may increase. A finite generating set contributes only finitely many algebraic entries. They generate a number field $K$, and matrix inverses stay over $K$, so every group element is represented over that field.

A $K$-linear automorphism of $K^d$ is also a $\mathbb Q$-linear automorphism of its underlying vector space of dimension $d[K:\mathbb Q]$. This operation is injective on the full matrix group: an operator acting identically on the underlying vector space already acts identically over $K$. The converse is the field inclusion. Nothing here bounds or preserves the original matrix dimension.

## The specialization obstruction

For a finite set of nonidentity elements of a faithful Laurent-polynomial representation, choose one nonzero entry from each difference from the identity. Their product, together with the finitely many necessary denominator or invertibility factors, is a nonzero polynomial after clearing monomials. Rational points are Zariski dense in a finite-dimensional parameter space, so a valid rational point avoids that finite collection.

There is no analogous countable-avoidance conclusion for algebraic parameters. The package's explicit group makes the failure exact. Conjugation of the upper-unitriangular generator by the diagonal generator produces $U(x^k)$, for every integer $k$. Powers, inverses and products give $U(f)$ for every integer Laurent polynomial $f$. For any nonzero algebraic $\alpha$, an integer polynomial annihilating $\alpha$ therefore gives a nonidentity element of the original matrix group which specializes to the identity. The evaluation is a well-defined homomorphism because the only possible denominator is a power of the nonzero parameter.

This argument is a counterexample to the general inference from generic to algebraic faithfulness. It is not a counterexample to the existence of some other faithful algebraic representation, and it does not analyze the kernel of a particular braid specialization. The submitted note preserves both limitations.

## The three-strand repair

The centralizer argument correctly rules out an embedding of $B_3$ into $\mathrm{GL}_2(\mathbb Z)$. The infinite central generator would have to map to an infinite-order matrix. It cannot be scalar in that group. Every nonscalar two-by-two rational matrix has a cyclic vector and minimal polynomial of degree two; its centralizer is the two-dimensional commutative algebra $\mathbb Q[C]$. The entire braid image would lie in this centralizer, contradicting noncommutativity and injectivity.

The proposed scaled matrices do give a representation over $\mathbb Q$, since both sides of the braid relation acquire the same scalar factor. [Kassel–Turaev, Braid Groups, Appendix A, Lemma A.1 and Theorem A.2](https://web.math.ucsb.edu/~bigelow/books/kasselturaev.pdf), gives precisely the standard matrices used in the note and identifies their projective representation with $B_3/Z(B_3)$.

For $\rho(g)=2^{e(g)}\phi(g)$, determinants force $e(g)=0$ whenever $\rho(g)=I$. The projective isomorphism then forces $g=z^k$, and $e(z)=6$ forces $k=0$. The value $\rho(z)=-64I$ is correct. Thus the repair controls the infinite center instead of silently discarding the central kernel of the modular representation. The trivial and infinite-cyclic cases $n=1,2$ also have the stated elementary representations.

## Checks and stopping point

The author's verification script was rerun in an isolated directory; its JSON receipt reproduced byte for byte. It checks the braid and center identities, eleven Laurent conjugation identities, and five annihilating-polynomial examples.

The separate independent_checks.py passed 35 exact assertions under SymPy 1.14.0. It checks the scaled relation, the modular orders, noncommutativity, central powers, representative centralizer equations, a restriction-of-scalars example over $\mathbb Q(\sqrt2)$, and four independently built specialization-kernel words. Reproduce from this directory with python independent_checks.py.

These calculations verify identities and examples. They neither establish higher-strand faithfulness from a finite word search nor prove that all higher-strand algebraic representations are impossible. The remaining requirement is a single finite-dimensional representation with uniform injectivity on every braid element. The package accurately stops short of that requirement and should be published only as unresolved partial analysis.
