# Inverse Frobenius obstructs an integral polynomial classification

## Statement and scope

Fix a prime number `p`. Let `(K, theta)` be an existentially closed algebraically closed field equipped with a multiplicative map. Thus `theta(0)=0`, `theta` takes nonzero elements to nonzero elements, and its restriction to `K*` is a group endomorphism. Existential closedness is taken among algebraically closed fields with such a map. These are the models of ACFH. Their existence in every characteristic follows from d'Elbée's model-companion theorem; see [1], Corollary 3.16 and the characteristic discussion in Section 3.3.

The language is the field language, with an additional unary function symbol for `theta`. We use a totalized field inverse when convenient. The source question concerns first-order-definable endomorphisms of the multiplicative group, not merely functions given by terms. The counterexample below requires no parameters and its graph is already quantifier-free in the pure field language.

Write `E = End_def(K*)`. Its addition is pointwise multiplication:

    (f +_E g)(x) = f(x)g(x).

Its multiplication is composition. Consequently the ring zero is the constant-one map on `K*`, the ring identity is the identity function, and the integer `n` acts by the power map `[n](x)=x^n`. In particular, although the field has characteristic `p`, the ring element `[p]` is Frobenius, not the zero endomorphism.

For `P(X)=sum_(i=0)^d a_i X^i` in `Z[X]`, put

    P(theta)(x) = product_(i=0)^d theta^i(x)^(a_i),   x in K*.

Since theta is multiplicative, this agrees with applying each iterate to `x^(a_i)`. The image of this evaluation map is `Z[theta]`. Negative integer coefficients mean group inverses; they do not mean inverse Frobenius or fractional powers. The operator theta itself is not assumed additive, injective, or a field automorphism.

**Theorem.** If `char(K)=p>0`, there is a parameter-free definable endomorphism `rho` of `K*` with `rho` not in `Z[theta]`. Moreover `rho` extends to a field automorphism of `K` commuting with theta. Therefore the assertion that every definable multiplicative endomorphism belongs to `Z[theta]`, with no characteristic restriction, is false.

The proof occupies the next two sections. Section 4 supplies an independent proof of its only genericity input.

## Inverse Frobenius is definable

The map `F:K -> K`, `F(x)=x^p`, is bijective. It is surjective because K is algebraically closed. It is injective because `u^p-v^p=(u-v)^p`, and a field has no nonzero nilpotents.

Define `rho(x)` to be the unique `y` satisfying

    y^p = x.

This is a definition without parameters. For nonzero x, its unique root is also nonzero, so it restricts to a definable function on `K*`.

For all x and z,

    (rho(x)rho(z))^p = xz.

Uniqueness of p-th roots therefore gives `rho(xz)=rho(x)rho(z)`. Also `rho(1)=1`. This proves the required group-endomorphism property.

The same uniqueness argument, using the characteristic-p binomial identity, gives `rho(x+z)=rho(x)+rho(z)`. Together with `rho(0)=0` and bijectivity, this makes rho a field automorphism.

Finally,

    theta(rho(x))^p = theta(rho(x)^p) = theta(x).

Thus `theta(rho(x))=rho(theta(x))`. The equality also holds at zero. In particular, the map qualifies even under the stronger interpretation of an endomorphism preserving the whole expanded field structure. This additional fact is not needed for the source's multiplicative-group formulation.

## Inverse Frobenius is not an integral polynomial in theta

Polynomial evaluation `Z[X] -> E` is injective in every model of ACFH. This is [1], Corollary 5.7; Section 4 below proves it directly from existential closedness.

Suppose, for a contradiction, that `rho=P(theta)` for some `P` in `Z[X]`. Since `[p]` is the p-th power map, the defining equation for rho implies

    [p] composed with P(theta) = Id.

In the endomorphism ring, this is

    (pP(X)-1)(theta) = 0_E.

Faithfulness would imply the polynomial identity `pP(X)-1=0` in `Z[X]`. This is impossible: the constant coefficient `p a_0 - 1` is congruent to `-1` modulo p, so it is nonzero. This proves the theorem.

The argument uses equality of functions on all of `K*`. It is not a finite-field computation. On any single finite field an inverse Frobenius can be an ordinary integer power map; this does not contradict the theorem because a finite field with an operator is not an algebraically closed existentially closed model of the specified theory.

## A direct proof of polynomial faithfulness

### Extension lemma for abelian groups

Let H be a subgroup of an abelian group A, let D be a divisible abelian group, and let `h:H -> D` be a homomorphism. Then h extends to a homomorphism `A -> D`.

For completeness, use Zorn's lemma on compatible extensions, ordered by inclusion of their domains. Let `h_B:B -> D` be a maximal extension and suppose `a` is in `A` outside B. If no positive power of a lies in B, choose any `d` in D and extend to the subgroup generated by B and a by `h_B(b a^k)=h_B(b)d^k`. The representation is unique, so this is well-defined.

Otherwise let n be the least positive integer with `a^n` in B. Divisibility supplies d with `d^n=h_B(a^n)`. The same formula defines a homomorphism on the subgroup generated by B and a. To check it is well-defined, any relation `a^k` in B has k divisible by n, since the subgroup of integers with `a^k` in B is `nZ`; the equality `d^n=h_B(a^n)` then enforces compatibility with every such relation. Both cases contradict maximality. Hence B=A.

### Faithfulness lemma

Let `(K, theta)` be any model of ACFH, in arbitrary characteristic. If `Q(X)=sum_(i=0)^d b_i X^i` is a nonzero integer polynomial, then `Q(theta)` is not the constant-one map on `K*`.

Choose algebraically independent indeterminates `t_0,...,t_d` over K and let L be an algebraic closure of `K(t_0,...,t_d)`. The group `L*` is divisible.

Inside `L*`, let H be generated by `K*` and `t_0,...,t_(d-1)`. When d=0, take H=`K*`. Algebraic independence implies that every element of H has a unique expression

    c product_(i=0)^(d-1) t_i^(m_i),  c in K*, m_i in Z.

Indeed, a nontrivial Laurent-monomial relation over K would yield a nonzero polynomial relation among the indeterminates after denominators were cleared.

Define a homomorphism `h:H -> L*` by

    h(c product t_i^(m_i)) = theta(c) product t_(i+1)^(m_i).

It is well-defined by that uniqueness, and it extends theta on `K*`. The extension lemma extends h to `theta_L:L* -> L*`. Set `theta_L(0)=0`. The expanded algebraically closed field `(L, theta_L)` is therefore an extension of `(K, theta)` in the base theory. It satisfies

    theta_L^i(t_0) = t_i,  0 <= i <= d.

Thus

    Q(theta_L)(t_0) = product_(i=0)^d t_i^(b_i) != 1.

The inequality follows again from algebraic independence because the vector of coefficients of Q is not zero. This also covers nonzero constant Q and negative coefficients.

The sentence asserting the existence of a nonzero x for which `Q(theta)(x) != 1` is existential in the chosen language. It holds in the extension `(L, theta_L)`, so existential closedness makes it hold already in `(K, theta)`. This proves the lemma and the injectivity of polynomial evaluation.

No saturation hypothesis, classification of definable sets, elimination of imaginaries, independence calculus, or assumption that theta is additive is used in this proof.

## The coefficient ring forced by positive characteristic

The counterexample also identifies a necessary enlargement of the proposed ring. In characteristic p, `[p]` is an invertible endomorphism whose inverse is rho. The integer endomorphisms commute with every multiplicative group endomorphism. Their invertible members have commuting inverses as well. Alternatively, commutation of rho with theta was proved explicitly above.

Consequently there is a ring homomorphism

    Z[1/p][X] -> E,    P(X)/p^n |-> rho^n composed with P(theta).

It is well-defined: equal fractions become equal after multiplying by a common power of p, and composition by the corresponding Frobenius power is invertible. It is injective: if its value is zero, composing with `[p^n]` gives `P(theta)=0_E`, so faithfulness gives `P=0`.

Its image is precisely the subring generated by theta and inverse Frobenius. It strictly contains `Z[theta]` by the theorem. This proves only an inclusion into all definable endomorphisms. It does not classify every definable endomorphism.

## What is and is not resolved

1. The universal equality with `Z[theta]` over all models of ACFH is disproved; a counterexample occurs in every positive characteristic.
2. The same conclusion holds whether definability permits parameters or forbids them.
3. Restricting the assertion to characteristic zero removes this counterexample. That restricted assertion is not resolved here.
4. Replacing the proposed ring by `Z[1/p][theta]` in characteristic p also removes this counterexample. Equality with the full definable endomorphism ring is not resolved here.
5. Generic theta is a multiplicative-group endomorphism. No inverse theta was introduced. Inverse Frobenius is available because a perfect field has unique p-th roots, independently of theta's genericity.
6. The work supplies a complete candidate argument for the literal source scope, not a novelty certificate or evidence of acceptance. Independent mathematical review is still required.

## References

[1] Christian d'Elbée, *Generic multiplicative endomorphism of a field*, arXiv:2212.02115v4, revised 17 January 2025, especially Corollary 3.16, Section 3.3, Section 5.1, Corollary 5.7, and Question 5.8. https://arxiv.org/abs/2212.02115v4 . Published in *Annals of Pure and Applied Logic* 176 (2025), 103554, https://doi.org/10.1016/j.apal.2025.103554 . The inspected full text is the versioned arXiv PDF.

[2] Christian d'Elbée, contribution on generic multiplicative endomorphisms, in *Model Theory: Combinatorics, Groups, Valued Fields and Neostability*, Oberwolfach Reports 20 (2023), report 2, printed pp. 97–98. https://doi.org/10.4171/OWR/2023/2 . Public PDF: https://ems.press/content/serial-article-files/46996 .
