# Attempt 5 of 5: Eliminate all negations and expose the multi-exponent arithmetic

## Target and verdict

The final attempt seeks an exact normal form for the full existential problem and tests whether the one-parameter algorithm extends. We prove that every existential sentence in the target structure can effectively be replaced by a positive-existential sentence. We then reduce the exact full problem to integer solvability of linear systems whose coefficients depend on independently chosen powers p^s. A concrete unbounded gcd family blocks the attempted fixed-modulus extension. No decision algorithm or undecidability interpretation for the resulting unrestricted problem is obtained.

## 1. Positive-existential nonzero and p-free parts

Write

    Unit_p(u) := OR_(r=1,...,p-1) EXISTS w (u=pw+r).

This says p does not divide u. It uses only addition and constants and works for negative integers because division with remainder can be taken with r∈{0,...,p-1}.

Define

    NZ(x) := EXISTS u [Unit_p(u) AND R_p(u,x)].         (1)

Then NZ(x) is equivalent to x≠0. If x≠0, divide by its maximal nonnegative power of p, yielding the unique p-free part u; then R_p(u,x). Conversely u is nonzero, so every p-power multiple of u is nonzero. This proof uses neither order nor multiplication of two integer variables.

In particular additive disequalities are positive-existential: L≠M iff there exists d with L=M+d and NZ(d).

For every nonzero x there is a unique integer u such that Unit_p(u) and R_p(u,x). It retains the sign of x. Uniqueness follows because if x=p^a u=p^b v with p∤u,v, comparing maximal p-power divisibility gives a=b and u=v.

## 2. Positive-existential complement of the directed relation

Let NR_p(x,y) be the disjunction of these four positive-existential conditions:

    (a) x=0 AND NZ(y);
    (b) y=0 AND NZ(x);
    (c) EXISTS u,v,d [Unit_p(u) AND Unit_p(v)
                     AND R_p(u,x) AND R_p(v,y)
                     AND u=v+d AND NZ(d)];
    (d) NZ(y) AND R_p(py,x).                          (2)

Then NR_p(x,y) iff not R_p(x,y).

Proof. Cases (a),(b) handle exactly the pairs with one zero. Case (c) says the two nonzero numbers have different signed p-free parts; this prevents either from being a p-power multiple of the other. Case (d) says x=p^(k+1)y for some k≥0 and y≠0, so x lies strictly later on the same directed p-chain. Such a pair cannot also satisfy y=p^s x. These prove every branch implies the complement.

Conversely suppose not R_p(x,y). If exactly one value is zero, use (a) or (b); both zero is not in the complement. Otherwise write x=p^a u and y=p^b v with signed p-free u,v. If u≠v, branch (c) holds. If u=v, the relation would hold precisely for a≤b. Its failure gives a>b, and x=p^(a-b)y with a-b≥1, which is branch (d). This proves the equivalence, including opposite signs and the zero exception in (d). QED.

The direction of R_p is indispensable in the last branch. Replacing it by an undirected same-chain relation would not justify this formula.

## 3. Equivalence of existential and positive-existential decision problems

Push a quantifier-free matrix into negation normal form. Replace every negated equality by (1), and every negated R_p-atom by (2). Rename newly introduced existential variables and pull them outward, distributing finite disjunctions if desired. All replacements use positive-existential formulas. Therefore every existential sentence is effectively equivalent to a positive-existential sentence in the same original language.

The converse reduction is trivial since positive-existential sentences are existential. Thus the two decision problems are equivalent. This theorem does not assert quantifier elimination or a bounded number of positive atoms: the replacements introduce additional independent R_p-atoms. It is compatible with the earlier one-positive-atom fragment result, whose atom budget would generally be lost under this translation.

## 4. Exact unrestricted matrix normal form

After DNF conversion, a positive-existential conjunction consists of integral additive equations and finitely many atoms R_p(L_i(z),M_i(z)). Introduce independent nonnegative exponent parameters s_i. The conjunction is equivalent to

    A(p^s_1,...,p^s_k)z=b(p^s_1,...,p^s_k),            (3)

where the i-th relation row is M_i(z)-p^s_i L_i(z)=0. Each such row depends affinely on its own parameter, and all other rows are constant. All arithmetic unknowns z are still integers. Exponent parameters are external variables in this exact solvability reformulation, not integer variables mistakenly assumed to be definable inside the original structure.

Conversely each system with this special row form translates back to R_p-atoms. Together with the negation-elimination theorem, this is an exact reformulation of the full AIM existential problem.

More general polynomial coefficients in finitely many power parameters are also expressible, using the synchronized multiplier G_p from Attempt 3 repeatedly. This broader presentation can be useful, but does not remove independent parameters.

## 5. A precise failure of the one-variable Bezout strategy

In Q[T_1,T_2], the polynomials T_1-1 and T_2-1 have no common nonconstant factor, but their ideal contains no nonzero constant: evaluating at (1,1) would make such a constant zero. Thus “polynomial gcd 1 implies a constant Bezout identity,” used legitimately in Q[T], is false in the multivariable ring.

The arithmetic obstruction is visible on the power locus:

    gcd(p^a-1,p^b-1)=p^gcd(a,b)-1                    (4)

for a,b≥0, with gcd(0,0)=0. For positive a,b, the Euclidean algorithm proves (4) using

    (p^a-1)-p^(a-b)(p^b-1)=p^(a-b)-1  when a≥b.

Zero cases follow directly. The gcd is unbounded as a=b→∞, so no single fixed modulus controls this example in the way the one-parameter coprime-polynomial proof requires.

Consequently the solvability of

    (p^a-1)z_1+(p^b-1)z_2=p^c-1                      (5)

is equivalent to gcd(a,b)|c, again with the zero convention. This particular exponent predicate belongs to decidable existential addition/divisibility arithmetic and is not itself an undecidability proof. It does, however, show exactly why independent exponent parameters cannot be replaced by a finite list of constant gcd divisors.

## 6. End-of-budget conclusion and exact next barrier

Five substantive attempts have produced:

1. A density-one lattice avoidance theorem for arbitrary negative literals.
2. Decidability with at most one positive R_p-atom per DNF conjunction, without a restriction on negative atoms.
3. A positive-existential named-power multiplication formula and an exponent addition/divisibility interpretation.
4. A decision procedure for arbitrary polynomial-matrix systems with one shared power parameter, including negative literals.
5. Positive-existential elimination of all negated atomic formulas and the exact independent-power matrix normal form.

The full original existential theory is not decided or proved undecidable. The remaining task is to decide integer solvability of the multi-parameter systems (3), or to obtain an existential interpretation of an undecidable structure within them. Neither the positive natural-number theorem of Pheidas nor the ordered named-exponent theorem of Rybalov supplies that missing step. All claims above are partial structural results, with no assertion of global novelty or first resolution.
