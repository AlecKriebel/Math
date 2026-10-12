# Independent audit of the family-129 complementation input

Audit checkpoint: 2026-10-06 21:14 PDT (2026-10-07 04:14 UTC).
Auditor: an independent AI subagent; no human peer review is implied.

Upstream checkout `/Users/alec/Desktop/math` was read only and its HEAD was
verified as `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Below `P/` abbreviates
`preprints/An-exponential-state-lower-bound-for-two-way-nondeterministic-complementation-September-25-2026/build/`,
and `L/` abbreviates `lean/OAI/Combinatorics/TwoWayAutomata/`. Line numbers
refer to that pinned checkout. No generated files were written upstream.

## Exact usable input

For integer `h ≥ 2`, let `H = Fin h`, let `Σ_H` contain **every** binary
relation on H, and compose in path order. For `w=R_1…R_k`, define
`r(w)=R_1…R_k` and `r(ε)=I_H`. Set
`L_H = {w ∈ Σ_H* : r(w) ≠ ∅}`.

There is an explicit partial **one-way** NFA in the marked model with
exactly `h+2` states recognizing this language. Every marked 2NFA with s
states recognizing `Σ_H* \ L_H` satisfies
`2^floor((h−2)/127) ≤ 2(s+1)`.
Equivalently, `s ≥ ½·2^floor((h−2)/127)−1`. The target remains
nondeterministic and has unrestricted two-way motion. The original source
is already one-way.

Evidence: `P/sections/introduction.tex:23–54`,
`P/sections/automata.tex:14–40,145–159`, `L/Source.lean:10–36,141–161`,
`L/Main.lean:10–43`, and `L/ExplicitFamily.lean:7–33`.

## Exact conventions and boundary cases

The state count includes initial and accepting states. The head starts at
the left endmarker. There are two distinct endmarker cells even on ε.
Transitions depend only on state and scanned symbol and choose a state and
one move in `{left,stay,right}`. Moves leaving the marked tape are disabled.
Finite reachability of an accepting configuration defines acceptance,
including a run with zero transitions if the initial state accepts. Missing
transitions reject that branch. Infinite nonaccepting branches do not
accept. No global halting assumption is present.

The source states are `q_in`, h states in H, and `q_acc`. Its only rules:

* `q_in` at the left marker → `(p,right)` for every `p∈H`;
* p at a relation R → `(q,right)` iff `(p,q)∈R`;
* p at the right marker → `(q_acc,stay)` for every `p∈H`.

All other transitions are missing. Only `q_acc` accepts. An accepting run
is exactly a path through the successive relations. On ε, the initial
right move reaches the right marker and the accepting stay is available;
this matches `I_H ≠ ∅`. The complement excludes ε. The alphabet has
`2^(h²)` symbols, including empty and identity relations.

Evidence: `P/sections/introduction.tex:12–21`,
`P/sections/automata.tex:21–40`; `L/Model.lean:13–41` realizes precisely
these semantics using `Fin (|w|+2)` positions and finite reflexive
transitive reachability. `L/Source.lean:26–36` gives precisely the rules.

## Complement universe in the binary reduction

The upstream complement is in **all** `Σ_H*`, not a promise subset. Its
formal premise is `B.language = A.languageᶜ`, where complement is in
`Set (List (SetRel H H))` (`L/Main.lean:11–14`).

Row-major adjacency encoding uses fixed blocks of length `ℓ=h²`. Every
ℓ-bit block is a relation. The only malformed binary strings have lengths
not divisible by ℓ. Define the source on every binary word by
`K_h={enc(w):w∈L_H}`. It rejects malformed lengths and accepts ε.
Its full binary complement is malformed words together with encodings of
empty relation products. Pulling back any target for `{0,1}* \ K_h` gives
exactly `Σ_H* \ L_H`, since `enc(w)∈K_h ⇔ w∈L_H` for every w.
Seeing only valid encodings does not weaken that restricted equivalence.

A verified bound `s'≤C h²s+C'` would consequently imply
`2^floor((h−2)/127)≤2(C h²s+C'+1)`. The binary source's actual count must
then be substituted with its polynomial growth preserved. This note does
not certify the compiler or its precise counts; reduction agents own that
independent task.

## Central upstream proof audit

I read the central handwritten proof and checked corresponding real formal
declaration chains, not the ComparatorChallenges statements. No `sorry`,
`axiom`, or `admit` occurs in the TwoWayAutomata source text; this textual
observation alone is neither a build nor an axiom audit.

1. **Finite computation representation.** Four local relations encode
   finite stays followed by one exit move. A fresh success state sweeps
   right and exits beyond the right marker; it can first be entered only
   from an original accepting configuration. A successful finite diagram
   path is therefore equivalent to original finite acceptance, including
   initial acceptance. Repeated crossings and stay cycles are allowed.
   Finite closure does not turn an infinite nonaccepting run into
   acceptance. Local augmented moves enforce marker restrictions.
   Evidence: `P/sections/automata.tex:50–126`;
   `L/Normalization.lean:58–65,67–123,125–201` and
   `L/Representation.lean:9–79`. The new exit position is a representation
   device, not a permitted position for the original machine.

2. **Order reversal.** More diagram edges preserve acceptance in every
   context. Sandwiching a word between singleton identities `I_p` and
   `I_q` tests whether its product lacks `(p,q)`. Thus componentwise
   `τ(u)⊆τ(v)` implies `r(v)⊆r(u)`. Applying this twice to equality makes
   `φ(τ(w))=r(w)` well-defined. This map is multiplicative, unital and
   surjective because every relation is a source letter. Evidence:
   `P/sections/diagrams.tex:134–228`; actual declarations are
   `word_diagram_order_reversal`, `diagram_relation_image` and
   `diagram_recognition_lower_bound` (`L/Recognition.lean:10–110`).

3. **Common transport.** Idempotent through edges are covered by
   rectangles associated with recurrent classes. A rectangle survives
   when its class is not missing; return edges persist in corner
   replacement. If two target classes of one sign share an old rectangle
   in their witnesses, crossing prefixes/suffixes gives mutual target
   recurrence, so the classes coincide. One common budget J therefore
   affects at most `2|J|` target classes, even with backward middle edges
   and repeated crossings. The two-sign factor is explicit; no
   deterministic-path restriction occurs. Evidence:
   `P/sections/diagrams.tex:238–351,359–415`;
   `L/Transport.lean:79–167`.

4. **Nested-chain budget.** A new recurrent class contains a surviving
   whole old class or two distinct whole old classes, signs preserved.
   Protected representatives of every initial class outside the common
   budget persist. Missing classes are unprotected. Give missing old
   classes weight ½ and other unprotected old classes weight 1. The
   unprotected count decreases by at least half the current loss, so
   summation bounds total loss by twice the initial budget. Nesting is
   distinct from diagram inclusion throughout. Evidence:
   `P/sections/nesting.tex:17–211`, `L/Nesting.lean:199–346`.

5. **Amplification and constants.** Minimal idempotent corners supply
   unit lifts rather than presuming permutations lift to units. A hub
   gives 128 conjugate generators; sandwiched products give 4096
   independent bipartite additions with common budget ≤`8·64·c`.
   The nested chain costs ≤`16·64·c`. Each restriction retains its two
   endpoints and all points outside the 129-point construction, giving a
   full relation monoid on `h−127` points, and costs at least half its
   inductive bound. Hence `c≥(64/32)D(h−127)=2D(h−127)=D(h)`.
   The base interval is `2≤h≤128`; the recurrence starts at h=129.
   There are at most `2m` classes, with `m=s+1`. Evidence:
   `P/sections/amplification.tex:27–104,108–368`;
   `L/ImageBound.lean:12–177,180–278`.

No substantive gap was found in this audit. I challenged unitality,
positive powers in finite semigroups, unit lifting, restricted-corner
surjectivity, signs, changing class identities, full-word complements, ε,
initial acceptance, marker restrictions, missing transitions, stay cycles
and infinite unsuccessful computations. Source/core formal semantics agree
with the handwritten theorem. This is an independent reading assessment;
the separate pinned-copy build and axiom-output reproduction remains owned
by `formal_reproduction`.

## Independent computational falsification

`agent_notes/upstream_algebra_check.py` implements the four-relation product
from scratch using Boolean matrices. It does not call upstream Lean or
copy executable upstream code. Output:
`agent_notes/upstream_algebra_check.json`.

No assertion failed. Width one: all 16 diagrams, all 56 corner pairs,
896 missing-product cases, 56 nested-class cases, all 4096 transport
contexts and 9216 common-budget cases. Width two: all 65,536 diagrams
enumerated, 12,821 idempotents; seed 129 gives 10,000 corner/nesting
samples, 30,000 product samples, 1,794 qualifying transport contexts and
7,412 common-budget samples.

These check tiny structural cases, not the 129-point amplification or the
uniform exponential theorem. Reproduce with
`python3 agent_notes/upstream_algebra_check.py` from this project folder;
Python standard library only.

SHA-256 checker:
`cfdb53dda2890064ba68e60c9ba79c31f5202f55bb67b04ed96f963547951ce8`.
SHA-256 result:
`83ffda5b2a15477885c26768ed33a869d635f5b08b08b30024f5ae9036a494c6`.

## Scope and provenance

The supplied author is **OpenAI**, dated September 25, 2026. Cite the
manuscript-specific BibTeX in its README. The repository README describes
internal-model authorship and warns that some unformalized results may
have issues. `lean/docs/129.md:10–14` explicitly identifies growing
alphabets and the marked finite-run model. That note does not certify the
fixed-binary follow-on or a uniform complexity-class separation.

This input is usable if its actual Lean reproduction and axiom audit
complete satisfactorily. This audit does not establish public priority,
check later corrections, review all companion literature, or claim binary
encoding machinery is novel. Those are separate checks. No external
individual was contacted.

Pinned Lean: `leanprover/lean4:v4.34.1`. Pinned mathlib:
`d13f23b723b8a846827a245b89c10fc7d3f11612`.

Exact SHA-256 source hashes are saved in
`agent_notes/upstream_complementation_sha256.txt`; paths there are relative
to the pinned read-only checkout. These identify every source read above,
including Normalization and Tape.

## Addendum: handwritten proof evidence versus unreproduced Lean checks

Timestamp: 2026-10-06 21:24 PDT (2026-10-07 04:24 UTC).

The earlier sentence, "This input is usable if its actual Lean
reproduction and axiom audit complete satisfactorily," remains above as
the original checkpoint record. Its implied requirement of a successful
Lean rebuild was stronger than my mathematical findings supported. I had
intended the rebuild and axiom output as additional verification and as a
prerequisite to a claim of **reproduced formal verification**. I did not
identify a mathematical lemma or semantic obligation whose only available
proof was a prospective successful Lean build.

On reassessing my own audit, there is no precise unresolved mathematical or
semantic concern requiring kernel reproduction before the input theorem
can be cited and used. The evidence supporting that assessment is the
handwritten proof inspection recorded above, independently of the existence
of the Lean files. In particular, I checked the full central uniform
argument, not merely the released theorem statement, README, small tests,
or formal signatures:

* The computation-to-diagram equivalence has both finite-path directions;
  its accepting-state sweep and local boundary guards preserve exactly the
  marked finite-run model, including epsilon and initial acceptance. The
  singleton identities then establish the full order-reversing relation
  image using arbitrary contexts, with no halting or promise assumption.
* The recurrent rectangles cover every idempotent through edge by finite
  repetition. Crossing two paths sharing one rectangle proves that they
  belong to one target class of the same sign. This supplies the common
  transport budget for an entire family of replacements, which is the
  stronger statement the amplification actually needs.
* The nested-class dichotomy and protected-label weight argument bound
  the sum of losses while the identities change. In particular, the proof
  does not attempt to compare cardinalities of missing sets belonging to
  different identities without transporting or using that chain bound.
* The finite-semigroup minimal-idempotent argument establishes unit lifts:
  an idempotent power of a preimage of a target unit must map to the corner
  identity and equal the minimal source identity. The preceding power then
  provides an inverse. Thus no unsupported lifting assumption is imported.
* For each amplification step, the retained set F satisfies `iPi=i`
  because the only bipartite pair with both retained endpoints is precisely
  the newly added pair, absent from the preceding P. The restriction of
  `Q R_H Q`, with `Q=PiP`, is a full relation monoid on F. The smaller
  source corner maps onto it, preserves order reversal, and has the unit
  lifts required by induction. The new idempotent lift maps to identity
  plus the new pair. Its loss is at most twice the original step's loss
  by transport and the positive-power missing-set inequality.
* Uniformly for `h≥129`, there are 4096 such steps and `|F|=h−127≥2`.
  Combining their costs gives `16·64·c≥(64²/2)D(h−127)`, hence
  `c≥2D(h−127)=D(h)`. The interval `2≤h≤128` supplies the base case.
  Finally `D(h)≤2m`, with `m=s+1`, yields exactly the stated bound.

These are the substantive obligations in
`P/sections/diagrams.tex`, `P/sections/nesting.tex`,
`P/sections/amplification.tex`, and `P/sections/automata.tex` already cited
in this audit. I found no circularity, unsupported central replacement
claim, quantifier restriction, or mismatch with the source/complement
automaton conventions in them. This does not promise infallibility; it
states the actual result of an independent mathematical proof audit.

The formal-reproduction agent reports that disk exhaustion prevented a
kernel build and axiom-output run. That is a limitation of the formal
verification evidence, not a discovered counterexample or mathematical
gap. Accordingly the package may accurately describe the upstream result
as an explicitly cited theorem whose handwritten proof and semantic fit
were independently inspected. It must **not** describe this effort as
having reproduced the upstream Lean verification, checked its kernel
axiom dependencies, or formalized the binary follow-on. The available
formal evidence is source/signature inspection only; the tiny computational
checks also remain supplementary.

No mathematical blocker is known to this auditor. Public priority, later
corrections, the binary compiler, and final-package claims remain separate
audits, as before. This addendum does not certify those tasks or alter any
upstream theorem or original audit text.
