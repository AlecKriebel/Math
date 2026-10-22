# Geometric consequences of the R-valued residue primitives

Authored proof, 14 October 2026. Shared PASS 2/5. This note uses RIGHT_END_LIFTING.md and the independently accepted PASS 1 left-exact repair. It concerns geometric function-field-valued cocycles. It is not a claim that the original arithmetic map or its prescribed relative formula has been constructed.

## 1. The full h² family and the coefficient ring

Let R=Z[1/6], let F be imaginary quadratic with maximal order O, and let (E_r)_(1<=r<=h) be the LSSW §3.1 CM model family over L=F(f). Its compatible CM lattices are C/a_r, and all isogenies between members are defined over L. Let

A_i=E_i1 × E_i2, for i=(i1,i2) in {1,...,h}².

Use the source's groups Gamma_i of O-linear automorphisms and its isogeny module systems Delta_i,j. In particular, no division by h or collapse to a single CM product is involved. The auxiliary ray modulus f here is the model field's modulus; it is not an assumption that the eventual target level N has injective unit reduction.

Write Ck(i) for the three Gersten terms with R coefficients. Let C(i) be the image of K2(L)⊗R in C2(i). The accepted PASS 1 results and the present right-end proof give

0 -> (C2(i)/C(i))^tf -> C1(i)^tf -> C0(i)^tf -> R -> 0.                  (1.1)

If 5 is unramified in F, they additionally give

0 -> C2(i)^tf -> C1(i)^tf -> C0(i)^tf -> R -> 0.                        (1.2)

All maps are compatible with the indicated group actions. Pushforward by an O-linear isogeny commutes with the full CM traces. Pullback preserves eventual invariance after the exceptional element is enlarged to exclude its kernel: the coprime-kernel square is cartesian. The same observations apply to constants and their quotient, so both sequences are module-system sequences.

No use is made here of the unmodified Z[1/30] sequence with 5 silently retained. Sequence (1.2) uses specifically the unramified-5 norm annihilator proved in PASS 1. When 5 ramifies, its leftmost injectivity is false in general.

## 2. Canonical auxiliary cocycle classes

Put q=Nc for a nonzero ideal c. On each product set

e_c,i=q²[0]-[A_i[c]],

eta_c,i=theta_c,E_i1 exterior E_i2[c] + q[0] exterior theta_c,E_i2.

RIGHT_END_LIFTING.md proves partial eta_c,i=e_c,i and invariance under every scalar alpha prime to c. Every Gamma_i fixes e_c,i, since its members are O-linear automorphisms and preserve the origin and the c-torsion subgroup scheme.

Use the source's row-vector convention for the action, or equivalently write gamma· for the chosen left action on coefficients. Assume first that 5 is unramified. There is a unique

Theta_c,i(gamma) in C2(i)^tf

satisfying

partial Theta_c,i(gamma)=gamma·eta_c,i-eta_c,i.                           (2.1)

Indeed the right side is a trace-fixed C1-cycle, so (1.2) gives existence and uniqueness. Injectivity in (1.2) then proves

Theta_c,i(gamma delta)=Theta_c,i(gamma)+gamma·Theta_c,i(delta).

If eta is replaced by any other trace-fixed primitive of e_c,i, their difference is the residue of a unique trace-fixed q_i in C2(i). The resulting cocycles differ by gamma·q_i-q_i. Consequently

[Theta_c,i] in H¹(Gamma_i,C2(i)^tf)

depends only on e_c,i. The construction is the connecting map for the short exact sequence obtained by replacing C0 with its degree-zero part; it is R-linear in the zero-cycle. For c=O it is the zero class.

When 5 ramifies, precisely the same proof gives a unique cocycle with values in

Q_i=(C2(i)/C(i))^tf,

and a canonical class in H¹(Gamma_i,Q_i). The existence of eta is no longer a conditional hypothesis: it has now been explicitly proved. It does not follow that the quotient cocycle lifts to an actual K2-valued trace-fixed cocycle. Section 7 states the remaining obstructions.

## 3. Pushforward and pullback identities

All identities in this section are identities of cohomology classes with the source's component changes and group-cochain maps. A chosen representative has an additional coboundary unless the indicated primitive itself transports exactly. This distinction matters.

### 3.1 Prime-to-c norms

Suppose f=f1×f2:A_i -> A_j and each f_u has kernel prime to c. Then

f_*e_c,i=e_c,j,

f_*eta_c,i=eta_c,j.

The second identity is literal: it follows from the exact one-curve norm formula. If the group action is intertwined by f, (2.1) and uniqueness therefore identify the transported representative cocycles exactly. If one passes between different arithmetic groups using restriction, conjugation, and corestriction, naturality instead gives the corresponding identity of cohomology classes.

In the source's notation, for i related to j by an ideal n prime to c,

[n]_*[Theta_c,i]=[Theta_c,j].                                            (3.1)

The base-change square needed for the group-cochain map is cartesian because the automorphism gamma and its conjugate are isomorphisms. Residues commute with proper pushforward, flat pullback, and the finite sums in corestriction. These facts prove naturality over R integrally; no cohomological averaging denominator occurs.

### 3.2 Arbitrary ideal pullback

Suppose f_u:E_iu -> E_ju has kernel E_iu[n] for both u=1,2. Then

f^*e_c,j=e_nc,i-(Nc)² e_n,i.

Naturality of the connecting map gives

[n]^*[Theta_c,j]=[Theta_nc,i]-(Nc)²[Theta_n,i].                           (3.2)

This is valid whether or not n and c are coprime. The exact chain-level difference is the explicit Steinberg boundary in RIGHT_END_LIFTING.md, (6.6); it is not simply equality of the chosen C1-primitives. In the unramified-5 case its unique trace-fixed K2 lift gives the relevant coboundary.

For completeness, non-coprime product norms are also explicitly known, even when the two kernel ideals differ: if g_u=a_u+c, then

(f1×f2)_*e_c
  =(Nc)²[0]-Ng1 Ng2 [E1'[c/g1]×E2'[c/g2]].

The norm of the primitive is formula (6.2) of the companion note. Thus the norm relation is not overstated as prime-to-c invariance at bad auxiliary primes.

### 3.3 Auxiliary exchange as a geometric identity

Let C_c denote central ideal pullback [c]^* on the appropriate tuple of geometric cohomology groups. The zero-cycle identity is

(Nd)² e_c-C_d e_c = (Nc)² e_d-C_c e_d.

Both sides equal

(Nc)²(Nd)²[0]-(Nd)²[A[c]]-(Nc)²[A[d]]+[A[cd]].

Therefore the same identity holds for the canonical cocycle tuples:

((Nd)²-C_d)[Theta_c]=((Nc)²-C_c)[Theta_d].                               (3.3)

This is a geometric auxiliary-compatibility identity. Replacing C_d by an Artin operator after arithmetic specialization is a separate assertion, and solving these equations by division to remove c is another separate assertion. Neither is inferred from (3.3).

## 4. Geometric Hecke and diamond identities over R

The integral zero-cycle calculation behind the source's geometric Hecke identity is as follows. For a prime ideal p, the Np+1 rank-one O/p submodules of A[p] each contain zero, while every nonzero point belongs to exactly one. Therefore the sum of their reduced cycles is

Np[0]+[A[p]].

The double-coset representatives defining T_p send the cyclic-kernel pullback of the origin to precisely these submodules. Hence, with the source's tuple/component convention,

T_p[0]=Np[0]+[A[p]].

Central ideal pullbacks commute with that double-coset action. Since [c]^*[0]=[A[c]], it follows that

T_p[A[c]]=Np[A[c]]+[A[pc]].

Consequently

T_p e_c=(Np+[p]^*)e_c.

The connecting map commutes with restriction, conjugation, and finite corestriction sums, so

T_p[Theta_c]=(Np+[p]^*)[Theta_c].                                       (4.1)

This proves the geometric all-prime identity on the full Gamma system over R when 5 is unramified, and in the constant-quotient coefficient system for all F. It is not the arithmetic bad-level identity U_p^*=1: these are different operators on different level systems, and (4.1) by itself does not supply that assertion.

Likewise, a source diamond representative is an O-linear isomorphism between the appropriate product models. Its pullback preserves the origin and every c-torsion scheme, so it transports e_c exactly. Naturality gives the source's diamond component compatibility for [Theta_c], again over R in the unramified case and in the quotient system otherwise. These arguments are integral incidence and push-pull calculations; no denominator of 5, h, Np+1, or an index of groups is introduced.

## 5. Representatives regular at the required torsion orbit

The following is a geometric regularity statement; it does not identify an arithmetic ray-field target or prove its integrality.

Let N be a nonzero proper ideal prime to c, fix a primitive N-torsion point P on the second curve, and let S consist of the points (0,uP) for u in (O/N)^×. Make the source's compatible ideal-representative choices, and choose

x in c Hom_O(E_i2,E_i1)

whose reduction at N is a unit between the two torsion modules. Such an x exists by the same invertible-ideal CRT argument used in RIGHT_END_LIFTING.md, §4. Let mu be the shear

(z1,z2) |-> (z1+xz2,z2).

It is an O-linear automorphism. Since x kills E_i2[c], pullback leaves the first term of eta_c,i unchanged on its support, while it replaces the vertical second term by a function on the graph z1+xz2=0. Set eta_c,i^mu=mu^*eta_c,i. It remains trace-fixed and has residue e_c,i.

The support curves of eta_c,i^mu avoid S:

- On E_i1×E_i2[c], a point (0,uP) could occur only if uP is c-torsion. Coprimality of c and N and the fact that N is proper rule this out.
- On the graph z1+xz2=0, it could occur only if xuP=0, which is ruled out by the unit reduction of x.

For gamma in Gamma_0(N)_i, its lower-left entry c_gamma is zero modulo N and its lower-right entry d is a unit modulo N. The transported support curves are tested at S by d and by c_gamma+dx respectively; both are units modulo N. Thus the support of

gamma·eta_c,i^mu-eta_c,i^mu

avoids S. In the unramified-5 case the unique C2^tf primitive has no residue at any divisor outside these finitely many support curves. By the Gersten kernel description it belongs to H²(V,R(2)) for their complement V, which contains S. It is therefore an element of the trace-fixed direct limit of H²(V,R(2)) over opens containing S.

This proves the R-coefficient analogue of the geometric regularity statement in LSSW Lemma 3.4.1 for these source groups, without imposing a unit-injectivity condition on N just for this geometric step. The proper-level and primitive-point hypotheses are explicit. It does not extend the point evaluation to the singular origin at the unit ideal.

Over a field K where a chosen point in S is rational, restriction to its stabilizer and pullback at that point give a cocycle valued in K2(K)⊗R; if the stabilizer acts trivially on K this is a homomorphism. This is an ordinary geometric specialization statement. Proving that the source's particular arithmetic action identifies K and its invariants with the intended ray field, and verifying the constant-sensitive descent on K2, remain additional tasks.

The same residue argument places the ramified-5 quotient cocycle in the corresponding quotient of the groups regular near S. Its evaluation remains a quotient by specialized constants, not an unambiguous K2(K)-class.

## 6. Base change, isomorphisms, and comparison with the source

The one-curve normalized theta elements commute with extension of L and with O-linear isomorphisms, by their proved uniqueness. Thus the explicit eta elements commute with those operations. In the unramified-5 case uniqueness in the surface left-exact complex shows that the associated cocycles commute as well. This is the precise geometric content needed in the source's model-comparison statement (Lemma 3.4.3), now with R coefficients.

After extending coefficients R -> Z[1/30], the elements theta_c,E and the sheared eta_c,i satisfy the same defining norm and residue conditions as the source's elements. The source's uniqueness therefore identifies them. The uniquely determined cocycle with that sheared residue is consequently the source's geometric auxiliary cocycle after extension of coefficients.

This comparison is at the geometric function-field level, where uniqueness has been proved. It is not a substitute for the source's later ray-field descent, elliptic-unit integrality, arithmetic norm relations, or the calibration of an unaugmented compactified map. Those steps cannot be obtained merely by extending the geometric statement backwards from Z[1/30] to R.

## 7. The remaining ramified-5 obstruction is unchanged

For ramified 5 the explicit eta and the right-end theorem remove the previously missing residue-input hypothesis. They do not remove either obstruction from accepted PASS 1:

1. Given an element of (C2/C)^tf, existence of a representative in C2^tf remains a separate fixed-lifting issue. For a fixed monoid M its obstruction is the connecting class in Ext¹_(R[M])(R,C), allowing enlargement of the exceptional monoid for eventual invariance.
2. For the inverse-image module G of Q=(C2/C)^tf in C2, the quotient cocycle class has an ordinary lift precisely when its connecting class in H²(Gamma,C) for 0->C->G->Q->0 vanishes. The lifted class can have the corresponding constant-valued H¹ ambiguity.

The original fixed left kernel is still K2(L)[5]. A proof that simply chooses a C2 representative and declares its cocycle identity by the residue identity would overlook this kernel. None of the formulas in this note does that.

## 8. Outcome and outstanding contract requirements

The following are established by the current proof plus the accepted PASS 1 input:

- Right-end degree-zero fixed lifting for all source CM products, and for general same-type maximal-CM products with the explicit 2,3-only descent above.
- A canonical one-curve theta system over R with exact norm/pullback laws and no unspecified constants.
- Explicit auxiliary residue primitives for all h² products and all nonzero ideals c.
- If 5 is unramified, canonical genuine geometric K2-valued auxiliary cocycle classes, their source geometric norm/pullback/Hecke/diamond identities, and regular representatives near the prescribed torsion orbit.
- If 5 ramifies, the corresponding canonical constant-quotient cocycle classes, with the previous conditional eta hypothesis now discharged.
- Comparison with the source's geometric auxiliary family after inverting 5.

Still unproved here: a constant-sensitive ramified-5 lift; ray-field descent and its compatibility at every small level; arithmetic auxiliary removal; the integer-ring absolute target, especially at prime-power levels; the actual arithmetic bad-U identity; compactification at all levels and characters; the prescribed relative cusp-symbol formula and its global relations. These are substantive remaining parts of the construction contract. The original problem remains UNSOLVED.

Public source: LSSW, *Eisenstein cocycles for imaginary quadratic fields*, §§2.4 and 3.1–3.4, https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf . The identities cited for comparison are rederived above on cycles or from exactness over R; the source's Z[1/30] theorem is not used as an R-coefficient theorem.
