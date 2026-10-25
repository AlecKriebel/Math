# Independent adversarial reconstruction before opinions, code or foreign bodies

The entire actual five-page PDF and full controlling 13594-byte TeX have been read, including the bibliography and all category/scope caveats. No support review narrative, historical/current scientific report, source checker or foreign primary body has been consulted. This note reconstructs the literal claim, attacks the universal quantifiers and supplies an alternative proof route; it is not a final verdict. Exact original source hashes are bound separately.

## Literal claim and success criterion

The category C is local Artinian W(k)-algebras with identified residue k. Here k=F4=F2[u]/(u²+u+1), G=(k,+)=C2×C2, N=F2 and Q=G/N=C2. The action is rho(a)(t)=t/(1+at). D_H is the set of lifts of the residual local action to continuous A-algebra automorphisms of A[[t]], modulo coordinate conjugation reducing to the identity. Nilpotent constant terms are expressly allowed. This is unframed deformation, not deformation preserving a chosen zero section. The target uses the actual fixed subfunctor D_N^Q, not a hull or a cohomological replacement.

The original theorem says that there exist no prorepresentable F=h_R and natural maps f:D_N^Q→F←D_Q:g for which the actual restriction–induction map D_G→D_N^Q×_F D_Q is formally smooth. R is complete Noetherian local over W(k), residue k; no tangent dimension is prescribed. In particular the refined one-dimensional-recipient proposal fails, while the variant additionally assuming D_N and D_Q prorepresentable is not addressed. All-natural-map collapse, full formal series, actual tangent restriction, and the exact source question/category are the obligations. Finite jets, a versal-ring map, tangent linearity of f/g or a claim that a Klein-four hull is universal would not suffice.

## Basic action and quotient, independently checked

Mobius substitution gives rho(a)rho(b)=rho(a+b), and its t² coefficient distinguishes a, so the action is faithful. Every nonzero a has rho(a)t−t=a t²/(1+at) of order2, hence conductor1. N is normal of index2.

Take y=t²/(1+t). Then t²+yt+y=0 and rho(1)(t)=t+y. The series y^m and t y^m have leading orders2m and2m+1, so successive leading-term subtraction gives the unique complete basis k[[t]]=k[[y]]⊕t k[[y]]. Its Laurent analogue is k((t))=k((y))⊕t k((y)); only finitely many negative powers are needed. Invariance sends A+tB to A+tB+yB, so B=0. This proves both fixed rings/fields, with no generic truncation inference. Since u(u+1)=1, rho(u)y=t²/((1+ut)(1+(u+1)t))=t²/(1+t+t²)=y/(1+y). Thus the quotient action is the conductor1 involution sigma(y)=y/(1+y).

The local coordinate category matters: y↦(y+e)/(1+y) has nilpotent constant e and unit linear coefficient1+e. Its Mobius determinant1+e is a unit, its matrix square is(1+e)I and it is an allowed involution. Nilpotent translations are continuous for the formal-series topology over an Artinian base: sufficiently high powers have arbitrarily high y-order after using nilpotence. They would be excluded by a different pointed-zero-section functor.

## Distinct adversarial recipient-collapse route: ring injections

Let A=k[e]/(e²), B=k[w]/(w³), and inject i:A→B by e↦w². Let v in D_Q(A) be sigma_e(y)=(y+e)/(1+y), and let0 be the basechanged residual action. This v is nonzero even allowing arbitrary identity-reducing conjugators y+e h(y), h∈k[[y]] including constants: every first-order conjugacy correction has constant coefficient h(0)−sigma'(0)h(0)=0, while sigma_e−sigma=e/(1+y) has constant perturbation1.

The following direct cubic-ring matrix identity should be checked exactly:

M_delta=[[1,delta],[1,1]], C=[[1+w,w],[0,1]],
M_(w²) C=(1+w) C M_0 modulo w³ in characteristic2.

Indeed both sides are [[1+w,w+w²],[1+w,1+w]]. C reduces to the identity and has unit determinant1+w. Thus D_Q(i)(v)=D_Q(i)(0) as actual deformation classes. Every h_R preserves injections of target rings: if i∘psi=i∘phi then psi=phi pointwise. Naturality of any eta:D_Q→h_R therefore forces eta_A(v)=eta_A(0). This proves collapse for every natural map and every allowed R, including mixed-characteristic R, without linearity or a chosen tangent dimension. The stronger property is not inferred from failure of prorepresentability alone; the specific injected tangent is used.

The paper instead first uses j:B→B,w↦w+w² fixing the deformation class x=[sigma_w]. I independently checked its proposed matrix shape: M_(w+w²) C=(1+w) C M_w modulo w³, and B^j=k+k w². Naturality makes the image map R→B fixed by j, and reduction B→A kills w², giving the basepoint. Both routes are valid if their exact matrix/free-coordinate conventions hold. The injection route is a distinct way to audit the unrestricted quantifier; it also exposes the precise prior-ingredient claim to check against Byszewski–Cornelissen Proposition6.1. No novel involution pathology is assumed.

## Distinct full-series module route: a rank-two matrix over k[[z]]

All algebraic k-derivations are coefficient derivations here. Every formal series h has the actual identity h=a(t)²+t b(t)² because k is perfect. Leibniz in characteristic2 gives d(h)=d(t)b²=d(t)h', with no assumed continuity. Therefore Theta=k[[t]]∂t and all such derivations are continuous.

The separable field polynomial t²+yt+y has derivative y≠0. An invariant derivation restricting to b(y)∂y extends uniquely with coefficient a(t)=b(y)(1+t)²/t². It preserves k[[t]] iff2ord_y b−2≥0, i.e. b∈y k[[y]]. Thus Theta^N identifies with M=y k[[y]]∂y. This threshold is **y**, not y²: for example b=y extends to(1+t)∂t, with a nonzero constant coefficient. A zero-section restriction would change this module and cannot be silently imposed.

On coefficients, Q acts by T f=(1+y)² f(y/(1+y)), with T²=1. Put z=y²/(1+y) and R0=k[[z]]. The same even/odd leading-order proof gives k[[y]]=R0⊕y R0 and invariant field k((z)). Multiplying that complete free basis by y gives

M=y R0⊕y² R0.

The operator is R0-linear because z is sigma-invariant. Its exact basis action is T(y)=y+y² and T(y²)=y², hence its matrix in(y,y²) is [[1,0],[1,1]]. Consequently ker(1+T)=image(T−1)=y²R0. This proves H¹(C2,M)=0 for the **whole complete formal-series module**, without passing from a finite-jet rank calculation or using an unproved limiting argument. In particular every cocycle value y²b(z) has the explicit coboundary primitive y b(z).

As an extra consistency check, on Theta^sharp=k[[y]]=R0⊕yR0, the matrix is [[1+z,z],[z,1+z]], using y²=z+zy. Since z is a nonzero divisor of R0, its invariant module is(1+y)R0 and its boundary image is z(1+y)R0=y²R0. Therefore H¹(Q,Theta^sharp) is one-dimensional over k, with representative1+y, consistent with the nonzero involution tangent v. A naive truncation can make z a zero divisor and introduce spurious cohomology; this exact R0-module calculation avoids that pitfall. The quotient Theta^sharp/Theta^N≅k has trivial Q action, so the prescribed H¹(Q,k) is k as stated, but is not needed for the contradiction.

## Restriction injectivity and the formal-smoothness obstruction

The first-order cocycle description must hold in this same unframed category: every lift over dual numbers is(id+e c(g))rho(g); relations give a1-cocycle with coefficients Theta, and identity-reducing coordinate changes give coboundaries. The category allows the constant coefficients used above. On restricting to N the map is the cohomological restriction.

Independently, if a G-cocycle is trivial on N in cohomology, first subtract a coboundary to make its N-values0. Commutativity of G and the cocycle relation force its value at u to be N-invariant. Order2 of u makes(1+T)c(u)=0. The exact M matrix gives c(u)=(T−1)m for m∈M. Subtract this coboundary: it leaves N-values0 and kills u, so it kills all of G. Thus ker(TD_G→TD_N)=0. Since D_N^Q(A) is literally a subset of D_N(A), the same zero-kernel assertion holds for restriction into the actual fixed subfunctor; no tangent formula for that subfunctor or extension of f to D_N is needed.

For any hypothetical natural f,g with representable recipient, naturality from k sends0_N to the unique recipient basepoint, and the collapse argument sends v to the same point. Thus(0_N,v) is an actual point of the fibre product over A. It reduces to the unique point over k. The surjection A→k is a small extension, so formal smoothness requires some w∈D_G(A) mapping to that pair. Its restriction0 forces w=0_G by injectivity, while naturality of induction makes ind(0_G)=0_Q, contradicting v≠0. This is a first-order target-surjectivity obstruction, not an unproved statement about higher obstruction groups or a deformation ring's universality.

## Falsification and source-interface ledger

1. Confirm actual source question is unrestricted; inspect Question4.4/6.4.4/OWR3039 separately from the conditional prorepresentability theorem. A citation-scope mismatch would not be cured by proving a different category.
2. Verify primary coordinate automorphisms really permit nilpotent constant terms. Pointed-zero-section deformations would exclude the crucial tangent and conjugator.
3. Check both cubic matrix identities modulo w³, unit determinants, allowed coordinate changes and ring-injection/naturality argument with no hidden tangent linearity.
4. Check exact quotient parameter, induced action, derivation extension and full rank-two R0-module matrices. Finite jets alone do not establish H¹=0.
5. Check restriction-cocycle compatibility and that actual fixed-subfunctor/basepoint maps are natural, not versal-hull substitutes.
6. Check first-order v≠0 against every formal conjugator, not just Mobius ones. The constant perturbation argument covers arbitrary h.
7. Check mixed-characteristic prorepresentable recipients cannot evade the injection/fixed-subring argument. A/B are legitimate W(k)-objects via W(k)→k.
8. Preserve prior credit for the additive action, involution pathology and tangent-cohomology theory. No firstness or current-open guarantee follows from a bounded search.

At this early checkpoint the literal mechanism has a coherent independent proof route and distinct adversarial checks; final status still awaits materially exact actual primary interfaces and own meaningful exact controls. No source correction, narrowed substitute, publication clearance, human/formal certification or outreach follows from this note.
