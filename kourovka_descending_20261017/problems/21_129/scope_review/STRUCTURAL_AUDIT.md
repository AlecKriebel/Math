# Independent adversarial audit of the four-pair reduction

**Verdict:** the reduction survives this audit. The full spherical-Artin implication, including reducible diagrams, is equivalent to the four implications for

\[
(F_4,H_4),\quad(D_6,E_6),\quad(D_7,E_7),\quad(D_8,E_8).
\]

This is a synthesis of existing results, not a solution of those implications or a novelty claim. The statement uses Cumplido–Paris's published coarse-type-I assertion in Remark5.2 as an existing input. The audit checked source statements and their applicability; it did not reprove all cited rigidity theorems or audit all computations in the noncommensurability papers.

## Exact formulation

For a connected spherical Coxeter diagram T, write A_T for its Artin group, P_T for its pure Artin subgroup, and

\[
Q_T=P_T/Z(P_T),\qquad \overline A_T=A_T/Z(A_T).
\]

These two central quotients must not be confused. Let \(\mathcal E\) be the four unordered pairs displayed above. Consider:

- **Full implication:** for all spherical diagrams Γ, Ω, including disconnected diagrams, \(A_\Gamma\simeq_{qi}A_\Omega\Rightarrow A_\Gamma\sim_{comm}A_\Omega\).
- **Four implications:** for each \(\{X,Y\}\in\mathcal E\), \(A_X\simeq_{qi}A_Y\Rightarrow A_X\sim_{comm}A_Y\).

The two assertions are equivalent. This equivalence does not require that the four commensurability comparisons remain open today. A positive commensurability result for a pair would make its implication automatic. Noncommensurability alone would leave the required quasi-isometry exclusion unproved.

## Checkable proof of the reduction

**1. Finite-index decomposition.** If Γ has p connected components and k have at least two vertices, the pure subgroup has the model

\[
P_\Gamma\cong\left(\prod_{i=1}^{k} Q_{T_i}\right)\times\mathbb Z^p.
\tag{1}
\]

For an A1 component, its pure group is infinite cyclic and its Q-factor is trivial. Every other Q-factor is nontrivial, centerless, finitely generated, and torsion-free: it is a direct factor of the corresponding pure Artin group, hence embeds in a spherical Artin group. The center equality and splitting are precisely [Cumplido–Paris Proposition3.1 and Corollary3.2](https://ems.press/content/serial-article-files/39000?nt=1), printed pp508–509. Torsion-freeness also follows from finite integral cohomological dimension.

**2. Recover the product factors geometrically.** CP Remark5.2, printed pp514–515, asserts coarse typeI for every nontrivial Q-factor in (1). Thus [KKL TheoremB](https://math.nyu.edu/~bkleiner/kkl.pdf), manuscript pp2–3, applied to Cayley graphs gives equal p, equal k, and, after permuting indices,

\[
Q_{T_i}\simeq_{qi}Q_{U_i}\quad(1\le i\le k).
\tag{2}
\]

The Euclidean dimension in this application is p, not the number of A1 components. The latter is p−k and is therefore recovered too. KKL does not require the entire quasi-isometry to lie at bounded distance from a product map; Remark1.4 explicitly warns against that stronger assertion when Euclidean factors occur. Only the factor conclusion (2) is used. Empty products are harmless; the empty diagram gives the trivial group, which is not quasi-isometric to any nonempty spherical Artin group. Purely abelian cases are also settled directly by the growth degree of \(\mathbb Z^p\).

**3. Recover each component's rank.** Taking the product of (2) with \(\mathbb Z\), and using Step1, gives

\[
A_{T_i}\simeq_{qi}Q_{T_i}\times\mathbb Z
\simeq_{qi}Q_{U_i}\times\mathbb Z\simeq_{qi}A_{U_i}.
\]

Each spherical Artin group has finite integral cohomological dimension equal to its diagram's number of vertices (recorded with its original reference in CP Proposition2.1). Quasi-isometries in both directions are uniform embeddings, so [Sauer Theorem1.2(i)](https://arxiv.org/pdf/math/0312129v2), p2, gives equality of these ranks. This uses finite cd on both sides and does not claim that equal rank alone implies quasi-isometry.

**4. Mapping-class factors force commensurability.** The Q-factor for A_n, n≥3, is a finite-index subgroup of the mapping class group of \(S_{0,n+2}\): CP Lemma6.4 identifies it with the pure mapping class group. Its complexity is n−1≥2. The Q-factor for D4 has finite index in the mapping class group of \(S_{1,3}\), of complexity3. More precisely, [Soroko Theorem5](https://arxiv.org/pdf/2009.10471v4), pp5–6, identifies **\(\overline A_{D_4}\)** with the pure mapping class group; Q_D4 is its torsion-free finite-index subgroup. The B_n factors are commensurable with the A_n factors by the existing A_n/B_n commensurability theorem and the central splittings.

Here is the finite-kernel argument without a centerless shortcut. Suppose a torsion-free Q_T is quasi-isometric to one of these mapping class groups M. The **complete** [BKMM Theorem1.2 in §10](https://msp.org/gt/2012/16-2/gt-v16-n2-p05-s.pdf), printed p875, gives a finite-index subgroup K<Q_T and a homomorphism

\[
K\longrightarrow M/Z(M)
\]

with finite kernel and finite-index image. Since K is torsion-free, that finite kernel is trivial. Also Z(M) is finite, and a torsion-free finite-index subgroup L≤M supplied by Q_A_n or Q_D4 meets Z(M) trivially. Thus L injects with finite-index image into M/Z(M). Hence Q_T is commensurable with L and with the relevant Q-factor. Multiplying finite-index isomorphisms by \(\mathbb Z\) lifts commensurability to the original irreducible Artin groups. This avoids the invalid general inference that a finite-kernel map alone gives abstract commensurability.

The complexity2 case is essential for A3 versus H3. BKMM's shortened introductory statement is insufficient, but its complete theorem explicitly handles complexity2, including the S1,2 exception through S0,5. Our target surface there is S0,5. Rank2 is handled by the existing dihedral commensurability result and does not need BKMM.

**5. Exhaust the finite-type list.** Equal-rank irreducible types are:

| Rank | Types | Pairs left after Step4 and existing commensurability results |
|---|---|---|
| 1 | A1 | None |
| 2 | A2, B2, I2(m), m≥5 | None: all are commensurable |
| 3 | A3, B3, H3 | None: A3~B3; mapping-class rigidity settles any QI comparison with H3 |
| 4 | A4, B4, D4, F4, H4 | F4/H4 only |
| 5 or ≥9 | A_n, B_n, D_n | None: A_n~B_n; the other comparisons have a mapping-class entry |
| 6, 7, 8 | A_n, B_n, D_n, E_n | D_n/E_n only |

Existing noncommensurability results can equivalently turn Step4 into quasi-isometry exclusions; these are CP Theorem2.4 and Soroko Theorem1. They are not assumptions that quasi-isometry always implies commensurability. If the four implications hold, every matched pair from Step2 is commensurable. Their finite-index quotient isomorphisms, multiplied together and with \(\mathbb Z^p\), make (1) commensurable on both sides. The A1 components match because p−k matches. This proves the full implication. Conversely, the full implication includes the four irreducible pairs, so it proves all four implications.

## Adversarial checks and exact boundaries

| Attempted falsifier | Finding |
|---|---|
| Read CP Remark5.2 as arbitrary QI⇒commensurability | Invalid reading. Its final algebraic paragraph starts with a finite-index isomorphism. The proof above uses only its coarse-type-I input and KKL's geometric factor conclusion. |
| Euclidean shearing breaks factor matching | No. KKL explicitly allows shearing while retaining the projections to matched non-Euclidean factors. |
| Forget A1 components | Would be a real scope error. Formula(1) and p−k retain them. |
| Apply acylindrical hyperbolicity to A1 | Invalid. Calvez–Wiest §2.2 excludes the abelian case by assuming a Coxeter edge. A1 is separated before applying coarse typeI. |
| Replace Q_T by \(\overline A_T\) in the finite-kernel argument | Invalid: the latter can have torsion, including D4. The pure splitting supplies torsion-free Q_T. |
| Apply only BKMM's introduction to A3 | Insufficient. Use full §10 theorem, printedp875. |
| Treat D4 as a sphere-type braid quotient | Incorrect. Its surface is the three-punctured torus; the complete theorem applies there. |
| Infer rank from commensurability before proving it | Avoided. Sauer gives the rank equality directly from QI and finite cd. |
| Infer a novel solution from the finite reduction | Unsupported. None of the four residual implications is proved by this audit. |

The Artin-specific coarse-type-I assertion was checked against its precise published location and its cited mechanisms: [Calvez–Wiest Theorem1.3](https://arxiv.org/pdf/1606.07778v2) supplies acylindrical hyperbolicity for the nonabelian irreducible quotient, and [Sisto Theorem1](https://arxiv.org/pdf/1310.7753v1) supplies Morse elements; KKL Proposition4.2 is the cited cone mechanism. These additional two PDFs and hashes are preserved in `sources/SOURCE_MANIFEST.json`. This audit does not replace CP's published derivation with an independently complete new proof of coarse typeI.

**Strongest verified result:** the four-implication equivalence above is justified by the stated published inputs. No central difficulty is transferred to an unstated stronger claim. **Exact discovery gap:** establish or refute each of the four implications; any negative answer must exhibit both quasi-isometry and noncommensurability for the same pair. Current literature completeness and priority beyond the supplied audit were not established here.
