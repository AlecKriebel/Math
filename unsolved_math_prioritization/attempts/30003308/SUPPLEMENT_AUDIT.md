# Independent audit of the principal-matrix proof supplement

## Decision and exact boundary

**ACCEPT THE CORRECTED SUPPLEMENT AS A CORRECT, SELF-CONTAINED FINITE WITNESS SUPPLEMENT TO THE BOUNDED PARTIAL RESULT.**

The accepted input is `PROOF_SUPPLEMENT.md`, exactly **5,543 UTF-8 bytes**, SHA-256:

`ed093c9161041818e5f6d41ac487f2170ee269fc8f84fe600fafc32d13512efe`.

This is a new independent review of the supplement. The original mathematical audit, identified by manifest SHA-256 `5cdb57536325ac3a6af278c0bf09365a2cd9e0028579be9059a61a67561aac3b`, predates it and does not retroactively cover it. The original manifest identity was verified. The accepted original manuscript and audit were used for context. The subsequently available proof-only `PROOF.md` was inspected for the referenced matrix B, Lemmas 2–3, Theorem 4, and scope; those references supply their stated definitions and analytic arguments.

The supplement's frozen sentence saying independent review is pending is historical. This separate, hash-bound report supplies the completed review without modifying those input bytes. No blocking defect remains in the corrected supplement. This report does not certify the surrounding publication packaging, remote publication, novelty, an exhaustive literature search, external human peer review, or formal proof-assistant verification.

## 1. Defect found and exact correction

The initial input was 5,544 bytes, SHA-256:

`4d727615aff49720b93e718460b0566fbd44918d7da055060f24eceb144cd7e1`.

That version is **not accepted unchanged**. Its displayed first-row determinant expansion used incorrect cofactors. Although `(-4)(-44) + 39 - 108` happens to equal 107, those three coefficients do not arise from the displayed minor. The independently computed signed first-row cofactors of that minor are

    (-48, -22, -23, -62).

Thus its actual first-row expansion is

    (-4)(-48) + 0(-22) + 1(-23) + 1(-62) = 107.

The corrected sentence `(-4)(-48) - 23 - 62 = 107` is valid. The independent checker caught the original defect before completion. The preparer separately identified and corrected it. The reviewer did not edit either input. Replacing only the corrected sentence by the original sentence reconstructs the original byte count and SHA-256 exactly, proving there were no undisclosed changes between the two pinned inputs. Restoration of the bad expansion is also a rejected negative control in the final checker.

## 2. Apéry table and universal completeness

Every one of the 21 membership expressions was independently evaluated as a nonnegative combination of 32, 48, 40, 21 and 49. Every displayed value has the designated residue modulo 21, including the base value d₀=0. All 84 displayed quotients were independently recomputed, with their correct residue-indexed table lookups. Every quotient is a nonnegative integer. The 21 remaining transitions, for the generator 21 itself, have quotient one.

These finite checks support a universal proof, rather than an empirical search cutoff. Starting with d₀=0, induction on the length of any nonnegative generator expression gives d_(s mod 21)≤s for every semigroup element s. Conversely, a nonnegative integer s in residue r with s≥d_r has s=d_r+21k for a nonnegative integer k, and the displayed membership expression for d_r proves s belongs to S. Thus the asserted membership criterion holds for every nonnegative integer.

Consequently 136 is the largest Apéry value and the Frobenius number is 115. The claimed gaps 7 and 108 are correctly rejected by d₇=49 and d₃=129; their sum is 115, so symmetry fails. The phrase about the last gap in a residue is read as the last integer outside S in that residue: for residue zero it is −21, with no nonnegative gap in that residue. This harmless convention does not affect the Frobenius maximum or any pseudo-Frobenius test.

The proof also establishes the **complete** pseudo-Frobenius set. If f is pseudo-Frobenius, f+21∈S but f∉S, forcing f=d_r−21. Conversely, for such a candidate every f+g is nonnegative, and its membership inequality is exactly Q_g(r)≥1. Testing the generators suffices for every positive element of S, by adding the remaining generators of any factorization. Thus neither an extra maximality assumption nor a missing search range is being used.

The rows having four strictly positive displayed quotients are exactly 2, 3, 8, 10, 14, 15 and 16. They give, in that order, 107, 108, 92, 115, 77, 99 and 100. Every other row has a zero entry and therefore a concrete failed generator test. It follows that

    PF(S) = {77,92,99,100,107,108,115},

with type seven. The standard numerical-semigroup-ring relationship between type, symmetry and Gorensteinness is inherited from the main proof; the supplement neither changes its scope nor purports to reprove the general ring-theoretic theorem.

As a separate computational cross-check, an independently implemented coin-reachability recurrence first reaches 21 consecutive semigroup elements beginning at 116. Adding 21 proves the entire remaining tail reachable. It independently recovers all 21 Apéry representatives, conductor 116, Frobenius number 115, and exactly the above seven pseudo-Frobenius numbers. This algorithm is supplementary: the displayed table and induction already prove the result without it.

## 3. Matrix arithmetic, rank and primitive adjugate

All five displayed products Ba=0 check term by term for a=(89,72,85,164,107). Direct column addition gives zero in every column. The diagonal magnitudes are (4,5,4,3,3), and the only off-diagonal zero entries are (1,2), (2,3), (3,4), (4,5) and (5,1). All other off-diagonal entries are positive.

The displayed four-by-four minor is exactly the matrix obtained by deleting row 5 and column 5 from B. Its determinant and its signed (5,5) cofactor are 107. A nonzero order-four minor gives rank at least four, while Ba=0 with a nonzero vector gives rank at most four. Thus rank is exactly four. The right kernel is the line through a; column balance makes the left kernel the all-ones line. The adjugate identities therefore give Adj(B)=h a·1ᵀ. The (5,5) entry forces 107=h·107, hence h=1. Also gcd(89,72)=1, so a is primitive.

Every one of the 25 adjugate entries was independently computed by exact integer cofactor expansion and matches a·1ᵀ. This independently confirms the argument, including its sign and transpose conventions. There is no unproved step from a primitive kernel vector to a primitive adjugate: the specific cofactor calculation supplies that essential step.

The stated principal multipliers were also independently checked without relying on the cited sufficiency theorem: for each generator, finite exact reachability using only the other four generators rejects every smaller positive multiple, including multiplier one, and accepts the displayed multiple. The resulting least multipliers are exactly (4,5,4,3,3). This extra check confirms minimal generation but is not needed by the supplement's source-based proof.

## 4. Exact source attribution and applicability

The primary reference is Papri Dey and Hema Srinivasan, [Principal Matrices of Numerical Semigroups, arXiv:2012.15464v3](https://arxiv.org/abs/2012.15464v3), dated 18 June 2021. The live arXiv record and PDF theorem text were checked. The matching local PDF has 228,072 bytes and SHA-256 `bbe2844903c0d53d9a039f4e6a407fb9bba14694d75462c0b9bfd903cfe246c5`. Definition 4 and Theorem 26, including its proof on printed pages 12–13, were inspected; the theorem statement was also rendered and visually checked locally after the web screenshot failed.

Theorem 26 assumes dimension at least three, a pseudo-principal integer matrix of rank n−1, diagonal magnitudes at least two, zero column sums, primitive first adjugate column, and at most one zero in each column. It concludes principality for the primitive positive kernel tuple and embedding dimension n. Here n=5. The supplement's “an adjugate column” formulation is equivalent because column balance and rank have already made every adjugate column equal. All the conditions hold for B. The source's dimension restriction, implicit in the five-by-five application, causes no omitted-hypothesis problem.

The citation is used solely for principality and minimal generation. The cyclic-order gap construction and Gorenstein obstruction belong to the authored argument. No classification or novelty conclusion is attributed to the source. No copied source PDF or extracted source text is part of this audit deliverable.

## 5. Cyclic witnesses and proof-only sufficiency

The defining formula of Lemma 3 independently gives

    v(2,4,5,3,1) = (-1,4,0,1,1),
    v(4,2,5,3,1) = (-1,2,0,2,1).

Their weighted values are 470 and 490, respectively. Every successor entry required by each cyclic order, including wraparound, is positive. For each of the five rotations of each order, the weighted value stays unchanged; adding one in the final vertex's coordinate gives a nonnegative factorization of the value plus that generator. All ten membership witnesses were independently checked. The saturated-lattice argument of Lemmas 2–3 supplies the nonmembership assertion. Independent coin reachability separately confirms that both 470 and 490 are gaps.

Theorem 4's general distinctness argument remains unchanged: equality of the two values would give a critical-generator relation with a positive coefficient strictly below its least allowed multiplier. The supplement establishes the concrete hypotheses rather than replacing that all-family proof by an example. It does not assert an exact pseudo-Frobenius set or exact type for the five-cycle example.

Read with its explicitly cited matrix, definitions and analytic lemmas in `PROOF.md`, the supplement is self-contained as finite verification: its membership expressions, Bellman entries, cofactor expansion and cyclic calculations can all be checked by hand. Neither unpublished raw certificate data nor an executable program is a premise. Standard credited mathematical theorems remain legitimate external references.

## 6. Reproducibility, controls and final scope

A separately written standard-library exact-arithmetic checker imports no author checker, raw certificate, external CAS or dataset. It parses the supplied membership and quotient table and displayed numerical claims, computes cofactors recursively, independently tests semigroup reachability, and checks every cyclic rotation. It uses explicit exception checks rather than assertions, so Python optimization cannot disable validation.

Both ordinary Python and Python -O runs pass on the accepted hash and agree in all mathematical outputs. Each rejects **138 deliberately corrupted controls**: all 21 Apéry values, all 21 membership expressions, all 84 Bellman quotient cells, plus 12 structural or claimed-result corruptions. The latter include a missing residue, altered complete/ordered pseudo-Frobenius sets and residue list, false Frobenius arithmetic, a row-product error, a minor-entry error, a wrong determinant, the original incorrect expansion, a wrong cyclic vector, a wrong cyclic order, and a wrong kernel vector. The mathematical induction and proof reading are separate from these computational checks.

Accepted: the corrected finite arithmetic; the complete type-seven calculation; the rank-four, primitive-adjugate and principality witnesses; and the two concrete pseudo-Frobenius witnesses supporting the already bounded five-cycle obstruction.

Not established: the original necessary-and-sufficient five-generator non-complete-intersection classification, a Gorenstein non-CI member of the identical-data pair, a universal exact-type formula, novelty, or worldwide current openness. The supplement preserves these limits. The audit leaves the accepted supplement, original author inputs, original audit, repository and queue unchanged, and performs no publication.
