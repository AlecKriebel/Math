# Substantive turn 4: displayed mutation cubes and the small-knot candidate gate

## 1. Research question and outcome

This turn tried to obtain an actual mutant pair by combining recent certified low-crossing unknotting improvements with mutation tables, and to determine which part of a crossing-search certificate can be transferred. No pair with different ordinary unknotting numbers was certified. The new retained statement is exact covariance of the entire crossing-resolution cube of a mutation-visible diagram, rather than a claim that a search restricted to such diagrams computes the unrestricted invariant.

The concrete four-knot Bernhard–Jablan construction fails the candidate gate: its knots are crossing-change neighbors, not a specified mutant family. Using the numbering conventions on Stoimenow's primary table page, none of 12n288, 12n491, 12n501, or 13n3370 occurs in the downloaded through-13 mutant groups. This is a reproducible statement about that table, not a proof that these knots have no other mutants, or an independently verified classification of all small mutants.

## 2. Resolution-cube theorem

Let D be a diagram displaying a Conway mutation: a planar disk contains one two-string tangle, the complementary diagram contains the other, and their four endpoints have the usual compatible markings. Write D^rho for the diagram obtained by one of the three ordinary spatial half-turns of the first tangle. Label the crossing set C of D and let phi:C -> C^rho be the geometric crossing bijection. There are no crossings on the separating circle.

For each subset A of C, switch precisely those crossings, and denote the resulting diagram by D_A. Then

(D_A)^rho = (D^rho)_{phi(A)}

as marked tangle diagrams up to the harmless diagram convention for the rotated view. Indeed, switching over/under information in a crossing ball commutes with the spatial rotation of that ball, while all outside crossing balls are unchanged. Endpoint connectivity is unaffected by any of these switches, so all these diagrams remain knots.

Consequently the following two Boolean functions agree under phi:

- f_0(A)=1 if and only if D_A is an unknot;
- f_1(A)=1 if and only if u(D_A)=1.

The first uses the classical preservation of the unknot by Conway mutation; the second uses Gordon–Luecke Theorem 7.1. Both implications are biconditionals because mutation is an involution. No claim is made that u(D_A) itself is preserved when it exceeds one.

In particular, the two multiaffine polynomials

P_j(D;x)=sum_{A subset C, f_j(A)=1} product_{c in A} x_c, j=0,1,

are carried to P_j(D^rho;x) by relabeling the variables. These are invariants of this paired displayed cube, not invariants of an unmarked knot. It follows that the number of unknotting subsets of every given size, every nonnegative crossing-weight minimum over them, and the diagram unknotting number

u(D)=min{|A|:D_A is an unknot}

coincide for D and D^rho. More generally the complete set of certificates entering the u=1 shell agrees, with crossing labels retained.

This proof applies even if a switched diagram makes the chosen Conway sphere inessential. Mutation is still the defined half-turn operation, and the unknot and u=1 preservation statements do not require the sphere to remain essential.

## 3. The remaining minimization is exactly the issue

For a fixed marked knot-and-sphere pair (K,S), let D(K,S) consist of all diagrams displaying that pair as two tangles, allowing isotopies that transport the marking. Define

m(K,S)=min{u(D): D in D(K,S)}.

The set is nonempty and the minimum is finite: a generic marked tangle projection exists, and changing crossings to a descending knot diagram unknots its underlying knot. Rotation bijects this entire class with D(K^rho,S), so the cube theorem gives m(K,S)=m(K^rho,S). Ordinary u(K) <= m(K,S).

Thus a strict mutant disparity would force a failure of sharpness on at least one side. If u(K)<u(K^rho), then

m(K,S)-u(K) >= u(K^rho)-u(K)>0.

Conversely, proving u(K)=m(K,S) for every marked pair would prove mutation invariance. The cube theorem supplies no such localization result. In particular, the disjoint surgery link in turn 3 is disjoint from its own crossing balls, not necessarily from the preselected mutation sphere. This is precisely the missing compatibility.

This minimum uses diagrams of the specified marked pair. Replacing it by all diagrams of the underlying knot and forgetting the sphere would silently assume the conclusion. In fact universal sharpness is false: Gordon–Luecke Theorem 8.2(2) supplies an EM-knot K with u(K)=1 and an essential Conway sphere S such that no unknotting arc is disjoint from S. If m(K,S)=1, the witnessing displayed crossing ball would give just such an arc. Hence m(K,S)>=2>u(K)=1. Its mutant still has u=1 by Theorem 7.1. Thus a positive localization defect, even a genuine one in a knot, is insufficient by itself to give unequal mutant unknotting numbers. The target is a difference of defects, not merely their existence.

## 4. Actual candidate and computational-bound checks

Brittenham–Hermiller, arXiv:1705.05985v2, Theorem 1.3 and Sections 2.3–2.4, establish:

- u(13n3370)<=2 by an explicit 20-crossing presentation with a crossing change to 11n21;
- the three 12-crossing knots 12n288, 12n491, 12n501 are crossing-change neighbors of minimal diagrams of 13n3370;
- the weak Bernhard–Jablan number of 13n3370 is 3, while the three neighbors have strong/weak Bernhard–Jablan numbers 2.

These are not assertions that any two of those four knots are mutants. The exact table screen uses Stoimenow's explicit offsets: 12 has 1288 alternating knots, so the three combined indices are 1576,1779,1789; 13 has 4878 alternating knots, so 13n3370 has index8248. All four are absent from the corresponding pinned lists. The through-12 and 13 files contain 91 and 774 groups, respectively. The table explicitly ignores the choice of mirror; this is harmless for ordinary u but does not supply an oriented marked identification.

Lee's September 2026 preprint arXiv:2609.09861v2, Theorem 5.1, now reports that all four ordinary unknotting numbers are 2. Its lower-bound mechanism uses branched-cover correction terms, with every candidate labeling/orientation checked; the upper bounds are the cited constructions. This turn read the proof description, but did not rerun the external state-enumeration code or certify the full preprint computation independently. Even accepting its result, four equal values give no separating mutant pair. The 959 alternating [2,3] cases in its Section 5.2 are explicitly still unresolved, despite exhausting crossing changes in minimal diagrams. They cannot be entered as exact value3.

There is a rigorous general reason to keep such bounds separate. Brittenham–Hermiller Theorem 1.2 refutes the claim that some crossing in a minimal diagram always lowers ordinary u. Earlier Nakanishi/Bleiler examples already distinguish u(D) from u(K). Taniyama's Theorem 1.2 gives diagrams of any fixed nontrivial knot with arbitrarily large u(D). These are credited results, not new deductions here; the last theorem concerns arbitrary diagrams and does not by itself prove a failure for minimal diagrams.

## 5. Checks and remaining goal

The self-authored checker exhausts Boolean label-permutation covariance in small cubes, including weighted and cardinality minima. This checks the finite combinatorial consequence, not knot recognition or Gordon–Luecke's theorem. A separately pinned source-screen receipt records the parsed DT-table sanity checks and the four absent combined indices. No external program was executed, no numerical knot identification was promoted to a theorem, and no computational upper bound was treated as exact without a lower-bound proof.

Four substantive turns are now recorded. The final turn will pursue a mutation-sensitive lower-bound/upper-certificate mechanism beyond the fixed visible sphere, or isolate a precise obstruction in a different prospective family. The original question remains open in this attempt.
