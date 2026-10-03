# Verification guide for the prior sharpness construction

This is a source reconstruction of Franz's existing proof, restricted to the cases needed for the OWR question. The general classification of all length vectors is unnecessary. We use rational coefficients throughout.

## 1. Geometry and source hypotheses

For odd r=2m+1, set X={sum u_j=0} inside (S³)^r, with S³={(u,z) in C²: |u|²+|z|²=1}. The sum map to C is a submersion on its zero set. To see this directly, if some z_j is nonzero then the tangent u_j variation is arbitrary complex and its radial correction can be made through z_j. If every z_j vanishes, a failure of surjectivity would give a nonzero real linear functional on C annihilating each tangent line i u_j R. All u_j would then be ±v for one unit v. An odd number of these cannot sum to zero. Thus X is a closed regular level, compact and oriented, of dimension 3r−2.

It is connected: scale all u_j continuously to zero and enlarge the moduli of the z_j to maintain the sphere equations, retaining each phase when defined and choosing any phase when its initial coordinate is zero. The endpoint lies in {u=0}, a connected torus. This gives a path for each initial point, not an asserted globally continuous deformation retraction.

At u=0 and all z_j=1 the stabilizer is trivial, so the r-dimensional torus action is effective and really has full-dimensional orbits. All stabilizers are coordinate subtori, hence there are finitely many. The orbit skeletons are finite unions of real algebraic subsets and are semialgebraic, locally contractible, with finite-dimensional cohomology. The examples therefore satisfy the locally compact, second-countable, finite-dimensional, finite-orbit-type and cohomological conditions in Allday–Franz–Puppe Sections3.1,3.2 and Assumption4.1. Compact connected orientability supplies rational Poincaré duality.

For even r=2m+2, ell=(0,1,...,1) gives exactly S³×X(1,...,1) for 2m+1 positive entries. The same conclusions follow by products. The zero length is permitted by Franz's genericity condition: the total positive length is odd, so no subset has half the total. If desired, replacing that zero by any epsilon in (0,1) stays in the same generic chamber, and Lemma2.1(3) identifies the equivariant diffeomorphism type. No positivity restriction is required by the OWR question.

## 2. Equilateral Morse input and literal presentation cautions

The needed geometric input is Franz's Lemmas3.1–3.2 in the equal-length case. Put V=S³, and consider f=-|sum u_j|² on V^r minus X. Critical manifolds P_J are circles, indexed by |J|<=m, with u_j=-v on J and u_j=v outside J, z=0. Their index is 3|J|. The negative normal directions are supplied by the submanifolds W_J, while V_J and W_J provide the two homology classes associated with each critical circle.

For clarity, the index can be checked without relying on sign wording in the source. Write j=|J|, s_i=-1 on J and +1 elsewhere, q=r−2j>0. Near v=1 use

    u_i=s_i exp(i theta_i) sqrt(1−|w_i|²), z_i=w_i.

The quadratic part of f is

    q sum_i s_i(theta_i²+|w_i|²) − (sum_i s_i theta_i)².

Its w-block has 2j negative directions. Its theta-block has one zero direction (the critical circle), j negative directions and r−j−1 positive ones. Indeed, split off the common theta direction; on sum s_i theta_i=0 the form is q sum s_i theta_i², with that signature. Hence the total index is 3j, and the kernel is exactly tangent to P_J. On the tangent space to W_J transverse to P_J this quadratic form is negative definite.

The printed derivative in equation(3.10) has the opposite sign from direct differentiation of f, and its minimum/maximum wording is not used here. Also, the unweighted function in equation(3.9) is used only for equal lengths. This restricted verification avoids extrapolating that display to arbitrary ell. It does not dispute or require the general classification theorem.

The perfection argument in Lemma3.2 then applies as written: conjugating z_i supplies (Z/2)^r characters on the negative bundles. Distinct J give different characters, so boundary maps between successive critical levels vanish over Q. Thus H_*(V^r minus X;Q) has the stated V_J,W_J basis. This is a verification of the credited Morse argument, not an independent new construction.

## 3. The equivariant map and Koszul modules

Franz's Lemmas4.4–4.5 and Proposition4.6 give free equivariant homology modules on those geometric classes and the inclusion map

    V_J -> V_J,
    W_J -> sum_{i notin J} (-1)^{(J,i)} t_i V_{J union i}.

The coefficient t_i is the equivariant Euler class of the normal complex line to the fixed S¹ in S³; the shuffle sign comes from the ordered product orientations. The resulting differential is exterior multiplication by sum t_i e_i.

In the equilateral case, J is short precisely when |J|<=m. The identity part on V_J cancels. The only nontrivial middle map is the Koszul map from exterior degree m to m+1. Let K_j be the j-th syzygy of Q=R/(t_1,...,t_r), with grading shifts suppressed. Exactness and self-duality of the Koszul resolution give

    coker(iota)=free summands ⊕ K_m,
    ker(iota)=free summands ⊕ K_{m+2}.                    (A)

The cohomology lies in the exact sequence

    0 -> coker(iota)[3r] -> H_T^*(X)
         -> ker(iota)[3r−1] -> 0.                        (B)

These are precisely the calculation behind corrected Proposition5.1. Omitting the shifts in (A) does not change syzygy order.

For an additional check of the corrected grading, the two nonfree summands in Proposition5.1 specialize at a=b=1 to K_m[3m] and K_{m+2}[3m+3]. The free summands have shifts 3|J| for |J|<m and 3|J|−2 for |J|>m+1. The odd difference between the two Koszul shifts removes their graded extension. The only possible extension of K_{m+2} by a free summand occurs when m=2, r=5; the relevant free target shifts are 10 and 13, differing from 9 by 1 and 4, rather than the exceptional difference 2. Allday–Franz–Puppe Lemma2.4 therefore also verifies the split description used by Franz.

One can recover the order from (A)–(B) without any grading issue. The Koszul resolution is exact because the variables form a regular sequence, and is minimal at the homogeneous maximal ideal. Thus K_j has projective dimension r−j and depth j there, and syzygy order exactly j. The class of m-th syzygies is closed under extensions, by the localized depth characterization. In (B), the left term has depth m and the right term depth at least m+2 at the maximal ideal. The depth lemma gives depth m for H_T^*(X), so it is an m-th syzygy but not an (m+1)-st. In particular it is not free. This is the same order conclusion as Proposition5.1; it is not a substitute general classification.

## 4. Even-rank extension

For the additional sphere factor let S¹ act on S³ by multiplying z and fixing u. Its Borel construction is the sphere bundle of the complex rank-two bundle 1⊕L over BS¹. Its Euler class is zero. The Gysin sequence consequently expresses H_{S¹}^*(S³;Q) as the free Q[t]-module Q[t]⊕Q[t][3].

The equivariant Künneth formula gives a direct sum of two shifts of H_{T'}^*(X_odd)⊗Q[t]. Polynomial extension preserves the syzygy order: tensoring a free resolution proves the lower bound, and a regular sequence witnessing failure at the next order remains nonregular after this faithful extension. This is Franz's Lemma5.2, used in Corollary5.3. Therefore the even example has the same exact order m, now with rank r=2m+2.

For all r>=5, m=floor((r−1)/2)<r, and the examples realize exactly the requested nonfree maximum.

## 5. Checked dependencies and limits

Read in full for the relevant chain: Franz's construction and Lemma2.1; equilateral Lemmas3.1–3.2; Lemmas4.4–4.5 and Proposition4.6; Koszul discussion, corrected Proposition5.1, Lemma5.2 and Corollary5.3. The standard equivariant duality and module criteria used there are credited established inputs. Allday–Franz–Puppe Lemma2.4, Corollary1.4 and the proof of Proposition5.12 were checked directly.

Franz–Huang Theorem1.2 and its coefficient convention give a later corroboration, but the full general-length proof is not needed or claimed as independently reconstructed in this packet. The finite checker tests parity, subset patterns, Koszul signs and the explicit Hessian; it does not certify arbitrary-rank topology through finite enumeration. The all-rank conclusion comes from the analytic argument and the cited primary theorem.
