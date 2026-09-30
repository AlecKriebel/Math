# KP-4.43: the printed absolute-value bound has a known counterexample

Status: source-corrected known negative answer to the **literal absolute-value question**; independent source/proof review pending. No new counterexample discovery is claimed. The different one-sided question is not resolved here.

## Primary-source match

The original [K3, printed p.224, Problem 4.43](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf) was visually inspected. It says “null-homotopic” and prints

2g(Σ) ≥ |s(K)|

for a surface in a punctured negative-definite smooth four-manifold. Those absolute-value bars are present in the primary source, not introduced by the dataset. Its first remark attributes the standard negative-definite connected-sum case to MMSW.

The cited [Manolescu–Marengon–Sarkar–Willis manuscript](https://web.stanford.edu/~cm5/S1S2sInvt.pdf), published as *Duke Mathematical Journal* 172 (2023), 231–311, DOI 10.1215/00127094-2022-0039, gives a different, **one-sided** bound in Corollary 1.9. Example 6.4 supplies a null-homologous smooth disk for the left-handed trefoil in punctured negative CP². The text after Corollary 6.11 explicitly records s(T₂,−₃)=−2. Definition 6.2 specifies relative null-homology. These pages were visually checked to preserve the overbar on CP². The construction comes from a negative crossing change of an unknot and is already credited to those authors' example.

## Verification of every hypothesis

Take X = CP² with reversed orientation and W = X minus an open smooth four-ball. Its intersection matrix is [−1], so X is closed, smooth, and negative definite. W is simply connected and ∂W is a three-sphere. Use the boundary knot and orientation convention of the cited example; reversing a chosen identification of the boundary changes the sign of s but does not change |s|.

Let Δ be the properly smoothly embedded disk in MMSW Example 6.4. By the cited definition, [Δ]=0 in H₂(W,∂W;Z). The following elementary argument verifies the stronger relative homotopy condition, rather than replacing the printed word by “null-homologous.”

**Lemma.** If W is simply connected and ∂W=S³, any relative null-homologous map f:(D²,S¹)→(W,S³) has zero class in π₂(W,S³).

**Proof.** The homotopy long exact sequence and π₂(S³)=π₁(S³)=0 give an isomorphism π₂(W)→π₂(W,S³). The homology sequence and H₂(S³)=H₁(S³)=0 give H₂(W;Z)→H₂(W,S³;Z) as an isomorphism. Since W is simply connected, the degree-two Hurewicz map π₂(W)→H₂(W;Z) is an isomorphism. Naturality identifies the relative Hurewicz map with this composite of isomorphisms. Consequently a zero relative homology class has zero relative homotopy class. ∎

There is also a fixed-boundary formulation. Choose a continuous filling f₀:D²→S³ of the boundary knot, possible since π₁(S³)=0. Glue Δ to the oppositely oriented f₀. The resulting sphere in W has zero homology, hence zero π₂-class by Hurewicz. Therefore Δ and f₀ are homotopic as maps rel their parametrized common boundary. This homotopy is not claimed to be through embeddings, and f₀ need not be an embedded disk. Such an embedding assertion would be much stronger than nullhomotopy and is not the source's stated condition. Under ordinary absolute nullhomotopy of the disk map, the condition is weaker still because the disk is contractible.

Thus the example satisfies both the literal ordinary-map reading and the meaningful relative-to-boundary reading of nullhomotopy. It does not merely exploit the contractibility of the disk while ignoring its relative class.

Finally g(Δ)=0 and |s(T₂,−₃)|=2. Hence 2g(Δ)=0<2=|s(T₂,−₃)|, contradicting the printed inequality.

## What this does and does not settle

This is a known example refuting the displayed two-sided assertion, not a discovery of an exotic four-manifold or a resolution of the smooth Poincaré conjecture. In the MMSW convention, the valid one-sided bound is s(K)≤2g(Σ); the same example obeys −2≤0. Reflecting the knot while holding the negative-definite ambient manifold fixed is not justified. Reflecting the entire pair reverses the ambient intersection form, so it cannot supply the opposite inequality in the same class.

MMSW Question 9.7 asks a broader one-sided adjunction question. This audit neither proves nor disproves it. If a repaired Kirby question was intended, it must be stated explicitly and tracked separately; the absolute value cannot be silently removed.

No new substantive construction search was required: this is a primary-source correction plus a standard homotopy-to-homology check. Proposed classification: `already_solved`, known negative answer to literal formulation, 0/5 new proof attempts, subject to independent review. Completion estimate: 100% of the literal source audit; 0% toward any new resolution of the repaired one-sided problem.

Runtime metadata: inherited runtime; exact model identifier not exposed to this worker; no model or reasoning switch made. No novelty or human-peer-review claim.
