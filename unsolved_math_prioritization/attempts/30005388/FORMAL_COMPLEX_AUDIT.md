# Formal-complex tests for the torsion equality question

This supplements REPORT.md. Every constructed object here is a formal complex. None is asserted to be realized by a knot. The calculations are obstructions to incomplete proof routes and do not settle the knot question. No novelty is claimed.

## 2. Decategorification and a formal long-box obstruction

One possible strategy is to recover the mod-two Arf value from a graded Euler polynomial and prove that it is determined by the horizontal almost-local class. The following calculation shows why the horizontal axioms alone are insufficient.

For n≥1, over F_2[U,V] take generators a,b,c,d,x with differential

    ∂a=U^n b+V^n c,   ∂b=V^n d,   ∂c=U^n d,   ∂d=∂x=0.

Give them bidegrees (0,0), (2n−1,−1), (−1,2n−1), (2n−2,2n−2), (0,0), respectively; U and V have degrees (−2,0) and (0,−2), and ∂ has degree (−1,−1). The square is acyclic after either variable is inverted, leaving the free x tower. Define the semilinear map j_0 to exchange U,V and b,c and to fix a,d,x.

For n>1 the horizontal truncation C_n, obtained by setting V=0, together with hat(j_0), satisfies all horizontal almost-iota axioms: the formal U derivative vanishes after U=0, hat(j_0)^2=1, and its required companion derivative has the zero chain-map lift. Projection onto x and inclusion of x give almost-local maps both ways. Consequently [C_n,hat(j_0)]=O.

Nevertheless, using Alexander degree (gr_U−gr_V)/2 and the parity of gr_U, its graded Euler polynomial is

    Δ_n(t)=3−t^n−t^(−n).

For odd n>1 this has Δ_n(−1)=5, while the unknot polynomial gives 1. These are the two different Arf residue classes if the polynomials arise from knots. Thus polynomial residues cannot be attached to every formal horizontal almost-local equivalence class by this rule. The formal example has not been shown to be the involutive complex of any actual knot.

There is an explicit obstruction to confusing this example with a full involutive knot complex. Write Φ=∂/∂U and Ψ=∂/∂V for formal derivatives of the differential. For odd n,

    ΦΨ(a)=U^(n−1)V^(n−1)d.

The proposed j_0 has j_0^2=1, so it fails the full square relation j^2≃1+ΦΨ. The defect is not nullhomotopic: every matrix coefficient of ∂H+H∂ lies in the ideal (U^n,V^n), whereas U^(n−1)V^(n−1) does not. This is a proof for every n, not just a finite test.

A repair reveals the loss of torsion. Put q=U^(n−1)V^(n−1), and let j_(λ,μ) exchange b,c and U,V, fix d, and satisfy

    j_(λ,μ)(a)=a+λx,   j_(λ,μ)(x)=x+μq d,

where λ,μ∈F_2. This is a grading-correct semilinear chain map, and direct multiplication gives

    j_(λ,μ)^2=1+λμq(a↦d),
    ΦΨ=(n mod 2)q(a↦d).

The full square identity therefore holds precisely when λμ=n mod 2. For odd n it forces λ=μ=1 within this displayed family. When n>1 the horizontal hat involution fixes x but sends a to a+x. Inclusion of x is a local map O→C_n. A local map f:C_n→O would have f(x)=1, but intertwining on a requires

    f(a)+f(x)=f(j(a))=f(a),

an impossibility. Hence O<[C_n,hat(j_(1,1))] in the translation-invariant partial order. Repeated addition gives a strictly increasing sequence, so this repaired horizontal class has infinite order. For n=1 the same repair is the figure-eight model, of order two. For even n the unmodified j_0 satisfies the full square identity, and the displayed horizontal class is trivial with Δ_n(−1)=1.

The statements about local maps cover all grading-preserving polynomial maps for these models. A term U^k z in a map out of O would need gr_V(z)=0 and gr_U(z)=2k; a nonzero map z↦U^k in the other direction needs gr_V(z)=0 and gr_U(z)=−2k. The only eligible generators here are a,x, and, for n=1, d, all of degree (0,0). Thus all eligible coefficients are constants. Locality forces the x coefficient to be one.

This rules out the simplest odd long-box formal counterexample. It also identifies a missing input: a general constraint from full involutive realizability and finite smooth concordance order, controlling the Euler-parity contribution of arbitrary discarded summands. The calculation proves no such general constraint. The two-parameter ansatz is not a classification of every possible full involution.

## 3. Tensor descent from a finite-order relation

A different approach starts from the slice relation mK=0 and tries to descend its local equivalence to one copy of K. Even-order tensor powers lose exactly the two-torsion information at issue. This failure can be checked at the chain-map level.

Use the n=1, λ=μ=1 horizontal model above, denoted E. Its differential is ∂a=Ub and ∂c=Ud. The hat involution sends a↦a+x, b↦c, c↦b, d↦d, x↦x+d. The correct tensor involution is

    j_tensor=j⊗j+(Φj)⊗(jΦ).

Suppress tensor symbols between generators. Define g:O→E⊗E and f:E⊗E→O by

    g(1)=ad+bc+cb+da+xx,

and let f take value 1 on precisely ad,bc,cb,da,xx and value 0 on the other basis elements. Both maps preserve the grading. In ∂g, the terms Ubd and Udb each occur twice and cancel; the same cancellations give f∂=0. Direct substitution in the displayed involution gives j_tensor g=g and f j_tensor=f. Both maps are local since they carry the free xx tower to the free tower. Thus E⊗E is almost-locally equivalent to O, although E is not.

There can therefore be no general inference of a local map E→O from local maps E⊗E⇄O. In characteristic two, averaging over a twofold symmetry cannot supply the missing descent either: the norm of a fixed vector is zero.

The decategorified finite-order constraint has the same limitation. If m is even, the symmetric polynomial Δ_K(t)^m is already a polynomial times its reversed polynomial, up to a Laurent unit, irrespective of Arf(K). At t=−1 every odd square is 1 modulo 8. If m is odd, both characters vanish by REPORT.md, Section 1. Thus applying the slice polynomial constraint to a multiple cannot distinguish the remaining even-primary cases. A successful tensor strategy needs a new parity-sensitive input from the particular geometric slice equivalence, beyond the existence of the tensor equivalence.

## Exact checks and limitations

verify.py uses sparse polynomials over F_2[U,V] and exact linear equations. It checks the differential, gradings, skew chain-map property, derivative relations, full square condition, horizontal axioms, map obstructions and tensor-square maps. The parameter tests use 1≤n≤11 and all four (λ,μ) values; the all-n statements above have independent symbolic proofs. All guard conditions use explicit exceptions and remain active under Python optimization.

The computation does not implement a recognition algorithm for actual knot Floer complexes, decide smooth sliceness, or establish any unknown knot's concordance order. In particular its formal horizontal example is not a counterexample to the target.

## References

The local-equivalence definitions and tensor law are from Kang–Park, *Torsion in the knot concordance group and cabling*, Section 2: https://doi.org/10.4171/JEMS/1520 and https://arxiv.org/abs/2207.11870. The n=1 complex is their Example 2.9; its order two is known. The present matrix certificates only check that fact explicitly.
