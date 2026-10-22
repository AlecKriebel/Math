# Turn 4: no parameter-free definable power predicate in the Puiseux model

Status: an obstruction to explicit predicate elimination, not to finite axiomatizability by arbitrary sentences. This uses the credited model from Turn2. The source already proves nonuniqueness of predicate expansions by another method; no historical priority is asserted here.

## 1. Scaling automorphisms

Return to M, the nonnegative finite Puiseux polynomials over the real algebraic numbers with integer constant coefficient. For every positive real-algebraic a, define

sigma_a(Σ c_q X^q)=Σ c_q a^q X^q.

Positive rational powers a^q belong to the real algebraic field and satisfy the usual multiplicative identities. Therefore sigma_a is a ring automorphism, with inverse sigma_(1/a), and it preserves the integer constant coefficient. Its leading coefficient has the same sign as before, so it is an ordered-ring automorphism and restricts to an L_OR automorphism of M. It fixes every standard integer.

If a polynomial u has degree1 and positive leading coefficient c, then sigma_(3/2)(u) has leading coefficient3c/2 at the same degree. Hence

u < sigma_(3/2)(u) < 2u.

All lower coefficients, including a possibly negative constant, are irrelevant to these strict comparisons.

## 2. No definable TEIP_P2 expansion without nonstandard parameters

Suppose that P⊆M were definable without parameters and that (M,P) satisfied the two power-predicate axioms P2-IP and P2-Div. Apply interval density to X to get u∈P with u≤X<2u. Leading-degree comparison forces u to have degree1. Definability makes P invariant under sigma_(3/2), so v=sigma_(3/2)(u) also belongs to P and u<v<2u.

The ordered-division axiom gives w∈P⊆M with uw=v. Since u>0, the inequalities force1<w<2, impossible in a discretely ordered ring. This contradiction proves that no parameter-free definable predicate supplies such an expansion. The same proof allows any standard parameters, since all scaling automorphisms fix them.

Consequently there is no parameter-free L_OR formula delta(u) such that TEIP proves the two power-predicate axioms with P2 replaced by delta. The model M satisfies TEIP but refutes the proposed uniform interpretation for every such formula. This strengthens the failure of the particular oddless replacement in Turn2.

It does not rule out definitions using arbitrary nonstandard parameters, interpretations which change the domain or the base arithmetic structure, or finite axiomatizations of TEIP which do not define a power predicate.

## 3. The missing predicates exist externally in many explicit forms

For a positive real-algebraic a, set

P_a={2^k a^q X^q:q>0 rational,k∈Z} ∪ {2^k:k∈N}.

This is sigma_a(P_1), so it gives a valid TEIP_P2 expansion. It can also be checked directly by leading-coefficient bracketing and quotient closure. Thus the absence of a definable expansion is not an absence of expansions.

For example P_1 and P_3 have no common nonstandard element. Equality2^k X^q=2^l 3^r X^r forces q=r>0 and 3^q=2^(k-l). Clearing the positive denominator of q contradicts unique prime factorization in the ordinary integers. More generally distinct odd primes give pairwise disjoint nonstandard parts of these predicates. This is consistent with all of them having the same ordinary powers of2 as standard elements.

## 4. A definable memoryless strategy shortcut is unavailable

Suppose a parameter-free definable function F:M_(>0)->M_(>0) always returns a legal response F(x)≤x<2F(x) and is safe for every three-round sequence when used without memory. Its image P is definable by an existential formula and is interval-dense. Any three elements of its image can occur as three responses, with repetitions allowed, so P has no forbidden triple uv<w<2uv. It also excludes0. By the credited equivalence of the power-predicate axioms (Lemma3.7 of the primary paper), this would be a definable TEIP_P2 expansion, contradicting Section2.

Thus this model satisfies all finite game axioms but has no parameter-free definable memoryless strategy even for the three-round game. History-dependent or nondefinable strategies are not excluded. One cannot extract a uniform explicit selector from finite game truth without an additional definability argument.

## 5. Remaining target gap

Finite axiomatizability of the reduct theory does not imply that its models have a definable power predicate. The scaling argument therefore blocks one route to a positive finite axiomatization but supplies no model of IOpen+A_N failing a later axiom. The original yes/no question remains open in this attempt.

`verify_turn4.py` checks exact scaling automorphisms on bounded-denominator rational samples, the degree-one separation inequalities and prime-exponent obstructions. It is not a test of first-order definability.
