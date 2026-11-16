# Source-first editorial contract: record 23444050, row 153

This is an informed editorial reading, not a new blind scientific family or an independent proof certificate. Before this reading, the parent supplied the title, intended editorial role, the need to retain the binary projective convention, all-rational obstruction, positive n=0 boundary, native dates/version and CC BY rights. I also retain background from earlier catalogue/editorial tasks. These expectations were not concealed. Current root clearance/review and peer findings, archived support/audit/README acceptance/results and new public copy have not been read. The only root material viewed was the four expressly authorized original-PDF page rasters.

I personally read all 299 lines of the actual main.tex, all four native PDF pages through those individually viewed rasters, the complete native record and files API responses, and the targeted LICENSE.txt. These sources are pinned separately. No proof program, source-archive program, project helper, scientific computation, renderer, network request or Git/Sheet action was run. The ZIP/PDF bytes were hashed for identity, not executed or altered. Historical audit and program-success statements inside the paper or native metadata remain source assertions; this reading does not reproduce or certify them.

## Exact authored claim

For characteristic-two E, the paper defines H_2^(n+1)(E) using differential forms modulo Artin–Schreier images and exact forms, with H_2^1(E)=E/wp(E). K_n(E/F) is the restriction kernel from H_2^(n+1)(F) to H_2^(n+1)(E); K denotes K_1.

The target question is the three-summand equality

K_n(LK(B)/F) = K_n(L/F) + K_n(K/F) + K_n(F(B)/F),

for finite purely inseparable L/F, separable quadratic K/F, and an anisotropic bilinear Pfister form B remaining anisotropic over L. It is Question 2 in Laghribi's contribution to Oberwolfach Report 5/2016, printed page 251. The paper's negative instance is at its allowed original index n=1, hence in H_2^2; it is not failure at every index.

Take algebraically independent b,z,s,t over F_2 and

- F=F_2(b,z,s,t);
- L=F(beta), beta^4=b, of degree four and exponent two;
- K=F(theta), theta^2+theta=s^(-1), separable quadratic;
- B=<1,t>_b, with B_L anisotropic.

The class is xi=overline(s^(-4) [bz^2/(1+bz^2)] dlog z). The authored theorem states xi lies in K(LK/F), hence in K(LK(B)/F), but lies outside K(L/F)+K(K/F)+K(F(B)/F). The third individual Pfister kernel is explicitly present in the nonmembership assertion.

## Binary function-field convention

F(B) means the function field of the projective quasilinear quadric of v -> B(v,v), not a positive-dimensional quadric convention that excludes the binary case. For B=<1,t>_b, the integral zero-dimensional quadric X^2+tY^2=0 in P^1 has F(B)=F(gamma), gamma^2=t. Thus M=LF(B)=F_2(beta,z,s,gamma) and LK(B)=M(theta). Copy must state this convention sufficiently to make the binary example meaningful. It must not describe this function field as a rational curve or omit the allowed zero-dimensional quadric.

## Universal nonmembership mechanism as read

In L set f=1+beta^2 z and h=beta^2 z/f. Cohomological Artin–Schreier relations give xi_L=[s^(-1),f)_L, so the composite with K kills the class. These are equalities modulo exact forms and Artin–Schreier images; wp is not being treated as L-linear.

Assume a decomposition into the three individual kernels. The cyclic relative Brauer description makes the separable term [s^(-1),c)_F for some arbitrary c in F*. Restricting to M kills both the L and F(B) terms, so [s^(-1),f/c)_M=0. This reduction includes the entire third summand; it is not just two-field nonsplitting.

For k=F_2(b,z,t), k'=F_2(beta,z,gamma), complete M=k'(s) to D=k'((s)). With T=D(theta) and pi=theta^(-1), pi^2+s pi+s=0, N(pi)=s, and N(A+B pi)=A^2+sAB+sB^2. The even/odd valuation comparison gives valuation min(2v(A),1+2v(B)), including zero A or B separately. A unit norm therefore has square residue in k', without a perfectness or defect assumption.

For every rational c in k(s)*, write c=s^r c0(1+O(s)), r any integer and c0 in k*. Multiplying f/c by the norm s^r, also for negative r, forces (1+beta^2 z)/c0 into k'^*2. Set S=k'^2=F_2(beta^2,z^2,gamma^2) and R=F_2(beta^4,z^2,gamma^2). Since k=R(z) has degree two over R, every rational c0, including arbitrary denominators, is u+vz with u,v in R. The identity 1+beta^2 z=q(u+vz), q in S*, with z not in S, forces qu=1 and qv=beta^2. Hence u is nonzero and beta^2=v/u would belong to R, contrary to its odd valuation versus the even valuations of R. This is the source's obstruction for all rational c, not a bounded polynomial or numerical test.

## Positive boundary and construction limits

At n=0 the authored proposition proves equality for every stated datum with B positive-fold: the composite Artin–Schreier kernel is the K/F kernel and the purely inseparable and Pfister kernels are zero. An Artin–Schreier root cannot first appear in purely inseparable or rational extensions. The projective-quasilinear chart is purely inseparable quadratic over a rational field in d-2 variables; d=2 has no rational variables. Separable extension preserves the needed anisotropy. A separate zero-fold assignment F(B)=F gives the same n=0 conclusion by convention; no function field of an empty quadric is invoked.

Replacing the independent Pfister slot t by z kills dz and absorbs xi. If b=u^2 already in the base, the calculation over L gives xi_L=[s^(-1),1+uz)_L and therefore membership in the L/F plus K/F kernel sum. It does not license that single-symbol equality in the base, where d(1+uz)=u dz+z du. The repaired auxiliary exponent-one statement must not be converted back into the invalid base-symbol shortcut. The positive exponent-one regime has antecedent treatment in Aravire–Laghribi–O'Ryan (2016).

## Credit, dates, rights and later copy contract

The paper explicitly identifies its mixed class and vanishing mechanism with Aravire–Laghribi–O'Ryan's Definition 1.3/Lemma 3.1 specialization, using n=m=1, f0=1, f1=z, a=s^(-4), in the 15 August 2019 author manuscript published in J. Algebra 542 (2020), 249–276. The direct additional-third-kernel survival argument is the note's stated contribution. No firstness, global openness or causal-independence claim follows from its bounded audit statements; cited journal-body and adjacent-paper access limits remain limits, not resolved reads.

The exact native title is “An explicit counterexample to three-summand Kato-kernel splitting”, author Alec Kriebel, ORCID 0009-0001-9320-500X. Native metadata.version is 1.0.0; metadata.publication_date is 2026-10-17; created is 2026-10-18T00:29:32.173838+00:00. The PDF prints 17 October 2026 and the unrefereed/extensively-AI-assisted designation, but no numeric version. Later copy must distinguish the native version from a printed version. Native DOI is 10.5281/zenodo.23444050, concept DOI 10.5281/zenodo.23444049.

Native record/files entries order is PDF then source-and-verification ZIP; the files endpoint's explicit order array is empty. Preserve that observed entries order and exact bytes. The authored paper/code/analysis licence is CC BY 4.0 according to the actual LICENSE.txt; no MIT licence is inferred. Third-party bodies are excluded and third-party rights are retained.

The full original abstract is the TeX/PDF abstract, separately pinned from the native Description. The native Description is a longer five-paragraph deposit description including historical audit/program assertions. Later light, white, Arial copy should show the complete original abstract, keep explanatory Description/SEO concise and distinct, preserve PDF/ZIP and a faithful BibTeX citation, identify the work as unrefereed and extensively AI-assisted, and use professional contribution-based collaboration language. It should avoid internal replay instructions, diagnostic counts as proof, duplicate full Description, unqualified novelty/priority language, or an unsolicited follow-up. Default follow_up is null. No public canonical/production authority is granted by this source reading.

Source-first reading is complete. The overall editorial task remains incomplete. This frozen INITIAL will not be amended after root authority is received; informed qualifications, judgments and draft copy await that separate handoff.
