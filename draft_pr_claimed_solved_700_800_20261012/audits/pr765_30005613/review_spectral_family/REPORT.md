# Independent operator-theoretic and spectral-completeness audit

Date UTC: 2026-10-16T04:46:43.060884+00:00. Target: claimed_solved draft PR #765, problem 30005613 / OWR-14297736-021. Exact frozen head: 021518f6f65a86658f72e0b31bfa0814bf1aa25d.

## Verdict

PASS for the claimed spectral mechanism and its application to the stated existential tower construction. I found zero mathematical issues requiring repair. The strongest verified conclusion is: for each integer d>=2, the existing countable induction, using the established finite-window norm-resolvent fact, yields a connected open quasi-conical domain with a complete orthonormal eigenbasis for its Dirichlet Laplacian A, with spectrum(A)=essential_spectrum(A)=[0,infinity), no zero eigenvalue, and H_ac(A)=H_sc(A)={0}.

The analytic dependency is explicit: finite-window norm-resolvent convergence for bounded partial towers with earlier windows held fixed. I verified that the cited primary-source result supplies precisely this input and that its geometric hypotheses apply. This report does not replace the independent geometry/capacity family, certify historical novelty, review a later preprint package, or assert a result for arbitrary preassigned cube widths. There is no unresolved spectral-completeness gap after that established analytic input is supplied.

## Independence, frozen inputs, and scope

I read the complete selected problem record, including its empty prior report, and the full author proof before reading inherited audit opinions, favorable verdicts, README claims, or another family’s mathematics. INDEPENDENT_DERIVATION.md records the early independent position and abstract reduction. I have not needed to read any historical audit or verdict during this review.

The inspected proof is original/unsolved_math_prioritization/attempts/30005613/author/PROOF.md, 14,044 bytes, SHA256 5d1bab0b62ac5f78c69b0d82babd0b79fa4944097470fa760fdb3c485e362a20. The root supplied the immutable source and eligibility receipts. I verified this proof hash directly. I did not mutate the original candidate, Git index, refs, branches, queue, other targets, or external applications. All authored material is confined to this review directory. This was verification of a saved candidate, not an original search turn or scope extension. No communication with external people occurred.

The mathematical goal is existential in both widths and apertures. The original OWR passage requests a domain in the expanding-tower construction; it does not impose a specific numerical width sequence. KL Section 3 expressly leaves later centers free and selects them during induction. Thus the candidate’s stated freedom is supported rather than silently substituted for a prescribed-tower theorem.

## Checkable independent abstract theorem

Let H be a Hilbert space, R_n uniformly bounded self-adjoint operators converging strongly to a genuine injective nonnegative resolvent R=(A+1)^(-1), and P_n^k, 1<=k<=n, finite-rank orthogonal projections. Suppose:

1. [R_n,P_n^k]=0 and P_n^1<=...<=P_n^n.
2. For n>=k, ||P_(n+1)^k-P_n^k||<=e_n where sum(e_n)<infinity, and the transported ranks are fixed for each k.
3. There is an orthonormal basis B and finite probe sets F_n increasing to B, with ||(I-P_n^n)f||<=eta_n for f in F_n and eta_n->0.

Then H_pp(A)=H.

Proof. For fixed k the projections are Cauchy in norm, hence converge in norm to an orthogonal projection P^k. Their limit has the same finite rank, because at large n their distance is less than 1; the maps between the two ranges induced by the two projections are injective. Also ||P^k-P_n^k||<=sum_(j>=n)e_j. Nesting passes to the limit.

For f in H,

||R_n P_n^k f - R P^k f|| <= ||R_n|| ||(P_n^k-P^k)f|| + ||(R_n-R)P^k f|| -> 0.

Likewise,

||P_n^k R_n f-P^k Rf|| <= ||(P_n^k-P^k)R_n f|| + ||P^k(R_n-R)f|| -> 0.

Hence [R,P^k]=0. The range of P^k is finite-dimensional and reducing for R. The finite-dimensional restriction has an orthonormal eigenbasis. Every eigenvalue mu is positive, because R>=0 and ker(R)={0}. If Rv=mu v, then v=mu^(-1)Rv belongs to dom(A), and Av=(mu^(-1)-1)v. Thus ran(P^k) is contained in H_pp(A).

For any fixed basis vector f, eventually f belongs to every F_n. Therefore

dist(f,H_pp(A)) <= ||f-P^n f|| <= eta_n + sum_(j>=n)e_j -> 0.

H_pp(A) is closed by its definition as the closed span of all eigenvectors. Every basis vector belongs to it, proving the theorem. Both continuous subspaces vanish by the orthogonal spectral-type decomposition. This proof neither infers completeness from dense eigenvalues nor invokes a trace-class theorem to eliminate singular continuous spectrum.

The candidate has e_n=2^(-n-2), tail sum 2^(-n-1), and eta_n=2^(-n). The bound is uniform over all k<=n, so using k=n in the diagonal completeness argument is valid even though the birth rank may grow with n. One does not interchange two unproved limits.

## Finite construction and multiplicities

Every partial tower is bounded, and the Dirichlet form domain extends by zero into H_0^1 of a containing box. Compact embedding gives compact resolvent; the containing-box Poincare inequality makes its eigenvalues positive. These statements require no global smoothness of the slit domain.

At stage n the protected projection P_n^n is finite rank and is a sum of complete eigenspace projections. Its finite spectral set S_n is positive. A resonance with a next cube of half-width a requires

lambda = pi^2 (m_1^2+...+m_d^2)/(4a^2).

Restricting a to (a_n+1,a_n+2) and lambda to finite S_n bounds every m_i. Only finitely many candidate widths are excluded, so a valid next width exists. This step changes neither previous geometry nor previous protections. Exact coincidence avoidance is sufficient; no quantitative spectral-gap lower bound is used.

For the disconnected union of the old partial tower and the nonresonant new cube, each protected lambda is isolated and has exactly the old full eigenspace, extended by zero. A small disjoint interval around each such lambda contains no other disconnected eigenvalue. Norm-resolvent convergence, equivalently norm convergence of the bounded resolvents, gives norm convergence of all of these cluster projections by a contour integral around each corresponding nonzero isolated resolvent eigenvalue.

The protection operates on full clusters. A multiple eigenvalue may split, but every split eigenspace within its isolating interval is retained. Sums over the appropriate intervals remain nested; distinct spectral intervals cannot share only part of an eigenspace. Because there are finitely many protected families at stage n, one positive aperture can satisfy all requested norm bounds simultaneously. Norm distance less than 1 preserves ranks. There is no circular demand to avoid the infinitely many future eigenvalues.

After transport, compact-resolvent completeness permits a finite birth cutoff above every protected eigenvalue and sufficiently high to approximate the finite probe set. The previously transported projections need not themselves remain lower spectral cutoffs. The proof explicitly permits selected finite spectral unions after birth, which is essential and valid.

## Common Hilbert space and the exhaustion

When an aperture half-width delta is less than the adjacent cube widths, the added aperture cube contributes only its middle interface face outside those cubes. This has d-dimensional Lebesgue measure zero. All partial and final L2 identifications can therefore be realized within the fixed direct sum of the final cube L2 spaces, with partial operators and projections extended by zero on the unused summands. Distances and ranks of projections are preserved by this isometric identification.

The cube sine bases are fixed at each cube’s creation. Their union is an orthonormal basis of the final H. The sets F_n={f_(j,l):j<=n,l<=n} are finite and exhaust that basis, revisiting every fixed vector indefinitely. These vectors are used solely as L2 probes; no assertion about their zero extensions being in dom(A) is required.

The open sets O_n increase to O. Their zero-extended H_0^1 spaces V_n are closed nested subspaces of V=H_0^1(O) for the form norm b(u,u)=||grad u||^2+||u||^2. A compact support in O is contained in some O_N because a finite subcover can be selected from the increasing open cover. Thus the union of V_n is form-dense in V. For f in H, the partial resolvent solution R_n f is the b-orthogonal projection of Rf onto V_n. It converges in form norm, hence in L2. This proves the required strong resolvent convergence directly and identifies R as the actual final-domain resolvent, so its injectivity is justified independently of projection transport.

## Finite-window input and primary-source applicability

[KL v2](https://arxiv.org/pdf/2205.08172v2), PDF pp.3–5, gives decreasing-domain Mosco convergence, bounded-domain norm convergence of zero-extended resolvents, and their application to the first and subsequent fixed-window interconnections. Its Section 3 leaves later centers unfixed. The inspected version is 20 May 2024; the published paper DOI is [10.1112/blms.13113](https://doi.org/10.1112/blms.13113).

For the candidate, fixing earlier windows and the next width gives a bounded decreasing family D_delta. Its only persistent newly included boundary point is the interface center p; all other added interface points disappear as delta->0. In detail, the new interface patch has transverse coordinates |x_i|<delta, so the intersection of its closures is {p}; int(intersection D_delta)=D_0 for d>=2. The point is removable for H1 in these dimensions. The cited propositions consequently apply with Gamma={p}; no interface edge, previous aperture, positive-measure neck, or unbounded-set compactness assertion is smuggled into this step. Norm convergence follows along any decreasing aperture sequence, sufficient for all finite stage choices. No additional spectral input is required from KL’s trace-class argument.

The [official OWR report](https://ems.press/content/serial-article-files/47475), printed pp.2077–2078 (PDF pp.61–62), presents the expanding-cube construction and poses elimination of both continuous spectral types on such a domain. The [2026 survey v1](https://arxiv.org/pdf/2609.28602v1), PDF p.16, repeats the singular continuous question as Open Problem 1. Their formulations support the existential scope checked here. The survey’s displayed equality of the entire spectral set with point spectrum for the disconnected tower is imprecise under the standard countable-eigenvalue definition; I do not use it. The candidate correctly distinguishes pure point type from every spectral point being an eigenvalue.

SOURCE_RECEIPTS.json records URLs, exact downloaded PDF hashes, dates, versions, and inspected page scopes. Complete relevant pages were rendered with Poppler and visually inspected, including the closure bars in Proposition 2.2/2.3. The ordinary OWR DOI open failed; the publicly accessible official publisher PDF was used. The web screenshot function failed as unsupported, so the local renders supplied the page check. Source bodies, extracts, and renders are temporary and will not be redistributed.

## Spectrum, weak escape, and zero

The half-widths grow at least linearly, so O contains arbitrarily large balls, is connected and open, and has infinite measure. For lambda>=0 choose |xi|^2=lambda and a unit-norm smooth compactly supported chi in the unit ball. With r_n=a_n/2 and cube center c_n, set

u_n(x)=r_n^(-d/2) chi((x-c_n)/r_n) exp(i xi dot x).

It is in C_c^infinity(O), hence dom(A), and ||u_n||=1. A acts as -Delta on such functions, and the product rule gives

||(A-lambda)u_n|| <= r_n^(-2)||Delta chi|| + 2|xi|r_n^(-1)||grad chi|| -> 0.

The supports lie in pairwise disjoint cubes, so the u_n are orthonormal and therefore weakly zero by Bessel’s inequality. This is a singular Weyl sequence for every lambda>=0, including zero. It establishes the entire essential spectrum [0,infinity); nonnegativity excludes anything below zero. Since the eigenvectors are complete, the spectral set is the closure of the point eigenvalues, proving density.

If Au=0 then the form identity gives ||grad u||=0. An H1 function with zero weak gradient is constant on a connected open set. An L2 constant on O must be zero because O has infinite measure. Thus zero is not an eigenvalue. Approximate zero modes and zero in the essential spectrum are fully compatible with this conclusion.

## Adversarial diagnostics and reproducibility

ADVERSARIAL_CHECKS.md proves four independent counterexamples to weakened mechanisms: rank-one projections escaping strongly to zero; exactly transported finite eigenfamilies missing a nonzero absolutely or singular continuous summand despite dense point eigenvalues; a noninjective resolvent limit allowing one protected vector’s energy to diverge; and a rotating branch inside a split multiple eigenspace that cannot transport an arbitrary initial rank-one vector. Each is explicitly excluded by a condition present in the candidate.

The standard-library controls.py uses exact rational arithmetic. It verifies split clusters and nested rank-two/rank-three projections at four rotation scales, all projection/commutation identities, and the rank-one negative control. It also exhausts a finite two-dimensional forbidden-width example and exhibits a valid width. Run python3 -B controls.py from this directory. CONTROLS_RESULTS.json records all passing assertions. CONTROL_RECEIPT.json records the exact code/result hashes, command, exit status, and honest timing bounds. The controls are diagnostic; the PDE input and infinite completeness conclusion rest on the source theorem and analytic deductions above.

## Final disposition

Issue count: 0. Repairs required: none. Exact remaining mathematical gap within this family’s reviewed claim: none, taking the precisely cited finite-window convergence theorem as an established external analytic input. The independent geometry/capacity family should still report its own judgment of that input. Historical priority, broader literature completeness, and whole-preprint presentation are outside this audit and receive no verdict here.
