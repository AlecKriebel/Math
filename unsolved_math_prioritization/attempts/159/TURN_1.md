# Turn 1: endpoint normalization and arithmetic obstructions

Original arbitrary-support conjecture unresolved. This first turn examines an arithmetic route to the full problem. It gives exact necessary conditions on any counterexample and proves broad conditional cases, but the missing sign-preservation step cannot be assumed. No novelty claim is made; the polynomial reformulation is credited to the literature.

## 1. Normalize without losing a probability hypothesis

Translate the finite supports so their minima are zero. Let F(x)=sum p_i x^i and G(x)=sum q_j x^j be the probability polynomials, with degrees m,n and positive endpoint coefficients. Independence means the sum polynomial is FG. If its support has s elements and its law is uniform, every positive coefficient of FG is 1/s. In particular p_m q_n=p_0 q_0=1/s.

Set A=F/p_m, B=G/q_n and C=sFG. Then A and B are monic with nonnegative coefficients, C has coefficients in {0,1}, and C(0)=1. Conversely any such factorization gives independent laws A/A(1), B/B(1) whose sum is C/C(1). Thus no assumption about consecutive support has entered.

Write A=sum a_i x^i and B=sum b_j x^j. Since b_n=a_m=1 and all terms are nonnegative,

a_i ≤ c_(i+n) ≤ 1, and b_j ≤ c_(m+j) ≤ 1.

Also a_0 b_0=c_0=1, so a_0=b_0=1. Consequently both factors have endpoint coefficients 1 and every coefficient lies in [0,1]. In the probability formulation, the masses at each summand's minimum and maximum agree and are maximal among all its atoms.

A factor of degree zero is 1 and the assertion is immediate. Equal positive degrees m=n are impossible: c_m contains the two distinct terms a_0 b_m and a_m b_0, each 1. This obstruction concerns a factorization with nonnegative coefficients and uniform sum; it does not say arbitrary finite distributions cannot have equal support sizes or equal degrees.

## 2. Rational searches cannot find a counterexample

Every coefficient of either monic factor is an algebraic integer. Indeed, its roots form a submultiset of the roots of the monic integer polynomial C; those roots are algebraic integers. Its coefficients are elementary symmetric polynomials in them and hence algebraic integers.

If A has rational coefficients, polynomial division over Q gives B in Q[x]. Rational algebraic integers are integers; combined with the [0,1] bounds this makes both factors 0–1. The same holds with A and B exchanged. In particular, if either original summand has rational probabilities, its monic normalization is rational and both summands must be uniform.

The coefficient fields agree. Starting from a_0=b_0=1, coefficient comparison gives

b_k = c_k − sum_(i=1)^k a_i b_(k−i),

with coefficients beyond the degrees read as zero. This proves all b_k lie in Q(a_1,…,a_m), and symmetry gives the reverse inclusion. Let K denote the common number field. Any counterexample requires a nontrivial number field and irrational coefficients in both normalized factors. All original probabilities are algebraic as well, since they are normalized by the algebraic sums A(1), B(1).

These are exact all-degree statements, not an inference from a rational grid scan. A search restricted to rational probabilities is therefore a blocked route to a counterexample.

## 3. The first fractional coefficient must collide with its complement

Let k be the smallest index at which any a_k or b_k is strictly between 0 and 1. Suppose a_k is fractional, interchanging factors if needed. All lower coefficients are Boolean. The coefficient identity is

c_k = a_k + b_k + S_k, where S_k=sum_(i=1)^(k−1) a_i b_(k−i)

is a nonnegative integer. Because 0<a_k<1 and 0≤c_k≤1, necessarily S_k=0, c_k=1 and b_k=1−a_k∈(0,1). Thus the first fractional index is shared by both factors, its two values are complementary, and no lower positive coefficient pair sums to k. In particular k≤min(m,n).

Apply the same argument to the reversed monic polynomials x^m A(1/x) and x^n B(1/x). There is also a common first fractional distance from the leading ends, with complementary coefficients and no earlier reverse collision. This does not assert that the two fractional indices measured from zero coincide, since the degrees need not agree.

## 4. A conditional conjugate-positivity theorem, and its exact gap

Suppose, in addition, that for every field embedding sigma:K→C all coefficients of sigma(A) and sigma(B) are nonnegative real numbers. Since sigma(A)sigma(B)=C and both conjugate factors remain monic, Section 1 gives every conjugate coefficient in [0,1]. For a nonzero coefficient alpha, its algebraic norm from Q(alpha) to Q is a nonzero integer. Every conjugate has absolute value at most 1, so that integer norm has absolute value at most 1. Hence all conjugates, including alpha, have absolute value 1, and nonnegativity gives alpha=1. Every coefficient is therefore 0 or 1.

It follows that any unfair factorization must lose nonnegative-real admissibility under some embedding of its coefficient field: at least one conjugate coefficient is negative or nonreal. If K is totally real, a negative conjugate coefficient is necessary. The argument does not prove that conjugate factorizations remain nonnegative. Conjugation preserves polynomial equations, not coefficient inequalities, so this is the sharp missing step in the attempted arithmetic proof of the full conjecture.

## 5. Controls and next route

The exact checker enumerates bounded rational coefficient grids and verifies the rational rigidity and first-fractional-prefix identities. Admissible nonintegral prefixes can occur, because a truncated prefix is not a finite factorization. They are deliberately distinguished from actual counterexamples.

The arithmetic route eliminates rational and conjugate-positive constructions, but does not rule out one positive real embedding among sign-changing conjugates. The next turn will investigate support-level collision constraints rather than silently assuming that extra arithmetic positivity.
