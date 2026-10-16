# PR789 / problem 30001478: independent target-only review strategy

Frozen initial position: 2026-10-16 17:40:01 UTC.

This strategy was formed after reading only the repository-root `AGENTS.md` and
`tmp/intake/SELECTED_PUBLIC_RECORD.json`. The originally supplied lowercase
record filename did not exist; listing the intake identified the uppercase
record. No candidate proof, prior review, author program, parent conclusion, or
other reviewer's work has been read. The listing exposed filenames only. The
repository branch is `main`. This reviewer will make no Git mutations, publish
nothing, launch no subagents, and contact no outside individual.

## Exact hypotheses and target

The input is a connected graded algebra over an uncountable algebraically
closed field `k`, with degree-one generators `x1,x2,x3,x4` and the six displayed
quadratic relations from the selected record. The parameters `alpha,beta` are
algebraically independent over the prime subfield. No characteristic-zero
assumption has been supplied.

The two claims to test are:

1. The augmentation ideal `R_+` is the only nonzero proper homogeneous prime
   ideal of `R` (with zero and the whole ring handled explicitly).
2. There is no nontrivial map from `R` to a twisted homogeneous coordinate ring;
   the review assignment specifies a positive-dimensional target.

These claims are hypotheses, not facts. The source must settle the convention
for “nontrivial map”: a non-augmentation unital graded map, a surjection, and a
map with positive-dimensional image are materially different targets. The
selected record alone does not justify conflating them. The same applies to
prime versus completely prime and homogeneous versus graded-prime.

## Initial mathematical position

The most immediate falsification route is a degree-one scalar specialization.
Each relation is a sum of quadratic terms with coefficients of the form
`alpha,-1,1,-alpha` or `beta,-1,1,-beta`; the diagonal assignment
`x1=x2=x3=x4=t` appears to cancel them all. This is a target-only observation,
not a conclusion borrowed from a candidate. It should be checked first,
because if valid it supplies a map to `k[t]` and a candidate nonzero homogeneous
completely prime kernel. The map can also be composed with a degree-one
inclusion into an untwisted coordinate ring of a positive-dimensional scheme.
Whether the latter meets the historical intended “nontrivial” convention must
be read from the primary source rather than assumed.

## Independent attack families

| Family | Mechanism and checkable evidence | Initial status | Exact gap |
| --- | --- | --- | --- |
| Scalar/commutative quotients | Substitute `xi=ci*t`, solve or directly certify the six homogeneous scalar equations; prove kernel properties from an explicit quotient | First priority; diagonal candidate observed | Exact relation check and source meaning of map |
| Linear subspace quotients | Set selected generators equal or zero, derive the resulting presentation, look for polynomial, quantum-plane, or monomial quotients | Unstarted | Obtain an actual homomorphism and certify its kernel rather than infer it from numerical samples |
| Point-scheme / multilinear relations | Analyze degree-two evaluation at successive projective points and any constant points or orbits | Unstarted | Distinguish a point module from an algebra quotient or THCR map |
| Prime-ideal logic | For each explicit quotient prove nonzero, proper, homogeneous, prime, and distinct from `R_+`; test ordinary primeness if only graded primeness is argued | Unstarted | Exact generators, degree-one independence, and domain argument |
| THCR construction and conventions | Build `B(X,L,sigma)` explicitly, first using `X=P^1`, `L=O(1)`, `sigma=id`; certify multiplication and grading | Unstarted | Establish the map satisfies the actual historical claim, especially image dimension/surjectivity |
| Source and priority | Retrieve the official 2010 OWR statement and cited primary literature; compare every coefficient and parameter restriction | Deferred until initial strategy frozen | Exact source wording, current literature status, and novelty of any elementary observation |
| Artifact and reproducibility | Independently derive formulas, then audit candidate code, tests, package pins, and rendered PDF against the mathematical claims | Deferred pending frozen pins | Whether computation is independent, sufficient, and consistent with the prose |

The families will remain conceptually separate. No route will be credited for
moving the central assertion into an unproved auxiliary claim. Finite samples,
low-degree dimensions, and successful script exits alone cannot prove an
all-degree ring assertion.

## Boundary and adversarial cases

- All allowed characteristics, including characteristic two; avoid dividing by
  two or importing a sign distinction without justification.
- Algebraic independence over the prime subfield, not over an accidentally
  enlarged coefficient field. Check that any denominator excluded by a
  computation is actually nonzero under the input assumptions.
- `0`, `R_+`, and `R` as kernel edge cases; degree-one independence follows
  only if the defining ideal really has no linear component.
- Ordinary prime, graded-prime, and completely prime must not be interchanged
  without the stronger quotient property being established.
- A positive-dimensional target does not force a positive-dimensional image.
  A nonzero map need not be surjective. An augmentation map need not be the
  only map with finite-dimensional image.
- `X` a point versus `P^1`; `L` ample versus merely invertible; degree one
  versus a Veronese regrading; integral versus reducible targets; all must match
  the source convention.
- Parameter specializations may disprove a universal auxiliary assertion but
  cannot disprove the algebraically independent-parameter target unless they
  remain within its hypotheses.
- A later paper may define an isomorphic-looking algebra with different
  relations; verify rather than identify by title, notation, or Hilbert series.

## Success criteria for the full independent review

1. Recover and cite exact primary-source wording and match all six relations,
   assumptions, and target conventions to the frozen candidate.
2. Give a fully checkable proof or counterexample for every promoted claim,
   including nonzero/proper/kernel and THCR definitions as applicable.
3. Independently falsify the candidate's central inferences, edge cases,
   computational reductions, novelty claim, and all-degree assertions.
4. Reproduce the frozen package and rendered preprint, verify internal pins,
   and distinguish a computational certificate from editorial metadata.
5. Report a verdict with exact file/line evidence, severity, strongest verified
   result, unresolved gaps, and proposed repairs if needed.

Completion estimate at this checkpoint: **5% of the complete whole-preprint
review**. The target and strategy are fixed, but no candidate or source audit,
proof verification, priority investigation, or reproduction has yet occurred.
