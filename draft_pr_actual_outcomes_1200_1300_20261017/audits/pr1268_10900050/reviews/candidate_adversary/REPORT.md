# Fresh adversarial audit: PR 1268, problem 10900050

Verdict: **PASS for the submitted complete negative counterexample in the precise printed-source scope.** The current proof has no identified mathematical gap. Its conclusion is

\[
O_{\mathbb Q(\sqrt{10})}=\mathbb Z[\sqrt{10}],\qquad
\omega(\Gamma_{\rm unit})=\omega(\Gamma_{\rm unit\ or\ prime\ element})=2,
\qquad \min_{0\ne Q\text{ prime}}|O/Q|=2.
\]

Thus the actual proposed equality has sides 2 and 4. This verdict is a fresh AI-assisted mathematical review, not publication approval, external human peer review, a formal proof-assistant certificate, or a novelty determination. No historical acceptance statement was treated as a premise.

## Scope and authenticated inputs

The audit read all ten original submitted files in full, including the proof, historical review, source/literature metadata and editorial map. `INPUT_AUTH_START.json` and `INPUT_AUTH_END.json` identify the same ten bodies by exact bytes and SHA-256, compare them with actual read-only Git blob bodies, and verify their blob identities in head `cecd7da6e8b5bb84b4294e169d940189b269a956`. The supplied snapshot hashes to `69e123cf726603583476566bb8b3f53c9cefe9e9fcff65840d5000efe9bcb32b`. Work stayed on main; no Git/index/ref/PR/service mutation occurred. Only this review directory was authored. No other audit family's mathematical conclusions were read before sealing.

The supplied live-preflight PR body was read and its SHA-256 independently recomputed as `80632e6a02d184fe4a5818161493a40b57af96a03a2cfd2f99e912c1e80d5162`. Its explicit complete-counterexample claim is the object tested. The preflight records an open draft with no comments/reviews; this audit did not manufacture outside approval.

Success required a universal proof for the full ring of integers and both infinite graphs, correct prime-element semantics and all ideal quantifiers, and a match to the actual printed question. Finite numerical tests alone would not satisfy this criterion.

## Fresh primary-source checks

Both primary PDFs were freshly downloaded over HTTPS and exactly matched the submitted fingerprints. See `SOURCE_LEDGER.json`; raw PDFs, text and rendered pages remain excluded from the authored manifest under `own_local/`.

- [Versioned problem list](https://arxiv.org/pdf/1512.04620v1): 280,293 bytes, SHA-256 `7c0dbfb0f5f5f5e39d876dbe0734c4c9df927ed23a29917008ccec77073f00e4`. Read PDF pp. 5–7 and visually inspected pp. 5–6. Question 7.1 specifies an irreducible integer polynomial with real roots and its full integer ring; PID status is asked about, not assumed. Question 7.2 imports that setup and displays the minimum over prime ideals. Reference [19] identifies the author manuscript.
- [Specified 16-page author manuscript](https://web.math.ucsb.edu/~long/pubpdf/LenstraHurwitz.pdf): 250,475 bytes, SHA-256 `166238dd17c2a2ffe1408c5f5c3d2f1ce9ae914c48f657ac309b7a83ee07594c`. Read and visually inspected PDF pp. 1, 9–10. The first definition admits units or differences that generate prime ideals. Section 3 defines prime cliques using condition (i) alone, so its separate unit-group-surjectivity condition is absent here. Theorem 3.1 prints a principal-ideal minimum; its proof uses a quotient field. No global PID hypothesis was found in the relevant scope or full-text hypothesis check.

These are exact version/read-scope claims. A final journal version, separate 17-page manuscript and Lopez thesis were not inspected in this fresh audit. Historical claims about them were not repeated as new evidence. Novelty, priority and present openness were not investigated.

## Universal reconstruction and attempted falsification

Write \(t=\sqrt{10}\) and \(O=\mathbb Z[t]\). The following reconstruction checks every substantive step independently of the historical verdict.

### 1. Full integral basis, rather than an order

The polynomial \(X^2-10\) is irreducible over \(\mathbb Q\): its rational roots would be integers, and no integer square is 10. Both roots are real. Every \(a+bt\), \(a,b\in\mathbb Z\), satisfies the monic integer polynomial \(X^2-2aX+a^2-10b^2\).

Conversely let \(r+st\) be integral with rational \(r,s\). If \(s=0\), a rational algebraic integer is an integer by the rational-root theorem. Otherwise its degree-two monic minimal polynomial has integer coefficients (Gauss's lemma), hence \(m=2r\in\mathbb Z\) and \(r^2-10s^2\in\mathbb Z\). Then \(40s^2\in\mathbb Z\). If \(s=u/v\) is reduced, coprimality gives \(v^2\mid40\), so \(v=1\) or 2. Thus \(n=2s\in\mathbb Z\) and \(m^2-10n^2\equiv0\pmod4\). An odd \(n\) would require an integer square congruent to 2 modulo 4. Therefore \(n\) is even, then \(m\) is even. Both \(r,s\) are integers. This proves the full ring statement, not merely an inclusion.

Attempted failure: a hidden half-integral basis element. It is excluded by the final modulo-four step, whose dependence on 10 is essential. The exact control \((1+\sqrt5)/2\), with integral trace 1 and norm -1, demonstrates why this argument cannot be transplanted to an arbitrary quadratic field.

### 2. The exact principal-ideal index, including signs

For \(\delta=a+bt\), multiplication in the actual integral basis has columns \((a,b)\) and \((10b,a)\), hence determinant \(D=a^2-10b^2\). Nonzero \(\delta\) has \(D\ne0\) because \(t\) is irrational. Its image is exactly \(\delta O\), not a smaller sublattice.

Here is an elementary justification of the index fact, to expose the only lattice import. For any nonsingular two-by-two integer matrix, a unimodular row operation obtained by Bezout turns its nonzero first column into \((g,0)\), \(g>0\). The second column becomes \((c,d)\) with \(d\ne0\). Every quotient class has a representative \(0\le x<g\), \(0\le y<|d|\), by subtracting the second column to reduce \(y\), then the first to reduce \(x\). Two such representatives cannot differ by a column combination: their \(y\) difference first forces the second coefficient zero, and their \(x\) difference then forces the first zero. The index is \(g|d|=|\det M|\). Row operations preserve the index. Thus

\[
[O:\delta O]=|a^2-10b^2| \quad(\delta\ne0).
\]

No PID assumption on \(O\) occurs. A determinant-zero element and signed-versus-absolute norm error were both explicitly tested and excluded. Conjugation \(t\mapsto-t\) preserves \(O\), and \(N(xy)=xy\overline{x}\overline{y}=N(x)N(y)\). An element is a unit exactly when its norm is \(\pm1\): one direction follows by applying this identity to an inverse, and the converse uses \(x^{-1}=\overline{x}/N(x)\). Thus every nonzero nonunit has absolute norm at least 2.

### 3. The norm-two ideal is maximal and nonprincipal

The map \(a+bt\mapsto a\bmod2\) is a surjective unital ring homomorphism: the constant coefficient of a product is \(ac+10bd\). Its kernel consists exactly of even \(a\), which is \(P=(2,t)\). Thus \(O/P\cong\mathbb F_2\), so \(P\) is nonzero, proper, prime, maximal and of index 2.

If \(P=(\delta)\), its nonzero generator would have \(|N(\delta)|=2\) by the index formula. Modulo 5, either sign would make \(a^2\) equal to 2 or 3. The complete square-residue list is \(0,1,4\), so both signs are impossible. This proves nonprincipality without using class number tables or prime factorization of ideals.

Attempted failure: proving only that 2 is not a generator, rather than excluding every generator. The norm equation applies to all \(a,b\in\mathbb Z\), so this objection fails.

### 4. The universal maximality step and prime-element exclusion

For every nonzero prime ideal \(Q\), choose any nonzero \(\delta\in Q\). The quotient \(O/(\delta)\) is finite by the determinant formula, and maps onto \(O/Q\). Thus \(O/Q\) is a finite nonzero integral domain. For any nonzero element of a finite domain, multiplication is injective and therefore surjective, so it has a multiplicative inverse. Hence this quotient is a field and every such \(Q\) is maximal. The quantifier is every nonzero prime ideal; no list or finite search over ideals is being substituted.

A unit cannot belong to the proper ideal \(P\). If a prime element \(p\in P\), then \((p)\) is a nonzero prime ideal, hence maximal. Its containment in proper \(P\) forces \((p)=P\), contradicting nonprincipality. No general Dedekind-domain or class-number theorem is needed. The crucial nonprincipal assumption cannot be dropped: the analogous parity kernel in \(\mathbb Z[\sqrt2]\) is generated by the prime element \(\sqrt2\).

### 5. A direct zero-divisor reconstruction of the exclusion

For an additional falsification check, there is an explicit universal construction showing that every nonzero \(p=a+bt\) with even \(a\) has a non-domain principal quotient. This is an algebraic reformulation of the same parity/norm obstruction, not a claim of a separate independent research family.

If \(b\) is even, write \(p=2q\). If \(q\) is a nonunit, the images of 2 and \(q\) modulo \((p)\) are nonzero and have product zero: \(p\mid2\) would make \(q\) a unit, and \(p\mid q\) would make 2 a unit by cancellation. If \(q\) is a unit, \((p)=(2)\); the nonzero class of \(t\) has square zero because \(t^2=10\in(2)\).

If \(b\) is odd, \(D=N(p)\equiv2\pmod4\), so \(D=2k\) with odd integer \(k\). The classes of 2 and \(k\) multiply to zero since \(D=p\overline p\). Neither is zero. Indeed \(p\mid k\) would imply even \(D\mid k^2\), impossible. If \(p\mid2\), norm multiplicativity gives \(D\mid4\); since \(D\equiv2\pmod4\), this forces \(D=\pm2\), already excluded modulo 5. Therefore \((p)\) is never prime. This verifies the exclusion without the general nonzero-prime-ideal-maximal theorem.

### 6. Both clique numbers and the all-ideal minimum

Equal colors under \(O\to\mathbb F_2\) mean the difference lies in \(P\). For distinct vertices that difference is nonzero and is neither a unit nor a prime element by the preceding arguments. Therefore both infinite graphs have a proper two-coloring. Every clique injects into the two colors, so each has size at most 2, including any hypothetical infinite clique. The edge \(\{0,1\}\), whose differences are \(\pm1\), attains the bound in both graphs. Consequently each clique number is exactly 2, independently of any convention for a supremum versus a maximum.

For every proper ideal, the quotient has distinct zero and one, so its cardinality is at least 2. The explicitly constructed nonzero prime \(P\) realizes 2. Every other nonzero prime quotient is finite by the universal argument above. If the zero ideal is included in an unqualified prime-ideal quantifier, its quotient is infinite and cannot lower the minimum. Thus the minimum in the printed question is exactly 2.

Sign/associate controls: negation preserves both units and principal prime ideals, so adjacency is symmetric. Zero is not an edge difference between distinct vertices; it is excluded from the prime-element convention. Units are excluded from prime elements because their ideals are not proper. A norm -31 prime-element control is \(3+2t\): the quotient map \(t\mapsto14\) to \(\mathbb F_{31}\) kills it and, by index 31, has precisely its principal ideal as kernel. Its negative associate also crosses the two colors. This control tests that negative norm is not mistakenly rejected.

## Source-boundary adversarial controls

The distinction from irreducibles is real. The element 2 is irreducible: a factorization into two nonunits would force both absolute norms to be 2, already excluded. But it is not prime, since \(t\notin(2)\) and \(t^2\in(2)\). Thus an irreducible-difference graph has the triangle \(\{0,1,2\}\), invalidating the candidate coloring. The cited definition selects the prime-element graph and the submitted proof expressly preserves this distinction.

The source theorem is not silently repaired. Literally allowing the unit ideal gives minimum principal-ideal norm 1; even after imposing a proper-ideal restriction, our ring has minimum principal-ideal norm 4, since absolute norms 2 and 3 are impossible modulo 5 while \(N(2)=4\). Its quotient by \((2)\) is not a field. Therefore the principal-ideal minimum cannot be identified with the printed question's prime-ideal minimum 2, and taking the theorem's quoted quotient-field wording as an unrestricted fact would be invalid. The candidate relies on neither operation. As a negative control, over \(\mathbb Z\) the prime-or-unit graph contains the four-clique \(\{0,1,2,3\}\); a literal use of the unit-ideal minimum 1 in that theorem would give an erroneous bound of 2. These observations identify a source wording issue without changing the target question.

The absence of a PID premise in the actual question matters. The nonprincipal ideal is a permitted witness in that domain. A PID-only or irreducible-only reformulation is outside the proved conclusion. Adding the Lenstra–Hurwitz surjectivity condition would also change the defined object, though it is not needed for this witness's clique bound.

## Fresh reproducible diagnostics and their limits

`verify_candidate.py` uses only the Python standard library and read-only Git queries. It has explicit exceptions, no assertion statements. The four recorded executions in `EXECUTION_RECEIPT.json` include ordinary and optimized Python runs, each with 352 passing checks, and deliberate false square-residue certificates that fail with exit code 1 in both modes. Thus validation does not disappear under optimization.

Exact arithmetic diagnostics include all residue classes modulo 5 and 4; all denominators whose squares divide 40; 6,561 product and 6,561 sum checks for the quotient map on a small box; direct coset enumeration for 48 nonsingular multiplication lattices; 44 constructed non-domain witnesses for even-constant elements; the edge, sign and norm controls above; a wrong-coefficient-coloring failure on the unit edge; a distinct-field control; and current metadata verification with explicitly selected schemas. Lattice enumeration uses exact adjugate divisibility, not floating point. It provides a consistency check of concrete cases; the universal index and ideal proofs are written above.

These finite checks do not classify units or prime elements, prove nonexistence from a bounded search, establish a class number, or prove the infinite graph result by enumeration. The written universal arguments are the proof. No source-author software was run.

To reproduce: run `python3 verify_candidate.py` or `python3 -O verify_candidate.py` from this directory or by absolute script path. Adding `--self-test-corruption` intentionally exits nonzero. Inputs must remain at the recorded audit location with the actual Git objects available.

## Present provenance checks and exact remaining limits

The public manifest's actual schema is `files[]` with keys `path`, `bytes`, `sha256`; it deliberately lists nine files and excludes itself. Its declared `file_count` is ten, counting itself. All nine rows authenticate, and their union with the manifest is exactly the submitted directory. There is no self-hash cycle or missing tenth-file error. The ten files total 56,661 bytes, matching the supplied PR body.

The checker separately selects `ACCEPTANCE.required_joint_artifacts[]`, `ACCEPTANCE.source_metadata[]` and its editorial-map singleton, plus `AUDIT_MANIFEST.artifacts[]` using its different `file` key. All present-file identities agree. In `EDITORIAL_MAP`, output identities, replacement bytes/hashes, unchanged/protected output slices and the exact output partition all verify. Historical input identities are a separate schema and were not guessed into present membership.

Three changed historical input bodies (old proof, old review, old audit manifest) are unavailable in the submitted ten-file snapshot. The present map's removed-input hashes therefore cannot be independently replayed here, nor can the historical claim that all original mathematical text was preserved be authenticated against those old bodies. The unchanged source/literature bodies do match their declared historical identities. This is a stated provenance limit, not a mathematical gap in the authenticated current proof. Historical audit independence, old searches and old publication-validator execution are likewise not retroactively certified by matching present hashes.

Strongest verified result: a complete elementary counterexample to the precise universal equality printed in the pinned Question 7.2 under the cited prime-element convention. Required mathematical repairs: none. Remaining gaps for other claims: novelty/priority, final-version relationships and unavailable historical editorial replay. This review grants no publication or merge approval. No individual was contacted.
