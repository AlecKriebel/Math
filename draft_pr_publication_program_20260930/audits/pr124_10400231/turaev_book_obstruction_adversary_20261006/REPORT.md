# Independent Turaev book obstruction audit for PR124 / problem 10400231

Status: COMPLETE SOURCE AUDIT — the exact original all-prime family and its general torsion-rank obstruction are direct consequences of published necessary conditions in the 2002 book. This is a blocking novelty finding for presenting those statements as new. An express earlier refutation of Conjecture 12.26, precise historical priority, and publication novelty remain unestablished. No priority or publication clearance is issued.

## Scope and independent inputs

The audit targets the immutable original head `d110ad761291aa6ac1d66d2a49e8b8212c18bed6`, original attempts 2/5. The full original `COUNTEREXAMPLE.md`, `source_record.json`, and `prior_imported_report.json` were read before any other family report. The mathematical/source gate is an authenticated PASS; this audit does not reopen central proof search. Independent checkpoints 01 and 02 were recorded before any inter-family conclusions were read. No tracked file, index, branch, commit, native status, queue, external publication, or service has been edited.

For every prime p, the original claim concerns

\[
H_p=\mathbb Z\oplus(\mathbb Z/p)^3,
\qquad \Delta_p=t+(p^3-2)+t^{-1}.
\]

The polynomial is the ordinary integral order of the infinite cyclic Alexander module, with ambiguity ±t^m; no integer content is divided away. It is symmetric and has value p^3 at t=1. The original central obstruction is ord_1(Δ mod p)≥dim_Fp(Tors H⊗Fp), whereas tΔ_p=(t−1)^2+p^3t has reduced order exactly two.

## Primary pages actually inspected

I viewed the full supplied pixels of printed pp.20,22,23,26,27,28,45,46,114,118 of V. Turaev, *Torsions of 3-dimensional Manifolds* (2002), DOI [10.1007/978-3-0348-7999-6](https://doi.org/10.1007/978-3-0348-7999-6). The root acquired them through the publisher-permitted Google Books preview, book ID `83ZJs9Z9BY0C`; unmodified hashes match the root's `ACTUAL_PREVIEW_PAGES_01.json` and `ACTUAL_PREVIEW_PAGES_02.json`, with the additional valid p.20 documented by `ACTUAL_PREVIEW_PAGES_03.json`. Copyrighted images are not copied into the public audit package.

[Printed p.22](https://books.google.com/books?id=83ZJs9Z9BY0C&pg=PA22) sets II.3 in precisely the closed connected orientable b1=1 case. Its integral polynomial part is B_e=[τ](M,e)=τ(M,e)+t^kν, where k=K_t(e)/2 is an integer and ν=Σ_T/((t−1)(t^{-1}−1)), Σ_T=∑_{f∈T}f. The definition handles every Euler structure; changing it multiplies B_e by a group element. This integral part, rather than τ itself, is the object in the next theorem.

[Printed p.23](https://books.google.com/books?id=83ZJs9Z9BY0C&pg=PA23), II.3.3, treats a splitting H=Z×H^(2)×⋯×H^(n) with at least three finite cyclic factors of descending-divisible orders d_2,...,d_n. With I(H) the integral augmentation ideal and J_d=(I(H),d), it requires B_e∈J_(d_4)⋯J_(d_n). II.3.4 requires the integer augmentation of B_e to be divisible by d_4⋯d_n. The exact original H_p has n=4 and all three d_i=p, so B_e∈(I(H),p) and p divides aug(B_e). These are printed published necessary results, without a special prime-2 restriction.

[Printed p.20](https://books.google.com/books?id=83ZJs9Z9BY0C&pg=PA20) additionally supplies the statements of the abelian Alexander–Fox ideal product (II.2.4) and the free-generator cancellation lemma (II.2.5) used in the proof of II.3.3. The p.19 export is an unavailable-image placeholder; it provides no theorem evidence. Our exclusion uses the complete II.3.3/II.3.4 statements on p.23 and does not require the missing p.19.

## Verified ordinary-Alexander definition and normalization

[Printed p.27](https://books.google.com/books?id=83ZJs9Z9BY0C&pg=PA27), II.5.1, defines the untwisted Alexander polynomial by the greatest common divisor in the integral UFD Z[G] after projecting the Alexander–Fox ideal to G=H/Tors H. Its ambiguity is only ±G. The gcd is not taken over Q[G], and no integer content or torsion-order factor is divided away. II.5.2 makes Δ(M) the corresponding polynomial of π1(M) and specifies exponent ε=2 in the closed case.

[Printed p.28](https://books.google.com/books?id=83ZJs9Z9BY0C&pg=PA28), II.5.2, identifies the b1=1 polynomial with pr(τ)(t−1)^ε and gives the closed symmetric relation (5.b). The normalization is the ordinary integral polynomial class required by the original claim. [Printed p.26](https://books.google.com/books?id=83ZJs9Z9BY0C&pg=PA26), II.4.6, provides the proof of the polynomial-part integrality used below; the theorem is not left dependent on the omitted boundary pages.

Let q:Z[H]→Z[t±1] send every element of T to 1. Apply the actual printed formula with its allowed unit ambiguity:

\[
q(\tau(M,e))=\varepsilon t^a
  \frac{\Delta_p(t)}{(t-1)^2},
\quad \varepsilon\in\{1,-1\},\ a\in\mathbb Z.
\]

Because q(Σ_T)=|T|=p^3 and (t−1)(t^{-1}−1)=−(t−1)^2/t,

\[
q(B_e)=\frac{\varepsilon t^a\Delta_p(t)-p^3t^{k+1}}{(t-1)^2}.
\]

II.3.2(i) makes this an integral Laurent polynomial. A Laurent numerator is divisible by (t−1)^2 only if its value and formal derivative at t=1 vanish; multiplying by any Laurent unit leaves this criterion unchanged. Since Δ_p(1)=p^3≠0 and Δ'_p(1)=0, these two equations give ε=1 and a=k+1. Consequently

\[
q(B_e)=t^k\frac{t\Delta_p(t)-p^3t}{(t-1)^2}=t^k.
\]

Thus aug(B_e)=aug(q(B_e))=1, contradicting p|aug(B_e). This excludes the entire original all-prime family with the verified source bridge. It does not choose a self-dual Euler structure, assume a preferred torsion sign, discard the finite group, or substitute the singular torsion for the polynomial part. Its monomial/unit ambiguity never removes the contradiction. Formula (5.b) itself uses a symmetric representative with value −|T| at 1; the exact original candidate uses +|T|. They are related by the allowed sign and monomial, which the pole-cancellation equations handle explicitly.

The local `verify_algebra.py` uses only exact integer Laurent arithmetic. It records the universal identity t[t+(N−2)+t^−1]−Nt=(t−1)^2 and universal pole equations; reproduces 25 primes and 21 integer Euler shifts per prime; and rejects wrong signs and adjacent wrong shifts. It certifies algebraic reproducibility, not topology or source interpretation.

## Relation to the original general rank obstruction

For an arbitrary finite T with invariant factors d_2,...,d_n satisfying d_(i+1)|d_i, let r_p count those divisible by p. Under q followed by reduction mod p, J_d maps to (t−1) if p|d and to the entire Laurent ring otherwise. If r_p≥3, exactly r_p−2 factors in II.3.3's product (indices i≥4) contribute (t−1). Hence q(B_e) mod p is divisible by (t−1)^(r_p−2). The projected singular correction multiplied by (t−1)^2 is proportional to |T| and vanishes mod p. The verified projection formula therefore gives

\[
\operatorname{ord}_{t=1}(\Delta_M\bmod p)\ge r_p.
\]

For r_p=1, the usual Δ_M(1)=±|T| already gives one root; for r_p=2, the even-exponent reciprocity permits an integral symmetric normalization with derivative zero at 1 and gives the double root. The zero reduced polynomial has infinite order. Thus the original general necessary condition is a direct consequence of the book's II.3.3 plus the standard rank-one Alexander conditions. This is a deduction made in this audit, not a claim that the book states the condition in the original determinant language.

## Separate mod-prime theorem and prime-2 failure

[Printed pp.45–46](https://books.google.com/books?id=83ZJs9Z9BY0C&pg=PA45), III.4.2–III.4.3, define τ(M,e;r) in the b1=1 case as the reduction of B_e. They require H/r to be free of rank b≥3 over Z/r. When r is a power of 2 they additionally require H/2r to be free of that same rank over Z/(2r).

For odd p and r=p, H_p/p=Fp^4 and b=4 is even. III.4.3 therefore gives B_e mod p in I^2. After q its augmentation vanishes (indeed it is divisible by (t−1)^2), contradicting the forced monomial above.

For p=2 and r=2, H_2/4=Z/4⊕(Z/2)^3 has cardinality 32, whereas a free rank-four Z/4 module has cardinality 256. It is not free. Applying III.4.3 to this pair would be invalid. II.3.3 and II.3.4 still apply and supply the prime-2 obstruction independently. Their use is essential to an all-prime conclusion from these pages.

## Realization pages do not override the obstruction

[Printed p.114](https://books.google.com/books?id=83ZJs9Z9BY0C&pg=PA114), VIII.5.1, formulates refined-torsion realization with H prescribed and refers to necessary conditions from Chapters I–III. It describes a general realization problem, not a solution that realizes every ordinary (H,Δ) pair satisfying only symmetry and augmentation.

[Printed p.118](https://books.google.com/books?id=83ZJs9Z9BY0C&pg=PA118), VIII.5.4, realizes a symmetric integral Laurent polynomial with nonzero value at 1 by a b1=1 manifold. Its proof explicitly takes H1=Z⊕Z/n with n=|Δ(1)|. For the exact original polynomial n=p^3, this is Z⊕Z/p^3, not Z⊕(Z/p)^3. The theorem concerns existence for the polynomial with cyclic torsion and supplies no realization of the noncyclic prescribed group. The full VIII.5.2 proof on pp.115–117 was omitted by the publisher preview; it is not used for our exclusion.

## Historical meaning and exact outstanding gap

Three claims must remain distinct: (i) a published necessary theorem, (ii) this exact counterexample family as its direct corollary, and (iii) an express earlier publication refuting Conjecture 12.26. The inspected pages establish (i); the fully verified source-to-algebra bridge establishes (ii). They do not expressly mention Conjecture 12.26 or this family. Establishing (iii), precise within-2002 chronology, earliest priority, and novelty of an alternate proof would need further positive source evidence. Failed searches do not establish any of those claims.

There is no remaining source/normalization gap in this exclusion. The remaining historical gap is positive evidence for an express earlier Conjecture 12.26 refutation and the relevant chronology. Only ten specific primary pages were inspected; no whole-book or earliest-source claim is made. The old theorem and its direct consequence block claiming the obstruction or this family as a newly discovered mathematical result on the present record. A different presentation or independently developed proof does not by itself establish publication novelty. Priority clearance and publication clearance remain false.
