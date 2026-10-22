# Independent audit: obstruction to nonnegative local blocking

Date: 2026-10-20 UTC.

Audited `ATTEMPT_4.md`, SHA-256 `dcaa06d8e22d8ef4bdc4834313598cf0597a19b94435befb5d480c4797387678`.

## Verdict

**PASS for the stated local-blocking obstruction and endpoint-cancellation diagnostic.** The matrix square, both refined endpoint formulas, and arbitrary-word generating function are correct. The limitations are appropriately narrow: this does not disprove any quadrant-loop radius or unrefined positivity conjecture, and does not rule out global cancellation methods.

## Matrix square and displacement retention

Direct multiplication of the direction matrix in state order E,N,W,S gives exactly the displayed M^2. Its entries are nonnegative for a>=-1. This calculation sums over the intermediate direction and forgets the displacement of the two steps.

For incoming N and terminal W, the intermediate directions E,N,W,S give, respectively,

    1, a x^(-1)y, a x^(-2), x^(-1)y^(-1).

Their unrefined sum is 2+2a, but the four endpoints are different. The two negative coefficients for a<0 cannot be discarded when endpoints or intermediate confinement are retained. Both the stated Laurent polynomial and its interpretation are correct.

## Obstruction for every fixed block length

A length-L block ending at displacement (-1,L-1) has displacement Manhattan norm L. Consequently every step must point toward the target: there is exactly one W, L-1 N, and no E or S. The L possible positions of W give all such blocks.

With an incoming N, the W is always immediately preceded by N, either in the block or across the initial seam. There is exactly one counted NW and no ES. Thus the sum is L a, including L=1. With terminal direction fixed to W, only N^(L-1)W remains and its weight is a.

Therefore a model whose block weights, hidden-state weights, and summation recovering this coefficient are all nonnegative cannot represent the exact incoming-direction/displacement-refined block transfer at any a<0. The attempt explicitly retains the condition that hidden states are recovered by nonnegative summation; it does not incorrectly rule out a representation using signed decoding or cancellations outside the block.

## Omitting the initial seam

For length k+1 and endpoint (-1,k), the same shortest-path argument gives one W and k N. The word starting W has weight one; each of the k other words has weight a. The exact unseamed sum is 1+k a, which is negative when k>-1/a.

These words are not quadrant paths starting at the origin. Translating their common starting point to x=1 places them all in the quadrant, so they do obstruct a wholesale positive representation of centered/interior blocks. The attempt correctly avoids treating them as closed quadrant counterexamples.

As an independent finite check, I enumerated every word through block length seven at a=-1,-1/2,-1/7 using exact rational arithmetic and verified both L a and 1+(L-1)a at the specified endpoint. These tests are normalization checks, not substitutes for the shortest-path proof.

## Arbitrary-endpoint cancellation at a=-1

The arbitrary-word rational series is

    1/[1-4t-2(a-1)t^2].

It follows either from the marked-corner contraction or by specializing the horizontal/vertical and endpoint variables in Albert–Bousquet-Mélou Proposition 18. I checked that primary-source specialization and the loop-radius statement in Proposition 21.

At a=-1 the denominator is (1-2t)^2, so the length-m coefficient is exactly (m+1)2^m and its per-step exponential growth is two. Proposition 21 gives unrestricted closed-loop radius 1/8 in the half-length variable at a=-1, equivalently per-step exponential growth sqrt(8). This larger closed-loop growth is compatible with the smaller total because arbitrary endpoint sums are signed; the preceding explicit endpoint formula already supplies negative endpoints.

The comparison correctly shows that taking a square of the arbitrary-word growth rate is insufficient on the lower signed branch. It is not a nonnegative set-containment argument and does not imply an inconsistency in either source formula.

Public reference: Michael Albert and Mireille Bousquet-Mélou, *Permutations sortable by two stacks in parallel and quarter plane walks*, Propositions 18 and 21. https://arxiv.org/abs/1312.4487v3 .

No required correction was identified. 
