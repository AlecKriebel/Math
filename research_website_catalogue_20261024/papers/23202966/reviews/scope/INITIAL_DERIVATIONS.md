# Independent paper-first reconstruction — CLOSED root135 comparison gate

This document was written after personally reading all six actual published PDF pages, all376 controlling TeX lines and all six freshly generated individual page rasters. No foreign scientific body, supplied programme/result, deposited archival audit, current peer scientific opinion or root scientific opinion has been read. The manuscript itself contains author claims about earlier automated audits; those embedded claims are recorded as claims and are not used as evidence. The deposited standalone README and ZIP programme/opinion bodies remain unread at this checkpoint. Source custody documentation, raw schema/namespace metadata and whole-byte hashes were inspected first. Source historical UNREAD/false/null fields are unchanged.

The target is a collection of explicit automata constructions and consequences of two external exponential lower bounds. I separate the internally checkable reductions from the unverified external hypotheses. No novelty, present worldwide openness, external theorem correctness or final disposition is assumed here.

## Exact objects, hypotheses and success criteria

Fix an integer h≥2. H has h vertices and Σ_h consists of all2^(h²) binary relations on H, including the empty relation and identity. Relation multiplication is in path order: a pair p→r lies in RS if a q satisfies pRq and qSr. The empty product is I_H, so ε belongs to L_h, the language of relation words whose product is nonempty.

Let b=h² and encode a relation by all b row-major adjacency bits, bit ph+q being its p→q edge. Concatenation gives an injective map on relation words. K_h is exactly enc(L_h), with its universe fixed as all binary words: words of length not divisible by b are rejected. On divisible lengths, a binary word decomposes uniquely into relation blocks. This exact full-word language, rather than an unspecified valid-code promise, is the object for the cubic source-size proposition and complementation theorem.

The marked machine has one initial state, accepting-state reachability at any position, distinct left/right markers even on ε, moves−1/0/+1, disabled outward marker moves and partial rows. A deterministic row has at most one successor. Time-zero acceptance is allowed by default; positive finite acceptance is discussed separately. Infinite nonaccepting runs do not accept. Ordinary epsilon-free1NFAs consume the entire input before their final-state test. All physical states, including initial and accepting/sink states, count.

Success requires the exact stated source constructions and lower bound, an sb-state two-way pullback preserving the entire machine model, correct use of both actual external theorem hypotheses, full-complement semantics, and the claimed stretched exponential in the cubic binary source size. A surviving internal error or a substantive mismatch with a critical external theorem is a defect of the original claim, not permission to substitute a narrower repaired theorem.

## Family1 — Language semantics and the encoded universe

Every b-bit string specifies a unique relation. Thus the image of Σ_h* is precisely the words of length divisible by b; image words decode uniquely, including ε. A product is nonempty exactly when there is a sequence v0,…,vk with each vi−1 Ri vi. This is a path-existence statement, with arbitrary starting and ending vertices. The product of zero letters is I_H≠∅.

Consequently, {0,1}*\K_h is the disjoint union of malformed-length words and enc(Σ_h*\L_h). No malformed word occurs in the latter image; ε occurs in neither complement. A falsifier would be a malformed accepted source word, an alternative block decoding, or reversed relation multiplication. The row-major/path convention fixes the latter issue explicitly.

## Family2 — Source compiler invariant and all destinations

At phase t of a block, U(p,t) means the incoming vertex is p and no edge has yet been chosen. The U range t<(p+1)h permits skipping all earlier rows and any strict prefix of row p, but forbids skipping its last offset (p+1)h−1. A surviving full-block branch must therefore choose a1 in row p. It cannot choose outside that row because the choice guard is floor(t/h)=p.

Choosing the edge at t=ph+q stores its target q. If another bit remains, the destination V(q,t+1) exists: t+1=ph+q+1≥q+1, and t+1<b. V consumes every remaining bit without making another choice. At the final bit it returns to U(q,0). Choosing the final bit directly returns to U(q,0). This gives exactly one chosen1 per surviving block, and each possible p→q edge can be chosen by a branch.

Induction on complete blocks identifies the set of reachable boundary states U(q,0) with all path endpoints. The first marker nondeterministically initializes every p. The only accepting right-marker rows are boundary states, so incomplete blocks cannot accept. On ε the two markers are adjacent; initialize U(p,0) and then take its right-marker stay into a. This is a finite positive-length accepting run. i is nonfinal; a has no outgoing transitions. Falsifiers include an off-row choice, an out-of-range V destination, a skip of an entire selected row, or a marker row at a nonboundary phase.

## Family3 — Exact combinatorics and ordinary-machine conversion

The U states number h∑_(p=0)^(h−1)(p+1)=(h³+h²)/2. For each q, V has b−q−1 phases, so its total is h³−(h²+h)/2. Their sum is (3h³−h)/2. Adding distinct i and a gives N_h=(3h³−h)/2+2. The quantity is an integer since3h³−h has even parity. For h=2, the families have6 and5 states, giving13 marked states and12 ordinary states.

For the ordinary epsilon-free machine, use U,V plus one new i0. Mark i0 and every U(p,0) final. There is no transition to i0. On the first consumed bit, the outgoing row at i0 is the union of the rows at all U(p,0). Thereafter this is exactly the body-bit computation already justified. ε accepts at i0; a nonempty computation accepts only after entire input consumption at a boundary. This is not an illicit free epsilon branching operation. Its physical count is N_h−1. Falsifiers include mistakenly testing finality before full consumption, retaining extra marker states, or allowing a return to i0 on a malformed length.

## Family4 — Cubic fooling family and marked splicing

Let P_p contain only p→p and z=enc(I_H). For p∈H and0≤t<b define x_(p,t)=enc(P_p)pref_t(z) and y_(p,t)=suff_(b−t)(z)enc(P_p). A matching concatenation is the valid three-block word encoding P_p I_H P_p=P_p, hence accepts. For phases t≠u, the crossed length is3b+t−u. Its nonzero difference t−u has magnitude less than b, so the length is not divisible by b and rejects independently of all bit values. When t=u and p≠r, the middle block remains I_H and P_p I_H P_r is empty, so that crossed word also rejects.

There are h·b=h³ pairs and every off-diagonal crossed pair rejects, which is stronger than the usual one-sided crossed rejection needed for an NFA fooling set. Choose one accepting computation per diagonal word and its control state after consuming x. If two such cuts shared a state, the prefix run of one and suffix run of the other would splice to an accepting crossed computation. A right-only machine's transition rules cannot see absolute input position, so translating the suffix to its new cut is legitimate.

In the marked finite-run model, early acceptance before a right marker cannot occur for this language: append one bit to an accepted valid word and reuse such a finite run, contradicting malformed-length rejection. Every accepting run must therefore traverse each cut before its suffix. Stay moves can be put on one side of a cut; no left moves can return across it. Here each x is nonempty and each y has at least b+1 bits, so no cut is itself the initial or terminal marker. Thus h³ distinct control states are forced in this category too. Falsifiers must break one of these actual splicing hypotheses, not import a two-way fooling-set rule where repeated crossing could invalidate it.

## Family5 — Two-way configuration covering and local table

For an arbitrary binary target with s states Q, attach a phase t∈{0,…,b−1}. On relation body cell j map(q,t) to binary state q at bit position(j−1)b+t+1. A binary stay retains phase and makes a real stay. A right move increments t and stays in the same relation cell unless t=b−1, when phase resets to0 and the real head moves right. A left move decrements a positive t and stays, or at t=0 changes to b−1 and moves to the previous relation cell. All moves still belong to{−1,0,+1}.

Each body step maps to exactly one binary step; there is no extra administrative epsilon step or hidden state family. Looking at a relation symbol can inspect any of its bits because the transition table is indexed by that whole relation letter; the table may be huge, but the claimed resource is states. There are exactly s·b physical states, and determinism is preserved row by row. Falsifiers include an invalid offset at a block boundary, extra reset states, an unnoticed reversal restriction or using a succinct-table computation model instead of ordinary finite-state transition tables.

## Family6 — Markers, empty tape, finite and infinite runs

At a real marker, every phase maps to the same binary marker configuration. Marker rows ignore the incoming phase. A left-marker stay retains it; a right move resets to0. A right-marker stay retains it; a left move sets b−1. Outward moves are disabled. Thus marker phase nonuniqueness does not create a new binary behaviour: every transition from an image configuration lifts from each corresponding phase copy.

For ε the real markers are adjacent, just as the binary markers are adjacent. A left-marker right move reaches the right marker with phase0; a right-marker left move reaches the left marker with phase b−1. Ignoring phase at either marker makes subsequent rows identical. Starting at(q0,0), induction on actual transition count gives both forward mapping and backward lifting of finite runs. Finality depends only on q, so zero-step and positive-step acceptance are preserved with the same run length. Transition-by-transition lifting also preserves infinite runs, but an infinite nonaccepting run adds no finite witness. Partial/missing rows remain missing. This is a direct configuration-cover proof, not a halting assumption.

## Family7 — Contrapositive transfer and full complement

If a binary deterministic target recognizes K_h, pulling it back along enc gives a deterministic relation target recognizing all of L_h. If a binary nondeterministic target recognizes the full binary complement, its pullback recognizes all of Σ_h*\L_h. It need not implement malformed-word acceptance in the pullback: the pullback's inputs are precisely valid relation words. This is restriction of a total recognizer along an injective coding, not a promise theorem and not an equivalence outside codewords.

The two exponential lower bounds are external inputs, not derived by the paper's elementary binary constructions. Before reading their actual bodies, I cannot certify that they quantify over exactly these relation words, allow this target machine model, have no hidden input-length/reversal/acceptance restrictions, or use the stated constants. The precise dependency to inspect is deterministic2^floor((h−2)/31)≤4(s′+2)² under both finite-run conventions and nondeterministic-complement2^floor((h−2)/127)≤2(s′+1) under zero-step acceptance, for every h≥2. A mismatch here is central and cannot be repaired by merely restating a conditional theorem if the claimed unconditional conclusion fails.

## Family8 — Numerical rearrangement and small h

Substitute s′=sh² into the deterministic input. Taking the nonnegative square root yields2^(floor((h−2)/31)/2)≤2(sh²+2), and hence s≥[2^(floor((h−2)/31)/2−1)−2]/h². The complementation input gives s≥[2^(floor((h−2)/127)−1)−1]/h². Negative right sides at small h are allowed and simply vacuous lower bounds; rounding a lower bound on integral s could strengthen it but is unnecessary.

For h≥2, h³≤N_h≤2h³. A fixed positive exponential rate in h survives division by h² and subtraction of constants: taking base2 logs, the loss is only2log2 h+O(1). Thus each target cost is2^Ω(h), and h≥(N_h/2)^(1/3) gives2^Ω(N_h^(1/3)). N_h−1 has the same cubic order. These examples rule out a universal polynomial state bound along this family on the fixed alphabet{0,1}; they do not yield2^Ω(n) in binary source states or a uniform L versus NL separation.

## Family9 — Acceptance conventions and category boundary

To convert a positive-finite-run complementing target to default zero-step reachability, add a new nonfinal initial state with the old initial state's transition rows, retaining old destinations. Every accepting new-machine run has a first transition and then exactly the old computation after that first step. No transition returns to the new state. This costs one physical state before the b-fold pullback, giving2^floor((h−2)/127)≤2((s+1)h²+1), rather than silently retaining the sharper zero-step formula.

Adding a nonaccepting stay-loop sink makes missing legal rows total and costs one source state. Outward marker moves remain disallowed, so totality must mean at least one legal successor per scanned-symbol row, not forced outward moves. Endmarker-only or halting-before-acceptance targets are subclasses of the permissive reachability target model; a lower bound for the permissive class applies to them. The actual external model still needs checking. Read-only targets are different from1-limited machines that can rewrite cells. Bounds on a particular chain proof method are not upper bounds on all possible state lower bounds.

## Family10 — Hypothesis/credit/edition interfaces to verify

The manuscript positively credits earlier adjacency-bit coding rather than asserting a new coding family. The critical comparison is the actual2011 Section5 and2013 Section8 text, including its malformed-block convention and target reversal restriction. A quadratic2026 relation-liveness antecedent, a limitation of a particular chain method, a rewriting1-limited complementation result, and the publicR816 record are different interfaces and must not be conflated. Actual primary bodies, exact editions and publication/creation/release dates must be read after this seal. No exhaustive historical-firstness inference can follow from a bounded search or the author's claimed October6 verification.

## Family11 — Falsification ledger and evidence hierarchy

The internal mechanisms above are uniform paper deductions with explicit adversarial boundary cases: ε, h=2, zero or identity relations, all-one relations, a1 in the first/last permitted row position, incomplete lengths1 through b−1, phase0/b−1 head crossings, marker stays, adjacent-marker crossings on ε, initially final targets, missing rows, deterministic self-loops, nonaccepting infinite loops and positive-run conversion. None requires trusting a supplied simulator or archived audit output. A finite new test could falsify a local construction but could not prove a uniform external exponential obstruction.

The source's support/code/results and archived opinions remain unread here. The separate adversarial lane owns the only native scientific replay. I may later design bounded independent checks from the mathematics, with their results frozen before any supplied scientific-code read, if they resolve a live proof uncertainty. No own numerical or scientific programme has been run at this checkpoint; only ordinary Poppler read/render tools and metadata/hash scripts have run.

## Family12 — Initial status and next gates

The locally explicit constructions have been reconstructed without importing any external scientific interpretation. The indispensable remaining uncertainty is the actual validity/scope of the two pinned upstream exponential inputs and their models, followed by the bounded prior/edition comparisons. This is not yet a final Pass/Deferred verdict. The target's own audit/formal-verification assertions are not substitutes for those checks. The note explicitly disclaims reproduced formal verification and binary formalization, so no such certification is inferred.

The actual printed date is October6,2026; no printed version line appears in any of the six pages or the full controlling TeX. Native version is separately ABSENT. The declared publication is October6 and creation is October7UTC; those are distinct facts. Original native order is README.md,paper.pdf,main.tex,verification.zip. Source unread flags remain historical. Rights will be checked against the actual native metadata and deposited licence/readme after this independent initial seal. Default follow-up is null: there is no justified new publishable follow-up proposal at this checkpoint.

Root135 comparison gate remains CLOSED. Only neutral custody/initial-seal progress may be sent. No scientific finding, partial conclusion or reconstruction from this document is released by its existence.
