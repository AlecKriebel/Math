# PR344 independent Honda/lifting audit

Prepared 2026-10-04T03:48:29Z. Candidate head: 86a758b1cc9c94322ce6afc3d17150fa2c90327a. Family: actual finite flat p-torsion realization over W(k), finite Honda conditions, and exact qss elliptic quotients. No historical audit or other-agent conclusion has been read.

## Verdict and precise scope

**PASS for this family.** The candidate supplies a valid p-killed finite Honda system over W(k), for k = algebraic closure of F_p and p > 3. The resulting actual finite flat commutative group has the submitted Dieudonne special fiber. That special fiber has a complete qss filtration with actual supersingular elliptic p-torsion factors, in the original source's sense. Direct sums yield the same conclusion for every n >= 3. No realization, unramified-lifting, elliptic-factor, or rank gap was found.

This verdict addresses the candidate's construction and its cited realization dependencies. The source asks about the special-fiber-qss hypothesis, not the stronger hypothesis of a qss filtration over W. The candidate correctly makes the former assertion only. It supplies unpolarized finite flat groups, not Jacobians, and says nothing contrary to the Coleman conjecture. Priority or novelty has not been certified in this family.

The complete original-source reading was frozen before candidate exposure in SOURCE_ONLY_EXPOSURE_GATE.md. Candidate exposure began 2026-10-04T03:42:57.869448+00:00. FIRST_CANDIDATE_ASSESSMENT.md was frozen before primary-classification retrieval or historical conclusions. Neither frozen file has been revised.

## Primary theorem checks

The official [Hoshi revised manuscript](https://www.kurims.kyoto-u.ac.jp/~yuichiro/rims1911revised.pdf), March 2021, was retrieved directly and pinned to SHA-256 a1ffb3c977e0601da08437823124c5ef2aa3958d808de1e28e4ced8b0eddde22, 129352 bytes. Visually inspected printed pages 5-9, 12-13. Dependency locators: Definitions 2.1-2.4; Proposition 2.5; Definitions 3.4-3.7; Remark 3.5.1; Proposition 3.11(2),(5); Definition 4.8(ii); Lemma 4.9. These give the semilinear convention, contravariant equivalence, duality, Honda splitting, lifting, reduction, and superspecial criterion used below. Lemma 4.9 applies to deformable objects; this hypothesis is checked for each two-dimensional factor.

The independently retrieved [Fontaine-Laffaille paper](https://www.numdam.org/item/ASENS_1982_4_15_4_547_0.pdf), Ann. Sci. ENS 15 (1982), was pinned to SHA-256 c049a7bff113a45f8bbcffc93118bd2e651e84f8b4a38305f7cb24b34c2011a2. Visually inspected printed 600-603. Section 9 sets e=1, A=W(k); sections 9.1-9.5 confirm the same module relations, Honda axioms, and p != 2 equivalence. In particular the original axiom FM intersect L = pL is met explicitly, not omitted. The classical classification is used as a sourced theorem, not re-proved here; its foundations are not a novel claim of this candidate.

The complete applicable axioms are mathematically displayed in the next section, with their checkable values. No separate Fontaine-Laffaille claim of arbitrary liftability is required. The elementary datum has all the demanded conditions.

## Finite flat realization and unramified lift

Write e0,...,e5 for the candidate's basis. F is sigma-semilinear; V is sigma inverse-semilinear. Since coefficients are in F_p, they are fixed by sigma and its inverse. W acts on M through W/pW = k, so M is a W-module of finite length six with pM=0. Witt Frobenius and its inverse descend to the displayed semilinear operations because k is perfect.

Direct evaluation gives:

\[
FM=\langle e1,e2,e4\rangle=\ker V,\qquad
VM=\langle e2,e4,e5\rangle=\ker F.
\]

Every nonzero F image is killed by V, and every nonzero V image is killed by F. Hence FV=VF=0=p on M. This also verifies the exactness required for a deformable object. With L=span(e0,e3,e5), the Honda checks are:

| Required condition | Explicit evidence |
| --- | --- |
| L is a W-submodule | k-subspace, with W acting through its reduction to k |
| FM intersect L = pL | Both are zero: the basis coordinate sets are disjoint, and pL=0 |
| L/pL -> M/FM is an isomorphism | L is a direct complement of FM; both spaces have dimension three |
| V restricted to L is injective | V(e0)=e5, V(e3)=e2, V(e5)=e4; these are independent, and sigma inverse is bijective |
| finite module and F,V relations | length six, pM=0, semilinearity and FV=VF=p checked above |

The image of L is the image of the k-linear section s of M -> M/FM, given by choosing the unique representative in L. Thus the actual datum is (D,s) in Hoshi's category; L is not just an informal label for a possible lift. Since p>3 implies p!=2, Proposition 3.11(2) produces a p-torsion finite flat commutative group scheme over W(k). Proposition 3.11(5) identifies its special-fiber module with D. The base is exactly the complete unramified Witt ring; no ramified extension or enlargement of the base enters.

This establishes existence via an explicit classification datum. Writing a Hopf algebra is not needed for the existence proof under the accepted equivalence. A classification theorem with unverified hypotheses would not suffice; all relevant hypotheses here have been checked.

## Qss filtration and elliptic identification

In the submitted order (u,v,w,z,a,b), the inverse basis formulas are integral, with no division:

\[
e0=a,\ e1=b,\ e2=z,\ e3=w-2b,\ e4=v-z,\ e5=u-w+b.
\]

The change of basis has determinant one over the integers. Consequently it is valid over every field of the allowed characteristic. Evaluating F,V gives F(u)=V(u)=v, F(w)=v+z, V(w)=z, F(a)=b, F(b)=z, V(a)=u-w+b, with other images zero. Therefore

\[
0=M_0\subset M_1=\langle u,v\rangle\subset
M_2=\langle u,v,w,z\rangle\subset M_3=M
\]

is stable. On M1, M2/M1, and M/M2 the pairs (u,v), (w,z), and (a,b) respectively satisfy F(x)=V(x)=y and F(y)=V(y)=0. Each factor has imF=imV=kerF=kerV=span(y), so it is deformable. Applying the superspecial criterion to this actual factor, over algebraically closed k, identifies it as a product of supersingular elliptic p-torsion groups; its two-dimensional module makes this a single elliptic factor. Equivalently, the rank-two case in the proof of Lemma 4.9 identifies this standard pair directly. The algebraic closure is essential to avoid an unsupported assertion about all perfect-field forms.

Contravariance sends the surjection M -> M/M_(3-i) to a subgroup H_i of H. For i=1,2,3 it gives:

| Group object | Module |
| --- | --- |
| H1 | M/M2 |
| H2 | M/M1 |
| H3=H | M |
| H1/H0 | M/M2 |
| H2/H1 | M2/M1 |
| H3/H2 | M1 |

The module category and the finite group-scheme category over the field are abelian, so the anti-equivalence reverses their exact sequences. This table checks the actual group subquotients, rather than merely listing three plausible modules. All three are E_i[p]. Hence H is qss under Takao Definition 1(3). Their ranks are p^2, so exact-sequence multiplicativity gives rank(H)=p^6. Finite-flat rank is constant over the connected local base Spec W(k), giving the same rank upstairs; this independently avoids relying on an unstated rank formula in the terse classification proposition.

No restriction of L to this flag has been claimed to realize a flag over W. Such a claim would require additional checks, as the original Proposition 1 warns. It is unnecessary to the exact source target.

## All n >= 3 and duality bridge

Append n-3 independent copies I_j of the standard two-dimensional elliptic module, and append span(x_j) to L. F and V preserve each summand. FM_n is the old FM plus the new y_j lines; L_n is its complementary span of e0,e3,e5 and the x_j. V(L_n) has the independent basis e5,e2,e4 and y_j. All Honda conditions therefore hold blockwise, for arbitrary n. Extend the module flag by M, M+I1,...,M+I1+...+I_(n-3); exact reversal gives a group qss flag with n elliptic factors, hence rank p^(2n).

For completeness, the candidate's obstruction is compatible with the primary duality convention: F^2(M)=span(e2), V^2(M)=span(e4), whereas the dual second images both equal span(e0*). Their intersection dimensions differ. Standard I_j summands have zero second images and preserve this difference. The candidate's independent invariant/semilinear families may assess that obstruction in greater depth; their conclusions have not been consulted here.

Once the special fiber is nonselfdual, no lift can be selfdual: an isomorphism over W with the Cartier dual specializes to one over k, since Cartier duality commutes with base change. This bridge needs neither an alternating pairing nor any principal polarization.

## Reproducibility and adversarial controls

check_realization.py is independent standard-library code, not imported or copied from the submitted checker. It uses rational exact basis solving and sparse basis maps. Execution 009 verified determinant one, all three factor matrices, Honda complements/injection and direct sums for n=3,4,7,12, and split elliptic controls n=0,1,2. It rejected a Honda subspace containing e1, the zero-operator nondeformable module, and the unstable span(e0,e1) flag. Its F_125 model uses t^3+t+1, which has no F_5 root; Frobenius powers 5 and 25 are genuinely different. All 125 constructed test vectors passed semilinear basis transport and FV=VF=0. The exact integral identities and disjoint basis proofs, not finite sampling, establish all-p and all-n assertions.

Execution 010 independently reran the pinned submitted checker, which exited zero and reported 9014 assertions, the stated ten prime fields, n=3 through12, and 2000 semilinear F_25 vector pairs. These computations validate algebraic controls; they do not instantiate a Witt-ring Hopf algebra or replace the classification theorem.

The commands captured by run_logged.py in executions/001 through012 record actual child argv, explicit credential-free environment, cwd, runner interpreter/version, start/end UTC, full stdout and stderr, subprocess exit code, and input before/after SHA-256 pins. Both checker input-stability checks passed. Official-primary download/render runs are also retained, including the successful local rendering after the web screenshot error. manifest_build_record.json is an internally assembled preparation record with declared process information and checked pins; it is not independent native process-exit or stream evidence. It does not replace the actual captured 009/010 checker receipts. No installation, Git write, outside-person communication, or unrelated edit occurred.

check_realization.py is a portable self-contained control suitable for a public verification package: it needs only Python's standard library and embeds its own algebraic datum. It verifies linear algebra, not the primary classification texts or complete source provenance. verify_readonly.py is the **full local audit verifier**, requiring this entire namespace, raw private primary PDFs/renders, and the original-source/candidate workspace inputs at the manifest's relative bindings. It is not a default public verification-package entry point. The manifest and seal bind that full local audit; they do not imply that the private source bundle should be distributed.

Strongest verified result: the submitted family datum realizes the required actual p-killed finite flat W-group and the exact special-fiber qss flag for all p>3, n>=3. Remaining gap in this family: none in the mathematical realization argument under the explicitly cited classical equivalences. Overall theorem promotion, cross-family adjudication, and novelty remain root responsibilities. Completion estimate: 95% for this family; final root review and authorized sealing remain.
