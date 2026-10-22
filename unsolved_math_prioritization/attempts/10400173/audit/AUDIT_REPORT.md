# Independent adversarial audit: rank 637 / AMR-103-0173

## Verdict

**PASS WITH NONBLOCKING CORRECTIONS.** The proposed whole-record status `unsolved`, with five approach families, is supported. The literal unrestricted lens-space subproblem has the stated A6 even-category values **1 and 0**. No mathematical counterexample to that calculation, its subfactor realization, its normalization, or the Funar obstruction was found.

This audit does **not** certify novelty, solve the broad optimal-classification clause, or decide what extra restrictions the historical authors may have intended. It supplies an independent exact certificate and a material historical source update. Originals were preserved. No repository, remote, public comment, or external message was changed.

## Frozen inputs and replay

The reviewed author manifest is SHA-256 `3327ea967f634bb8b57bba52dc46c29ffeaaec98ceeabf8fcaaba12d76cb2d60`; the reviewed research note is `043b210954b19fdbe23b5377f0b2d79c9c46bea53de4a0e055ca5f7922140eb3`.

- All 11 manifest-bound author files match their lengths and hashes.
- The author's 283 explicit checks pass under both ordinary Python and `python3 -O`. Each output is byte-for-byte equal to `CONTROL_RESULTS.json`.
- All 10 existing scholarly PDF metadata entries match the privately held bytes. The selected private catalogue record matches ID 10400173 / AMR-103-0173; its statement SHA-256 is `9b6f12ee44ded2b844dc99145b66861788f075499f0274bc8e9f4278cddf412b`, as claimed. The full corpus hash and live repository/duplicate-search history were not independently replayed in this mathematical audit.
- The original author ZIP is 20,850 bytes, SHA-256 `30c15b4c945b8e9a51f668bb900812e921c62b632247c0754e4b5b663be1280b`. It contains exactly the 12 expected author entries, each byte-identical to the frozen packet. No source PDF, extraction, raw corpus, or private coordination file occurs there.
- A separate implementation passes 81 explicit exact runtime checks in ordinary and optimized Python. It does not import, parse, execute, or copy the author's arithmetic implementation. Counts include repeated specialization consistency checks; they are not advertised as 81 independent mathematical theorems.

An initial timing wrapper failed because `/usr/bin/time` was absent; no verifier ran in that attempt. The direct ordinary and optimized commands were then run successfully. This was an audit-environment issue, not a failure of the packet.

## 1. Realizability and categorical assumptions

Kawahigashi, Example 4.1, explicitly identifies both even bimodule fusion categories of the Jones A_n subfactor with the even part of SU(2)_{n-1}. Specializing n=6 therefore gives the required finite-index finite-depth subfactor; the calculation is not merely a candidate modular datum. [Primary source](https://arxiv.org/abs/2111.14332).

Bischoff's actual source location is **Section 3.2, Example 3.6**, for the SU(2)_k dimensions and twists, followed by Proposition 3.7 for the subfactor construction. The packet's repeated reference to Section 3.3 is wrong but does not affect the facts. At k=5 and labels 0,2,4 the twists are 1, exp(4 pi i/7), exp(12 pi i/7), exactly as used. [Primary source](https://arxiv.org/abs/1506.02606).

The even labels are fusion closed. The inherited braiding is nondegenerate: the exact normalized S matrix squares to the identity, and the independently reconstructed Hopf pairing below has H^2=Dim(C) I. The category is unitary with positive simple dimensions in the physical embedding. Neither a degenerate premodular category nor a nonspherical pivotal structure is being substituted.

Turaev-Virelizier Theorem 11.1 identifies the spherical state sum with RT of the center; the introduction specializes this to the product of a modular category's RT value and its reversed-orientation value. In the unitary case this is the absolute square. Its theorem hypotheses hold here. [Primary source](https://arxiv.org/abs/1006.3501).

## 2. Independent exact calculation without sqrt(7)

Write w=exp(2 pi i/7), x=1+w+w^{-1}, y=1+w+w^{-1}+w^2+w^{-2}, and Delta=1+x^2+y^2. These are the positive dimensions 1,x,y and global dimension of the even category in the chosen complex embedding. The supplied fusion rules and twists theta=(1,w^2,w^6), through ribbon balancing, give the unnormalized Hopf pairing

    H = [[1,x,y],[x,-y,1],[y,1,-x]].

The independent verifier constructs H from the fusion coefficients, rather than taking a sine S matrix as input. It uses integer cyclic convolution modulo w^7=1, then reduces with 1+w+...+w^6=0. Irreducibility follows from the Eisenstein criterion applied to Phi_7(X+1). Equality of its six integer coefficients is exact; no numerical zero tolerance is used.

For a negative continued fraction [a1,...,an], let

    A = (H T^a1 H ... T^an H)_{00}.

The TV value is A conjugate(A)/Delta^(n+1), because S=H/sqrt(Delta), while the RT framing correction has unit modulus. The independent finite-color sum proves

    A([7]) = Delta,
    A([4,2]) = 0.

Thus the target TV values are exactly 1 and 0. The same program verifies all six coprime q values at p=7, opposite braiding, a continued-fraction blowup, fusion-dimension identities, H^2, the Gauss-sum norm, and the S3 and S2 x S1 normalizations. The denominator is nonzero because Delta is a sum of positive dimension squares; exact coefficient arithmetic also verifies Delta != 0.

Sato-Wakui's PDF p. 28 gives precisely the negative-continued-fraction surgery formula used. In particular 7/2=[4,2]. A separate integral SL(2,Z) check gives ST^7S=[[-1,0],[7,-1]] and ST^4ST^2S=[[-2,1],[7,-4]], so there is no accidental substitution of L(2,7). Swapping the standard inverse-q convention or orientation only permutes the checked q orbits {1,6} and {2,3,4,5}; the target distinction survives. [Primary source](https://arxiv.org/abs/math/0208242).

## 3. New historical source: Sokolov 1997 is now inspected

The author packet honestly stated that Sokolov's full text had not been obtained at its freeze. During this audit an ordinary request to the official MathNet full-text endpoint succeeded. The three-page original was rendered and visually read because its text extraction is corrupt. It remains private; this audit distributes only the title, public URL, hash, size, and authored mathematical analysis.

Sokolov's **Proposition 2, printed p. 469**, already distinguishes L(p,1) from L(p,q) when q is neither 1 nor p-1, using r=p. His displayed formula (*) on printed p. 468 gives, at p=r=7, d=gcd(7,14)=7 and c=2pr/d^2=2:

    TV_{7,1}(L(7,1)) = 1/2,
    TV_{7,1}(L(7,2)) = 0.

[Official primary PDF](https://www.mathnet.ru/php/getFT.phtml?jrnid=mzm&paperid=1525&what=fullt). [Bibliographic record](https://www.mathnet.ru/eng/mzm1525).

These values concern the full SU(2)_5 theory, not the rank-three even category. There is no factor-of-two error in the A6 result. The full category splits into the even sector and the rank-two semion sector generated by label 5, whose twist is i. On both target lens spaces the semion TV value is 1/2: its unnormalized surgery numerators are 1-i for [7] and 2 for [4,2], with squared denominators 4 and 8. Multiplying gives precisely Sokolov's 1/2 and 0. The independent controls check this normalization consistency.

A further inspected scholarly corroboration is Bärenz-Barrett, Section 1.1, PDF p. 2, which explicitly attributes this lens-space separation to Sokolov Proposition 2. It is corroboration, not a replacement for the now-inspected original. [Primary research paper](https://arxiv.org/abs/1601.03580).

Wakui's 2007 introduction nevertheless explicitly described the subfactor question as open. Its p. 10 generalized-E6 table really gives the same complex value (11-i sqrt(11))/22 on both lens spaces; the rendered table was rechecked. The original Ohtsuki p. 513 also motivates exotic subfactors, but its separately numbered Problem 9.9 has no express exotic-only restriction. These historical statements should be retained without inventing an explanation for the discrepancy. The new primary evidence strengthens the prohibition on novelty or whole-problem-resolution claims; it does not change the literal A6 computation. [Wakui source](https://www2.itc.kansai-u.ac.jp/~wakui/ILDT07wa.pdf).

## 4. Other approach families

**Finite groups.** The homotopy argument is valid for all finite-group 3-cocycle state sums: an oriented homotopy equivalence reindexes classifying maps and preserves evaluation on the fundamental class. Here 2 is a square mod 7, whereas it is outside the homeomorphism orbit of q=1. The independent order-14 calculation uses integer carries and residues mod 7, rather than the author's Fraction phases, and reproduces the equality for all 14 cocycle powers. The tempting contrary online computation must not be promoted to a theorem.

**Funar.** The visual theorem statement on printed p. 2291 contains the condition **-v** is a nonzero quadratic residue mod q. The packet has it right; some extracted text loses the minus sign. For k=1,q=5,v=4, all conditions are satisfied, and the published matrix formulas give exactly A=[[1,25],[4,101]], B=[[1,1],[100,101]]. They have determinant 1 and trace 102. The theorem supplies nonisomorphic fundamental groups and equality for every spherical fusion category. Since finite-depth subfactor even categories are unitary spherical fusion categories, the obstruction applies to all of them simultaneously. The author's moduli 2..100 conjugacy checks are correctly labelled finite sanity checks, not the proof of universal congruence or integral nonconjugacy. [Primary theorem](https://msp.org/gt/2013/17-4/gt-v17-n4-p09-s.pdf).

**Morita equivalence and products.** Turaev-Virelizier defines the equivalence used immediately before Corollary 11.5 by braided-equivalent centers and explicitly includes weak Morita equivalence. The packet's citation is therefore adequate in its unitary setting. Finite Deligne-product state sums factor, and common collisions persist. Its caution that multiplication can erase a distinction when another factor vanishes is correct.

**Target boundary.** Visual inspection of Ohtsuki p. 513 confirms that strong amenability introduces separately numbered Problem 9.10. It must not be appended to Problem 9.9's requirements. Conversely, the undefined strongest-possible-classification request is genuinely left unanswered. Funar rules out complete separation in the finite-depth setting, but does not select an optimal partial classification or define the missing criterion. [Original problem page](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf).

## 5. Corrections and packaging hardening

1. Correct Bischoff Section 3.3 to **Section 3.2, Example 3.6, and Proposition 3.7** wherever it occurs in a future revised release.
2. Add the now-inspected Sokolov original and its historical separation result in an addendum or a newly frozen version. Do not silently alter the author's earlier retrieval history. Preserve the 2007 open-status tension and the no-novelty statement.
3. The original `verify_manifest.py` ignores unexpected directories because its inventory filters `is_file()`. A synthetic copied packet with an extra directory and harmless sentinel was accepted. This does not contaminate the actual frozen packet or archive, both of which were inspected and are clean. It does weaken the advertised closed allowlist for later builds. The supplied `hardened_author_manifest.py` rejects directories, symlinks, unexpected entries, and altered frozen hashes. Its negative-control rejection is recorded.

All corrections are nonblocking for the frozen mathematical conclusions. Apply the packaging hardening before relying on the verifier as a future no-source-redistribution gate. The audit bundle itself uses a strict flat allowlist and contains no inspected source bytes or private source paths.
