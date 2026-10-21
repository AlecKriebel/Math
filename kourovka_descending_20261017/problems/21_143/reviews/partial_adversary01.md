# Adversarial review of the partial 21.143 deductions

2026-10-17T21:13 UTC. Independent review requested by the research coordinator.
Review completion estimate: **100%** for the supplied partial claims; estimated
completion toward resolving 21.143 remains **at most 8%**, with the central
question completely open. No solution, originality, formal verification, or
independent human verification is certified. No external individual was
contacted, no outreach was prepared, and no Git, release, PR, or shared-queue
operation was performed by this reviewer.

## Verdict and precise strongest claim

I found no fatal mathematical gap in the current rational-recoding proposition
or in the stated parametric obstructions. The main new partial statement is
valid with its explicit hypotheses:

> There is no rational relation R from **all** Guba–Sapir normal words N into a
> finite-alphabet language L, preserving the represented element on every
> related pair, if the **full** right-y multiplier of L is rational.

L may have an arbitrary, non-letterwise interpretation in F, and that
interpretation need not be injective. The statement therefore applies to
graph-automatic presentations as well as classical automatic structures. It
excludes only presentations admitting the specified total rational recoding
from N. Neither an arbitrary regular combing nor an arbitrary graph code is
known to admit such a recoding, so the all-structures quantifier needed for a
negative answer to 21.143 has not been obtained.

## Rational relations: independent proof and convention audit

The accepting-suffix lemma in `rational_recoding_obstruction.md` is correct.
For any successful prefix labels (p,r) reaching state q, fix an accepting
suffix (a_q,b_q). Because **every** accepted pair satisfies the right-multiplier
equation, the concatenation with this fixed suffix gives

    eval(p) eval(a_q) y = eval(r) eval(b_q),
    eval(p)^(-1) eval(r) = eval(a_q) y eval(b_q)^(-1).

The right-hand side depends only on q. Thus left-invariant word distance
between the two prefix endpoints is uniformly bounded. Finite word labels
on transitions add at most the maximum sum of their lengths while the
transition is traversed. Epsilon moves, nondeterminism, epsilon/epsilon
cycles, and infinitely many partners for one word do not defeat this proof.
It gives monotone surjective continuous clocks with pauses, without asserting
a bound on relative clock speeds. The lemma concerns generator-word paths
on its input tapes; it is not being applied directly to arbitrary graph-code
prefixes.

A padded synchronous relation is rational: replace each right-padding symbol
on a transducer tape by epsilon, preserving ordinary symbols. Its exact
right-padding convention is important to the separate length-gap lemma;
padding in the middle of words would not justify that argument. For rational
relations themselves, inversion swaps the tapes. Composition is the standard
finite-state product construction synchronizing the intermediate tape,
splitting word labels into letters and allowing epsilon transitions. These
closure properties do not require length bounds or finite fibers.

For the recoding proposition, the forward inclusion in

    R ; M_y(L) ; R^(-1) = M_y(N)

uses element preservation on **both** occurrences of R. For the reverse
inclusion, totality supplies an R-output for each of the given N-words, and
the **full** multiplier contains those two outputs. No surjectivity of R onto
all codes of L is required. No uniqueness of R-output is required. Replacing
the full multiplier by an incomplete selection of adjacent code pairs would
invalidate the reverse inclusion and is not allowed. Restricting an originally
larger rational relation to the regular input domain N preserves rationality.

The graph-automatic extension is sound. Once the composite is formed, both
outside tapes are again actual generator words in N, so the accepting-suffix
lemma applies to that composite. If a graph presentation uses a different
finite generating set, express y as a fixed word in that set and compose its
full edge relations; a surjective presentation supplies all intermediate
codes. This also yields its full y multiplier. The argument never assumes
that output symbols evaluate as individual generators.

## Parametric witnesses and other local deductions

* **GS words.** The forbidden-subword definition does include both
  u_n=y x^n and v_n=x^n y X^(n+1) y x^(n+1), for every n>=1. There is no
  free cancellation and no forbidden positive-x block between the y letters
  in v_n. Their lengths are n+1 and 3n+4. With f_(uv)=f_u after f_v,
  a_1=x y X^2 has closed support [0,1/2], and conjugating by x^(n-1)
  gives closed support [0,2^(-n)]. Its support is disjoint from the interior
  support of y, including the n=1 boundary, so a_n commutes with y. This
  proves u_n y=v_n in the specified PL convention; it is not a convention
  imported from an oppositely acting diagram model.

* **Synchronous obstruction.** At prefix time 2n+3, v_n has quotient
  coordinates (-1,2), whereas the stationary u_n endpoint is (n,1).
  The l1 distance is n+2. The exponent-sum quotient is nonexpanding because
  each standard generator maps to a unit vector or its negative.

* **Asynchronous obstruction.** v_n reaches (n,0) before (-1,2), while
  the x coordinate on u_n is nondecreasing and nonnegative and its y
  coordinate lies in [0,1]. A K-close monotone surjective matching would
  force the two corresponding u_n coordinates a,b to satisfy
  a>=n-K, b>=a, and K>=b+2. Therefore 2K>=n+2. This remains valid for
  continuous clocks: both specified v_n vertices must be reached in the
  stated order. This establishes nonrationality of the full N multiplier,
  rather than merely nonregularity of its padded convolution.
  The subsequently supplied exact discrete quotient formula was also
  checked: A_n=2 for n=1,2, and A_n=ceil((n+3)/2) for n>=3. When K<n,
  the first matched u_n point has positive x coordinate and therefore
  y coordinate one, strengthening the lower bound to 2K>=n+3. Otherwise
  K>=n; the point (-1,2) always gives K>=2. The two described monotone
  constructions attain n (for n>=2) and ceil((n+3)/2), respectively.
  This proves the formula with the exceptional first two cases. It is
  explicitly a discrete quotient result, not an exact Cayley distance.

* **Finite-fiber length gaps.** The pumping argument is correct in both
  directions. A tail of q letters after the other tape ends has q+1
  state visits along an accepting run, yielding a pumpable nonempty tail
  cycle. The shorter word stays fixed, contradicting its finite fiber.
  Arbitrary nonunique automatic languages need not have finite fibers;
  the notes apply the lemma only with the appropriate uniqueness/finiteness
  hypothesis. The necessary length function in the obstruction note does
  not constitute an automatic structure by itself.

* **Unary and binary indices.** The unary pair represents x_0^(-n) and
  x_0^(-n)x_1^(-1)=x_(n+1)^(-1)x_0^(-n); its symbol-length gap is n+2.
  In the binary obstruction, all four generators increase reduced dyadic
  point depth by at most one, including their low-depth boundary points.
  The breakpoint-preimage inclusion yields depth<=|w|+2. The genuine
  breakpoint of x_i at 1-2^(-(i+2)) then gives |x_i|>=i. The strengthened
  short-witness claim supplied during review is valid for arbitrary
  rational relations: from an accepting run delete all cycles inside
  input-epsilon segments. The resulting run has the same input, still
  accepts, and has output length bounded linearly in input length.
  Every retained output of a semantically correct relation must remain
  a representative of the same group element. Thus even a multivalued
  total rational relation cannot decode O(log i)-length binary codes to
  generator words for x_i. An explicit code family containing x_i is
  essential. No arbitrary graph code or nonrational decoder is excluded.

* **Tree domains.** The serial comb intersection and synchronized
  (AB)^k(CD)^ell D intersection are exact; in the latter, top-row tree
  balance forces k=ell. The n=1 unreduced pair is correctly excluded,
  and the first synchronized witness is n=2. Reducedness is checked by
  common exposed-caret leaf positions. Rational images of regular
  languages are regular, so the exact-image restriction in the tree
  decoration theorem is essential and sufficient. The exact multiplier
  projection theorem correctly assumes every group element has a code.
  The ranked-tree proof correctly determinizes before identifying two
  left-comb states. It excludes the specified separated-tree domain only.

* **Frontier calculation.** On the negative cone, the current insertion
  index is 1 plus crossed multiplicity, and H_(i+1)=H_i+s_i-1. The first
  nonpositive height is exactly zero, and eventual zero follows from
  finite support. The first-return language on the unchanged stream is
  nonregular via its b*#* slice. The notes correctly refrain from
  concluding that every frontier recoding fails. Tagged zipped and LSB
  binary successor slices demonstrate why such a conclusion would fail.

* **Other structural routes.** The disjoint-support infinite-rank argument
  and the elementary slope proof of uniform positive cyclic stable length
  are sound. At the leftmost support endpoint, the first nonidentity
  right-hand slope must be 2^k with k!=0; powers multiply its logarithm,
  whereas a word of length m has one-sided log slope bounded by m.
  The root-degree bound uses equality of fixed sets for positive powers of
  an increasing interval homeomorphism. Neither this nor quadratic filling,
  subgroup embeddings, or infinite cohomological dimension supplies the
  missing all-automatic obstruction. The wreath and higher-filling routes
  are accurately recorded as blocked or without decisive evidence.

## Issues found and corrections

No mathematical error requiring rejection was found in the reviewed final
statements. Two scope sentences in the first draft of the recoding note were
tightened after review:

1. A general phrase about “bounded local substitutions” could accidentally
   include unbounded iteration of bounded rewrites, whose overall relation
   need not be rational. The current version says finite-state substitutions
   and explicitly preserves the unbounded-iteration exception.
2. “Requires genuinely unbounded memory” was stronger and model-dependent
   compared with the proved conclusion. The current version says the total
   conversion must be nonrational. Nonrational algorithms are not excluded.

These changes preserve the theorem while preventing a route obstruction from
silently becoming a claim about arbitrary normalization algorithms. The
corrected wording was re-read before this verdict.

## Reproduction and source audit

Both supplied scripts were rerun successfully:

* `constructive_checks.py`: the GS, unary-index, and x_i depth families for
  indices 1 through 64; 8,188 dyadic generator/point checks; all 1,365 words
  through length five; the two finite presentation relators and inverse
  identities. Its output report was regenerated by the script.
* `tree_language_verify.py`: 203,456 equal-caret tree pairs through seven
  carets; opposite combs through 100 carets; 5,461 exponent vectors of
  length at most six with entries 0 through 3. All claimed finite counts
  and exact intersection descriptions reproduced.

For additional independence I directly evaluated the four generators using
their elementary branch formulas, without the supplied breakpoint
composition routine, on dyadic points near both endpoints and on a uniform
grid for n=1,...,64. I also independently implemented the monotone quotient
dynamic program for n=1,...,40. These extra finite results are recorded in
`partial_adversary01_checks.json` (8,066 direct branch point checks and
40 independently recomputed matching values); they corroborate conventions and bounds,
not the universal quantifiers. The universal arguments above remain decisive.

All 19 retained source objects in `priority_sources/manifest.json` passed
independent SHA-256 revalidation. The two intentionally rejected identifier
payloads and two failed fetches were not counted as retained evidence.
The retained primary text was checked directly for Corwin et al. §2.2
(the GS rules, regularity, uniqueness, and distinction from synchronously
regular rewriting), Elder–Taback Definitions 2.1–2.3 and Lemma 3.7
(right padding, arbitrary symbol codes, and the exact unary witness), and
Guba–Sapir's historical definition of regular rewriting. The official
October 6, 2026 entry is the unstarred 21.143 question, and the retained
October 8 proposer list still contains “Is F automatic?” Source hashes
certify bytes, not the validity of long source proofs. Strike-through
status is not inferable from text extraction; the companion visual audit
supplies that separate check. This reviewer did not perform a new exhaustive
current-literature search.

The source's informal claim about a four-counter GS implementation is not
being used as a lower-bound theorem: its details are explicitly omitted in
that paper. No citation or current-status statement is being upgraded into
a proof of the new deduction. No originality claim is justified by this
review. Long inherited theorems in the priority note remain literature
inputs, with the note's stated access and verification limits.

## Exact unresolved gap

A full affirmative result still requires a regular surjective generator-word
language and its exact equality and all generator multiplier relations, or a
uniform all-adjacent-pairs synchronous fellow-traveller proof. A full negative
result still requires an obstruction for **every** such regular language.
The present proof shows that any hypothetical structure must be related to N
by a conversion outside the rational class considered here. No theorem
forces hypothetical automatic structures to lie inside that class. Thus
Kourovka 21.143 remains unresolved by this research checkpoint.
