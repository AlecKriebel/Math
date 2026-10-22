# Strong rational Diophantine quadruples

Problem 8500009 / AMR-084-0009. Mathematical audit dated 6 October 2026.

## Outcome

**PARTIAL. No strong rational Diophantine quadruple has been constructed here, and nonexistence has not been proved.** The latest inspected author-maintained problem list is dated **5 October 2026** and retains the existence question as Problem 1.15 [1]. This investigation stops after three focused approaches: exact benchmark and regular-extension checks; the full square-lifting curve; and the sign/zero-product distinction. Further routine bounded searches would not close the rational-point gap identified below.

The deliverable consists of an exact correction to the benchmark's failure condition, a full extension-curve formulation with its genus proved, an explicit counterexample to replacing individual squares by their product, and a sign-normalization lemma with its indispensable exception. These are reproducible audits and elementary rederivations, with **no claim of priority or novelty**.

## The exact question

Find four **distinct, nonzero rational numbers**, of unrestricted sign, for which all ten values a_i a_j + 1 with i <= j are rational squares. Zero is a square, so a cross-product a_i a_j + 1 = 0 is allowed. Positivity is not assumed. Repeating an element or appending zero does not answer the question. Ordinary Diophantine quadruples impose only the six off-diagonal conditions. No nonzero integer can satisfy its diagonal condition: for |n| >= 1, n^2 < n^2+1 < (|n|+1)^2.

The maintained survey's applicable location is **Section 5.5**, not the current Section 5.4 [2]. The exact problem web page could not be retrieved: the web reader reported inaccessible, and direct HTTPS returned 403. The statement was reconciled against the original primary definition and the current problem list; this access limit is not evidence of a mathematical discrepancy.

## Approach 1  Exact benchmarks

The original 2008 paper [3, Section 5, manuscript p.11] gives the almost-strong example

(a,b,c,d) = (140/51, 2223/30464, 278817/33856, 3182740/17661).

All **four diagonal** conditions hold. Its only failure is **c d + 1**, an off-diagonal condition. In particular, it is not an ordinary Diophantine quadruple with one bad diagonal.

| Pair | Nonnegative rational square root of a_i a_j + 1 |
|---|---:|
| 1,1 | 149/51 |
| 1,2 | 149/136 |
| 1,3 | 447/92 |
| 1,4 | 1937/87 |
| 2,2 | 30545/30464 |
| 2,3 | 3725/2944 |
| 2,4 | 6109/1624 |
| 3,3 | 280865/33856 |
| 3,4 | Not a rational square |
| 4,4 | 3182789/17661 |

The exceptional value in reduced form is 459627303/309488. Its numerator lies strictly between 21438^2 and 21439^2, and its denominator strictly between 556^2 and 557^2. A reduced nonnegative rational is a rational square precisely when its numerator and denominator are integer squares. This certifies failure without floating-point arithmetic.

A separate transcription issue is present in the live 5 October 2026 version of [1, p.4]: it prints **2223/3046**. Visual inspection confirms the missing final digit. The original manuscript [3, p.11] and maintained survey [2] give **2223/30464**; the shorter-denominator value fails even its diagonal condition. The certificates use the original value, not the typo.

The positive strong triple (1976/5607, 3780/1691, 14596/1197), recorded in [3], has the ordinary regular extensions

135938/106533 and 789662/11837.

They satisfy all three new cross-product conditions but fail the new diagonal condition. The respective diagonal values are 29828419933/11349280089 and 623706188813/140114569, neither a rational square. Thus ordinary regular extension does not finish even this concrete starting case. This is an exact rejection of these two candidates, not a classification of the triple's extensions.

## Approach 2  Keep every square condition

Let a_1,...,a_k be fixed distinct nonzero rationals with a_i^2+1 rational squares; k >= 1. When seeking an extension of a strong tuple, also require the existing cross-conditions. Put

x = (t^2-1)/(2t),  t in Q and t != 0,

Q_i(t) = a_i t^2 + 2t - a_i,

f_i(t) = 2t Q_i(t).

### Proposition 1  Exact lifting criterion

A rational x extends the given strong tuple by a new nonzero element if and only if there is t in Q*, with x=(t^2-1)/(2t), such that every f_i(t) is a rational square, x != 0, and x is distinct from each a_i.

**Proof.** The identity

x^2+1 = ((t^2+1)/(2t))^2

gives the new diagonal. Conversely, if s^2=x^2+1, then t=x+s is nonzero (otherwise 1=0) and x=(t^2-1)/(2t). For every i,

f_i(t) = (2t)^2 (a_i x+1).

Since (2t)^2 is a nonzero rational square, the individual square conditions are equivalent in both directions, including when a_i x+1=0. Nonzero and distinctness restrictions must still be imposed. Here x=0 corresponds precisely to t=1 or t=-1. Repetition x=a_i corresponds to t=a_i +/- sqrt(a_i^2+1). This proves the criterion. □

### Proposition 2  The full curve has genus 3 for a pair and 9 for a triple

Consider the smooth projective normalization of

y_i^2 = f_i(t),  i=1,...,k.

It is geometrically connected, its map to the t-line has degree 2^k, and its geometric genus is

g = 1 + 2^(k-1)(k-1).

Thus k=1,2,3 give g=1,3,9, respectively.

**Proof.** Choose s_i in Q with s_i^2=1+a_i^2. The two roots of Q_i are (-1+s_i)/a_i and (-1-s_i)/a_i. They are distinct and nonzero, because a_i != 0 and s_i^2>1. No root is shared by Q_i and Q_j when i != j: subtraction would give (a_i-a_j)(t^2-1)=0, hence t=+/-1, neither of which is a root of any Q_i.

Over the algebraic closure, a nonempty product of some f_i has odd valuation at a root unique to one selected Q_i. Consequently the square classes of the f_i are independent. The multiquadratic cover is connected and has degree N=2^k.

Its branch points are t=0, t=infinity and the 2k distinct roots just described. Every branch point has ramification index exactly two. At a root of Q_i only the i-th square class ramifies. At zero every f_i has valuation one; at infinity every f_i has valuation minus three. In each of those latter two cases the common parity vector spans only one inertia direction, so the index remains two, not 2^k. More explicitly, over the algebraically closed residue field every unit in the completed local ring has a square root, so the completed extension is generated by a single square root of a local parameter.

Riemann-Hurwitz gives

2g-2 = -2N + (2k+2)(N/2) = 2^k(k-1),

which is the asserted formula. Rational t=0 is excluded from the extension criterion; the projective normalization is used here to compute the genus, not to introduce extra permissible x-values. □

### Why the product-square relaxation is insufficient

For k=2, replacing the two individual equations by their product gives the elliptic quotient

w^2 = Q_1(t) Q_2(t),  w = y_1 y_2/(2t).

This loses a square-class condition. An exact example uses the valid strong pair (3/4,-4/3) and t=3/4, so x=-7/24. Then x^2+1=(25/24)^2, while

(3/4)x+1 = 25/32,  (-4/3)x+1 = 25/18.

Neither is a rational square, although their product is (25/24)^2. In the quotient coordinates, Q_1(t)Q_2(t)=(25/16)^2, so the rational quotient point exists but cannot lift to the full two-equation curve over Q.

Likewise, the genus-two product curve for a fixed triple in [3, manuscript p.2] is a useful necessary condition, not an equivalence to all four new square conditions. Proposition 1 states the missing lifting requirements explicitly. No rational-point completeness calculation is claimed here.

## Approach 3  Signs and zero products

The fractional-linear transformation below generalizes the triple transformation in [3, Section 2]. Its exception cannot be discarded.

### Proposition 3  A tuple with no zero cross-value can be made positive

If a strong rational tuple has a_i a_j+1 != 0 for all distinct i,j, then a positive strong tuple of the same size exists.

**Proof.** Simultaneous negation preserves all products, so arrange that the maximum element a is positive. Keep a and replace every other element b by e_b=(a-b)/(ab+1). Every denominator is a positive rational square, and b<a, so each e_b>0. Direct identities give

a e_b+1 = (a^2+1)/(ab+1),

e_b^2+1 = (a^2+1)(b^2+1)/(ab+1)^2,

e_b e_c+1 = (a^2+1)(bc+1)/((ab+1)(ac+1)).

They are all rational squares. The transformation is injective because its determinant is -(a^2+1), and e_b=0 would force b=a. Equality e_b=a would force b(a^2+1)=0, contrary to b != 0. Thus distinctness and nonzero cardinality are preserved. □

### Proposition 4  At most one zero cross-value

In any real tuple satisfying all off-diagonal square conditions, a zero cross-value can occur for at most one unordered pair of distinct elements, and that pair is the minimum and maximum of the tuple.

**Proof.** Suppose ab=-1, with a>0 and b=-1/a<0. For every other element c, the inequalities ac+1>=0 and bc+1>=0 force b<=c<=a. Thus the endpoints a,b are the extreme elements. Any other pair with product -1 would by the same argument have to be those same two extreme elements. □

The exceptional case is real, even for strong triples: [3, Section 4] gives (37620/26299,195/28,-28/195), verified in the certificate. The final pair has product -1. Consequently a signed quadruple cannot be reduced to the positive problem by blindly dividing by all cross-values.

These lemmas leave two genuine possibilities: a positive strong quadruple, or a strong quadruple containing exactly one reciprocal-negative extreme pair. Neither possibility is settled here.

## Precise remaining gap and stopping decision

For the known almost quadruple, the first two entries define a genus-three full strong-extension curve. The final two entries are genuine rational lifts on that curve, but they are not mutually compatible. Closing this route requires finding two distinct nonzero extensions whose mutual product plus one is square, or rigorously classifying all rational lifts for that pair and excluding all compatible pairs. No such classification or compatible pair was obtained.

For a fixed strong triple, the full genus-nine curve requires a rational point outside x=0 and the repeated-element values, with all square classes lifting simultaneously. Finding a point on a product quotient or obtaining another ordinary regular extension is insufficient. No universal obstruction, exhaustive rational-point computation, or proof that every strong pair fails to extend has been supplied.

Three approaches have been used, within the five-approach ceiling. Stop on this sharply stated partial result. The proposed mathematical status is **partial, 3/5**, not solved. Literature status and originality are separate: the current primary sources retain the question, but an unsuccessful search does not establish novelty.

## Primary sources and scope

1. Andrej Dujella, *Open problems on Diophantine m-tuples and elliptic curves*, live PDF dated 5 October 2026; Problem 1.15, p.4. Direct bytes and cover/problem-page images were inspected. The cached web extraction was older, dated 28 March 2026. https://web.math.pmf.unizg.hr/~duje/pdf/open2.pdf
2. Andrej Dujella, maintained survey, *Rational Diophantine m-tuples*, Section 5.5. https://web.math.pmf.unizg.hr/~duje/ratio.html
3. Andrej Dujella and Vinko Petričević, *Strong Diophantine triples*, Experiment. Math. 17 (2008), 83–89. Author manuscript, especially pp.2–5, 8–11. https://dujella.github.io/pdf/strong3.pdf
4. Andrej Dujella, Matija Kazalicki and Vinko Petričević, *Rational Diophantine sextuples with strong pair*, RACSAM 119 (2025), Article 36. Theorems 1–2 and proof sections inspected. The result gives two strong elements inside ordinary sextuples, not four strong elements. https://dujella.github.io/pdf/strongDKP.pdf
5. Andrašek, Kazalicki and Vlah, *Quartic Rational Diophantine Quadruples and the Euler Surface*, arXiv:2604.19140v1, 21 April 2026. Definition 1.1 requires i<j; its fourth-power cross-products do not impose diagonal-square conditions. https://arxiv.org/html/2604.19140v1

Related strong D(-1) and D(q) triple papers were inspected as well; their conclusions do not give a D(1) quadruple. Some older title/abstract matches use “strong quadruple” differently or do not visibly verify the diagonals; no adverse conclusion about those papers is needed or claimed in this report. The retained primary status statement is limited to the inspected sources and date.

## Reproduction and boundaries

Run `python verify_exact.py --test`, `python -O verify_exact.py --test`, and `python -I verify_exact.py --test`. `python verify_exact.py` emits the exact certificate. `python run_mutations.py` reruns the genuine file in isolated relocated directories, checks unchanged certificate output, and requires each deliberately faulty implementation to fail its tests. All arithmetic uses integers and reduced fractions.

The program checks exact examples and identities, not the abstract Riemann-Hurwitz proof. Test success is not a classification of rational points. No external packages, network access, or source PDFs are required to rerun the mathematical tests. Public metadata records source and corpus integrity without including source text or corpus records. Publication requires a fresh independent mathematical audit of this frozen packet.
