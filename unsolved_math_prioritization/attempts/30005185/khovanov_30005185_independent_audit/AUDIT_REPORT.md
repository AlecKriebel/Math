# Independent adversarial audit: reduced Khovanov rank modulo four

Problem 30005185; queue rank 744; source label OWR-11101915-009. Audit date: 2026-10-05 UTC.

## Verdict

**PASS, scoped to a correct unresolved investigation.** No mandatory mathematical correction was found in the frozen package. This verdict is not a proof of the universal conjecture. Retain the outcome **unresolved / unsolved, five substantive approaches out of five, no knot counterexample, no novelty claim**.

The exact odd-characteristic/rational reduction is valid. Its missing geometric parity statement remains missing. The coefficient-transfer obstruction is valid. All six small-knot controls pass an independently implemented chain-complex calculation, and the audit additionally certifies their integral reduced homology is torsion-free.

## Frozen object and reproducibility

The 20,354-byte author ZIP has SHA-256 c52b643a0fc86a59ca0aa6f21b12f36d92eba1dac66424d4201f27c91bd40052. Its author manifest has SHA-256 df783c4badd6db54bf2655cb8044b0e7ac7a88b249090b6bc3716044ebdf3d70. All 12 archive members match the on-disk files byte for byte; all 11 manifest entries match their declared size and digest. The author's two mathematical receipts replay exactly, as does the author's manifest verifier. A fresh extraction and different-working-directory replay produce byte-identical independent results. The original freeze was not changed.

Seven fresh scholarly PDF retrievals reproduce all seven author-declared byte counts and SHA-256 digests. Only the public retrieval metadata was retained in this audit. No PDFs, extracted source text, raw census files, or private coordination records are included. No remote write was performed.

## Source and hypothesis review

- **Exact problem scope: PASS.** Marengon's [OWR 34/2022 report, printed p.1976](https://ems.press/content/serial-article-files/46971) explicitly weakens the Khovanov parts of its two modulo-eight conjectures to modulo four. The coefficient choices are integral rank and prime fields. The relevant integral rank is free rank; the equivalent rational formulation is correct. Ordinary reduced even Khovanov homology and total rank, rather than unreduced rank or an Euler characteristic, are the objects under discussion.
- **Concordance and known cases: PASS.** The [2023 rank paper](https://arxiv.org/abs/2303.04233), Conjecture 1.3(b), Theorem 1.5 and its Section 4 proof, matches the claimed full smooth-concordance equivalence. The stable-ribbon input is explicitly present there. Theorem 1.8 has the stated rational/odd-prime restriction and credits Lipshitz–Sarkar. Section 6.2 supports the extortion-order-one argument. Section 7 provides the geometric 6_2 local-move obstruction. None of these facts establishes the general conjecture.
- **Graded normal form: PASS.** [Schütz, Section 2.1](https://maths.dur.ac.uk/users/dirk.schuetz/d40.pdf) supplies graded Smith decomposition over the field polynomial ring. Unit factors are contractible and must be discarded. [Sarkar, Section 5](https://arxiv.org/abs/1903.11095) supplies one free tower generated in degree (0,s_F+1), the homogeneous X-primary factors, and their grading shifts. Shifting the quotient reduction down by one gives the author's (0,s_F) free generator. The characteristic exclusion is essential and was respected.
- **Recent-results boundary: PASS.** [Dunfield–Gong, Section 2.8](https://arxiv.org/abs/2512.21825) reports the 582 order-two ribbon examples after computations over Q, F3 and F5. Maximum torsion exponent two ensures an even exponent occurs; it says nothing by itself about the parity of their number. [Lobb's 2026 paper](https://arxiv.org/abs/2602.12692) concerns a rational summand in the T(4,5) concordance class. A summand or a rank lower bound imposes no needed mod-four condition on its complement.
- **Manuscript metadata: PASS within the checked scope.** The arXiv histories display the cited single v1 editions for the 2023 rank paper, the December 2025 Dunfield–Gong paper, and the February 2026 Lobb paper. Schütz's [author publication list](https://www.maths.dur.ac.uk/users/dirk.schuetz/publications.html) supports the journal attribution. The institutional record did not load during this audit, so its exact acceptance/online-date history is not independently re-certified here. The original problem site's earlier 403 and the author's repository searches are historical reports, not fresh audit results.

## Reconstructed mathematical checks

### Odd rank, connected sums, and concordance

The integral Euler characteristic at the unit Jones variable is one. It remains one after extension to any field, so total reduced rank is odd. Reduced Künneth multiplicativity and mirror duality give the square rank for K#(-K), and every odd square is one modulo eight. This proves the stated special family, without identifying arbitrary ribbon knots with that family.

Given the credited stable-ribbon lemma, the two divisions modulo four are legitimate because every rank is odd. If S is slice and R and S#R are ribbon, their assumed residues force the residue of S to be one. If K and J are concordant, K#(-J) is slice, and every unit modulo four is its own inverse. The argument does not invoke the slice-ribbon conjecture or restrict concordance to ribbon concordance.

### The lifted-Lee reduction and its normalization

For a surviving elementary pair d(u)=X^a v, homogeneity gives h(v)=h(u)+1 and q(v)=q(u)+2a. Therefore delta(v)-delta(u)=a-1. Specialization X=0 kills this differential and produces two reduced classes. The free tower produces one class, so r=1+2k.

With D the signed determinant and epsilon=(-1)^(s_F/2), the contributions give

    D = epsilon + 2 sum_{a odd} (-1)^{delta(u)}.

Equivalently, directly reducing this identity modulo four,

    r ≡ D + s_F + 2E (mod 4),

where E counts even exponents with multiplicity. For a slice knot s_F=0 and normalized Fox–Milnor factorization makes D an odd square, hence D≡1 modulo eight. This yields exactly r≡1+2E modulo four. No determinant contribution from an even exponent was overlooked.

The audit's free-degree negative control has free delta one, a single exponent-one pair in source delta zero, determinant one and rank three. It shows that dropping the free-generator/s-invariant hypothesis would make the desired implication false. The author includes that hypothesis correctly. The audit checks 10,922 graded parity configurations, including 2,731 with the slice-compatible determinant residue; these are regression checks of the displayed algebra, not proof by finite sampling.

### Formal countermodels and coefficients

The author's X^2 three-generator complex has the claimed homogeneous differential, split tower, localization behavior, determinant one and reduced rank three. It disproves only the stated package of algebraic sufficient conditions. It is never presented as the complex of an actual knot. No actual ribbon counterexample follows.

For a bounded free integral complex, each p-primary cyclic homology summand contributes once under tensor and once in the adjacent Tor term. Summing gives r_Fp=r_Q+2t_p with cyclic factors counted once, independent of their exponent. Thus an odd t_p changes the residue by two, including p=2. The audit tests elementary integral factors 2,3,4,6,9,10,25 over four prime fields in 1,372 combinations and includes exact rank-drop controls. This does not transport the odd-characteristic lifted-Lee theorem to characteristic two.

## Independent computational evidence

The audit code never imports the author's code. It uses a half-edge graph rather than arc union-find, the marked-circle quotient rather than the marked-x subcomplex, the opposite cube-sign convention, and dense exact row elimination rather than sparse column elimination. The two sign conventions are additionally compared using their explicit degree-wise sign change.

For all six diagrams, integer d squared is zero, normalized differential quantum degree is zero, and exact ranks match every author-reported homological chain dimension, differential rank, and homology dimension over Q, F2, F3 and F5:

- Unknot: rank 1; signed determinant 1
- Trefoil and mirror: rank 3 each; signed determinant -3
- Stevedore: rank 9; signed determinant 9
- Square knot: rank 9; signed determinant 9
- 6_2: rank 11; signed determinant -11

Additional checks cover 200 state partitions by independently wiring the three braid closures, all 100 half-edge basepoints of the five nonempty diagrams over F3, both normalized Reidemeister-I curls, a Hopf-link control and a Reidemeister-II unlink control. The square-knot splice has exactly two inter-half edges, and reconnecting either side recovers the original trefoil or mirror diagram. Every supplied nonempty diagram has exactly one knot component.

The normalized Euler polynomials of the braid controls agree with the mirrored [Knot Atlas trefoil](https://katlas.org/wiki/3_1), [stevedore](https://katlas.org/wiki/6_1), and [6_2](https://katlas.org/wiki/6_2) polynomials. This pins down the harmless global mirror convention more precisely than total ranks alone. It does not claim Jones-polynomial equality proves knot identity. The braid identities remain separately sourced; ribbonness of stevedore is separately sourced, and the square knot has its standard symmetric ribbon construction.

Finally, independent integral cancellation uses only differential entries +1 or -1. Each such pivot is a unimodular chain contraction; the remaining differential is the corresponding Schur complement. Removing the paired generators also removes the appropriate adjacent matrix row and column. All six complexes contract to zero-differential free complexes with the displayed homology ranks. This certifies torsion-freeness and therefore the same ranks over every field for these six examples only.

## Mandatory corrections and limitations

**Mandatory corrections: none.** The author's explicit unresolved status and safety limitations must remain with any use of this audit. In particular:

1. Do not promote the conditional E-parity identity to a ribbon parity theorem.
2. Do not promote the formal countermodels to knot counterexamples.
3. Do not identify maximum X-torsion order with the number of even elementary factors.
4. Do not treat the present small controls as a replay of any published census or as an algorithm deciding ribbonness.
5. Keep the characteristic-two exclusion on the Lee argument and the separate UCT issue.

The search for subsequent work was bounded and dated. Failure to find a resolution is not a proof that none exists. The audit verifies a sound stopped investigation, not a complete solution or a claim of new mathematics.
