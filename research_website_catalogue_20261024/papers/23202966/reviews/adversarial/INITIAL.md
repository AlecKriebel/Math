# Paper-first independent reconstruction — record 23202966

This document precedes exposure to any foreign scientific primary body, supplied scientific program, expected scientific result, or archived/current review opinion. The review comparison gate is closed. This is extensive AI review, not human peer review or reproduced formal certification. The published target is **Binary consequences of relation-liveness automata lower bounds**, Alec Kriebel, printed October 6, 2026. No printed version is stated; the native API version field is absent, not version 1.0. Source READY historical unread flags are preserved unchanged and do not describe this later reading.

## Exact claim and success conditions

For every integer h >= 2, put H={0,...,h-1}, b=h^2, and let Sigma_h consist of all binary relations on H. Relation multiplication is in path order. L_h contains exactly the words whose product is nonempty, including the empty word because its product is I_H. Encode each relation by its row-major b adjacency bits. K_h is enc(L_h), as a total language over {0,1}*, rejecting lengths not divisible by b.

The local claims are: a marked right-moving source with N_h=(3h^3-h)/2+2 states; an ordinary epsilon-free source with N_h-1 states; an h^3-state lower bound for every ordinary or marked right-only source; an exact s b-state pullback from any s-state binary read-only 2NFA to a relation-alphabet 2NFA, preserving determinism and finite accepting run length. The main target claims then substitute that pullback count into two separately cited exponential obstructions, obtaining

2^floor((h-2)/31) <= 4(s h^2+2)^2,

2^floor((h-2)/127) <= 2(s h^2+1).

These imply target state costs 2^Omega(h)=2^Omega(N_h^(1/3)), and preclude a polynomial bound for the stated simulation/complementation problems on one binary alphabet. The paper does not claim 2^Omega(n) for n source states, L != NL, small uniform relation transition tables, a new binary coding invention, or a new proof of the two external exponential theorems.

Success requires the uniform local constructions to be correct in exactly the stated machine model; the external theorems to hold with the claimed language, quantifiers, constants, and conventions; and the novelty/credit/verification claims to survive focused examination of their actual primary sources. A finite checker pass alone cannot establish either the local universal claims or the external obstructions. A mismatch in an essential external hypothesis blocks the unconditional theorem even if every binary reduction step is valid.

## Family A: source compiler reconstructed from first principles

At a boundary, the U(p,0) branches correspond to possible current vertices p. At an offset t before an edge is chosen, U(p,t) can skip bits only through the end of row p minus its last position. A 1 at offset p h+q permits choosing that outgoing edge and retaining q. At a nonlast bit this enters V(q,t+1); at the very last bit it returns directly to U(q,0). V merely counts the remaining block positions, retaining q. Consequently a branch survives a complete block if and only if it selects precisely one edge in the row of its old vertex. The set of boundary vertices is therefore propagated by the decoded relation. No skip can carry U past its row without an edge choice; no V can become a boundary early. Only U(p,0) has a right-marker accepting move.

Starting the head on the left marker in nonfinal i supplies all p; after that first move the empty input is already at the distinct right marker and accepts by the final stay. In the ordinary source, replace i and the separate final state by one final start state whose bit row is the union of all boundary bit rows. All nonempty words then behave like the marked source after the first consumed bit, while epsilon accepts directly. No transitions enter this replacement start.

The U count is h sum_{p=0}^{h-1}(p+1)=(h^3+h^2)/2. The V count is sum_q(b-q-1)=h^3-(h^2+h)/2. Together these give (3h^3-h)/2 internal states, plus the two marked states. For h=2 the count is 6+5+2=13, with ordinary count 12. These are constructed counts, not assertions of exact minimality. The separately proved lower bound gives the order only.

Falsification targets: h=2; row p=0 and p=h-1; last bit of a row; final bit of a block; all-zero relation; first and last diagonal entries; partial blocks; empty input; a branch that skips every bit in its row; accidental return to U(q,0) before a full block. Independently compare raw binary membership against full relation multiplication and against a literal transition-system implementation. An intentionally malformed-length-ignoring recognizer must be rejected by the control.

## Family B: state lower bound by incompatible cuts

Let P_p={(p,p)}, and let z encode identity. Define x_(p,t)=enc(P_p) pref_t(z) and y_(p,t)=suff_(b-t)(z) enc(P_p), for all p and 0<=t<b. There are h b=h^3 pairs. The matching concatenation has exactly three blocks and product P_p I P_p=P_p, so accepts. A crossed concatenation with t != u has length 3b+t-u. Since 0<|t-u|<b, this is malformed. A crossed concatenation with t=u and p != r has product P_p I P_r=empty. Thus every diagonal is in K and every off-diagonal cross is outside K, a stronger property than the usual one-sided fooling-set criterion.

Choose an accepting run of each diagonal. The state after its x prefix must differ for all pairs: a collision would splice a prefix and suffix into a forbidden crossed accepting computation. For marked right-only machines, an accepting computation cannot stop before reaching the right marker, because then the identical finite computation would accept a one-bit extension of its accepted, well-formed input. The right-only run must therefore traverse the cut and can be spliced there. Stays can be included on one side consistently. Epsilon transitions, if permitted for an ordinary NFA, can likewise be assigned at the cut and do not invalidate the usual argument.

Critical dependency: malformed-word rejection does real work. If another binary-liveness definition accepts unfinished blocks or has a different coding, the cubic lower bound need not transfer. Check t=0 and t=b-1 explicitly, and do not replace this total language by a promise problem.

## Family C: exact local lifting for arbitrary targets

Use states (q,t), q in the target's s states, 0<=t<b. Over a relation R, read the encoded bit at t. A simulated stay preserves t and the real cell. A simulated right move increments t and stays on the relation cell unless t=b-1, in which case it resets t to 0 and moves one cell right. A simulated left move decrements t and stays unless t=0, in which case it sets t=b-1 and moves one cell left. The target q transition is retained in every case. Final states depend only on q.

On a k-letter relation word, a body configuration ((q,t),j) maps to binary position (j-1)b+t+1 with state q. All phases at the left and right relation markers map to the corresponding binary marker. At a marker, target rows are independent of phase: stays retain it, movement from left marker sets phase 0, movement from right marker sets phase b-1, outward movement is disallowed. This produces a transition-preserving map in both directions: every pullback transition projects, and every target transition lifts from every matching pullback configuration. The initial state maps correctly, including empty input where the two distinct markers are adjacent. Induction gives equal finite run lengths and acceptance; zero-length and positive-length semantics follow separately. Determinism is preserved row by row, since each pullback row reads one particular binary row.

Potential attack points: phases at the markers are many-to-one, so prove lifting from each one rather than pretending the configuration map is injective. On empty input, a phase b-1 or 0 after a marker crossing must remain harmless. Include a target whose initial state is final, a partial target with no transition, stays, leftward block crossings, repeated marker visits, self-loops, nonaccepting cycles, and nondeterministic mixtures. Test the local configuration graphs independently of global language acceptance. Finite tests are supplementary to this uniform lifting argument.

## Family D: full complement and asymptotic transfer

Fixed length b coding is a bijection from relation words onto binary words of length divisible by b, including epsilon. Therefore K's full binary complement is the disjoint union of malformed lengths and enc(Sigma_h* minus L_h). For every relation word, the pullback sees a valid codeword; it recognizes the complete upstream complement, rather than only a subset. Empty input belongs to K and to L, hence neither complement contains it.

Assuming the two external inequalities with precisely the claimed semantics, substitute s'=s h^2. The deterministic square root gives s h^2+2 >= 2^(floor((h-2)/31)/2-1). The nondeterministic inequality gives s h^2+1 >= 2^(floor((h-2)/127)-1). Rearrangement matches the displayed formulas. Their numerators can be negative for small h; the nontrivial claim is asymptotic, so no small-h positivity should be inferred. Floors, a polynomial denominator h^2, and constant subtractions do not destroy an exponential in h. For h>=2, h^3<=N_h<=2h^3, so h and N_h^(1/3) are within constants.

For positive-run complement acceptance, a fresh nonfinal initial state copying the old initial row, with all destinations old states, converts precisely the old positive-run language to zero-step acceptance at a cost of one state. This check is separate from the target pullback. Total rows can be completed with a rejecting sink if stays are allowed. Right-marker-only and halting-acceptance targets are subclasses of the larger target class, so a lower bound for the larger class applies. Whether the upstream formulations actually include these conventions must still be read in the native primary material.

## Family E: external dependencies, originality, disclosure

The two OpenAI theorem bodies at exact pin adc7f1241b42e322a6451854ab7e4b4c146bf78a have not yet been read. The target's quotations are hypotheses for this initial reconstruction, not independently established external facts. The exact state constants, alphabet/language definition, finite-run semantics, read-only restriction, markers, stays, initial/final states, word universe, and h range all need comparison. If the source proofs require an additional unsupported theorem equivalent to their central lower bound, that route is blocked rather than repaired by restating the same difficulty.

The manuscript openly credits binary adjacency coding to Kapoutsis, discusses a public TheoremDB antecedent with only inherited quadratic strength, and attributes its exponential inputs to OpenAI. Actual critical primary bodies/sections must be read before any conclusion about those attributions. Repository and printed manuscript dates must remain distinct. A focused literature check cannot prove worldwide firstness, and the result's independent contribution may be an explicit exact-count corollary rather than a new lower-bound mechanism. No follow-up question is nominated at this stage; default null.

The disclosure states extensive AI use, no conventional human refereeing, no reproduced upstream Lean build owing to disk limits, and no formalization of this binary reduction. Do not turn an archived automated review or finite checker into formal certification. I have not read those archived opinions and will not use them as independent evidence.

## Initial status and next independent checks

The local source, fooling-set, lifting, complement, and algebraic mechanisms have been reconstructed without finding a counterexample at this stage. This does not validate the external inputs. Stage fresh independent controls before opening the scientific program; then fully read the actual selected native checker, runner, README, and whole expected result before any unchanged isolated replay. Read actual pinned upstream theorem and model bodies when raw acquisition is available after both lane initials are sealed. No current peer findings are to be exchanged. Review completion estimate: 30%, reflecting complete manuscript reading and a substantial local proof reconstruction, with native replay, primary-dependency validation, and final adversarial assessment still open.
