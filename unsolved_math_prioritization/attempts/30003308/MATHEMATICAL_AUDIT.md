# Independent mathematical audit: five-generator principal matrices

## Publication-edition boundary

This is the complete original mathematical audit, with a private coordination
reference removed and this publication note added. Its mathematical arguments,
finite findings, acceptance decision and limitations are preserved. It records
the examination of a broader original manuscript and computational evidence,
not a fresh review of the narrowed proof-only edition. Recorded computations
in §§2, 6 and 7 are historical findings, including optional finite claims no
longer adopted by PROOF.md; their raw code and certificate datasets are not
distributed. No essential proof claim in PROOF.md is justified merely by
those omitted files.

The separately authored PROOF_SUPPLEMENT.md was added after this audit.
The separate [SUPPLEMENT_AUDIT.md](SUPPLEMENT_AUDIT.md) now accepts its exact
corrected bytes. The original acceptance below does not cover its new
presentation; the supplement’s frozen pending-review sentence is historical
and is superseded by the separate completed review. The original audited proof has SHA-256
6709b3ab95c2dfca3da51cc258983816fa7b97734a3823e23126e1a9513c18c3
and 17,745 bytes. This AI-assisted audit is unrefereed; acceptance does not
mean external human peer review, journal acceptance, or formal
proof-assistant certification.

## Decision and pinned input

**ACCEPT AS A CORRECT, EXPLICITLY BOUNDED PARTIAL RESULT. NOT A SOLUTION OF THE ORIGINAL NON-COMPLETE-INTERSECTION CLASSIFICATION.**

The entire submitted original proof, certificate data, source audit, metadata and status were examined. The externally supplied SHA-256 of the input manifest is

`83dcc6b07a65357dbb92889e3da292c44630d379ef81a29eb90ea87586e45169`.

The input manifest matches this hash, and all 12 listed files match their sealed byte counts and hashes. Reverification after the computations also passes. No frozen input, repository, or queue was changed. No publication or outreach was performed.

No blocking mathematical error or required correction was found. This decision accepts two obstructions and their exact examples; it does not certify novelty or exhaustive current literature coverage.

## 1. Source scope and attribution

The originating contribution was independently read in full, printed pp. 3227–3230, including the definitions, four-generator theorem, five-generator question, decomposable case, and references. The page containing the actual question was also visually inspected. It is situated expressly in the Gorenstein non-complete-intersection discussion. The neighboring bound on numbers of ideal generators is a different question. The “relatively prime” convention is collective gcd one; pairwise coprimality is neither intended nor valid for the examples.

The report's early rank-n recovery discussion cannot justify assuming all genuine principal matrices have full rank n−1. The later primary source explicitly exhibits different ranks for different legitimate row choices. The target is structural characterization with a clear choice quantifier, not recovery of a tuple followed by an ordinary symmetry computation.

The Gimenez–Srinivasan 2020 paper was inspected in full. Its four-generator criterion and strengthening in Section 3 are prior work. Its gluing definition, Lemma 14, Theorem 15 and Corollary 17 support the ideal generation, complete-intersection and type claims used here. Question 11 asks about type from maximal-rank data and is not generally answered by the submitted obstruction.

The Dey–Srinivasan v3 paper was independently inspected for definitions, Example 2, the rank bounds and block results (including Theorems 13, 15 and 22), Section 4 and Theorem 26, and the later examples and references. The rank-3 patterns are already classified there. Theorem 26 is a sufficient principality theorem; its introductory reference as “Proposition 26” is a source numbering inconsistency, not an omitted extra result. It does not supply the submitted non-Gorenstein conclusion. The displayed sign slip in one block of the printed Theorem 22 is not adopted in the audited result.

Public primary references:

- Hema Srinivasan, joint work with Philippe Gimenez, “Gorenstein Monomial Curves,” OWR 57/2016, pp. 3227–3230: https://doi.org/10.4171/owr/2016/57
- Philippe Gimenez and Hema Srinivasan, “Structure of some numerical semigroup rings,” Banach Center Publications 121 (2020), pp. 53–61: https://doi.org/10.4064/bc121-5
- Papri Dey and Hema Srinivasan, “Principal Matrices of Numerical Semigroups,” arXiv:2012.15464v3, 18 June 2021: https://arxiv.org/abs/2012.15464v3

All three local PDF byte counts and SHA-256 identities were independently checked against the submitted metadata. The live arXiv record confirms title, authors and v3 date. Two DOI opens failed at the web tool, so those sources were inspected using the already available, hash-matching primary PDFs. Historical retrieval timestamps are not independently reconstructed. No source PDF or source-text extract is included in this audit package.

## 2. The indistinguishable rank-3 pair

The ordered tuples are a=(32,48,40,21,49) and b=(40,60,50,27,63). Both have positive distinct entries and collective gcd one. The independent implementation proves that their complete critical multipliers are (3,2,2,7,3). Every lower positive multiple is checked, and **every** nonnegative factorization excluding the corresponding generator is enumerated at the first successful multiple. In both tuples the complete row lists are the same five singletons:

```
(-3, 2, 0, 0, 0)
( 3,-2, 0, 0, 0)
( 1, 1,-2, 0, 0)
( 0, 0, 0,-7, 3)
( 0, 0, 0, 7,-3)
```

The pure-pair bounds on possible first multipliers are respectively (3,2,4,7,3), so this finite calculation has a proved bound. Since all critical multipliers exceed one, neither tuple has a redundant generator. The set of all principal matrices is the Cartesian product of these row lists. Hence each set consists of precisely the displayed matrix. The first block has rank two and the second rank one, so rank is three. There is no hidden rank-four choice, even when every off-diagonal choice is permitted.

The supplied modular proof was checked independently as well:

- For (d,e)=(8,7), any positive contribution from 7<3,7> to a target divisible by 8 is at least 7·16=112, exceeding the first-block critical targets 96,96,80. In the other direction the only possible positive 8<4,5,6> contribution divisible by 7 up to 147 is 8·14=112. The equations for the omitted 21 or 49 generator have no nonnegative solutions in their stated ranges.
- For (d,e)=(10,9), the only positive 9<3,7> contribution compatible with divisibility by 10 at the first-block targets is 90. The remaining 10 or 30 cannot be formed from the first-block generators. The lower targets do not allow a new relation. In the other direction the only positive multiples of 9 in 10<4,5,6> below 190 are 90 and 180. For 27r, 1≤r≤7, the congruences in 3r=10k+7v force r=1 or 2 for k=1 or 2, giving negative v. For 63r, 1≤r≤3, the corresponding equation 7r=10k+3u forces the same small r and a negative u. The pure pair relation first appears at 189.
- The internal relations in <4,6,5> at 12,12,10 and in <3,7> at 21 have exactly the stated factorizations.

These arguments establish uniqueness, not merely the existence of a common pseudo-principal relation matrix.

### Types, symmetry and complete intersection

Independent exact membership calculation gives:

| Tuple | Frobenius number | Genus | Pseudo-Frobenius set | Type |
|---|---:|---:|---|---:|
| (32,48,40,21,49) | 115 | 75 | {77,92,99,100,107,108,115} | 7 |
| (40,60,50,27,63) | 259 | 130 | {259} | 1 |

Every submitted Apéry entry and its factorization witness agrees with the independent calculation. The two gaps 7 and 108 in the first example sum to 115 and separately certify failure of symmetry. The equivalence of symmetry, type one and the Gorenstein property is the standard numerical-semigroup-ring result and does not require a restriction on the field.

The complete-intersection attribution is correct. For the second tuple, gcd(10,9)=1, 10=3+7 belongs to <3,7> and is not one of its generators, while 9=4+5 belongs to <4,6,5> and is not one of its generators. The latter factor is itself the gluing 2<2,3>+5<1>, with 5=2+3. The factors are complete intersections, so the known gluing theorem applies. Its ideal-generation statement gives exactly

```
x1^3-x2^2,  x3^2-x1*x2,  x4^7-x5^3,  x1*x3-x4*x5.
```

Their weighted degrees in b are 120,100,189,90. They generate the height-four toric ideal by gluing. The first factor and the independent two-generator factor are domains, and the gluing binomial is a nonzero divisor in their tensor-product semigroup domain; equivalently the gluing resolution is the complete-intersection resolution. Thus the displayed defining regular sequence is justified by the credited theorem, rather than inferred from symmetry alone.

### Exact quantifier consequence

An arbitrary Boolean function of one selected principal matrix cannot distinguish this pair when asked to work for every tuple and every genuine choice. Neither can a Boolean function of the complete matrix set, because the sets are identical singletons. Switching an arbitrary matrix-only predicate between existential and universal quantification does not fix this example.

This conclusion concerns the full class including complete intersections. It does not preclude generator/scale data in a criterion, and does not prove an impossibility theorem for the original non-CI class. The submitted manuscript correctly preserves those limits. In the rank discussion, “maximal rank” must mean full possible rank n−1; the maximum rank attained by this pair's choices is of course three.

## 3. Saturated row-lattice lemma: proof audit

Let B be any n−1 independent rows of A whose maximal minors have gcd one. Its rational row space is the kernel of the primitive linear form z↦z·a, since both spaces have dimension n−1. For z in that integer kernel, write z=λB over Q. Every nonsingular column-deleted submatrix B_j gives det(B_j)λ integral by Cramer's rule. Zero determinants are irrelevant. Bézout applied to all maximal minors then yields λ integral. Thus B alone generates the whole kernel lattice, and so does A. No rational-to-integral step is being assumed without proof.

If A has rank n−1, column sums zero and Aa=0, then the left kernel is spanned by the all-ones vector. Consequently Adj(A)=h a·1^T for an integer h, because a is primitive. Thus all adjugate columns coincide. Their entries are exactly the signed maximal minors of the corresponding row-deleted matrix. A primitive nonzero adjugate column makes h=±1 and supplies the required gcd-one minors. This proves the stated reduction.

Without the minor condition, the rational row space still equals a-perp, so the saturation of the row lattice is L(a). This is invariant for all full-rank principal choices of the same ordered tuple. It does not establish equality of the unsaturated row lattices and is not a Gorenstein classification. The manuscript makes the correct, weaker claim.

## 4. Cyclic-order lemma: all-family proof audit

The proof is valid for every integer matrix and tuple satisfying its stated assumptions; the finite checks below are supplementary.

For a linear order p, define v_j as the sum of A_ij over vertices i after j, minus one. Suppose v·a=w·a with w nonnegative integral. Equality L_A=L(a), not just equality of rational spans, supplies an integral coefficient vector λ with v-w=λA. Choose j as the last vertex in p among those having minimal λ-coordinate. Column balance gives

```
(λA)_j = sum_{i != j} (λ_i-λ_j) A_ij.
```

Each summand is nonnegative; for every i after j the integer difference is at least one. Hence this coordinate is at least sum_{i after j} A_ij=v_j+1. On the other hand v_j-w_j≤v_j, a contradiction. This proves a genuine gap. The primitive-minor hypothesis is essential to this proof's integral coefficient step and is not silently dropped.

Moving the first vertex i to the end changes v by row i of A. For coordinate i, column balance gives the change -c_i; for each other coordinate it adds A_ij. Therefore the weighted value v·a is unchanged. If each cyclic successive pair j,i has A_ij>0, rotating the order to put j last leaves v_j=-1 and every other coordinate at least zero, because its successor is later and contributes at least one. Adding the j-th unit vector is a nonnegative factorization of f+a_j. This proves the pseudo-Frobenius condition for every generator, including wraparound after rotation.

There is no hidden sign convention problem. A negative pseudo-Frobenius number in a minimal semigroup with at least two generators would have to be -m, since its sum with the multiplicity m is a semigroup element below m. Then every other minimal generator minus m would belong to the semigroup, contradicting minimality. The produced pseudo-Frobenius numbers are thus in the usual nonnegative convention.

## 5. Five-cycle obstruction: hypotheses and distinctness

The pattern has exactly A12=A23=A34=A45=A51=0 and all other off-diagonal entries positive. The orders p=(2,4,5,3,1) and q=(4,2,5,3,1) use the following successor entries:

- p: A42,A54,A35,A13,A21;
- q: A24,A52,A35,A13,A41.

All ten are positive in the specified pattern. The lattice lemma applies from the full-rank primitive-adjugate assumption. The preceding all-family lemma supplies two pseudo-Frobenius numbers.

The only order change swaps vertices 2 and 4. Its exact weighted difference is A42·a2−A24·a4. If it vanished, the positive multiplier A42 would express a2 using a4 alone. Column two has sum zero and off-diagonal terms 0,A32,A42,A52, so

```
0 < A42 < A32+A42+A52 = c2.
```

This contradicts criticality of the second row. The distinction between row-two criticality and the column-two sum is intentional and valid: both contain the same diagonal c2. This is a structural proof for the full stated family, not numerical evidence extrapolated from one matrix. It yields type at least two, not a universal exact type.

Dey–Srinivasan Theorem 26 is applicable to the companion principality statement: rank n−1, column balance, primitive adjugate, at most one zero per column, and diagonal magnitude at least two are all present. In this five-cycle pattern, balance even gives c_i≥3. The main proof already assumes genuine principality, so it does not depend circularly on its own conclusion or on this source theorem.

The appropriate matrix-choice statement is existential sufficiency: one matrix satisfying the hypotheses proves the underlying semigroup non-Gorenstein. No second choice can change its actual pseudo-Frobenius numbers. It is neither asserted nor proved that the zero pattern survives every choice. The manuscript does not make that invalid inference.

## 6. Full-rank example and controls

For the submitted B and a=(89,72,85,164,107), independent enumeration gives precisely one critical row per index with multipliers (4,5,4,3,3); consequently B is the unique principal matrix. Its rank is four. Every column sums to zero. Its only off-diagonal zeros are the five specified cyclic positions. Every adjugate column is exactly the positive vector a, of gcd one. For each of the five ways to delete a row, the gcd of all four-by-four minors is one, verifying lattice saturation directly.

The stated order vectors (-1,4,0,1,1) and (-1,2,0,2,1) and every rotated nonnegative addition witness check exactly. Their values are 470 and 490. Independent membership gives F=618, genus 340 and PF={345,468,470,476,490,494,525,618}. All 120 linear orders satisfy the gap and row-rotation identities; 40 are admissible, corresponding to eight cyclic classes, and their values are exactly this PF set. These extra finite facts are not used as a proof about all pattern matrices.

For <6,7,8,9,10>, the independent calculation gives F=11, genus 6, PF={11}, and exactly 16 principal matrices, all rank four. At degrees 14,15,16,18,20 the complete factorization graphs have 2,2,3,3,2 connected components. A lower-degree binomial multiplied into one of these degrees joins only factorizations sharing a common monomial factor, hence only vertices in the same graph component. Therefore at least 1+1+2+2+1=7 minimal binomial generators are needed across these degrees. The toric ideal has height four, proving this symmetric example is non-CI. This establishes the control's label without conflating symmetry and CI.

For the Dey–Srinivasan tuple (22,33,26,39,34), the complete row-option counts are (1,1,2,2,2). Its eight genuine principal matrices have rank distribution two of rank three and six of rank four. The two matrices copied as mathematical fixtures coincide with the source's Example 2, and the submitted ranks are correct. This directly guards against a false fixed-rank assumption.

## 7. Independent computation and rejection controls

The audit implementation imports no author checker and uses no external CAS. It is a separately written standard-library program. Exact rational row reduction computes ranks, and Leibniz determinants compute cofactors. For criticality, a positive pure-pair relation supplies a finite upper bound; Boolean coin recurrence finds the first multiple, and coefficient-by-coefficient generating-polynomial expansion lists all its factorizations. This checks row completeness as well as criticality.

Semigroup membership is recomputed by an unbounded integer recurrence until m consecutive positive integers are reachable. Adding m then proves that all subsequent integers are reachable. Thus the stopping condition is a mathematically sufficient conductor certificate, not a guessed search cutoff. Apéry entries, all gaps, F, genus, symmetry and all pseudo-Frobenius numbers are derived from this independent computation. Submitted Apéry factorization witnesses and Bellman inequalities are checked separately.

Both normal and optimized runs pass, with 17 deliberately corrupted controls rejected. These include a true but noncritical relation, omission of a legitimate alternative row, wrong multipliers/ranks, altered Apéry entries/witnesses, false type/genus/Frobenius/symmetry, a corrupted adjugate and invalid cyclic values/vectors/witnesses. Explicit exception checks remain active under Python -O.

The author's checker was also run normally and under -O with bytecode writes disabled; both recorded runs pass their 12 rejection controls. Those author runs are supplemental and did not replace the independent implementation.

## 8. Acceptance boundaries and remaining work

Accepted: the same-singleton-data obstruction on the full class; the saturated balanced five-cycle non-Gorenstein theorem; all stated numerical certificates and controls; principality, minimality, collective gcd, gluing/CI attribution, lattice saturation, cyclic-order construction, distinctness and choice quantification.

Not established: a necessary-and-sufficient criterion on five-generator non-CI semigroups; a Gorenstein non-CI member of an identical-principal-data pair; a general answer for all rank-four patterns or nonsaturated row lattices; a resolution of remaining rank-three cases; a universal type-eight formula; novelty or worldwide current openness.

The artifact is useful mathematical partial progress and a sound correction to overbroad matrix-only or universal-full-rank premises. It must retain its present partial-result status if presented downstream.
