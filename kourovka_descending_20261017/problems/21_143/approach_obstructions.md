# Kourovka 21.143: independent obstruction audit

Author metadata for the research program: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.

Scope: standard dyadic piecewise-linear Thompson group F, with the group-theoretic synchronous meaning of automatic. This file records an independent obstruction search; it does not assume the verdict of another approach family. No external communication, Git operation, release, or publication was performed by this agent.

## Exact claim and quantifiers

Put S={x0,x0^-1,x1,x1^-1}. For a word u let u(t) denote the group element represented by its prefix of length min(t,|u|). A negative solution must establish that for EVERY regular language L over S surjecting onto F and EVERY K, there are u,v in L with d(u(end),v(end))<=1 and some t with d(u(t),v(t))>K. The equivalent definition with padded synchronous equality and right-multiplier automata is also acceptable. It is sufficient to work with this fixed finite generating set, since group automaticity is independent of finite generating set. It is NOT sufficient to exclude a particular normal form, all geodesic languages, or all biautomatic structures.

For a positive solution, one needs an actual regular surjective language and all equality/right-multiplier relations, or an all-pairs synchronous fellow-traveller proof with an explicit finite K. Nothing below supplies these.

## Checkpoints

- 2026-10-17 21:06:50 UTC: Initial independent search started. Discovery completion estimate 2%; obstruction audit completion estimate 10%. Exact all-structures quantifier fixed.
- 2026-10-17 21:07:54 UTC: Geodesic route audited against primary counterexamples. Discovery completion estimate 3%; audit completion estimate 40%. A general implication from absence of regular geodesic representatives to nonautomaticity is false, even among virtually abelian groups.
- 2026-10-17 21:08:30 UTC: Centralizer, dimension, filling, and distortion routes separated. Discovery completion estimate 3%; audit completion estimate 65%. Elementary length and PL-slope lemmas below isolate genuine necessary constraints; neither contradicts F.
- 2026-10-17 21:10:59 UTC: Primary higher-filling theorem and explicit subgroup-inheritance counterexamples located. Discovery completion estimate 4%; audit completion estimate 90%. Independently checked the constructive agent's adjacent GS-language family and the root's finite-state rational-recoding obstruction; both are language-specific and do not decide all-structures automaticity.

## Family A: seesaw words, geodesic pumping, and almost convexity

Mechanism: force an arbitrarily long monochromatic suffix in every geodesic representative, then pump it; or force geodesic paths to adjacent endpoints through opposite long corridors.

Primary results:

- Cleary–Taback, *Seesaw words in Thompson's group F*, https://arxiv.org/abs/math/0310466 (v2 PDF https://arxiv.org/pdf/math/0310466), Theorem 4.2, excludes a synchronous combing by geodesics in the standard generators.
- Cleary–Elder–Taback, *Cone types and geodesic languages for lamplighter groups and Thompson's group F*, https://arxiv.org/abs/math/0410616, Theorem 30 and its application to F, excludes EVERY regular geodesic language that surjects to F in these generators. This is stronger than merely nonregularity of the full geodesic language. Their Theorems 28–29 also establish infinitely many cone types and nonregularity of the full geodesic language.
- Cleary–Taback, *Thompson's group F is not almost convex*, https://arxiv.org/abs/math/0204249, concerns the standard two-generator word metric.

Precise gap: an automatic structure may use nongeodesic words. A pumping contradiction that uses the requirement that all accepted words are shortest representatives does not apply to an arbitrary automatic language.

An actual counterexample to the missing implication is supplied by Neumann–Shapiro, *Regular geodesic normal forms in virtually abelian groups*, Bull. Aust. Math. Soc. 55 (1997), 517–519, https://arxiv.org/abs/math/9702203, DOI https://doi.org/10.1017/S0004972700034171. They construct a virtually abelian group and a finite symmetric generating set for which NO regular language of geodesic words surjects onto the group. Such a group is nevertheless automatic: finite extensions of finitely generated abelian groups are automatic, and automaticity is independent of generating set. Thus even the strongest conclusion in the preceding paragraph cannot settle the target.

Source-interpretation warning: Wladis, https://arxiv.org/abs/0809.1677, has an abstract phrasing that may appear to deny synchronous combability without qualification. Section 1.2.1 says "by geodesics", and Definition 1.3 restricts the paths under discussion to geodesics. Reading this as exclusion of arbitrary automatic combings changes the theorem.

Status: BLOCKED as a route to all-structures nonautomaticity. Reopen only with a mechanism that controls arbitrary nongeodesic regular combings, rather than importing geodesicity.

### Explicit elementary boundary example: automatic words may have unbounded excess

In Z=<a>, write A=a^-1 and use the regular unique language

    L = (aaA)* union (AAa)+.

The representative for n>=0 is (aaA)^n and for n<0 is (AAa)^(-n). It has length 3|n|. Adjacent endpoints on the same side have identical paths until the shorter word ends; the remaining block deviates by at most 2 from that endpoint. The two remaining edges adjacent to 0 have the same bound. Thus L has synchronous fellow-traveller constant 2, so is an automatic structure with unbounded additive excess 2|n|. Regularity plus synchronous fellow travelling does not force accepted words to be geodesic or uniformly additively close in length to geodesic.

This example is a checkable boundary case, not a claim of novelty.

## Family B: finite-state pumping without geodesicity

The following is a genuine necessary condition and does not assume canonical tree forms.

### Lemma B1 (bounded length change for unique synchronous multipliers)

Suppose L is a regular unique representative language and each padded synchronous relation

    R_s={(u,v) in L x L : eval(u)s=eval(v)}

is accepted by a finite automaton M_s with q_s states, for s in S. Then

    ||u|-|v|| < q_s

for every (u,v) in R_s, with an inessential <=q_s bound also sufficient.

Proof. If the second word has at least q_s extra letters, the accepting run has at least q_s+1 state visits while the first track reads padding and the second track reads letters. Two visits coincide. Pump the intervening nonempty cycle. The result remains a correctly padded synchronous pair with the identical first word and a strictly longer second word. It is accepted, so both different second words represent eval(u)s. Uniqueness in L gives a contradiction. The other length inequality follows by pumping the first track instead. This works for nondeterministic automata by fixing any accepting run. End-of-word padding is essential. QED.

Every automatic group admits an automatic structure with uniqueness. Its construction keeps the shortlex least word within EACH existing equality class in the accepted language; it does not assert that the word is shortlex least among all group words. A standard reference is Bartholdi–Silva, *Groups defined by automata*, https://cmup.fc.up.pt/main/sites/default/files/publications/BS2.pdf, Lemma 1.3 and following discussion.

Consequently an automatic structure would give a proper integer-valued function ell(g)=|nf(g)| with

    |g|_S <= ell(g) <= ell(1)+q |g|_S,
    |ell(gs)-ell(g)| <= q,

and a rational generating function sum_g z^ell(g), because L is regular and unique. Here q=max_s q_s. Finiteness of fibers of ell follows from finiteness of the alphabet.

Exact remaining gap: no theorem is proved here saying F cannot have such a length function, and such a length function alone does not provide multiplier fellow travelling. The rational series concerns normal-form length, not standard word length. A computation of nonrational metric growth would therefore require an additional bridge before giving a negative answer.

Status: PARTIAL NECESSARY CONSTRAINT, currently without contradictory F evidence. A bounded-state search can reject individual candidates; failure at any finite state bound does not exclude all state bounds.

## Family C: infinite abelian rank, cohomological dimension, and CAT(0) dimension

F contains a direct sum of countably many infinite cyclic groups: choose pairwise disjoint dyadic intervals I_i in (0,1), put a nontrivial element f_i supported in each I_i, and use disjoint supports. The f_i commute. If a finite product product_i f_i^n_i is identity, restriction to I_j gives f_j^n_j=1; an increasing homeomorphism of an interval has no nontrivial finite-order element, so every n_j=0. In particular F contains Z^r for every finite r. Cohomological dimension is monotone under subgroups over Z; cd(Z^r)=r. Thus cd(F)=infinity.

What this proves: F cannot have a finite-dimensional K(F,1), nor a free cellular F-CW action on a finite-dimensional contractible CW complex. It prevents the finite-dimensional/cocompact CAT(0) shortcut one sometimes tries to apply.

What it does not prove: an arbitrary automatic group need not come with a known finite-dimensional classifying space. Do NOT replace the standard automatic-group conclusion F_infinity/FP_infinity by finite cohomological dimension.

A primary historical diagnostic is the AIM workshop problem list *Thompson's Group at 40 Years*, https://aimath.org/WWN/thompsonsgroup/thompsonsgroup.pdf, Q4.2: the proposed exclusion of Z^infinity from automatic groups is itself listed as a desired theorem, alongside the question about F. It cannot be imported as an established result. This historical source is used only to identify the logical gap, not to assert a complete 2026 literature status.

F already satisfies the standard F_infinity finiteness condition (Brown–Geoghegan's classical construction). Its infinite-dimensionality is compatible with that condition.

Status: BLOCKED unless an independently proved automatic-group dimension/rank theorem is supplied. Merely restating such a theorem transfers the central difficulty.

## Family D: centralizers, subgroup inheritance, and left/right asymmetry

Gersten–Short, *Rational subgroups of biautomatic groups*, Annals of Mathematics 134 (1991), 125–158, https://annals.math.princeton.edu/1991/134-1/p04, prove closure statements for centralizers of finite subsets of BIAUTOMATIC groups and show polycyclic subgroups are virtually abelian. The hypotheses cannot be changed silently to right automatic groups, nor can "polycyclic" be changed to arbitrary solvable.

The logical reason for the centralizer issue is visible at the automata level. For fixed f, the condition nf(gf)=nf(fg) requires both right multiplication by f and left multiplication by f in a common language. Right automaticity supplies the former and does not supply the latter on that same language. Passing to inverse words gives a left automatic structure on a potentially different language, not a biautomatic structure.

Gill–Short, *Conjugacy, roots, and centralizers in Thompson's group F*, https://arxiv.org/abs/0709.1987, Theorem 7.2, describe C_F(f) as a finite product F^a x Z^b determined by fixed intervals and bump chains. This is consistent with automaticity of F, since automatic groups are closed under finite direct products. This observation produces no contradiction even if a suitable centralizer inheritance theorem were available.

Arbitrary subgroup inheritance is false for automatic groups. Baumslag–Bridson–Miller–Short, *Finitely presented subgroups of automatic groups and their isoperimetric functions*, https://arxiv.org/abs/math/9605201, JLMS 56 (1997), 292–304, DOI https://doi.org/10.1112/S0024610797005395, recall the explicit Stallings subgroup of a product of three rank-two free groups: it is finitely presented but not FP_3, whereas the ambient product is automatic. Their constructions provide further examples. Therefore an embedded nonautomatic wreath/solvable subgroup of F, by itself, is not an obstruction to automaticity of F.

The polycyclic restriction also gives no immediate obstruction: Guba–Sapir's Theorem 21 in https://arxiv.org/abs/math/0005114 implies that a nonabelian subgroup of the interval PL group contains Z wr Z. A polycyclic group cannot contain this nonpolycyclic subgroup, because all subgroups of a polycyclic group are polycyclic. Thus polycyclic subgroups of F are already abelian. A secondary lecture source attributes a stronger automatic-group polycyclic theorem to a Harkins thesis, but no primary thesis was authenticated here; no conclusion depends on importing it.

Status: BLOCKED in current form. An actual all-automatic theorem with applicable hypotheses, plus an incompatible F centralizer/subgroup, is missing.

## Family E: isoperimetry and higher filling

Guba, *The Dehn function of Richard Thompson's group F is quadratic*, https://arxiv.org/abs/math/0211395, Theorem 1, proves delta_F(n) is equivalent to n^2. Corollary 1 gives linear isodiametric function. Thus the ordinary automatic-group quadratic isoperimetric necessary condition is satisfied, not violated.

The AIM workshop list cited above, Q4.3, suggests higher-dimensional filling as a potentially genuine structure-independent mechanism: prove a filling invariant of F grows beyond the corresponding automatic-group upper bound. This suggestion is not itself a lower bound for F.

A precise modern primary upper-bound source is Behrstock–Drutu, *Combinatorial higher dimensional isoperimetry and divergence*, https://people.maths.ox.ac.uk/~drutu/Combinatorial.pdf (manuscript dated 4 October 2017), Theorem 4.8. For a bounded quasigeodesic combing it proves Iso_k(x) <=_coarse x^(k+1), where Definition 3.8 uses spheres of volume at most A x^k. In terms of input volume V this is the Euclidean exponent (k+1)/k. The bounded quasigeodesic-combing hypothesis and the finite-skeleton/universal-cover framework must be checked in each application; an automatic structure can be normalized to a quasigeodesic synchronous combing. Different homological, homotopical, and divergence functions must not be conflated.

Exact remaining gap: this audit has constructed no higher-dimensional spheres/cycles in F with a certified super-automatic lower bound. Flat Z^r subgroups give Euclidean phenomena, not automatically a super-Euclidean lower bound. A lower bound for a subgroup's filling function need not survive in an ambient group, where additional fillings are permitted.

Status: OPEN MECHANISM, no decisive evidence produced. Do not claim that infinite rank alone yields a bad higher filling function.

## Family F: cyclic distortion and roots

This elementary PL argument rules out a tempting shortcut.

### Lemma F1 (uniform positive stable length in standard generators)

For every nontrivial f in standard F, there is a nonzero integer k such that

    |f^n|_S >= |n| |k|  for every integer n.

Proof. Let a be the left endpoint of the leftmost component of the support of f. Since f has finitely many linear pieces and is identity to the left of a, on an interval immediately to its right f has form a+2^k(x-a), with k != 0. The endpoint a is fixed. Thus the right derivative of f^n at a is 2^(nk), also for negative n. Every standard generator or inverse has log_2 slope in {-1,0,1} wherever its one-sided derivative is taken. The chain rule for one-sided derivatives bounds the absolute log_2 slope of any word of length m by m. Apply this to f^n at a. QED.

In particular <f> is undistorted and its stable word length is at least 1. If f=h^r with positive r, f and h have the same support (an increasing interval map has the same fixed set as any positive power), and the same argument gives r<=|k_f|<=|f|_S. Thus each fixed nontrivial f has bounded root degree.

External check: Guba–Sapir, *On subgroups of R. Thompson's group F and other diagram groups*, https://arxiv.org/abs/math/0005114, prove stronger undistortion results for finitely generated abelian subgroups and describe distorted soluble subgroups. These distinctions agree with the elementary cyclic argument.

Status: CYCLIC-DISTORTION OBSTRUCTION FALSIFIED FOR F. No claim is needed that every automatic group has all cyclic subgroups undistorted; even the stronger biautomatic cyclic constraint is already met here.

## Strongest verified conclusion and exact remaining gap

The established obstruction is to regular/geodesic structures in the standard generators, with a separate obstruction even to geodesic synchronous combings. The general step from those obstructions to nonautomaticity is false, as a primary virtually abelian counterexample shows. F satisfies quadratic Dehn, linear isodiametric, F_infinity, and undistorted-cyclic necessary-looking conditions. Finite-state normalization yields a genuine length constraint, but no contradiction has been established.

No all-structures negative solution, affirmative automatic certificate, or novel theorem deciding 21.143 is claimed. A next meaningful advance must either construct a full nongeodesic automatic structure or produce a new invariant/theorem that applies to ALL such structures.
