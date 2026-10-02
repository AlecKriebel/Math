# Source resolution: sequence defined on multisets

Problem 3048 / OPG-37226 is **already solved in the literature**. Recommended disposition: already_solved, 0/5 proof-attempt turns. This is source verification and formulation alignment, not a new proof attempt or novelty claim. Independent source review remains pending.

## Published resolution

Shalom Eliahou and Martin J. Erickson, *Mutually describing multisets and integer partitions*, Discrete Mathematics 313(4) (2013), 422–433, DOI https://doi.org/10.1016/j.disc.2012.11.014. The publisher's abstract states eventual periodicity for nonnegative finite multisets and classifies the cycles, all of length at most three. The author's institutional publication list confirms the citation. The full 2013 article was not retrieved; no full proof audit of it is claimed.

An accessible full primary treatment is Onno M. Cain and Sela T. Enin, *Inventory Loops (i.e. Counting Sequences) have Pre-period 2 max S1 + 60*, https://arxiv.org/abs/2004.00209v1 (2020). Section 3 defines the exact positive-integer multiset operator. Corollary 4.5.1 gives eventual periodicity; Theorems 5.3 and 5.5 and Corollary 5.5.1 give period at most three. The definitions and Sections 4–5 were read; the cycle corollary was visually checked. The later quantitative preperiod analysis is not needed for the target and is not independently certified here.

This supplies verifiable literature beyond the source page's unlinked July 2011 solution comment. Historical priority is not being adjudicated; the 2020 bibliography also credits earlier counting-sequence work.

## Exact alignment with the array operation

For a two-row array T, let pi(T) be the multiset of its entries, counting each cell once. In particular, the second row is not interpreted as weights expanding the first row. Let H(M) be the array whose top row is the distinct elements of M in increasing order and whose bottom row lists their multiplicities. Let

d(M) = support(M) ⊎ { multiplicity_M(x) : x in support(M) },

where each support element is included once and the braces on multiplicities denote a multiset, so equal multiplicities are repeated. This is the operator in the cited literature.

The original array transition is F(T)=H(pi(T)), and flattening gives

pi(F(T)) = pi(H(pi(T))) = d(pi(T)).

Therefore, for any allowed initial array T_0, its flattened orbit M_t=pi(T_t) follows M_(t+1)=d(M_t). Every M_t is a finite multiset of positive integers. The established theorem makes M_t eventually periodic with period q∈{1,2,3}. Since T_(t+1)=H(M_t), the array orbit then repeats with period dividing q, which is also 1, 2 or 3. This covers the entire source request. If empty arrays are allowed by convention, the empty array is an additional fixed point.

The operation treats a large integer as one atomic entry, not as decimal digits. Sorting occurs only in the top row; row order and initially arbitrary bottom-row values cause no obstruction to the argument. No bound on the original labels, multiplicities or number of columns is assumed.

## Verification limits

The accompanying finite checks verify the translation, the source's displayed orbit, representative periods and large atomic labels. They do not prove eventual periodicity for every input. That conclusion is credited to the cited literature. The packet does not claim independent certification of every source figure, external program, cycle-family computation or quantitative preperiod bound.
