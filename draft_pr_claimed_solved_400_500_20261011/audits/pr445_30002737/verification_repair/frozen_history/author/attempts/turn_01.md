# Turn 1 of 5: a planar unweighted counterexample

Date: 2026-10-03. Substantive proof attempt. Status: candidate complete negative resolution of the unrestricted, dimension-unspecified implication; awaiting independent review. No novelty or peer-review claim.

## Target and scope

The target is van Enter's Conjecture 1 in Oberwolfach Report 53/2014, printed p.2996, DOI 10.4171/OWR/2014/53. We interpret absolute continuity in its standard ambient sense: with respect to Haar measure on the dual group, hence two-dimensional Lebesgue measure for an R2 translation action. The printed conjecture does not impose dimension one or any spectral multiplicity condition.

We construct an unweighted, aperiodic, repetitive FLC Meyer set in R2 with a uniquely ergodic translation hull. Its diffraction is entirely singular, but its dynamical system has a nonzero spectral measure equivalent to planar Lebesgue measure. Thus the assertion fails in this class, if the construction below is correct. It does not resolve the separately restricted one-dimensional question.

## 1. One-dimensional input

Let X be the binary Rudin-Shapiro hull over {-1,1}, with shift S and unique invariant probability measure mu. Write f(x)=x_0. We use exactly these established properties:

1. X is minimal and uniquely ergodic.
2. Integral f dmu=0.
3. Integral f(x)f(S^m x) dmu(x)=1 for m=0, and 0 otherwise.

These properties, including a direct correlation proof, are recorded in Baake and Grimm, 'Can Kinematic Diffraction Distinguish Order from Disorder?', arXiv:0810.5750v2, pp.2-3 (published as 'Kinematic diffraction is insufficient to distinguish order from disorder', Phys. Rev. B 79, 020203(R), 2009, with erratum 80, 029903(E)). The binary sequence comes from the primitive substitution a->ab, b->ac, c->db, d->dc, under a,b->1 and c,d->-1.

By unique ergodicity, the means and two-point averages above converge uniformly over X along integer intervals. In particular, for every x in X,

lim_N (2N+1)^(-1) sum_{i=-N}^N x_i = 0,

lim_N (2N+1)^(-1) sum_{i=-N}^N x_i x_{i+m} = delta_{m,0}.

No probabilistic independence of the entries of a Rudin-Shapiro sequence is assumed.

## 2. Product action and a simpler weighted model

On X times X use the Z2 action T^(m,n)(x,y)=(S^m x,S^n y). Its unique invariant probability is mu times mu. Indeed, invariance under the first coordinate makes the conditional measures in the first factor equal to mu, after which second-coordinate invariance fixes the second marginal. Minimality follows because the Z2 orbit of (x,y) is the Cartesian product of its two dense shift orbits.

As a preliminary model, put w_(i,j)=4+x_i+2y_j. The four possible values 1,3,5,7 distinguish (x_i,y_j), so the weighted array retains both sequences. Its autocorrelation coefficient at displacement (m,n) is

eta(m,n)=16+delta_(m,0)+4 delta_(n,0).

Expansion and separate averaging prove the identity: all linear and mixed terms vanish by the zero means, the x-x term equals delta_(m,0), and the y-y term equals delta_(n,0). Therefore the weighted lattice comb has diffraction

16 delta_(Z2) + lambda times delta_Z + 4 delta_Z times lambda,

where lambda is one-dimensional Lebesgue measure. It is carried by (R times Z) union (Z times R), a planar null set. Yet the observable g(x,y)=x_0 y_0 has correlation delta_(m,0) delta_(n,0), hence Haar spectral measure on T2. This already proves the discrepancy for a positive weighted FLC lattice comb. The next sections eliminate weights and give a direct R2 spectral measure.

## 3. An unweighted Delone realization

Set e=(1/10,1/10), a=(1/3,0), b=(0,1/3), and define

Lambda_(x,y) = Z2 union (Z2+e)
  union {(i,j)+a : i,j in Z, x_i=1}
  union {(i,j)+b : i,j in Z, y_j=1}.

All points have weight 1. The four residue classes 0,e,a,b modulo Z2 are distinct.

Uniform discreteness and relative density: Lambda lies in (1/30)Z2 and contains Z2. Thus it is Delone. Its difference set lies in (1/30)Z2, so it is Meyer and has finite local complexity.

Recognizability: among the four possible residue classes C={0,e,a,b}, the relation d-c=e modulo Z2 holds only for (c,d)=(0,e). Consequently the points p of Lambda with p+e also in Lambda are exactly the anchor lattice Z2. This remains true after any translation. The anchor lattice recovers the translation phase modulo Z2; presence or absence at anchor+a recovers x_i, and at anchor+b recovers y_j. These tests use fixed finite-radius neighborhoods. In particular no information is lost by the decoration.

Let Sigma(X) be the unit suspension (X times [0,1])/(x,1)~(Sx,0). The hull of Lambda is topologically conjugate to Sigma(X) times Sigma(X), with the two coordinates of R2 acting separately. To see surjectivity, independent integer shifts are dense in X times X and fractional shifts give the suspension phases; compactness gives every hull limit. The marker test gives injectivity modulo the suspension identifications. Continuity of the forward decoration map is immediate in the local topology, and a continuous bijection from a compact space into the Hausdorff hull is a homeomorphism.

Therefore the hull is minimal and uniquely ergodic. Its invariant probability corresponds to mu times mu times Lebesgue measure on [0,1)^2. Thus Lambda is repetitive and has uniform patch frequencies. Any translation period would preserve the recovered anchor lattice, hence be an integer pair (m,n), and would impose S^m x=x and S^n y=y. No element of X is periodic: otherwise minimality would make the whole hull a finite orbit, contradicting the delta correlation. Thus Lambda is aperiodic.

The construction is deterministic and substitution-derived. In fact the product of two copies of the four-letter Rudin-Shapiro substitution is a primitive 2-by-2 block substitution on 16 letters: the entry (r,s) in the image of (c,d) is (rho(c)_r,rho(d)_s). The binary codings followed by the fixed four-slot decoration produce Lambda. We do not assert that every possible reformulation with extra irreducibility or one-dimensional hypotheses is refuted.

## 4. Autocorrelation and diffraction of the unweighted set

Write omega_x=sum_i x_i delta_i and omega_y=sum_j y_j delta_j. Let

D=delta_0+delta_e+(1/2)delta_a+(1/2)delta_b,
P=D*delta_(Z2),
A=(1/2)delta_a*(omega_x times delta_Z),
B=(1/2)delta_b*(delta_Z times omega_y).

Then delta_Lambda=P+A+B. This is only an algebraic decomposition used to compute the diffraction of the positive unweighted measure delta_Lambda.

Use square averaging [-N,N]^2. Fixed motif shifts affect only O(N) boundary points; divided by area their contribution to any fixed autocorrelation coefficient vanishes. Since the difference set is locally finite, coefficient convergence gives vague convergence.

The P-P autocorrelation is (D*D_tilde)*delta_(Z2). The A-A autocorrelation is (1/4)delta_0 times delta_Z, since the x correlation at horizontal displacement m is delta_(m,0) and the vertical weights are constant. Similarly, B-B gives (1/4)delta_Z times delta_0. The self-correlations are unaffected by the fixed translates a,b.

Every P-A or P-B cross-correlation is zero because it contains a one-dimensional average of x_i or y_j. Every A-B cross-correlation is zero: at any fixed displacement its coefficient factors into the product of an x interval mean and a y interval mean, each tending to zero. These calculations apply uniformly over x,y because the one-dimensional averages do.

Hence

gamma_Lambda=(D*D_tilde)*delta_(Z2)
  +(1/4)(delta_0 times delta_Z+delta_Z times delta_0).

With Fourier transform exp(-2 pi i k dot t), Poisson summation gives

hat(gamma_Lambda)=sum_(k,l in Z) |1+exp(-2 pi i(k+l)/10)
  +(1/2)exp(-2 pi i k/3)+(1/2)exp(-2 pi i l/3)|^2 delta_(k,l)
  +(1/4)(lambda times delta_Z+delta_Z times lambda).

The whole measure is supported on E=(R times Z) union (Z times R). E is a countable union of lines and has two-dimensional Lebesgue measure zero. Thus hat(gamma_Lambda)_ac=0. The line terms have no atoms, so they are genuinely singular continuous in the ambient plane. As a normalization check, gamma_Lambda({0})=3 equals the density of Lambda, while the Bragg intensity at the origin is 9=3^2.

## 5. A nonzero absolutely continuous R2 dynamical spectral measure

On Sigma(X), use the L2 observable h([x,u])=x_0 for 0<=u<1. It need not be continuous across the suspension section; measurable bounded observables are admissible for dynamical spectral type.

For real t, the unit suspension flow changes the symbolic coordinate by floor(u+t). Conditional on u,

integral_X h([x,u]) h(T_t[x,u]) dmu(x)=delta_(floor(u+t),0).

Integrating u over [0,1) gives

C_h(t)=(1-|t|)_+.

This holds also for negative t and for integer t; endpoints of the section have measure zero. Fourier inversion of the triangle function gives the finite probability spectral measure

d sigma_h(k)=(sin(pi k)/(pi k))^2 dk,

with the value at zero understood as 1.

On Sigma(X) times Sigma(X), put H([x,u],[y,v])=x_0 y_0. Under the R2 action its correlation is

C_H(t_1,t_2)=(1-|t_1|)_+(1-|t_2|)_+,

because the invariant measure is the product measure. Its spectral measure is therefore

d sigma_H(k_1,k_2)=sinc^2(k_1) sinc^2(k_2) dk_1 dk_2,

where sinc(k)=sin(pi k)/(pi k). The density integrates to 1 and is positive off a planar null set (the lines where either coordinate is a nonzero integer). Thus sigma_H is nonzero and equivalent to planar Lebesgue measure. Transfer H across the established hull conjugacy to obtain the required observable on the unweighted Delone hull.

This proves a nontrivial absolutely continuous dynamical component. No assertion about exact multiplicity, simplicity, or pure absolute continuity of the full representation is used. Constants and suspension phases already give point spectrum, and further singular components may coexist.

## 6. Why the standard positive results do not contradict the example

Pure-point diffraction equivalence does not apply: the original diffraction contains singular-continuous line terms. Dworkin's inclusion is respected: the original diffraction sees the separate row and column observables, each spectrally confined to lines, while their product sees the full plane. The singular spectral subspace for a higher-rank action need not be closed under multiplication.

The theorem reconstructing dynamical spectrum from all suitable factor diffractions also remains true. The locally decoded weighted lattice factor z_(i,j)=x_i y_j has autocorrelation delta_(0,0), hence planar Lebesgue diffraction. It is an additional factor, not the diffraction of the original unweighted point set. Presence of the product in a factor is exactly the information that the physical point-set diffraction misses.

If the intended target secretly meant dimension one, or required a stronger hypothesis encompassing every local factor's diffraction, this planar counterexample would not answer that modified question. Such restrictions are not printed in the primary conjecture. Likewise, 'absolutely continuous along a line' is not absolute continuity with respect to the ambient Haar measure and must not be substituted for it.

## Verdict and next step

The argument is a complete candidate counterexample to the printed unrestricted assertion, already with an unweighted aperiodic repetitive FLC Meyer set and unique invariant measure. Stop substantive proof attempts at 1/5 if independent review confirms the construction and source scope. A finite exact checker will verify marker uniqueness and algebraic correlation identities only; it is not a substitute for the infinite-system proof. Historical priority remains unresolved. No external publication or remote mutation is authorized by this file.
