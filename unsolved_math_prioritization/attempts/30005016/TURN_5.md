# Turn 5: high-degree completions still fail in a larger mixed family

AI-assisted mathematical proof candidate; independent review pending.

## 1. The new construction class

Allow arbitrary polynomials f,g and arbitrary constants a,c. Consider

V_1=span{1,x,x²+a y,f},
V_2=span{1,y,y²+c x,g},
V_3=span{1,x,y,x²},
V_4=span{1,x,y,y²}.

These need not be directional cubic spaces, and the fourth generators may have arbitrarily high degree. Nevertheless this family cannot cover all four-point sets over R, or over any algebraically closed characteristic-zero field. As usual, a member of dimension below four cannot help.

This is a new obstruction within the final author turn. It does not classify all four-member families and does not prove an unrestricted lower bound five.

## 2. A four-point simultaneous kernel mechanism

Put B=−a, D=−c. We will choose T such that the two equations

p=x²−B y−T²=0, q=y²−D x−T²=0

have four distinct solutions in the field. Every such solution annihilates p∈V_1∩V_3 and q∈V_2∩V_4. Both p and q are nonzero polynomials. Hence on any four distinct common solutions, each four-dimensional V_i has a nontrivial evaluation kernel and fails interpolation. The fourth generators f,g do not affect this obstruction at all.

It remains essential to prove that the four solutions really exist in the chosen field; Bézout alone would not suffice for real or rational points.

## 3. Four distinct real solutions, with explicit quantitative bounds

Assume a,c∈R and set L=1+|B|+|D| and T=4L. For each pair of signs σ,τ∈{−1,1}, let R_{στ} be the closed square

|x−σT|≤L, |y−τT|≤L.

On this square define

F_{στ}(x,y)=(σ sqrt(T²+B y), τ sqrt(T²+D x)).

For every point of the square, |x|,|y|≤T+L=5L and |B|,|D|<L. Therefore each expression under a square root lies strictly between

T²−5L²=11L² and T²+5L²=21L².

Since (T−L)²=9L² and (T+L)²=25L², each square root lies between T−L and T+L. Thus F_{στ} maps the square into itself. The derivative of either coordinate with respect to its one active variable has absolute value bounded by

max(|B|,|D|)/(2(T−L)) < 1/6.

Consequently F_{στ} is a contraction in the sup norm. Iterating it from the center gives a Cauchy sequence, since successive differences decrease geometrically; the closed square is complete, so the limit is a fixed point. Squaring the two fixed-point equations shows p=q=0. The four squares are disjoint, so their four fixed points are distinct. This proves the real assertion without relying on numerical root finding.

## 4. Four distinct solutions over an algebraically closed field

Let K be algebraically closed of characteristic zero, with arbitrary B,D∈K.

If B=0, choose T avoiding 0,D,−D. Then x=±T; for each choice, y²=T²+D x is nonzero and has two distinct roots. These give four distinct solutions.

If B≠0, eliminate y=(x²−T²)/B. The remaining equation is

F_T(x)=(x²−T²)²−B²D x−B²T²=0.

Its discriminant in x is

−B⁴(27B⁴D⁴−288B²D²T⁴+256B²T⁶+256D²T⁶−256T⁸).

This is a nonzero polynomial in T, because its leading coefficient is 256B⁴. Choose T outside its finite root set. Then F_T has four distinct roots in K. Each determines a unique y through the eliminated equation, giving four distinct common solutions. The displayed discriminant identity is verified symbolically in the checker by the resultant definition. This proves the algebraically closed assertion.

No unconditional rational-field claim follows from this argument. Four geometric solutions need not be four rational solutions.

## 5. Final author outcome after five genuine turns

Original problem: unresolved, five of five author turns completed. No sixth author search is permitted within this attempt.

The strongest unrestricted bound in this packet is 4≤m_4(K)≤5 for algebraically closed characteristic-zero K, via classical arrangement local cohomology. The same range holds for the best worst-case bound over all characteristic-zero fields. The exact credited value m_4(Q(t))=1 and the conditional number-field consequence remain distinct. Over R the unrestricted bounds established here are 2≤m_4(R)≤5.

Turns 3–5 rule out two broad mixed construction classes and solve the separate directional-cubic minimum exactly (six). None rules out every possible four-member polynomial family. The missing result is either an unrestricted four-space construction or a valid obstruction excluding every such family; field-specific values can require different arguments.

Informal completion estimate remains 35%. The final independent review should check each scoped result and exact source, while preserving the unresolved original disposition. It must not count the source-preamble correction or a restricted-class theorem as a full solution.
