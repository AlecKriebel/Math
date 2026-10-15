# Independent review of the Countryman five-turn partial packet

**Verdict: PASS_SCOPED_PARTIALS. Original problem remains unsolved, 5/5.**
No mandatory mathematical correction identified. This is an independent
adversarial assistant review, not a certification of novelty or human peer review.

## Binding artifacts and independence

This verdict binds RESULT.md SHA256
`dcca131134cdc67a7962082124eb69ced8c763a673652c95e60ff4d82f62517b`
and FROZEN_MANIFEST.json SHA256
`7b27622529076e3ca2302a31ed54c4a0b5259994eb4948995dd13330022c5ce8`.
All 26 listed author files and four primary PDFs hash-match. The reviewer
made no contribution to the author derivations and did not alter the frozen
files. This review examined all five infinite arguments, not only the summary.

## 1. Exact source and axiom boundaries

The original OWR 11/2017 printed p.543 asks the strong-surjectivity question
under PFA. I visually inspected that page. Moore's full author manuscript
uses exactly the eventually-zero sequences over C*+{0}+C. His Theorem 1.2
is embedding universality, not a quotient theorem. The latest arXiv record
for Polymeris–Martinez-Ranero remains v2, revised October 14, 2025; its
Question 6 and concluding p.28 explicitly retain the question. I visually
inspected the latter as well. This is a source-status observation, not a
claim that an exhaustive current literature search proves openness.

The packet correctly retains normal input in the later Countryman results.
The source fixes normal C before Lemma 3.10. Corollary 3.2 is under
MA_(aleph1); the fragmented-target conclusion is under PFA. The source's
first-coordinate-primary product agrees with the author; Camerlo–Carroy–
Marcone use the reversed multiplicative convention. Nonempty targets are
required throughout. The arbitrary-C structural/countable results do not
silently inherit a forcing axiom or a normal-input hypothesis.

## 2. Structural normality and its limited implication

The direct proof works. Finite-prefix cylinders are convex and copy the
whole eventual-zero order. Padding finite words with zeros exhausts it.
The finite product and countable-union preservation argument for the
Aronszajn exclusions is valid: an uncountable forbidden suborder in a product
either has an uncountable first-coordinate projection or an uncountable
fiber; choosing representatives preserves the relevant order type. The
same argument applies within the countable finite-support exhaustion.

In the displayed countable alphabet stage, an excluded point x has a missing
symbol at some coordinate j. Every point of the stage differs from x by
coordinate j at the latest. Changing x later than j and later than its
support cannot change any such comparison. Both signed changes remain
outside the stage and in the same complementary interval as x, on its two
sides. Thus no complementary interval has either endpoint. Continuity at a
limit follows from finitely many nonzero symbols. The order is endpoint-free
and every ray and nonempty open interval is uncountable. This establishes
the stated normality for arbitrary Countryman input.

The four endpoint sets are empty, including the two universal-quantifier
versions: each countable stage has nonempty complement and every component
fails each endpoint property. Hence the cited necessary stationary-set
condition has no force for this domain. The packet makes no converse claim.
The normal C0+C0* example is a credited countercontrol, not eta_C. Its final
summand would have countable image in C0, yet surjectivity would force an
uncountable final ray into that image; the contradiction is correct.

## 3. Retractions, sections, and all countable targets

Both directions of the cut criterion are sound, including empty outer cuts.
A monotone retraction fixes B, so its value at x must be the relevant greatest
left or least right B-point. The explicit lower-first rule is constant on
complementary cuts and monotone across them. Choosing one point per fiber
of an epimorphism gives an increasing section and hence a retraction onto
an alternative copy. This correctly distinguishes failure of a specified
embedding from nonexistence of any epimorphism.

The binary section in a bounded interval was the main constructive issue.
The ancestor bounds genuinely bracket every ambient continuation of the
selected finite word, not just binary descendants. A symbol smaller than
both branches lies between the previous lower ancestor and the entire
current subtree; the lower ancestor is adjacent in the section cut. The
upper case is symmetric. A symbol strictly between a branch and zero is
adjacent to the current node on the appropriate side. At a zero symbol,
any later nonzero tail places x to one side of that same node with no
section point between. Eventual zero forces one of these finite exits;
infinite all-branch paths, which would cause nonprincipal cuts, are absent.
The full finite-node binary order is dense and endpoint-free.

Adding the interval endpoints handles points outside the interior cylinder.
Shortness and absence of endpoints give countable coinitial and cofinal
sequences, which can be chosen as one increasing Z-indexed sequence.
The interval retractions agree at shared endpoints, so their union is a
global retraction onto a countable dense endpoint-free section. Finally
K×Q is countable, dense and endpoint-free for every nonempty countable K:
within a fiber use density of Q; between distinct fibers move farther in
the earlier fiber. Its first-coordinate projection is a quotient onto K.
Thus the all-countable-target theorem, including targets with endpoints or
adjacent pairs, follows in ZFC for arbitrary C.

## 4. Prefix lifting and nonfragmented examples

The short-product input is correctly invoked: U×V maps onto V for nonempty
short U,V. I checked the actual definition-by-pieces proof and Corollary 2.11
in Camerlo–Carroy–Marcone, as well as Lemma 3.4 of the later paper. The
second-coordinate projection is indeed false and is not used.

Fibers of an index epimorphism D^n->I are nonempty convex short orders.
The decomposition into their products with L, followed by the short-product
map and each prescribed summand map, is an honest monotone surjection onto
the ordered sum. Finite-sum examples follow and contain L, so they are
nonfragmented in the source's eta_C-relative sense. Their embedding back
into L uses PFA; the quotient constructions themselves do not.

For the additional normal-C/MA conclusions, the base D^2->C,C* argument
requires only the stated normal-Countryman strong-surjectivity input and
the short-product lemma, not the PFA rank induction. Normal C contains Q,
so it has all countable quotients under that input. This validates the
countable and Countryman-indexed closure with the exact added hypotheses.
None gives an index quotient from a finite D^n onto arbitrary L. The warning
about interleaving and nondecreasing recursive fiber complexity is correct.

## 5. Forcing route and obstruction scope

For finite monotone partial maps, a new domain point can be assigned a
neighboring existing value. A new range value can be placed in the gap
between the last lower-value and first higher-value domain points; density
and absence of endpoints supply a point in every required finite gap.
The domain/range dense sets number at most aleph1. A directed filter meeting
them gives a total onto monotone map. Properness would therefore suffice
under PFA, but has not been proved.

The reversed singleton assignments indexed by C form an uncountable
antichain. That defeats ccc, not properness. It does not contradict the
identity quotient for target L. Likewise the rational-cut example is valid:
S=Q-indexed Q-blocks with the zero block removed is coinitial and cofinal in
T; the selected onto map has open, endpoint-free fibers; every proposed
value on the missing block must equal an irrational Dedekind cut and hence
cannot be rational. Both S and T still have type Q and other quotients
exist. This is a chosen-map extension obstruction only.

The packet identifies the actual remaining target: a universally suitable
section or proper forcing argument for every uncountable nonfragmented
suborder, or an intrinsic counterexample excluding all sections. None is
present. There is no unearned full solution.

## 6. Computation and turn accounting

All five author outputs replay byte-for-byte: 157,360; 9,738; 1,887,478;
142,914; and 12,242 exact controls. My separately written checker passes
542,624 exact assertions. It uses dyadic coordinates for the binary section,
all sections of finite monotone surjections, missing-alphabet comparisons,
and independent rational domain/range extension controls. It imports no
author checker. Finite tests are not treated as evidence for a forcing axiom,
properness, stationary-set theorem, or universal uncountable conclusion.

The five completed ledger entries correspond to genuine distinct deductions:
structural normality; the exact section criterion and a false-counterexample
control; the countable quotient construction; finite-prefix lifting; and the
forcing criterion with limit-cut/ccc obstructions. Source retrieval and
packaging are separate. The original status should remain **unsolved, 5/5**.
The unchanged mathematical packet is suitable for a scoped partial-result
draft subject to the parent's publication gate.
