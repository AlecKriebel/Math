Theoretical computer science · Automata · Research note


# Binary consequences of relation-liveness automata lower bounds


Alec Kriebel · ORCID: 0009-0001-9320-500X


6 October 2026 · Unrefereed preprint


A finite automaton can describe a language compactly yet require many more states when its nondeterminism is removed, or when the language is complemented. This note transfers two attributed relation-liveness lower bounds to a single binary alphabet, with explicit compilers, exact state counts and a precise treatment of every binary word.




## Read the paper


Open the searchable PDF



The reader displays the original deposited paper. Open the PDF directly for your viewer’s search and navigation.


Original downloads: README · PDF · LaTeX source · Verification ZIP · BibTeX


Persistent record: doi:10.5281/zenodo.23202966.




## Abstract


We give explicit fixed-binary-alphabet consequences of OpenAI’s two relation-liveness lower bounds. Encoding each relation on h points by its h² adjacency bits gives a language recognized by a one-way nondeterministic automaton with Nₕ=(3h³−h)/2+2 states. Every equivalent two-way deterministic automaton, and every two-way nondeterministic automaton for its full binary complement, requires 2^{Ω(h)}=2^{Ω(Nₕ^(1/3))} states. We specify all transition rules, including an exact sh²-state pullback for an s-state binary target. The binary language rejects incomplete blocks; a fooling set proves that its one-way nondeterministic state complexity is Θ(h³). The exponential obstructions are inherited from the two upstream theorems; binary adjacency coding is established machinery.




## One binary language, including malformed words


Fix an integer h ≥ 2, let H = {0,…,h−1}, and let Σₕ be the alphabet of all relations on H. A relation on H is encoded by its h² adjacency bits in row-major order: bit t = ph+q records whether the edge (p,q) is present. Relation products are composed in path order, so a sequence is live when some path survives through all its relations. The empty product is the identity relation.


b = h²
Lₕ = {relation words whose product is nonempty}
Kₕ = enc(Lₕ) ⊆ {0,1}*;  enc(ε) = ε.


Every complete b-bit block codes exactly one relation. The language Kₕ is defined on all binary words: it rejects every word whose length is not divisible by h², and otherwise tests the decoded product for liveness. It accepts ε. This strict rejection of incomplete blocks is part of the result, rather than a promise that inputs will be well formed.




## An exact source compiler and its cubic cost


The marked one-way nondeterministic source has one nonaccepting initial state, one accepting state, and two families of scanning states. U(p,t) retains the preceding vertex before choosing an outgoing edge; V(q,t) retains the selected next vertex. Their ranges are


U(p,t): 0 ≤ p < h, 0 ≤ t < (p+1)h
V(q,t): 0 ≤ q < h, q+1 ≤ t < h²
Nₕ = (3h³−h)/2 + 2 marked states
ordinary epsilon-free 1NFA: Nₕ−1 states.


At the left marker the source chooses a starting vertex. Within each block, a surviving branch must choose exactly one 1 in that vertex’s row; its final row position cannot simply be skipped. The chosen column becomes the next block’s vertex. Every body-bit move goes right, and only complete block-boundary states can take the accepting stay at the right marker. Thus partial blocks reject, while ε has a two-transition accepting run. The ordinary epsilon-free source combines the first-bit choices in one initial final state and tests acceptance only after consuming the entire word.


A matching lower bound uses h³ incompatible prefix–suffix cuts, one for each vertex and bit offset. Diagonal pairs encode a live singleton–identity–singleton product. Different-offset crosses have malformed lengths; equal-offset, different-vertex crosses have empty products. Splicing runs with the same cut state would accept a forbidden cross.


This proves an h³ lower bound for ordinary one-way NFAs and for marked right-only sources, including stays in that right-only model. It is not a cut-state lower bound for arbitrary two-way machines. Consequently this particular strict-block language has one-way nondeterministic state complexity Θ(h³); the claim does not assert optimal source costs across all binary encodings.




## The target machine model


All states are counted. The head begins on the left of two distinct endmarkers, which remain distinct and adjacent on empty input. Transitions may be partial and may move left, stay, or move right. Outward moves at markers are disabled. A deterministic target has at most one successor per state-symbol row; a nondeterministic target may have several.


Acceptance means reaching an accepting state by a finite run, initially allowing zero transitions. Missing transitions and nonaccepting infinite runs do not accept. The pullback also preserves positive-run acceptance. There is no hidden halting, reversal, word-length or writable-tape restriction.




## A pullback with exactly sh² states


Given an s-state binary target, the relation-alphabet pullback uses states (q,t), where q is an original target state and t ranges from 0 to b−1. At a relation cell it reads the adjacency bit at phase t. Its simulation rules are:



Body-cell simulation, with the original new state q′ in every row


 | Binary move | New phase | Relation-tape move



 | stay | t | stay


 | right, t < b−1 | t+1 | stay


 | right, t = b−1 | 0 | right


 | left, t > 0 | t−1 | stay


 | left, t = 0 | b−1 | left



At each marker the original marker row is used independently of the stored phase. Marker stays retain the phase; inward moves reset it to 0 at the left marker and b−1 at the right marker. Missing rows remain missing. The initial state is (q₀,0), and (q,t) is accepting exactly when q is accepting.


A relation-cell configuration at cell j maps to binary position (j−1)b+t+1. Each transition corresponds to one binary transition, and every binary transition lifts from every corresponding preimage. Marker phases may be nonunique without introducing an accepting path. The argument covers adjacent markers on ε, both zero-step and positive finite acceptance, stays, partial rows, arbitrary revisits and nonaccepting infinite runs. Determinism and finite-run lengths are preserved. The exact state count is sh², with no extra marker-state family.




## The inherited binary lower bounds


The two exponential engines are OpenAI’s attributed Math Release preprints on deterministic simulation of one-way liveness and on nondeterministic complementation. Applying their full relation-alphabet inequalities to the pullback gives the following bounds for every h ≥ 2.


If an s-state marked two-way deterministic automaton recognizes Kₕ, then


2^(⌊(h−2)/31⌋) ≤ 4(sh²+2)²
s ≥ [2^(⌊(h−2)/31⌋/2−1) − 2]/h².


If an s-state marked two-way nondeterministic automaton recognizes the complement of Kₕ in all binary words, under zero-step finite acceptance, then


2^(⌊(h−2)/127⌋) ≤ 2(sh²+1)
s ≥ [2^(⌊(h−2)/127⌋−1) − 1]/h².


The full complement is the disjoint union


{0,1}* ∖ Kₕ
  = {x : h² does not divide |x|}
    ∪ enc(Σₕ* ∖ Lₕ).


The malformed words belong to the binary complement, while the pullback sees every valid encoding of a dead relation product. It therefore recognizes the entire upstream complement. ε is absent from both complements. Restricting the complement to a well-formed-input promise would change the statement.


For a positive-run complementing target, one new nonaccepting initial copy converts the target to zero-step acceptance. The explicit variant is 2^(⌊(h−2)/127⌋) ≤ 2((s+1)h²+1). The displayed deterministic inequality already covers both finite-run conventions. Requiring total rows can be handled by a nonaccepting sink; targets that must halt or accept at the right marker are subclasses of the stated model.


Since h³ ≤ Nₕ ≤ 2h³, both target costs are 2^{Ω(h)} = 2^{Ω(Nₕ^(1/3))}. Polynomial factors and fixed subtractions do not change this asymptotic statement; some small-h numerical lower bounds are simply vacuous. Thus neither simulation nor complementation admits a polynomial state bound on this one fixed alphabet.


The exponent is proportional to the cube root of this binary source size. The note does not assert 2^{Ω(Nₕ)}, a uniform separation such as L ≠ NL, or a small transition-table algorithm. Relation-alphabet pullback tables can be large. The contribution is the explicit transfer and exact language/model accounting, not an independent proof of the upstream exponential obstructions.




## Earlier work and the scope of the contribution


Sakoda and Sipser established the classical deterministic-simulation problem for two-way nondeterministic automata. Binary adjacency coding is established machinery: Kapoutsis’s 2011 conference treatment and the author preprint linked with the 2013 journal work discuss binary one-way liveness for deterministic targets with few reversals. The latter linked body is an October 2011 author preprint; journal pagination is a separate bibliographic reference.


The public TheoremDB R816 construction uses a different separator/two-bit encoding, a different off-canonical total language and a linear-size binary source, with an inherited quadratic lower bound and a deterministic macro pullback. It is self-reported, source-only context. It neither supplies the two exponential engines used here nor establishes present worldwide openness. Different source costs for a different language do not contradict the cubic lower bound for this exact strict-block language.


Adeogun and Kapoutsis supply the prior quadratic unrestricted deterministic comparison. In their limitation preprint, the connectivity-chain ceiling is proved as Theorem 2; the general-property extension is stated as Theorem 1 with its proof deferred. That restriction concerns a particular method, not all possible lower-bound arguments. Guillon, Prigioniero and Taheri’s polynomial complementation theorem targets 1-limited automata that may rewrite cells using common guessed annotations. It is not a small read-only 2NFA for the full unannotated complement.


The two actual exponential inputs are credited to OpenAI at the pinned source commit adc7f1241b42e322a6451854ab7e4b4c146bf78a. Their manuscript dates and public release dates are distinct. No independent resolution of the base conjecture, exclusive historical priority, invention of binary coding, or exhaustive current-openness claim is made.



- OpenAI, An exponential two-way deterministic state lower bound for one-way liveness, Math Release preprint, Theorem 1.1. Pinned manuscript.


- OpenAI, An exponential state lower bound for two-way nondeterministic complementation, Math Release preprint, Theorem 1.1. Pinned manuscript.


- W. J. Sakoda and M. Sipser, Nondeterminism and the Size of Two Way Finite Automata, STOC 1978, 275–286. DOI.


- C. A. Kapoutsis, Nondeterminism Is Essential in Small 2FAs with Few Reversals, ICALP 2011, Section 5. DOI.


- C. Kapoutsis, Nondeterminism Is Essential in Small Two-Way Finite Automata with Few Reversals, Information and Computation 222 (2013), 208–227. Journal reference; the linked author-preprint context above concerns its Section 8.


- K. Adeogun and C. Kapoutsis, A Quadratic Lower Bound for 2DFAs against One-Way Liveness. Version 2.


- K. Adeogun and C. A. Kapoutsis, Unrestricted 2DFA Simulation of 1NFAs: A Quadratic Limitation to a New Lower Bound. Version 2.


- B. Guillon, L. Prigioniero and J. Taheri, Polynomial Complementation of Nondeterministic Two-Way Finite Automata by 1-Limited Automata, STACS 2026, 48:1–48:18. Published article.


- TheoremDB, R816, The one-way-liveness bound transfers to a fixed binary alphabet. Public record; self-reported context, without inferred peer-review status.





## Verification and research status


The uniform arguments are written in the paper. The supplementary exact and tiny-instance computations support reproducibility and falsification; they do not replace those proofs or establish the inherited upstream lower bounds by finite sampling. Nonaccepting loops are handled through configuration reachability in the supplied simulator.


Saved optimized Python output alone is not verification of assert-based checks, because optimization removes those assertions and calls within them. The historical build receipt pins an earlier TeX body and does not certify a fresh build of the deposited sources. The original paper, TeX and supporting files are supplied unchanged.


No reproduced upstream Lean kernel build, axiom printing or Comparator validation is claimed, and the binary results are not formalized. The attributed mathematical inputs rest on their written proofs and stated models.


AI tools were used extensively in research, drafting and verification. This is an unrefereed preprint and has not undergone conventional human peer review or refereeing. Automated adversarial reviews are not external human peer review. Attribution to OpenAI does not assert an affiliation or coauthorship.


Professional collaboration on these contributions is welcome. Independent proofs, precise corrections and applications with explicit hypotheses are useful contributions; credit should reflect actual work.


The note and its authored supplementary materials, including code, are available under Creative Commons Attribution 4.0 International. Referenced third-party works retain their own rights.




## Citation


Alec Kriebel (2026). Binary consequences of relation-liveness automata lower bounds. Zenodo. https://doi.org/10.5281/zenodo.23202966. Download BibTeX.




Original Zenodo deposit description


This complete original description differs from the printed abstract and is reproduced separately.


Explicit fixed-binary-alphabet consequences of OpenAI's two relation-liveness lower bounds. A strict h-squared adjacency-block language has a one-way nondeterministic source with (3h^3-h)/2+2 endmarked states, and an ordinary epsilon-free source with one fewer state. Equivalent two-way deterministic automata and two-way nondeterministic automata for its full binary complement require 2^Omega(h), hence 2^Omega(n^(1/3)) in the cubic source size. The note gives exact transitions, an sh^2-state pullback, all-word complement semantics, and an h^3 fooling-set source lower bound. The exponential obstructions are inherited from OpenAI; binary coding is established machinery, attributed to earlier work. AI tools were used extensively. This preprint has not undergone conventional human peer review or refereeing. Automated proof and package audits are documented. Upstream Lean build, axiom printing and Comparator validation were not reproduced due local disk exhaustion; neither reproduced formal verification nor binary formalization is claimed.
