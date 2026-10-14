# Exact scalar-five normalization of the genuine auxiliary cocycles

Authored proof, 14 October 2026. Shared PASS 3/5, row 1777 / 30005572. This proves a constant-sensitive geometric normalization for every source CM component and every auxiliary ideal prime to 5. It does not claim arithmetic specialization, all isogeny pullback identities at 5, auxiliary removal, or the full construction contract.

## 1. Result and why the previous obstruction is not contradicted

Put R=Z[1/6], A=E1 x_L E2, C2=K2(L(A)) tensor R, and C=K2(L) tensor R, embedded as constants. Assume the source's maximal imaginary-quadratic CM action is defined over L. Let T_alpha denote simultaneous CM pushforward, so T_5 acts on C by 5^4=625. Write

Q=(C2/C)^tf,

where tf means eventual invariance under all CM traces outside some exceptional element. The accepted PASS 1 theorem makes the residue map Q -> C1^tf injective. The accepted PASS 2 theorem supplies the actual eta_c with boundary (Nc)^2[0]-[A[c]], and the canonical quotient cocycle theta-bar_c with residue gamma eta_c-eta_c.

**Theorem.** If the auxiliary ideal c is prime to (5), then theta-bar_c has a unique lift Theta_c whose values are both eventually trace-fixed and fixed by T_5. This lift is an ordinary C2-valued cocycle, pointwise lifts the specified quotient cocycle, and has its exact Gersten residue. In fact every value is fixed by every T_alpha with (alpha,c)=1. The construction is independent of the ordinary lift, every finite-orbit normalization choice, the trace annihilator, and its exceptional set.

The theorem holds in every one of the source's h^2 components, including fields where 5 ramifies. It uses only R coefficients. It is canonical for the specified eta_c; varying eta by an appropriately normalized boundary changes the cocycle by a coboundary.

The nonzero eventual trace-fixed constant kernel C[5] in the ramified case remains unchanged. What removes it here is the additional exact identity T_5=1. On C[5], T_5=625 is zero, so no nonzero such constant can also be T_5-fixed. Unlike the eventual trace condition, this extra identity is available for the actual eta_c whenever (c,5)=1.

## 2. An integral splitting lemma

Let q lie in Q and suppose T_5 q=q. Choose an exceptional element beta for q and enlarge it to include 5. The accepted PASS 2 scalar-trace construction gives an R-linear operator B_beta with

B_beta(C)=0, augmentation(B_beta)=5,

such that B_beta x is M_beta-fixed and lifts 5q for every ordinary representative x of q. Here M_beta is the CM multiplication monoid prime to beta. Its operators commute with T_5.

Define

P_beta = 125 B_beta + T_5 - 625,

and

sigma(q)=P_beta x.                                                     (2.1)

This formula has only integral coefficients in addition to the already permitted R coefficients of B_beta. There is no division by 5, a torsion order, an orbit degree, or a class number.

The operator P_beta kills C, because both B_beta and T_5-625 do. Thus (2.1) does not depend on x. Its image in C2/C is

125(5q)+(1-625)q=q.

For alpha in M_beta, (T_alpha-1)x is constant. Hence

(T_alpha-1)P_beta x=P_beta(T_alpha-1)x=0.

Likewise (T_5-1)x is constant, so

(T_5-1)P_beta x=P_beta(T_5-1)x=0.

Thus sigma(q) is eventually trace-fixed and T_5-fixed.

For uniqueness, two such representatives differ by an eventually trace-fixed constant. The accepted constant-kernel result makes this difference zero if 5 is unramified and an element of C[5] if 5 ramifies. In the latter case its T_5-invariance says 625t=t, whereas 5t=0 implies 625t=0, so t=0.

Consequently sigma is independent of B_beta and beta, additive and R-linear. It identifies

{z in C2^tf : T_5 z=z}  -->  {q in Q : T_5 q=q}

bijectively. The inverse is the quotient map. It commutes with the geometric automorphism action, which fixes constants and commutes with every scalar trace. This is a splitting on the displayed restricted submodule, not a claim that all of Q has invariant representatives.

If 2 is admissible, one may choose B_beta=(16-T_2)/3. Then the same formula works. Alternatively the shorter operator

P=(T_5-42T_2+47)/6                                                     (2.2)

kills constants and has augmentation one, and defines the same sigma whenever q is fixed by T_2 and T_5 and is eventually trace-fixed. Indeed its value is invariant under every eventual trace and T_5 by the same calculation. Formula (2.2) is an illustrative identity, not an assumption that 2 is prime to every c.

## 3. Evaluation of both previously unresolved tests on the actual values

This section computes the accepted two-stage obstruction, rather than merely naming it again. Keep the fixed B_beta and ordinary representative x. Set

a=5x-B_beta x in C,

b=(T_5-1)x in C.

Since B_beta kills constants and commutes with T_5,

0=(T_5-1)B_beta x=(T_5-1)(5x-a)=5b-624a.

Thus 624a=5b. Since 625-624=1,

a=5(125a-b).                                                          (3.1)

The first obstruction [a] in C/5C is therefore exactly zero. The explicit permitted constant correction is b-125a, giving

y=x+b-125a=P_beta x.

For alpha in M_beta write b_alpha=(T_alpha-1)x and d_alpha=N(alpha)^2. The defining fivefold lift and commuting traces give respectively

5b_alpha=(d_alpha-1)a,

624b_alpha=(d_alpha-1)b.

The residual character from the accepted second test is therefore

(T_alpha-1)y
 = b_alpha+(d_alpha-1)b-125(d_alpha-1)a
 = b_alpha+624b_alpha-625b_alpha
 = 0.                                                                 (3.2)

Both obstructions vanish pointwise. The computation applies whenever q is T_5-fixed; Section 4 proves that hypothesis for the actual theta-bar_c(gamma), not for a hypothetical replacement.

## 4. Applying the splitting to every genuine auxiliary value

The accepted one-curve normalization gives

T_alpha theta_c,E=theta_c,E if (alpha,c)=1.

The explicit surface primitive is

eta_c=theta_c,E1 exterior [E2[c]] + Nc[0] exterior theta_c,E2.

Consequently T_alpha eta_c=eta_c for every alpha prime to c, including alpha=5 when (c,5)=1. Simultaneous scalar traces commute with gamma, so

T_alpha(gamma eta_c-eta_c)=gamma eta_c-eta_c.

For the unique quotient value q=theta-bar_c(gamma), T_alpha q remains eventually trace-fixed: all scalar traces commute. It has exactly the same residue as q. Injectivity of Q -> C1^tf therefore proves

T_alpha theta-bar_c(gamma)=theta-bar_c(gamma)

for every alpha prime to c. In particular T_5 q=q.

Define

Theta_c(gamma)=sigma(theta-bar_c(gamma)).                               (4.1)

The R-linearity and Gamma-equivariance of sigma give the ordinary cocycle identity immediately. Its residue and its pointwise quotient are precisely the prescribed ones. This uses an actual equivariant section, not vanishing of an ordinary H^2 obstruction.

For alpha prime to c, T_alpha Theta_c(gamma) and Theta_c(gamma) are both eventually trace-fixed, T_5-fixed representatives of the same quotient value. Uniqueness proves exact full prime-to-c trace invariance of Theta_c(gamma).

The sheared primitive used to make evaluation regular at an N-torsion orbit also commutes with T_5, since the shear is O-linear. Hence this argument applies to that representative at every proper N prime to c, with no extra restriction that N be prime to 5. This is a geometric regularity/normalization statement, not yet an arithmetic descent assertion.

## 5. Finite-orbit independence after normalization

Let Psi_S be the accepted canonical D-fold ordinary cocycle associated with eta_c and any finite reduced Gamma-stable S disjoint from its auxiliary cycle, with D=deg_L S. Let x be any ordinary representative of the quotient cocycle. The accepted construction gives Psi_S=D x-r_S, with r_S constant-valued.

For any one common beta for the quotient cocycle, the formula in Section 2 therefore gives

P_beta Psi_S=D Theta_c.                                                (5.1)

This is pointwise equality of cocycles. It does not divide D. In particular, applying P_beta to any of the accepted Bezout ordinary lifts returns exactly Theta_c, independent of S, the Bezout coefficients, and all local Gersten primitives. More generally every ordinary cocycle lift of theta-bar_c has the same image under P_beta, because differences are constant-valued.

The raw multiple Psi_S is not claimed to equal D Theta_c: their difference is a potentially nonzero constant-valued cocycle. Equation (5.1) is the proved normalization and independence result.

## 6. Proven naturality, with the pullback-at-five boundary retained

### 6.1 Base extension and isomorphisms

Extension of the coefficient number field and O-linear model isomorphisms commute with scalar traces, constants, residues, and the normalized one-curve theta system. They consequently transport eta_c and its quotient cocycle exactly. Their transported Theta_c is again eventually trace-fixed, T_5-fixed, and has the required residue. Uniqueness proves exact compatibility of the representative cocycles. No choice of finite torsion field or auxiliary evaluation scheme is involved in this argument.

In particular this proves the geometric model-isomorphism compatibility needed for the analogue of LSSW Lemma 3.4.3, for auxiliaries prime to 5. Identifying an arithmetic ray-field target remains a separate step.

### 6.2 Prime-to-c product norms, including norms of 5-power degree

Let f=f1 x f2:A -> A' be a product of O-linear L-isogenies, each with kernel ideal prime to c. The accepted exact one-curve norm law gives

f_*eta_c,A=eta_c,A'.

Proper pushforward commutes with simultaneous scalar traces even when the isogeny degree is divisible by 5. It takes constants to degree(f) times constants. Thus, on intertwined automorphism groups, f_*Theta_c,A and Theta_c,A' have the same residue and are both eventually trace-fixed and T_5-fixed. Uniqueness proves their exact equality. With the source's restriction/conjugation/corestriction conventions this yields the corresponding norm identity of cocycle classes on the full component system.

This includes arbitrary component-changing product norms prime to c. It does not require their degree to be invertible in R or prime to 5.

### 6.3 Pullbacks of degree prime to 5

Let f be an O-linear isogeny whose kernel is prime to 5. Finite-flat base change then makes f^* commute with T_5. It preserves eventual trace invariance after enlarging the exceptional element by its kernel. Therefore f^* preserves the normalized coefficient submodule in Section 2.

For a simultaneous ideal isogeny with kernel A[a], where (a,5)=1 and (c,5)=1, the accepted zero-cycle and chain identities give

f^*[Theta_c]=[Theta_ac]-(Nc)^2[Theta_a].                                (6.1)

To justify the coboundary rather than suppress it, the difference of the prescribed C1 primitives is a closed element, eventually trace-fixed and T_5-fixed. The accepted quotient exactness lifts it to Q. Injectivity of its residue map makes that quotient lift T_5-fixed, and sigma supplies a unique normalized C2 lift. Its group coboundary is precisely the representative correction. Thus (6.1) is an identity of classes; it need not be literal equality of the initially specified representatives.

The same argument supplies geometric auxiliary exchange for c,d both prime to 5 and the good geometric Hecke class identities at primes not dividing (5), with the source's component conventions. These use only the accepted zero-cycle identities and naturality of the now normalized coefficient system for these pullbacks.

### 6.4 No unsupported pullback claim at 5

If an isogeny kernel meets A[5], the pullback square with [5] need not be cartesian. Such pullback need not commute with T_5. Hence it has not been proved here to preserve the normalized coefficient submodule. The all-prime geometric Hecke identity at primes above 5 does not follow from this argument, and neither does a blanket all-isogeny pullback statement.

The norm result in Section 6.2 has no such restriction, because it uses commuting proper pushforwards rather than a non-cartesian pull-push interchange.

## 7. Dependence on the primitive and comparison with the source

Suppose eta and eta' are eventually trace-fixed, T_5-fixed primitives of the same auxiliary zero-cycle. Their difference is a closed C1-element. The accepted quotient exactness gives its unique quotient lift q. The same residue-injectivity argument proves T_5q=q. Let z=sigma(q). Then eta'-eta=partial z, and the two normalized cocycles differ by gamma z-z. Their normalized cohomology classes agree.

Thus for auxiliaries prime to 5 the ordinary normalized class is independent of the chosen primitive within this specified class, including changes between eligible sheared representatives. No independence under unrestricted ordinary Gersten primitives is asserted.

After extension of coefficients R -> Z[1/30], Theta_c is trace-fixed with exactly the source's specified residue. The source's uniqueness identifies it with the existing geometric auxiliary cocycle. This is stronger than mere agreement up to a constant after inverting 5, but it remains a geometric comparison. Arithmetic ray descent, integral arithmetic residues, and auxiliary cancellation require separate proofs.

## 8. Exact remaining scope

Proved here:

- Canonical, constant-sensitive, genuinely trace-fixed geometric cocycles over Z[1/6] for every source component and every auxiliary c prime to 5, also in ramified-five fields.
- Explicit vanishing of both prior invariant-representative tests on every actual value in that family.
- Independence of the ordinary finite-orbit/Bezout construction after the explicit normalization, with no orbit-degree division.
- Exact model-isomorphism and base-field compatibility, prime-to-c product norm compatibility including 5-power degree, and normalized pullback/class identities for kernels prime to 5.
- Exact comparison to the source geometric family after inverting 5.

Not proved here:

- This normalization for auxiliary ideals c divisible by a prime above 5. Their eta_c need not be T_5-fixed.
- An invariant representative for every element of Q, or removal of the nonzero eventual trace-fixed constant kernel.
- All-isogeny pullback or all-prime Hecke compatibility at 5.
- Arithmetic ray-field descent, all-character auxiliary removal, integer-ring absolute integrality, compactification, every arithmetic bad-prime identity, or the prescribed relative theta-symbol formula.

Auxiliary ideals prime to both 5 and any given target level are always available, so the restriction does not force exclusion of levels above 5 from the geometric construction. That observation does not itself discharge the separate arithmetic and calibration requirements of the frozen construction contract. The original problem remains UNSOLVED.

## Sources and dependencies

The proof uses the accepted PASS 1 constant-quotient exactness and exact constant kernel, and the accepted PASS 2 one-curve normalization, explicit residue primitive, fivefold lift, finite-orbit construction, and zero-cycle identities. It does not assume an R-coefficient version of a theorem stated only after inverting 5.

Public source for the comparison and conventions: E. Lecouturier, R. Sharifi, S.-C. Shih, J. Wang, *Eisenstein cocycles for imaginary quadratic fields*, Sections 3.1-3.4, https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf . The exact scalar-five normalization in Sections 2-4 is the authored argument above.
