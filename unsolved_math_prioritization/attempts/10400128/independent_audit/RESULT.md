# Problem 10400128: scoped audit of Seifert optimistic limits

## Disposition

**Original target unresolved; five substantive approaches, 5/5.** This is a bounded partial and source-scope correction, not a solution, a counterexample to the original formal question, or a novelty claim. Independent review is pending at this author freeze. No publication was performed.

The source is H. Murakami's Problem 7.13 in T. Ohtsuki (editor), *Problems on invariants of knots and 3-manifolds*, printed page 482, PDF page 110. It asks for the optimistic value of N^(-1) log(tau_N^{SU(2)}(M)) for Seifert fibered 3-manifolds. Its adjacent discussion expressly leaves the rigorous definition unsettled. We use the closed oriented setting and the ordinary SU(2) root q=exp(2 pi i/N), shifted level N, actual level N-2. The factor 2 pi i in the preceding conjecture is not part of the quantity asked for in Problem 7.13. [S1,S2]

## Established results

1. A standard Heegaard/TQFT argument gives |tau_N(M)| <= D_N^g for a genus-g Heegaard splitting, where tau_N(S^3)=1 and D_N=sqrt(N/2)/sin(pi/N). This is an upper bound; it supplies no nonvanishing or lower bound.
2. For +8 surgery on the unknot, the branch-corrected formal prescription applied to the displayed surgery sum has two regular critical values pi^2/2 and 2 pi^2 for the quantity with factor 2 pi i. Equivalently, the candidate values for the quantity in Problem 7.13 are -i pi/4 and -i pi. They are distinct even modulo 4 pi^2 before dividing by 2 pi i. This calculates a presentation-dependent formal candidate set, without selecting a contour or declaring either candidate to be the requested invariant.
3. The classical example RP^3=L(2,1) has tau_N=0 for every odd N. For even N its absolute value is 1/[sqrt(2) cos(pi/(2N))]. Hence the ordinary all-level logarithm is undefined infinitely often; extending log|0| to -infinity gives liminf=-infinity and limsup=0 after division by N. Kirby and Melvin already record the stronger exact real-valued even-level formula. Our cancellation and modulus derivations are supplied as transparent checks, not new topology. [S3]
4. A finite rational-phase asymptotic expansion has principal-log/N limit zero on each residue class with a surviving nonzero leading coefficient. Cancellation of every coefficient on a class prevents that inference. Arbitrary choices of logarithm can introduce any prescribed purely imaginary limiting shift. Thus an asymptotic expansion is not by itself a canonical optimistic-limit selection rule.

5. For every identity mapping torus Sigma_g x S^1, the positive Verlinde trace gives a genuine ordinary logarithmic rate of zero. Explicit two-sided polynomial bounds are supplied; this is a classical-formula consequence in a constructive Seifert subclass, not a canonical formal-branch theorem. [S7]

Full analytic arguments and conventions are in PROOF.md. There is no numerical evidence standing in for a proof, and no executable mathematical checker is needed for these arguments.

## Literature position

Hansen's 2005 preprint gives broad Seifert asymptotic results, with explicit scope limitations. Andersen–Han–Li–Mistegard–Sauzin–Sun's 2025 preprint proves the asymptotic expansion conjecture for Seifert integral homology spheres; its current arXiv page still lists only v1. These are credited results about expansions, not a verified all-Seifert answer to the source's formal selection problem. Murakami–Tran's published torus-surgery theorem uses exp(4 pi i/n), odd n, and additional surgery hypotheses, so it cannot silently replace the root and manifold scope here. See SOURCES.md for precise qualifications.

## Remaining gap

A full resolution would need a specified, invariant formal prescription for the entire intended Seifert class, including admissible presentation, logarithm/dilogarithm lifts, critical-point or critical-component selection, and treatment of zero/amplitude-degenerate terms; then prove invariance and compute its result. If the aim is an actual asymptotic statement, integration cycles, errors, phase cancellation, normalizations, and zero subsequences also have to be addressed. Neither the partial results here nor the inspected sources fill that complete gap. This bounded search does not certify that every possible later paper has been excluded.

The exact target and complete inherited report were checked before mathematical work. The inherited report was generic literature triage, without a substantive proof attempt. Targeted GitHub searches returned no prior target attempt. This is a negative-search observation, not proof of historical absence. INPUT_METADATA.json records the exact input hashes; SOURCE_METADATA.json records reading-copy hashes and inspected portions. No source PDFs, source text, source images, or full datasets are part of this authored packet.
