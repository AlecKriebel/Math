# Acceptance report: Farb Question 7.6

This is an AI-assisted, unrefereed mathematical draft. Acceptance means an internal AI mathematical audit found the stated argument valid with the explicit standard imports; it is not human peer review or formal proof-assistant certification. This is a prose proof-and-audit edition, not a computational reproduction package. No novelty, priority, or worldwide-current-openness claim is made.

## Accepted mathematical conclusion

The complete proof answers the stated bounded-multiplicity question negatively for every fixed g >= 2 and k >= 3, counting ambient orientation-preserving Mod_g-conjugacy classes of pseudo-Anosovs belonging to I_g(k). For every N, one spectral value has at least N such classes. Both g and k, and the subgroup H, are fixed independently of N.

The independent audit's verdict is PASS_WITH_EXPLICIT_STANDARD_IMPORTS. No fatal gap or required mathematical repair was found. The final proof adopted the audit's optional simplification: use the unique invariant Teichmüller disk directly to force every relevant ambient conjugator into the full disk stabilizer. The audit's complete Nielsen–Schreier/Hopf justification that the two generators form a free basis remains in AUDIT.md.

## Dependency ledger and logical checks

1. Separating filling pairs exist for every g >= 2 (Farb; Aougab–Taylor Lemma 2.2). The pair is fixed throughout. Its even intersection n satisfies n >= 4.
2. The single-pair Thurston rectangle construction gives congruent squares and faithful two-parabolic derivatives. For n > 2, the only nonhyperbolic nonidentity words are conjugates of powers of the two twist generators (Leininger §5.1, Lemma 6.3, Theorem 6.1 and Proposition 6.4).
3. Johnson centrality puts the jth lower-central subgroup of the twist group inside I_g(j), with the declared indexing (Farb–Leininger–Margalit, proof of Proposition 4.8).
4. Signed saddle holonomies span a rank-two lattice preserved by the entire affine derivative group. Area preservation gives determinant one. No finite-index assertion for the full disk stabilizer or the twist subgroup is used.
5. The fixed iterated commutator u_k and its B-conjugate v_k are noncommuting, form a free basis of H, and have zero abelianization. Every nontrivial word in H is pseudo-Anosov.
6. The faithful derivative image J lies in the index-six free subgroup [PSL_2(Z),PSL_2(Z)]. The finite covering core bounds ambient conjugacy fusion by 6|V(Y)|. Proper powers require no extra factor.
7. A pseudo-Anosov has a unique invariant Teichmüller disk, and its disk stabilizer consists of affine mapping classes (Leininger Theorems 3.1–3.2, importing Bers). Thus ambient conjugacy implies conjugacy in the integral derivative group; the full derivative kernel is harmless.
8. Horowitz Example 8.2 supplies 2^m pairwise nonconjugate nonidentity words with universal equal trace. The fixed free representation lifts to SL_2(R); hyperbolicity gives |t_m| > 2 and common dilatation (|t_m| + sqrt(t_m^2-4))/2. The lower bound ceil(2^m/(6|V(Y)|)) tends to infinity.

## Boundaries

The standard Teichmüller and Johnson-filtration imports are not independently reproved from first principles. The original Bers paper was not separately inspected; the theorem as explicitly restated by Leininger is the checked source. Full PDF retention and hash agreement establish byte identity, not truth or complete page inspection. The optional finite checks are not premises of the theorem, and the audit did not execute them.

No primitivity claim, infinite multiplicity at one fixed value, answer to simple-length-spectrum Question 7.7, external human review, formal certification, novelty, or worldwide-openness certificate is asserted. The bounded source-context and duplicate checks are informational. Publication preparation adds no new mathematical theorem or computational proof.
