# Independent exact reconstruction

Recorded 2026-10-05T23:16:55.580377+00:00, before reading round-1 report or earlier mathematical reviews. I read the public manuscript and programs and selected primary HT v2/Ohtsuki/GP passages in place. The reasoning below checks the asserted specialization rather than searching for a new central mechanism.

Let a root-lattice class be sum a_j(e_j-e_{j+1}), a_j in {0,...,4}. This basis is unimodular as a basis of Y; it identifies Y/5Y with (Z/5)^4 and fixes the count625. A character has factors sum_a exp(2pi i a(v_j-v_{j+1})/5). Each is5 or0. The annihilator is v/5 in Y*=X. Equivalently its five coordinates have the same residue; imposing residue0 would wrongly replace5X by5Y.

For q nonzero mod5, each residue c fixes one permutation through w rho_i congruent q rho_i-c. All five coordinates of rho are distinct mod5, hence each c fixes a unique permutation and there are exactly five. For q1 these are cyclic shifts, each even because a5-cycle has sign+1. For q2 the residue-multiplication permutation has sign-1 (the nonzero residues form a4-cycle); the cyclic shifts keep that sign. Their dots with rho respectively are (10,0,-5,-5,0) and (5,5,-5,0,-5), in the displayed order of the manuscript. Thus with t=exp(pi i/5), B1=t^-2+2+2t and B2=-(1+2t^-1+2t).

Put h=t+t^-1=(1+sqrt5)/2 in the specified positive embedding. Its square is h+1. Hence t²+t^-2=h²-2=(sqrt5-1)/2 and t³+t^-3=h³-3h=1-h, the negative of the former. Multiplying B1 by its conjugate gives9+4h+2(t²+t^-2)+2(t³+t^-3)=11+2sqrt5. B2=-(1+2h)=-(2+sqrt5), giving9+4sqrt5.

In HT Theorem5.1 for A4, m=1,kappa=r=10, rank4, positive roots10, rho norm²10, vol(Y)=sqrt5. The prefactor is i^10 exp(pi i S(q/p))/((10p)² sqrt5); no p–r coprimality is assumed. At p5 the inner quadratic phase is exp(2pi i q norm²)=1 and the character sum625 collapses the numerator to625 Bq. At p1 its numerator is A, with Weyl denominator A=-P. P=product_{j=1..4} (2sin(pi j/10))^(5-j)=5sqrt5-10>0. Its square is225-100sqrt5; multiplying by its conjugate algebraic expression225+100sqrt5 gives625. Therefore S00=-A/(100sqrt5)>0 and

|tau(L(5,q))/tau(S3)|² =625 |Bq|²/(225-100sqrt5)=(225+100sqrt5)|Bq|².

The products are (225+100sqrt5)(11+2sqrt5)=3475+1550sqrt5 and (225+100sqrt5)(9+4sqrt5)=4025+1800sqrt5. Difference550+250sqrt5>0; neither can vanish. s²=(9-4sqrt5)/2000 and D=1/s=100+40sqrt5 follow algebraically.

Full-weight route: each code vector X=5(lambda+rho); its exponent z100^(-2 dot(X,Y)/5) equals exp(-2pi i dot(lambda+rho,mu+rho)/10). Its theta exponent z100^((norm²X-norm²X0)/5) equals exp(pi i (norm²(lambda+rho)-10)/10). Thus the stored Weyl sum N gives physical S=-N/(100sqrt5). For code word numerators U and V with respectively two and three S factors, normalization gives |U|²/(50000|N00|²) and |V|²/(50000²|N00|²). The sign from three factors disappears in the norm. There is exactly one division by physical S00 in both words, never one per S factor. Code difference50000|U|²-|V|² compares these common-denominator normalized squares. It is an exact cyclotomic comparison, not a category axiom proof.

The finite label set consists of all four nonnegative labels sum<=5. Charge sum j*a_j mod5 is unrestricted. The ordinary unitary phases, central charge12, T=-theta and anomaly-1 cannot affect squared moduli. Positive surgery fractions5=[5],5/2=[3,2] correspond to the negative-surgery HT lens convention after orientation reversal. Continued-fraction reversal yields q inverse; q2 inverse3 and q1 inverse1. All such controls preserve the two respective moduli. The longest Weyl permutation has sign+1, takes rho to-rho, and gives q sign conjugation together with the odd Dedekind symbol.

For the unknot exterior, longitude is nullhomotopic and meridian generatesZ. Filling slope-5/q adds mu^5=1, so both fundamental groups areZ5; no further topological equivalence is needed.

Bounded conclusion if executions and package checks succeed: the stated finite ordinary fullSU5 counterexample is correct conditional on the explicitly imported established foundations. No priority conclusion follows, especially while directly relevant Kuriya hypotheses remain unread.

Completion estimate toward assigned bounded review:30%.
