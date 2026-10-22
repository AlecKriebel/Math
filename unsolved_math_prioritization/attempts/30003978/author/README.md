# Irrational Seshadri constants and the Nagata question

Problem 30003978 / OWR-16628-010; queue rank 743. Checked 5 October 2026.

## Outcome

**Prior-literature resolution candidate, 1/5 substantive approaches.** Recent primary preprints supply the requested conclusion for every integer r >= 9. The proof of this implication is the short theorem application below. This is a literature finding, not a new solution or a claim to have proved Nagata's conjecture. Both decisive manuscripts are currently preprints; no peer-reviewed publication was verified. A fresh independent audit of this packet remains required before any publication.

The August 2026 catalogue triage predates both decisive manuscripts. Further original-solution attempts were stopped once their exact theorem statements and parameter coverage had been checked.

## Recovered question and scope

The primary source is Krishna Hanumanthu's contribution, joint work with Brian Harbourne, in [Oberwolfach Report 45/2018, printed pp. 2760–2761](https://ems.press/content/serial-article-files/46765?nt=1). Its final question asks whether the conclusion of Theorem 1 follows from Nagata for X_r alone. Thus the target is:

For each r >= 9, let X_r be a complex plane blown up at r sufficiently general centers. Assuming Nagata's degree-versus-sum-of-multiplicities inequality on X_r, does some ample integral line bundle L on X_r have irrational epsilon(L;x) at a very general point x?

The cited full paper makes the blowup centers **very general**: see the setup on p. 2 and Question 2.6 on p. 5 of [Hanumanthu–Harbourne](https://www.cmi.ac.in/~krishna/irrational-seshadri-constants.pdf). This is the interpretation used here. “Very general” means outside a countable union of proper closed subsets. This packet does not replace that by a single Zariski-open locus of centers, and makes no assertion for arbitrary centers or all evaluation points.

The desired invariant is the **one-point** constant of an ample integral divisor on the smooth surface X_r. It is not the r-point constant of O(1) on the plane, a constant on a singular quotient, or an irrational real scalar multiple of a rational divisor. The evaluation point requires one additional blowup in the nef-threshold formulation. The antecedent printed in the question is Nagata for X_r, not the negative-curve conjecture for X_(r+1).

A source warning: the OWR proof sketch writes a negative intersection with pi*L although a pullback of an ample divisor is nef. The relevant Seshadri boundary class includes the subtracted exceptional term. The question and the cited full-paper setup, rather than that abbreviated sketch, govern this packet.

## Decisive later statements

1. Antonio Laface and Luca Ugaglia, [Irrational Seshadri constants from dihedral orbits, arXiv:2609.26521v2](https://arxiv.org/abs/2609.26521), Theorem 2, p. 2. First submitted 22 September 2026; inspected revision 25 September 2026. For nine very general plane points the integral divisor

   L = 9H - 3(E1+...+E5) - 2(E6+...+E9)

   is ample, and epsilon(L;x)=2 sqrt(5) at a very general point. The theorem concerns a smooth blowup and has no Nagata assumption.

2. Grzegorz Malara, Łukasz Merta, Justyna Szpond and Marcin Zieliński, [Dihedral reflections and an infinite series of irrational Seshadri constants, arXiv:2610.01783](https://arxiv.org/abs/2610.01783), Theorem 1.2, p. 2; inspected v1, 1 October 2026. Put n=2k+1 >= 7 and r=k+7. On the blowup at r very general plane points,

   L_n = (3n-4)H - nE1 - (n-2)(E2+...+E5)
         - 4(E6+...+E_(k+5)) - 2(E_(k+6)+E_(k+7))

   is ample and has epsilon(L_n;x)=2 sqrt(n(n-4)) at a very general point, without a conjectural hypothesis.

These are credited theorem inputs. This packet does not present their geometric constructions as independently discovered mathematics.

## Complete deduction of the answer from these theorems

Fix r >= 9. For r=9 use statement 1. Its square is 81-5(9)-4(4)=20, and 2 sqrt(5) is irrational.

For r>=10 set n=2r-13 and k=r-7. Then n is odd, n>=7, and k+7=r. Statement 2 therefore applies to this exact r, not merely to an infinite subsequence. Its coefficient blocks have 1+4+k+2=r entries. Moreover,

(n-3)^2 < n(n-4) < (n-2)^2,

because the respective positive differences are 2n-9 and 4. These are consecutive nonnegative integer squares. Consequently n(n-4) is not a square, and the asserted constant is irrational. All divisor coefficients are integers.

This proves the desired conclusion on very general X_r for every r>=9 using the two cited theorems. A conclusion available without Nagata also holds when Nagata is assumed. The original conditional problem has not been converted into a proof of its antecedent, and the unconditional examples are credited solely to the later theorems.

## Checks and their limits

- The complete two decisive PDFs were downloaded, their statements and all proof sections read, and both theorem pages visually inspected. The source hashes and precise inspection scope are in SOURCE_VERIFICATION.json.
- The ampleness criterion cited by the uniform construction was checked directly against Hanumanthu, arXiv:1507.06391v3, Theorem 2.1. Its hypotheses match the inequalities verified here.
- PROOFS.md supplies elementary universal checks and exact controls against scope errors. verify_math.py gives reproducible symbolic and finite arithmetic verification; verification.json records 85,787 assertions. These counts do not prove nefness, quotient descent, or specialization.
- The decisive papers' geometric arguments remain cited mathematical inputs. No proof-assistant formalization, external referee acceptance, or complete reproof of their imported algebraic-geometric foundations is asserted.
- The primary setup and the latest identified theorem statements match. No mathematical gap in the short deduction above was found. A stronger claim for arbitrary centers, every evaluation point, or the full Nagata conjecture is outside scope.

## Reproduction and files

Use Python 3 and SymPy 1.14.0:

    python3 verify_math.py > reproduced.json
    cmp reproduced.json verification.json
    python3 verify_manifest.py

Run reproduction outside this frozen directory or remove the temporary reproduced.json before strict inventory verification. The manifest covers only authored reports, proofs, code, result JSON and public verification metadata. Source PDFs, source text extractions, source images, raw datasets and private coordination material are excluded. No remote write was made in this attempt.

This work used AI extensively and is unrefereed. No novelty, first-priority, or independent full proof claim is made.
