# Independent adversarial audit: problem 3341 / OPG-37448

Audit date: 2026-10-04 UTC. Target: rank 599, “MSO alternation hierarchy over pictures.”

## Verdict

**PASS for the conservative classification `unsolved`, five approaches exhausted (`5/5`), with one small factual wording correction and two recommended source-precision additions.** No complete solution, later solved status, new discovery, or polynomial-hierarchy separation is certified. No fatal mathematical flaw was found in the release's partial results.

The strongest unconditional mathematical result is a valid reconstruction of the known first alternation separation on binary square pictures. The higher square and balanced hierarchy questions remain unproved by this package. Proposition 7 gives a sound conditional route from polynomial-hierarchy separation; it does not establish an equivalence or unconditional separation.

This audit was independent of the authoring worker. No helper agent was used. The release was not modified. No remote writes, repository mutations, external communications, or source redistribution were performed.

## Frozen object and integrity

Audited directory: `../release`.

Frozen manifest SHA-256:

`f7b7257998fdaa783353f008e3364078176153416f2a264189932bfa885bb7ea`

All seven manifest entries verified before and after review. All six paths recorded in the private freeze record, including the release manifest itself, also match their recorded hashes. There are exactly seven payload files plus the manifest in the release, and no source PDFs or raw private corpus snapshots. The replay was run from `rerun/`, not in the frozen directory, because the supplied script writes its output file.

`evidence/freeze-verification.json` records each expected and observed hash. These integrity checks establish identity with the frozen object; they do not establish correctness of its proofs.

## Proof-by-proof examination

### 1. Vocabulary, quantifiers, and balance domains

The write-up consistently uses pixels as elements, directed immediate H/V adjacency, and letter predicates. Its row/column and diagonal constructions do not smuggle in built-in coordinate equality, numerical order, arithmetic, or higher-arity set variables. Boundary predicates are FO definable in the stated vocabulary.

For fixed C and d, Sq is contained in B(C,d), and the relative-definability monotonicity lemma is valid. If a simpler formula agreed with the proposed witness throughout a larger domain, it would agree on squares. This does not require an FO definition of Sq. On nonsquares the same formula is an extension of the square witness, not necessarily the literal rectangular mirror language.

The source alignment requires care. The OPG question uses polynomial/linear relatedness informally. Gardy's slide 22 explicitly lists square languages and exact formats w=c h and w=P(h), while slide 23 states a folding/unfolding equivalence for linear balance. The release correctly warns that exact-format classes and B(C,d) are different and does not rely on an unproved folding equivalence. It should nevertheless say explicitly which precise conditions Gardy uses. In particular, Sq is not a subdomain of the exact class w=c h when c>1, so the monotonicity lemma alone must not be advertised as a transfer to each such class.

### 2. Tower restriction and FO finiteness

Proposition 1 is correct. Eventual growth beyond C h^d excludes every sufficiently large height from B(C,d); only finitely many formats and finite-alphabet pictures remain. The lower bound using binomial(h,d+1) proves the asserted exponential-versus-polynomial limit. Complete finite atomic diagrams give an FO definition of the remaining finite picture language.

This is a route-specific obstruction. It does not rule out other balanced encodings or adaptations of unrestricted-grid lower bounds. The release maintains that limitation.

### 3. Blank padding and lack of an automatic converse

Relativization to the nonblank active rectangle preserves every monadic block on correctly padded inputs. For each quantified set, the map S to S intersect Active is surjective, and the translated subformula depends only on that restriction. Structural induction therefore works for both quantifier polarities, including alternation.

The converse obstruction is also correct: a one-dimensional c-copy interpretation creates at most c h w elements, whereas the square needs w squared. Quotients cannot increase that bound. An interpretation on d-tuples would turn a monadic output variable into a d-ary relation on the source, so it gives no automatic MSO inverse. The artifact correctly distinguishes this counting argument from a universal impossibility theorem. The fresh blank symbol and well-formed-padding promise are essential and are stated.

### 4. Six-set EMSO mismatch certificate

All six quantified objects D,E,T,R,X,Y are unary sets. H-invariance together with exactly one left-boundary point makes a selected set exactly one whole row; the vertical/top-boundary version makes one whole column.

For either diagonal, every marked point has a predecessor until reaching the top row. It must therefore descend from the unique selected corner. Every nonbottom marked point also has its next diagonal successor. On squares these requirements force exactly the intended diagonal, including side one. On nonsquares the terminal-boundary requirement prevents a model; no nonsquare existence is used.

T selects a diagonal index j, so its intersections with D and E lie in columns j and n+1-j. X and Y select exactly those columns, and R chooses a row with different bits there. Conversely, every asymmetric square supplies the six witnesses. When n is odd, selecting the central column compares a cell with itself and cannot create a false mismatch. Side one correctly has no mismatch.

### 5. Tiling splicing lower bound

The use of EMSO recognizability is appropriate. A presentation of a putative sentence that agrees with Mirror on squares may accept anything off the square domain; every picture used in the contradiction is nevertheless square.

There are 2^(2r^2) distinct symmetric binary squares built from arbitrary 2r-by-r left halves, but at most g^(4r) two-column cut signatures of accepting lifts. The strict inequality follows from r>2 log2(g). If two distinct halves have lifts with the same signature, splicing the left lift of one to the right lift of the other preserves every local 2-by-2 tile. Tiles crossing the seam, including tiles touching the top/bottom exterior border, are covered because both seam columns match. All other tiles are inherited from one original lift. The fixed exterior border also handles corners and outside edges.

Projection of the splice is [A | reverse(B)], which is symmetric exactly when A=B. The pigeonhole pair has A different from B, yielding the required contradiction. The lift alphabet is necessarily nonempty under the assumption that all symmetric squares are accepted; g=0 is therefore no omitted countercase.

Thus Mirror is in Pi_1 but not Sigma_1 on squares. Its complement is in Sigma_1 but not Pi_1; adding a dummy existential block gives Sigma_1 strictly contained in Sigma_2. The relative-domain transfer to every stated B(C,d) is valid. This remains a known first-level result, not a resolution of the arbitrary-level question.

There is a harmless signature detail worth recording: the locally inspected Grandjean–Olive–Richard source uses cyclic successor functions and boundary predicates. The direction needed here follows by replacing H(x,y) with succ_h(x)=y and not Right(x), and similarly for V. This embeds the release's EMSO formulas into that source's signature without changing the set prefix. The recognizability theorem then applies. A converse FO definition of wraparound in H,V is unnecessary. See CORRECTIONS.md for an optional addition making this bridge explicit.

### 6. Boolean closure and projection

Proposition 5 is correct. In each DNF conjunction, independent existential prefixes may be placed before independent universal prefixes because their matrices have no other term's bound variables. Finite disjunction preserves a Sigma_2 form: if both independent universal matrices have counterexamples, the paired counterexample defeats their disjunction; if one is universally true, the disjunction is universally true. The same construction applied to the complement gives Pi_2.

Uniform closure under color projection across alphabet expansions would let B Sigma_1 absorb existential monadic quantification, and complement closure then handles universal monadic quantification. Induction along a monadic prefix gives the claimed collapse condition. The artifact does not prove that closure, and failure of a single such closure alone would not provide every higher separator. No false MSO collapse follows from Proposition 5.

### 7. PH upper bound and tableau reduction

Proposition 6 is correct for explicit N-cell inputs and each fixed formula: a fixed number of N-bit set vectors, followed by fixed-FO brute-force evaluation, lies in the matching PH level. The degree of the final polynomial is allowed to depend on the formula.

Proposition 7 has the required uniformity. For a fixed verifier and k, a deterministic one-tape simulation has a polynomial worst-case time/space bound over every assignment of the prescribed witness lengths. The reduction chooses a square side exceeding those bounds. The output contains polynomially many cells, and its finite alphabet and sentence depend on the verifier and k, not the input.

A legal initialized row evolves deterministically through a finite radius-one transition rule. A one-head invariant need not be imposed separately on every row: it follows from the legal top row and transition induction. Exact one-symbol-per-cell constraints plus a total transition rule give one and only one valid full tableau for every witness assignment. The one-sided left boundary and the unreachable right boundary can be encoded with fixed local cases. Absorbing accepting/rejecting states make last-row acceptance faithful.

For an existential last block, existentially quantifying the unique tableau and requiring Valid AND Accept is correct. For a universal last block, universally quantifying it and using Valid IMPLIES Accept is also correct: invalid assignments are harmless and the existing unique valid tableau enforces the verifier answer. Merging these sets with the last X block preserves dependency and alternation. This is not an illicit existential witness after a universal block.

The unique-tableau claim is a proof obligation, not established by the small parity tests. It is satisfied by the construction just reviewed. No full Turing-machine-to-FO compiler was implemented or independently executed, and the release accurately says so.

### 8. Binary coding

The code works on the reduction's promised outputs. Ring centers are FO-recognizable by a fixed neighborhood predicate. All runs of three adjacent 1s arise in ring rows; isolated payload bits cannot create such a run. Candidate ring patterns are separated between blocks by sufficiently wide zero strips, so only the intended centers satisfy the marker formula. Reading payload offsets and taking fixed-length H/V paths therefore recovers the original structure. Relativization to marker cells preserves both monadic quantifier polarities by the same surjectivity argument as padding.

The sentence that blocks have zero margins is literally inaccurate if it means all four block edges: the ring uses row 1 and column 1. The construction does have ample zero strips between neighboring markers and payload regions. Replacing that phrase fixes the prose without moving any pixels, changing the code, or altering the proof. This is the only directly falsified factual assertion found.

### 9. Conditional consequence

If the square Sigma_k and Sigma_(k+1) classes coincide, every Sigma_(k+1)^P language can be reduced into a square Sigma_(k+1) sentence, replaced by its hypothetical Sigma_k equivalent, and decided in Sigma_k^P. Polynomial-time reductions preserve the complexity class. The argument is valid over binary pictures because of the fixed block code.

This proves the one-way implication from PH strictness to square logical strictness (and thence the stated balanced superdomains). It does not infer PH strictness from a logical separation. In particular, low algorithmic complexity of Mirror is compatible with its logical lower bound. The release avoids claiming equivalence.

## Source check and status limits

The original OPG main page was readable at the www URL during this audit; the non-www and SFU mirror routes still failed. Its displayed question, attribution, 2012 date, first-level context, and proposed Boolean-EMSO possibility agree with the pinned source record. No actual posted comment thread or solution update was displayed. This is evidence about the accessible page, not proof of a literature-wide absence of solutions.

Gardy's primary slides were readable as PDF text. Their exact-format balance definitions and stated folding result must remain distinct from B(C,d). Their mirror example has n-by-2n format; the release supplies its own square proof rather than pretending the slide's example is literally the same language.

The private Grandjean–Olive–Richard PDF/text hashes match the freeze. Its Theorem 2.5/2.6 and associated definitions support the recognizability theorem used here; its coordinate-structure hierarchy discussion is not a balanced-pixel resolution. The MST 2002 publisher abstract again supports unrestricted grid strictness and iterated-exponential format witnesses. The full MST article was not downloaded or independently re-proved in this audit.

A bounded fresh title/balanced/square literature search found no verified later full resolution. Search coverage was noisy and incomplete. Neither that negative result nor the original page's lack of an update proves the question is currently open in an absolute sense. The proposed `unsolved` is the status of this five-approach effort, and `already_solved_verified=false` is appropriate.

Verified primary links:

- [Original OPG page](https://www.openproblemgarden.org/op/mso_alternation_hierarchy_over_pictures)
- [Gardy's slides](https://lsv.ens-paris-saclay.fr/~gardy/Talk/balancedMSOpicturelangages.pdf)
- [Grandjean–Olive–Richard preprint](https://arxiv.org/abs/1201.5853)
- [Matz–Schweikardt–Thomas publisher record](https://www.sciencedirect.com/science/article/pii/S089054010292955X)

## Reproduction and independent controls

1. The supplied Python control script was copied unchanged to `rerun/controls/check.py` and run there. Its output is byte-for-byte identical to the frozen CONTROL_RESULTS.json (SHA-256 `79abc831d84ae92ab9549f2bbed5cee23c977b84de9c48708cfc9d9a63c9dc97`). It reports 66,066 binary squares, 4,096 compatible splice pairs, and 372 block-coded pictures.
2. `independent_checks.py` uses separately written tests. It exhaustively evaluates the diagonal set clauses on rectangles through 4-by-4, checks 66,066 binary squares, tests 864 nonbinary arbitrary-cut splices including boundaries, checks 65,812 alternating truth tables through four one-bit blocks, and tests 192 broader binary-code layouts with payload widths 1 through 12. All passed.
3. The independent code explicitly confirms that the top/left block margins are not all zero. This supports correction C1 rather than undermining marker uniqueness.
4. These are bounded controls, not an enumeration of all formulas or tiling systems, not execution of a general tableau compiler, and not a certificate of the missing infinite hierarchy theorem.

## Publication and queue gate

The release consistently records five distinct approach mechanisms and an unsolved outcome. Its status proposal preserves exhaustion at 5/5 and does not reset the budget. No Findings-field mutation is authorized by the package. This audit does not revalidate the entire current repository, PR state, remote HEAD, or latest queue; the parent must perform any live publication gate separately.

Recommended disposition: retain `unsolved`, `5/5`, no full-resolution or novelty upgrade. Apply the small prose correction and source clarifications in a new version if publication is to incorporate them, then regenerate that version's manifest. Preserve this frozen version and this audit for provenance. No alteration was made here.
