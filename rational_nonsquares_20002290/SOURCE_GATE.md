# Statement, prior baseline, and literature scope

Checked 2026-10-03 UTC.

## Original target

AIM, *Problems related to “Definability and Decidability Problems in Number Theory”*, moderated by Thomas Scanlon, notes by Jeroen Demeyer, September 9–13, 2013, printed page 2, Question 6 (Koenigsmann): https://aimath.org/pastworkshops/definabilityinntproblems.pdf.

The target is equality of existential and existential-positive definability in (Q;0,1,+,P₂), where P₂ consists of all rational squares, including zero. The source gives two target sets whose positive-existential definability together is equivalent to the original assertion: nonzero rationals and rational nonsquares. Its language symbol is calligraphic O₂. Squaring in its displayed description of the nonsquare set is semantic notation, not an extra function symbol.

No multiplication, order, integer predicate, or squaring graph is supplied. Equality is logical. Fixed rational parameters do not change the problem: any m/n, n>0, has a unique additive definition using 0 and 1; negative coefficients can be moved to the opposite side of an equation. All formulas here can therefore be expanded without parameters.

The exact catalogue URL https://www.unsolvedmath.com/problems/20002290 returned 403 in a direct cloud-browser check and could not be read through web extraction. Its identity and statement were checked against the supplied hash-verified catalogue and an indexed listing. Exact live-page freshness is not claimed. The original AIM PDF was independently downloaded, read, and its Question 6 visually inspected. Its 2013 header corrects the earlier report's 2014 source-year citation.

## Prior baseline: credited, not a fresh attempt

The existing catalogue report explicitly gives only partial progress. Its main formula is

Theta(x): exists a,b₁,b₂,b₃,b₄ such that x=a+b₁+b₂+b₃+b₄, P₂(a), P₂(a+2), and all P₂(b_i).

This formula defines x>0. Indeed its summands are nonnegative, and x=0 would force a=0 and hence the false predicate P₂(2). Conversely, rational t tending to sqrt(2) gives

u=(t-2/t)/2, v=(t+2/t)/2, v²-u²=2,

with 0<u²<x. Set a=u². Lagrange's four-square theorem writes x-a as four rational squares: for a positive rational A/B, represent the integer AB as four integer squares and divide by B². These are witnesses for Theta(x).

Therefore Q× is defined by Theta(x) or exists z (x+z=0 and Theta(z)). Negated equalities can then be replaced using the nonzero formula. Disjunctive normal form shows that the remaining obstruction is exactly a positive-existential definition of ¬P₂(x). These arguments are verified prior background and consume none of the five new attempts.

Bounded repository searches for the exact problem ID and code found no earlier research artifact or PR, and the live queue entry began queued at 0/5. Absence from these searches is not a claim about all unindexed history.

## Primary and authoritative sources

1. Bjorn Poonen, *The set of nonsquares in a number field is diophantine*, Mathematical Research Letters 16 (2009), 165–170, Theorem 1.1. Author's corrected PDF: https://math.mit.edu/~poonen/papers/nonsquares.pdf. This is a full-ring-language theorem and does not itself solve the reduct question.
2. Jochen Koenigsmann, *Defining Z in Q*, Annals of Mathematics 183 (2016), 73–93. Official article: https://annals.math.princeton.edu/2016/183-1/p02; accepted preprint: https://arxiv.org/abs/1011.3424. Its elementary nonsquare theorem likewise uses the ring language.
3. Bjorn Poonen, *Introduction to arithmetic geometry*, Theorem 26.3 (quadratic-form representation over Q versus all completions): https://math.mit.edu/~poonen/782/782notes.pdf. This classical Hasse–Minkowski input is the basis for Attempt 3.
4. Hector Pasten, *Diophantine equations with few solutions*, AGRA IV lectures (2021), Theorem 5.9 and its proof: https://indico.ictp.it/event/9617/session/2/contribution/4/material/1/0.pdf. Attempt 4 adapts the genus-two uniformity strategy to rational coefficients and uses three shifts to handle a rational exceptional case.
5. Joseph Lipman, *Büchi's problem about squares*, notes revised 2021, p. 10: https://www.math.purdue.edu/~jlipman/Buchitalk-Huge.pdf. Source for the rational tuple (11,50,71,88,103)/9. The Pasten–Pheidas–Vidaux survey (2010) also records this example in its indexed excerpt; a full fetch of that survey timed out, so the directly inspected Lipman reference is supplied.
6. Fabrice Jaillet and Xavier Vidaux, *A note on Buell's theorem on length four Büchi sequences*, CUBO 27(1) (2025), 1–5: https://cubo.ufro.cl/index.php/cubo/article/download/3991/2391/11881. Its domain is integer sequences; it is not a rational rigidity theorem.
7. Stanley Yao Xiao, *Hilbert's tenth problem for systems of diagonal quadratic forms, and Büchi's problem*, arXiv:2412.16740v3, 7 June 2025: https://arxiv.org/abs/2412.16740 and https://arxiv.org/html/2412.16740v3. Theorem 1.3 explicitly claims a result for integer squares. The proof is not audited here, and its validity is not needed. Even if accepted, clearing denominators changes the second difference, so it does not supply the rational theorem needed in Attempt 4.
8. Hector Pasten and Xavier Vidaux, *Positive existential definability of multiplication from addition and the range of a polynomial*, Israel Journal of Mathematics 216 (2016), 273–306. Author PDF: https://people.math.harvard.edu/~hpasten/preprints/PVmultPoly.pdf. The abstract's theorem is conditional and stated over the integers.
9. Manuel Bodirsky, *Complexity of Infinite-Domain Constraint Satisfaction*, Theorem 2.5.2: https://wwwpub.zih.tu-dresden.de/~bodirsky/Book.pdf. The indexed primary-source excerpt states the homomorphism-preservation theorem modulo a theory. A full web fetch exceeded the size limit. Attempt 5 includes its specialized compactness proof, so that deduction does not depend on an inaccessible proof text.

No full resolution of the exact additive-square-predicate question was located in the checked primary sources or targeted current searches. This is a limited literature finding, not proof of worldwide current openness. The restricted deductions and conditional reductions make no claim to historical novelty. The catalogue's prior Q× definition and the standard Büchi/preservation mechanisms are credited rather than presented as new full solutions.
