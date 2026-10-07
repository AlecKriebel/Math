# Current theorem and validation scope

Status: uniform proofs complete; upstream handwritten arguments independently
audited without a known substantive gap. Both complete-package reviews passed
the exact final candidate04. Production Zenodo publication and tracker
readback are verified; see FINAL_RESULT.md. This live status update follows
publication; the immutable verification ZIP retains its earlier workflow snapshot.

For h≥2, let L_h be nonempty products of all binary relations on h points,
including the empty identity product. Let E_h encode each relation by its
row-major h² adjacency bits. K_h=E_h(L_h), defined on every binary word,
rejects exactly incomplete blocks and nonlive complete-block words; ε accepts.

Theorem: K_h has an endmarked one-way NFA of exactly N_h=(3h³−h)/2+2 states
and an ordinary epsilon-free 1NFA of N_h−1 states. Every ordinary 1NFA for
K_h needs at least h³ states. Every s-state marked binary 2DFA recognizing
K_h satisfies 2^floor((h−2)/31)≤4(sh²+2)². Every s-state marked binary 2NFA
recognizing the full complement {0,1}*\K_h satisfies
2^floor((h−2)/127)≤2(sh²+1). Both lower bounds imply 2^Ω(N_h^(1/3)).
The complementing target may be nondeterministic and use unrestricted
left/right/stay moves, partial transitions and infinite nonaccepting runs.
Positive finite-run complementation has the manuscript's one-state variant.

The source compiler and h³ fooling set are proved independently of the
upstream exponential bounds. The target compiler uses exactly sh² states,
with step-for-step finite and infinite run correspondence. The base lower
bounds are external OpenAI family-129 results, attributed rather than
reproved in the note. Separate agents checked both original proof mechanisms,
actual Lean declarations and semantic agreement. No substantive gap was found.

Formal limitation: source hashes/signatures/lexical scans were checked,
but kernel compilation, #print axioms and Comparator validation were not
reproduced because local disk exhaustion interrupted dependency acquisition.
There is no claim of reproduced formal verification or binary formalization.
This limitation is disclosed in the manuscript and package. Handwritten
proof audits constitute the dependency validation basis.

New scope: fixed-binary consequences, explicit complete-semantic compilers,
quantitative cubic source expansion, and strict-block cubic one-way lower
bound. Binary coding is older machinery, and all exponential obstructions
are inherited. No first claim, 2^Ω(n) binary-source exponent, L≠NL, or stronger
uniform complexity separation is made.

All required complete-package reviews, clean-package reproduction, production
Zenodo publication and read-back-verified spreadsheet entry are complete.
The DOI is 10.5281/zenodo.23202966, resolved to the published record.
Tracker range: Math Puzzles!A35:D35. Exact receipts are retained separately.
