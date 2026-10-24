# Fresh adversarial audit of the arithmetic approach to 21.135

Checkpoint: **2026-10-24T18:12:13Z**. Review completion: **100% of the supplied arithmetic package**. The author's discovery estimate remains **12%**; this is not a probability that the open problem will be solved. Outcome: **no outstanding substantive mathematical objection to the explicitly restricted claims**. The original unrestricted problem remains unresolved, and this report supplies neither a priority certificate nor a publication recommendation.

I did not author the reviewed proofs. I read the root `AGENTS.md`, the full 21.135 statement in `PROBLEM.md`, `arithmetic/research_notes.md`, the arithmetic verifier and JSON, the source manifest, and the later `followup_20261024.md` and spectrum-quotient filter. I attempted to falsify the hypotheses and numerical boundaries rather than infer correctness from the author's passing script. I did not import or execute the author's verifier. All new files are confined to this review directory. No external outreach, Git operation, publication, or tracker change was performed.

## 1. Original problem and admissible conclusions

The input is the multiset of ordinary complex irreducible degrees of an arbitrary finite group. Neither character kernels nor a Hopf structure is given. A set of degrees, codegrees, or the full character table cannot silently replace this invariant. The question asks preservation of a trivial solvable radical for all reference groups with that property. Every theorem accepted below is a restricted certificate or an obstruction to an attempted proof, not a resolution of that universal question.

## 2. Line-by-line deductions

**Itô and the lcm defect.** The primary 1951 theorem says every irreducible degree divides the index of each maximal abelian normal subgroup. Extending a given abelian normal subgroup to such a subgroup proves the version used in Lemma 1. Thus its order divides `delta=|H|/lcm(cd(H))`. A nontrivial solvable normal subgroup does contain a nontrivial elementary abelian subgroup minimal among H-normal subgroups: use the last nonzero derived term and then minimality. Consequently `delta=1` excludes the entire radical, not merely the center. The product formulas are valid despite collisions among product degrees; maximal valuations add. For odd PSL2(q), q>5, q and q±1 occur; the half degree divides q±1. The explicit q=5 exception is correctly retained. No q=2 or q=3 simple-group assumption is made.

**Central masses and determinants.** A central C_p has p central-character blocks of equal algebra dimension |H|/p. If it is contained in H', every representation determinant is trivial on it, so a nontrivial central character forces p to divide the representation degree. This proves the mass inequality, the square-gcd condition, and p^3 dividing the order. The bounded subset-sum equation is only a necessary condition and is correctly so described. If the central C_p is not contained in H', its faithful linear character extends through H/H'. Tensoring by that character has every orbit length divisible by p, even when its own order exceeds p. If m(1)=p, its order is p and the claimed direct-product splitting follows. I found no hidden order-p assumption in the general orbit argument.

**Perfect-group certificate.** A homomorphic image of a perfect group is perfect. A perfect subgroup of a solvable GL_a(p) is trivial. Therefore each eligible minimal elementary abelian normal subgroup is central, and minimality then forces its rank to be one. This is precisely where the solvability bounds matter; replacing them by mass excess alone is false. The independently computed GL2(2) and GL2(3) derived-series orders are respectively 6,3,1 and 48,24,8,2,1. Arbitrary GL1(p) is cyclic. No assertion concerning GL3(2) or higher general ranks is accepted.

**The infinite A7 product family.** I reconstructed the A7 degrees and both masses. For q=2^f, f≥2, elementary expansion of the stated degree multiplicities gives

    alpha_2 = 1-q/(q^2-1),
    alpha_3 = (q+3)/(2(q+1))       if q=1 mod 3,
    alpha_3 = 1/2+1/(q(q-1))      if q=-1 mod 3.

The first expression is increasing for integer q≥4 and has minimum 11/15. The other expressions exceed 1/2. Multiplication with the A7 masses gives exactly the strict inequalities needed by the certificate, and delta remains 12. This establishes the stated restricted theorem for every f, not just the finite examples. It neither implies arbitrary products nor has established originality.

**The affine barrier.** The group V⋊SL2(4), V=F4^2 additively, is an actual finite group, not a formal spectrum. The natural and dual nonzero orbits both have size 15, and the dual stabilizer is C2^2. An invariant linear character of V extends to its inertia subgroup because this subgroup is split. Little-group induction then gives the four degree-15 characters, together with the inflated A5 characters. The natural module is irreducible over F2 by transitivity and has [V,S]=V; S is perfect. The radical is exactly V because the quotient is simple. All conclusions about this barrier are sound. No radical-free degree twin has been constructed, so it is not a counterexample to 21.135.

**The PSL2(16):C2 tensor root.** Multiplication by 4 has three fixed sign-pairs and two two-cycles modulo 15, and four two-cycles modulo 17. Cyclic-quotient extension and induction give the claimed spectrum `{1^2,16^2,17^6,30^4,34^2}`. Its order is 8160, lcm 4080, and multiplicity gcd 2. The derived-central quotient equation has no solution: after dividing by four it is `64a+225b+289c=586`, with a=0..2, b=0..4, c=0..2. This was independently exhausted. The outside-derived case would split C2×K with the displayed normalized packet. That packet is an associative algebra specification only; its existence as a group algebra is not inferred.

The later quotient filter is also valid. Inflation makes every quotient spectrum a submultiset, and a quotient of a perfect group is perfect. Independently enumerating divisor orders and bounded square sums leaves only orders 1 and 4080. Thus any actual realizing K would be simple. This conditional deduction does not construct K. The cited prior recognition theorem for almost simple PSL2-socle groups indeed has equality of degree **multisets** as its hypothesis, and applies to the original 8160-order example. It removes this candidate without resolving the general problem.

**Socle divisibility and the large-prime barrier.** Clifford restriction gives L(N) dividing L(G), hence delta(G) dividing [G:N]delta(N). It is not necessary that N be a direct factor. A radical-free socle is a product of nonabelian simple groups. Granville–Ono Corollary 2 has only 2- and 3-prime exceptions, so its stated p≥5 use is correct. The resulting bound controls the socle quotient and does not assert a p-defect-zero character for an arbitrary radical-free overgroup.

For every prime p≥5, let q=p^p. The p-th power Frobenius has order p on F_q and induces an outer field automorphism of PSL2(q). The only p-divisible ordinary degree of the socle is its Steinberg degree q; its p-valuation is p, and it is field-invariant and extends through the cyclic quotient. All characters over it have degree q. All other socle degrees are prime to p and acquire at most one additional p factor by index-p Clifford theory. Thus the maximum p-valuation in the extension is p, while its order has valuation p+1. Since delta divides p, delta is exactly p. This proves the theoretical family, including primarity and field-action order. The large numerical examples in my check are specializations of this proof, not computed character tables of enormous groups.

## 3. Independent computation and exact scope

Run `python3 independent_checks.py` from this directory; its output is `independent_results.json`. The script uses only Python's standard library and does not read the author's Python code as a module. It:

- Reconstructs the dimensions of symmetric-group modules by Young branching, rather than hook lengths, and then applies the standard alternating-group restriction rule. It matches every recorded A_n arithmetic entry for 5≤n≤32.
- Reconstructs both even-field semidirect spectra by union-find on the full nonzero parameter sets, under sign and field multiplication, rather than the author's canonical-pair orbit loop.
- Rechecks all nine finite A7 product certificates and both central-block arithmetic obstructions.
- Constructs every determinant-one 2×2 matrix over F16 and the order-two fourth-power field action. The chosen generators generate all 4080 socle matrices; none of the 4080 possible inner implementers realizes this field action. The semidirect product has order 8160 and exactly 16 conjugacy classes. This corroborates the character count without deriving the entire character table from matrices.
- Independently constructs the F4 affine group of order 960, checks generation of SL2(4), the dual orbit and elementary abelian stabilizer, and the full module commutator set. It finds exactly nine affine conjugacy classes.
- Computes the complete derived series of GL2(2) and GL2(3) from finite commutator sets.
- Reconstructs the 48 tensor-root quotient packets by bounded-sum dynamic programming, followed by divisor filtering. The only surviving quotient orders are 1 and 4080.
- Verifies all four local primary-PDF byte counts and SHA-256 checksums against the source manifest.

The finite group constructions are actual matrix or affine groups. Their claimed degree spectra additionally depend on the ordinary PSL2 character classification and Clifford/little-group arguments explicitly reviewed above. The normalized tensor-root packet has **no actual group certificate**. No GAP/Sage run or independent human verification is claimed.

## 4. Primary dependencies and priority limits

I inspected the cached primary statements of Itô (1951), White §4 (2011), Granville–Ono Corollary 2 (1996), and Malle–Navarro–Robinson Theorems 3.6–3.7 (2016). The latter's almost-simple, cyclic p-power abelianization conditions are essential and correctly retained in the follow-up. It confirms that the defining-characteristic field-extension obstruction lies in known defect-zero territory; it is not a theorem about arbitrary radical-free groups.

I independently opened the primary Heydari–Ahanjideh paper, *Almost simple groups with the socle PSL(2,p^n) are determined by their complex group algebras*, Publ. Math. Debrecen 91 (2017), 467–487, DOI 10.5486/PMD.2017.7797. Theorem 1.2 and Corollary 1.3 explicitly recognize these groups among all finite groups from the multiset/complex algebra. Primary URL: https://publi.math.unideb.hu/paper/2188/download/10_5486_PMD_2017_7797.pdf . Its existence is not a new finding of a solution to 21.135.

I have not established priority of every combined restricted certificate, and do not certify that the notes contain a publishably original theorem. No full-problem conclusion survives merely by identifying a smaller class where the radical is excluded. The precise surviving obstruction is the arbitrary noncentral elementary abelian minimal normal module in a comparison group, together with the absence of any mechanism that reconstructs character kernels or a finite group basis from the degree multiset alone.
