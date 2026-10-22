# Direct verification of the revised submission's colored-C4 dependency

Date2026-10-17. This is mathematical dependency checking, not a priority
classification. Root read the primary HTML version of Homs--Kuznetsova--Stolz,
arXiv2609.02382v1, Definitions2.1--2.13 and3.8, Proposition3.9, and the full
statement/proof of Proposition3.26. The numerical C4 specialization quoted
by the revised submission is correctly reported. I independently verify it
below, avoiding reliance on the general-cycle proof or a primeness theorem.

Take C4=K2,2, ordered by its two bipartition classes. All four vertex
diagonals share one color; all four cross edges have distinct colors.
The concentration space consists of K=[[alpha I2,C],[C^T,alpha I2]]. The
original report's statistic map is trace plus the four cross entries. The
2026 primary version uses twice the edge entries, an invertible coordinate
rescaling with no effect on fibers, elimination transition, or thresholds.

At one column, det(cross) is a nonzero statistic polynomial belonging to
the defining2-minor ideal. Therefore I1 is nonzero. At two columns use
X=[I2;2I2]. The statistic Jacobian has rank5, as independently checked by a
nonzero5-square minor. Submersion proves I2=0 by the same direct polynomial
vanishing argument used for K4,4. Thus the adjacent transition is atn=1.

For any real data vector z, let D=diag(1,1,-1,-1). Symmetry of the cross
block gives z^T D K z=alpha(z_L^T z_L-z_R^T z_R). If Kz=0 and the
nonzero polynomial h(z)=||z_L||^2-||z_R||^2 does not vanish, alpha=0.
A PSD matrix with every diagonal zero is zero, since each2-square principal
minor forces its off-diagonal entry zero. Hence outside h=0 there is no
nonzero PSD concentration stress. The exact PSD completion criterion yields
MLE existence. A nonzero polynomial has Gaussian probability-zero zeros,
so MLT=WMLT=1. There is no smaller positive sample count; at zero columns
trace zero cannot have a PD completion.

The rank-one data vector (2,0,0,0) has trace4 and zero cross entries,
matching I4. Thus the report's cone-intersection antecedent atn=1 holds
with an actual real rank-one PSD lift as well. The literal numerical cases
both require MLT2 and are contradicted. The Boolean intersection alternative
holds; this still does not answer the bare Boolean conjecture.

The standalone exact script checks the full Jacobian minor, symbolic stress
identity, nonzero obstruction, rank-one vanishing and PD-statistic witness.
The quantified argument is given above; sampling is not used. No claim
about when this example was first publicly recognized is made here.

Primary version read: https://arxiv.org/html/2609.02382v1 . This note is an
independent proof of its quoted C4 specialization; it does not endorse
unrelated statements elsewhere in that paper.
