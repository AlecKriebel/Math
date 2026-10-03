# 30000590: final five-turn research result

**Proposed disposition: unsolved, 5/5 substantive author turns. Independent review pending.**

The exact question is whether every virtually-FP group Gamma has total H*(Gamma;ZGamma) finitely generated as a **right ZGamma-module**. Here FP means a finite-length resolution of the trivial integral module by finitely generated projectives. It does not mean only FP-infinity, and the requested finite generation is not over Z. SOURCE_SCOPE.md pins the primary contribution, definitions, known positive classes and prior-attempt gate.

## What is proved

1. **Turn 1:** right-equivariant finite-index coinduction reduces the virtually-FP question exactly to the FP case. Right-coherent group rings give positive examples. For a finite projective cochain complex of positive length n, the next-to-top H^(n-1) is finitely generated exactly when the top H^n is FP_2. An explicit monomial-ring bad kernel is only an algebraic control.
2. **Turn 2:** ascending HNN extensions of positive FP groups remain positive. The relevant cohomology incidence map is 1 minus a strictly height-raising transport, so finite-support minimum height proves injectivity, even when the transport is not injective. Finite free products are positive. The Baumslag--Solitar calculation keeps the Fox coefficient and right ideal explicit.
3. **Turn 3:** for two positive FP groups, integral product finite generation is equivalent to finite generation of all the actual integral Tor terms. Torsion-free cohomology of one factor suffices. Over each fixed field, the product property is equivalent to the property in both factors. Integral PD factors only shift it. Fixed-modulus Bockstein identifies the exact torsion-kernel condition.
4. **Turn 4:** a good FP normal subgroup and an integral duality quotient imply a good FP extension. The dualizing module is explicitly assumed Z-flat. The full right action, inner-action prism, nonsplit lift cancellation, spectral collapse and diagonal generators are proved.
5. **Turn 5:** an explicit three-entry matrix over Z[F2 times F2] has non-finitely-generated kernel. The source is a three-generator height kernel H with H_2(H;Z) free of countably infinite rank. Faithful induction transports its non-FP_2 augmentation syzygy. The ambient FP group itself has positive regular cohomology, generated in degree two by four tensors. Therefore this matrix cannot be promoted into a counterexample about the group's own regular cochain resolution.

These are scoped structural results and failed-construction controls, using credited standard machinery and known positive examples. No priority claim is made.

## Exact unresolved gap

A finite group-ring matrix with a bad kernel, even over an actual good FP group ring, is not enough. One needs a group whose own finite projective augmentation resolution dualizes to a non-finitely-generated regular cohomology module, or a general proof that these augmentation-resolution constraints prevent that. Neither is supplied. Likewise no theorem removes the actual Tor, flatness or ascending-height hypotheses from the partial positive results.

The previously exhausted PD-over-all-fields versus PD-over-Z problem 2579 is distinct and has not been retried or counted here. No sixth proof-search turn is taken.

## Reproducibility and history

The five author checkers replay byte-for-byte and contain 747,103 exact finite assertions: 300,681; 46,264; 79,346; 83,797; 237,015. These check identities, signs, finite supports, normal forms and finite orbit controls. The infinite mathematical claims rest on the written proofs, not on finite testing.

Run `python verify_packet.py` from this directory to check every final public file, all historical manifests and every replay. Add `--source-dir PATH` to check the six locally downloaded primary PDFs; raw sources are deliberately not public artifacts. The final review must bind FINAL_AUTHOR_MANIFEST.json and inspect the complete five-turn argument.

All old manifests, proofs and historical states remain unchanged. FINAL_STATE.json gives the current state. SOURCE_LOCATOR_CORRECTION.md corrects the Sharifi page number additively; it changes no theorem or source hash.
