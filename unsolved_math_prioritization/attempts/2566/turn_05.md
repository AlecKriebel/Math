# Attempt 5/5: fixed overgroups, minimal-simple input, and the final obstruction

Date: 2026-10-03 UTC. Objective: force an invariant maximal pi-overgroup using the odd quotient action, completing the extension step left by the previous attempts. Outcome: a precise fixed-point equivalence, additional proved/credited positive cases, and an explicit unresolved gap. No complete solution.

## 1. An exact fixed-point reformulation

Assume G=HN, A=H∩N, and define

Omega={B≤N : B is pi-maximal in N and A≤B}.

This is a nonempty finite set. H acts on Omega by conjugation because N and A are H-invariant. Every a∈A lies in each B∈Omega, so its conjugation fixes B. The action therefore factors through

P=H/A≅G/N,

an odd pi-group.

There is an H-fixed member of Omega if and only if A is pi-maximal in N. Indeed, if B∈Omega is H-invariant, then BH is a pi-subgroup of G containing H. Maximality gives B≤H∩N=A, so B=A. Conversely, if A is pi-maximal, Omega={A} is fixed.

Thus a counterexample is precisely a genuine group-theoretic realization of a fixed-point-free odd P-action on the set of maximal pi-overgroups of A.

## 2. What orbit counting really proves

If P is a p-group and A is not maximal, every P-orbit in Omega has length divisible by p. Therefore p divides |Omega|. If |Omega| is not divisible by p, the assertion is true in this particular configuration.

More generally, let r be the least prime dividing |P| when P≠1. Every nontrivial orbit has size at least r. Hence |Omega|<r forces a fixed point and maximality. In particular, an odd P cannot act without fixed points on a set of one or two elements.

However, oddness does not force a fixed point on an arbitrary finite set: C_3 has a regular action on three points. Nor does a pi'-cardinality alone suffice when P has several prime divisors: C_15 has an action consisting of one orbit of size 3 and one of size 5, with total size 8 and no fixed point. Thus a parity argument, or a claim that pi'-cardinality always forces an invariant overgroup, would be invalid.

The original problem requires special information about this specific overgroup set Omega. The existence of the odd action alone does not provide it.

## 3. The even control displays exactly the missing mechanism

The exact checker from turn 4 now finds all pi-maximal overgroups of A in N for the known PGL_2(7) example. There are exactly two, each of order 24. To certify completeness, it computes <A,g> for every g∈N. The generated pi-groups have orders8 or24; every proper pi-overgroup contains one of the order 24 groups, which already has the full {2,3}-part of |N|=168, so cannot be enlarged within pi-subgroups.

The chosen order 8 generator of H interchanges those two overgroups. Thus H/A≅C_2 acts without a fixed point. Odd quotient actions cannot imitate this two-point obstruction. An odd counterexample would require at least three maximal overgroups or a more complicated orbit configuration.

This computation checks a credited known control example only; it does not enumerate all possible odd configurations.

## 4. A successful boundary case from current primary literature

Guo–Revin, 'Classification and properties of the pi-submaximal subgroups in minimal nonsolvable groups', Bulletin of Mathematical Sciences 8 (2018), 325–351, DOI 10.1007/s13373-017-0112-y, Theorem 1.1 and Tables 1,3,5,7,9 classify the odd-pi cases for the minimal simple groups. Each relevant table states that its pi-submaximal subgroups are pi-maximal. The empty-prime and single-prime cases are immediate (the latter also follows from turn 4).

Since every A=H∩S in a normal extension of a simple S is strongly pi-submaximal, the original assertion is therefore true when N is minimal simple. This is a consequence of the published classification, not a new resolution or an independent classification proof.

It also settles minimal nonsolvable N. Let R=Rad(N). Any proper normal subgroup of N is solvable, so N/R is simple; every proper subgroup of N/R has solvable preimage, so it is minimal simple. Apply the quotient lemma of turn 2 with R, use the published minimal-simple result for N/R, and lift pi-maximality back to N.

Together with turn 3, one obtains the following further sufficient condition: the assertion holds whenever N/Rad(N) is a direct product of nonabelian simple groups each of which is either minimal simple or has pi'-outer automorphism group. The direct-product localization theorem applies to the quotient, and the solvable-radical lifting lemma returns the conclusion to N.

## 5. Why the final attempt still stops

To settle the full question by the fixed-point route, one needs a theorem ensuring an H-invariant maximal pi-overgroup of A in every finite N. None has been proved here. For an attempted counterexample, one needs an actual normal extension G=HN with the fixed-point-free action and with H pi-maximal; an abstract odd permutation action or a self-normalizing odd subgroup is not enough.

The remaining cases include genuinely odd outer automorphism actions on non-minimal simple groups, and radical-free normal groups with layers above their socles. The direct-product argument does not justify replacing such a group by its socle. The solvable quotient lemma does not justify removing nonsolvable layers.

The 2024 nonpronormal odd-order example is important adjacent work, but simple ambient groups have no proper nontrivial normal kernel, so it provides no missing normal-intersection realization. Pronormality and the exact question must remain separate.

## Final result of the five-turn budget

Five substantive proof/counterexample attempts have been written. No proof of the universal statement and no odd-order counterexample have been obtained. The appropriate status is unresolved after 5/5 attempts, with rigorous reductions and positive subcases recorded and only modest exact control computations. Retrieval, source checks, auditing, and packaging are not additional attempt turns. No claim of novelty, priority, or complete resolution is made.
