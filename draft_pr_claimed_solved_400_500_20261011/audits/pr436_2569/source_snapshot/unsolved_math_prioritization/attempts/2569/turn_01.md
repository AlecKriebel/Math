# Attempt 1: test the passage from a Grothendieck equality to a lattice lift

Target: KOU-21.60 / 2569. This is the first mathematical attempt, after the statement and prior-work gate. It does not count source retrieval as a research turn.

Put O=Z_(p), k=F_p. The proposed converse starts with a rational representation V and an O G-lattice L in V such that [L/pL]=[P] in G_0(kG), where P is a projective indecomposable. The tempting next step is to identify L/pL with P. This is false, even in the smallest modular examples.

For G=C_p, the regular kG-module P=kG is its only projective indecomposable. With S the trivial simple module,

    [P]=p[S]=[S^{direct sum p}].

The right-hand module is the reduction of the rational module Q^{direct sum p} with trivial action, but it is not projective: its generator acts as the identity, whereas on kG the operator g-1 is a single nilpotent Jordan block of length p. A free kC_p-module has dimension divisible by p, but divisibility alone plainly does not make the trivial p-dimensional module free. Thus a witness in the positive monoid is not itself a lifting of P. The example does not refute the conjecture, since O C_p is local and the rational regular representation supplies a different lift.

The same example prevents applying coinvariants to a Grothendieck-group equality. Coinvariants by C_p send kC_p to a one-dimensional vector space and S^{direct sum p} to a p-dimensional vector space. The coinvariant functor is right exact, not exact, and so it does not define the claimed homomorphism on ordinary G_0. An argument that takes tops or coinvariants after the monoid equality needs an additional justification. In particular, these notes do not use that maneuver from the proof of Proposition 3.2 in Johnston–Rumynin as a black box; this observation is a warning about that step, not a counterexample to the stated proposition.

What information survives? On p-regular elements the Brauer character of P equals the restriction of a rational ordinary character, so it is rational-valued. Its unique p-adic projective lift has ordinary character Psi_P equal to this Brauer character on p-regular elements and zero on p-singular elements. Consequently Psi_P is rational-valued on all of G. That is a genuine necessary conclusion and suggests replacing the faulty direct-lattice step by rational descent of the projective lift.

Outcome: the most immediate proof fails for an explicit reason; the monoid condition does force rationality of every projective ordinary character. Next attempt: identify the additional obstruction to realizing that rational-valued character over Q.
