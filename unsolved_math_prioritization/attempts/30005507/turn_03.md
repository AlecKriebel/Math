# Attempt 3: can real counts and one projective indicator force the answer?

## Exact numerical formulation

Write g(lambda) for the coset-square indicator. For each h, let r_h be the number of degree-2^h characters of D with g(lambda) nonzero, and let m_h be the number with g(lambda)=-1. The desired bijection exists if and only if, at each height h, the block has the same counts for each of -1,0,+1. Indeed, necessity is immediate and sufficiency follows by independently matching the three finite sets within every height.

Sambale's Theorem A already supplies the numbers r_h of real characters in the block; the usual nilpotent-block bijection supplies the total character counts at each height. Thus the remaining question is exactly the negative-indicator count at every height, not the mere existence of a height-preserving bijection.

A nilpotent block has one Brauer character phi. Under a Broue–Puig degree parametrization its decomposition numbers are lambda(1). Therefore its unique projective indecomposable character Phi satisfies

    epsilon(Phi) = sum_h 2^h (r_h - 2 m_h(B)).       (1)

Even if the scalar formula of Conjecture C is assumed for B, (1) is generally just one linear constraint on several negative counts.

## An exact obstruction to this shortcut

Take D=Q8 times Q8 and E=D times C2. Since t is central with t^2=1, g is the ordinary Frobenius–Schur indicator of D. The characters of Q8 have degrees 1,1,1,1,2 and indicators +1,+1,+1,+1,-1. Products therefore give:

- height 0: 16 characters, all indicator +1;
- height 1: 8 characters, all indicator -1;
- height 2: 1 character, indicator +1.

Every character is real. Exactly two elements of Q8 square to 1, so E outside D contains exactly 2 times 2 = 4 involutions. The degree-weighted sum is

    16 - 2(8) + 4 = 4.

Now consider a hypothetical sign assignment with the same degrees and real characters:

- height 0: 16 positive;
- height 1: 2 positive and 6 negative;
- height 2: 1 negative.

It also has degree-weighted sum

    16 + 2(2-6) - 4 = 4.

It satisfies the height-zero nonnegativity condition as well. But its height-by-height indicator counts differ, so no height-preserving, indicator-matching bijection to the local pattern exists.

Equivalently, after fixing height-zero signs, (1) only gives

    m_1 + 2 m_2 = 8,
    0 <= m_1 <= 8,  0 <= m_2 <= 1.

There are exactly two integer solutions: (8,0) and (6,1).

This is a counterexample to an inference from these numerical constraints. It is NOT a finite group or block realizing the incorrect assignment, and is NOT a counterexample to Sambale's conjecture. The point is that the listed information alone does not select the correct solution. Additional subsection identities can rule out a numerical assignment; those identities have not been assumed here.

## Limited sufficiency and remaining gap

If all signed counts except one height are known, equation (1) determines the last one. More generally, rank-many independent height-weighted equations would determine the vector of signed counts. This is elementary linear algebra, not a new block theorem.

The tempting stronger inference, “Conjecture C for B alone implies the desired bijection for B,” has not been established. Sambale explicitly warns that his implication from C to B is not block-by-block. Attempt 4 explains the additional local and quotient instances needed in that argument.

**Outcome:** exact proof that real-character counts, height-zero nonnegativity, and the single scalar projective formula are insufficient as numerical data. No incorrect sign assignment has been realized by a block.

Source: [Sambale](https://arxiv.org/abs/2301.13440), Theorem A, Proposition 8(iii), Conjecture C and the remark after Theorem D. The numerical obstruction above is independently derived; no novelty or priority claim is made.
