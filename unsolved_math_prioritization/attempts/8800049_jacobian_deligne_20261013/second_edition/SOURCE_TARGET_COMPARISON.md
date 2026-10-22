# Exact source coverage and the second-pass strengthening

## Conclusion

The standalone theorem supplies the literal no-complexity-bound connection asked for on Howe's 2006 IPAM slides, PDF pages 37–38. It combines the polarized Deligne description with the geometric Beauville–Ritzenthaler recognition method to decide whether a promised ordinary absolutely simple threefold isogeny class contains a genus-three Jacobian over its original finite field. The strengthened connection realizes each specified polarized ideal and computes its own descent character. No source-imposed mathematical requirement has been identified as unmet. [Howe 2006](https://ewhowe.com/talks/IPAM.pdf)

This conclusion concerns exact theoretical computability. Useful efficiency, implementation, historical intent, and worldwide novelty are separate questions. The mathematical statement does not establish them, and they should not be added retroactively as requirements of the displayed source problem.

## Source requirements mapped to the proof

1. The source supplies a Weil polynomial for an ordinary absolutely simple abelian-threefold class. The integrated proof takes exactly that realizability promise and degree; making the finite field explicit is a computable representation choice, not an additional mathematical restriction. No maximal-order, invertible-ideal, odd-characteristic, or bounded-class-number hypothesis is added.
2. The source asks for an actual connection to Deligne modules. M2 completely enumerates ideal classes and polarization orbits. D1–D6 produce a model whose integral Frobenius and polarization matrices are certified against the specific input pair. Its meaning does not rest on arbitrary assignment of labels to an unlabeled list. The aggregate count-certified alternative M3–M6 remains independently valid.
3. The recognition method needs algebraic input. M3 and D2 supply complete theta-equipped projective equations, group laws, effective Cartier and line-bundle data. The verified Frobenius fingerprint is M4. A numerical period matrix or a missing realization oracle is not substituted for this contract.
4. The source permits either of the proposed recognition approaches. G1–G5 use the geometric Beauville–Ritzenthaler method. There is no requirement to implement the modular-form method as well. All hypotheses of the cited geometric statements are obtained from the input or checked exactly. [Beauville–Ritzenthaler](https://arxiv.org/abs/1005.3683v1)
5. The source asks for a Jacobian over the original finite field. G6 proves that the chosen odd-degree extension preserves the quadratic Serre character. The returned sign is its value on the original q-Frobenius, which determines the entire character. The hyperelliptic branch has trivial obstruction.
6. The source asks for existence anywhere in the class. M2 and C2 cover every principal-polarization orbit on every relevant full ideal class. Rejecting all of them proves NO; accepting one proves YES. Rejection of only one selected polarization is insufficient.
7. No characteristic restriction is displayed. The marked construction, the bounded-point theorem, and the recognition method all include characteristics two and three, with their distinct torsion, constant-group, invariant-section, polarization, and Artin–Schreier safeguards written out.
8. The source asks for a decision. Every individual certificate check terminates; D6 proves eventual occurrence of a successful marked certificate, and C2 combines finitely many such searches. The theorem proves both YES and NO termination. It is not merely a positive search or a finite experiment.

## What the full comparison convention does

Deligne's functor depends on a comparison choice. D1 fixes an effective algebraic tower, compatible primes above p, compatible residue embeddings, and the complex inclusion on the algebraic unramified ring. A candidate cannot choose a different embedding to fit the desired ideal. The CM type is induced by this fixed convention, and the full integral matrix check supplies the global ideal-class marking. [Deligne 1969](https://publications.ias.edu/sites/default/files/Number6.pdf)

This is effective mathematical data defining the interpretation of the input pair. It is neither an uncomputed oracle nor an extra restriction on the class-level source input. A different full convention may be used consistently; enumerating all polarized classes gives the same existential answer. Merely fixing a CM type or matching a characteristic polynomial would not supply the same marked assertion.

The marked input need not be an invertible ideal, and its polarization orbit is part of the certified identification. The canonical-lift residue extension retains the original q-Frobenius endomorphism, not q to the extended-field degree. The later good-point extension has odd degree for a separate reason: preservation of the quadratic obstruction.

## Quantitative geometric improvement

For a geometrically indecomposable ppav threefold with smooth rational theta, Part III proves

B(Q) = 2Q² + 18Q^(3/2) + 2321Q + 24√Q + 2270

as an upper bound for its exceptional-set points. For Q≥81, more than one sixth of all rational points are good. The least positive odd degree n with q^n≥81 is 7 for q=2, 5 for q=3 or 4, 3 for 5≤q<81, and 1 for q≥81. Thus recognition uses a prescribed odd extension of degree at most seven.

The proof handles rational image points without rational preimages by bounding a collision-curve union. Its characteristic-two argument uses geometric two-torsion point counts and retains inseparable multiplicities. The geometric bound needs no ordinarity assumption, and its auxiliary genus-three curve is only a proof device; it is not an extra algorithmic input.

This bound improves one stage. It supplies no useful bound on the much larger model, lift, or topology certificate searches. The conditional expected count of fewer than six good-point tests assumes an independent uniform sampler; no efficient sampler is supplied by that observation.

## What is and is not claimed

The mathematical claim is exact termination, exact per-ideal marking, exact original-field descent, and complete class-level decision. The prior aggregate theorem already met the literal existential source question; the marked inverse strengthens the interface, and the numerical bound strengthens its geometric stage.

The following remain outside the proven deliverable:

- A useful total complexity or resource bound
- Effective practical height, degree, or numerical-precision estimates
- A direct short theta or modular-form formula from the ideal lattice
- An implemented nontrivial end-to-end marked-lift or theta-geometry example
- Optimality of the constant or extension bound
- A claim about the historical practical endpoint or worldwide priority

These are meaningful further directions, but the displayed source does not impose them as mathematical acceptance conditions. The independent source-coverage audit reaches the same distinction. Its queue recommendation is an audit recommendation, separate from the theorem itself.

Finite arithmetic tests and independent argument audits support their stated narrow conclusions. Source inspection was bounded; no absence-of-prior-work theorem is inferred. Existing classification, recognition, arithmetic, topology, and point-bound results remain credited to their authors.
