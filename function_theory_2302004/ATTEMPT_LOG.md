# Investigation log: 2302004 / Function Theory 2.4

## Turn 1: source resolution and explicit analytic verification

The exact catalogue URL was attempted, the stable record recovered, and
the source question and resolution update checked on the original PDF
pages. The substantive prior-work checks distinguished neighboring
Problem 2.5 and PR 491 from this problem. The recorded historical answer
was then corroborated in the original 1977 Hwang follow-up.

Toppila's original 1970 paper and Barth–Schneider's 1972 paper were not
recovered. The full Gol'dberg 1968 article was recovered, but its main
result has the different Problem 2.5 quantifiers. Hwang's own theorem
prescribes asymptotic values; it cannot by itself establish the required
exceptional-value omission. Neither related theorem was substituted for
the target statement.

A direct error-function witness was then verified. The proof consists of:

1. Entire-function definition, oddness, conjugation symmetry, and exact
   derivative of erf(z)
2. A uniform relative error estimate for 1-erf(z), derived by integration
   by parts in Re z>0; this proves eventual omission of 1 in a fixed
   wedge about pi/4
3. An omitted-two-values Montel argument: the rescaled functions tend
   to 1 at the center, whereas their center derivatives grow like the
   scaling radius. This forces every other finite value to occur
   infinitely in every angular neighborhood.
4. Reflection from pi/4 to the partner ray at 3pi/4, with exceptional
   value -1
5. A bijective affine change of values to obtain any prescribed a!=b

These are components of one completed proof, not five artificially
counted attempts. The concrete terminal question is resolved, with
historical priority retained. The investigation therefore stops at 1/5
under the early-completion exception. No further turns are claimed and
no exhausted status is used.

## Verification and limits

The statement and source update pages, plus both original Hwang pages,
were rendered and visually read. The proof itself supplies all witness-
specific estimates. The remaining analytic inputs are standard and
explicitly named. Forty-two finite controls check elementary algebra,
selected high-precision evaluations, and four deliberately incorrect or
out-of-domain variants. They are sanity checks, not a finite proof of
infinite preimage or normal-family claims.

There is no novelty, first-resolution, general-classification, or
original-Toppila-proof-verification claim. The public package excludes
all source copies. Independent review is a separate gate; this author
log does not declare that gate passed.
