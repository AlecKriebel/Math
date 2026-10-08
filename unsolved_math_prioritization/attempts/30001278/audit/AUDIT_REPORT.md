# Independent mathematical audit: problem 30001278

Problem: OWR-3480-009, queue rank 971. Audit date: 2026-10-07 UTC.

## Verdict

**Accepted as a correctly scoped unresolved partial investigation.** All five complete authored arguments have been read and independently checked. No mathematical correction is required for their stated conclusions. The exact Kummer relative-different estimate remains conditional. This audit does not establish a complete solution, counterexample, novelty, exhaustive literature status, or formal verification.

There is one optional, nonmathematical verifier hardening patch. The original command-line verifier resolves a symlink alias to a clean packet before invoking its root-symlink guard. Its direct integrity API rejects that alias. The optional patch makes the main verifier preserve its direct root path before checking it. This distinction neither permits changed payload bytes under the supplied external anchor nor invalidates a mathematical claim. Details and actual reruns appear below.

### Frozen input binding

- Original archive: `ramification_30001278_author.tar.gz`, 24,920 bytes.
- Original archive SHA-256: `d6bf160fd3973409c26ed8b514bc231956b7d3d113cf888e5e15b5f6060779d1`.
- Original author manifest SHA-256: `e6f747996c9dcf7fd9d525cc34f347577538f169e620b4dd3a98269f27b31e29`.
- The archive contains exactly the 15 regular public files, including the manifest. Every archive member equals its on-disk author counterpart byte for byte. Every one of the 14 manifest entries was independently rehashed outside the author verifier.
- `AUTHOR_MANIFEST.json` is an exact copy of that frozen manifest. `AUTHOR_BINDING.json` records this binding. The original author files and archive were not modified.

The audit consists of this report, newly authored independent controls and their results, source/corpus verification metadata, the optional patch, and a separate audit manifest. It contains no PDFs, source extracts, dataset records, or private coordination material.

## 1. Source question, conventions, and literature scope

The official report's Caruso contribution sets up a perfect residue field and a semistable representation. Its printed pp. 1710–1711 continue with a chosen stable lattice, its reduction modulo p^n, and the associated splitting field. Conjecture 3 changes the normalization parameter from nr/(p−1) to r/(p−1). Its scope is semistable. The final paragraph separately asks about stronger bounds specifically for crystalline representations. Consequently the catalogue's crystalline formulation is a restriction of the conjecture, while its literature explanation conflates two questions. The author packet correctly separates them. [Official OWR report](https://ems.press/content/serial-article-files/46230?nt=1)

The valuation is the extension of the K-normalized valuation. If the different ideal is the d-th power of the maximal ideal of L and m=e(L/K), its value here is d/m. The discriminant exponent over K is fd, where f is the residue degree; it equals [L:K] times this normalized different value. The statements are not about an unnormalized integer different exponent or discriminant exponent.

For r≥1, there is a unique a≥0 satisfying (p−1)p^(a−1)<r≤(p−1)p^a. Set b=r/((p−1)p^a), s=n+a, and

B = 1+e(s+b)−p^(−s).

The packet correctly excludes r=0 from this parametrization. Its Hodge–Tate sign convention agrees with the OWR decomposition into Tate twists. Dualization reverses the weights and preserves the finite free representation's kernel; an arbitrary Tate twist need not preserve that kernel.

The cited ramification results use the shifted numbering G^(μ)=G^(μ−1) in the ordinary Serre notation. For a ramified finite Galois extension, the normalized different is strictly less than the largest shifted upper break. This strict inequality does not supply a rank-independent quantitative gap. A theorem giving trivial action for μ>U yields an upper break at most U; it does not establish endpoint triviality. These distinctions are used correctly throughout.

Caruso–Liu's Theorem 1.1 and Conjecture 1.2 have separate upper-break and different conclusions. Their theorem uses the older nr normalization; the conjecture uses r. The author packet correctly credits the old theorem and does not convert one conjectural conclusion into the other. The quotient-of-lattices formulation is compatible with reduction of a lattice: a quotient killed by p^n is a quotient of Λ/p^nΛ, and its splitting field is a subfield. [Caruso–Liu manuscript](https://xavier.caruso.ovh/papers/publis/boundramif.pdf)

Caruso's Theorem 3.28 explicitly states the upper-break conclusion. The global field convention allows a complete discretely valued mixed-characteristic field with perfect residue field. The finite-extension-of-Q_p assumption in Theorem 3.5 is attached to that finite-height/potential-semistability result; it is not a displayed hypothesis of Theorem 3.28. The ramification proof also points to Liu's integral theory. This audit accepts Theorem 3.28 as stated rather than extending Theorem 3.5. The inspected text is the 2012 manuscript, with the 2013 Duke publication confirmed bibliographically; no comparison with the journal PDF is claimed. [Caruso manuscript](https://xavier.caruso.ovh/papers/publis/phitau.pdf), [arXiv revision and journal reference](https://arxiv.org/abs/1010.4846v3)

## 2. Approach 1: upper break versus different

**Accepted:** the target holds whenever r≥p^a+1, in the entire semistable lattice setting.

Independently substituting Caruso's bound gives

U = 1+es+max{eb−p^(−s), e/(p−1)},

U−B = max{0, e(p^a−r)/((p−1)p^a)+p^(−s)}.

The first argument supplies the maximum exactly when e(r−p^a)≥(p−1)/p^n. The right side lies strictly between 0 and 1 and the left side is integral. Thus the condition is precisely r≥p^a+1. In that region the strict different-versus-break inequality proves the target strictly. The unramified case is immediate since B>0.

When a≥1, the exceptional integers run from (p−1)p^(a−1)+1 to p^a, numbering p^(a−1); when a=0 the sole exceptional integer is 1. The positive loss stated by the author follows by subtraction. At r=p^a it equals p^(−s), and throughout the exceptional band it remains positive. Therefore d<U alone does not imply d≤B.

I independently reconstructed the integral identity from the lower different sum. Removing an unramified part reduces to inertia order m. The tame contribution is 1−1/m, and the Herbrand substitution on each positive lower interval gives integrand 1−1/|G^(u)|. Thus d≤μ(1−1/m)≤U(1−1/m). The supplementary criterion U/m≥U−B is valid when m is actually bounded. No arbitrary synthetic filtration used in checking this identity is asserted to arise from a semistable lattice.

For (p,e,n,r)=(3,1,2,7), the independent values are a=2, b=7/18, s=4, B=871/162, U=11/2, and U−B=10/81. The maximum cannot be erased. This is a deduction gap, not a counterexample to the conjecture.

## 3. Approach 2: Kummer tower

**Accepted:** the tower calculations and conditional reduction. **Not established:** its antecedent for arbitrary input.

For K_j=K(π^(1/p^j)), the defining polynomial is Eisenstein and its root generates the integral ring. Its derivative has K-normalized valuation ej+1−p^(−j). This also works at j=0. With L_j=LK_j, different transitivity gives

d(L/K) ≤ d(L_j/K) = ej+1−p^(−j)+d(L_j/K_j).

At j=s, the condition d(L_s/K_s)<eb therefore implies d(L/K)<B. This implication does not require K_s/K to be Galois; L_s/K_s is Galois.

The stated property (P_eb) is measured using v_K and quantifies over all algebraic E/K_s. In K_s-normalized units, its threshold is p^s eb=er p^n/(p−1). Caruso–Liu's Proposition 4.2.1 and Corollary 4.2.2 support the deduction of the strict relative different bound from this property. The valuation scaling and strictness are correct. [Caruso–Liu, pp. 17–19](https://xavier.caruso.ovh/papers/publis/boundramif.pdf)

The older method allows any N satisfying its monomial-annihilator hypothesis. Its strict level condition is j>n+log_p(N/(e(p−1))), and its relative contribution is Np^n/((p−1)p^j). The author does not assume N=er without justification.

Caruso's later proof changes the Witt ideals and obtains the Galois-control inequality j>n−1+log_p r. The chosen s satisfies that strictly because r≤(p−1)p^a<p^(a+1). The source proof is a sketch referring to the earlier method. Its explicit upper-break theorem and its equal-characteristic Witt-ideal containment do not, merely by quotation, constitute a reconstructed finite-level mixed-characteristic lifting argument at the exact relative precision eb. The report correctly leaves that argument conditional rather than rejecting the source theorem or claiming the desired relative statement is unknown to the literature. [Caruso, Lemma 2.13 and Theorem 3.28 proof](https://xavier.caruso.ovh/papers/publis/phitau.pdf)

For the hypothetical sharper estimate at level j, the total expression is

F(j)=1+ej+(er p^n/(p−1)−1)/p^j.

Its adjacent difference is e−er p^(n−j−1)+(p−1)p^(−j−1). At j=s−1 this is e(1−r/p^a)+(p−1)p^(−s), positive in the exceptional band. However, the lower-level precision epb exceeds e. Equivariance at that level does not supply the old method's mixed-characteristic precision. At b=1, the older strict level condition becomes equality at s; the author properly routes that endpoint through Approach 1 instead.

## 4. Approach 3: height annihilators

**Accepted:** all cases p^(n−1)|r, including all n=1, and the exact scalar obstruction.

Write E=u^e+pH. In the binomial expansion of (E−pH)^r, the j-th non-leading coefficient is p^j binom(r,j). From j binom(r,j)=r binom(r−1,j−1), its valuation is at least v_p(r)+j−v_p(j)≥v_p(r)+1. Under the divisibility hypothesis this is at least n. Thus u^(er) vanishes modulo (p^n,E^r).

For b<1, N=er now satisfies the old strict level condition at s and its relative estimate gives the target. For b=1, Approach 1 applies. More generally R=p^(n−1)ceil(r/p^(n−1)) gives u^(eR)≡E^R modulo p^n, hence a valid annihilator modulo E^r. This is consistent with and already encompassed by Caruso–Liu Lemma 2.4.1; no new comparison theorem is being asserted. [Caruso–Liu, §2.4](https://xavier.caruso.ovh/papers/publis/boundramif.pdf)

For E=u^e−p, introduce z=u^e−p. The quotient is free on 1,u,…,u^(e−1) over W_n(k)[z]/z^r. Hence the coefficient test for (z+p)^m is both necessary and sufficient, not merely an upper bound. The minimal u-nilpotence exponent is eM, with

M = min{m≥r: m−j+v_p(binom(m,j))≥n for 0≤j<r}.

No m<r works because the coefficient of z^m is 1. The bounds r≤M≤r+n−1 follow directly. At m=r, the minimum coefficient valuation is 1+v_p(r): the preceding binomial lower bound proves one inequality and k=1 attains equality. Thus M=r exactly when p^(n−1)|r. The argument also justifies the assertion that no intermediate exponent eM−t, 1≤t<e, vanishes.

At p=3,n=2,r=7, M=8 and the coefficient 21 is nonzero modulo 9. The effective bound 440/81 exceeds 871/162 by 1/18. The monotonicity argument is correct: within each normalization interval the bound rises strictly, and its right jump at a power of p is e/p+(p−1)p^(−(n+a+1))>0. A larger annihilator cannot be hidden by renaming the parameter.

These obstructions refute a proposed proof substitution. They do not refute the different conjecture.

## 5. Approach 4: explicit characters and nonsplit lattices

**Accepted:** the integrally split theorem at arbitrary rank and the crystalline lattice obstruction to a rational-splitting reduction.

A finite unramified extension U kills the finite reductions of the unramified characters, so the actual integral direct-sum representation has splitting field contained in U(ζ_(p^n)). Differentiating the cyclotomic polynomial at a primitive root gives valuation e(n−1/(p−1)).

The author does not assume monogenicity over U. If f is the minimal polynomial and A=O_U[ζ], then the trace dual of O_M lies in the trace dual of A, which is f'(ζ)^(−1)A. Hence f'(ζ)O_M⊆D_(M/U). Since the complementary monic factor of the cyclotomic polynomial is integral, d(M/U)≤v_K(f'(ζ))≤e(n−1/(p−1)). Different transitivity then supplies the same bound for L/K. Its difference from B is strictly positive. The trace-dual inclusion has the correct direction.

For the lattice over K=Q_p(ζ_(p^m)), I independently conjugated diag(χ,1) by the basis matrix with columns e_1 and (e_2−e_1)/p^m. This gives exactly the displayed integral matrix with off-diagonal entry (1−χ)/p^m. It is integral because χ(G_K)=1+p^m Z_p. Modulo p^n, its kernel requires and is implied by χ≡1 modulo p^(m+n), giving L=K(ζ_(p^(m+n))) of degree p^n over K.

In contrast the standard split lattice gives K(ζ_(p^n)). Modulo p, the special lattice has trivial diagonal characters and nontrivial unipotent inertia of order p. The residual semisimplification therefore loses actual wild ramification. This example is realized inside a crystalline rational representation; it is not an unrealized matrix construction.

Subtracting the two absolute cyclotomic different valuations gives d(L/K)=e_K n, and B−e_K n=1+e_K/(p−1)−p^(−n)>0 for r=1. The example exposes the reduction error without contradicting the target.

## 6. Approach 5: inertia order

**Accepted:** the actual inertia-order criterion, the ambient GL criterion, and every rank-one case.

Let m=e(L/K), t=v_p(m), and pass to the maximal unramified intermediate field. The remaining extension is totally ramified, its integral ring is generated by a uniformizer, and an Eisenstein polynomial f of degree m generates its different through f'. Each nonzero derivative term indexed by i has L-normalized valuation congruent to i−1 modulo m. These residue classes are distinct, including the leading derivative term. Thus the minimal valuation is unique and cannot cancel. In particular

v_L(f'(π_L))≤me t+m−1,

so d(L/K)≤et+1−1/m. The unramified case m=1 yields zero. Completeness and perfectness of the residue field are sufficient; residue-field finiteness is unnecessary.

If t≤s, the gap to B is e(s−t+b)+1/m−p^(−s)>0 because eb>1/p≥p^(−s). This criterion is purely local-field theoretic.

The inertia image embeds in GL_d(Z/p^nZ). Its p-order is at most d²(n−1)+d(d−1)/2, obtained from the reduction kernel and the product formula for GL_d(F_p). Consequently that expression being at most s is sufficient. At d=1 it equals n−1, covering all rank-one representations in the stated numerical setup without any Hodge hypothesis. Failure of the ambient inequality gives no lower bound for actual inertia. In the residual test d=2,n=2,a=2, the ambient value is 5>s=4, so the criterion alone does not settle arbitrary rank-two lattices.

## 7. Separately credited crystalline low weight

For crystalline weights in [0,1], the chosen lattice reduction is the representation of a finite flat group scheme killed by p^n. Hattori's survey states this immediately before Theorem 2.18 and records Fontaine's strict normalized different bound e(n+1/(p−1)). Its initial setup allows a perfect residue field and arbitrary absolute ramification e. The target at r=1 is larger by 1−p^(−n)>0. Therefore every crystalline r=1 case is covered by this separately credited literature input. No higher-weight conclusion follows merely from this finite-flat case. [Hattori survey, pp. 2 and 15](https://www.comm.tcu.ac.jp/shinh/RennesHodge/RennesHodge.pdf)

Hattori's 2009 upper-break theorem distinguishes r=1 from 1<r<p−1: the former displayed bound is larger than B by p^(−n), while the latter agrees with B. The author correctly avoids using qualitative strictness to erase that positive loss. The arXiv record confirms revision v4 on 20 June 2009. The retained PDF's internal date says November 19, 2018; that does not contradict the separately stated arXiv submission date and is not treated as a new theorem revision. [Hattori record](https://arxiv.org/abs/0801.2149)

The 2026 Wach-module theorem concerns mod p crystalline representations over absolutely unramified bases, including abstract and geometric cases. The other inspected 2026 article's ramification theorem concerns mod p geometric cohomology. Neither scope alone supplies arbitrary mod p^n crystalline lattices. Publication information was checked against the author's bibliography and the publisher record. [Wach-module manuscript](https://arxiv.org/abs/2410.23453v2), [author bibliography](https://pcoupek.github.io/research.html), [Documenta publisher record](https://ems.press/journals/dm/articles/14299210)

## 8. Executed controls and their limitations

### Frozen author checks

The original verifier passed with the external manifest anchor, both normally and with Python optimization. Both author scripts also passed in a source-free isolated copy, normally and optimized. The normal and optimized stdout hashes agree exactly for each script. The author mathematical result contains 60,000 parameter controls, 1,350 scalar polynomial cases, 720 general Eisenstein cases, 1,779 lattice cases, 11,055 lattice product cases, and the other recorded counters. The author's 17 negative controls passed in both modes.

### Independent checks

`independent_controls.py` imports no author code and uses no Python assertions. Normal and optimized executions produced identical `INDEPENDENT_RESULTS.json`:

- 4,185 independent parameter-boundary cases, including larger primes and heights than the author's sample
- 810 scalar nilpotence checks using binary polynomial exponentiation and modular long division, checking both the proposed vanishing exponent and its immediate predecessor
- 864 general Eisenstein polynomial checks
- 1,779 rational matrix conjugations and exact kernel checks
- 1,080 derivative-term valuation profiles
- 280 direct general-linear group-order checks
- 54 synthetic filtration identities

These are bounded independent controls. They do not enumerate actual ramification fields, validate arbitrary semistable comparison data, or turn finite samples into proofs. The infinite arguments are the mathematical reconstructions above.

### Corruption tests

The independent adversarial harness recorded 33 rejections, including changed bytes in each of the 14 author payload files, malformed or duplicate manifest data, boolean/negative sizes, invalid fingerprints and paths, extra source-like or hidden files, a nested directory, symlink payloads, a missing manifest, an anchored coordinated prose/manifest change, incompatible math-only/anchor options, and a direct API symlink root.

Two accepted behaviors were deliberately measured:

1. An authored mathematical prose error plus a coordinated manifest rehash passes an unanchored integrity call. This is expected and already disclosed by the packet: internal consistency is not authenticity, and the arithmetic controls do not parse or prove the prose. The supplied external anchor rejects the same coordinated change.
2. The original verifier CLI accepts a direct symlink alias to the same clean anchored packet because `resolve()` precedes the root check. The direct API rejects it. This is path-alias acceptance, not changed-byte acceptance.

The verifier also remains a bounded-control program rather than a malicious-code sandbox or proof assistant. Its arithmetic helpers are tested only in the stated prime/integer domain; their limited argument validation is not a mathematical extension to arbitrary caller inputs. An untrusted executable must itself be authenticated externally before its self-report is relied upon.

### Optional hardening

`OPTIONAL_CLI_HARDENING.patch` changes only the main verifier's root construction from `resolve()` to `absolute()` and updates the affected manifest entry. It applies cleanly to an isolated copy of the original packet. The patched manifest SHA-256 is `3fd0911eb41ac797bc393d822e65eeda04bf3afc3f10df1b21620acb4a427e8c`.

Both scripts pass normally and optimized after application, and both executions of the patched main verifier reject the direct symlink-root alias with the intended diagnostic. All mathematical outputs remain identical. This narrow patch does not claim to reject all symlinks in ancestor paths, change the negative-controls helper's own path-alias behavior, or alter deliberate math-only operation. Applying it creates a new author manifest identity; it must never be represented as the original frozen author packet.

## 9. Source and corpus verification

All eight cited retained PDFs were independently re-fetched from their listed public URLs during this audit. Each fresh retrieval matched the retained bytes and SHA-256 exactly. The original OWR target page, Caruso theorem page and proof page, and Fontaine finite-flat statement as reproduced in Hattori were independently re-rendered and visually inspected. Relevant extracted statement/proof sections were read; this does not claim a line-by-line audit of every page of all cited papers.

Both full corpora were independently hashed and parsed. Counts, the unique matching problem row, canonical problem-object hash, and absence of a matching research key or problem-ID literal all agree with the author metadata. `CORPUS_CHECK.json` contains only verification metadata, not dataset contents. These checks authenticate the supplied record and its dated assertions; they do not make its literature assessment authoritative.

## 10. Exact accepted coverage and remaining gap

The accepted sufficient conditions are overlapping:

1. r≥p^a+1, with arbitrary allowed e,n,rank, and perfect residue field.
2. p^(n−1)|r, including all n=1, with the same generality.
3. The specified integral direct sum of unramified twists of cyclotomic powers, at arbitrary rank.
4. Actual v_p(e(L/K))≤n+a; the displayed ambient-rank inequality is sufficient, and all rank-one cases follow.
5. Separately credited: every crystalline r=1 case by the finite-flat theorem.

The Kummer calculation additionally proves a conditional implication: the exact relative bound d(L_s/K_s)<eb, or the stated property (P_eb), would supply the full target. Its general antecedent has not been established here.

The packet's unrestricted example p=3,e=1,n=2,r=7 retains an upper-break margin of 10/81 and an optimized old-scalar margin of 1/18. Neither integral splitting nor a sufficiently small inertia image has been proved for every lattice there. This describes the remaining gap in these arguments, not the global open status of that exact subfamily.

**Final disposition: independent mathematical audit accepted; unresolved partial results; no required mathematical correction; optional narrowly tested verifier hardening only.**
