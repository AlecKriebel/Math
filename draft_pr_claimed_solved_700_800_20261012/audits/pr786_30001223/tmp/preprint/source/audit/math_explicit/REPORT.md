# PR786 explicit polynomial-matrix mathematical review

**Mathematical verdict: PASS. No remaining mathematical issue identified.** Exact target: PR786/problem30001223, immutable original head 34f21454986a28ca49f24999be3a0fd1b42755f8, original budget 1/5 unchanged. This is validation, not an additional proof-search attempt. All 41 original files were independently matched to actual Git objects.

The verified claim is precise: for every odd prime p, k algebraically closed of characteristic p, q=1, r=2p-1 and lambda=(2p-2,1), the source-convention Young module is simple of dimension 2p-2, but I_n(lambda) is nonprojective for every n>=2. The p=3 pair(overline(F3),(4,1)) already refutes the broad positive-characteristic bridge. This does not refute the separate De Visscher–Donkin projective-injective classification or a characteristic-zero nontrivial-root variant. Novelty/priority and present worldwide status are not assessed by this mathematical family.

## Independence and mechanisms

The complete selected record and empty prior report were read first. INITIAL_POSITION.txt was frozen at 11:46:59 UTC before author proof, historical audits, or peer/root mathematical conclusions. INDEPENDENT_DERIVATION.md was then frozen at 11:49:09 UTC, after independent reconstruction from the candidate and primary sources but before historical/peer conclusions. This worker session was reused because new-session creation failed ENOSPC; it was not a newly created session. No peer packet was opened and no peer communication occurred. Eligibility metadata necessarily disclosed an odd-characteristic/all-ranks claimed result. The first initial conjectural route was not assumed to be the candidate.

The main independent mechanism is explicit formal polynomial action: repeated multiplication of linear forms produces coefficient matrices, alongside algebraic-torus weights and formal unipotent coefficient graphs. It uses neither candidate-code imports nor evaluations on a finite group as a substitute for algebraic-group invariance. A second concrete check generates the symmetric-group augmentation action algebra. The analytic all-prime/all-rank argument is in the frozen derivation; finite computations are falsification controls, not an enumeration proof.

## Mathematical reconstruction

The point permutation module splits as constants plus augmentation because p does not divide 2p-1. A nonzero augmentation submodule contains a vector with unequal coordinates; subtraction of a transposition yields a nonzero coordinate difference, whose conjugates span the entire augmentation. This proves simplicity over k. The shape(r-1,1) Specht module consists precisely of those differences and selects the correct Young summand.

The later-inspected historical convention supplement is also sound and can be independently checked. At stable rank N>=r, H=Sym^(r-1)(E_N) tensor E_N is injective. DD's symmetric-power injective decomposition and dominance permit only labels(r),(r-1,1), each with multiplicity 1; for L_N(r), the required weight occurs because the coefficient r of x_1^(r-1)x_2 in a translate of x_1^r is nonzero. Multiplication H->Sym^r splits by polarization divided by r. Its kernel is therefore I_N(r-1,1). The multilinear Schur weight has r basis vectors, all mapped to the same monomial, with symmetric-group permutation action. Its kernel is exactly augmentation, fixing Y=FI labels without conjugation/sign ambiguity. No simplicity of Sym^r in stable rank is assumed.

In rank 2, Sym^(2p-1) is simple because all its binomial coefficients are nonzero modulo p. In B=Sym^(2p-3), the coefficient support W consists of indices 0..p-3 and p..2p-3. It is an invariant simple Frobenius-product submodule. The two omitted weights form a simple quotient, linked in both directions by scalar p-1. Distinct torus characters force a complement to be the span of the two omitted monomials; a nonzero upper coefficient sends one into W, so the extension is nonsplit. After determinant twist the socle label is (2p-2,1) and the head label (p,p-1). They differ even when p=3 and both constituent dimensions are 2.

Costandard reciprocity identifies I_2(lambda) with det tensor B: only the row label strictly dominates lambda, and that rank 2 row costandard is simple with no L(lambda) constituent. The injective has different head and socle, hence is not contravariantly self-dual, so it cannot be projective.

For every larger rank, projective I_N(lambda) would be a tilting T_N(mu). Its highest weight dominates lambda, forcing mu=(r) or (r-1,1), both of length at most 2. DD's exact truncation theorem applies to these actual labels and yields I_2(lambda)=T_2(mu), an injective tilting and hence projective, contradiction. This excludes every permitted rank, not only sampled ranks. It does not assert generic preservation of projectivity or heads under arbitrary idempotent truncation.

## Actual finite checks and attack controls

Fresh independent ordinary Python 3.14 and optimized bundled Python 3.12 runs have identical full output. Repeated-polynomial-expansion matrices give:

- p=3: Sym5 coefficient span 36; det tensorSym3 span 12; simple constituent spans 4 and 4; splitting equations rank 4, augmented 5; endomorphism dimension 1; S5 augmentation generated algebra dimension 16, the full End of its 4-dimensional module.
- p=5: Sym9 span 100; det tensorSym7 span 52; constituent spans 36 and 4; splitting equations 12/13; endomorphism dimension 1; S9 augmentation generated algebra dimension 64.
- Fourteen odd-prime formal graphs through 47 have exactly the stated simple socle/quotient components and the directed obstruction to a complement. These finite primes do not establish the universal prime quantifier.
- The finite-group danger is real: all 48 matrices in GL2(F3) produce Sym5 span 20, below the formal span 36. A finite-field-only certificate would therefore be insufficient.
- The p=2 graph lacks the proposed nonsplit pattern, and the p=3 degree3 augmentation algebra has dimension 3 rather than full 4. These detect illegitimate characteristic/degree extensions.
- Multiplication/polarization was checked on 218 monomials across five small(p,n) cases, including stable rank(p,n)=(3,5). There the Schur weight kernel has dimension 4. Higher-rank row Frobenius submodule dimensions 18<21 and 75<126 detect an invalid transfer of rank 2 row simplicity to higher rank.

Both complete original publication wrappers passed, normal Python 3.14 and optimized Python 3.12, with identical output. They validate 41 files, 3 archives/30 members, all 3 historical gates and nested author 34/first-audit 28/second-review 24 controls in their stated normal/O drivers, including coherently repinned false cases/results. The original decomposition matrix is explicitly derived from the proof and reciprocity; it is not an independent numerical decomposition-number certificate. Our independent section equations, coefficient spans and action-algebra checks corroborate its concrete implications.

## Sources, wording and limits

Fresh primary bodies: actual OWR2009 publisher PDF, printed pp. 945-946 (and contextual 944-947); actual DD2005 dated manuscript, printed pp. 7-12. OWR printed p. 946 and DD printed p. 9 were rendered and visually inspected. Primary hashes and actual locators are recorded; full bodies/images stay outside this flat packet. DD's repository body is an unspecified manuscript version, not silently treated as byte-identical to the final journal article.

The broad Conjecture 7 has no local characteristic-zero or q!=1 exclusion. DD explicitly includes q=1 positive characteristic and defines quantum characteristic as p. The characteristic-zero caution appears later in OWR's separate rational-category method.

One source-wording correction must survive promotion: the selected record calls the index-set statement "equivalently"; actual OWR says "More strongly". The candidate proof correctly separates these. This is not a candidate mathematical repair: the counterexample refutes the first implication directly and excludes membership in the proposed sufficient index sets without assuming classification completeness.

No unresolved mathematical gap remains in this explicit family. General highest-weight reciprocity, projective-injective duality/tilting and precise rank truncation remain explicitly cited standard dependencies. The packet is an AI mathematical review, not external human peer review, a formal proof-assistant certificate, exhaustive priority, or a new solution-search turn. The parent handles persistence/publication and any status wording. No inputs, Git state, native records or external accounts were changed; no individual or agent except the assigning parent was contacted.
