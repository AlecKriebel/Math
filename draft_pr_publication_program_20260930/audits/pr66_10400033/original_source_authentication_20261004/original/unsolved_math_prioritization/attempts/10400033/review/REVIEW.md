# Independent adversarial review: Willerton's degree-three bound

**Verdict: PASS_COMPLETE_PROOF.** The reviewed argument proves the full
inequality in Ohtsuki Conjecture 2.11, together with its stated stronger
even-crossing bound. No mandatory mathematical correction was identified.
This is an independent AI review of a candidate proof, not human peer review
or a historical-priority determination.

Reviewed on 2026-09-30 using GPT-6 Astra at xhigh reasoning effort.
The exact reviewed `CANDIDATE.md` has SHA-256
`fc2be9794873073e6482e8dfe93ccfd6c5d6f8674c2058ba0a8fc900d906d698`.
Its unchanged bytes are preserved in `author_replay/CANDIDATE.md`.

## 1. Exact target and imported identity

The original target concerns every classical knot diagram with (n)
crossings, with no minimality or positivity condition. The invariant is
normalized to be additive, mirror-odd, and (1) on the right trefoil. The
candidate matches these hypotheses and the floor in the original bound.
The normalization and target on printed pp.403 and 405 were inspected
visually. This does not solve the separate joint-range Problem 2.10.
See [Ohtsuki's original problem list](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf).

The two pictures in [Polyak--Viro, Theorem 2, equation (5),
p.448](https://www.math.stonybrook.edu/~oleg/math/papers/1994-Polyak-Viro.pdf)
were read directly from the scan. Their arrows are simple arrows, not
multiplicity-two arrows. The path has coefficient (1/2), and the triangle
has coefficient (1), when occurrences are counted by their three-arrow
images. Their overpass-to-underpass convention agrees with the candidate.

The distinction between images and labelled embeddings is essential. It is
not safe to read the original informal representation definition as counting
all labelled embeddings while retaining the displayed triangle coefficient.
The independent audit located a direct published clarification:
[Östlund, *A diagrammatic approach to link invariants of finite degree*,
Math. Scand. 94 (2004), 295--319](https://journals.msp.org/mscand/article/view/775),
Sections 1.6, 2.2--2.4 and Proposition 4(4), especially the note on p.302.
Its [publisher PDF](https://journals.msp.org/mscand/article/download/775/774)
was retrieved and pp.301--302 were inspected visually. In the symmetrized
embedding convention its formula is (T/3+P/2); the triangle has three
rotational symmetries and the path has one. Consequently this gives exactly
one signed contribution per triangle image and one half per path image.

There is also a harmless circle-orientation convention to check. Reflecting
the displayed cyclic order preserves the triangle type and exchanges the
two path types. Östlund's Proposition 4(1), the vanishing (O_3) identity,
equates their signed counts on classical knot diagrams. Both path types
give the same directed-path domination below. Thus choosing the candidate's
explicit cyclic transcription introduces neither a missing term nor an
orientation hypothesis. Zhang's opposite over/under convention was not
silently substituted for the original convention; its Remark 4.1 was used
only as an additional check of the symmetry conversion.

The normalization also agrees with [Willerton, Section 1](https://arxiv.org/abs/math/0104061v1):

\[
v_3=-\frac{J'''(1)+3J''(1)}{36}.
\]

In particular the right trefoil polynomial (J(q)=q+q^3-q^4) gives (v_3=1).
The Jones coefficient (j_3=[h^3]J(e^h)) is (-6v_3), not (v_3).
The audit keeps this scaling explicit.

## 2. Audit of the all-diagram argument

**Crossing signs.** A selected three-arrow image contributes its fixed
nonnegative pattern coefficient times a product of three signs in
({-1,1}). The triangle inequality therefore gives
(|v_3|\le N_T+N_P/2) without requiring positive crossings or realizability
of independently chosen signs. The proof never assumes these summands all
have the same sign.

**The partial orientation.** For two interlaced arrows (c,d), rotate their
four endpoints to start at the tail of (c). Their order is either
(t_c,t_d,h_c,h_d), giving (c\to d), or
(t_c,h_d,h_c,t_d), giving (d\to c). These exhaust the interlaced cases
and prove antisymmetry. Noninterlaced pairs have no edge.
For the candidate's path, the directed edges are (b\to c\to a), with
the (a,b) edge absent. For its triangle they are
(c\to b\to a\to c). This verification depends only on cyclic endpoint
order, not on crossing signs or on other arrows of the diagram.

**Random completion.** There is one cyclicity indicator per unordered
three-element vertex subset. A triangle image has cyclicity probability
one; a path image has probability one half, since precisely one orientation
of its unique missing edge closes a cycle. Other configurations contribute
zero or a positive probability and have zero weight in the imported
two-pattern formula. This last point handles all other chord configurations;
they need not be classified further in the proof. Linear expectation is
valid even when triples overlap. Nothing requires the completed tournament
to be realizable by a knot or a chord diagram.

**The sharp tournament estimate.** Each transitive triple has exactly one
vertex beating the other two. Hence its count is
(\sum_i\binom{d_i}{2}), with no double counting. Using
(\sum_i d_i=n(n-1)/2) gives

\[
C=\binom n3-\sum_i\binom{d_i}{2}
 =\frac{n(n^2-1)}{24}
  -\frac12\sum_i\left(d_i-\frac{n-1}{2}\right)^2.
\]

Every completion therefore has at most
(\lfloor n(n^2-1)/24\rfloor) cycles. Taking the expectation preserves
this integer upper bound; the argument does not incorrectly round an
expectation. For even (n), every squared term is at least (1/4), giving
(C\le n(n^2-4)/24). If (n=2m), this last expression is
(m(m-1)(m+1)/3), so it is an integer. Combining the estimate with the
previous domination proves both asserted inequalities.

**Boundary cases and sharpness.** The three-arrow formula vanishes for
(n=0,1,2), and both relevant bounds are zero there. Arbitrary diagrams,
mixed crossing signs, and composite knots remain covered. The known
(T(2,n)) value for odd (n\ge3) gives equality in the first bound.
It is used only for sharpness. No sharpness claim for knots at every even
crossing number is required or made. The proof also bounds the corresponding
formal arrow evaluation, but it does not establish a virtual-knot invariant.

## 3. Reproducible independent checks

All five files in the author's frozen manifest matched their recorded
hashes. The copied verifier reproduced `author_replay/verification.json`
byte for byte: **42,867 exact assertions**, comprising 42,684 graph/sign
controls and 183 Jones/formula assertions on 59 classical diagrams.

The independently written `independent_checks.py` imports no author code.
It uses signed cyclic words rather than endpoint-pair canonicalization,
and evaluates the Jones polynomial by Temperley--Lieb multiplication rather
than by the author's state-sum union-find calculation. Its exact checks cover:

- all 720 labelled six-endpoint orders, every crossing-sign choice, cyclic
  basepoint changes, circle reversal, and the two automorphism orders;
- both the displayed path and its reflected version;
- all 33,868 tournaments on zero through six vertices, checking the direct
  cycle count, the outdegree identity, the square identity, the bound and
  small-order attainment;
- 65 closed two- or three-strand classical braid diagrams, including mixed
  signs, both trefoils, the figure-eight knot, and (T(3,4),T(3,5)), with
  independently computed full Laurent Jones polynomials and reflected-path
  identities.

The resulting **115,776 assertions pass**. These finite controls detect
transcription, normalization and implementation errors. The general result
rests on the imported knot-invariant identity and the written
all-diagram argument, not on the finite sample.

To reproduce, run `python author_replay/verify.py` and
`python independent_checks.py` from this review directory and compare stdout
with the respective `verification.json` and `independent_results.json`.
The preserved candidate snapshot is a required dependency of the independent
checker because it verifies the reviewed hash.

## 4. Attribution, limitations, and recommendation

The original p.403 display (\lfloor n(n-1)(n-2)/15\rfloor) is inconsistent
with that source's trefoil normalization when (n=3). The author's source
note reports this accurately, and the candidate does not use that display.
It does not affect the correctly transcribed Conjecture 2.11.

The audit found primary literature for the Polyak--Viro identity, its symmetry
correction, and the known torus-knot case. Limited current searches did not
establish whether the general tournament argument has appeared previously.
The Polyak--Viro formula, Östlund's convention clarification, elementary
tournament counting, and torus evaluations must retain their attribution.
Neither this review nor a successful finite calculation establishes first
discovery or present-day historical novelty.

The package may be presented as a complete candidate proof that passed a
separate adversarial AI review, with human peer review and historical priority
unconfirmed. There is no remaining mathematical gap identified by this audit
and no mandatory change to the frozen proof. Adding Östlund's explicit
published convention clarification to the source bibliography would improve
its documentation; the clarification is already fully recorded here.

The review did not alter the author's mathematical files. Third-party source
PDFs and rendered pages used for this audit are not part of the public review
bundle.
