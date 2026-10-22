# Independent acceptance: scalar-five normalization

Date: 14 October 2026 UTC. Shared PASS 3/5; row 1777 / 30005572. No additional mathematical pass is opened.

## Verdict

ACCEPT the stated geometric normalization and its expressly limited naturality. Audited input: `pass3_trace_normalization/SCALAR_FIVE_NORMALIZATION.md`, SHA-256 `0fd5b52591d193b1949afbe17b022414610101b7fbb8fca2eb3ee65f215f66ca`.

This is a genuine advance for the actual auxiliary cocycles with c prime to five: it removes their invariant-representative obstruction over Z[1/6], including in ramified-five CM fields. It does not prove arithmetic ray descent, the full Hecke system at five, or the original construction. No novelty claim is made.

## 1. Independent operator check

Write C for constants, Q for the eventual trace-fixed constants quotient, and B for the accepted augmentation-five operator. For a T5-fixed q in Q and any ordinary representative x, both B and T5-625 kill C. Hence

P = 125 B + T5 - 625

kills C and induces multiplication by 125·5+1-625=1 on q. Every eventual trace defect of x is constant, as is its T5 defect. Commutation of the scalar pushforwards therefore proves that Px is both eventually trace-fixed and T5-fixed. This is a pointwise construction, not division by five.

The accepted eventual constant kernel is zero in unramified-five fields and C[5] in ramified-five fields. The additional T5 equation kills that latter kernel because T5 acts by 625 on constants. This proves uniqueness. It also proves independence of the chosen exceptional monoid or annihilator, and permits different elements to be compared after enlarging their exceptional sets. Additivity and Gamma-equivariance follow.

The illustrative shorter projector (T5-42T2+47)/6 also has augmentation one and kills constants: 625-42·16+47=0. Its stated T2-fixed hypothesis is necessary and retained.

## 2. The actual quotient cocycle is T5-fixed

This is the essential nonformal hypothesis, and it is proved.

The accepted normalized one-curve theta function is fixed by every CM norm prime to c. Its torsion divisor and the origin are also preserved by the corresponding pushforward. Thus the displayed product primitive eta_c is fixed by simultaneous T_alpha whenever (alpha,c)=1. An O-linear shear commutes with these simultaneous scalar maps, so the moved primitive used for torsion specialization has the same property.

T5 acts on the quotient Gersten complex: constants are stable, residues commute with finite pushforward, and T5 commutes with every trace in any eventual fixed monoid. Consequently T5 theta-bar_c(gamma) is another eventual fixed quotient value with exactly the same residue. The accepted injective quotient residue map identifies it with theta-bar_c(gamma).

When c is prime to five, the condition is therefore verified on every actual value and every source component. There is no step that mistakes eventual invariance, which may exclude five, for literal T5 invariance.

## 3. Both earlier obstruction tests are explicitly zero

For a=5x-Bx and b=(T5-1)x, the identity (T5-1)Bx=0 gives 624a=5b. Hence a=5(125a-b), verifying the required divisibility in C itself. The correction y=x+b-125a is exactly Px.

For an eventual trace T_alpha, put b_alpha=(T_alpha-1)x and d_alpha=N(alpha)^2. The two commuting-operator equations are

5 b_alpha=(d_alpha-1)a,
624 b_alpha=(d_alpha-1)b.

Substitution yields (T_alpha-1)y=(1+624-625)b_alpha=0. This independently checks the signs and the explicit annihilation of the residual C[5]-valued character. Neither stage is inferred from an equality after coefficient localization.

Applying this equivariant R-linear section to theta-bar gives a genuine group cocycle. Its value is fixed by every trace prime to c, since any such trace gives another normalized representative of the same quotient value.

## 4. Finite-orbit independence and naturality

The accepted finite-orbit multiple has the form Psi_S=D x-r_S with r_S constant. Applying P gives P Psi_S=D Theta_c. This proves the exact claimed independence after normalization, without dividing D or claiming that the original unnormalized multiple already equals D Theta_c.

Base-field extension and pointed O-linear model isomorphisms commute with finite scalar pushforward. The accepted normalized one-curve functions and the chosen eta transport compatibly. Uniqueness of the eventual-and-T5-fixed representative thus gives the exact model transport that was missing for ordinary lifts. This directly addresses the geometric premise of source Lemma 3.4.3.

For product isogenies with each kernel prime to c, the accepted one-curve norm and torsion pushforward formulas show f_*eta_c=eta'_c. Proper pushforwards commute with every simultaneous scalar pushforward, including T5. The resulting residue comparison therefore proves the stated norm compatibility even for degree divisible by five. On compatible group systems the restriction/conjugation/corestriction conventions are the same as the already accepted PASS 2 argument; no index is divided out.

For pullback, the needed square with [5] is Cartesian only under the stated prime-to-five kernel hypothesis. Under that hypothesis, pullback commutes with T5 and preserves eventual invariance after excluding the rest of the kernel. The accepted zero-cycle/chain identities and the new unique normalized lift of their closed C1 correction prove the stated class-level pullback and auxiliary-exchange identities. The same coefficient subsystem supports the geometric Hecke identities away from five.

The draft explicitly retains the failure of this argument for kernels meeting A[5]. This restriction was raised during review and is present in the frozen input. An arbitrary isogeny pullback, or a Hecke identity at a prime above five, is not accepted by this argument.

## 5. Exact scope

Accepted: the canonical genuine geometric cocycle over R for all source components and auxiliaries prime to five; exact vanishing of the two prior valuewise trace obstructions; normalized finite-orbit independence; model/base-field transport; the stated product norms; pullback/class compatibility away from five; and comparison with the source after coefficient localization.

Still open: auxiliaries meeting five, all-isogeny pullbacks and Hecke identities at five, arithmetic ray descent and integrality, all-character auxiliary removal, unrestricted compactification, actual all-level bad-U identities, and the genuine relative theta-symbol construction.

The prior nonzero eventual trace-fixed constant kernel remains valid. The new construction lies in its smaller T5-fixed part, where that kernel is zero. There is no contradiction and no claim that all eventual quotient classes admit invariant representatives.

## Source boundary

The proof uses the accepted PASS 1 and PASS 2 R-coefficient results and the explicit authored projector calculation, rather than importing a source theorem backwards across inversion of five. Source conventions were checked in LSSW Sections 3.1–3.4:

https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf

The original construction remains UNSOLVED.
