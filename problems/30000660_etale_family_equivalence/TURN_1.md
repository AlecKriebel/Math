# Author turn 1: a smooth Russell-form family obstructing étale equivalence

**Result:** a complete negative answer to the literal étale conclusion of OWR2007 Problem2, over k=F_p-bar for every prime p. This is an application of the classical Russell form on p.527 of Russell1970, not a novel example. The later2014 finite-degree question is expressly separate and is not solved here.

## 1. The two families

Let k be any algebraically closed field of characteristic p>0. Define

    X=Spec k[t],
    S=Spec k[t,x,y]/(y^p−x−t x^p),
    T=Spec k[t,z],

and let both structure morphisms be induced by k[t]. They are affine morphisms of varieties. We prove that every geometric fiber of each is an affine line, whereas no dominant étale U->X makes S_U and T_U isomorphic over U.

## 2. Total spaces and smoothness

The equation F=y^p−x−t x^p is irreducible in k[t,x,y]. Indeed, as a polynomial in t over the UFD k[x,y], it is primitive: gcd(x^p,y^p−x)=1, since x does not divide y^p−x. It has degree one over the fraction field k(x,y), hence is irreducible there. Gauss's lemma proves irreducibility in k[t,x,y]. The quotient is a domain, so S is integral. It has dimension2; T is the affine plane and X the affine line.

The relative derivative of F with respect to x is −1. The Jacobian criterion, or the standard smooth presentation with this invertible derivative, shows S->X is smooth of relative dimension1 everywhere. In particular it is flat. Both maps are surjective and dominant: S has the section t |-> (t,0,0), and T has the section z=0. Thus none of the construction depends on a singular, nonreduced or reducible total space or on a failure of dominance.

## 3. Explicit fiber isomorphisms

Let a be a closed point of X, identified with a∈k, and choose b∈k with b^p=a. On the fiber S_a set

    w=y−b x.

Then w^p=y^p−b^p x^p=x. Conversely

    x=w^p,        y=w+b w^p.

These are inverse k-algebra parametrizations, proving

    k[x,y]/(y^p−x−a x^p) ~= k[w].                               (1)

Thus S_a~=A¹_k~=T_a scheme-theoretically, with reduced smooth geometrically integral fibers. The same calculation holds at every geometric point, including a geometric generic point, after taking b in its algebraically closed residue field. Over the original F_p model, every closed point has a finite perfect residue field, so (1) also proves an isomorphism of the actual closed fibers over their residue fields.

One must not replace this with the stronger assertion that the generic fiber over k(t) itself is A¹; the next section proves exactly that this is false.

## 4. A leading-coefficient lemma

**Lemma.** Let L be a field of characteristic p and a∈L not in L^p. Then

    C_a=Spec L[x,y]/(y^p−x−a x^p)

is not isomorphic to A¹_L. In fact there is no nonconstant L-morphism A¹_L->C_a.

**Proof.** Such a morphism gives f(s),g(s)∈L[s] satisfying

    g(s)^p=f(s)+a f(s)^p.                                     (2)

If f is constant, (2) makes g constant as well, so the morphism is constant. Otherwise put n=deg f>0 and let c be its leading coefficient. Since pn>n and a≠0, the right side has degree pn and leading coefficient a c^p. It follows that deg g=n. If d is the leading coefficient of g, equality of leading terms gives d^p=a c^p, hence a=(d/c)^p, a contradiction. An isomorphism to A¹ would give a nonconstant morphism of this kind. □

This direct proof works for every prime p, including p=2, and concerns isomorphism of schemes, not only isomorphism of group structures.

## 5. No dominant étale base change

Assume U->X is a dominant étale morphism of k-varieties with S_U~=T_U over U. Choose an irreducible component of U which dominates X and then its generic point. Because U->X is étale and locally of finite type, its relative dimension is zero; this component's function field L is a **finite separable** extension of K=k(t). Pullback of the supposed isomorphism to Spec L gives

    Spec L[x,y]/(y^p−x−t x^p) ~= A¹_L.                         (3)

But t is not in L^p. To see this, t is not a p-th power in K because its valuation at t=0 is1, while the valuation of any p-th power is divisible by p. If c∈L satisfied c^p=t, then K(c)/K would be a nontrivial purely inseparable extension inside the separable extension L/K, which is impossible. Therefore the lemma with a=t contradicts (3).

If one permits a non-quasi-compact étale scheme rather than a variety, dominance over this noetherian base still supplies an affine étale neighborhood of a point above the generic point; its residue field is finite separable, so the same contradiction applies. The variety formulation already suffices for the source question.

## 6. Why finite-degree base change is different

Take U=Spec k[b] with t=b^p. This is dominant finite flat of degree p and purely inseparable, not étale. On S_U the substitution

    w=y−b x,       x=w^p,       y=w+b w^p

defines an isomorphism S_U~=Spec k[b,w]=T_U over U. Hence the example is entirely compatible with the2014 published Generic Equivalence Theorem's finite-degree conclusion. It exhibits why replacing “finite degree” with “étale” in positive characteristic is a material change.

It also refutes the printed2007 proposition in positive characteristic even when k has infinite transcendence degree; the obstruction is separability, not countability. It does not provide a counterexample over Q-bar, nor to the all-fields finite-degree extension left open in2014 Remark2.2. Those are different residual questions.

## 7. Credit and disposition

The generic curve is exactly the standard form y^p=x+a x^p, a not in L^p, displayed in Russell, *Forms of the affine line and its additive group* (1970), p.527; Lemma1.1 there describes its purely inseparable splitting mechanism. The family and elementary leading-coefficient proof here package that classical obstruction for the literal2007 statement. The published2014 wording already avoids claiming étaleness in positive characteristic.

This is **one substantive author turn**, completed after the source/prior gate. Proposed result is a credited negative resolution of the literal2007 étale formulation, with the corrected later question left unresolved. It is not an exhausted five-turn attempt, and no result about the corrected later target is being claimed. Independent source/proof review determines final public disposition before any QUEUE or PR change.

## 8. Exact finite controls

The verifier checks the equation and inverse fiber/base-change substitutions over small prime and extension fields, the invertible relative derivative, and the degree/leading-coefficient implication in polynomial models. These supplement the symbolic proof; they do not constitute a search over all étale extensions or a novelty certificate.
