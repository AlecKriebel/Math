# Attempt 4: simultaneous square constraints through Büchi rigidity

## Strategy

The preceding attempts force attention to simultaneous constraints. A natural candidate is the family

B_M(x,y): for i=0,...,M-1, P₂(y+2i x+i²).              (1)

All coefficients in (1) are fixed integers once M is chosen, so this is a legal positive quantifier-free formula after writing multiplication by 2i as repeated addition. It does not contain a squaring function. Semantically the tested values come from the monic quadratic f(T)=T²+2xT+y.

If some fixed M forces every rational monic quadratic with square values at 0,...,M-1 to be a polynomial square, then B_M(x,y) defines y=x². This is a rational Büchi-rigidity hypothesis, not a theorem established here.

## Conditional compilation of the ring language

Under that hypothesis, if B_M(x,y) holds, write f(T)=(T+c)². Comparing coefficients gives c=x and y=x². Conversely y=x² makes every tested value (x+i)² a rational square. Thus the relation Sq(x,y):=B_M(x,y) is exactly the squaring graph.

Define Mult(a,b,c) by

exists s,t,u: Sq(a,s), Sq(b,t), Sq(a+b,u), u=s+t+c+c.

The polarization identity makes this equivalent to ab=c. This is a positive-existential formula in the original language. Every ring polynomial equation can then be expanded into finitely many intermediate additions and instances of Mult, preserving existential positivity. Poonen's Theorem 1.1 on Diophantine nonsquares consequently supplies the desired original-language definition of N. The prior nonzero definition then removes negated equalities, while N removes negated square atoms, so the complete AIM Question 6 has an affirmative answer conditional on rational Büchi rigidity.

This is a conditional implication, not an importation of variable multiplication as if it were already available.

## An explicit geometric sufficient hypothesis

We can derive the needed rigidity from the following unproved uniformity hypothesis:

(U_B) There is an integer B≥0 such that every smooth projective genus-two curve over Q has at most B rational points.

**Proposition.** Assuming (U_B), formula (1) with M=(B+1)³+3 defines the squaring graph.

**Proof.** Let f(T)=T²+2xT+y and put δ=y-x². Suppose δ≠0 and all the values f(0),...,f(M-1) are rational squares. Since the nonzero polynomial f has at most two roots, there is ε in {0,1,2} with f(ε)≠0. Set c=x+ε and

g(U)=f(U³+ε)=(U³+c)²+δ.

The derivative is 6U²(U³+c). A repeated root of g must therefore have U=0 or U³+c=0. The first alternative would give g(0)=f(ε)=0; the second would give g(U)=δ=0. Both are excluded. Thus g is squarefree of degree six, and the smooth projective model of V²=g(U) has genus two.

For every integer j=1,...,B+1, the integer n=j³+ε lies between 0 and (B+1)³+2=M-1. Hence f(n) is a rational square and supplies a rational point on this curve with U=j. These B+1 points are distinct, contradicting (U_B). Therefore δ=0, giving y=x². The converse was already proved. □

The use of three shifts is deliberate for rational coefficients. Two shifts 0 and 1 would both fail the smoothness test for f(T)=T(T-1), corresponding to x=-1/2, y=0. An integer-coefficient formulation that rules out this case cannot simply be copied to rational x. The third shift resolves it. The proof is a rational adaptation of the standard genus-two uniformity strategy for Büchi's problem, as discussed in Hector Pasten's ICTP lecture notes, https://indico.ictp.it/event/9617/session/2/contribution/4/material/1/0.pdf, Theorem 5.9 and its proof. The hypothesis (U_B) remains an assumption here.

## Small constraints give exact false positives

The five rational numbers

11/9, 50/9, 71/9, 88/9, 103/9

give the square values of f at 0,...,4 when

x=383/27, y=121/81.

Directly,

f(i)=i²+(766/27)i+121/81,

and its values are 121/81,2500/81,5041/81,7744/81,10609/81, respectively. Their second differences equal 2, but

y-x²=-145600/729≠0.

Thus B_5 has a concrete false positive, as do its shorter initial conjunctions. This tuple is a known rational Büchi example recorded in the indexed Pasten–Pheidas–Vidaux survey excerpt and Joseph Lipman's directly inspected notes (p. 10), https://www.math.purdue.edu/~jlipman/Buchitalk-Huge.pdf, not a new counterexample discovered here. Exact rational arithmetic checks are supplied separately. It would be invalid to verify a few small M and infer a uniform valid M, or to claim that B_5 defines multiplication.

## Attempt outcome

We obtained a fully explicit conditional path from a uniform genus-two rational-point bound to an affirmative answer to Question 6, with a precise original-language formula at the intermediate squaring step. Neither that uniformity hypothesis nor an unconditional rational Büchi bound was proved. Current primary sources inspected include Lipman's notes, the indexed Büchi survey excerpt (full fetch timed out), and the 2025 Jaillet–Vidaux paper on length-four integer sequences; those concern related progress and do not provide the needed unconditional rational bound. The attempt therefore does not resolve the remaining nonsquare definition.

## Additional current-literature scope check

Stanley Yao Xiao's arXiv:2412.16740v3 (7 June 2025), https://arxiv.org/abs/2412.16740, claims an unconditional theorem for five INTEGER squares, explicitly in Theorem 1.3. Its displayed theorem does not concern arbitrary rational square values. This investigation neither validates nor refutes its proof; even if accepted, the theorem does not supply rational Büchi rigidity. Clearing a common denominator multiplies the second difference by its square, so it does not turn a rational second-difference-two sequence into the required integer second-difference-two sequence. The known rational tuple above illustrates the obstruction directly. Pasten–Vidaux's 2016 paper, https://people.math.harvard.edu/~hpasten/preprints/PVmultPoly.pdf, is likewise conditional and stated over the integers in its abstract. Neither is credited with resolving this rational reduct question.

Fresh substantive attempt count: 4/5.
