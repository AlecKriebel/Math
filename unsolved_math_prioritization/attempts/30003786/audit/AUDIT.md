# Independent adversarial audit: 30003786 / OWR-16160-016

Date: 2026-10-03 UTC. Reviewer: a fresh reviewer not involved in the author construction.

## Verdict

**PASS for the complete mathematical counterexample to the literal, unrestricted abstract-embedding question.** No mathematical repair is required. The frozen proof supplies the infinite argument; neither the author's finite tests nor the auditor's tests substitute for it.

**HOLD for any claim of a newly resolved open problem, first negative answer, or historical priority.** Such claims are absent from the candidate, correctly. In fact, Appendix B below verifies a transfer from Kucharczyk's 2014 preprint / 2015 published rigidity theorem to a negative answer to the same literal embedding-independence question. This is a documented prior-theorem implication, not a claim that the paper explicitly states the SL7 construction or discusses the 2018 question. The packet's cautious statement that this transfer had not been checked can now be updated.

The accepted result is an explicit elementary certificate and classical synthesis. Publication, repository changes, and catalogue status changes are outside this audit.

## 1. Frozen object and independence

Reviewed the exact files under `public/`. All six entries in `MANIFEST.sha256` verified. In particular:

- `ATTEMPT_1.md`: `bc5f2f6db65d2ee5455904f0f3a852e42ad5621b6a2b36af4520e84edee6aa94`
- The author verifier was run unchanged, with byte-identical output.
- The independent verifier does not import the author verifier. It uses a separate generic matrix engine, a constructive kernel-word formula, exact relation-vector tests, and actual 7-by-7 matrices.
- No frozen author file was edited. No remote writes were performed. No further author search or new author attempt was undertaken.

The catalogue and Alec-repository search claims were not comprehensively repeated. They are provenance claims, not dependencies of the mathematical certificate. The original question and the relevant older theorem were independently read in their primary sources.

## 2. Source scope: PASS

The original report is [Oberwolfach Report 19/2018](https://ems.press/content/serial-article-files/46739), Alain Valette, “Diameters in box spaces,” printed pp.1150–1151. The precise question is on printed p.1151, PDF page 35 (zero-based 34). The preceding context concerns finitely generated residually finite groups. The target paragraph defines congruence by intersection with an ambient congruence subgroup of SL_N(Z), then asks whether the notion depends on the embedding.

There is no condition in that paragraph requiring an algebraic extension, an irreducible representation, a connected common Zariski closure, or Zariski density in the full ambient SL_N. The two SL7 representations meet the literal hypotheses, including a common coefficient ring and dimension. The report identifies the workshop as April 15–21, 2018; the 2018 attribution is correct.

The equivalence between the intersection definition and containing a principal kernel is valid: if K_rho(m) is contained in H, the full inverse image in SL_N(Z) of red_m(rho(H)) is an ambient congruence subgroup whose pullback is exactly H. This uses only that H is a subgroup and rho is injective.

## 3. Line-by-line mathematical audit

### Freeness and the character: PASS

The two disjoint ping-pong sets are nonempty and the displayed inequalities are strict, including for negative powers. For finite |x|>1, the B denominator cannot vanish and |2sx+1|>|x|. Infinity maps to 1/(2s), inside the other set. A mixed reduced word with opposite end types is conjugated to one with equal end types by the stated choice of exponent; both new end exponents are nonzero. Pure nonzero powers are nonidentity. This proves freeness rather than merely testing it. Hence assigning chi(A)=1 and chi(B)=0 defines a surjection to C5, with index-five normal kernel.

### Elementary generation over every odd residue ring: PASS

For each prime dividing n, the first column of a determinant-one matrix is not zero. Choosing t to avoid one forbidden residue when necessary, and applying CRT, makes a+tc a unit even when n is composite or has repeated prime factors. After the first row operation, the displayed lower and upper operations yield diag(u,u^-1): the upper-right entry b is explicitly the current one, so the parameter -bu is correct. The identity w(u)w(-1)=diag(u,u^-1) has the correct signs. Every U(t), L(t) is a power of U(1), L(1). The n=1 case is handled separately.

### No C5 quotient at odd level: PASS

The diagonal D exists precisely because n is odd. Conjugacy forces f(U)=4f(U), so 3f(U)=0; multiplication by 3 is invertible in C5. The stated J conjugates U(-1) to L(1). Generation kills all of f. The argument includes n divisible by 5, powers of 5, n=3, and mixed odd composites; it is not a coprime-order shortcut.

### Exact separation of even and odd factors: PASS

For m=2^k n, A^(2^k) and B^(2^k) have trivial 2-primary component and odd unipotent parameters 2^(k+1). These parameters are invertible modulo n. Thus the image contains the whole odd factor alone, not just a surjection onto it. Removing that component from an arbitrary lift of h gives (h,1), proving the direct-product equality. This addresses the genuine potential subdirect-product gap. Cases k=0 and n=1 are valid.

The kernel of reduction from level 2^k to level 2 has the stated congruence filtration. The map I+2^jX to X modulo 2 is a group homomorphism into an additive 2-group with the next filtration term as kernel. Iterating proves it is a 2-group, and therefore so is H_k. The k=1 factor is trivial. Neither factor of the direct product admits a C5 quotient, hence neither does the image at any m.

### The noncongruence inference: PASS

If K(m) were contained in ker(chi), chi would factor through the actual image red_m(G), with the same nonzero value at A. This contradicts the previous conclusion. The statement is quantified over every positive m, including m=1. There is no reliance on finite sampling.

### Faithfulness and the principal level-2 equality: PASS

A 5-cycle has determinant +1, order 5, and distinct 0–1 matrix powers modulo 2. Both block embeddings are integral determinant-one homomorphisms and are faithful on their first block. Every original 2-by-2 group element is I modulo 2. Thus the second block alone detects chi at level 2, giving K_rho1(2)=ker(chi), with both implications checked. Padding does not change K_rho0(m). The congruence families consequently differ.

### Scope distinction: PASS

The finite cyclic character need not extend to an algebraic morphism on the connected SL2 closure. Results about algebraic embeddings of a fixed algebraic group therefore do not disprove this example. No strengthening of the original question should be silently inserted to exclude the block construction.

## 4. Independent exact controls

Run `python3 independent_controls.py > independent_results.json` from the audit directory. The checked-in output reports PASS on 25,051 exact assertions: 10,005 constructed witness levels, 52 full image-relation tests, 1,365 explicit block-word checks, and 64 independently checked supplied witnesses.

Controls include:

1. Unchanged author replay, byte-identical to the supplied 15,667-assertion output.
2. Independent evaluation of all 64 supplied kernel witnesses over the integers, with determinant, reduction, and C5 label checked separately.
3. Constructive kernel words for every m=1,...,10000 and five large prime-power/mixed boundary cases, including moduli far beyond feasible finite-group enumeration. Appendix A proves the construction uniformly.
4. Exhaustive finite-image Cayley graphs at 52 moduli: 1,...,48 and 60,75,80,100. All non-tree edge exponent vectors are collected over F5; rank two is required. This independently rules out every homomorphism to C5, not just the proposed chi, at those finite levels.
5. Actual 7-by-7 block matrices and their products for every four-generator word of length at most 5, including unreduced words and inverse generators. Exact determinant and level-2 tests avoid replacing the representation with a symbolic label alone.

These checks are corroboration. Freeness, all-moduli separation, and the theorem itself are certified by the written mathematical arguments.

## Appendix A. Independently constructed noncongruence witnesses at every level

This short alternate derivation is an auditor control of the existing certificate, not an additional author attempt.

If 5 does not divide m, use g=A^m. It is I modulo m, while chi(g)=m modulo 5 is nonzero.

Otherwise write m=2^k n, n odd. Put h=2^k, choose t with 2ht=1 modulo n, and let r=ht. Set C=A^r, E=B^r. Both are I modulo h, and modulo n they equal U(1), L(1). Choose v=2^-1 modulo n and define

    D = C^2 E^(-v) C E C^(-1).

Modulo n this is w(2)w(-1)=diag(2,2^-1); modulo h it is I. Therefore

    g = D C D^(-1) C^(-4)

is I modulo both n and h, hence modulo m. Its character is -3r modulo 5. Since 5 divides n and 2r=1 modulo n, r is nonzero modulo 5, so chi(g) is nonzero. This gives an explicit finite expression for a witness at every modulus, including moduli divisible by 5, without any enumeration or assertion about the full image group.

## Appendix B. Verified prior-theorem transfer and attribution boundary

### B.1 The published theorem used

Kucharczyk's [primary manuscript, arXiv:1408.3024](https://arxiv.org/pdf/1408.3024), p.2 (PDF page 2), states the arithmetic-Fuchsian special case of Theorem A: an abstract isomorphism between arithmetic Fuchsian groups that preserves their congruence families in both directions is conjugation by an element of PGL2(R). The [arXiv record](https://arxiv.org/abs/1408.3024) dates the preprint to August 2014 and identifies publication in Acta Arithmetica 169 (2015), pp.77–100. The theorem's general form is on manuscript pp.3–4; the special case suffices here.

The rest of this appendix supplies the explicit transfer. It is a mathematical inference from that prior theorem, not a quotation or claim that the article presents this particular corollary.

### B.2 Identifying the required arithmetic lattice

Let Gamma(2)=ker(SL2(Z) to SL2(F2)), let q be projection to PSL2(R), and retain G=<A,B> from the certificate. Then

    Gamma(2) = <A,B,-I> = G union (-G),
    q(G) = q(Gamma(2)).

For completeness, the generation assertion follows by an even-step Euclidean algorithm. In a matrix of Gamma(2), the first-column entries a,c are coprime with a odd and c even. Left multiplication by A^r replaces a by a+2rc; if c is nonzero, choose r nearest -a/(2c), giving |a+2rc| <= |c|, with equality excluded by parity. Left multiplication by B^s similarly replaces c by c+2sa, and the same parity argument makes the inequality strict whenever needed. Alternating reduces the maximum absolute first-column entry until c=0. Then a=d=±1 and b is even, so the residual matrix is ±A^j. Reversing the row operations proves the claim.

Every g in G has diagonal entries 1 modulo 4 and off-diagonal entries even: this holds for A, B and their inverses and is preserved by multiplication. Thus -I is not in G, and q restricts to an isomorphism G to q(Gamma(2)). The latter is a finite-index subgroup of PSL2(Z), hence an arithmetic Fuchsian lattice. It fits the arithmetic special case with k=Q, B=M2(Q), and order M2(Z). Arithmetic groups admit the modular embedding required in the general theorem, but the stated special case already covers this situation.

### B.3 Matching the two congruence topologies

In the manuscript's definition, choose the order M2(Z). The principal projective congruence subgroup at n is q(Gamma(2)) intersected with q(Gamma(n)). Its pullback under q|_G is

    S(n) = {g in G : g = I or -I modulo n}.

The sign here is one common sign modulo n, exactly as arises from an integral lift; no larger set of arbitrary scalar square roots of 1 is being substituted.

Let K(n)={g in G:g=I modulo n}. We have K(n) contained in S(n). Conversely S(4n)=K(4n) is contained in K(n), because g=-I modulo 4n is impossible for an element with both diagonal entries 1 modulo 4. These inclusions show that the projective congruence family pulls back to precisely the integral family on G. This explicitly resolves the central-sign and small-prime issue rather than assuming it away.

### B.4 A nongeometric automorphism

Because G is freely generated by A,B, the Nielsen map

    f(A)=AB, f(B)=B

is an automorphism; its inverse sends A to AB^-1 and fixes B. It induces an automorphism of q(G). But tr^2(A)=4, whereas

    AB = [[5,2],[2,1]],    tr^2(AB)=36.

Conjugation in PGL2(R) preserves squared trace of PSL2 elements. Consequently this automorphism cannot be projective conjugation. By the contrapositive of the published theorem, it fails to preserve the projective congruence family. By B.3, f fails to preserve the integral congruence family of G as well.

Hence the faithful embeddings i:G to SL2(Z) and i composed with f induce different congruence-subgroup families on the same abstract group. If a common SL7 ambient group is desired, pad both with I5. This proves that the literal negative answer is already a consequence of the older theorem.

### B.5 What this establishes, and what it does not

Established: the broad negative answer follows from a theorem available in 2014 and published in 2015, with an explicit lattice, automorphism, and verified topology transfer. This materially strengthens the packet's “relevant prior literature” note.

Not established: that Kucharczyk stated the later Oberwolfach question, that the exact index-five finite-block example appeared earlier, that any particular mathematician knew the inference in 2018, or that an exhaustive novelty search has been performed. The SL7 construction gives a particularly elementary and explicit differing subgroup, whereas the prior-theorem transfer above obtains the existence of a differing subgroup by rigidity. Any first-resolution or novelty claim remains unsupported.

## 5. Repairs and permitted conclusion

- Required mathematical repairs: none.
- Attribution/documentation repair: update the packet's Kucharczyk entry from “transfer unverified” to a reference to the verified transfer above, if the packet is revised. Preserve the distinction between an explicit new write-up and a newly resolved open problem.
- Optional clarification: “literal unrestricted abstract-embedding formulation” should remain in summaries; do not state a result about all conceivable strengthened variants.
- Do not characterize this audit as human peer review or proof-assistant verification.

Approved mathematical conclusion: there is an explicit index-five subgroup of a free integral matrix group that is noncongruence for one faithful SL7(Z) embedding and principal level two for another. The proof is complete. Its broad negative conclusion is also implied by prior published rigidity theory.
