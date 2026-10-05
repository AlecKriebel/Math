# Controlling audit addendum: existence is not knowledge

This addendum accompanies, and does not alter, the frozen authored packet for ID 2890 / modern K3 Problem 4.14. The bound author-manifest SHA-256 is `579a41fb8e474f60df00a4ecfe5d40e221e885385d5b8ee12557a9d7d32bdc37`.

## Exact location and correction

In `PROOF.md`, Approach 4, the definition paragraph at line 120 contains this sentence:

> If such an n is not known to exist, regard the height as infinite.

Replace its mathematical meaning by the following controlling definition:

Let S(C,f) be the set of nonnegative integers n for which f extends to an orientation-preserving diffeomorphism of C#n(S²×S²), with connected sums taken in the interior. Define h(C,f)=min S(C,f) if this set is nonempty, and h(C,f)=∞ if this set is empty. If existence of an extension has not been established, its finiteness is unasserted; lack of knowledge is not a proof that the set is empty.

Similarly, define s(X,X′) as the minimum of the set of nonnegative n for which the stipulated oriented stabilized diffeomorphism exists, with value ∞ exactly for the empty set. The convention concerns mathematical existence, not an algorithm's ability to exhibit the diffeomorphism.

## Dependency check

No deduction in the frozen packet uses an unknown extension as evidence of nonexistence.

- Proposition 4.1 assumes h(C,f)≤n and explicitly chooses an extension F. Its proof uses only this witness and the inverse boundary map. If a witness is given at m<n, an orientation-preserving diffeomorphism can be isotoped to fix a small interior ball, and extended across each additional connected sum by the identity. Thus extension existence is upward closed, as the notation h≤n requires.
- Corollary 4.2 assumes a finite height, or a finite collection of finite heights. Its uniform-bound conclusion is conditional on that assumption.
- The later attempted contradiction requires an actual unbounded sequence of closed-pair distances. The author expressly does not supply that sequence.
- The cited stable-extension assertion is a credited external input, not a deduction from ignorance. The source-hypothesis audit is separate from the direct gluing proof.
- Neither this sentence nor its correction affects Approaches 1, 2, 3, or 5, the complement lemma, or the unresolved status.

The issue is a bounded definitional imprecision, not a counterexample to the conditional stabilization theorem. The audit's acceptance requires reading the packet together with this addendum. The original files remain byte-for-byte frozen.
