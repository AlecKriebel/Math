# Independent bounded bosonization sign check

Started 2026-11-15 04:37:39 UTC. Scope completion estimate: 10%.

This lane checks the displayed parity-bosonization conventions in the permitted
primary `source-resume-20261115/published-source/main.tex`, lines 73–88. It does
not assess the topological imports or prove the paper's infinite theorem.
Only that primary target and the root AGENTS.md were read before construction.
No native verification source, earlier/current reviews, triage, result, or
opinion files were read. No external communication or Git operation is allowed
within this lane. Parent handles publication and integration.

## Independently chosen infinite test algebra

Let H = k<e,o>, the free associative algebra on an even letter e and odd letter
o. Assign degrees 2 and 1 respectively. Its basis consists of all finite words,
including the empty word 1; neither products nor expressions are truncated.
Make both letters primitive and extend the coproduct using the Koszul product
on H tensor H. An explicit finite expression for the coproduct of a word w is
the sum over subsets L of its positions: put the letters in L into the left
word u in original order, and all other letters into v in original order.
The sign is (-1)^N, where N counts pairs r<s of odd letters with r assigned
right and s assigned left. Thus Delta(o^2)=o^2 tensor 1 + 1 tensor o^2;
the two mixed terms have opposite signs over the integers.

The counit is 1 on the empty word and 0 otherwise. If w has length n and q
odd letters, the graded antipode is

    S_H(w) = (-1)^[n+q(q-1)/2] reverse(w).

Indeed each primitive letter contributes a minus sign, and reversing q odd
letters contributes q(q-1)/2 Koszul crossings. Concatenation is associative.
The unshuffle formula is the multiplicative extension of the primitive
coproduct, and either iterated coproduct assigns each letter to one of three
ordered slots with precisely the same odd-inversion count. These observations
give independent derivations of the model formulas; the executable checks below
test their implementation and the paper's bosonization formulas on finite
domains, not a general theorem about all Hopf algebras.

## Bosonized formulas to be checked

Write (w,i) for w # g^i with i in {0,1} and |w|=q mod 2. Use

    (u,i)(v,j) = (-1)^[i|v|] (uv,i+j),
    Delta_B(w,i) = sum c(u,v) (u,|v|+i) tensor (v,i),
    epsilon_B(w,i) = epsilon_H(w),
    S_B(w,i) = (-1)^[(i+|w|)|w|] (S_H(w),i+|w|).

All group exponents are modulo two. The last displayed formula is the expanded
form of (1 # g^(i+|w|))(S_H(w) # 1), so its extra multiplication sign must be
retained. Ordinary B tensor products have no additional Koszul sign.

The intended success criterion is exact equality of finite coefficient maps
for unit, associativity, coproduct multiplicativity, coassociativity, counit,
and both antipode identities on explicitly recorded domains in F_3 and F_5.
F_2 also tests the bosonized formulas; separately, forgetting the grading on H
must make its coproduct an ordinary algebra map because all signs become +1.
Basis tests extend to linear combinations in the tested spans by linearity or
multilinearity, but bounds on separate inputs do not impose any truncation on
their outputs.

## Negative control and boundary prediction made before execution

Define Delta_bad by omitting |v| from the left group's exponent, retaining all
other formulas. For x=(o,0), Delta_bad(x*x) has only x^2 tensor 1 and
1 tensor x^2, whereas Delta_bad(x)^2 additionally has 2 x tensor x. This must
fail in F_3 and F_5, with difference coefficient -2 if left minus right is used.
In F_2 that particular multiplicativity witness disappears. It should not be
misreported as a failure to detect signs: -1=+1 in that field. Retaining the
original antipode while using Delta_bad still fails on x in every tested field,
since S_B(x)+x=(o,1)+(o,0), two distinct basis elements.

Planned bounds: all H or B words of length <=6 for unary coalgebra/antipode
identities, each input word length <=4 for binary compatibility identities,
and each input word length <=3 for associativity. No native source code will
be read at any point in this lane.

## Independent internal oracle, added after the first run

To challenge the unshuffle and closed antipode formulas by a different route,
the final checker also expands coproducts using only the generator equations

    Delta(e)=e tensor 1 + 1 tensor e,
    Delta(o)=o tensor 1 + g tensor o,
    Delta(g)=g tensor g,

and ordinary tensor multiplication. It separately expands antipodes using
S(e)=-e, S(o)=og, S(g)=g and reversal of products. Every basis word with group
exponent 0 or 1 and length <=6 is compared with each closed formula. This
oracle shares the definition of B multiplication, so it is additional finite
implementation evidence, not fully separate software verification.
