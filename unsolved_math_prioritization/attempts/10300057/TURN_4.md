# Author turn 4: the proposed torsion pair cannot be tautly realized

**A source-backed obstruction to the specific turn-3 construction, not a general answer.** For M given by positive 15-surgery on the figure-eight knot, every cooriented taut foliation in the standard regularity covered by the cited contact-perturbation theorem has Euler class zero. Therefore neither of the plane-field classes with Euler classes 2c and8c in TURN_3 can be so realized. This turn tests and rejects that concrete route instead of treating arbitrary plane fields as taut foliations.

## 1. The Spin-c-specific Floer obstruction

We use F=Z/2 coefficients. Lin's *A remark on taut foliations and Floer homology*, proof on printed pp2–3, refines the classical nonvanishing argument. A cooriented taut foliation on a rational homology sphere Y has positive and negative contact approximations that are C0-close as plane fields. Symplectic caps and the pairing theorem give nonzero reduced Floer classes in the Spin-c structure of that plane field. In particular,

HF_red(Y,s_F) is nonzero.                            (1)

Although the theorem is stated as a total-module assertion, its proof remains in this Spin-c summand: the canonical Spin-c structures on the caps and cylinder restrict to the contact/foliation Spin-c structure on Y, and the Floer pairing respects this decomposition. A C0-small plane-field perturbation does not change that structure. The cited paper explicitly permits translation between monopole and Heegaard Floer theories using the established isomorphisms; we use only the nonvanishing consequence (1), not a new Floer comparison theorem.

This is a statement for cooriented taut foliations to which the cited contact approximation and filling theorem applies, in particular smooth cooriented taut foliations. It is not inferred for arbitrary nonsmooth distributions from integrability alone. The full argument and its regularity inputs remain credited to the cited work and its references.

## 2. The exact figure-eight complex

Hendricks–Manolescu, *Involutive Heegaard Floer homology*, Section8.2 and Figure17 (printedp53), records the ordinary doubly filtered knot Floer complex of the figure-eight knot as a direct sum over F[U,U^(-1)] of one isolated generator x and one square. We use the ordinary complex and ordinary surgery theorem, not an involutive invariant.

A convenient notation for the square indexed by n in Z is:

 a_n at (n,n), b_n at (n-1,n), c_n at (n,n-1), e_n at (n-1,n-1),

with differential

 d a_n=b_n+c_n, d b_n=d c_n=e_n, d e_n=0.

The isolated x_n is at (n,n), with zero differential. Multiplication by U shifts every index n to n-1. The label e_n here denotes the bottom-left generator of the square; it is the corresponding shifted copy of the source's e, so it is not asserted to coincide with the source's displayed unshifted e at (0,0).

For an integer s, the large-surgery quotient is

A_s^+=C{i>=0 or j>=s}.

Each whole square kept in this quotient is acyclic, as is each wholly deleted square. Only the square n=min(0,s) is partially retained:

- s>0: retain a_n,c_n, with d a_n=c_n; acyclic
- s<0: retain a_n,b_n, with d a_n=b_n; acyclic
- s=0: retain a_0,b_0,c_0, with d a_0=b_0+c_0; its homology is one copy of F, killed by U

To check that no square is overlooked, a_n is deleted exactly when n<0 and n<s, while the bottom-left generator is retained when n-1>=0 or n-1>=s. The integer gap between those two cutoffs contains just n=min(0,s). The isolated x_n generators form the usual infinite tower, starting at n=min(0,s). Therefore, up to grading shifts,

H_*(A_s^+) = T^+ plus F for s=0, and T^+ for s!=0.   (2)

The finite F in (2) is genuinely reduced: the direct sum decomposition is a U-module decomposition and the extra cycle is killed by U. No unknown extension with the tower is introduced.

## 3. Positive 15-surgery and its Euler consequence

The ordinary large-surgery formula is stated as Theorem6.8 of Hendricks–Manolescu, with its effective range explained immediately afterward and in Proposition6.9. It identifies HF^+(S^3_p(K),[s]) with H_*(A_s^+) when p>=g(K)+|s|. The figure-eight has genus one. For p=15 choose the complete set of labels -7<=s<=7; all satisfy 15>=1+|s|.

Thus (2) implies that the only Spin-c structure of M with nonzero reduced Floer homology is [0]. In the standard surgery labeling [0] is the spin structure, as explicitly stated in the source introduction. Because H^2(M;Z)=Z/15 has odd order, this is the unique self-conjugate Spin-c structure and has first Chern class zero.

Combining this with (1) forces s_F=[0], hence

e(TF)=c_1(s_F)=0.

In fact every codimension-one foliation on this M with a continuous tangent field is normally coorientable: H^1(M;Z/2)=Hom(Z/15,Z/2)=0. Thus the coorientation restriction does not leave a hidden orientation-double-cover escape on this particular manifold, although the regularity assumptions of the approximation theorem still must be respected.

The two plane fields in TURN_3 have nonzero Euler classes 2c and8c, so neither can be tangent to a taut foliation in this setting. Their finite-cover plane-field homotopy statement is unaffected, but it cannot be promoted to the required example.

## 4. What the obstruction does and does not establish

This calculation rules out the proposed torsion classes on this specific hyperbolic manifold using a foliation constraint invisible to abstract plane-field homotopy. It does not say that M has no taut foliation, that all foliations with Euler class zero are isotopic, or that other hyperbolic manifolds cannot support a relevant torsion pair. No upstairs isotopy-orbit convergence was proved or used.

`verify_square_quotients.py` checks the quotient square complexes over F2 and the degree15 arithmetic. The infinite-complex computation is justified by the cutoff argument in Section2, not by truncation alone. The source square was visually checked against Figure17; the contact-classification paper was inspected as context but is not needed for this proof.

Four substantive turns complete. The original question remains unresolved. The fifth turn should examine a genuinely foliation-sensitive descent obstruction or sufficient mechanism, without converting the surviving Euler-zero possibility into an existence assertion. Completion estimate20%, reduced after this realization route failed.
