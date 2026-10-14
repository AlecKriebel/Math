# Scope clarification: model transport and mixed automorphisms

14 October 2026 UTC. Row 1777 / 30005572. This is an independent-review clarification within shared PASS4/5, not an additional mathematical pass. The frozen PASS3 proofs have not been edited.

## Precise reading of the accepted model-transport statement

The phrase “O-linear model isomorphisms ... transport eta exactly” in the accepted PASS3 scalar-five proof, section 6.1, is accepted for product-coordinate elliptic-model isomorphisms of the kind in LSSW Lemma 3.4.3, with the indicated shear transported as well. More generally it is true when the target primitive is explicitly defined to be the transported primitive. It is not a statement that an arbitrary mixed GL2(O)-isomorphism preserves an independently selected axis primitive.

For the unshifted primitive

eta_c = theta_(c,E1) exterior E2[c] + Nc [0] exterior theta_(c,E2),

an arbitrary mixed automorphism changes the coordinate supports. Indeed, the residue gamma eta_c - eta_c is exactly what defines the geometric cocycle. Declaring the primitive invariant under all such maps would erase that definition.

## What holds for a general O-linear isomorphism

Let g:A -> A' be an O-linear isomorphism between the relevant surfaces, with the group actions identified by conjugation. For c prime to 5, both the pullback of a normalized target primitive and a separately selected normalized source primitive are eventual-trace-fixed and literally T5-fixed, with the same zero-cycle boundary. Their difference is a closed C1-chain.

The accepted quotient exactness and scalar-five splitting provide the unique eventual-and-T5-fixed K2 lift b of that difference. The corresponding cocycles then differ by the coboundary delta b. Thus the construction transports canonically at the level of cohomology classes even when independently chosen primitives do not transport literally.

A general change of projective-module decomposition, such as a Steinitz identification, must use this class-level statement. It must also identify the actual induced CM endomorphisms and group conjugations; being merely an abstract isomorphism of coefficient groups is insufficient.

## Specialization requires the regular version

If both primitives are supported away from the required marked torsion orbit, their closed difference has no residues at that orbit. The K2 lift b is then regular there by the same local Gersten argument used for the original normalized cocycles. Its specialization gives a genuine coboundary in the target group. One cannot specialize an arbitrary comparison lift without checking this regularity.

This clarification does not grant arithmetic ray-field descent, full component assembly, all small levels, or a relative symbol formula. Those conclusions require their separately stated proofs. The original construction remains UNSOLVED.

## Frozen dependency and source

- PASS3 scalar-five proof: SHA-256 `0fd5b52591d193b1949afbe17b022414610101b7fbb8fca2eb3ee65f215f66ca`.
- PASS3 scalar-five acceptance: SHA-256 `0ed919b9ae134cf452569f861e5df0a0268b2cff139fc99b90da6384b257df20`.
- LSSW, *Eisenstein cocycles for imaginary quadratic fields*, Lemma 3.4.3, author manuscript p.26: https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf . The lemma uses a pair of elliptic-curve isomorphisms and the same transported shear.
