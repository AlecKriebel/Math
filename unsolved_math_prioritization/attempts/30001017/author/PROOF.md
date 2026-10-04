# First Voronoi intersection numbers: partial results and exact obstructions

Problem 30001017 / OWR-2049-004. Prepared 2026-10-04.

## 1. Exact target and disposition

Let X_g = A_g^Perf = A_g^F be the first Voronoi (perfect cone) compactification over C, let G=g(g+1)/2, let L be the first Chern class of the determinant of the Hodge bundle, and let D be the boundary divisor. For 0 <= n <= G set

    I(g,n) = degree_X_g L^n D^(G-n).

The conjecture asks whether I(g,n)=0 whenever n is not triangular: n != k(k+1)/2 for every integer 0 <= k <= g. This is exactly the conjecture on printed page 2187 of the Oberwolfach report [S1], and Conjecture 1.2 of [S2]. We use rational Chow groups and the moduli-stack normalization of [S2]. The question is about all genera, not merely a finite table.

This document does not prove or disprove the conjecture. It supplies complete proofs of limited lemmas, a source-normalized account of the established range, an exact arithmetic reproduction within that range, and reductions identifying what remains. The strongest global vanishing range used below is an external theorem of Erdenberger, Grushevsky, and Hulek (EGH), not a new theorem here. No novelty is claimed for the elementary lemmas.

## 2. Conventions that affect computations

Write H_g = degree L^G and a_N^(g)=I(g,G-N). On the stack, [S2, Theorem 1.1] gives

    H_g = (-1)^G 2^(-g) G! product_{k=1}^g zeta(1-2k)/(2k-1)!!.

We take H_0=1. Since zeta(1-2k)=-B_(2k)/(2k), with standard Bernoulli numbers, this is an exactly computable rational number. In particular

    H_1=1/24, H_2=1/2880, H_3=1/181440,
    H_4=1/1814400, H_5=13/16329600.

The boundary of the rank-one partial compactification is a universal Kummer family. If j:X_(g-1)->D is the universal abelian-family cover, its degree is 2, so j_*[X_(g-1)]=2[D]. For the symmetric theta class theta rigidified along the zero section,

    j^*D=-2 theta.

The unnormalized universal theta class theta' satisfies theta'=theta+p^*L/2, so the equivalent formula is j^*D=-2 theta'+p^*L. One must not combine the latter formula with the isogeny weight of the former theta class.

For coarse-space divisor classes whose pullbacks are L and D, stack integration is one half of coarse integration, because the generic stabilizer has order 2. In particular the genus-four numbers 1/907200, -1/3780 and -1759/1680 in [S1] and [S3] are coarse numbers; the corresponding stack numbers are 1/1814400, -1/7560 and -1759/3360. This changes coefficients, never zero versus nonzero. One should check the pullback of each divisor rather than applying an unqualified conversion to differently defined boundaries on another compactification.

## 3. Approach 1: Satake support and localization

Let pi:X_g->S_g=A_g^Sat be the Satake contraction, ell its rational Hodge class, and beta_r=pi^(-1)(A_(g-r)^Sat). Thus L=pi^*ell and dim A_(g-r)^Sat=T_(g-r), where T_k=k(k+1)/2.

### Lemma 3.1: support cutoff

If a cycle alpha is supported on beta_r and n>T_(g-r), then L^n cap alpha=0.

Proof. A positive multiple of ell is the class of a globally generated ample line bundle. The intersection of n sufficiently general hyperplanes with the closed subvariety A_(g-r)^Sat is empty when n exceeds its dimension. Pulling their classes back to beta_r gives zero. Rational coefficients remove the chosen positive multiple. The same reasoning applies on level covers and descends to the stack. This proves the claimed operational action on every cycle supported on beta_r. QED.

As D is supported on beta_1, this proves a_N^(g)=0 for 1<=N<=g-1. More generally, if two cycle calculations agree off beta_r, their difference is supported on beta_r by Chow localization, and multiplication by L^n kills that difference when n>T_(g-r).

This explains exactly why calculations on X_g minus beta_3 apply when N<3g-3: G-N>T_(g-3). It does not justify equality at N=3g-3 or beyond.

### Failure of a support-only induction

A cycle of dimension n can live properly inside a Satake stratum of dimension larger than n. The absence of a Satake stratum of dimension exactly n does not imply that its n-dimensional Chow group is zero. For instance, the projective plane has no 1-dimensional stratum in the trivial one-stratum partition but does have nonzero curve classes. This logical obstruction remains even if every boundary component maps to a union of the permitted Satake strata.

In the first unresolved genus-five case n=2, beta_3 maps to A_2^Sat of dimension 3. Lemma 3.1 therefore cannot kill its contribution. Support on beta_4 would suffice, since A_1^Sat has dimension 1, but that stronger support assertion is not established here.

## 4. Approach 2: multiplication weights on abelian powers

Let p:B->S be a principally polarized abelian scheme of relative dimension h, on a base or level cover where the indicated rational divisor classes exist. Let theta be its symmetric rigidified polarization class. For a positive integer m, [m]^*theta=m^2 theta and [m] is finite flat of degree m^(2h).

### Lemma 4.1: normalized theta pushforward

For d != h, p_*(theta^d)=0. For d=h, p_*(theta^h)=h![S].

Proof. The equality p o [m]=p and the finite-flat identity [m]_*[m]^*=m^(2h) give

    m^(2d) p_*(theta^d) = p_*[m]^*(theta^d)
                        = p_*[m]_*[m]^*(theta^d)
                        = m^(2h) p_*(theta^d).

Choose m=2 and use rational coefficients when d!=h. In degree h the fiber has polarization degree theta^h=h!, yielding the stated constant. QED.

Here the middle expression is shorthand for pushforwards with identical source/target B: p_*[m]_*beta=p_*beta. It is not an assertion that [m]_* acts trivially on Chow(B).

Combining this lemma with j_*[X_(g-1)]=2D, j^*D=-2theta, and localization away from beta_2 gives, for g<=N<=2g-2,

    a_N^(g) = 0 for N>g,
    a_g^(g) = (1/2)(-2)^(g-1)(g-1)! H_(g-1).

Together with Lemma 3.1 this recovers all required zeros for 1<=N<=2g-2. Intersections on the nonproper partial family are understood after choosing the Hodge hyperplanes avoiding the deleted Satake stratum, or by the localization argument, not by inventing an absolute degree map for an arbitrary nonproper stack.

### Lemma 4.2: multigraded version

On B^r over S, let theta_i be the rigidified theta class of the i-th factor and P_ij the normalized Poincare class for factors i,j, with the sign fixed by addition^*theta=theta_i+theta_j+P_ij. Put

    alpha = product_i theta_i^(a_i) product_(i<j) P_ij^(b_ij).

Then p_*(alpha)=0 unless, for every i,

    2 a_i + sum_(j!=i) b_ij = 2h.                     (W)

Proof. Multiply the i-th abelian factor by m and leave the others fixed. The map has degree m^(2h); theta_i acquires factor m^2, P_ij acquires factor m, and all remaining classes are unchanged. Apply the proof of Lemma 4.1 separately to each factor. QED.

Adding (W) shows that a surviving pure monomial has total divisor degree rh. Consequently its pushforward has codimension zero on the base. For a connected base the coefficient is its fiber intersection number.

These fiber numbers have the generating polynomial

    p_* exp(sum_i s_i theta_i + sum_(i<j) u_ij P_ij)
       = det(M)^h [S],

where M has diagonal entries s_i and off-diagonal entries u_ij. Equality refers to the pushforward of the formal exponential in rational Chow groups. To verify its coefficients, write a symplectic basis for each of the h polarization planes of the abelian variety. On one plane the top exterior coefficient is det(M); the h planes multiply, giving det(M)^h. The polarization normalization fixes the sign by theta_i^h=h!.

For r=2 this says

    p_*(theta_1^(h-k) theta_2^(h-k) P^(2k))
      = (-1)^k h! (2k)! (h-k)! / k!,

for 0<=k<=h, and every other pure monomial pushes to zero. This agrees with [S2, Theorem 7.1].

### Why this does not prove the compactified conjecture

The argument controls abelian schemes, not arbitrary semiabelic compactifications. Boundary self-intersections and singular-fiber Todd corrections need not remain pure expressions with the same multiplication weights. A base twist already breaks the naive conclusion: for h=1,

    p_*((theta+c p^*ell)^2)=2c ell.

In fact p_*((theta+c p^*ell)^d)=binomial(d,h)h! c^(d-h)ell^(d-h) for d>=h. The cancellation in -2theta'+L is essential.

There is also no justification for assuming multiplication extends as a finite-flat self-map of the same degree across a fixed degeneration. On the multiplicative group, the map z->z^m has degree m, whereas on a smooth elliptic curve multiplication has degree m^2. Thus extending the argument to a compactified degenerating family requires new geometry, not merely reusing the smooth-family equality.

## 5. Approach 3: corank-two geometry and exact finite sums

[S2, Theorem 1.1] proves that for N<3g-3 the only possible nonzero exponents are N=0,g,2g-1. Equivalently, the conjecture holds for n>T_(g-3). The third number is a sum of contributions from the one-, two-, and three-boundary-component loci in the partial compactification. We do not claim to reprove its singular-fiber GRR calculation. We independently implement the finite arithmetic formulas and their normalizations.

Let h=g-2, N=2g-1, and for positive a,b with a+b<=N define

    C_g(a,b)=(-1)^(a+b+g) h! sum_{i=0}^{min(a-1,b-1,h)}
      (-4)^i (a-1)!(b-1)!(2h-2i)!
      / [i!(a-1-i)!(b-1-i)!(h-i)!].

The finite range avoids negative factorials. The two contributions with no GRR coefficient extraction are

    II = H_h/4 sum_{a=1}^{N-1} binomial(N,a) C_g(a,N-a),
    III = H_h/12 sum_{a,b,c>=1; a+b+c=N}
                      N!/(a!b!c!) C_g(a,b).

II agrees exactly with the separately printed closed expression in [S2, Theorem 8.3]:

    II = -H_h/[64(2g-1)]
         [2^(4g)(g-1)!(g-2)!+32(-1)^g(2g-3)!].

For I, the implementation follows the finite double sum in the proof on preprint page 33. Its coefficients, for positive n and even k, are

    b_(n,k-n)=(-1)^(n+1) B_k/k!,

and zero for odd k. This is the Todd expansion in [S2, Lemma 9.3], expressed using standard even-index Bernoulli numbers. See verify.py for the full rational finite sum and an independently evaluated simplified expression.

The checks recover I, II, III, and their sum for g=2,3,4,5. In particular at g=5:

    I=-1/1296, II=-3637/2520, III=1063/7560,
    a_9^(5)=-59123/45360.

The g=2 calculation is a numerical consistency check with the known low-genus table; N=3 is not within the strict theorem range N<3g-3 in that genus.

### Preprint-specific warnings

The available arXiv document is version 1, submitted in 2007, even though its automatically typeset title-page date says August 5, 2021. It is not evidence of a 2021 mathematical revision.

Its printed simplified Proposition 9.4 disagrees with the preceding unsimplified finite double sum: the correction term requires an additional multiplicative factor 2^(2g-4)(2g-2)! to reproduce that finite sum. In genus 3 the printed simplified formula gives I=-119/1920; the preceding finite sum and its own table give I=-1/80. The checker retains this discrepancy rather than silently treating all displayed formulas as interchangeable.

Further, its genus-6 table gives II=-23837/315 and III=1639/315, whereas the finite formulas with its stated stack H_4=1/1814400 give -23837/630 and 1639/630. The table's values correspond to doubling H_4 in those terms. In genus 7 the finite III sum gives 203645/189, different from the listed 17594928013/16329600. These are arithmetic comparisons of the retrieved preprint only. The journal PDF was unavailable to this investigation; this is not a claim that the journal article contains the same discrepancies. Values for g>=6 in CONTROL_RESULTS are formula evaluations pending source reconciliation, not promoted as newly established geometric intersection numbers.

None of these discrepancies supplies a nontriangular nonzero intersection or refutes the conjecture.

## 6. Approach 4: birational comparison and the first missing case

### Lemma 6.1: modifications over a small base locus

Let f:X'->X be a proper birational morphism of proper integral spaces of dimension G, p:X->S a proper morphism, and H=p^*ell. Suppose D,D' are rational Cartier divisors and E=D'-f^*D is supported on a closed set Z with dim(p f(Z))<=s. Then for n>s and N=G-n,

    degree_(X') (f^*H)^n (D')^N = degree_X H^n D^N.

The same statement holds for the corresponding rational stack intersection theory.

Proof. Expand (f^*D+E)^N-(f^*D)^N. Every term contains E and is represented by a cycle supported on Z. The n-fold pullback of ell acts as zero on Z by the hyperplane proof of Lemma 3.1. All terms of the difference vanish after multiplication by (f^*H)^n. The remaining term pushes to H^nD^N because f_*[X']=[X]. QED.

The perfect-cone and second-Voronoi fans agree in ranks at most 3, as recalled in [S2, Section 11]. Choose a common toroidal refinement agreeing there. The difference between the pullbacks of their rank-one-boundary closures is supported over A_(g-4)^Sat. Applying the lemma to both compactifications shows that their L^n D^(G-n) numbers agree for n>T_(g-4), whenever g>=4 and the respective D is the specified rational Cartier boundary class.

In genus 4 this also follows explicitly from [S3]: D_Vor=pi^*D_Perf-4E with E contracted to a point, so every intersection containing L and a positive power of E vanishes.

In genus 5 the particular unknown number L^2D^13 is unchanged by any such modification over A_1^Sat, since 2>T_1=1. In particular it can be computed on a common smooth toroidal refinement using any rational Cartier divisor that agrees with the perfect-cone pullback outside that locus. Interpreting this as the usual intersection of the boundary on another possibly singular model requires that model to carry the specified rational Cartier boundary class; we do not assume that without checking. This does not evaluate the number. The rank-three contribution remains and is not removed by switching to a model differing only over deeper strata.

## 7. Approach 5: eliminate known coefficients in genus five

The known range yields an especially precise residual problem. For g>=3 the still-uncovered required-zero Hodge exponents are exactly

    { n : 0<=n<=T_(g-3), n is not triangular }.

There are (g-3)(g-4)/2 such exponents. This follows by subtracting the g-2 triangular numbers 0,T_1,...,T_(g-3) from the T_(g-3)+1 integers in the interval. Consequently every required zero for g<=4 is already covered, and for g=5 only n=2 is missing from this theorem.

Set P(t)=degree_(X_5)(L+tD)^15 and write a_N=a_N^(5). Its known part is

    K(t)=H_5 + binomial(15,5)a_5 t^5 + binomial(15,9)a_9 t^9,
    H_5=13/16329600, a_5=1/9450, a_9=-59123/45360.

The established vanishing range gives exactly

    R(t):=(P(t)-K(t))/t^12
         =455 a_12 +105 a_13 t+15 a_14 t^2+a_15 t^3.

The quotient is a polynomial; its definition at t=0 is by extension. Therefore

    a_13=[R(-2)-8R(-1)+8R(1)-R(2)]/1260.            (F)

Proof. The indicated numerator vanishes on 1,t^2,t^3 and equals 12 on t; the coefficient of t in R is 105a_13. QED.

Thus an exact computation of four total-divisor intersection numbers at these arguments would determine the entire missing vanishing, with the three other unknown coefficients eliminated. The formula is an extraction identity, not an evaluation algorithm for those unknown geometric inputs. The divisor L+tD need not be ample to define its intersection polynomial; asymptotic h^0 estimates cannot be substituted without proving the necessary positivity and error control.

As a falsification test of an overly optimistic algebraic argument, give a_13 an arbitrary rational value and leave a_12,a_14,a_15 arbitrary. Every already-known coefficient constraint remains satisfied. In particular both a_13=0 and a_13=1 fit that formal data. This is a countermodel only to deduction from those coefficients alone, not a geometric counterexample.

## 8. Exact remaining gap and stopping point

The five approaches do not determine the contribution over A_2^Sat to L^2D^13 in genus 5, much less every deeper-boundary contribution in arbitrary genus. The multigrading calculation would be useful if one had a compatible global boundary formula whose pushforwards introduced no unaccounted positive-codimension classes on the Satake base. That assertion has not been proved and is stronger than the computations presented here. A complete proof must control those compactified boundary corrections; a counterexample must compute an actual nontriangular nonzero number in the stated normalization.

All five substantive approaches are closed as partial/blocked. Further work here is limited to independent validation of the frozen packet, rather than a sixth search attempt.

## References

[S1] Samuel Grushevsky, joint with Cord Erdenberger and Klaus Hulek, “Intersection numbers of divisors on A_g,” in Komplexe Analysis, Oberwolfach Report 38/2008, printed pp. 2186-2188. Report DOI: https://doi.org/10.4171/owr/2008/38 . Official report: https://ems.press/content/serial-article-files/46182?nt=1 .

[S2] C. Erdenberger, S. Grushevsky, K. Hulek, “Some intersection numbers of divisors on toroidal compactifications of A_g.” arXiv:0707.1274v1, https://arxiv.org/abs/0707.1274 . Published in Journal of Algebraic Geometry 19 (2010), 99-132, DOI https://doi.org/10.1090/S1056-3911-09-00512-8 . The author publication list confirms the journal pagination: https://www.math.stonybrook.edu/~sam/papers.html .

[S3] C. Erdenberger, S. Grushevsky, K. Hulek, “Intersection theory of toroidal compactifications of A_4.” https://arxiv.org/abs/math/0503017 . Bulletin of the London Mathematical Society 38 (2006), 396-400, DOI https://doi.org/10.1112/S0024609305018394 .

[S4] E. Clader, S. Grushevsky, F. Janda, D. Zakharov, “Powers of the theta divisor and relations in the tautological ring.” https://arxiv.org/abs/1605.05425v2 . IMRN 2018 (24), 7725-7754. Section 2 distinguishes the universal abelian theta identity from the considerably more complicated compactified semiabelian extension. It does not supply a full solution of the present target.
