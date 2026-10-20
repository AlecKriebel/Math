# Attempt 4: can nonnegative even powers repair the signed transfer method?

## The apparent route

For arbitrary words, let M have entry a on the ordered pairs NW and ES, and entry 1 otherwise. Although M has negative entries when a<0, its square is entrywise nonnegative throughout a>=−1. In the state order E,N,W,S,

    M² = [3+a, 3+a, 2+2a, 2+2a;
          3+a, 3+a, 2+2a, 2+2a;
          4,   4,   3+a,  3+a;
          4,   4,   3+a,  3+a].

This suggests blocking two transitions and applying Perron–Frobenius theory. The essential question is whether the positivity survives when block displacement is retained, as it must be for endpoint extraction and quadrant confinement.

It does not. The obstruction holds for every positive block length, not just two.

## A no-go lemma for displacement-preserving fixed-length blocking

Fix an incoming direction N before a block of L>=1 further steps. Let F_L(z) be the signed sum over all such blocks having displacement z, counting the corner between the incoming N and the first block step and all subsequent internal corners. The terminal direction is not constrained.

**Lemma.** For every L>=1,

    F_L(−1,L−1) = L a.

**Proof.** The target displacement has Manhattan length L. A block of L steps with that displacement therefore consists of exactly one W and L−1 N, and no E or S. There are exactly L possible positions for W. In each word, W is preceded by N, either inside the block or as the specified incoming state. Consequently there is exactly one NW corner and no ES corner. Each word has weight a, proving the formula.

In particular, the coefficient is strictly negative for every a<0. If the terminal direction is additionally fixed as W, there is only the word N^(L−1)W and the coefficient is a.

Therefore no exact fixed-length block transfer with nonnegative transitions can simultaneously retain block displacement and the incoming direction for this model at any negative a. Refining such a model by extra nonnegative hidden states cannot help if summing those states is required to recover this exact coefficient: a sum of nonnegative weights cannot equal L a<0.

This excludes that precise strategy, not every conceivable loop-specific sign-reversing transformation. One could change the object class or allow cancellations outside a block; neither is a nonnegative local extension of Attempt 1.

## What the unrefined square forgets

For example, the two-transition matrix entry from incoming N to terminal W is 2+2a. Before erasing displacement, its Laurent polynomial is

    1 + a x^(−1)y + a x^(−2) + x^(−1)y^(−1).

The four summands correspond to intermediate E,N,W,S respectively. For a<0 it has two negative coefficients. Nonnegativity only appears after setting x=y=1, which sums different spatial displacements that must not be combined in a loop argument.

## Forgetting the incoming state also fails for long blocks

Let W_m(a;z) be the signed sum of all linear words of length m with endpoint z, with no initial seam. For k>=1,

    W_{k+1}(a;(−1,k)) = 1 + k a.

Indeed the only shortest words are the k+1 shuffles of one W and k N. The word beginning W has no counted corner; each of the other k words has exactly one NW corner. For any fixed a<0, taking k>−1/a makes this coefficient negative. Thus even the unrestricted endpoint-refined word model cannot be replaced wholesale by a nonnegative weighted model preserving every length and endpoint.

The example is not itself a quadrant path from the origin, but translating it sufficiently far to the right places every word within the quadrant. It is therefore relevant to the centered-box/interior blocks used in a quadrant proof, while not by itself disproving positivity of the closed quadrant coefficients.

## Exact endpoint-cancellation diagnostic at a=−1

The full arbitrary-endpoint word series is

    1 / (1 − 4t − 2(a−1)t²).

At a=−1 this becomes (1−2t)^(−2), whose coefficient of t^m is (m+1)2^m. Hence its exponential growth per step is 2. But the known unrestricted closed-loop coefficient has exponential growth 8 per half-length, or sqrt(8)>2 per step. There is no contradiction: the arbitrary-endpoint sum includes negative endpoint totals and cancellation between different endpoints.

In particular, squaring the arbitrary-word Perron growth rate cannot give the closed-loop rate on the lower conjectured branch. This is an exact structural obstruction rather than a lack of sufficiently long computations.

## Outcome

The M² positivity observation is correct but cannot support a displacement-preserving Markov-chain proof for a<0, at any fixed blocking length. The full conjecture is neither proved nor disproved by this attempt. The remaining promising signed route must control cancellation globally, for example by the exact operator pencil of Attempt 2, rather than replace it with an unjustified nonnegative block chain.

## Public reference

Michael Albert and Mireille Bousquet-Mélou, *Permutations sortable by two stacks in parallel and quarter plane walks*, Proposition 18 for the arbitrary-word series and Proposition 21 for the unrestricted-loop radius. https://arxiv.org/abs/1312.4487.
