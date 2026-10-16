# Early independent checkpoint

Timestamp: 2026-10-15T05:23:38.470440+00:00
Completion estimate: 25% of this algebra/reproducibility review. Candidate files and older verdicts have not been read.

## Primary target read
Read the complete Motegi/Ito/Teragaito OWR 8/2020 contribution at printed pp. 491-493, including a rendered inspection of p. 493. Source: https://ems.press/content/serial-article-files/46844 (DOI 10.4171/OWR/2020/8). The final question universally fixes an arbitrary hyperbolic knot with no finite surgery, then asks for some rank-two free subgroup whose intersection with the UNION of rational-slope normal closures is trivial. It does not ask merely that the intersection of all those kernels be trivial.

The standard slope p/q is represented by mu^p lambda^q; 0 is the longitude and infinity is the meridian. Rational slopes include 0 and exclude infinity.

Read the 2026 primary https://arxiv.org/pdf/2604.01697v1 pp. 2-3 and section 7.1 at pp. 16-17. Its persistent element survives every nonmeridional filling; persistent subgroup requires this for every nonidentity element. Q7.1 fixes an arbitrary hyperbolic knot and asks for a persistent F2. The preceding paragraph separately describes lack of known hyperbolic examples. Refuting a universal statement does not settle the existential search for at least one example. Its subgroup minimizer results assume no torsion surgeries (finite or reducing); that restriction is not in the printed Q7.1.

## Independently derived obstruction
For any group G and quotient q:G -> Q with Q''=1, every subgroup H isomorphic to F2 has nonzero H'' inside ker(q). Choose an abstract free basis x,y for H (not arbitrary ambient generators). Put c=[x,y], d=xcx^-1, w=[c,d] under [a,b]=aba^-1b^-1. Then c,d are in H', so w is in H''. Direct reduction gives c=xyXY, d=xxyXYX, w=xyXYxxyXYXyxxYXX (length 16), which is nonempty and has no adjacent inverse pair. Thus w is nonidentity in free H, while q(w)=1. Consequently H meets the union of filling kernels nontrivially whenever a single admissible rational filling has metabelian group. The same slope works for every H, although the word's image in G depends on H's basis.

For a torus bundle, pi_1 = Z^2 semidirect_A Z with A in GL(2,Z), with product (v,n)(u,m)=(v+A^n u,n+m) and inverse (-A^(-n)v,-n). Projection to Z has abelian kernel Z^2; all commutators lie in that kernel, so the second derived group is trivial. This works for all unimodular A, including negative n, finite-order, unipotent and orientation-reversing A. The figure-eight's longitude filling is expected to supply this obstruction; the required independent classical topology facts (hyperbolicity, no finite rational surgery, zero filling a torus bundle) still require source authentication. Matrix checks alone cannot establish them.

## Success criteria and open checks
Authenticate these topology facts, inspect all frozen proof/scope/sources and code, reproduce all frozen JSON/byte outputs and release-verifier self-tests in isolated scratch, run independent algebra controls plus negative controls, and report scope carefully. No inference that survival of two generators implies injectivity is permitted.
