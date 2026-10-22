# PR1129: root mathematical reconstruction and positive prior implication

Scope: problem30005461, OWR-12697710-007, exact head26fed29c1130e539ba018a37200f133870f0e036. This AI-assisted research note is unrefereed. It is not a publication package or a human/formal proof certificate.

The actual submission has no QUEUE edit but explicitly claims both original questions. The original coefficient family is f_c=x^4*y^2+x^2*y^4+1-c*x^2*y^2, homogenized as M_c=x^4*y^2+x^2*y^4+z^6-c*x^2*y^2*z^2. A different positive-definite perturbation does not answer this question. Fresh GWS180-row inspection before substantive work found no exact problem, alias, Motzkin or mixed-odd result. Later authenticated complete account and existing package checks are separately recorded. No provider or PR mutation is authorized by these observations alone.

## Independent direct proof check

G=ABC-D^3 is primitive linear in C over R[A,B,D], since gcd(AB,D^3)=1. Gauss's lemma makes it irreducible and prime in the polynomial UFD. S=V(G) in projective3-space is thus an integral reduced surface. The nonempty D!=0 chart is ABC=1, with ring R[A^+-1,B^+-1]; clearing Laurent denominators and the successive one-variable identity principle give real Zariski density. Its only irreducible component has dimension2. H=O_S(1) is invertible and very ample even at the singular vertices.

For any real representative on S, AM-GM yields A^2+B^2+C^2>=3D^2, independent of signs. For c<3, q_c=A^2+B^2+C^2-cD^2 is positive where D!=0; at D=0 it is the strictly positive sum of the remaining squares. Local division by the square of a nonzero coordinate verifies exactly the sign convention for H^2 sections.

Fresh Scheiderer arXiv1104.1772v1 pp9-11, especially Corollary4.2 on p11, agrees with the published theorem's documented identity. It permits reduced singular projective schemes, requires density/no curve components/ample M/positive sections f of L^2 and g of M^2, and gives f*g^N SOS in sections of L*M^N for EVERY sufficiently large N. Take L=M=H, f=g=q_c; an even N gives odd m=N+1 and square roots in H0(O_S(m)).

The hypersurface exact sequence 0->O_P3(t-3)->O_P3(t)->O_S(t)->0 and H1(P3,O_P3(t-3))=0 give homogeneous polynomial lifts at t=m and identify the ideal kernel at t=2m. Consequently q_c^m-sum(H_j^2) belongs to (G). The ring substitution (A,B,C,D)=(x^2*y,x*y^2,z^3,x*y*z) kills G exactly and sends q_c to M_c. It gives the EXACT polynomial SOS identity, not a rational identity with a denominator or multiplier. The rational project's base points do not affect a ring homomorphism. Setting z=1 proves the requested affine claim.

The mixed-exponent clause is already Blekherman-Kozhasov-Reznick Theorem5.3, with the Pinelis truncation ingredient credited. Independently: for odd a,b and N=a+b-1, split (u+v)^N=v^b*B_{N,a-1}(u,v)+u^a*B_{N,b-1}(v,u). The binary even truncations are nonnegative on R^2 (strictly positive on the one-variable chart) and SOS by real factorization. The split partitions the binomial indices exactly. Substitution supplies a direct arbitrary-degree proof and handles zero polynomials and a=1 or b=1. The PR's two source display corrections are necessary: truncation index2r, and homogeneous sum through2r.

One odd SOS power propagates to all larger odd powers by multiplication by a square. No uniform exponent in c or positive endpoint c=3 conclusion follows. For c>3, f_c(1,1)<0. Together with the closed downward interval definition of c_k, eventual inclusion of every fixed c<3 gives lim c_k=3.

## Positive earlier full-result implication

The priority question is not settled by the direct proof being correct. Baldi-Blekherman-Kozhasov-Plaumann-Reznick-Sinn, Stubborn Polynomials, arXiv2602.01191v1, submitted1Feb2026, Theorem6.4 states that a nonnegative non-SOS ternary sextic with total real delta<=8 has some odd SOS power. This is an earlier public PREPRINT, not an identified journal publication. The current publisher BKR body cites that classification in Section6, although its later threshold-limit question remains printed. Neither fact asserts that those authors explicitly recognized or printed the threshold-limit consequence.

Here is the complete all-parameter bridge. For c<=0, M_c is already SOS term by term. For 0<c<3, AM-GM shows M_c>=0 and gives exactly the two real projective zeros P=[1:0:0], Q=[0:1:0]: positivity of (3-c)*x^2*y^2*z^2 forces xyz=0 at a zero; z!=0 is impossible; at z=0 the expression is x^2*y^2*(x^2+y^2).

At P, in x=1 coordinates (u,v)=(y,z), F0=u^2+u^4+v^6-c*u^2*v^2. Its multiplicity is2 and unique real tangent is u=0. Three vertical blowup strict transforms are:

F1(a,v)=a^2+a^4*v^2+v^4-c*a^2*v^2;
F2(b,v)=b^2+b^4*v^4+v^2-c*b^2*v^2;
F3(t,v)=1+t^2-c*t^2*v^2+t^4*v^6.

The first two exceptional restrictions are a^2 and b^2, so there is one real next center each. Their multiplicities are2; F2 has positive-definite tangent b^2+v^2. The third exceptional restriction is1+t^2 and has no real zero. The complementary chart restrictions at the three stages are respectively1,1,1+s^2, so no real tangent direction or intersection direction is omitted. Thus Definition6.3's real recursion adds binom(2,2)=1 at exactly three centers. By symmetry each global zero contributes3 and the total real delta is6 for EVERY0<c<3. The c-dependence occurs only in higher terms; no continuity argument from c=1 is used.

If M_c is SOS, there is nothing further to prove. Otherwise the exact hypotheses of the earlier Theorem6.4 hold, so it has an odd SOS power. This case split avoids needing an independent non-SOS criterion to apply the published statement's conditional interface. Propagation gives all larger odd powers, and the previous bound/interval argument gives limit3. This is the whole second-clause conclusion, including arbitrary real coefficients below3. It asserts neither an exponent, rate, strict threshold monotonicity nor the false positive endpoint claim. At c=3 extra global zeros appear, so delta6 is not asserted there.

The source's final proof invocation prints L=M=omega, where the preceding positivity and ampleness and its own resulting square-root degrees require omega^-1, and also a mismatched X label. These are deterministic local notation corrections, not new existence hypotheses. The principal PR proof independently proves the same conclusion using published Corollary4.2 and avoids needing the deeper preprint foundations for mathematical correctness. Priority exclusion relies on the earlier theorem-level full implication, not on a global absence search or on dating a guessed author PDF.

## Existing preparation

A separate retained effort already records the same prior-full-consequence disposition at draft_pr_actual_claims_1100_1200_20261017/audits/pr1129_30005461/ROOT_PRIORITY_DECISION.md and ACCEPTANCE_GATE.json, dated17Oct2026. Root read both, but the present families reconstructed their mathematics and priority independently before this discovery. That effort records no paper, DOI or Zenodo upload for1129. Its useful correct proof exposition remains untouched. No new record should be created for this result under the user's novel-full-solution workflow.

## Exact limit of this note

No substantive mathematical defect has been found in the actual complete two-clause claim. Subject to final independent review adoption, it is a verified prior theorem consequence and is ineligible as a novel open-problem resolution. This does not determine ultimate discovery priority or certify every foundation in the earlier preprint. Hashes establish byte custody only; the written deductions supply the reasoning.
