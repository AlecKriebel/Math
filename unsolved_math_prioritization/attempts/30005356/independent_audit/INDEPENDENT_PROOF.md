# Inverse Frobenius in existentially closed multiplicative fields

## Exact assertion

Let T be the theory of algebraically closed fields equipped with a unary map theta that is zero precisely at zero and is a homomorphism on the multiplicative group. Fix a prime p. There are existentially closed models of T of characteristic p. In every such model (K, theta), the parameter-free definable multiplicative endomorphism rho defined by rho(x)^p = x does not belong to the ring Z[theta]. This disproves the assertion with no characteristic restriction. This proof does not classify all definable endomorphisms.

The meaning of Z[theta] is important. Addition of multiplicative endomorphisms is pointwise multiplication, multiplication is composition, zero is the constant-one function on K*, and the integer n denotes x -> x^n. For Q(X) = sum b_i X^i, evaluation is Q(theta)(x) = product theta^i(x)^(b_i). Integer coefficients are ordinary integers, even when K has positive characteristic.

## Existence in positive characteristic

The model-companion result in d'Elbee, Corollary 3.16, already suffices: begin with the algebraic closure of F_p and the identity operator and embed this T-model in an ACFH model. A field embedding preserves its characteristic.

Existence also follows without the geometric axiomatization. Here is the standard countable construction in enough detail for the present case. Begin with the countable T-model M_0 = (F_p^alg, Id). Given a countable T-model M_n, list every existential formula with a quantifier-free matrix and a finite tuple of parameters from M_n. Process this countable list in sequence. At each step, if the current T-model has a T-extension realizing the listed formula, choose such an extension and a witness; otherwise keep the current model. A countable elementary substructure of the chosen extension containing the old model and witness exists by downward Lowenheim-Skolem, so every step can remain countable. At the end of the list let M_(n+1) be the union.

Every chain union used here remains a T-model: a polynomial and all its coefficients occur at one stage, so its root is available there; field axioms, multiplicativity and nonvanishing of theta are preserved by the inclusions. Let M be the union of the M_n. Suppose a quantifier-free existential formula over M has a witness in a T-extension N of M. Its parameters lie in some M_n. When that formula was considered during construction of M_(n+1), N was also an extension of the then-current model, so the realization branch was available and a witness was added. Thus M is existentially closed. Its characteristic remains p. This proves non-vacuity independently of the more substantial model-companion theorem.

This construction is an existence argument using ordinary choice and model theory, not an effective algorithm for deciding which extensions exist.

## Homomorphism extension lemma

If H is a subgroup of an abelian group A and D is divisible, every homomorphism h: H -> D extends to A. To prove this, choose by Zorn's lemma a maximal partial extension h_B on a subgroup B. If a is outside B and no positive power of a lies in B, freely assign any image d in D. Otherwise let n be the least positive exponent with a^n in B and choose d with d^n = h_B(a^n). Define the extension on B<a> by b a^k -> h_B(b) d^k. Every relation a^k in B has k in nZ, so this is well-defined in the second case; uniqueness of the free representation handles the first case. Either case contradicts maximality unless B=A.

This lemma does not require h to be injective or surjective. Its codomain may equal A; it is still a homomorphism-extension statement and imposes no additive field condition.

## Polynomial faithfulness from existential closedness

Let Q(X) = sum_(i=0)^d b_i X^i be a nonzero integer polynomial. Choose algebraically independent t_0, ..., t_d over K, and let L be an algebraic closure of K(t_0, ..., t_d). The subgroup

    H = K* times <t_0, ..., t_(d-1)>

is the direct product of K* and the free abelian group on these d generators. Indeed, a nontrivial Laurent-monomial relation over K would give a polynomial relation among the algebraically independent t_i. For d=0, use H=K*.

Define h on H by extending theta on K* and prescribing h(t_i)=t_(i+1) for 0 <= i < d. The direct-product description proves it is well-defined and multiplicative. Since L* is divisible, the extension lemma gives a map theta_L: L* -> L* extending h. Setting theta_L(0)=0 makes (L,theta_L) a T-extension of (K,theta).

For every i<=d, theta_L^i(t_0)=t_i. Hence

    Q(theta_L)(t_0) = product_(i=0)^d t_i^(b_i) != 1.

The inequality holds because Q is nonzero and the t_i have no nontrivial Laurent-monomial relation over K. This includes nonzero constants and coefficients divisible by p.

The witness transfers to K by existential closedness. Even if the language has no inverse-function symbol, the formula can be written as

    exists x [x != 0 and
      product_(b_i>0) theta^i(x)^(b_i)
      != product_(b_i<0) theta^i(x)^(-b_i)].

Every factor is nonzero; empty products are 1. Thus this is a quantifier-free matrix in the field language with theta. We conclude Q(theta) is not the zero endomorphism. Polynomial evaluation Z[X] -> End_def(K*) is injective.

This proves the needed content of Corollary 5.7 independently; it uses neither that corollary nor the more elaborate surjectivity theorem leading to it.

## The counterexample

In an algebraically closed field of characteristic p, x -> x^p is onto. It is also one-to-one, because u^p=v^p implies (u-v)^p=0 and hence u=v. Define rho(x) to be the unique y with y^p=x. Its graph is parameter-free and quantifier-free in the pure field language.

For x,z in K*, (rho(x)rho(z))^p=xz, so uniqueness gives rho(xz)=rho(x)rho(z). It preserves 1 and is bijective. The same argument with addition shows it is a field automorphism on K. Also

    theta(rho(x))^p = theta(rho(x)^p) = theta(x),

so rho and theta commute. Its restriction to K* is therefore a definable multiplicative endomorphism; it would even qualify if preservation of the whole expanded field structure were demanded.

If rho=P(theta) for an integer polynomial P, composing with the p-th power map gives

    (pP-1)(theta) = 0

in the endomorphism ring. Faithfulness would force pP-1=0 in Z[X]. Its constant coefficient is p a_0-1, which is -1 modulo p and cannot be zero. This is the contradiction.

One must not replace the ring element [p] by zero using the characteristic of the field. On K* it is the invertible Frobenius endomorphism. The endomorphism ring has characteristic zero by the faithfulness lemma.

## Scope remaining after the counterexample

Since Frobenius is invertible and central among multiplicative endomorphisms, the faithful map extends to Z[1/p][X] by sending P(X)/p^n to rho^n composed with P(theta). A common denominator proves well-definedness, and multiplying by the corresponding Frobenius power reduces injectivity to polynomial faithfulness. This strictly extends Z[theta]. It is only a subring of all definable endomorphisms; equality has not been proved.

In characteristic zero the inverse-p-th-root graph is not a function for p>1, so this counterexample does not settle that case. Neither the characteristic-zero classification nor the positive-characteristic classification over Z[1/p] is resolved here. The conclusion is a negative answer to the literal unrestricted assertion, with no novelty, priority, human-referee, or journal-acceptance claim.

## References

- Christian d'Elbee, Generic multiplicative endomorphism of a field, arXiv:2212.02115v4, Corollaries 3.15-3.17 and Section 5.1. https://arxiv.org/abs/2212.02115v4
- Christian d'Elbee, Generic multiplicative endomorphism of fields, contribution in Oberwolfach Report 2/2023, printed pp. 97-98. https://doi.org/10.4171/OWR/2023/2
