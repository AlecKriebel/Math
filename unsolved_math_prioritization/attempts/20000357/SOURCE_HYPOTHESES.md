# Named source hypotheses and applications

The named inputs were checked against the retained primary sources whose hashes and inspection locations appear in SOURCE_PINS.json. The checks below concern the precise applications in PROOF.md; they do not reprove the underlying established theorems.

## Clark index existence

[Clark, Corollary 4](https://plclark.github.io/PeteLClark/Research/crelle.pdf), physical page 2, applies to every number field and every positive index. Its genus-one curves give the smooth projective geometrically integral curve required in the upper-bound example. The argument uses an actual divisor of degree equal to the index, and then Riemann–Roch, rather than assuming every rational Picard class descends to a divisor. The construction requires \(n\ge2\); the identity treats \(n=1\). No prescribed-Jacobian or Galois-cover conclusion is attributed to Clark.

## Hilbert irreducibility

[Viray–Vogt, Proposition 3.3.1](https://msp.org/ent/2026/5-1/ent-v5-n1-p01-s.pdf) applies to a nice curve over a number field and a degree-\(d\) morphism to \(\mathbb P^1\). Nice means smooth, projective and geometrically integral. Both the sharpness maps and the composed map in Theorem 2 have these hypotheses. The conclusion supplies a Zariski dense set of rational base points with a single closed degree-\(d\) fiber. The proof does not apply that conclusion to an arbitrary elliptic or abelian target.

## Pencils and closed fibers

[Viray–Vogt, Lemma 4.1.1](https://msp.org/ent/2026/5-1/ent-v5-n1-p01-s.pdf) starts with an actual closed point on a nice curve over a number field. It supplies the pencil interpretation used after the multiplication theorem has produced such a point. Lemma 4.1.4 equates degrees of maps to \(\mathbb P^1\) with degrees of \(\mathbb P^1\)-parameterized closed points. It is not an assertion that every rational effective class is irreducible.

## Dilated abelian parameterization

[Viray–Vogt, Definition 4.3.1 and Proposition 5.2.1](https://msp.org/ent/2026/5-1/ent-v5-n1-p01-s.pdf) require a nice curve over a number field, an AV-parameterized closed point, a positive-rank abelian subvariety, and an integer multiplier at least two. Theorem 2 applies this result on the target curve \(D\), with multiplier \(r\ge2\), obtaining a closed point in the class \(r[x]\). A pencil representing that class is then composed with \(f\). A second Hilbert step on \(C\) produces the actual degree-\(rne\) closed point. Norm after pullback keeps the pulled-back abelian subvariety positive-rank. Multiplication on the variety is surjective; surjectivity on rational points is not assumed.

The undilated translate in degree \(ne\) has no guaranteed closed-point representative in this argument. That inclusion and the full classification of density-degree sets remain unresolved here.
