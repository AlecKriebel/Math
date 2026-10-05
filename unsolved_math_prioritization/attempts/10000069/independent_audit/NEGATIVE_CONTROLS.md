# Rejected shortcuts and audit negatives

The independent exact program rejects ten finite or algebraic shortcuts. These are controls, not ten research attempts.

1. Mean-only closure: at p=3/4, deterministic X=1 and equally weighted X in {1/2,3/2} both have mean one, but output means are 7/4 and 27/16.
2. Reverse block/Jensen direction: m_1^2-m_2=p(1-p)^2, equal to 3/64 at p=3/4.
3. Reciprocal second-moment cap: X=1 has normalized second moment one, exceeding 2p-1 for every interior p.
4. Constant eigenprofile: T(1) has two distinct atoms whenever 0<p<1.
5. Maximum substituted for minimum: for a uniform {0,2} input, the expected minimum is 1/2 and maximum is 3/2.
6. Resistance substituted for distance: parallel unit edges have distance one and resistance one half.
7. Compactness from mean alone: f_n=n on (0,1/n), zero elsewhere, has mean one but no mean-one L1 limit; its second moment diverges.
8. Incorrect cone perturbation: T(f)+epsilon*1 fails positive homogeneity off the mean-one slice. The required term is epsilon*M(f)*1.
9. Dropping monotonicity of the quantile profile: f(u)=2u gives AS-CM=-2/9, so the load-bearing sign need not hold for increasing functions.
10. Missing cross term in the series second moment: at p=3/4 and X=1, the true second moment is 13/4; omitting 2p*(EX)^2 incorrectly gives 7/4.

Two additional analytical safeguards are outside the finite program:

- A positive essential lower bound for perturbed eigenprofiles cannot be assumed to persist at epsilon=0. If q>0, the output essential infimum equals the input one; an eigenprofile with rho>1 therefore has essential infimum zero.
- Replacing an upper bound on a second moment by equality is invalid. This is the local reconstruction erratum E1 and must not be silently accepted.

The numerical test coverage does not certify Schauder, Helly/Vitali, universal Jensen domination, variational equality, all-p asymptotics, the original catalogue wording, historical priority, or peer review. Those are separately reviewed or explicitly excluded.
