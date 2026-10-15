# Turn 5: unique roots do not make the derived subgroup root-closed

Completed 2026-10-02 UTC. Original unresolved, 5/5 substantive turns. Subjective completion toward the original question remains 18%. This final direction tests a different possible route: infer root-closure of H' from orderability, uniqueness of roots, absence of free subgroups and finite presentation. Explicit countermodels disprove that inference; the PL condition excluding them is identified exactly. Author search stops after this turn.

## 1. The credited one-bump germ argument

For a PL map f on [a,b] with no fixed point in (a,b), the initial-slope map is injective on its PL centralizer. This is the classical Brin–Squier method; see Kassabov–Matucci, *The simultaneous conjugacy problem in groups of piecewise linear functions*, arXiv:math/0607167v3, Corollary4.5 and Lemma4.6, pp9–10. https://arxiv.org/abs/math/0607167 . The stronger cyclic-centralizer theorem is not needed here.

For clarity, the short proof is included. A commuting k with initial slope1 is the identity near a. For any x in (a,b), iterating either f or f^{-1} moves x arbitrarily close to a: an interior limit would be a fixed point. Commutation then transports the identity of k back to x. Thus k is the identity everywhere. The quotient of two centralizing maps with the same positive initial slope has slope1, proving injectivity. The slope map is a homomorphism into the abelian positive reals, so this one-bump centralizer is abelian.

Every element under discussion has finitely many linear pieces on the closed interval. We do not use this argument for arbitrary homeomorphisms with no affine endpoint germ.

## 2. Unique roots and balanced powers in PL_+(I)

**Unique roots.** If f^n=g^n for n>=1 in PL_+(I), then f=g.

Write w=f^n=g^n. Both f and g commute with w and preserve each of its finitely many support components, since an increasing map cannot permute a finite ordered set of intervals nontrivially. On a component J, w is one-bump, so f|J and g|J belong to its one-bump centralizer. Their positive initial slopes have the same nth power, hence are equal. The injective germ map makes the restrictions equal. Outside supp(w), a point fixed by a positive power of an increasing map is fixed by that map, so both f and g are the identity there. This proves the assertion, including w=1.

**Balanced powers.** If f != 1 and s^{-1}f^p s=f^q for nonzero integers p,q, then p=q.

The supports of all nonzero powers of f are the same, so s preserves each support component J=(a,b) of f. At its left endpoint the initial slope lambda=f'(a+) differs from1: otherwise finite piecewise linearity would make f the identity on a nonempty initial subinterval of J. Taking slopes at the common fixed point a cancels the conjugator's slope and gives lambda^p=lambda^q. Since lambda>0 and lambda!=1, p=q.

These facts hold in every subgroup of PL_+(I). They concern equality or conjugacy of powers. The target asks instead whether a power lying in a product-of-commutators subgroup forces its root to lie in that subgroup. Neither result establishes this different condition.

## 3. Exact finitely presented countermodels to the abstract inference

For m>=2, let P_m have the finite presentation

    <x,y,z | [x,z]=[y,z]=1, [x,y]=z^m>,

where [x,y]=xyx^{-1}y^{-1}. It has the following concrete model on Z^3:

    (a,b,c)*(a',b',c')=(a+a', b+b', c+c'+m a b').

The identity is (0,0,0); the inverse of (a,b,c) is (-a,-b,-c+mab). Associativity follows by expanding the bilinear cross term. Set x=(1,0,0), y=(0,1,0), z=(0,0,1). These satisfy the displayed relations and generate every triple. Conversely, the presentation allows collection to x^a y^b z^k, whose model triple is (a,b,mab+k). Distinct collected normal forms have distinct triples. Thus the model realizes exactly the finite presentation, not merely a quotient.

Its commutator formula is

    [(a,b,c),(a',b',c')]=(0,0,m(ab'-a'b)).

Therefore P_m'=<z^m>, the center is <z>, and

    (P_m)_ab = Z^2 direct-sum Z/m.

In particular z has exact order m in the abelianization while z itself has infinite order. The group is nonabelian nilpotent of class2, hence has no nonabelian free subgroup (all subgroups of a class2 group are class at most2; a free group on two generators is not class2).

All of the following additional potential proxy hypotheses hold:

- **Torsion-free and unique roots:** for n>=1,

      (a,b,c)^n=(na,nb,nc+m n(n-1)ab/2).

  Equality of nth powers forces equality of a, then b, then c; a power equal to the identity forces all three zero.
- **Bi-orderable:** use the lexicographic sign of (a,b,c). The positive cone is closed under multiplication: first examine (a,b) in lexicographically ordered Z^2, and when both projections are zero the central c coordinates add. Conjugation fixes (a,b), and when these are zero it fixes c as well, so the cone is conjugation-invariant. Its disjoint trichotomy gives a bi-invariant total order.
- **Balanced powers:** if a nonidentity triple u has a nonzero (a,b), comparison of these coordinates in v^{-1}u^p v=u^q forces p=q. If u is central, comparison of c forces p=q instead. This works for arbitrary nonzero signed p,q.

Thus finite presentation, torsion-freeness, bi-orderability, unique roots, balanced powers, and absence of a nonabelian free subgroup, even all together, do not force torsion-free abelianization. This is a concrete failure of the proposed axiomatic route, not a counterexample to Question111.

## 4. Why the countermodels cannot embed in F

In fact every homomorphism P_m -> PL_+(I) kills z. Suppose its image h of z were nonidentity, and choose a component J of supp(h). The images of x and y commute with h, so preserve J and belong on J to its one-bump centralizer. Their restrictions commute by Section1. But their commutator equals h^m, which is nonidentity everywhere in J. This is a contradiction. Hence h=1, and then the images of x and y commute. All such images are abelian.

This gives a direct dynamical obstruction to embedding this entire finitely presented torsion family. It is consistent with the solvable-image conclusion in Turn3 but is independently proved here using one-bump centralizers. Likewise Section2 immediately excludes a faithful PL representation of a Baumslag–Solitar relation s^{-1}a s=a^n with a!=1 and n>=2; those familiar affine candidates cannot be used as F subgroups either.

There is no analogous argument that every torsion witness of an arbitrary subgroup centralizes its generators. Röver's valid finitely generated F subgroup has a noncentral torsion witness. This missing centrality, together with the inability to deduce a finite ordinary generating set for its normal closure, remains a concrete barrier.

## 5. Verification and final disposition

verify_turn5.py checks the integer model, finite-presentation normal-form coordinates, commutators, positive powers, conjugation-invariance of the order cone, and the mod-p abelianization dimensions on bounded exact inputs. It separately reuses the rational PL implementation to check germ-power and conjugacy slope formulas. The infinite assertions follow from the formulas and proofs, not the finite controls.

The five-turn packet supplies several positive classes and rigorous obstructions to candidate mechanisms. It supplies neither a proof for every finitely presented subgroup of F nor a finitely presented embedded counterexample. Final original disposition: **unsolved, 5/5**, pending full independent review. No historical novelty is claimed for the classical germ facts, nilpotent examples, or deductions from the cited classification/splitting theorems.
