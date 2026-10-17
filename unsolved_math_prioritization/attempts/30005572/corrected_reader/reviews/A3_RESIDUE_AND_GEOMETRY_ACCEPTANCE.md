# Independent audit: residue lifting and geometric cocycles

Date: 14 October 2026 UTC. Row 1777 / problem 30005572. This verification is within shared PASS 2/5 and consumes no further mathematical pass. The construction contract and accepted PASS 1 summary were read. No proof, queue, pass ledger, or remote repository was changed.

## Verdict

Accept the mathematical claims of the two pinned notes, with precisely their stated target and compatibility restrictions. No substantive defect was found. In particular, the right end is now proved over R = Z[1/6]; it is not imported from a theorem over Z[1/30]. The original arithmetic construction remains UNSOLVED.

Pinned inputs:

- RIGHT_END_LIFTING.md: SHA-256 ee853634d28da3c9d324f25cc90a7a9d9aed95875bc385782746aad73cf720f4; 18,188 bytes.
- GEOMETRIC_COCYCLES.md: SHA-256 d654d5ebe0ffe14d5fc8b229b72c6ad9de82f299271dafd9c072e0e8bd2ecaa9; 15,176 bytes.
- Accepted PASS 1 CONSTANT_QUOTIENT_REPAIR.md: SHA-256 6943210fbd4d1761d2317e0715491e00688a7a803197d60c6c9c49561f92f9c0.
- Its independent acceptance: SHA-256 512b6424efbd6f3134a673a0d292205659d2fecbeeeda9116a12ce0d9c406ba0.

The PASS 1 left-exact result is an explicitly accepted input here, rather than being reproved or silently strengthened. In particular, quotienting all constants precedes taking trace-fixed parts.

## 1. One-curve integral lifting and normalization

The rational origin removes the potential Picard descent/Brauer problem: the degree-zero divisor-class group is Pic^0(E)(L). Tensoring the divisor/principal-divisor sequences with R is exact. The scalar norm actions are integrally m^2 on constants and m on Pic^0. Hence (T_m-m)(T_m-m^2) really annihilates both groups, including their torsion.

The augmentation numbers (1-m)(1-m^2), for m prime to any prescribed exceptional integer, generate R. For every prime ell at least 5, a nonzero residue different from 1 and -1 exists; CRT realizes it while retaining the prescribed coprimality. Thus there is no common prime divisor outside 2 and 3. A finite Bezout combination is justified in the PID R.

Applying the resulting operator to a divisor class first proves its principality in the tensor group. Applying it to an ordinary primitive then kills every constant norm discrepancy at once. This second step uses commutativity with all CM traces, and therefore establishes full-CM invariance, not merely scalar invariance. The same argument annihilates any fixed constant difference, proving uniqueness and eliminating a possible fifth-root normalization ambiguity. The construction uses tensor-valued functions and does not assert the existence of literal fractional-power functions.

Unit support, exact invariance at every extra trace fixing the divisor, and base-field extension compatibility all follow from this uniqueness. Norms preserve the specified torsion support, and the relevant exceptional monoids can be enlarged together.

## 2. Torsion support and the correct orbit lift

The finite-support argument for a signed invariant measure is valid even with cancellation. Each support point has a support preimage; following predecessors into a repeated point places the original point on the resulting periodic cycle. Periodicity under [m] implies torsion. After selecting a common annihilating ideal n, CRT realizes every unit of O/n by an allowed CM scalar. A fixed cycle is therefore a linear combination of reduced Galois-and-diagonal-unit orbits.

For degree zero, subtracting each orbit's cardinality times the rational origin introduces no orbit-size denominator. The proof does not claim diagonal orbits are products of one-factor orbits.

When all O-linear Hom maps are L-defined, the Hom-ideal argument is correct. For compatible lattices C/a_i, J = a_2 a_1^(-1); a choice alpha nonzero in each J/pJ for p dividing n gives integral kernel ideal alpha J^(-1) prime to n. It gives an L-defined isogeny identifying the n-torsion modules. These modules are free rank one over O/n because an invertible module over that finite semilocal ring is free.

Writing a point as (aU, phi(bU)) places it on the image of T -> (aT, phi(bT)). For a nonzero point this image is an elliptic subvariety B defined over L. It is O-stable, so it contains the entire Galois-and-unit orbit, regardless of whether that orbit is Cartesian. Its rational origin and maximal O-action make the one-curve lemma applicable. Pushing the resulting function from B into the surface Gersten term gives exactly the required orbit-minus-degree-origin residue. This proves all degree-zero right-end lifting, not just the auxiliary e_c cycles.

For general same-type twists, the Galois action on J is O-linear with image in Aut_O(J) = O^×. Its kernel extension is Galois of degree dividing 2, 4, or 6. Transfer divided by this degree is legitimate over R, commutes with traces, and has the correct residue by p_*p^* = [L':L]. No arbitrary extension or class-number denominator enters. Opposite CM types and nonmaximal orders are not asserted to satisfy this general argument.

## 3. Exact norm and pullback formulas

The one-curve identities were checked at the divisor level and then against the normalization lemma. For f with kernel E[a], g = a+c, one has

- f^*[E'[c]] = [E[ac]];
- f_*[E[c]] = Ng [E'[c/g]];
- f_*theta_c = Ng theta_(c/g);
- f^*theta_c = theta_ac - Nc theta_a.

These remain exact when a and c are not coprime. The kernel of f on E[c] is E[g], and the image has annihilator c/g; the degree and origin coefficients agree. Pullback is eventually trace-fixed by the coprime-kernel cartesian square after excluding a. Thus equality is exact, rather than only modulo constants.

Exterior products produce the claimed eta_c and its boundary q^2[0]-[A[c]]. Finite-etale component decomposition handles nonrational torsion without a splitting-field denominator. Its CM-trace invariance follows term by term.

The general product norm formula (6.2), pullback formula (6.4), and diagonal ideal identity (6.5) have the right coefficients. In (6.2), differentiating the first summand produces q Ng_2[0] exterior E'_2[c_2], which cancels the corresponding second-summand term, leaving the displayed q^2 origin coefficient and Ng_1 Ng_2 torsion coefficient.

The sign and factor in (6.6) also check: with u = theta_a,E1 and v = f_2^*theta_c,E2', div(v) = q E_2[a] - E_2[ac] and div(u) = Na[0] - E_1[a]. Expanding q(u exterior div(v) - div(u) exterior v) gives exactly f^*eta_c - eta_ac + q^2 eta_a. The ordinary Steinberg symbol is correctly not declared trace-fixed. A unique trace-fixed replacement is available in the unramified case; in general uniqueness is in the constants quotient.

## 4. Source family and geometric coefficient systems

The retained author-hosted LSSW source, Section 3.1, explicitly supplies L-defined isogenies between every pair E_r, compatible descriptions C/a_r, and the Hom identifications. Its Lemma 3.1.1 proves all isogenies are defined over L once the curves are L-isogenous. Thus the unextended right-end proof applies to every source h^2 product; no hidden class-number-one or same-component restriction appears.

The auxiliary modulus f has injective unit reduction in the source model construction. This does not amount to imposing that restriction on the eventual target level N. No claim of arbitrary-level arithmetic descent follows from that distinction alone.

Combining this right end with accepted PASS 1 gives the full exact augmented complex with coefficient (C_2/C)^tf for all stated source products, and the unquotiented C_2^tf version when 5 is unramified in the maximal CM order. Pushforward commutes with traces. Pullback preserves eventual invariance after excluding its kernel. Constants and their quotient are stable, so these are indeed the required isogeny-module-system sequences.

## 5. Cocycle, Hecke, and regularity claims

The residue difference gamma eta - eta is a fixed C_1 cycle. The relevant injective left-end map gives a unique lift and proves the cocycle identity. Changing eta gives a coboundary. This proves canonical classes with genuine trace-fixed K_2 values when 5 is unramified, and canonical constants-quotient classes for every F. It does not prove that choosing ordinary representatives in the ramified case respects the cocycle identity.

The norm and pullback class identities follow by naturality of this connecting construction with restriction, conjugation, proper transfer, and finite group corestriction sums. No division by a group index is required. Literal equality of representatives is asserted only where the chosen primitives transport exactly. Arbitrary ideal pullback instead has the explicitly calculated boundary correction. The auxiliary-exchange identity expands on both sides to the same four zero-cycles and is therefore valid in these geometric coefficient systems.

The geometric Hecke calculation is the integral incidence count on the two-dimensional O/p vector space A[p]: its Np+1 lines count zero Np+1 times and every nonzero point once. Source double-coset representatives give exactly these lines. Commutation with central ideal pullback then proves T_p e_c = (Np+[p]^*)e_c. The diamond representatives are O-linear isomorphisms preserving origin and c-torsion. These facts justify the corresponding geometric cohomology-class identities. They do not identify the arithmetic bad-level U_p^* operator with T_p or prove U_p^*=1.

For regularity, an element x in c Hom(E_2,E_1) invertible on N-torsion exists by the same invertible-ideal CRT argument when (c,N)=1. The shear kills its displacement on E_2[c] and carries the remaining vertical support to the graph z_1+xz_2=0. Both supports avoid every (0,uP) for primitive proper-level N-torsion. In the source row-vector convention, transformed support is tested by d and c_gamma+dx; both are invertible modulo N for gamma in Gamma_0(N). Thus the residue support is disjoint from the full torsion orbit. The Gersten kernel description on its complement gives regular K_2 classes there (or regular classes modulo constants in the ramified coefficient system).

Evaluation after making a point rational and restricting to its stabilizer is a legitimate geometric pullback. It is not yet the required ray-field descent, integer-ring image, or constant-sensitive arithmetic normalization. The note maintains that distinction.

After extension to Z[1/30], the same one-curve normalization and the same sheared residue identify the constructed objects with the source's geometric auxiliary family by uniqueness. This comparison does not descend an arithmetic theorem backwards across coefficient localization.

## 6. Acceptance boundary

Accepted now: the full stated right-end theorem over R; the exact normalized one-curve theta system; explicit eta_c on every product; canonical genuine geometric cocycle classes in unramified-5 fields; canonical constants-quotient classes in every field; the stated geometric norm, pullback, auxiliary-exchange, Hecke, diamond, and regularity properties in those targets.

Not accepted from these two notes: ordinary or trace-fixed ramified-5 cocycle lifts; canonical constant normalization there; arithmetic ray-field descent; arithmetic removal of c; the integral absolute target; arithmetic bad-U identities; compactification at all levels/components; or the prescribed global relative theta-symbol formula. The separate ramified-5 lifting proof, if completed and audited, will receive a separate pinned supplement. No assertion from its unfinished version has been incorporated here.

## Source verification

The author-hosted source is Lecouturier, Sharifi, Shih, and Wang, *Eisenstein cocycles for imaginary quadratic fields*, https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf . The current public URL was opened during this audit. The retained 47-page PDF has SHA-256 3c50732ecd6f44ad448a9d6d77e7543421ea9c12b4ba497a1ebfc1665df6dcb5; its text has SHA-256 65cb84925a911d3b2863e3fc56cc63a543099bbe19fa1b9babc9b23d4784cf93. Sections 3.1–3.4 (printed pages 19–26), including the family/Hom hypotheses, coefficient convention, geometric Hecke calculation, and shear representative were directly inspected. These comparisons confirm scope and standard setup; the new R-coefficient claims were checked by their arguments above, not imported from the source's Z[1/30] theorem.
