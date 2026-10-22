# Independent algebra and Meyer-signature audit: PR938 / 30003634

This family passes its assigned mathematical claim: the stated nested expression belongs to the ordinary third derived subgroup of the classical pure braid group on three strands, and its ordinary oriented closure signature is **-2** with the published Gambaudo--Ghys convention. The independent calculation uses their Theorem A directly, including singular and zero Meyer forms. It does not use a Goeritz calculation, a historical acceptance verdict, or an original program as a premise.

The complete counterexample remains conditional here on the separately assigned topological statement that an algebraically split 1-solvable link has zero ordinary signature and on identifying the source question's precise filtration. Neither is proved by this family. Subject to those bridges, the witness refutes the universal containment through the single case n=1, m=3. This does not assert failure for every n.

## Scope, provenance, and independence

The inspected proof is the 13,197-byte original PROOF.md at immutable commit `2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b`, prefix `unsolved_math_prioritization/attempts/30003634`, SHA256 `0492e0e0de785be263174e86d69855120b2f5c24b105c6479739cd72d64abe3b`. `AUTH_START.json` and `AUTH_END.json` authenticate every one of the 44 actual Git blobs against the selected disk snapshot, and authenticate the supplied outer manifest pin. The shared working branch stayed main; its current HEAD is distinct from the selected historical commit and is recorded explicitly. This reviewer did not modify Git, the index, branches, originals, PRs, services, trackers, or publication state.

Read order was charter, complete private source record, complete original proof, primary published source, independent definitions/implementation/result, independence checkpoint, then original certificate. No historical audit verdicts, sibling reports, or original programs were read or imported. The source body and downloaded PDF/text/renders remain private. The independent checkpoint pins the implementation and initial output before the certificate was opened. The later comparison checks all 104 terms rather than just their sum.

This reconstructs an existing route explicitly present in the candidate, so it adds **0 positive proof-search turns** to the author's original **1/5** accounting. It is an independent verification mechanism, not a substantively new discovery route. Priority, current openness, and publication readiness were not audited. No person was contacted; communication was limited to the parent root.

## Exact group and strand reconstruction

Write `[x,y]=xyx^-1y^-1`, `a=sigma1^2`, `b=sigma2^2`, `c=[a,b]`, `d=a^-1ca`, `e=b^-1cb`, `u=[c,d]`, `v=[d,e]`, and `beta=[u,v]`. Both a and b are pure because the associated transpositions are squared. Thus c belongs to P3^(1). A derived subgroup is characteristic and therefore normal in P3, so d and e also belong to P3^(1). Hence u,v belong to P3^(2), and beta belongs to P3^(3). This is membership in the ordinary derived series; no finite invariant is being used as a substitute for group membership.

Direct substitution produces 176 Artin letters before cancellation. A stack cancels adjacent inverse letters, leaving exactly 104. These cancellations are free-group equalities, hence are valid in the braid group without any word-problem assumption. Grouping identical adjacent generators gives 46 alternating syllables, or 23 pairs. The independently recovered lists are

```
A = [2,-4,2,2,-2,2,-4,2,2,-2,-2,4,-2,-2,4,-2,2,-2,-2,4,-2,-2,2]
B = [2,-2,2,-2,-2,2,2,-2,-2,4,-2,2,-2,2,-2,-2,2,2,-2,-2,2,2,-2]
```

Both sums vanish; their absolute-value sums add to 104. Expanding these lists reproduces every free-reduced letter. For additional representation controls the programs verify the Artin relation `121=212` both as a matrix equality and as an automorphism of a free group on three generators. They verify inverse cancellation and compare relation insertions in 161 short contexts. These controls do not replace the nested derived-membership deduction.

Following strand labels through each crossing returns the permutation (1,2,3). For each pair of labels the signed crossing sum is zero, so halving gives linking numbers (0,0,0). The full 104-step trace is recorded. Because each closure component comes from a single pure strand, deleting the other strands leaves a one-strand braid. The one-strand braid group is trivial; its usual closure is an unknot. Consequently all three components are unknots (and have Arf invariant zero). No assertion that closure signature is a homomorphism on string links is involved.

## Primary theorem, full applicability, and conventions

The independently downloaded version of record is Jean-Marc Gambaudo and Etienne Ghys, *Braids and Signatures*, Bull. Soc. Math. France 133 (2005), 541--579, DOI [10.24033/bsmf.2496](https://www.numdam.org/item/10.24033/bsmf.2496.pdf). Its SHA256 and the exact complete-page visual scope are in `SOURCE_PINS.json`.

Theorem A, printed p544, applies to any two braids and any nontrivial root of unity. It identifies the closure-signature multiplication defect with minus the Meyer cocycle of the Burau--Squier representation. The definitions on pp542--543 concern oriented links and recover the ordinary symmetrized-Seifert signature at -1. There is no knot-only or non-pure hypothesis and no Alexander-root exclusion. Thus every prefix and signed generator of this pure three-braid is eligible. The positive and negative generator closures are trivial links and have signature zero.

The matrices on p549, evaluated at t=-1 and n=3, give the cohomology representation

```
T1 = [[1,0],[-1,1]],    T2 = [[1,1],[0,1]].
```

Products are read left to right as matrix products on column vectors. The source explicitly distinguishes this representation from the transposed homology anti-representation on pp548--550. Proposition 2.1 and pp550--554 identify it with the first relative cohomology of the branched double cover. For odd n its intersection form is nondegenerate. Here n=3, the fiber is a once-punctured torus, and the relevant real symplectic dimension is two. The identity action on a stabilized orthogonal complement contributes zero to the Meyer form, so the finite 2x2 calculation is the one in Theorem A.

On this two-dimensional space every nonzero skew form is lambda times

```
J = [[0,1],[-1,0]],    Omega(x,y)=x1*y2-x2*y1.
```

Both matrices preserve J. The sign of lambda is fixed by the source, not guessed from the witness: p545 Remark 3 gives signature 1-k for the positive two-strand power of length k. In the containing three-strand space, take k=2. Theorem A then requires Meyer(T1,T1)=+1. With J the image intersection is spanned by e2; choose x=y=e1 and obtain q(e2)=Omega(2e1,e2)=2. Thus the actual source skew form is a **positive** multiple of J in these coordinates. Positive scaling does not change any signature. This determines the convention for all pairs, not merely the tested examples. In particular the positive trefoil has signature -2. Reversing the global ordinary-signature convention would change the final answer to +2 while preserving the required nonvanishing; no repair is needed with the source convention.

## Universal rational Meyer form, including kernels

For any A,B in SL(2,Q), set `D1=A^-1-I`, `D2=I-B`, and

```
E = im(D1) intersect im(D2).
```

For e in E choose x,y with D1*x=e=D2*y. The p544 computational definition is q(e)=Omega(x+y,e). Our implementation first forms

```
K = ker [D1,-D2],     pi(x,y)=D1*x.
```

The map pi is onto E, with kernel `ker(D1) direct_sum ker(D2)`. A basis for K is obtained by exact rational row reduction. Independent pi-images select a basis for E and associated lifts. The matrix of the form in those lifts is `Qij=Omega(x_i+y_i,e_j)`.

There is no hidden inverse of A-I or B-I. If x changes by a vector k fixed by A, then Omega(k,D1*z)=Omega(A*k,z)-Omega(k,z)=0. The corresponding identity for B handles y. Thus q is independent of lifts even when D1 or D2 has a kernel. To see symmetry, write `A^-1*x=x+e` and `B*y=y-e`. Symplectic invariance gives

```
Omega(x,e') - Omega(x',e) = -Omega(e,e'),
Omega(y,e') - Omega(y',e) =  Omega(e,e').
```

Adding proves Qij=Qji. The pullback form on the whole K is therefore Q with an additional radical of dimension dim K-dim E. Computing inertia both on E and on K must give identical positive and negative indices; only the zero index changes. The independent program checks this exactly for every witness term and every additional matrix pair.

Rational symmetric congruences compute inertia. A nonzero diagonal pivot gives the scalar pivot and its Schur complement. If all diagonal entries vanish but an off-diagonal entry is nonzero, the corresponding 2x2 block has one positive and one negative eigenvalue, and an exact block Schur complement applies. An entirely zero remaining block contributes only nullity. Consequently the computation handles zero-dimensional E, nontrivial radical, singular one-dimensional forms, and singular two-dimensional forms without numerical tolerances.

Identity/identity has E=0; identity/transvection also has E=0; equal transvections give a nonzero one-dimensional form; inverse transvections give a zero form on a nonzero line. The short matrix-pair controls realize all E dimensions 0,1,2, including nullities 0,1,2 and both definite and indefinite rank-two forms. This closes the degeneration and kernel issue, rather than assuming nonsingularity from the eventual witness matrix.

## Exact 104-term evaluation and checks

For a word g1...g104, put A0=I and Aj=Aj-1*T(gj). Applying Theorem A at every step, with zero generator signature, gives

```
signature(beta closure) = -sum(j=1..104) Meyer(Aj-1,T(gj)).
```

The initial term is zero. `INDEPENDENT_RESULTS.json` records every prefix matrix, generator, D1,D2, kernel basis, E basis, lifts, both form matrices, both exact inertia decompositions, cocycle value, and accumulated closure signature. There are 50 terms +1, 48 terms -1, and six zero terms. The zero terms occur at steps 1,3,6,7,13,14; step 6 has a nontrivial one-dimensional zero form. The sum is 2, so the ordinary signature is **-2**.

The final matrix is

```
[[-1401703009468415,  3686720931790848],
 [ 2187353096552448, -5753116310519807]].
```

Its determinant is exactly 1, it preserves J, and det(I-B(beta)) is 7154819319988224. The last determinant is an additional exact matrix identity, not the basis for interpreting signature.

The program passes 48 named closure controls (generators, inverses, positive/negative two-braid powers, stabilized unknots/trefoils, figure eight, and small torus braids), plus 161 reduced words for inverse and mirror sign reversal, 161 Artin-relation contexts, 161 free-cancellation contexts, 805 Meyer symmetry tests, and 1,610 cocycle identities. There are 115 distinct short matrices. These finite controls support the implementation; the universal source theorem and rational-form argument provide its mathematical interpretation.

Only after the independent result was checkpointed, `compare_after.py` opened the original certificate. The entire word, all syllables, linking numbers, all four final matrix entries, signature, and **all 104 cocycle values** agree. A second implementation specializes the generator image to its known coordinate line and solves an explicit 2x2 system without the nullspace/form routines; all 104 values agree again, as do 186 short-control crossing terms. The full witness mirror and inverse have signature +2; its reversed word and a conjugate retain -2. The initial private-directory cold replay returned the same complete independent output except for its timestamp. Subsequent hardened stdout-only replays preserve that comparison. No original program was executed or imported.

## Findings, exact remaining gap, and reproduction

**Required corrections within this family: none.** The claimed -2 normalization agrees with the published source. The case distinctions and symplectic orientation are fully supplied by this audit, so there is no unresolved mathematical Meyer-route gap.

**Optional exposition:** the candidate could include the explicit E-space formula and short calibration to make its corroborating signature paragraph self-contained. This is an exposition improvement, not an additional premise required for the independently verified result.

**Outside-family dependencies:** verifying the source's ordinary integral smooth filtration and proving the universal 1-solvable-link signature obstruction remain necessary before promoting the full counterexample. This family does not infer them from the finite signature controls. Priority and immutable/public release decisions also remain outside scope.

Run `python3 reproduce.py` inside this family directory for the independent computation (Python standard library only). Its default is the complete result on stdout; it does not rewrite the sealed baseline. An explicit `--output PATH` is required to save a result. `compare_after.py` also defaults to stdout, obtains a child replay through stdout, preserves the active optimization level, and compares all mathematical data after removing only UTC. `authenticate.py` defaults to stdout; `python3 authenticate.py --output AUTH_END.json` explicitly saves a fresh actual Git/disk authentication. No script writes its result merely because it is imported.

The original independence checkpoint and its result stay byte-identical. Its implementation hash identifies the pre-hardening version, which is retained as a historical pin; the replacement external public-map seal authenticates the current hardened code. The old external seal was `fdef3b2c42f877192921622330166c2986a513cb90be927bb1b7014b78c1cf31` (13 entries). This transition is documented in `HARDENING_LOG.md` rather than silently rewriting the independence history.

All mathematical/provenance checks in the three public programs now use explicit fail-closed exceptions; no optimization-removable checks remain. `hardening_checks.py` verifies full baseline equality and nonmutation of default replays under normal Python, `-O`, `-OO`, and actual inherited `PYTHONOPTIMIZE=2`. Twelve direct valid program replays pass; twenty deliberately false signature, form, authentication, and certificate controls reject. `HARDENING_RESULTS.json` records observed parent/child optimization levels, including environment inheritance. This is code hardening with no mathematical or source change. Re-run it with `python3 hardening_checks.py` (stdout only), adding `--output PATH` only to save a new report.

`PUBLIC_MAP.json` is an explicit curated allowlist with SHA256/size records. It excludes itself, all private/raw/extracted/rendered bodies, replay products, caches, temporary files, and private source records. Its final digest and entry count are reported externally to the parent after all listed files are settled. No release or push was performed by this child reviewer.
