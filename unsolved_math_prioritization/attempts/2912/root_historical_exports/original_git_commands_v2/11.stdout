# Independent adversarial review: 2912 / Kirby 4.36

**Verdict: PASS for the stated partial deductions and unresolved disposition.** No mandatory mathematical correction was found. This is an independent AI review, not human peer review. It does not certify a solution, a counterexample, or historical novelty.

Reviewed on 2026-09-30 using `gpt-6-astra` with `xhigh` reasoning. The reviewed mathematical artifact is `OBSTRUCTION.md`, SHA-256:

`69a3ffb7b6c2ba3bf1a4df8d7d83960d66095db9d175d78cfe49e2324aac1a71`.

The snapshot is preserved as [reviewed_obstruction.md](reviewed_obstruction.md). Its author used two substantive approaches and explicitly left the original question unresolved. This review did not change the author's files or add a further proof attempt.

## 1. Exact source and scope

The [2026 Kirby survey](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), Problem 4.36, printed pp.219–220, asks whether the homotopy type of an actual 2-knot complement is determined by its complete homotopy 2-type. I checked both pages visually. The invariant includes the fundamental group, its action on the second homotopy group, and the compatible first k-invariant. A chosen boundary identification or meridian is not included in the stated invariant.

[Lomonaco's published paper](https://userpages.cs.umbc.edu/lomonaco/5knots/Lomonaco-Pacific-Journal-Math.pdf), Section X, pp.373–375, confirms the smooth or locally flat PL formulation, the affirmative result when both third universal-cover homology groups vanish, and the criterion involving a finite splitting relative to the meridian. Its list of quasi-aspherical subclasses supports the package's background statements. The draft correctly separates this theorem from the unrestricted question.

The reviewed deductions concern compact oriented exteriors with boundary $S^2\times S^1$. Their interiors/complements have the same homotopy type. They are not statements about arbitrary CW complexes or marked-pair classification.

## 2. Universal-cover homology and the pair-map criterion

The kernel formula in Section 2 is correct with its stated module convention. The meridian has infinite order because it maps to a generator of the infinite cyclic abelianization. Consequently the boundary fundamental group injects as the infinite subgroup $H=\langle\mu\rangle$. Neither $R=\mathbb Z[G]$ nor its restriction to $H$ has a nonzero invariant with finite support. Thus the initial terms of the relative cohomology sequence vanish, giving

\[
H^1(X,\partial X;R)
=\ker\{H^1(X;R)\longrightarrow H^1(\partial X;R)\}.
\]

Degree-one cohomology with local coefficients depends only on the fundamental group and its action. Poincaré–Lefschetz duality therefore identifies $H_3(\widetilde X;\mathbb Z)$ with the conjugate of the asserted group-cohomology kernel. The involution is necessary when converting the right cohomology module to the left homology module; the draft retains it.

For the sufficient pair-map criterion, relative degree one implies boundary degree one by naturality of the homology boundary map. On $S^2\times S^1$, the integers induced on the generators of $H^1$ and $H^2$ multiply to the boundary degree. Both are therefore units. In particular, the boundary fundamental-group map is an isomorphism. Together with the assumed isomorphism of the exterior fundamental groups, this gives an isomorphism of the two restriction kernels. The cap-product identity with the relative fundamental classes then makes the map on $H_3$ of universal covers an isomorphism.

The remaining step is valid: the lifted map is already an isomorphism on homology in degrees 0, 1 and 2, using simple connectivity and Hurewicz. An exterior has the homotopy type of a 3-dimensional CW complex, so no higher homology needs to be checked. A homology equivalence of simply connected CW spaces is a homotopy equivalence, and the fundamental-group isomorphism descends this conclusion to the exteriors.

This criterion does not construct the required map. An isomorphism of the unmarked 2-types has not been shown in the package to give a degree-one map of pairs or the necessary boundary compatibility. The explicitly stated realization gap is genuine.

## 3. Amalgam and restriction-kernel calculation

The presentation in Section 3 agrees with [Hillman's book](https://arxiv.org/abs/math/0212142), Section 14.6, printed p.277. Hillman omits the redundant relation $b^7=1$: conjugating by $a^3=1$ gives $b=b^8$. The group admits the stated description $A*_C B$, where $A=C_7\rtimes C_3$, $C=C_3$, and $B=C_3\rtimes_{-1}\mathbb Z$. The identification of a particular stable letter as a geometric meridian is correctly kept as an additional condition.

The Mayer–Vietoris sequence has the asserted form. Invariants under the infinite groups $B$ and $G$ vanish. The restrictions of $R$ to the finite groups $A$ and $C$ are sums of regular modules, with zero positive cohomology. In particular, the next $H^1(C;R)$ term is zero, justifying the surjection onto $H^1(B;R)$.

The important injectivity of restriction from $B$ to $T=\langle t\rangle$ can also be checked without relying only on transfer. On each regular $B$-block of $R$, write $N_C=1+a+a^2$. The $C$-invariants have basis $N_Ct^n$, $n\in\mathbb Z$, and left multiplication by $t$ shifts this basis. Inflation through $B/C\cong\mathbb Z$ therefore identifies the block contribution to $H^1(B;R)$ with a copy of $\mathbb Z$. For $T$, there are three regular blocks, so the corresponding contribution to $H^1(T;R)$ is $\mathbb Z^3$. Restriction sends the generator represented by $N_C$ to $(1,1,1)$. This is injective, and direct sums give the general assertion. The author's transfer argument is consistent with this explicit description.

It follows that the kernel of restriction from $G$ to $T$ is exactly the image of $R^C$, namely $R^C/R^A$. On every right $A$-coset, this quotient is

\[
\mathbb Z^7/\mathbb Z(1,1,1,1,1,1,1)\cong\mathbb Z^6.
\]

The diagonal vector is primitive, so this is an integral, torsion-free conclusion, not just a rank calculation over a field. The right $C\backslash A$ permutation convention and its conversion by inversion to the left $A/C$ convention are correct. The displayed actions $j\mapsto 2j$ and $j\mapsto j+1$ satisfy the defining relations. The quotient by the diagonal is used consistently; it has not been silently replaced by an augmentation submodule.

This calculation describes the third-cover-homology module only under the specified group-pair identification. It supplies neither a second exterior nor a compatible isomorphism of complete 2-types. Thus it cannot be promoted to a counterexample.

## 4. Current-source exclusions

Theorem 4.6 of [Jabłonowski's August 2026 preprint](https://arxiv.org/abs/2608.03818) explicitly distinguishes the first k-invariants under every compatible group/module isomorphism. The examples consequently fail the same-complete-2-type hypothesis. I checked the theorem and its explanation in the full cached manuscript; this review does not certify all results of that preprint.

Theorems 1.1, 1.3 and 2.8 of [Conway–Kasprowski](https://arxiv.org/abs/2510.18836), in the August 2026 revision, explicitly require boundary fundamental-group surjectivity. For a 2-knot exterior that image is cyclic, and surjectivity would force $G\cong\mathbb Z$. Their other boundary data and hypotheses must also be satisfied. The draft correctly excludes their use as a solution for general noncyclic knot groups.

The indexed primary opening page of [González-Acuña–Montesinos, 1983](https://www.e-periodica.ch/cntmng?pid=com-001%3A1983%3A58%3A%3A19) states the meridional splitting criterion and announces counterexamples to the proposed converse from infinitely many ends to non-quasi-asphericity. Direct retrieval remains behind a verification page; neither the author nor this review claims to have read the full paper. This limited source use is disclosed. None of the algebraic deductions above depends on its proof.

No exact full resolution was located in this bounded source check. This is a search result, not a theorem that the problem remains open.

## 5. Reproducibility and independent controls

The submitted verifier reproduces all **507 exact assertions**, with output byte-for-byte identical to its committed receipt. The five cached PDF hashes match the author's source manifest. [submitted_verifier.py](submitted_verifier.py) and [submitted_results.json](submitted_results.json) preserve the reproduction.

[independent_checks.py](independent_checks.py) imports none of the author's code. It passes **29,933 exact assertions** covering a permutation construction of the order-21 group, all multiplication laws on the six-dimensional quotient, the primitive diagonal kernel, an integral coinvariant control, the $C_3\rtimes\mathbb Z$ normal form, and finite-support controls for the injective diagonal restriction map described above. Its receipt is [independent_results.json](independent_results.json).

These computations check arithmetic and representation conventions. They do not computationally establish Poincaré duality, group-cohomology exactness, knot realization, or homotopy classification. Those claims were assessed mathematically in Sections 2–3.

## 6. Publication disposition

The package is suitable for a draft PR explicitly labeled **unsolved / stalled, with standard partial deductions and no novelty claim**. Keep both realization gaps and the 1983 source-access qualification. No mandatory correction is required. Review-status metadata may be updated without changing the mathematical text, with the final hash recorded separately.

The general Kirby 4.36 question remains unresolved by this work.
