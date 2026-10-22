# Source-only mathematical review of PR1271 / problem30003042

**Verdict: the full target is false.** The n=8 case satisfies
\[
 e_8\in\Gamma^5K(X_{F(S)}),
\]
which is the opposite of the requested nonmembership. This follows from a later primary theorem and the transfer mechanism already given with the original conjecture. It is a literature-based falsification, not a novel discovery and not publication clearance for any submitted package.

## Scope and independence

This review began with only the supplied conjecture and primary-source pointers. I did not open `submitted/`, the PR body, candidate conclusions, or other review families. I retrieved primary sources independently. The isolated internal lambda adversary received the same target without candidate material; its initial obstruction analysis preceded my notification of the later Spin(18) source. No outside person was contacted. No branch, index, reference, commit, or push was changed. The repository was on `main` when checked. Only this review family was authored.

## Exact original object

The OWR statement is Karpenko's Conjecture 3, printed pp226–227, in DOI [10.4171/OWR/2016/5](https://ems.press/content/serial-article-files/46609). Its fuller version is Conjecture 4.7 in [a16i3](https://sites.ualberta.ca/~karpenko/publ/a16i3.pdf), printed p11.

Use the source's convention for nondegenerate forms, including characteristic two. The initial data are a field F, an integer n≥1, a nondegenerate form φ of dimension 2n+1, and X=OGr(n,φ). The extra hypothesis is
\[
 \operatorname{ind}C_0(\varphi)=2^n.
\]
Thus the even Clifford algebra has maximal index and is division. Let S be its ordinary Severi–Brauer variety and put k=F(S). The target for every n≥8 is
\[
 e_n\notin\Gamma^{d_n}K(X_k),\qquad
 d_n=n+1-\lfloor(n+1)/2\rfloor=\lceil(n+1)/2\rceil.
\]
Here e_n is the K-class corresponding to the smallest-dimensional special Schubert variety after splitting. Its existence as a K-class over k does not assert the existence of a geometric Schubert subvariety over k.

An equivalent even-dimensional setup uses a nondegenerate ψ of dimension 2n+2 with trivial discriminant and C⁺(ψ) division of degree 2^n; X is a component of its maximal Grassmannian. A nondegenerate odd-dimensional subform identifies the two X's and Clifford algebras. Over k=F(S), ψ has trivial Clifford invariant, hence Witt class in I_q³. The paper's use of “generic” here means this construction; it is broader than one particular standard versal-torsor construction. No identification of these genericity definitions is needed below.

## Later theorem and falsification

The relevant later primary source is Karpenko, [On isotropy fields of Spin(18)-torsors](https://sites.ualberta.ca/~karpenko/publ/spind18-04.pdf), dated 28 August 2023 (published as DOI [10.1090/spmj/1848](https://doi.org/10.1090/spmj/1848), St. Petersburg Math. J.36(2025),115–120; bibliographic metadata checked separately). Its Theorem 4.1 and Corollary 4.4 give critical index exponent 3 for dimension17 and exponents i₄=i₅=3 for dimension18. The paper explicitly extends the consequence to **every** 18-dimensional nondegenerate form with trivial discriminant and Clifford invariant: it gains Witt index at least5 over some finite extension of degree not divisible by16. The universal formulation applies to ψ_k above.

Here is the specialized transfer argument, independently checked against the original implication on a16i3 p11 / a16i5 p12. Let n=8, dimψ=18, and Y be the associated 16-dimensional quadric over k. Write T for the topological filtration. Let ℓ_j denote the K-class of a j-plane after splitting, with its canonical K-theoretic lift, and h the hyperplane-section class. These symbols need not represent actual k-linear subspaces. The later theorem supplies a finite L/k of degree N with v₂(N)≤3 and a 3-plane on Y_L. Transfer gives
\[
 N\ell_3\in T^{13}K(Y).
\]
A splitting extension of 2-power degree gives a second transferred multiple of ℓ₃. Integer Bézout, followed by multiplication by a power of2, therefore gives
\[
 8\ell_3\in T^{13}K(Y).
\]
The quadric K-identity used in the original proof is
\[
 8\ell_3=\ell_0+h^{15}+2h^{14}+4h^{13}.
\]
All three h-terms are in T¹³, so ℓ₀∈T¹³. For the incidence variety Z with projections g:Z→Y and f:Z→X_k, the source's identity is e₈=f_*g^*(ℓ₀). Pullback preserves the filtration, while f is a projective bundle of relative dimension8, so
\[
 e_8\in T^{13-8}K(X_k)=T^5K(X_k).
\]
The original Theorem 4.3 identifies this last filtration with Γ over k. Consequently e₈∈Γ⁵. Since d₈=5, the universal conjecture is refuted at its first index.

The existence of the power-of-two splitting extension can, for the counterexample alone, be taken in characteristic zero by adjoining square roots to a diagonal form. The cited later theorem itself has arbitrary-characteristic scope. A single allowed characteristic-zero instance already defeats the all-fields claim.

## What was independently computed, and what remains a dependency

The later proof replaces the earlier computer-assisted index determination with a short mod2 argument. I independently checked its finite algebraic witness using [CHECK_MOD2.py](CHECK_MOD2.py), by both multiplying all sixteen linear factors and using an additive-polynomial recurrence. Both give 150 monomials over F₂. In
\[
 \prod_{I\subset\{5,6,7,8\}}(x+\sum_{i\in I}x_i),
\]
the coefficient of x⁸x₇⁴x₈⁴ is1. Under the stated flag-Chow basis, it yields the nonzero term x₇⁴x₈⁴e₈. The result is recorded in [CHECK_RESULTS.json](CHECK_RESULTS.json).

This check does not independently reprove all geometric inputs. The bridge from this polynomial obstruction to the index is the published Proposition 3.2, relying on the author's earlier description of the rational Chow image. The transfer identities, Clifford K-theory, and equality Γ=T are also published dependencies, not new first-principles reconstructions here. I read the complete later seven-page argument and the critical original pages; I do not certify every referenced theorem or an unread page.

## Distinct approach families and boundary checks

| Family | Mechanism | Status / exact gap |
|---|---|---|
| Geometric falsification | Later universal isotropy bound, transfer on the quadric, incidence pushforward | Succeeds at n=8, using the published inputs stated above. |
| Intrinsic lambda-ring / integral lattice | Transport Γ through the splitting K-isomorphism and test membership in the weighted-Chern lattice | Valid framework, but a codimension argument does not establish nonmembership. The internal adversary independently confirmed this before the later-source notification. |
| Chow-only divisibility | Use the split Chow presentation and rational-cycle subring | Does not prove the target. The original paper itself shows the anticipated Chow obstruction fails in dimension18. A Chow subring computation cannot silently replace a K/gamma computation. |

The June2016 final preprint [a16i5](https://sites.ualberta.ca/~karpenko/publ/a16i5.pdf), printed p11, explicitly clarifies that scalar extension transports Γ but does not make the topological filtration strict; Γ and T on the split variety need not coincide. Thus the geometric codimension8 of e₈ after splitting is consistent with e₈∈Γ⁵. The original observation e₈∈Γ⁴ gives a lower membership and does not contradict the stronger membership now obtained.

The strongest conclusion certified here is the falsity of the full universal target, with e₈∈Γ⁵ justified through the later theorem. This review does not determine the exact gamma depth of e₈, the status of each n≥9, or the validity of any submitted manuscript. A proof of the original all-n nonmembership statement cannot be supplied without contradicting these primary results.

## Custody and chronology

Raw PDFs, extracted text, rendered pages, HTML, and scratch are confined to ignored `_local/`; source bodies are not authored deliverables. `SOURCE_LEDGER.json` records the pages actually read and visualized. Absolute source/input paths occur only in receipt files and are not authored-manifest membership. Inputs were hashed after retrieval/reading, then reauthenticated at the seal; this authenticates that final interval, not an unrecorded earlier freeze.

The log corrects an avoidable timestamp error: some early progress messages used inferred future UTC labels. Their events are bounded by actual clock readings 00:38:08 and 00:40:48 UTC on 2026-10-18; exact intermediate times are unknown. No mathematical observation was backdated, and event order is retained. The seal uses an actual UTC clock. No candidate material was requested or received before this report was written.
