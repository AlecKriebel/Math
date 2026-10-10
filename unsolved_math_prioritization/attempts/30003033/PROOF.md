# Orthogonal-pair theta modules and an obstruction to ordinary Jacobi principal series

## Status and exact scope

**Accepted partial result, not a solution of the original unrestricted question.** The accompanying [mathematical audit](MATHEMATICAL_AUDIT.md) accepts the exact scope below. This AI-assisted manuscript and audit are unrefereed; acceptance is not external human peer review, journal acceptance, or formal proof-assistant certification. Recorded audit date: 10 October 2026.

This is a partial result for problem 30003033 / OWR-14211-008, not a solution of the unrestricted principal-series realization question. It gives an explicit algebraic module calculation, a principal-series embedding of its oscillator socle, and a nonembedding theorem for the full module in the usual smooth or distribution-vector principal series. No novelty assertion is made. In particular, Westerholt-Raum already described these theta functions as extensions of Schrödinger–Weil representations and as reducible indecomposable modules in the originating report.

The analytic theorem below is proved for the orthogonal negative/isotropic-pair family on which the usual completed theta expansion exists on a nonempty open chamber with locally normally differentiable sums. This includes the rational-isotropic-edge subfamily covered by the cited convergence/completion theorems. For any additional OWR data, the same conclusion is conditional on that analytic hypothesis; this note does not remove the irrational-isotropic-edge issue. It does not replace the OWR family by arbitrary cones.

We work with the full vector-valued theta series, or its zero discriminant component when considering its local infinitesimal module. Singularities are allowed. All differential identities are identities of ordinary functions away from the singular divisor, continued as identities of analytic germs. They are **not** distributional identities obtained by extending the functions across their poles or the sign walls. This distinction is essential to the obstruction below.

## 1. Data, completion, and conventions

Let V=L tensor R have nondegenerate bilinear form B, q(v)=B(v,v)/2, signature (p,r), n=p+r. For arithmetic modularity and discriminant Weil type we use the integral/even convention: B(L,L) is contained in Z and q(L) is contained in Z, with discriminant group L^vee/L. The chamberwise local differential-module calculation only needs a discrete full lattice and the stated analytic expansion. For the unconditional rational-ray convergence argument below, retain the integral-lattice hypothesis and rays rational with respect to L. Take r pairs (c_i,d_i), with q(c_i)<0, nonzero isotropic d_i, and mutually orthogonal planes span(c_i,d_i). Use the orientation B(c_i,d_i)<0, as in the precise construction in [WR15, section 3]. This orientation is needed for the sign-difference cone to be nonnegative; the short OWR announcement suppresses it. Necessarily p>=r.

Choose an orthogonal real basis b_1,...,b_n, with b_1,...,b_p positive and b_{p+i}=c_i negative. Write q(z)=sum_j m_j z_j^2 in its coordinates, m_j=q(b_j), and beta_j=-2 pi m_j. Thus beta_j<0 in positive directions and beta_j>0 in negative directions. The coordinates of nu in this basis are nu_j; no integral splitting of L in this real basis is assumed.

Use E(t)=2 integral_0^t exp(-pi s^2) ds, so that E(+infinity)=1. Put a=v/y for tau=x+iy and z=u+iv. The conventional normalized completed kernel is

K_nu(y,v)= product_i [ E(B(c_i,nu+a) sqrt(y)/sqrt(-q(c_i))) - sgn B(d_i,nu+a) ].

Then, on a convergence chamber,

Theta_mu(tau,z)=sum_{nu in L+mu} K_nu(y,v) exp(2 pi i(q(nu) tau+B(z,nu))).                 (1)

The normalization of E and of the sign term is relative, not optional: both must have limiting magnitude 1. Formula (1) is the standard error-function normalization of the OWR sign-difference completion. Overall nonzero constants or factors 1/2 per pair do not affect any module statement below. The chamberwise holomorphic part uses the sign difference stated in OWR. Changes of chamber are handled by the established analytic continuation, not by differentiating a discontinuous sign function across its wall.

[WR15, Theorem 3.6 and Corollary 3.7] give weight n/2, lattice index L, and discriminant Weil type, with the relevant singularities discussed in Proposition 3.3. [WR17, Theorem 4.2] supplies a qualified convergence/modularity theorem for rational isotropic edges. We use neither theorem as a principal-series realization theorem. We also do not infer a product decomposition of the *arithmetic theta function*: [WR15, section 3.1] explicitly distinguishes product type from an actual product over smaller rational lattices.

## 2. The real group and its central character

Set W=V direct-sum V with symplectic form

Omega((lambda,mu),(lambda',mu'))=B(lambda,mu')-B(mu,lambda').

Let H_B=W x R, with product (w,t)(w',t')=(w+w',t+t'+Omega(w,w')/2). The center acts by psi(t)=exp(2 pi i t). Let

J_B=SL_2(R) semidirect H_B,
Jtilde_B=Mp_2(R) semidirect H_B.

SL_2 acts on the two V coordinates through its standard two-dimensional symplectic action. A choice of left rather than right semidirect-product convention only changes the notation for this action. We use the metaplectic cover throughout, so half-integral weights present no ambiguity. The unitary Schrödinger representation of H_B has its oscillator extension omega_B to Jtilde_B. On its smooth vectors it is realized on the Schwartz space S(R^n). The kernel of Mp_2 -> SL_2 acts on omega_B by (-1)^n; it is not asserted to be genuine on this particular cover when n is even.

For the standard real Heisenberg generators P_j,Q_j, use

P_j=partial_{t_j}, Q_j=4 pi i m_j t_j,
L_j=(P_j-i Q_j)/2, R_j=(P_j+i Q_j)/2.

Then [L_i,R_j]=delta_ij beta_j, and L_j^*=-R_j in the unitary Schrödinger model. These are the normalizations of the covariant lowering/raising operators used below.

## 3. Differential identities of the completed theta generator

On weight-k functions on the Jacobi half-space the covariant operators are

L_j=-i y partial_{bar z_j},
R_j=i partial_{z_j}-4 pi m_j v_j/y,
F=X_-=-2 i y(y partial_{bar tau}+sum_j v_j partial_{bar z_j}),
E_+=X_+=2 i partial_tau+2 i sum_j(v_j/y)partial_{z_j}-4 pi q(v)/y^2+k/y,
H=k.

Products are interpreted on the graded direct sum of weights: L_j lowers the weight by 1, R_j raises it by 1, and F,E_+ shift by -2,+2. In particular the k used in a successive E_+ is the weight at that stage. Their commutators are

[L_i,R_j]=delta_ij beta_j, [F,E_+]=-H,
[F,R_j]=-L_j, [L_j,E_+]=R_j,
[H,R_j]=R_j, [H,L_j]=-L_j.

These agree with [CR15, Definition 2.5 and Proposition 2.6].

Define the oscillator elements and the commuting residual sl_2:

E_osc=sum_j R_j^2/(2 beta_j),
F_osc=-sum_j L_j^2/(2 beta_j),
H_osc=sum_j R_j L_j/beta_j+n/2,
E_0=E_+-E_osc, F_0=F-F_osc, H_0=H-H_osc.                                (2)

Direct commutation proves that E_0,F_0,H_0 commute with every L_j,R_j and form an sl_2 triple. Equivalently this is the virtual Levi splitting in [CR15, section 5.1]. At fixed nonzero central character the enveloping algebra is

A_n tensor U(sl_2,0),                                                         (3)

where A_n is the Weyl algebra generated by R_j,L_j. No Stone–von Neumann assertion about arbitrary algebraic A_n modules is used here.

### Lemma 1 (the actual OWR annihilators, and stronger residual identities)

For Theta from (1), at weight k=n/2,

L_j Theta=0                         (1<=j<=p),
R_j L_j Theta=0                     (p<j<=n),
E_0 Theta=F_0 Theta=H_0 Theta=0.                                      (4)

Proof. On a fixed chamber every sign term is locally constant. In a negative coordinate put w=v_j+y nu_j. The nonconstant factor is E(-2 sqrt(-m_j)w/sqrt(y)); its derivatives, denoting that factor by A, satisfy

A_y=(nu_j/2-v_j/(2y)) A_v,
A_vv=(8 pi m_j/y)(v_j+y nu_j) A_v.                                  (5)

The same identities, with zero derivatives, hold for the chamberwise constant part. For h_nu=exp(2 pi i(q(nu)tau+B(z,nu))),

R_j L_j(A h_nu)=[y A_vv/4-2 pi m_j(v_j+y nu_j)A_v]h_nu=0.

In positive directions every factor is locally holomorphic, proving the first identity in (4). Orthogonality ensures that differentiation in a negative coordinate acts only on its corresponding error-function factor. The holomorphic heat equation is

(partial_tau-sum_j partial_{z_j}^2/(8 pi i m_j))(K_nu h_nu)=0.          (6)

For one variable the amplitude remaining in (6), after the holomorphic exponential terms cancel, is

-i A_y/2+A_vv/(32 pi i m_j)+i nu_j A_v/2=0

by (5). The multivariable equation is the sum of these identities; there are no mixed second derivatives in the diagonal heat operator.

Expanding (2) gives

E_0=2 i partial_tau-sum_j partial_{z_j}^2/(4 pi m_j)+(k-n/2)/y.

Thus (6) gives E_0 Theta=0 at k=n/2. On a kernel term the amplitude in F_0 is

y^2 K_y+y sum_j v_j K_{v_j}-sum_j y^2 K_{v_jv_j}/(16 pi m_j),

which vanishes by (5). Finally H_0 Theta=0 follows from the first two identities in (4). Locally normal differentiability justifies summation, and analytic continuation preserves the identities. For the rational-isotropic-edge subfamily, the sign walls are locally finite. Differentiating a nonconstant factor only replaces it by a polynomial times its decaying Gaussian. The Gaussian supplies the majorant in that negative direction; the other directions retain the convergence estimates of the cited orthogonal-pair construction. On compact subsets avoiding the walls this gives the differentiated versions of those estimates. This is the analytic input used here; it is not claimed for arbitrary irrational edges. QED.

### Direct convergence and differentiation for rational isotropic rays

The following direct argument is supplied by the accompanying audit. It justifies the analytic input in this orthogonal family without assuming that absolute convergence alone implies termwise differentiability. In this subsection the plane coordinates beta_i are unrelated to the commutator constants beta_j used above.

Rescale real coordinates separately on each signature \((1,1)\) plane so its quadratic form is \(\alpha_i^2-\beta_i^2\), its negative vector is along the \(\beta_i\)-axis, and its isotropic vector points in the direction \((1,1)\). The orientation condition \(B(c_i,d_i)<0\) permits this choice with the signs used below. Put \(w=\nu+v/y\) and \(\lambda_i=\alpha_i-\beta_i\). The completed factor is

\[
K_i(w)=-E(2\sqrt y\,\beta_i)-\operatorname{sgn}(\lambda_i).
\]

Decompose it, for estimates only, as

\[
D_i+T_i,
\qquad D_i=-\operatorname{sgn}(\beta_i)-\operatorname{sgn}(\lambda_i),
\quad T_i=\operatorname{sgn}(\beta_i)-E(2\sqrt y\,\beta_i).
\]

The cone contribution \(D_i\) is supported where \(\beta_i\lambda_i\ge0\). On this support

\[
q_i(w)=\lambda_i^2+2|\lambda_i||\beta_i|.
\]

For a rational isotropic ray, \(B(d_i,L)\) is discrete after a fixed rescaling, under the integral-lattice hypothesis. On a compact subset of a chamber avoiding every isotropic sign wall there is therefore one \(\delta>0\) with \(|\lambda_i|\ge\delta\) for every lattice term and every index \(i\). It follows that

\[
q_i(w)\ge\delta(|\lambda_i|+2|\beta_i|)
\ge\delta\sqrt{\alpha_i^2+\beta_i^2}
\]

on the cone support. The complementary tail satisfies

\[
|T_i|\le e^{-4\pi y\beta_i^2}.
\]

Multiplying that tail by the absolute value of the exponential changes the plane's quadratic decay from \(q_i\) to \(q_i+2\beta_i^2=\alpha_i^2+\beta_i^2\). Every differentiated error factor likewise is a polynomial in the lattice coordinates, with coefficients uniformly bounded on the chosen compact set, times this Gaussian. Undifferentiated factors retain the cone-plus-tail bound. Differentiating the holomorphic exponential only introduces additional polynomial factors.

The remaining positive orthogonal space contributes positive-definite Gaussian decay. After expanding the finitely many choices of cone/tail factors, all summands of every prescribed finite derivative are bounded uniformly by

\[
C(1+\|\nu\|)^N e^{-c\|\nu\|},\qquad c>0.
\]

This is summable over any full lattice. In obtaining the bound one uses

\[
|e^{2\pi i(q(\nu)\tau+B(z,\nu))}|
=e^{2\pi yq(v/y)}e^{-2\pi yq(\nu+v/y)};
\]

the first factor is bounded on the compact set. Thus all needed derivatives, and indeed derivatives of every finite order, converge locally normally on such chambers. No rational splitting of the full lattice into the real planes was used.

This verifies the rational-ray part of the claimed analytic input. The argument gives no uniform \(\delta\) for general irrational isotropic data. It therefore does not erase the attempt's irrational-edge boundary. Likewise, the estimate is not a license to differentiate sign jumps across a wall or poles across a singular divisor as if no distributions were created.

### Casimir normalization

Let Omega_0=H_0^2-2H_0+4E_0F_0. It is central in (3). With the Casimir differential operator C_{k,L} normalized as in [CR15, equation (2.4)],

Omega_0=(k-n/2)(k-n/2-2)-2 C_{k,L}.                                  (7)

One can derive (7) either from [CR15, Theorem 5.1 and its proof] or by expanding (2). Since all residual generators kill Theta and k=n/2, C_{n/2,L}Theta=0. This verifies exactly the Casimir, p first-order, and r second-order annihilators announced in OWR.

The shift in (7) matters. It is wrong to assert that the same zero-normalized C_{k,L} kills every descendant at its shifted weight. Omega_0 does kill the full module, whereas on an oscillator descendant of weight k, C_{k,L} has eigenvalue (k-n/2)(k-n/2-2)/2.

Also, F Theta is generally **not** zero. The correct identity is F Theta=F_osc Theta. Consequently the stronger assertion ker(X_-) must not be substituted for the residual equation ker(F_0). In the inspected [WR15] PDF, section 2.1 and Corollary 3.7 appear to imply this stronger assertion using the lowering operator printed in (1.5). The same formulas occur in the published version, equations (2.5), section “Various spaces of H-harmonic Maaß-Jacobi forms,” and Corollary 4.7. Our calculation does not rely on that implication; with those literal conventions it conflicts with (5). The OWR annihilators themselves remain verified. This is a normalization/subspace issue that must be resolved if importing that additional source assertion verbatim.

### An explicit Fourier coefficient detects ordinary lowering

One can rule out cancellation in the theta sum explicitly. Take the even integral lattice \(\mathbb Z^2\) with \(q(a,b)=a^2-b^2\), \(c=(0,1)\), \(d=(1,1)\). Choose a chamber with \(2(v_+-v_-)/y\notin\mathbb Z\). The zero Fourier mode in the real elliptic variables of the completion is

\[
A(y,v_-)-\sigma,
\quad A=E(-2v_-/\sqrt y),
\]

where \(\sigma\) is chamberwise constant. Directly,

\[
F(A-\sigma)=\frac{yv_-}2A_{v_-}
=-2v_-\sqrt y\,e^{-4\pi v_-^2/y}.
\]

This is nonzero when \(v_-\ne0\). Distinct lattice vectors have distinct elliptic Fourier characters because \(B\) is nondegenerate. Thus other Fourier modes cannot cancel this coefficient. The normally convergent Fourier expansion justifies the uniqueness argument. This establishes nonvanishing on the actual theta function, not only nonvanishing on an isolated formal summand.

The printed WR15 incomplete-gamma normalization can multiply the nonconstant amplitude by a fixed nonzero scalar; that cannot make this derivative vanish. Nor can the printed isotropic sign's omission of the shift create a compensating ordinary derivative inside a fixed chamber. This calculation, independently supplied by the accompanying audit, verifies the literal ordinary-lowering incompatibility. It does not diagnose how every source theorem should be restated; the original OWR annihilators proved above remain valid.

## 4. Exact algebraic theta module

Normalize x_j=R_j and d_j=L_j/beta_j, so [d_i,x_j]=delta_ij. For A_1=C<x,d>/([d,x]-1), define

P=A_1/A_1 d,
M=A_1/A_1(xd),
Q=A_1/A_1 x.

All quotients are left modules; A_1(xd) means the left ideal generated by xd, not a two-sided ideal.

### Lemma 2 (rank-one extension)

There is a nonsplit exact sequence

0 -> Q -> M -> P -> 0,                                                  (8)

where 1 in Q maps to d v, with v the class of 1 in M. A basis of M is

v, x^a v (a>=1), d^b v (b>=1).

For N=xd these vectors have distinct eigenvalues 0,a,-b. The actions are

d x^a v=a x^{a-1}v (a>=1), d v=dv,
x d^b v=-(b-1)d^{b-1}v (b>=1).

The last expression is zero for b=1. These formulas follow from [d,x]=1 and xd v=0. They both provide an explicit module model and prove linear independence of the displayed basis. The span of the d^b v is Q, and the quotient is P. A hypothetical splitting would lift 1 in P to v+w with w in span{d^b v:b>=1} and d(v+w)=0. The coefficient of dv in this expression is 1, impossible. Q is the unique simple submodule and is essential: from any nonzero submodule, a polynomial in N isolates an eigenvector, then powers of x or d reach dv. QED.

### Theorem 3 (faithful tensor-product description)

Let V_Theta denote the cyclic graded differential (equivalently infinitesimal Jacobi) module generated by Theta. Under the analytic hypotheses in section 1,

V_Theta is isomorphic to T=P^{tensor p} tensor M^{tensor r},             (9)

with sl_2 acting through the oscillator formulas (2) and residual sl_2 acting trivially. Its full cyclic annihilator in (3) is the left ideal generated by

d_j (j<=p), x_j d_j (j>p), E_0,F_0,H_0.                                (10)

Proof. Relations (4) give a surjection T -> V_Theta. The joint eigenvectors of the commuting N_j=x_jd_j form one-dimensional joint weight spaces in T, with weights n_j>=0 in each P factor and n_j in Z in each M factor. From any nonzero finite linear combination one isolates a joint eigenvector with a polynomial in the N_j. In positive coordinates powers of d_j reach the vacuum. In a negative coordinate, powers of d_j (from a nonnegative weight) or x_j (from a weight below -1) reach d_j v. Therefore every nonzero submodule contains

s=product_{j>p} d_j v,

and the module generated by s is the simple essential socle

S=P^{tensor p} tensor Q^{tensor r}.                                   (11)

It remains to show that s maps nontrivially. Apply every negative L_j to the theta kernel. The chamberwise sign terms vanish, and each differentiated E contributes

-2 sqrt(-m_j y) exp(4 pi m_j(v_j+y nu_j)^2/y).

Thus product_{j>p}L_j Theta is a nonzero constant times y^{r/2} times the majorant Gaussian theta kernel. At tau=i,z=0 its analytically extended zero-discriminant component is the nonzero constant times

sum_{nu in L} exp(-2 pi q^+(nu)),
q^+(nu)=sum_{j<=p}m_j nu_j^2-sum_{j>p}m_j nu_j^2.                       (12)

The sum in (12) is finite and strictly positive. This evaluation is on the smooth Gaussian shadow, not an evaluation of Theta at a possible pole. Therefore s has nonzero image. Any nonzero kernel of T -> V_Theta would meet the essential simple socle and hence contain it, contradicting (12). The map is an isomorphism. Formula (10) now follows from the presented tensor-product module and (3). QED.

The module has finite composition length 2^r, with the tensor-product filtration obtained from (8), and is indecomposable because it has a simple essential socle. These are algebraic statements. They identify the extension mentioned by Westerholt-Raum, rather than claiming that the general idea of such an extension is new.

Although every vector is finite under the compact Cartan, finite multiplicity of its weights is not asserted. Indeed for p,r>=1, a positive exponent and a negative lowering exponent can grow together while keeping the total H weight fixed. Thus a fixed compact-Cartan weight space in (9) is infinite dimensional. The phrase “Harish-Chandra module” in the source must therefore be interpreted with the Jacobi/nonreductive conventions in mind, not silently replaced by an admissible reductive (g,K)-module.

## 5. A specified principal series and the oscillator-socle embedding

Let B_2 be the upper triangular subgroup of SL_2(R), and let Btilde_2 be its inverse image in Mp_2(R). For s in C and epsilon in {0,1}, let I(s,epsilon) be normalized smooth induction from the character

diag(a,a^{-1}) -> |a|^s sgn(a)^epsilon,

pulled back to Btilde_2 and trivial on its covering kernel and unipotent radical. Concretely f(bg)=|a|^{s+1}sgn(a)^epsilon f(g); the group acts by right translation. This convention fixes the parameter, including the half-modulus shift.

Define the fixed-central-character Jacobi principal series

Pi_B(s,epsilon)=omega_B tensor-hat I(s,epsilon).                         (13)

Equivalently, with Ptilde=Btilde_2 semidirect H_B, (13) is normalized induction from Ptilde to Jtilde_B of (chi_{s,epsilon} tensor omega_B|Ptilde). The half-modulus factor is |a|. The tensor identity is explicit: v tensor f maps to the omega_B-valued induced function

j=(g,h) -> f(g) omega_B(j)v.

At s=-1,epsilon=0, constant functions give an explicit copy of the trivial representation in I(-1,0).

The socle S in (11) is the algebraic Hermite oscillator module for omega_B: L_j kills its vacuum in positive directions and R_j kills its vacuum in negative directions. Its vacuum corresponds, up to a nonzero scalar, to

G(t)=exp(-2 pi sum_j |m_j|t_j^2).

This identifies S with the span of polynomial-Hermite derivatives of G, with the same Heisenberg and oscillator sl_2 actions. Consequently there is an explicit infinitesimal injection

S -> Pi_B(-1,0),          Phi -> Phi tensor 1.                           (14)

In theta terms, the generator of S is the full Gaussian shadow in (12); normalize its isomorphism with G by sending that nonzero vector to G. Formula (14) is a principal-series relation with a specified group, subgroup, inducing representation, parameter, and infinitesimal map. The finite polynomial-Hermite span is not invariant under all real Heisenberg translations. Its Schwartz oscillator globalization has the group-equivariant injection S(R^n) -> Pi_B(-1,0), Phi -> Phi tensor 1. It is a relation for the **socle**, not an embedding of the full completed theta module.

## 6. Why the full extension cannot be inserted into the ordinary model

### Theorem 4 (smooth and distribution-vector nonembedding)

If r>0, then for every s,epsilon,

Hom_{gtilde_B}(V_Theta,Pi_B(s,epsilon))=0,
Hom_{gtilde_B}(V_Theta,Pi_B(s,epsilon)^{-infinity})=0.                    (15)

The distribution vectors in the second line mean the strong continuous dual of the smooth contragredient, not arbitrary meromorphic germs or unrestricted hyperfunctions.

Proof. Choose a negative coordinate j, so beta_j>0. In its unitary Schrödinger factor write a,a^* for the normalized annihilation/creation operators, [a,a^*]=1. The conventions of section 2 give

R_j=sqrt(beta_j)a, L_j=-sqrt(beta_j)a^*,
R_j L_j=-beta_j(a a^*)=-beta_j(N_Hermite+1).                             (16)

On the Hermite basis the eigenvalues are -beta_j(l+1), l=0,1,2,...; in particular zero is absent. The inverse multiplies the l-th Hermite coefficient by -1/[beta_j(l+1)]. It is continuous both on Schwartz functions (rapidly decreasing coefficients) and on tempered distributions (polynomially growing coefficients). With other variables and any principal-series factor present, the same inverse acts in that coordinate alone and remains continuous. In the compact realization I(s,epsilon) is a smooth section space over a compact one-dimensional manifold. Distribution vectors are its dual paired with the Schwartz factor, so the transposed inverse is again defined and continuous. Equivalently one can apply the Hermite-coefficient argument with coefficients in that distribution space.

Hence R_j L_j has zero kernel in both targets in (15). Any intertwiner sends the cyclic theta generator, annihilated by R_j L_j, to zero, and is consequently zero. QED.

The obstruction is independent of the inducing parameter; changing s does not repair it. Even the inclusion (14) cannot extend to a map from the full module in (9).

Sun's equivalence [Sun, Theorem A/Proposition 4.2] makes the category issue precise: smooth Fréchet representations of moderate growth with this nondegenerate unitary central character have the form omega_B tensor-hat E. The same operator argument applies there. Therefore the full theta module cannot occur as a nonzero infinitesimal submodule of such a globalization, nor of a closed smooth subquotient still in that category. We do **not** assert a theorem about arbitrary nonclosed algebraic subquotients of an induced representation.

This does not contradict the existence of meromorphic theta functions. Their infinitesimal equations hold away from poles. Extending them as distributions across singularities can create terms supported on the singular set; one cannot simply promote the chamberwise equations to global distribution-vector equations. The theorem rules out that unqualified step.

## 7. What is still missing

The original question allows more than the ordinary moderate-growth principal-series model specified here. A full resolution would need a precisely defined larger realization, for example an appropriate meromorphic/localized induced module, an explicitly specified boundary-value category, or a representation involving singular support and an extension map. It would have to retain the **full** module (9), not just the Gaussian shadow, and prove its intertwining and global analytic properties. No such construction is supplied here.

Additionally, this note does not prove convergence and the chamberwise differentiation hypothesis for every possible irrational-isotropic datum in the abbreviated OWR statement. The rational-edge completion results are not permission to declare all real isotropic data covered. This is a distinct analytic boundary of the present partial theorem.

Thus the verified conclusion is: the theta module has an explicit oscillator-extension structure, its socle maps into Jacobi principal series at normalized parameter -1, and its full extension is excluded from every ordinary smooth or distribution-vector Jacobi principal series. The original broader connection question remains unresolved by this attempt.

## Edition and verification limits

The complete mathematical argument is preserved from the accepted partial manuscript. The direct rational-ray convergence/differentiation bound and explicit source-discrepancy Fourier coefficient above reproduce expository arguments from the accompanying audit. They do not enlarge the accepted theorem. The arithmetic lattice convention and the infinitesimal/global socle distinction are made explicit as required by that audit.

Recorded finite checks are supplementary evidence, not substitutes for the analytic and algebraic proofs. Edition preparation rechecked frozen byte identities and publication integrity; it did not rerun the original mathematical programs or perform new scholarly retrieval, source-text inspection, or literature search. This proof-only edition distributes no programs, raw outputs, datasets, copied third-party source documents/text/images, or private coordination material.

## References

[OWR] Martin Westerholt-Raum, “Analytic properties of some indefinite theta series,” contribution to Lattices and Applications in Number Theory, Oberwolfach Reports 3/2016, printed pp. 138–139. https://doi.org/10.4171/owr/2016/3

[WR15] Martin Westerholt-Raum, H-Harmonic Maaß-Jacobi Forms of Degree 1: The Analytic Theory of Some Indefinite Theta Series, arXiv:1207.5603v3 (20 May 2015), especially sections 1.3, 2.1–2.4, 3, 3.1, 4; Theorem 3.6, Corollary 3.7, and Theorem 4.2. https://arxiv.org/abs/1207.5603v3 . Published version: Research in the Mathematical Sciences 2:12 (2015), https://doi.org/10.1186/s40687-015-0032-y ; the specific operator/subspace assertions were also checked in that version.

[WR17] Martin Westerholt-Raum, Indefinite Theta Series on Cones, arXiv:1608.08874v2 (16 January 2017), especially sections 1.3, 1.6, 3 and 4; Theorem 4.2. https://arxiv.org/abs/1608.08874v2

[CR15] Charles H. Conley and Martin Raum, Harmonic Maaß-Jacobi forms of degree 1 with higher rank indices, arXiv:1012.2897v2, especially Definition 2.5, Proposition 2.6, Remark 1, and sections 5.1–5.2. The downloaded PDF has arXiv margin date 23 January 2015 and an internal title-page date 10 November 2018; both are recorded rather than conflated. Published bibliographic DOI: https://doi.org/10.1142/S1793042116501165 . Preprint: https://arxiv.org/abs/1012.2897v2

[Sun] Binyong Sun, On representations of real Jacobi groups, arXiv:1004.5508v2 (12 October 2010), Theorem A and sections 4–5. Published in Science China Mathematics 55 (2012), 541–555. https://arxiv.org/abs/1004.5508v2 ; https://doi.org/10.1007/s11425-011-4333-3

The oscillator tensor-product description, virtual Levi splitting, and extension interpretation have the prior attributions above. The proofs in this note are self-contained algebraic/operator calculations for the stated scope; they are not a literature-based novelty certificate.
