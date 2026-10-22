# Independent audit: Kourovka 21.90 / ID 2599 / rank 770

## Decision

**Mathematical scope: PASS. Source wording: five exact editorial replacements and one clarification sentence required before publication of a revised author payload. General problem under the connected/nondegenerate interpretation: UNRESOLVED; five of five investigation approaches completed.**

No counterexample to the frozen proofs or rational certificates was found. The crown family verifies the permissive convention allowing disconnected strongly regular graphs with μ=0. It does not settle the connected/nondegenerate interpretation. The primary problem entry does not explicitly impose that interpretation, so its author's intent must not be presented as a verified fact.

The 14-entry author archive and its original source directory were preserved. No remote writes were performed. This audit contains authored reasoning/code, the authored certificate input, generated exact results, and public verification metadata only. It excludes source PDFs/text, dataset contents, and private coordination reports.

## 1. Receipt and frozen inputs

Author archive: `KOUROVKA_2599_AUTHOR_SAFE_FREEZE.zip`.

- Bytes: 59,164
- SHA-256: `2c4530b0d0daf358e64d8e701ee739bbe97d5a83fa87037a2a2e5d1b47643bba`
- `AUTHOR_MANIFEST.json` SHA-256: `7ddf656ed2dc847097cdb3134a578791021748d4cfa9d9202b8bc60c32aa4d0e`
- 14 archive entries: manifest plus 13 pinned payload files
- All byte counts/hashes verified against the receipt and manifest

The initial audit handoff omitted the two letters `ee` in the archive digest. The on-disk receipt is correct; this is a handoff transcription issue, not an author archive defect.

Every authored file was inspected, including all proofs, all four verification programs, the five certificate objects, saved outputs, source metadata, limitations and research log. Author scripts were run in a separate copy. Their three generated output files are byte-identical to the frozen versions; the author manifest checker passes before and after replay. Details appear in `AUTHOR_REPLAY.json`.

## 2. Mandatory editorial corrections

`REQUIRED_CORRECTIONS.json` gives unambiguous old/new strings and their locations. There are four occurrences presenting the nondegenerate interpretation as the author's verified intention, plus one chronological phrase:

1. `README.md`: replace its opening “intended nondegenerate” disposition with conditional connected/nondegenerate wording.
2. `RESEARCH_LOG.md`: condition the corresponding statements in approach 2 and the stopping paragraph.
3. `SOURCE_VERIFICATION.json`: condition the `outcome` text.
4. `README.md`: use “related 2019/2020 exclusions” instead of “subsequent 2019/2020 exclusions”. The three-array exclusion appeared September 18, 2019, before the matching October 7, 2019 paper.
5. Add the specified clarification sentence to `README.md` explaining that the primary entry does not explicitly impose connectedness/nondegeneracy and the research interpretation is an inference.

These are editorial/source-accuracy corrections; no mathematical replacement is required. The freeze was not silently edited. A revised author payload needs a new manifest/freeze and a bounded check that only these approved changes were made. Historical “audit pending” fields in the original freeze remain valid historical metadata and need not be falsified retroactively.

## 3. Mathematical audit

### 3.1 Crown graphs and the convention boundary

The direct distance classification in the crown graph on 2n vertices is correct for every n≥3: same-side distinct pairs are at distance two; matched opposite vertices are at distance three. Neighbor counts give `{n−1,n−2,1;1,n−2,n−1}`. The exact-distance graphs are two n-cliques and n isolated edges, respectively, with μ=0 in both cases. Neither distance graph is connected.

The tensor idempotents are pairwise orthogonal and complete. Their adjacency eigenvalues n−1, 1, −1, −(n−1) are distinct for n≥3. The four displayed Schur product equations have the correct coefficients and normalization. Their off-diagonal Krein support is an irreducible path because n−2>0. Thus the Q-polynomial proof is valid, including the smallest case n=3, the six-cycle.

Independent controls constructed the graphs from adjacency, computed all distances by breadth-first search and verified all intersection numbers for n=3,…,10. This is not merely a re-evaluation of the proposed distance formula.

### 3.2 Fusion reduction and integrality

For multiplication matrices oriented by columns, the h-th coefficient of A_i A_j is entry (h,j) of the matrix for A_i. Rebuilding this recurrence confirms both generic fusion differences. Strong regularity of distance two equates the coefficients at original distances one and three; strong regularity of distance three equates those at distances one and two. Since diameter three gives positive b₂,c₂,c₃, the divisions used in the reduction are legitimate.

The resulting array, degree, local parameters and eigenmatrix are correct. The independent symbolic program verifies the full characteristic polynomial, all 16 eigenmatrix entries, all 16 projector orthogonality identities and the order formula. It constructs idempotents using Lagrange spectral projectors and never inverts the author's displayed eigenmatrix.

The proof that t is integral is sound: t=b₁/c₂ is rational; the exhibited rational eigenvalue a+t of an integral adjacency matrix is an integer; a=k−c₃ is integral. Distinctness of the four displayed eigenvalues follows from t>0, c≥1, a≥0. The nonnegative local parameter a₂=(t−1)(c+1) then yields t≥1.

### 3.3 Krein reduction and all boundary cases

The normalization Q=vP⁻¹ and the formula for Krein coefficients are consistent with the chosen row/column conventions. The Gram tensor argument proves their nonnegativity. All six displayed factorized square coefficients are independently verified symbolically using spectral projectors.

For a>0,t>1, generators E₂ and E₃ each have two positive nonprincipal off-diagonal square coefficients, which is incompatible with a Q-polynomial path beginning at E₀. The remaining generator forces D=0 exactly as stated. No sufficiency is inferred.

The t=1,a>0 boundary has a negative Krein coefficient. For a=0,t>1, E₁ and E₃ have two positive off-diagonal square coefficients; E₂ squares inside span{E₀,E₂}, so cannot generate a four-dimensional Schur algebra. The surviving boundary a=0,t=1 is precisely the crown parameter array. The Diophantine range and distance-three λ/μ formulas follow correctly.

As an additional check, the symbolic audit gives μ(Γ₂)=t(c+1)(t−1). Together with μ(Γ₃)=a(a+1)/(c+1), this is positive throughout a>0,t>1. Thus, if realized, these strongly regular distance graphs are connected. Their complements contain the original connected graph Γ and are connected as well. This confirms the hypotheses of the primitive strongly regular absolute bound in the sieve.

### 3.4 Elementary exclusions and absolute bound

Shell edge parity is a valid necessary condition: the induced exact-distance-h relation on a distance-i shell is regular of degree p_ih^i. The local independent-set estimate follows by the greedy bound and the first two Bonferroni terms; it is a lower bound on the union and yields the stated necessary inequality.

When c₂=1, a local connected component must be a clique: a shortest local path of length two would otherwise supply a forbidden second common neighbor. Its size a+t must divide k=a+2t. For a>0 this degree lies strictly between a+t and twice a+t, so the c₂=1 exclusion is valid.

For the strongly regular absolute bound, the two restricted eigenvalues yield two distinct inner products. Repeated projected vertices force twins and an imprimitive graph or complement. In the connected/complement-connected case, the quadratic separating functions are independent; the sphere relation reduces the polynomial space dimension to f(f+3)/2. Both the proof and application to fused eigenspaces are correct.

For t=2, the sole integral c≥1 solution is (a,c)=(2,5); v=50 and a fused restricted eigenspace has dimension 7, contradicting 50≤35. For t=3 the four stated pairs are exhaustive. Two have negative distance-three λ; (a,c)=(5,9) has odd local edge-end count 35×7; (4,4) is excluded by the first exact certificate. Hence the connected/nondegenerate regime requires t≥4,c≥2 without relying on a cited paper's potentially erroneous arithmetic.

### 3.5 Triple-intersection identity and five certificates

All three pairwise marginals and zero-coordinate values have the correct index orientation. The proof of the vanishing-Krein identity is valid: expanding the sum of squares of T(x,y,z), using orthogonal idempotents and then the Schur product gives q_rs^u rank(E_u)/v. Zero therefore forces every individual square, and every corresponding triple equation, to vanish.

The independent verifier recreates all 88 equations for each certificate. It checks base-triangle existence, distinct/valid multiplier indices, every one of 64 resulting coefficients, the displayed right side, and nonnegativity. No optimization solver or floating point is used.

Verified cases, with (t,c,a), base-triangle multiplicity, and contradiction right side:

- `{19,12,5;1,4,15}`: (3,4,4), multiplicity 4, right side −3
- `{17,8,6;1,2,12}`: (4,2,5), multiplicity 8, right side −40
- `{77,60,13;1,12,65}`: (5,12,12), multiplicity 12, right side −5
- `{199,168,25;1,24,175}`: (7,24,24), multiplicity 24, right side −7
- `{83,54,21;1,6,63}`: (9,6,20), multiplicity 54, right side −15

All five arrays survive the stated basic sieve and are distinct. Complete coefficient lists are in `AUDIT_RESULTS.json`. Their discovery method is irrelevant to the validity of the final rational identities. No novelty is asserted.

### 3.6 Bounded sieve

The independent enumeration uses integer divisibility to generate c, rather than copying the author's rational-generation branch. Distance multiplication is rebuilt from the intersection recurrence. Idempotents use spectral interpolation. Q-polynomiality is checked by the connected path support of the Krein multiplication graph, rather than enumerating all candidate orderings.

All tests reproduce all 959 authored rows, including every rejection label, checked through a canonical SHA-256 digest. Exactly 159 arrays survive the basic tests and 154 remain after the five certificates. The ten basic survivors for t≤6 agree. A surviving array is neither a construction nor an assertion that its existence remains open in the literature. Published external exclusions have not been silently added to the count.

## 4. Computational replay and adversarial controls

The standard-library verifier completes 155,035 check invocations, including six intentional mutation-rejection tests. Positive checks include 24,320 actual crown-graph intersection counts and 119,952 triple-equation checks over all 1,176 ordered distinct base triples for crowns n=3,4,5. The six mutated certificate tests change the right-side sign, a multiplier, a left-side coefficient, a graph parameter, the base triangle, and the equation count; all are rejected. An incorrect Q-polynomial relation is also rejected.

The separate SymPy program passes 46 generic symbolic identities. Its dependency and exact results are disclosed. The finite certificate proof does not depend on SymPy, a network connection, floating point, or external services. Both programs are tested from a relocated directory and their result files reproduce byte-for-byte.

The verifier checks mathematical identities, not a formalized proof assistant development. “Independent” means separately implemented and reasoned, using the frozen certificate coefficients as data. It does not mean the certificate coefficients were newly discovered or that arbitrary external literature proofs were re-proved.

## 5. Primary-source and corpus verification

The October 2026 editor PDF was freshly downloaded and its full bytes independently hashed. The problem page was visually inspected: printed p.190, PDF zero-based page 189. Statement, proposer and absence of a solved/AI-claim annotation match the author metadata. The exact primary statement leaves the strongly regular convention unstated. Absence of an annotation is an editorial-status observation, not proof that no resolution exists elsewhere.

The directly matching 2019 paper explicitly treats the crown parameter boundary and separately states primitive hypotheses. Therefore the crown example is known prior literature. All six cited research articles' primary bibliographic details were checked. Both locally downloaded IMM PDFs match the frozen hashes and sizes. The 2023 exclusion is verified at abstract/bibliographic level; its full PDF remains unavailable by the tested route. No full independent audit of any external paper proof is claimed.

All three full public corpus files were independently hashed and match the frozen pins. ID2599, KOU-21.90, rank770, the statement hash, catalogue review-hash pin, and status values match. The target statement was compared to the primary entry. No exact target key/content match was found in research results. The raw corpus and selected record are excluded from the publication payload.

The author's earlier bounded GitHub searches were inspected as historical provenance, not rerun or upgraded into an exhaustive-history claim. No conclusion about deleted branches, unindexed artifacts, or private work follows. Public metadata and precise inspection limits are in `SOURCE_AUDIT.json`; only sanitized public source-verification metadata is included.

## 6. Reproduction and stopping condition

From the extracted audit directory:

    python verify_independent.py
    python verify_symbolic_independent.py
    python verify_audit_manifest.py

The symbolic command needs SymPy; the other two use only the Python standard library. `TRIPLE_CERTIFICATES.json` is copied byte-for-byte from the author's pinned certificate file. The full author archive is not embedded in this audit.

Mathematical audit is complete for the scoped partial results. Required editorial corrections remain explicitly pending for any revised author payload. No graph realizing the connected/nondegenerate target was constructed, no global obstruction proved, and no solved/editorial-acceptance status is authorized by these findings.
