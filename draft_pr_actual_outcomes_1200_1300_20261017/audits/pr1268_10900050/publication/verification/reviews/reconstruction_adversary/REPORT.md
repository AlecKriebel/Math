# Adversarial verification of the sealed source-only reconstruction

Verdict: **PASS within the stated printed-question scope.** No actionable mathematical or source-scope defect was found. The sealed reconstruction supplies a checkable counterexample to universal equality in Long's Question 7.2, interpreting a prime difference as a prime element, as required by the cited author definition. This review grants no priority, novelty, present-day openness, publication, release, or PID-restricted result.

This is a new adversarial review of the sealed source-only work. I did not inspect the candidate submission, PR body, submitted folder, root mathematics, or another review. Reading the reconstruction necessarily disclosed its proposed example before my independent verification; this audit is therefore independent verification of a disclosed construction, not a second blind discovery. The reconstruction's historical source-only independence is attested by its own seal, not something hashes alone can prove. The same quadratic example and its two proof formulations count as one obstruction mechanism, not distinct approach families.

## 1. Exact claim, assumptions, and falsification criteria

The claim under review is that there exists a totally real number field in the setup of the versioned question for which

\[
\omega(\Gamma_{\rm prime})<
\omega(\Gamma_{\rm unit})\min_{\mathfrak p\ne0\text{ prime}}|\mathcal O_k/\mathfrak p|.
\]

Here all algebraic integers are vertices, a unit difference is an edge in both graphs, and a nonzero prime-element difference is an additional edge in the prime graph. A prime element is a nonzero nonunit generating a prime ideal; irreducibility alone is insufficient. The field is not required to have class number one or be a PID. The target is the prime-ideal minimum actually printed in the question, not the principal-ideal parameter of the cited theorem.

I attempted to falsify: membership of the example in the field family; the claimed full ring of integers; the determinant/index formula; nonprincipality; the exclusion of prime elements from the chosen ideal; the direct arithmetic alternative; the global rather than bounded nature of the clique upper bound; the interpretation of prime versus irreducible; and the checker replay contract in optimized Python. Failure of any essential step, a missing PID assumption in the source, or changed sealed bytes would require changes. None occurred.

The verified exact values are

\[
k=\mathbb Q(\sqrt {10}),\quad R=\mathcal O_k=\mathbb Z[\sqrt {10}],\quad
\omega_u=\omega_p=2,\quad m=2,
\]

so the proposed equality becomes the false equality \(2=4\). The exact remaining mathematical gap for this counterexample and the printed universal equality is **none**. A statement restricted to PIDs is outside the verified claim.

## 2. Input authentication and read ledger

The sealed input directory is `../source_question_family/`. I explicitly parsed its actual schema `authored-file-manifest-v1`: the top-level list is `files`; each entry uses `relative_path`, `size_bytes`, and `sha256`. No invented `authored_files` input key was used. The source manifest also declares `self_excluded`, `excluded_directories`, and `paths_relative_to`.

The three externally supplied SHA-256 anchors matched at initial authentication:

| Input | SHA-256 |
|---|---|
| `SOURCE_ONLY_RECONSTRUCTION.md` | `2103dde0343d006ce2d2caf4440355d5c88b1f02841bee6896eaa9fa5e0fff6c` |
| `VERDICT.json` | `bc654f898c640c34e67e8729f2625bcedb175547a4a2610caa26812527118acd` |
| `MANIFEST.json` | `a7514fa649aa012aca37b753d5840011c18f45a4db6996467dd994f79a86eb2f` |

All eight manifest-listed files were read in full and their actual bytes, sizes, and hashes checked: `.gitignore`, `FINITE_CHECK_RESULTS.json`, `RESEARCH_LOG.md`, `SEAL.json`, `SOURCE_ONLY_RECONSTRUCTION.md`, `SOURCE_PROVENANCE.json`, `VERDICT.json`, and `finite_checks.py`. I also read the complete source manifest itself and the governing repository `AGENTS.md`. The start record is `INPUT_AUTHENTICATION_START.json`; a separate end record checks every listed input again, compares against the start, rechecks all three external anchors, and verifies independently retrieved raw-source hashes. The sealed input directory was never written.

Primary sources were independently retrieved through HTTPS, opened through the web tool, rendered locally, and visually inspected in the critical scope:

| Primary | Independent bytes / SHA-256 | Actually verified scope |
|---|---|---|
| [Delp, Hoffoss and Manning, versioned question PDF](https://arxiv.org/pdf/1512.04620v1) | 280293 / `7c0dbfb0f5f5f5e39d876dbe0734c4c9df927ed23a29917008ccec77073f00e4` | Full rendered printed pages 5, 6, 7 visually inspected; Section 7.1 setup, all of Question 7.2, and reference [19] read for this audit. |
| [Long and Thistlethwaite, author-hosted PDF](https://web.math.ucsb.edu/~long/pubpdf/LenstraHurwitz.pdf) | 250475 / `166238dd17c2a2ffe1408c5f5c3d2f1ce9ae914c48f657ac309b7a83ee07594c` | Full rendered printed pages 1, 9, 10 visually inspected; initial conditions (i)-(ii), Section 3 prime-clique definition, Theorem 3.1 and its complete proof read. |

Both independent raw hashes exactly match `SOURCE_PROVENANCE.json`. The question PDF has 7 pages and the author PDF 16. Their URLs and exact bytes, rather than metadata dates or guessed revision history, anchor this audit. The author URL is unversioned.

Unread or not audited: question PDF pp.1-4; author PDF pp.2-8 and 11-16; unrelated questions and references on visually inspected pages; the preceding theorem proof on author p.9 and the corollary on p.10; the original reconstruction's ignored `_local/` contents; candidate and other research inputs; present-day literature or priority. Extracting or opening a whole PDF is not represented as reading all its pages. No outside person was contacted or outreach prepared. No Git, branch, index, PR, service, release, or publication writes occurred. All new files are confined to this review folder, whose `.gitignore` was written before raw downloads or renders were created.

## 3. Source interpretation attack

The visual question pages confirm that the irreducible polynomial has all real roots, \(k=\mathbb Q(\alpha)\), and \(\mathcal O_k\) is its full ring of integers. The preceding PID and Euclidean questions are questions about this family, not assumptions imposed on it. Question 7.2 refers back to that family and adds prime differences to the unit graph. Its displayed minimum is over prime ideals. This validates the reconstruction's printed-scope interpretation. [Versioned question, printed pp.5-7](https://arxiv.org/pdf/1512.04620v1).

Condition (i) in the author definition requires a nonunit difference to generate a prime ideal. Section 3 explicitly uses condition (i) alone for prime cliques. Condition (ii), requiring the units to surject onto the nonzero residue classes, belongs to Lenstra-Hurwitz cliques and is not needed for the prime graph here. Theorem 3.1's parameter is worded as a principal-ideal minimum, whereas its proof describes the quotient as a field and its generator as prime. The reconstruction correctly records this wording distinction without using it to add a PID hypothesis or change the printed target. [Author PDF, printed pp.1,9-10](https://web.math.ucsb.edu/~long/pubpdf/LenstraHurwitz.pdf).

Nonblocking clarification: the quotient-field wording of that proof is stronger than necessary for its principal-ideal bound. A finite quotient ring still partitions a clique, and if a nonunit \(q\) divides a prime-element difference, the cofactor must be a unit. Thus this audit does not infer that the cited theorem's numerical inequality is false. It verifies only that the reconstruction never equates the distinct minima or relies on the quotient being a field. In the example, \((2)\) has norm 4 and its quotient has a nonzero nilpotent, while \(P=(2,\sqrt {10})\) has norm 2 and field quotient. The mismatch is therefore real and handled correctly.

## 4. Arithmetic and proof audit, in reconstruction order

### 4.1 Field and full ring of integers

\(X^2-10\) is Eisenstein at 2: the constant coefficient is divisible by 2 but not 4, and the other nonleading coefficient is zero. Its two real roots establish the required totally real field.

For an arbitrary integral \(\theta=x+y\sqrt {10}\) with rational \(x,y\), trace \(t=2x\) and norm \(n=x^2-10y^2\) are integers. This standard integrality property follows since conjugates of algebraic integers are integral, their sum and product are integral, and a rational algebraic integer is an integer. Consequently \(40y^2=t^2-4n\) is integral. If \(y=r/s\) in lowest terms, then \(s^2\mid40\); hence \(s=1\) or 2. Setting \(u=2y\), we obtain \(t^2-10u^2\equiv0\pmod4\). Odd \(u\) would force a square to be 2 modulo 4. Therefore \(u\) is even, then \(t\) is even, proving \(x,y\in\mathbb Z\). Conversely the displayed monic polynomial for \(a+b\sqrt {10}\) proves integrality of every element of \(\mathbb Z[\sqrt {10}]\). This argument includes rational elements and does not assume the usual quadratic integral-basis formula.

The denominator and parity steps are exact, not asymptotic. As a boundary control, \((1+\sqrt5)/2\) is integral in the neighboring field, with norm -1 and trace 1; the same odd/odd parity pair is allowed with coefficient 5 but forbidden with 10. Thus the proof is not an unjustified generalization from a quadratic order to every quadratic maximal order.

For \(z=a+b\sqrt {10}\), the signed norm is \(a^2-10b^2\), nonzero when \(z\ne0\). Expansion gives the identity

\[
(ac+10bd)^2-10(ad+bc)^2=(a^2-10b^2)(c^2-10d^2),
\]

proving multiplicativity for all integer coefficients. An inverse forces the integral norm to divide 1, and a norm of either sign 1 provides the conjugate inverse in the ring. This validates the unit criterion without enumerating units.

### 4.2 Quotient, ideal norm, and nonprincipality

The map \(a+b\sqrt {10}\mapsto a\bmod2\) is unital, multiplicative, additive, and onto \(\mathbb F_2\). Its kernel consists exactly of even constant coefficients, and equals \((2,\sqrt {10})\). Its index is 2, so this nonzero proper ideal \(P\) is maximal and prime. Every nonzero prime-ideal quotient is a field with at least two elements; since this one has two, the minimum is exactly 2. Inclusion of the zero prime would only add the infinite quotient and cannot lower this minimum.

If \(P=(a+b\sqrt {10})\), multiplication on the proved integral basis has columns \((a,b)\) and \((10b,a)\). Its nonzero determinant is \(a^2-10b^2\). The index of the image of a full-rank integer matrix is its absolute determinant, so \([R:P]=2\) forces norm \(\pm2\). Modulo 5, the squared constant coefficient would have to be 2 or 3. The complete square residue set is \(\{0,1,4\}\). Hence \(P\) is nonprincipal. No class number, factorization of ideals, or PID assumption enters.

The optional minimum-proper-principal-ideal assertion also checks: the same residues exclude norms \(\pm3\); nonzero nonunits have absolute norm at least 2; 2 and 3 are excluded; and the element 2 has absolute norm 4. Norm-one principal ideals are the unit ideal and must be excluded, as the report explicitly says. Independently, \(P^2=(4,2\sqrt {10},10)=(2)\), using \(2=10-2\cdot4\); this is consistent with, but not needed for, the index proof.

### 4.3 Nonprincipal prime-ideal obstruction and its boundaries

A unit cannot lie in a proper ideal. If a nonzero prime element \(\pi\) lay in \(P\), its nonzero principal prime ideal would be contained in \(P\). In this ring the quotient \(R/(\pi)\) has finite size \(|N(\pi)|\) by the determinant calculation. Primality makes it an integral domain, and every finite integral domain is a field: multiplication by a nonzero residue is injective, thus surjective, yielding an inverse. Therefore \((\pi)\) is maximal, and containment in proper \(P\) gives equality, contradicting nonprincipality. This verifies the critical lemma without assuming unique factorization.

For any ring of integers the same result follows since every nonzero prime ideal is maximal. The mechanism actually survives in any number-field order, because a nonzero principal ideal still has finite index; integral closure is not required for this particular lemma. That extension is an explanatory boundary observation, not a new claim needed for the source problem. In rings of integers, the criterion is exact: a nonzero prime ideal is nonprincipal precisely when it contains no prime element, since a principal prime ideal contains its prime generator.

It must not be extended to arbitrary domains. In \(\mathbb Z[X]\), the ideal \((2,X)\) is nonprincipal and maximal, but it contains the prime element 2, since \(\mathbb Z[X]/(2)=\mathbb F_2[X]\) is a domain. To see nonprincipality, a proposed generator would divide the constant 2, so have degree zero; a nonunit constant divisor would be associated to 2, whose ideal does not contain \(X\). The key failure is that the nonzero principal prime ideal \((2)\) is not maximal. The reconstruction restricts its lemma to rings of integers, so this countercontrol does not falsify its actual statement.

### 4.4 Universal graph bound and attained lower bound

Equal residues of distinct vertices mean their nonzero difference lies in \(P\). The preceding lemma prohibits both allowed edge types. Thus reduction modulo \(P\) is injective on every prime clique, without any bound on coordinates or prior finiteness assumption. There are two residues, hence every clique has at most two vertices; an infinite clique is excluded for the same reason. Unit cliques obey the same bound because the unit graph is contained in the prime graph. The pair \(\{0,1\}\) is a unit clique and attains both bounds. This proves exact global maxima, not empirical maxima from a finite search.

Zero never labels an edge because the graph uses distinct vertices. Sign invariance of units and prime elements makes the edges undirected. Zero as a vertex is harmless and supplies the lower-bound witness. The argument does not require any prime-element classification or residue-unit surjectivity.

### 4.5 Direct arithmetic alternative and irreducible control

For a nonzero element \(\delta\) with even constant coefficient, its integral norm is even, so it is not a unit. If it were prime, it would divide its nonzero rational integer norm. Factoring the absolute integer norm into rational primes and repeatedly applying the defining divisibility property forces \(\delta\) to divide some rational prime \(p\). The factor -1, if present, is a unit and cannot be divisible by \(\delta\). Applying the quotient map to \(p=\delta\gamma\) makes \(p\) even, so \(p=2\). Then \(4=|N(\delta)||N(\gamma)|\); the even absolute norm of nonunit \(\delta\) is 2 or 4. The modulo-5 obstruction removes 2; norm 4 makes \(\gamma\) a unit, so \(\delta\) is associated to 2. But \(2\mid(\sqrt {10})^2\) and \(2\nmid\sqrt {10}\) in the established coefficient basis. Hence 2, and any associate, is not prime. This completes the direct argument without ideals.

The report correctly labels this as the same parity/norm obstruction, not independent discovery evidence. The element 2 is nevertheless irreducible: a factorization into two nonunits would give absolute norms 2 and 2, already excluded. Thus under the wrong irreducible-edge convention the pairwise differences of \(\{0,1,2\}\) are allowed. This three-clique is a genuine semantic countercontrol, proving that replacing prime by irreducible changes the graph. It is not a counterexample to the reconstruction's prime-element graph.

## 5. Reproducibility and adversarial finite controls

`audit_checks.py` reads the source manifest in its actual schema, authenticates every listed file, copies the sealed checker into the specified scratch directory, and runs only copies. No sealed input output is overwritten. Its independent `--worker` mode has no file writes and uses exact integer or rational arithmetic with explicit exceptions. A replay command from this folder is:

```text
python3 audit_checks.py --source ../source_question_family --scratch ignored_local/replay --output ignored_local/replay/CHECK_RESULTS_replay.json
```

The checker and independent worker each passed normal, `-O`, and `-OO` Python. The sealed checker's stdout was byte-for-byte identical to the sealed `FINITE_CHECK_RESULTS.json`, with SHA-256 `0ec1bf74f3ea21d3392bc86e7bd45041eb457e2372b958ba5b9a24ee239f864e`, in all three modes. The independent worker checked the complete finite residue spaces and 6561 exact norm-multiplication pairs; its semantic results were identical across all modes. The universal norm identity and proof above do not rely on this bounded coefficient check.

Six independently generated checker mutants were each rejected with the expected explicit exception in all three modes, for 18 passing negative controls: wrong modulo-5 residue target; wrong quotient coordinate; wrong quadratic multiplication relation; wrong divisibility predicate; wrong denominator divisibility condition; and wrong trace congruence coefficient. The recorded results include the expected exception messages. These targeted controls establish that those guards execute under optimization; they do not claim exhaustive mutation coverage or prove the quantified mathematics by execution.

Finite complete residues establish the modular obstructions and map identities because the relevant functions factor through those finite rings. Finite computation alone does not establish the full ring of integers, the lattice-index theorem, maximality of nonzero principal primes, or the global clique bound. Those are separately justified in Section 4. The checker honestly claims only finite support, so its narrower coverage is not a defect.

## 6. Findings, exact gap, and seal boundary

Actionable findings: **none**. Required changes: **none**. The principal-ideal wording distinction is already documented in the input and is retained as a scope clarification, not silently corrected by assuming PID. The direct proof is correctly described as sharing the first proof's mechanism. No part of this review verifies novelty, firstness, present-day literature completeness, a theorem for all PID fields, or publication readiness.

The only release from this audit is an authenticated mathematical-review packet under `reconstruction_adversary/`: this report, machine-readable verdict, source-retrieval ledger, initial/final input authentication records, exact checks/results, research log, and authored-file manifest. Raw PDFs, extracted text, rendered pages, checker copies, and negative-control scripts are excluded as ignored local scratch. The manifest excludes itself and raw material. Its own hash and the report/verdict hashes are reported to the commissioning root outside the manifest.

Completion estimate: **100% of the scoped adversarial validation**, conditional on the final recorded hash reauthentication succeeding. No new external input was necessary. No changes to the sealed family are recommended.
