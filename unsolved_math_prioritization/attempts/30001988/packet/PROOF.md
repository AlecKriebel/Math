# Exact target, partial results, and gap

## 1. Conventions and effective presentation

Work in ordinary differential fields of characteristic zero, with one derivation delta. This is the DCF_0 setting of the source, not a statement about positive characteristic or several commuting derivations.

Let K be computable, let L be a computable differential extension with a specified computable embedding of K, and let z in L be promised differentially transcendental over K. Put F = K<z>. A canonical computable presentation is the rational-function field

    F = K(z_0, z_1, z_2, ...),    delta(z_i) = z_(i+1),    z_i = delta^i(z).

Every expression uses finitely many z_i. The transcendence promise gives an injective evaluation map into L. Enumerating rational expressions and discarding duplicates by equality in L gives a computable presentation of the generated subfield. Converting an ambient element promised to lie in F back to an expression is a terminating search. No algorithm here decides whether an arbitrary z has the transcendence promise, or membership of an arbitrary ambient element in F. A merely abstract, uneffectively specified embedding is not an effective input.

For clarity write C_E for the constrained pairs over E, and T_E for its complement (the paper's convention). An admissible pair has p monic and algebraically irreducible, q nonzero, and ord(q) < ord(p). It is constrained when any two solutions of p=0, q!=0 in differential extensions have identical vanishing differential polynomials over E, equivalently generate E-isomorphic differential fields with the solutions matched. The target is T_F <=_T T_K. Replacing either oracle by its complement makes no difference to this Turing-reducibility question.

The full target allows constant K and allows its differential closure Khat to be algebraic over K. Neither class may be deleted from the problem. The 2014 theorem covers nonconstant K with Khat/K not algebraic; that theorem alone is insufficient for the full target. The source gate gives exact locations.

## 2. Why ordinary splitting is insufficient

As an ordinary field F is purely transcendental over K with an effective transcendence basis. Ordinary factorization reduces to factorization over K, uniformly under this presentation and promise. Only finitely many z_i occur in an input polynomial, and irreducibility over the corresponding finite rational-function field is preserved by adjoining the remaining algebraically independent variables.

This does not decide C_F. For every characteristic-zero differential field E, p(Y)=delta Y is algebraically irreducible in E[Y,delta Y,...]. Nevertheless (p,1) is not constrained: 0 and 1 are solutions, and h(Y)=Y vanishes at one but not the other. Thus ordinary irreducibility and differential isolation are different predicates. This is a counterexample to the proposed shortcut, not to the target reduction.

## 3. A rational-antiderivative obstruction

**Lemma 1.** For a in K with a!=0, there is no r in F with delta r = a z_0.

**Proof.** If r belongs to K, then delta r belongs to K, whereas a z_0 does not. Otherwise choose the largest index m such that r genuinely depends on z_m. In the rational function field K(z_0,...,z_(m+1)), the chain rule gives

    delta r = delta_K(r) + sum_(i=0)^m (partial r / partial z_i) z_(i+1),

where delta_K acts only on coefficients. The coefficient of the algebraically independent variable z_(m+1) is partial r / partial z_m; all other terms are independent of z_(m+1). It must be zero if delta r = a z_0. In characteristic zero, the kernel of partial/partial z_m on K(z_0,...,z_m) is K(z_0,...,z_(m-1)). This contradicts the choice of m. For m=0 the same argument removes z_0 and returns to the first case. QED.

**Lemma 2.** No solution y of delta y = a z_0, for a!=0, is algebraic over F.

**Proof.** If y were algebraic, the finite extension E=F(y) would be separable. The derivation extends uniquely to E and to a normal closure, and commutes with F-embeddings into that normal closure. Consequently differentiation commutes with field trace. With n=[E:F],

    delta(Tr_(E/F)(y)/n) = Tr_(E/F)(a z_0)/n = a z_0.

The element in parentheses lies in F, contradicting Lemma 1. Division by n uses characteristic zero. QED.

## 4. Exact constraint classification for a linear family

**Proposition 3.** For every a in K, (delta Y - a z_0, 1) belongs to C_F if and only if a!=0. For computable K, this family is decidable uniformly from field equality, with no T_K oracle.

**Proof.** For a=0 the two constant roots 0 and 1 from Section 2 refute constrainedness.

For a!=0, set b=a z_0. The polynomial delta Y-b is monic and algebraically irreducible, of order 1, and q=1 has order -1. Solutions exist: extend the derivation to the purely transcendental field F(s) by delta s=b. For any solution y and each j>=1,

    delta^j y = delta^(j-1) b in F.

Given h in F{Y}, substitute these fixed expressions for every positive derivative of Y, producing H(Y) in F[Y]. This H depends on h and b, not on the chosen solution. Lemma 2 says every solution y is algebraically transcendental over F. Hence h(y)=0 if and only if H is the zero polynomial. All solutions therefore have the same vanishing differential polynomials over F. The pair is constrained. The algorithmic claim follows by testing a=0. QED.

This proof includes constant bases and differentially closed bases. It neither decides arbitrary nonlinear pairs nor supplies a reduction for all inputs.

## 5. A precise specialization failure

Suppose K is itself differentially closed. Proposition 3 says (delta Y-z_0,1) is constrained over K<z>. For every specialization z_0 -> c in K, differential closedness gives b in K with delta b=c. Both b and b+1 satisfy delta Y-c=0, while Y-b distinguishes them. Therefore every specialized pair (delta Y-c,1) is unconstrained over K.

Thus even this first-order linear constrained pair loses constrainedness under every specialization into Khat=K. One cannot remove the algebraic-closure exception from the published specialization method simply by replacing its high-order points with arbitrary base-field points. This proves failure of that proposed method, not failure of the target theorem.

More generally, when Khat/K is algebraic, every element of Khat has differential order zero over K, since it already satisfies an ordinary algebraic polynomial over K. A procedure that searches Khat for constrained elements of arbitrarily high order has no witnesses in this case.

## 6. Constant bases: what the later primitive-element theorem repairs

Pogudin's theorem applies to a finitely differentially generated extension of finite ordinary transcendence degree that contains a nonconstant, even if the base derivation is zero. This removes the elementary primitive-element obstruction previously attached to a constant base. Existence yields an effective search in a computable presentation: enumerate candidate generators and rational differential expressions recovering all the given generators, and test the finitely many recovery equalities. An existence theorem is needed for termination; no effective numerical bound is being asserted.

There is also a direct way to supply a nonconstant when examining a tuple in Khat: adjoin an element t of Khat with delta t=1 before applying the theorem. The resulting finite differential extension has finite ordinary transcendence degree. This does not, by itself, prove the required constraint-oracle transfer: t cannot then be used as a coefficient in a formula required to be over K<z> unless its presence is eliminated or justified.

For a constant K, a constrained element of Khat that is itself constant must be algebraic over K. Indeed, if c were a transcendental constant satisfying (p,q), specialize every derivative variable to zero. The resulting p(Y,0,...) must vanish identically, and q(Y,0,...) is nonzero. Infinitely many a in K avoid its finitely many roots. The root a and c would then both satisfy (p,q), distinguished by Y-a, a contradiction. Hence a finite extension generated only by such constants is algebraic and has an ordinary primitive element. This treats the all-constant alternative in the primitive-element search.

These observations are useful ingredients for revisiting the constrained-extension proof. This packet does not claim that the entire constant-base transfer has been independently audited. In particular, the separate algebraic-dependence oracle in the cited 2014 Theorem 6.1 is stated there with a nontrivial-derivation hypothesis. Replacing one later primitive-element invocation alone does not check this earlier dependency. The full chain, including oracle uniformity and the specialization bounds, would have to be written and independently verified before promoting a constant-base extension of that theorem.

## 7. Precise remaining gap and stopping point

No decision procedure for all constrained pairs over K<z>, relative only to T_K, has been established here outside the cited theorem's hypotheses. The most concrete unresolved branch of this attempt is a computable differentially closed K: T_K is computable, yet this report does not decide T_(K<z>). Proposition 3 shows nontrivial constrained pairs really occur there, and Section 5 shows why the naive specialization route cannot classify them.

A second unfinished dependency task is to turn the constant-base primitive-element repair into a complete uniform oracle reduction without importing an unproved constant-base algebraic-dependence algorithm. The paper's stronger hypotheses are retained until that work is done. Neither missing proof is evidence of a counterexample, and a literature search not locating a full resolution is not a proof that none exists.

Five substantive approaches are exhausted for this attempt. Classification remains **unsolved**; no full-target candidate is submitted for verification.
