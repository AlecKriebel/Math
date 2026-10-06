# Independent later-literature priority checkpoint, PR117

This checkpoint records the independent LaClair/Blanco reasoning before opening the newly communicated Takagi 2013 source. The exact PR117 candidate and source gate were read, together with the original source statement and complete empty prior report. No new priority-family report was read. The communicated existence of Takagi 2013 is recorded as a subsequent lead, not independent discovery by this family.

The candidate mathematics is valid. It is a negative answer to a universal existence question. Novelty cannot follow merely from no located earlier text naming Question 2.2 or Question 8.

## LaClair comparison

Actual primary PDFs inspected: arXiv2304.13299v1 (26 April2023), v2 (16 June2023, previously retrieved immutable body), and the open-access published2025 body, DOI10.1007/s10801-025-01439-x (15 July2025). Read the introductions, equation(8), Theorem2.12/Remark2.13, the complete Proposition3.12 and Lemma3.13 proof chain, Corollary3.14 and Remark3.15. The published proof/remark is on physical page18; its pixels were inspected.

For the triangle, the original augmented program has optimum3. LaClair equation(8) has one further full-vertex-set cap bounding total weight by2, and optimum2: a two-edge directed path attains it. Corollary3.14 implies lct(J_K3)<=2. The original Shibuta–Takagi Proposition2.1 says a singleton optimal-image fiber would force lct=the original optimum3. Thus these prior results already entail failure of that hypothesis for the very triangle ideal. This is this reviewer's deduction, not a claim that LaClair explicitly names or answers Question2.2. The difference between two polytopes alone would be insufficient; the conditional theorem and strict threshold bound provide the implication.

Remark3.15 removes all subset caps, including size-two edge caps, so its resulting polytope should not be identified verbatim with the original augmented polytope. Restoring those edge caps gives the original program (up to orientation and coordinate permutations). Both relaxed and original triangle programs have optimum3. No conclusion depends on claiming identical relaxed feasible polytopes.

## A qualifying prior ideal in Blanco–Encinas

The actual arXiv1405.3942v1, dated15 May2014, Example5.6 pp26–27, and v5 dated11 February2017, Example6.6 pp34–35, both give

I=(f x4, f x5, g x4, g x5), f=x2^2-x1*x3, g=x1^3-x3^2.

The generator order differs between versions. Their own statement reports lct(I)=17/12. The journal's metadata gives online17 March2017, volume155(2018),141–181, DOI10.1007/s00229-017-0929-4. The publisher PDF was not accessible; the Valladolid repository attempt timed out. Do not claim its journal body was inspected. The preprint witness itself already predates this research by twelve years.

The following are independent checks of that qualifying ideal, not a new candidate construction attempt. Evaluation with all variables1 annihilates all four generators and rules out every nonzero monomial. For minimality let R=k[x1,x2,x3], B=(f,g), T=k[x4,x5], J=(x4,x5). Weighted degrees(4,5,6) give deg f=10, deg g=12; the lowest degree in m_R*B is14, so B/m_R*B has dimension2. J/m_T*J has dimension2. Since I=B tensor_k J as an S=R tensor_k T module, I/m_S*I is the tensor product of those quotients and has dimension4. These four generators are minimal globally and at the homogeneous maximal ideal for the positive weighted grading.

Use the v5 generator order. The original augmented matrix has five monomial rows and four generator rows. With LP coordinates(mu1,...,mu4,nu1,...,nu4), its upper three rows are

- x1: 3(mu3+mu4)+nu1+nu2;
- x2: 2(mu1+mu2);
- x3: nu1+nu2+2(nu3+nu4).

The two further monomial rows are p1+p3 and p2+p4, where pi=mui+nui; the four bottom rows are p1,...,p4. All are bounded by1.

The dual vector(1/2,1/2,1/2,0,0,0,0,0,0) covers every column; the two mu3/mu4 columns have strictly positive dual slack1/2. Its value is3/2. The feasible vector(1/2,0,0,0,1/2,1/2,0,0) attains3/2. Complementary slackness therefore forces every optimum to have mu3=mu4=nu3=nu4=0, mu1+mu2=1/2, nu1+nu2=1. The complete rational optimal face is the rectangle

z(a,p)=(a,1/2-a,0,0,p-a,1-p+a,0,0),
0<=a<=1/2, 1/2<=p<=1, a,p rational.

Its augmented image is(1,1,1,p,3/2-p,p,3/2-p,0,0), independent of a. Every optimizer has a distinct rational optimizer with the same image, obtained by replacing a by0 if a is nonzero, and by1/2 otherwise. This gives a full direct failure of the original assumption for an ideal already printed in2014, independently of trusting the reported threshold calculation.

The sign-changed ideal a2 in those examples is not the relevant witness: x4 times its second degree-three generator minus x5 times its first yields2*x1*x3*x4*x5, a monomial in characteristic0. The unmodified a1 above satisfies the no-monomial requirement.

The full augmented matrix has rank6 (four bottom rows plus rank2 of exponent differences). An initial diagnostic expected7; the false expectation was caught and preserved in CONTROL_EXPECTATION_REPAIR.json and the failed source. The rectangle calculation did not change. The final effective diagnostic normal run passed1175 explicit guards; optimized and deliberate-false runs are pending at this checkpoint.

## Independent conclusion and exact gaps

The later primary literature supplies concrete prior consequences of the negative answer, including the same prime triangle ideal by2023 and another qualifying printed ideal by2014. This family cannot support a claim that the broad original problem was still open and newly resolved here. The candidate is a concise elementary presentation and its exact optimal segment is useful, but substantive new mathematics beyond the prior obstruction is not established.

No located text in these inspected sources explicitly labels the answer to the numbered question. This absence is not evidence of novelty. The theoretical threshold algorithm and all examples in Blanco–Encinas were not re-proved; our elementary augmented-fiber proof avoids relying on them. A distinct later2026 diagonal-F-threshold lead was found, but its quotient-ring invariant is not yet inspected and is not evidence for the original LP. The newly communicated Takagi2013 exact-prior source has not been opened at this independence checkpoint.

No original proof/source cache, PR, native assessment, global state, Git reference, index, or publication service was mutated. New central candidate proof-search turns:0. Family investigation estimate85%; novel-open-problem publication clearance:no.
