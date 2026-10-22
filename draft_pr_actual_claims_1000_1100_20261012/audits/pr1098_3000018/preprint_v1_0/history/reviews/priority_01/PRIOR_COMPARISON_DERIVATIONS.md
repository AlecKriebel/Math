# Exact priority comparisons for PR #1098

These deductions were made after reading the complete submitted main proof and oriented appendix and the ROOT mathematical adoption. They assess attribution and implications; they are not a claim to have discovered the candidate's mathematics independently. All finite controls below are freshly authored and import no candidate or sibling implementation.

## 1. The bank multiplicities are a specialization of an earlier lemma

The directly read primary body is Holroyd, Levine and Winkler, *Abelian logic gates*, arXiv:1511.00422v2, Lemma 4.1, PDF/printed page 15. Its unary construction primes parallel topplers according to the consecutive increments of an increasing linear-plus-periodic function. The following exact substitution is our comparison deduction.

Fix a periodic indicator h of a nonempty set A modulo q. Put

    f(k) = k + h(0) - h(k),  k >= 0.

Then f(0)=0, f(k+1)-f(k) belongs to {0,1,2}, and f(k+q)=f(k)+q. Thus it has the hypotheses of that lemma, with slope one and period q. At the lemma's position i in {1,...,q}, the multiplicity is

    d_i = f(i)-f(i-1) = 1+h(i-1)-h(i).

That toppler is primed in state a=q-i, read modulo q. Consequently

    d_i = 1+h(-a-1)-h(-a) = c_a.

This is exactly the candidate's 0/1/2 multiplicity formula, including its offset phase. It is not merely a superficial similarity to a counter. If F(k) counts topplings of those q separate primed topplers, then

    F(k) = sum_a c_a floor((a+k)/q) = f(k).

The candidate's physical counter storage therefore obeys the conservation identity

    S(k) = S(0) + q k - q F(k)
         = S(0) + q(h(k)-h(0)).

Averaging over a period gives S(0)-q h(0)=q(q-1)/2-|A|. This derives the exact bank identity from the earlier priming construction and an elementary storage calculation. The formula for c_a, and the parallel primed-toppler mechanism, require explicit credit to the earlier lemma. The note may give the short self-contained proof, but cannot present this mechanism as a certified new invention.

The earlier gates do not automatically satisfy the candidate's physical graph conditions. A toppler emitting one letter per q inputs is not an ordinary chip-firing vertex of degree one, whose threshold is one. A splitter also creates letters. The source itself distinguishes conservative gates in Section 8.3, page 32. The candidate instead feeds q physical counters per bank, returns q chips per counter toppling through distinct vertices, uses a single root of the correct outdegree and total mass, and closes the system without dissipative sinks. The exact conserved amount per bank is q F(k), not F(k). These are mathematical parts of the conservative realization, not conclusions supplied by Lemma 4.1 alone.

## 2. The CRT/SAT stage has an exact classical antecedent

The directly read primary source is Stockmeyer and Meyer, *Word problems requiring exponential time: Preliminary report* (STOC 1973), Theorem 6.1 and its proof, PDF/printed pages **7-8**. The preliminary message to the parent used pages 6-7; the verified locator is 7-8. The theorem's proof encodes Boolean assignments as residues 0 or 1 modulo distinct variable primes. A clause uses the product of its three variable primes and the unique falsifying Boolean residue. The union of all invalid-variable and failed-clause languages is universal exactly for an unsatisfiable formula. Gregor Gramlich, *Probabilistic and Nondeterministic Unary Automata* (MFCS 2003), Fact 3, PDF pages 5-6, also directly reconstructs this classical reduction. Gramlich is the sole author on the actual title page; the preliminary message and opaque acquisition ID mentioning Schnitger do not add a coauthor.

For the candidate's normalized formula, let A_i={0,1} modulo p_i and let A_C be the Boolean satisfying residues modulo q_C=product_{i in C} p_i. Define

    Good(k) = AND_b [ k mod q_b in A_b ],
    Bad(k)  = OR_b  [ k mod q_b not in A_b ].

Then Good(k) is exactly NOT Bad(k). On words a^k, Bad is the language accepted by the classical union construction: non-Boolean residues fail a variable condition, and a Boolean assignment fails a clause exactly at that clause's falsifying residue. Restricted clauses of length one or two use the same argument. CRT supplies a representative for every assignment, while products of at most three polynomially bounded primes keep each local cycle polynomial. The candidate's simultaneous allowed predicates are therefore precisely the complement presentation of this earlier encoding. Omitting the prime 2 is immaterial to the argument. Both the encoding and the decision to avoid expanding the global CRT period need attribution; neither is priority-cleared as new.

This is not an earlier claim that ordinary chip-firing halting is NP-complete for simple digraphs. An automaton's accepting state is not a stable chip configuration. A separate implementation must make simultaneous acceptance equivalent to ordinary conservative halting. The candidate does so through storage deficits and the root threshold.

## 3. The root-last viewpoint also has an explicit antecedent

Farrell's Cornell senior thesis, dated 2 December 2014, Sections 1.1 and 4.1, pages 2-3 and 9, chooses a distinguished vertex, stabilizes the remaining vertices, fires the distinguished vertex, and repeats. It relates full halting to a large enough mass in a recurrent nonsink configuration along a cyclic subgroup. Section 4.1 also uses CRT to decide an integral-congruence condition. Farrell and Levine's arXiv:1502.04690v3, Section 2, develops the same comparison with and without a temporarily designated sink. These are meaningful antecedents for the candidate's scheduling and mass accounting.

The thesis's congruence question is linear integrality/coset membership and is polynomially decidable. It is not the disjunction of allowed Boolean clause residues above. Its attempted hardness route in Section 4.2 goes through a lattice and potentially very large edge multiplicities. The later Farrell-Levine Section 3 gives the full binary-multigraph hardness theorem and Section 3.1 explicitly separates the simple case. Neither the thesis's linear CRT test nor the general multigraph theorem is a proved source of the complete simple conservative result.

For the candidate, after k distinguished-root firings and legal nonroot stabilization,

    x_r(k)=C-S(k)=Q+B-1-S(k),
    x_r(k)<Q iff S(k)=B iff every local predicate is allowed.

This algebraic interface uses integrality, the pointwise upper bound S(k)<=B and nonnegative storage deficits. The root remains an ordinary vertex; its delayed firing is a legal scheduling choice. The earlier root-last method deserves credit, while the exact SAT threshold equivalence remains part of the candidate's self-contained proof.

## 4. Generalized rotor reachability does not supply the claimed corollary

The actual journal PDF of Auger, Coucheney and Etse, *Linear Extensions of Rotor-Routing in Directed Graphs: Reachability Problems*, Electronic Journal of Combinatorics 33(2) (2026), P2.5, DOI 10.37236/13580, was downloaded directly. It was published 14 April 2026. The complete hardness construction, Theorem 21 and Lemmas 22-23 on pages 39-43, was read, including the variable and clause gadgets and exact final target. The arXiv v2 PDF is a separate edition with distinct bytes; it is not labelled publisher-identical.

The variable gadget has an initial arc state at a_start and two available sequences of arc-face transitions, one passing the two positive literal arcs and the other the two negative literal arcs. Three particles implement one choice of sign. Final arc states and particles at several sinks are specified. Thus the existential choice can produce different literal-sink outputs from the same local starting configuration. Ordinary chip-firing at a given vertex has one fixed output vector; legal choices of firing order do not change a reachable stable endpoint. Erasing the arc mechanism would erase the reduction's assignment choice. Moreover the source proves reachability of a specified pair of arc/particle configurations, rather than the existence of any ordinary stable configuration.

The reported NP-completeness in this more general conservative VAS model does not imply hardness in a subclass merely because that subclass is also a conservative VAS. No reduction compiling those branching mechanisms and exact targets to the candidate's simple conservative halting language was found or proved in the directly read source. This is a precise missing implication, not a dismissal based on the title. The source's converse paragraph says "4 particles" after specifying 3; this audit relies on the explicit three-particle gadget and its structural distinction, and does not certify every line of the source proof.

## 5. Sandpilization preserves a different quantifier

Bond-Levine, *Abelian networks II. Halting on all inputs*, Definition 6.5 and Corollary 6.6, pages 17-18, preserve whether a network halts **on all inputs**. They do not state that an arbitrary specified input and internal state have the same outcome after simply replacing every processor by the reset-state toppling network with its mean production matrix.

A concrete control makes the distinction checkable. A unary two-state self-feedback processor alternates states 0 and 1, emitting respectively 2 and 0 pending letters. With one pending letter and state 0, two processings return to the same pair (pending letters, state)=(1,0), so the process does not halt. Its reset-state modulus-two sandpilization emits two letters only on the wrap transition. On the same reset state 0 and one pending letter it absorbs that input and halts. Both fail the all-input halting property, consistently with the source corollary. This refutes only the unsupported same-reset-input transfer; it does not rule out every possible state-aware reduction. The candidate does not invoke that invalid transfer.

## 6. Petri nets: exact restrictions matter

Represent each chip vertex v by a place p_v and a transition t_v. The transition consumes d_v tokens from p_v and produces one token in p_u for every arc v->u. This is a weighted choice-free and join-free (fork-attribution) Petri net, with one consumer per place, one input place per transition, unit output weights and exact token conservation. Its nonunit input weight is essential. Plain conflict-free Petri-net definitions in the directly read Esparza-Nielsen and Cheng-Esparza-Palsberg bodies use set-valued flow relations and threshold one on each input place. A purported degree-three-to-threshold-one normalization changes the outcome even for a single counter initially at zero receiving one chip.

Conversely, generalized communication-free nets may have several transitions consuming the same place, arbitrary weighted outputs, nonconservative growth, and target reachability rather than halting. Such broader hardness cannot be restricted to the candidate's one-consumer, balanced, unit-output subclass without an actual reduction. The Mayr-Weihmann technical-report PDF routes failed, so their full construction is **UNKNOWN** here, not declared nonapplicable from its abstract. The Hujsa-Devillers 2017/2018 full PDF routes also failed. The accessible author-uploaded 2017 text was inspected only for the class definitions, stated contributions and structural-all-marking quantifiers; the full exact given-marking implication remains **UNKNOWN**. The retrieved file initially named Hujsa_single_shared is in fact Best-Devillers-Erofeev-Wimmel's *Target-oriented Petri Net Synthesis*; its actual title and narrow read scope are recorded and it is not substituted for either missing paper.

These limits prevent a worldwide priority guarantee. No presently unread body is asserted to contain, or exclude, the exact complete theorem. Accurate attributed-proof publication does not depend on making that unsupported guarantee.

## 7. Other close controls and unsupported transfers

The directly read Perrot-Pham MINREC decision interface and hardness proof concern optimizing over recurrent configurations with a designated dissipative sink. Kiss-Tothmeresz instead minimize the additional chips needed for nontermination; their simple Eulerian hardness quantifies over an added distribution. Knowing that an optimized distribution exists is not deciding halting for one supplied distribution. The ordinary halting problem on simple Eulerian graphs has the distinct earlier polynomial method, so these optimization theorems cannot silently become the candidate's many-one hardness.

Schulz's 2007 DIST construction likewise chooses an added chip distribution to force recurrence in a finite boundary-dissipative grid. Moore-Nilsson's circuit simulation predicts the final state of a system that halts. Cairns's undecidable cases use spatially infinite periodic-plus-finite backgrounds. None of the directly inspected interfaces supplies the missing finite conservative simple-graph SAT equivalence. These source proofs are not all re-certified globally; their precise hypotheses are the comparison.

Eriksson's full three-page 1991 source gives simple directed graphs and polynomial initial chips with exponentially long terminating games. It refutes a polynomial simulation-time inference, but an explicit hard-to-simulate family is not a many-one NP-hardness reduction. The candidate must not claim firstness for long clocks or small-chip exponential behavior.

Ji-Li-Wang's directly read parallel-chip-firing motor construction (2024 preprint, inspected arXiv v3 revised 8 April 2025), Lemma 4.3 and Theorem 4.6, realizes prescribed binary firing strings in a synchronous rule. Their cycles and waterfalls are relevant timing antecedents, but the proof does not implement simultaneous modular SAT storage, and a synchronous prescribed word is not by itself an ordinary-halting reduction. Huang-Tian's October 2026 body, Section 4 and full proof of Theorem 4.1, analyzes the least period of an already active fixed-priority periodic orbit. It does not classify from an input which trajectories stabilize; its conclusion leaves that transient question explicit. This recent source therefore provides a period comparison, without an established exact antecedent for the candidate theorem.

Naively subdividing each arc of the binary multigraph hardness instance costs one new vertex per physical arc. An entry 2^k has k+1 binary bits but would require 2^k such vertices. Thus general binary-multigraph hardness plus numerical edge expansion is not a polynomial simple-graph reduction. The candidate's local prime-product expansions avoid this obstruction; that fact is part of the proof, not evidence of literature novelty.

## 8. Diagnostic scope

`check_prior_interfaces.py` verifies the exact earlier-lemma substitution on 8,177 nonempty banks and 278,282 positions, including full predicates. It checks the classical union-complement equivalence on 256 formulas, 26,880 residue positions and 2,048 assignments; 3,720 physical toppler interfaces; the two-state sandpilization distinction; two sign traces in the GRM gadget; and binary expansion samples through 257 input bits. Six deliberately damaged implications are rejected. Normal and optimized Python produce byte-identical complete JSON, and an unconditional invalid guard fails in both modes.

The tests support these explicit comparison deductions. They are not an exhaustive theorem audit, literature search, novelty certificate, publisher validation or peer review. The exact complete theorem was already independently accepted at the mathematical stage, and no mathematical correction is requested by this priority review.
