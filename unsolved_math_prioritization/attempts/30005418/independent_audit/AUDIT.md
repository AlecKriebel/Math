# Independent audit: Kähler package and Koszulness

Problem 30005418 / OWR-12697689-014, rank 797. Audit date: 5 October 2026 UTC.

## Decision

**PASS for the stated partial results and controls. The universal target remains UNSOLVED, with all five approach families used.** No substantive mathematical error was found. This is an independent AI-assisted adversarial audit, not formal verification or external human peer review. It makes no novelty, first-priority, or universal-resolution claim.

The author freeze was not modified. Its ZIP is 23,857 bytes, SHA-256 `6c6762fa475fe36c8c14c81fb9895fe9cee8489794d52cc54b08b6101b54981c`. Its manifest SHA-256 is `86dad4963c8b21ab475b2ef612c09ac499bfe11437d72ef81fbcb583c1b10553`. All eleven ZIP members and their extracted bytes match the frozen directory. Historical statements that the audit was pending remain historical. This audit supplies the later disposition separately.

## 1. Exact source and target

The full three input corpora were parsed independently, not replaced with the selected row. The 15,458 problem records, 6,701 prior-report entries, and 15,458 catalog entries have the recorded byte counts and SHA-256 hashes. The ID and problem number each select exactly one record. There is no joined prior report for this problem number. Rank 797, the statement hash, the full-record review hash using the missing-report value `{}`, and the catalog Git blob all match. A desk assessment is not an earlier substantive attempt.

The six local scholarly PDFs independently match their recorded hashes and byte counts. Fresh text extraction was performed from those PDFs; the report's printed page 379 and the talk's slide 57 were also freshly rendered and visually inspected. Source text, PDFs and rendered images are excluded from this audit package. Inspection details appear in SOURCE_INSPECTION.json; programmatic byte and join checks appear in INDEPENDENT_SOURCE_RESULTS.json.

The exact universal question is on printed p. 379 of [the published Oberwolfach report](https://ems.press/journals/owr/articles/12697689), immediately followed by a warning that hard Lefschetz alone is insufficient. The same target appears as Question 6.8 in [Mastroeni–McCullough](https://arxiv.org/abs/2111.00393v3). Neither target specifies a preassigned geometric cone.

[McCullough's slide 57](https://faculty.sites.iastate.edu/jmccullo/files/inline-files/Koszul%20algebras%20Japan%202023_0.pdf) uses a common linear element in the Lefschetz and primitive-HR conditions. Its general-field notation does not itself define positivity over an arbitrary field. [Schweitzer–Vecchi, Definitions 2.1–2.3](https://arxiv.org/abs/2601.00782v2), supplies an explicit real-field, multiplication-pairing formulation. The author's real standard-graded convention, fixed orientation, signs, and primitive exponents agree with this formulation. This is ordinary commutative algebra, with half-cohomological grading where relevant, not the anticommuting degree-one convention. No positive-characteristic HR interpretation is being certified.

The bounded literature recheck found no universal resolution. This is an observation about checked sources, not a proof that no resolution exists. The Bott–Samelson result concerns a structured quadratic-complete-intersection class. The 2026 Chow-polynomial construction supplies full-package algebras with specified Hilbert series without universally supplying quadratic presentations. Neither result eliminates the recorded gap.

## 2. One full-package element versus a mixed cone

Proposition 1 is valid for its local, existential statement. At the diagonal tuple, every required Lefschetz map is invertible. For i at least 1, the primitive map from A^i onto A^(d-i+1) is surjective: on the subspace ell A^(i-1), its composite with multiplication by ell is the preceding-degree Lefschetz isomorphism with exponent d-2i+2. This also shows that multiplication by ell into that subspace is injective. For i=0 the primitive target is zero.

Consequently the primitive kernels have locally constant dimension, and their restricted symmetric forms vary continuously in local bases. Invertibility and positive definiteness hold on an open neighborhood of each diagonal tuple. There are finitely many degrees. A sufficiently small common affine-slice ball has every relevant Cartesian power inside those neighborhoods. Positive radial rescaling produces an open convex cone and preserves the signs and kernels.

This argument also covers the middle-degree empty Lefschetz product and socle degree one. It proves the existence of a small mixed cone for a fixed algebra and orientation. It does not prove HR on an independently prescribed ample cone, nor does it preserve quadraticity or off-diagonal Tor under deformation of the algebra. The author explicitly retains all those limitations.

## 3. Square-zero obstruction

For d at least 2, multiplication and duality make B_ell(a,b)=deg(ab ell^(d-2)) nondegenerate. The ell line is positive; its orthogonal complement is exactly the primitive degree-one subspace and is negative definite. The signature is therefore (1,h1-1).

If WW=0 and dim W is at least 2, the restriction of the linear functional B_ell(ell,-) to W has a nonzero kernel element w. Then w is primitive but B_ell(w,w)=0, contradicting negative definiteness. This is a Witt-index-one argument. It excludes the type-at-least-two degree-one idealization route globally, not merely at a tested Lefschetz element. It does not exclude all quadratic Gorenstein algebras.

## 4. Credited hard-Lefschetz non-Koszul control

The six base quadrics coincide with the characteristic-zero construction in [McCullough–Seceleanu, Theorem 3.2](https://arxiv.org/abs/2004.10237v2), itself credited there to Roos. The source's canonical-module shift notation need not be interpreted to verify the packet: its explicit graded dual construction A^i=R_i direct-sum (R_(3-i))* unambiguously fixes the algebra.

The independent checker does not import, execute as a library, or copy the author's arithmetic code. It uses SymPy 1.14.0 over Q, independently computes Gröbner bases, reconstructs the multiplication table, and builds bar differentials with a different word ordering. The author's certificate is read only as coefficient data to test.

Independent findings:

- The base has Hilbert function (1,4,4,0,0). Every cubic monomial reduces to zero.
- The multiplication kernel has 28 quadrics. A separately computed Gröbner basis of their ideal has 35 members and Hilbert function (1,8,8,1,0,0), proving the quadratic presentation. The ideal's ranks in degrees 2,3,4 are 28,119,330. A Gröbner basis need not itself be quadratic for an ideal to be generated by quadrics.
- Multiplication by z in the asserted R bases has determinant -1 and the displayed matrix. The A^1–A^2 pairing is perfect. All 512 generator-triple associativity checks pass; the full multiplication is also justified by the dual-module law.
- For L=z+eta, deg(L^3)=3 and det(B_L)=1. Exact characteristic-polynomial root isolation yields inertia (4,4,0). On the primitive subspace, Q1 has inertia (4,3,0). Thus both required Lefschetz maps are isomorphisms, while HR fails.
- The four dual degree-one generators span a square-zero subspace. Proposition 2 rules out HR at every possible element, regardless of the orientation. This algebra is not a target counterexample.

The bar chain-group dimensions in internal degree 4 are 16,192,256 for homological degrees 2,3,4. The independent rational ranks of d3 and d4 are 16 and 175, and d3 d4 is zero. Thus Tor_(3,4) has dimension 1. The proposed two-term cycle is a cycle because u^2+uz=0 and R3=0. Adjoining it to the boundary matrix increases the rank from 175 to 176. The supplied 62-term rational separating cocycle annihilates every boundary and pairs to 1 with the cycle; a fresh exact nullspace computation produces a separately verified separating functional as well.

No rank over a finite field is lifted to Q. All these computations use exact characteristic-zero arithmetic. The augmentation-preserving inclusion R to A and projection A to R split the normalized bar complexes, so the nonzero class remains nonzero in A. This proves non-Koszulness without a Hilbert-series test. Faithful scalar extension from Q to R preserves this Tor certificate.

## 5. Low-socle theorem and the infinite affirmative family

For d=0 the algebra is the ground field. For d=1, duality gives the one-variable square-zero algebra. For d=2, HR makes the multiplication pairing Lorentzian. The one-variable cubic-truncation case is not quadratic. For n at least 2, the asserted real hyperbolic basis exists and gives precisely the displayed presentation B_n.

Under the specified grevlex order the proposed leading monomials are every degree-two monomial except uv. Therefore the candidate initial quotient has standard monomials 1, the degree-one generators, and uv only. The presentation surjects onto the known (1,n,1) multiplication algebra, so the upper and lower Hilbert bounds agree in every degree. This proves the quadratic Gröbner basis for every n, without extrapolating from finite tests. The standard quadratic-Gröbner-basis criterion implies Koszulness; the cited source explicitly recalls this known criterion. The socle-degree-two result is not claimed as new.

Adjoining an independent t with t^2=0 preserves the quadratic Gröbner basis, proving the entire family A_n Koszul. The standard monomials and the product pairing also prove its stated Hilbert vector and Gorenstein property.

For the full asserted cone, write L=a+st with a in one timelike component and s>0. The form is the block matrix with upper-left block sB, off-diagonal Ba, and bottom-right zero. Its Schur complement is -B(a,a)/s, so its inertia is (1,n). The cube is 3sB(a,a)>0, hence the degree-one primitive form is positive definite.

For mixed degree one, two future timelike a0,a1 have B(a0,a1)>0. Thus B_(L1)(L0,L0)=s1 B(a0,a0)+2s0 B(a0,a1)>0. The orthogonal complement of this positive line in a Lorentz form is negative definite and is exactly the stated mixed primitive kernel. For mixed degree zero, each of the three summands in the displayed cubic product is positive. These are all relevant degrees in socle degree three. This proves the whole cone uniformly; sampled tuples are controls only.

The independent checker verifies quadratic Gröbner presentations for n=2 through 12, the exact primitive diagonal (2,1,...,1,6), 33 additional rational cone points, 99 mixed pairs using Sylvester's exact determinant criterion, and 297 triples. At n=7, the Hilbert vector matches the idealization's (1,8,8,1), so the contrast is valid. Equality of Hilbert vectors is not an equality of algebras or a Koszulness test.

## 6. Apolar control and stopping boundary

For a cubic F with no degree-one annihilators, apolar duality gives (1,e,e,1). With top evaluation divided by 6, direct differentiation gives deg(L^3)=F(l) and B_L=Hess(F)(l)/6. Positive cube and Lorentzian Hessian are therefore exactly the degree-zero and degree-one package conditions. They impose no automatic quadratic presentation.

For F=X^3-Y^3, the independently checked quotient has Hilbert function (1,2,2,1,0,0). At L=2x+y the cube is 7, B_L=diag(2,-1), and x+4y is primitive with Q1-value 14. The sole quadratic relation xy does not generate x^3+y^3. It is a valid HR, nonquadratic, non-Koszul control, not a target counterexample.

No construction in the packet simultaneously provides quadraticity, full HR, and non-Koszulness. No argument covers all remaining socle degrees. The five-family stop is respected: this audit reconstructs and challenges existing claims and adds verification controls, not a sixth search for a general proof or counterexample.

## 7. Reproducibility and limits

The author verifier passes with the externally supplied manifest digest and regenerates the author's math output byte-for-byte. The independent verifier passes over Q. Full-source hashing and joining pass separately, with no source bytes distributed. The audit wrapper checks strict inventories, frozen author bindings, optional original ZIP bytes, and exact arithmetic replay; it rejects optimized Python. The audit includes explicit correction/scope notes, even though no mathematical correction was required.

Normal and relocated final-package replay results are recorded in the delivery receipt. Replays certify the listed computations and file bindings, not universal mathematics, literature exhaustiveness, the behavior of all package versions, or new source inspection. Only authored audit/proof discussion, code, results, and public verification metadata are distributed. No remote write, release, DOI, or contact with a third party was made by this audit.
