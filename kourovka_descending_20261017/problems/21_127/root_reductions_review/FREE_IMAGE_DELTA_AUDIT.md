# Fresh delta audit: a nontrivial P4 word killed by every free-group image

Reviewed 2026-10-24T20:59:02.006155+00:00. Assigned delta-audit completion estimate:100%. Full problem21.127 remains unresolved.

**Verdict: PASS. No substantive correction required.** The word is a valid exact obstruction to recovering arbitrary RAAG scl as the supremum of its values under homomorphisms to free groups. It is not an irrational value or a full rationality theorem. No novelty or residual-free classification is certified.

## Frozen claim

G=<a,b,c,d | [a,b]=[b,c]=[c,d]=1>, with [x,y]=xyx^(−1)y^(−1), and u=[[a,c],[b,d]]. The authored claim is u≠1, scl_G(u)=1/2, and f(u)=1 for every homomorphism from G to any free group.

I reviewed `FREE_IMAGE_BLIND_WORD.md`, `verify_free_image_blind.py`, and `free_image_blind_certificate.json`. Their SHA256 values are frozen in `blind_word_reproduction.json`; source-theorem scopes remain those independently checked in this directory's main AUDIT.md.

## All free targets, including rank zero, one, and infinite rank

Write A,B,C,D for the images. If B=1, then [B,D]=1 and the outer commutator is1. If C=1, then [A,C]=1 with the same consequence. These two cases are essential; one must not apply a cyclic-centralizer theorem to the identity.

In the remaining case, B and C are nonidentity and commute. Their free-group centralizers are the same maximal cyclic group. A short justification of the input is available from the free action on the Cayley tree: a nonidentity element has a translation axis, every element of its centralizer preserves that axis and its orientation, and translation distance gives an injection of the centralizer into Z (the kernel fixes a vertex, hence is trivial). Thus the centralizer is cyclic. A nonidentity element of that cyclic centralizer has the same axis and maximal cyclic centralizer. Since A commutes with B and D commutes with C, both A and D lie in this same cyclic group. Then [A,C]=[B,D]=1, so f(u)=1.

A rank-one free group is cyclic and all images already commute; rank zero is trivial. In infinite rank, the four images are finite words and therefore all lie in a finite-basis free subgroup. Applying the same argument there proves the identity in the whole target. There is no hidden finite-rank restriction or need for f to be surjective. Composing a homomorphism with any further homomorphism cannot resurrect u once its image is1.

## Matrix certificate and signs

The proposed elementary transvections are a=I+E23, b=I+E45, c=I+E12, d=I+E34. In the required pairs (a,b), (b,c), (c,d), the strictly upper-triangular elementary parts multiply to zero in both orders. Hence all three defining relators are satisfied and the assignment defines a homomorphism from the actual presented RAAG.

For a and c, the reverse elementary product E12E23=E13 while E23E12=0, giving [a,c]=I−E13. Similarly [b,d]=I−E35. In the outer commutator, (−E13)(−E35)=E15, the reverse product is0, and all higher terms vanish. Thus u maps to I+E15, which is different from I over Z. The sign is positive with the explicitly stated commutator convention.

The new `independent_blind_word.py` expands the 16-letter word `acACbdBDcaCAdbDB` and evaluates it by signed elementary-transvection **column updates**. It does not import or duplicate the author's general matrix multiplication/inversion code. It reproduces every generator matrix, every relator, both inner commutators, and the outer image exactly. It additionally checks several positive powers produce I+N E15. The exact nontriviality of u follows already from N=1. Output: `blind_word_reproduction.json`.

No faithful representation is required: a homomorphic image of u different from1 suffices. The nilpotent matrix target is used solely for nontriviality; no scl lower bound is inferred from that amenable image.

## Exact scl conclusion and route obstruction

The word is in the commutator subgroup and is a single commutator of two arbitrary group elements. The independently reviewed punctured-torus-cover construction gives scl≤1/2. The matrix image proves nonidentity, so the actual Heuer RAAG-gap theorem applies and gives scl≥1/2. Hence scl=1/2 exactly.

Every free-group image is the identity and has scl0. There are homomorphisms to free groups, including the trivial homomorphism, so the supremum is over a nonempty family and equals0. Thus the proposed universal equality with the free-image supremum is false by the strict inequality0<1/2.

This argument does not preclude RAAG-specific quasimorphisms, exact surface constructions, induced-subgraph retract calculations, or methods using different target groups. It establishes no statement about arbitrary homomorphisms defined only on finite-index subgroups. It does not claim irrationality, universal half-integrality, or a complete solution of21.127.

## Input receipt

- FREE_IMAGE_BLIND_WORD.md: `fb3c807584a68af7199cd12e2264b744ef0b9c8162e62f4432fe6ccd0948d89c`
- verify_free_image_blind.py: `73e47d39b68489e18c321b08db3531c6ae1cb68f4eb0bd7c24e959611f1d3b29`
- free_image_blind_certificate.json: `4e3a1c6690fc52e3785d06b7a5e9a96a4f6c8b58f414453a25fecf57116d5810`

These are the exact files inspected and independently reproduced. No Git operation, external communication, publication, or tracker write was performed.
