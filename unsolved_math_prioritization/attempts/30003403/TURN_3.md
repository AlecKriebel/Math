# Author turn 3: an actual quotient onto every countable target

**Partial: all countable targets are covered in ZFC; the uncountable PFA target remains unresolved.** 2026-10-01.

The route in turn 2 is now implemented for a suitable alternative section, rather than discarded because a given embedding fails. Let C be any Countryman line, D=C*+{0}+C, and L=eta_C=E(D), the lexicographic order of eventually-zero sequences. No normality assumption on C and no forcing axiom are used in this turn.

## 1. A bounded rational section

Fix a<b in L. There is a finite-prefix cylinder [p] contained in (a,b). Indeed, let j be the first difference of a,b and choose N greater than j and both support bounds. Follow a through coordinate N-1, then place any positive symbol at N. Every continuation of this prefix is greater than a, and is less than b by the unchanged comparison at j.

Choose two fixed symbols d_-<0<d_+ of D. For each finite word s in the two-letter alphabet {d_-,d_+}, define

    t_s = p concatenated with s concatenated with the zero tail.

Set T={t_s:s is a finite two-letter word} and B={a,b} union T. The order on T is the usual in-order arrangement of the full binary tree: the entire d_- child subtree is below t_s, and the entire d_+ child subtree is above t_s. In particular T is countable, has no endpoints, and is dense. For density, if t_s<t_t and their words split, their common-prefix node lies strictly between unless it is an endpoint, in which case a child node of that endpoint pointing toward the other point lies between. If one word extends the other, append the opposite sign sufficiently far along the longer word to obtain a point between. Equivalently the finite binary search tree has an additional descendant between any two of its nodes. Hence B has type 1+Q+1.

We claim that B is a retract of [a,b]. Use the cut criterion from turn 2. Points below all of [p] have a as greatest B point below them (unless they equal a); points above all of [p] have b as least B point above them. As [p] is convex, these are all points outside [p].

For x in [p], strip p and follow the remaining coordinates while they equal d_- or d_+. At each finite word s keep two bounds l_s,u_s in B: start with a,b; on a d_- step replace the upper bound by t_s, and on a d_+ step replace the lower bound by t_s. The entire subtree T_s lies between l_s and u_s, and no B points outside that subtree lie strictly between these bounds. The same bounds bracket any ambient point whose coordinates continue the word s.

Because x has finite support and d_-,d_+ are nonzero, there is a first next symbol v that is neither d_- nor d_+. At that place:

- If v<d_-, then x lies below the whole subtree T_s, and l_s is the greatest B point below x
- If v>d_+, then u_s is the least B point above x
- If d_-<v<0, then t_s is the least B point above x
- If 0<v<d_+, then t_s is the greatest B point below x
- If v=0, then x is either t_s itself, or is on one side of t_s with no B point between x and t_s; the remaining tail decides that side

These cases are exhaustive in a linear order. They verify the retraction criterion, so [a,b] has a monotone retraction onto B. Infinite paths with all coordinates in {d_-,d_+} could realize nonprincipal cuts of T; crucially, they are absent from E(D). This is where finite support provides more than a merely dense embedded copy of Q.

## 2. Gluing into an unbounded rational quotient

The order L is short and has no endpoints, as established in turn 1. Thus it has an increasing sequence (a_n) indexed by Z that is coinitial and cofinal. One obtains it from a countable decreasing coinitial sequence below a_0 and a countable increasing cofinal sequence above a_0. Shortness supplies the two countable cofinalities; no separability of L is asserted.

Apply Section 1 independently on each interval [a_n,a_(n+1)], producing a section B_n with endpoints a_n,a_(n+1) and type 1+Q+1. Let r_n be its retraction. On a shared endpoint the two maps both fix that endpoint, so the maps glue to a monotone map

    r:L -> B = union over n in Z of B_n.

The intervals cover L. Their ordered ranges have the same shared endpoints, so this map is monotone globally and fixes B pointwise. The countable order B is dense and has neither endpoint; hence B is isomorphic to Q. We have produced an actual monotone epimorphism L -> Q, not just an embedding of Q or a map on finite levels.

## 3. All countable targets, with explicit credit

Every nonempty countable linear order K is a monotone image of Q. This is a standard result credited in Camerlo–Carroy–Marcone, *When embeddability and epimorphism agree*, introduction p2, citing Proposition 16(1) of their reference [4]. A short direct verification is available: K×Q, with the K-coordinate primary, is countable, dense, and without endpoints, so it is isomorphic to Q; its first-coordinate projection onto K is monotone and onto. Composing this map with r gives

    eta_C -> K

for every nonempty countable K. In particular all countable suborders of eta_C satisfy the strong-surjectivity requirement. This partial result holds for every Countryman input, independently of PFA. No historical novelty is claimed.

## 4. Exact remaining gap

The binary section works because it has only countably many branching instructions and every ambient point leaves the two-letter path after finitely many steps. It does not provide a section of a general uncountable Aronszajn target. Replacing binary nodes by whole Countryman families would require coherent target cuts and would reintroduce the uncountable epimorphism problem. The credited normal-Countryman and fragmented-target theorems retain their own hypotheses; this proof has not extended them to all Aronszajn targets.

Thus the original question remains: under PFA, is there an epimorphism from eta_C onto every uncountable suborder? No counterexample and no such general map have been found. The countable part is now genuinely closed by a quotient construction. The finite diagnostic checks the node classifier and its cut inequalities; it is not evidence for a transfinite gluing theorem.

Substantive author turns: 3/5. Estimated completion toward the original target: 25%.
