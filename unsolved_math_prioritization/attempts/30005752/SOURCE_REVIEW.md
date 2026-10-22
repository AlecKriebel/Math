# Sources, credit, and acceptance boundaries

Problem 30005752 / OWR-14298157-001 is the divisibility case of Lee–Li–Rupel–Zelevinsky's Conjecture 1.10 on universal positivity of rank-two quantum greedy elements. This edition publishes an authored audit of a source-credited proof of the full original target.

## Credited proof and scholarly status

Qiyue Tang, *A Note on Universal Positivity of Rank-Two Quantum Greedy Elements*, arXiv:2609.37452v1, September 26, 2026, supplies the proof. Its second page discloses generative-AI assistance. The source record inspected during the October 10, 2026 audit established neither journal acceptance nor refereeing of the manuscript. Credit belongs to Tang. No new-proof, discovery, novelty or priority claim is made by this edition.

- [Versioned primary record](https://arxiv.org/abs/2609.37452v1)
- [Versioned primary PDF](https://arxiv.org/pdf/2609.37452v1)

The accepted audit read the complete fifteen-page manuscript and visually inspected mathematical pages 1–14. It checked every named imported result at the statement and proof-interface level in the specified source version. It did not independently re-prove unrelated portions of the long references. Internal mathematical acceptance is not external human peer review, journal acceptance, or formal proof-assistant certification. This AI-assisted audit is also unrefereed.

## Exact accepted target

For all positive integers b,c satisfying b|c or c|b, every integer label (A,N) in Z², every ordered adjacent cluster (Xₘ,Xₘ₊₁), and indeterminate v, the original quantum greedy element has coefficients in Z≥0[v,v⁻¹] in normalized monomials v^(rs)Xₘ^rXₘ₊₁^s. The underlying torus relation is X₂X₁=v²X₁X₂ and X^mX^n=v^(−det(m,n))X^(m+n). Both recurrence branches are required on their overlapping equality boundary, and nonpositive labels are included. Original Theorem 1.9(d) supplies indecomposability only after positivity is established.

The scope is not restricted to finite or affine type, cluster variables, primitive labels, real roots, numerical specialization v=1, or one cluster. The original full lattice Z² is retained. For c=kb and a primitive ray D=(−bp,cq), its actual pairing subgroup is b gcd(p,k)Z. The argument proves positivity at this minimal full-lattice step, then handles positive, negative and zero pairings. Interchanging parameters supplies the other divisibility direction; the original reflection formulas transfer all-label positivity to every ordered adjacent cluster.

## Complete proof-interface chain

The [complete mathematical audit](MATHEMATICAL_AUDIT.md) preserves every proof-interface check, including:

1. The exact original recurrence, positive parts, vᵇ/vᶜ Gaussian parameters, equality boundary, uniqueness and six-case support.
2. Schur division by [k]ₓ/[gcd(M,k)]ₓ: root-of-unity integrality and sl₂ multiplicity differences for the sign; the gcd identity reducing the quantum shift to the full lattice.
3. Framed source-color moduli, stability signs, freeness, smoothness, properness, the ordered-eigenvalue family, extension across collisions, Springer block signs, and the exact centered degree shifts.
4. Uniform bad-framing codimension and compatible stabilization to stack cohomology; the finite-dimensional primitive BPS character and degreewise finite formal characters.
5. The canonical equivariant PBW interface, slope-genericity at noncoprime multiples, zero potential, Euler-form exchange sign, its cancellation by the total-label sign twist, Young invariants and primitive character comparison.
6. Hall factorization order, the right-module/opposite-quiver convention, inverse/opposite-torus homomorphism, color projection, graded dilogarithm parity and the odd factor Ψₜ(−tʲZ)⁻¹.
7. Scattering on the original lattice, incoming Lie-algebra indices, finite broken-line coefficients, classical label transfer, the positive-coefficient support argument, all three chart maps, normalized leading coefficient and divisibility uniqueness.
8. Parameter transposition, every integer label, every ordered adjacent cluster, inversion of v, and the distinction between positivity and its indecomposability consequence.

There is one correction in the original background source: the first horizontal divisor displayed in equation (2.1) of arXiv:1405.2414v1 has a parameter typo. Tang explicitly corrects it to vᵇ. The original recurrence, proof of Proposition 3.7 and direct adjacent-chart expansion agree with vᵇ. This already-audited correction is preserved, not silently changed to vᶜ or presented as a new correction discovered by this edition. No unresolved mathematical gap or new mathematical correction is identified by the accepted audit.

## Primary dependencies and background

All versions and inspected portions below are historical audit findings, with complete PDF identities in [SOURCE_METADATA.json](SOURCE_METADATA.json).

- Lee, Li, Rupel and Zelevinsky, *The existence of greedy bases in rank 2 quantum cluster algebras*, [arXiv:1405.2414v1](https://arxiv.org/abs/1405.2414v1): Definitions 1.6 and 3.1; Theorems 1.7, 1.9 and 5.8; Lemma 2.2; Propositions 3.7 and 5.1; closing proof of Theorem 1.9. The inspected metadata lists Advances in Mathematics 300 (2016), 360–389. This provides the original conjecture and recurrence/support/reflection interfaces.
- Cheung, Gross, Muller, Musiker, Rupel, Stella and Williams, *The greedy basis equals the theta basis*, [arXiv:1508.01404v2](https://arxiv.org/abs/1508.01404v2): Theorem 4.3, Remark 4.5 and Theorem 5.1, including the exact all-label classical transfer T(h₁,h₂)=(h₁+b min(h₂,0),h₂).
- Davison and Mandel, *Strong positivity for quantum theta bases of quantum cluster algebras*, [arXiv:1910.12915v3](https://arxiv.org/abs/1910.12915v3): Sections 2.2–2.3; Theorem 2.13; Proposition 3.1 and Theorem 3.2; equations (26), (28), (30); Section 6.1; Theorems 6.3 and 6.6; Lemma 6.13 and Proposition 6.14. The audit uses the general scattering, transport, Hall, parity and BPS interfaces, without substituting skew-symmetric cluster positivity for the skew-symmetrizable target.
- Davison and Meinhardt, *Cohomological Donaldson–Thomas theory of a quiver with potential and quantum enveloping algebras*, [arXiv:1601.02479v5](https://arxiv.org/abs/1601.02479v5): Theorems A and C; equations (1) and (15); Example 2.11; Corollaries 4.11 and 5.9; Section 6.3. The actual canonical primitive/PBW construction and its Euler-form symmetry are essential.
- Hoskins, *Parallels between moduli of quiver representations and vector bundles over curves*, [arXiv:1809.05738v2](https://arxiv.org/abs/1809.05738v2), Section 2.2: GIT stability sign, generic stability, free effective quotient, dimension and projectivity interfaces.
- Feng, Yun and Zhang, *Higher Siegel–Weil formula for unitary groups: the non-singular terms*, [arXiv:2103.11514v4](https://arxiv.org/abs/2103.11514v4), Section 3, especially Corollaries 3.4 and 3.7 and the proof of Proposition 3.8: block action and sign-support identity in the Betti flag construction over C; no finite-field Frobenius assertion is required.
- Nakanishi, *Pentagon relation in quantum cluster scattering diagrams*, [arXiv:2202.01588v7](https://arxiv.org/abs/2202.01588v7): title/version inspected, retained as background only. It is not a proof dependency and is not treated as a universal greedy-positivity proof.
- Nakanishi's *Classical vs Quantum Pentagon Relations* contribution in *Cluster Algebras and Its Applications*, [Oberwolfach report DOI](https://doi.org/10.4171/owr/2024/2), printed page 77 / PDF page 9: original 2024 workshop target and exchange convention. Relabeling or reversing the seed preserves its symmetric divisibility criterion.

## Finite checks and publication boundary

The independent exact recurrence suite checked 3,718 instances: the 22 divisible ordered pairs with 1≤b,c≤6 and all labels in [−3,9]². It checked 3,050 equality-boundary sites, initial and adjacent coefficient positivity, bar invariance, six-case support, transposition, row/column divisibility and adjacent chart expansions. It inspected 475,912 nonzero initial Laurent terms and 29,306,600 nonzero adjacent Laurent terms. The Schur suite checked 737 admissible partitions through size 12 for k≤6; the PBW sign check covered 12,005 instances. The wall suite independently reconstructed ordered quantum-torus factors through total degree four for eight divisible pairs and (2,3).

The complete audit retains the adverse controls: a negative coefficient invisible at v=1, a negative minimal-full-lattice quotient in the nondivisible case, failure of mere symmetric monomial positivity, failure without the gcd factor, a wrong odd-dilogarithm sign, and the incorrect horizontal divisor. These are finite corroborating diagnostics. They supply neither the universal proof nor a hidden computational premise; the full conclusion rests on the geometric, representation-theoretic and scattering arguments and their checked imported interfaces. No conclusion about uncomputed coefficients follows from enumeration.

This edition preserves the full authored mathematical audit, its summarized diagnostics, the source ledger, and authored acceptance/status/source-review wrappers. Programs, raw computational-output files, generated certificates, datasets, copied third-party source documents/text/images and private coordination are excluded. The report's single distribution sentence is edited to make the absence of programs accurate; three ledger references to internal coordination are replaced with historical verification descriptions. No mathematical section, convention, dependency, sign, normalization, summarized finding or limitation is removed. Original and distributed identities are distinguished in [ACCEPTANCE.json](ACCEPTANCE.json).

Edition preparation checked sealed input identities and editorial/publication integrity. It did not retrieve new scholarly sources, inspect source PDFs anew, rerun the mathematical diagnostics, or conduct a new literature search. Historical source checks do not certify exhaustive literature status. QUEUE.md and unrelated repository content are unchanged; no merge, release, DOI, journal submission or outreach is implied.
