# Hyperarithmetical lower bounds of skip two-cycles

This is an AI-assisted, unrefereed mathematical draft. Acceptance records one internal AI mathematical reconstruction of a credited prior result, with explicit foundational imports. It is not human peer review or formal proof-assistant certification. This is a prose proof-and-audit edition, not a computational reproduction package. No novelty, priority, or worldwide-current-openness claim is made.

Target: 30004677 / OWR-7155442-011. PROOF.md preserves the full accepted mathematical reconstruction. AUDIT.md is an editorial acceptance and dependency record for this same reconstruction, not a second independent mathematical audit.

An authored reconstruction and scope audit of a prior result, 11 October 2026.

## Disposition and attribution

**Accepted prior-result component:** for every enumeration degree b,

b has a hyperarithmetical representative if and only if b <= a for every enumeration degree a satisfying a^^ = a,

where ^ denotes the skip, not the Turing jump or the enumeration jump. There is at least one such a. A cycle here comprises a and a^; quantifying over all a satisfying a^^ = a already quantifies over both members of every cycle.

The converse characterization is credited to **Jun Le Goh**, as explicitly reported in Mariya Soskova's problem contribution to Oberwolfach Report 21/2021, PDF page 34, printed page 1182 [OWR]. Its lower-bound direction and the existence of cycles are due to Andrews, Ganchev, Kuyper, Lempp, Miller, A. Soskova and M. Soskova [AGKLMSS, Theorem 3.20 and Proposition 3.21]. This document offers no novelty or priority claim.

**The full two-component target is not resolved by this audit.** Its other component asks for an *arithmetical* enumeration degree a for which every finite skip is nontotal. No construction or nonexistence proof for that component is supplied here. [AGKLMSS, Conjecture 6.3] predicts nonexistence. Nonarithmetical examples, including all skip two-cycles, do not answer that component. Bounded searches failing to find a later result are not a certificate of present open status.

The proof below reconstructs the fixed-point argument, the uniform transfinite lower-bound argument, and the analytic basis argument rather than treating Goh's workshop announcement as a proof certificate. Its remaining standard foundational imports are isolated in Section 7. Acceptance here is internal AI mathematical review, not machine-checked formal verification or expert peer review.

## 1. Conventions and elementary reductions

Fix an acceptable effective enumeration (Gamma_e) of the enumeration operators. Thus Gamma_e(A) enumerates x when one of its c.e. axioms (x,F), with F finite, has F contained in A. Write

K_A = {<e,x> : x belongs to Gamma_e(A)},
S(A) = complement(K_A),
T(B) = B join complement(B).

Here join is a computably tagged disjoint union. The skip of deg_e(A) is deg_e(S(A)). Let S^n denote iteration with S^0(A)=A. An enumeration degree is total when it contains T(B) for some B, and cototal when it contains C with C <=_e complement(C). Arithmetic and hyperarithmetic degree mean a degree with a representative of the indicated complexity. Any set enumeration reducible to a hyperarithmetical set is arithmetical in it and therefore hyperarithmetical, so the latter property is independent of the representative.

Four basic observations will be used.

1. K_A is enumeration equivalent to A, uniformly. One reduction is the universal enumeration operator; the other selects the identity-operator column. If B=Gamma_e(A), then complement(B) is a computable column of S(A). Consequently complement(B) <=_1 S(A), uniformly in e.
2. If A <=_e B, then K_A is a column of K_B, with its column index effectively obtained by composition. Complementing that column gives S(A) <=_1 S(B). Conversely a one-one reduction S(A) <=_1 S(B) complements to K_A <=_1 K_B, hence A <=_e B. In particular skip is degree invariant and order preserving for enumeration reducibility. This is a different order from set inclusion.
3. S reverses **set inclusion**: A contained in B implies K_A contained in K_B, hence S(B) contained in S(A). Therefore S composed with S preserves inclusion.
4. S(A) is not enumeration reducible to A. Otherwise the diagonal set D={e : e does not belong to Gamma_e(A)} would be enumeration reducible to A, by taking the diagonal column preimage of S(A). Let D=Gamma_d(A). At d the defining equivalence reads d in D if and only if d not in D, a contradiction. Also A <=_1 S(S(A)): complement(A) <=_1 S(A) by (1); complementing this reduction gives A <=_1 complement(S(A)), and the identity column gives complement(S(A)) <=_1 S(S(A)).

For totalizations one has T(B) <=_e T(C) if and only if B <=_T C. In the forward direction, enumerate both tagged answers for B from the computable-in-C oracle T(C), and wait for the answer for each input. In the reverse direction, each halting computation from C asks finitely many positive or negative questions; their answers are positive finite information in T(C). The same observation proves that T(B) <=_e A entails B <=_T A, because an ordinary Turing oracle for A can run the enumeration until one of the two answers appears.

## 2. Nonempty class of exact set fixed points

Put F=S composed with S on the complete inclusion lattice P(omega). By Section 1(3), F is monotone. For completeness, the needed fixed-point instance can be proved directly. Let

L = intersection {B contained in omega : F(B) contained in B}.

The family is nonempty because it contains omega. For each such B, monotonicity gives F(L) contained in F(B) contained in B; therefore F(L) contained in L. Applying monotonicity again gives F(F(L)) contained in F(L), so F(L) itself is a member of the intersected family. The definition of L now yields L contained in F(L). Hence F(L)=L.

Define P={A contained in omega : S(S(A))=A}, using **equality of sets**. We have just shown P is nonempty. Membership in K_A is an arithmetical formula with predicate A. Substituting this formula twice, and asserting equality on each integer, gives an arithmetical formula with predicate A for membership in P. Thus P is a lightface Sigma^1_1 class (indeed it is arithmetical). No ordinal notation, parameter coding a noncomputable real, or chosen fixed point occurs in that class definition.

Every A in P gives a degree two-cycle. For the converse in Section 5 we only need this subclass of degree two-cycles; it is unnecessary to show that every cycle degree has an exactly fixed representative. This avoids conflating set equality with degree equality.

## 3. Every cycle degree bounds every hyperarithmetical degree

We first establish explicitly the uniform successor operation used in the transfinite argument.

### 3.1. Uniform jump transport

Suppose a known enumeration index witnesses T(B) <=_e C. Then, uniformly in that index,

T(B') <=_e S(C),

where B' is the ordinary Turing halting jump. Indeed, using the tagged answers in T(B), a finite halting B-computation is certified by finite positive information in C. Thus B' <=_e C, uniformly, and its complement is a fixed column of S(C). In addition, complement(T(B)) is a fixed column of S(C); swapping its two tags produces T(B) from S(C). From these recovered answers one enumerates the positive halting set B'. Combining the positive and negative halting sets produces T(B'). Each operation described is an effective operation on enumeration indices, and uses neither a test that an oracle is total nor a decision procedure for the validity of the original reduction. Its correctness is conditional on the asserted input equality T(B)=Gamma_e(C).

Applying this operation twice transports T(B'') to S(S(C)), uniformly in the original index. The standard computable oracle reduction B' <=_T B'' transports T(B') to T(B'') uniformly as well.

### 3.2. A single operator on all valid ordinal notations

Let a^^=a and choose a representative A. Fix once and for all an enumeration reduction Theta witnessing S(S(A)) <=_e A. This index is allowed to depend on A; no uniform choice across cycles is asserted.

Use the usual Kleene notation system O and hierarchy H(p): H(1)=empty set; H(2^q)=H(q)'; and for a valid limit notation p=3*5^e with q_i=phi_e(i), H(p)=join_i H(q_i). At a limit, the q_i are valid notations for strictly increasing ordinals below the limit. The hierarchy completeness theorem listed in Section 7 says that every hyperarithmetical set is Turing reducible to some H(p).

We construct one enumeration operator Phi(Z,p), with an ordinary integer parameter p, such that

Phi(A,p)=T(H(p)) for every p in O.

Using the recursion theorem, the construction may refer to its own enumeration index. Here are the clauses, which are effective syntactic clauses on the integer p, not tests for membership in O.

- For p=1 output T(empty set).
- For a successor-shaped integer p=2^q, take the index for the q-column of Phi. Apply the uniform transformation of Section 3.1 twice, obtaining a candidate reduction from S(S(Z)) to the totalization of the second Turing jump of the q-column's underlying set. Project down one Turing jump and compose the resulting enumeration operator with Theta. This gives the p-column on input Z. On the distinguished input Z=A, whenever the q-column is correct, this outputs T(H(q)')=T(H(p)).
- For a limit-shaped integer p=3*5^e, dovetail computations phi_e(i). Whenever q_i is obtained, copy the appropriate tagged output of Phi(Z,q_i) into column i. Rearranging the tags realizes the totalization of the effective join. On a valid notation all phi_e(i) halt, so both positive and negative columns are copied correctly.
- Other integer shapes may have empty output. On invalid notations no correctness claim is made.

These instructions generate c.e. sets of finite-oracle axioms uniformly from a proposed index for Phi and the fixed index Theta. They are therefore eligible for the ordinary recursion theorem. The resulting operator exists on every oracle, even though its intended correctness is asserted only on A and on valid notations. In particular the construction never queries O and never assumes a computable list of exactly the valid notations.

Transfinite induction on the ordinal denoted by p now proves the displayed equality. The zero clause is immediate; the successor clause follows from Section 3.1, twice, and the fixed reduction Theta(A)=S(S(A)); the limit clause uses the simultaneous induction hypotheses for its lower notations and the uniform join. This explicitly supplies the uniformity needed at limit stages; merely saying that A separately bounds each earlier H(q_i) would not suffice.

More plainly in the successor step, the chain of witnessed reductions is

T(H(q)') <=_e T(H(q)'') <=_e S(S(A)) <=_e A.

Let X be hyperarithmetical. Choose p with X <=_T H(p). Then T(X) <=_e T(H(p)) <=_e A, and consequently X <=_e A. This proves the lower-bound direction for all hyperarithmetical enumeration degrees, including the nontotal ones. The wording “total hyperarithmetic degree” in [AGKLMSS, Proposition 3.21] is sufficient because every hyperarithmetical X lies below its hyperarithmetical totalization T(X).

## 4. The analytic basis lemma, reconstructed

We need the following prior theorem of Harrington, Shore and Slaman [HSS, Theorem 2.1]: if a fixed set X is Sigma^1_1 relative to every member of a nonempty lightface Sigma^1_1 class K of reals, then X is lightface Sigma^1_1. The relative defining index may vary with the class member. This is important: the theorem is not restricted to a single uniform index.

Here is a proof using effective analytic normal forms, with the fusion issue made explicit. A nonempty effective analytic class has a presentation as the projection of a recursive tree on pairs (Z,W). Thus a witness W certifies membership by satisfying a sequence of finite-prefix conditions. There are countably many relative Sigma^1_1 formulas theta_e(Z,n); list all of them.

Start with the condition C_0=K. At stage e we maintain a nonempty effective analytic class C_e, together with finite prefixes of the intended real Z and of witnesses for all the finitely many conditions introduced so far. These prefixes extend the previous prefixes and have length at least e. We ask whether some natural number n and some nonempty effective analytic subclass D of C_e satisfy either

(i) n is outside X, and every Z in D satisfies theta_e(Z,n); or
(ii) n is in X, and every Z in D fails theta_e(Z,n).

This is an existence construction; it is not claimed to be an effective decision procedure from X or from the index of C_e. If such a D exists, add a recursive-tree witness for D. Choose a member of D and witnesses consistent with the existing prefixes, and extend the prefix of Z and every current witness to length at least e+1. Restrict by these finitely many prefixes, obtaining the next nonempty effective analytic condition. The finite strings and the finitely many recursive indices are natural-number parameters and introduce no real parameter into its effective analytic definition.

If this succeeds forever, the increasing prefixes give a real Z and, separately for each condition, a complete witness. For any fixed finite-prefix requirement, all sufficiently late stages satisfy it. Therefore these limits satisfy all the recursive-tree conditions. In particular Z belongs to K and to every chosen D. At stage e the chosen n then witnesses that theta_e(Z,.) does not define X. As this holds for every e, X is not Sigma^1_1(Z), contradicting the hypothesis on every member of K. Notice why nesting nonempty analytic classes alone would not suffice: their intersection could be empty. The retained and lengthened witnesses establish membership of the limit.

It follows that the construction must stop at some e. No n and D as in (i) or (ii) then exist. We claim

n is in X if and only if there exists Z in C_e with theta_e(Z,n).

If the right-hand side holds with n outside X, intersecting C_e with the effective analytic set defined by theta_e(.,n) yields a nonempty D of type (i), contradiction. If n is in X and the right-hand side fails, C_e itself is a D of type (ii), contradiction. The displayed right-hand side is Sigma^1_1: analytic classes are closed under finite intersection and existential real quantification. This proves the lemma.

This proof follows the mathematical argument of [HSS, PDF pages 3-4], with its normal-form foundation stated explicitly. It is an authored reconstruction, not a new basis theorem. Neither arbitrary analytic sets with real parameters nor an uncountable enumeration of formulas is used.

## 5. Characterization of the common lower cone

Suppose b is below every degree a with a^^=a, and choose X in b. For each exact fixed point A in the nonempty class P of Section 2, we have X <=_e A. In particular X is c.e. in the ordinary Turing oracle A; its complement is co-c.e. in A. Both sets are arithmetical in A and therefore Sigma^1_1(A). This last statement does **not** assert complement(X) <=_e A, an unjustified conclusion for a general nontotal degree.

Apply the basis lemma of Section 4 to X and P, and then separately to complement(X) and the same P. It follows that X and its complement are both lightface Sigma^1_1. Therefore X is Delta^1_1, that is, hyperarithmetical. This proves the upper-bound direction. Section 3 proves the reverse direction, completing the claimed equivalence.

There is no uniformity gap: the assumption supplies one enumeration index for each A, not a single index for all A. The basis lemma was proved with precisely that nonuniform premise. There is also no vacuity gap: P was proved nonempty before this implication was used.

## 6. The arithmetic question and the exact limit of the answer

For any degree c, c <= c^ is equivalent to cototality. If C is a cototal representative, C <=_e complement(C) <=_e S(C), giving the forward comparison. Conversely if A <=_e S(A), then K_A <=_e complement(K_A), so the representative K_A witnesses cototality. The enumeration jump has degree of K_A join complement(K_A), which is total, and is degree equivalent to A join S(A). Consequently c <= c^ implies that c^ is total. Every total degree is cototal, by using a totalized representative and interchanging its two tags.

For a_n=a^(n), with n starting at zero, it follows that

(for every n, a_n is not <= a_(n+1)) if and only if (for every n, a_n is nontotal).

Indeed a total a_n is cototal and violates the left condition. Conversely a comparison a_n <= a_(n+1) makes the next skip total and violates the right condition. This is an equivalence of the **universal conditions**, not a claim that “nontotal” and “not cototal” agree for each single degree.

In a degree cycle a^^=a, the two entries are incomparable. The direction a^ <= a is excluded by the skip diagonalization of Section 1. If a <= a^, monotonicity of skip gives a^ <= a^^=a and again contradicts that diagonalization. Thus all finite skips in such a cycle are nontotal.

Nevertheless no cycle degree is hyperarithmetical. If A were a hyperarithmetical representative, A' would be hyperarithmetical too. Section 3 would give T(A') <=_e A. By Section 1's totalization argument this implies A' <=_T A, contradicting strictness of the ordinary Turing jump. In particular a cycle degree cannot be arithmetical. This shows directly, rather than merely by a missing hypothesis, why the known cycles cannot be arithmetic counterexamples.

The source's first question initially specifies “arithmetical” and then drops that adjective in its equivalent reformulation. Retaining that restriction is mandatory to make the intended question nontrivial and consistent with the already stated examples. The imported target preserves it in its first clause. The source contribution also contains a third question, first-order definability of skip. That third question is outside this two-component target and is not claimed settled here.

## 7. Dependency boundaries and challenge record

Reconstructed here: skip degree invariance and diagonal obstruction; the exact set fixed-point argument; effective-analytic definability of its class; the uniform jump-transport and transfinite reduction construction of the lower bound; the HSS basis lemma including witness fusion; the two applications yielding Goh's converse; the universal zigzag/nontotal equivalence and the nonhyperarithmetical nature of cycles.

Standard foundational results used but **not independently proved here**:

- Existence of an acceptable numbering of enumeration operators, effective composition/parameter substitution, and the ordinary recursion theorem. Section 3 spells out the operator to which self-reference is applied.
- The Kleene notation hierarchy: its syntactic successor/limit clauses and well-founded induction on valid notations; the classical identification of Delta^1_1 sets with sets Turing reducible to some H(p). The second part is a substantive standard characterization, not a computational check made by this audit.
- Effective analytic normal form as projections of recursive trees, its relativization, and its closure under finite intersection and existential real quantification. These are the exact foundations needed for Section 4; they are also stated in [HSS, pages 1-3].
- Ordinary set-theoretic countable dependent choices in the fusion construction and ordinary Turing-jump strictness. No reverse-mathematical strength claim is made.

No unsupplied research lemma specific to skip cycles is left as an import. The characterization is accepted relative to these named standard foundations. The complete contents and all unrelated theorems of the cited papers have not been audited. In particular their generic-set constructions, skip inversion, and definability results are not dependencies of this proof.

Adversarial checks resolved in the text:

1. Replacing “every cycle” by “some cycle” would be false: a cycle degree bounds itself but is not hyperarithmetical.
2. Replacing “degree equality” by “set equality” everywhere is unnecessary and unjustified; only the nonempty test subclass uses exact equality.
3. Treating skip as either jump invalidates the cycle argument. Its definition includes complementation of K_A and does not add A.
4. Confusing inclusion antitonicity with reducibility monotonicity reverses the relevant order. Both relations are distinguished in Section 1.
5. Negating an enumeration reduction need not give an enumeration reduction. Section 5 uses arithmetical relative definability instead.
6. Separately bounding every earlier H(q_i) does not supply the effective join. A single self-referential Phi supplies it.
7. Deciding membership in O is not allowed; the construction only branches on notation shapes and asserts correctness on valid notations.
8. A nested family of nonempty analytic sets need not have a common member; Section 4 retains compatible witness prefixes.
9. Totality and cototality are not synonyms; the arithmetic equivalence needs a one-step shift.
10. A finite toy computation cannot certify an assertion over all ordinal notations or reals. The original audit’s finite checks, not distributed in this prose edition, only exercise the order-theoretic identities, while hashes check artifact integrity.

## Sources

[OWR] Computability Theory, Oberwolfach Report 21/2021, DOI 10.4171/owr/2021/21. Relevant contribution by Mariya Soskova, PDF page 34 / printed page 1182. https://ems.press/content/serial-article-files/46899

[AGKLMSS] Uri Andrews, Hristo A. Ganchev, Rutger Kuyper, Steffen Lempp, Joseph S. Miller, Alexandra A. Soskova, Mariya I. Soskova, *On cototality and the skip operator in the enumeration degrees*. Author-hosted 39-page PDF; relevant pages 3-4, 12, 20-21 and 37. https://people.math.wisc.edu/~slempp/papers/cototal.pdf . The audit uses the page numbers printed in this retained author version; it does not infer final-journal page offsets.

[HSS] Leo Harrington, Richard A. Shore, Theodore A. Slaman, *Sigma^1_1 in every real in a Sigma^1_1 class of reals is Sigma^1_1*. Retained author manuscript dated July 11, 2016, 12 pages; Theorem 2.1 and its proof on pages 3-4. https://math.berkeley.edu/~slaman/papers/Sigma1116.pdf . Slaman's bibliography identifies the work as published in *Computability and Complexity*, Springer, 2017: https://math.berkeley.edu/~slaman/papers/Publications.html . The downloaded manuscript has not been byte-compared with a publisher edition.

[SOSKOVA] Mariya Soskova, *The e-verse*, WDCM 2021 slides, PDF page 15 / displayed slide 14 of 20, independently credits Goh for the characterization. https://people.math.wisc.edu/~soskova/talks/WDCM2021Soskova.pdf . The slides supply attribution and a theorem statement, not a separate proof.
