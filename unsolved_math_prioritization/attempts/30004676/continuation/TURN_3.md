# Recovered author turn 3: HYP relativization and the finite-cover barrier

## Goal and source boundary

The attempted route was to generalize the HYP construction underlying the
classical failure of atomic interpretability to preserve full admissible
computability. The [Avdeev–Puzarenko author-posted 2017 announcement](https://www.researchgate.net/publication/321476274_A_Computable_Structure_with_Nonstandard_Computability)
states the existence of a computably presented admissible structure not strongly
reducible to HF(empty), using a recursively saturated model and a finite-priority
presentation construction. This is prior work, not a new example here. The
long 2019 proof was not retrieved in this turn; ordinary-oracle relativization
is not asserted to imply arbitrary-admissible relativization.

The attempted extension would require a well-founded admissible B with an
A-Delta atomic presentation, while ensuring that **no** strong presentation
reduces B to A. A defect of one chosen surjection would not suffice.

## 1. Internal boundedness cannot be forced by strong reducibility

There is a decisive obstruction to strengthening the recovered cover lemma into
a characterization of strong reducibility.

**Proposition.** There are admissible A and B with B strongly Sigma-reducible
to A, for which no surjection nu: |A| -> |B| has exact internal A-set covers of
every B-membership fiber. This failure holds for every presentation map, not
just for one inconvenient map.

**Proof.** Choose an admissible B containing the ordinary infinite set omega
as an element; a countable example is the least admissible constructible level
strictly above omega. Use the graph-representation theorem recalled in the
[original problem's source](https://ems.press/content/serial-article-files/46899)
to choose a graph M_B with

    B ==_Sigma HF(M_B).

Put A = HF(M_B). Every internal A-set is externally finite: its elements are
hereditarily finite sets over the urelements M_B. The graph M_B may be infinite;
this does not make its entire urelement domain an element of HF(M_B).
Nevertheless B <=_Sigma A by the credited representation theorem.

For any surjection nu: |A| -> |B| choose y with nu(y) = omega. If c is an
internal A-set, el_A(c) is finite, and hence its image under nu is finite.
It cannot equal el_B(omega), which is infinite. Thus the exact-cover condition
fails for this y for every nu. QED.

This uses a published representation theorem as a premise; it is a simple
consequence, not a new construction of that graph. It establishes neither that
C(A) holds nor that A is not a jump fixed point. It is therefore not a
counterexample to the original conjecture.

It also explains why ordinal height alone cannot be used as a strong-degree
obstruction: B can have ordinal height above omega while the strongly
equivalent HF(M_B) has only finite pure ordinals. Information can be carried
by the urelement structure instead of by internal ordinal height.

## 2. A countable-witness limitation

A second obstacle affects a naive use of ordinary noncomputable theories to
produce witnesses over very rich admissibles.

**Proposition.** In ordinary set theory with choice, let A = H_(omega_1), the
set of hereditarily countable sets. Every countable admissible B in a finite
relational language is strongly Sigma-reducible to A.

**Proof.** Choose an external listing (b_n) of B, with repetitions if needed.
Encode its complete first-order elementary diagram, including constants for
the b_n, by a real T_B subset omega. Both omega and T_B are elements of A.
Define an external surjection nu from A onto B by nu(n)=b_n for finite
ordinals n, and nu(a)=b_0 for all other a. Membership in omega is bounded
definable using the parameter omega, so the corresponding index map is
definable in A. For every fixed Sigma(B) formula and parameter tuple, its
pullback is decided by membership of the appropriately coded sentence in T_B.
Primitive-recursive finite syntax coding is Delta over A. The pullback and its
complement are therefore Sigma over A. The same nu serves all formulas;
T_B is one fixed parameter for this B. Thus nu witnesses the strong reduction.
H_(omega_1) is admissible in the usual ambient ZFC setting. QED.

This observation does not decide C(H_(omega_1)), which quantifies over all
admissible targets with suitable interpretations, including uncountable ones.
Nor does it decide whether H_(omega_1) absorbs its structural jump. It shows
that countable classical witnesses and their real-coded theories cannot alone
refute the global property at this A: their complete diagrams are already
available as parameters. A generalized counterexample construction must retain
the correct domain and parameter scope.

## 3. Why the attempted priority relativization remains incomplete

The classical announcement uses a low real, limit approximation, enumeration
of finite data, and a finite-priority construction. Replacing that real by an
arbitrary admissible structure is not a syntactic oracle substitution. An
external enumeration of a countable A is not automatically A-definable;
uncountable A cannot be enumerated by natural-number stages at all. A
generalized construction must explain its admissible stages, selection of
witnesses, stabilization and Delta atomic presentation. These have not been
provided.

The representation consequence in Section 1 rules out recovering that missing
construction by merely forcing exact covers in a strongly equivalent HF
presentation. Such covers can be impossible even when the strong reduction
already exists. The replacement must encode truth through the urelement
structure or another mechanism, rather than through finite preimage covers.

## Outcome

The two propositions give genuine restrictions on this route: exact internal
covers are not necessary for strong reducibility, and rich admissibles absorb
every countable target using a truth-diagram parameter. The attempted general
HYP/priority relativization is still missing its definable presentation theorem.
No full converse proof or counterexample has been obtained. This is recovered
author turn 3; independent checking of these deductions remains pending, and
the five-turn continuation stays active.
