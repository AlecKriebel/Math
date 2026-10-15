# Why the full affine-group shift is a classical corollary

This is an audit derivation, not a priority claim. It concerns the exact double polygon and conventions of CURRENT_PROOF_V3.md, authenticated by SHA256 501baf64b54ab2c5b2301f7ca682a782c60446e082c3bcf066134fee620bdcde.

Put N=n-2. In odd n there is one cone. On that cone an orientation-preserving affine map has angular action equal to an increasing lift F of its derivative, plus one constant multiple of 2pi. Since F(x+pi)=F(x)+pi, the induced integral prong labels undergo one common translation. This is local angular bookkeeping and does not require a new global theorem.

For even n>=6 the two cones are exchanged by the half-turn h. Veech's original construction identifies this half-turn as hyperelliptic: [Veech1989, pp.564–565](https://gdz.sub.uni-goettingen.de/download/pdf/PPN356556735_0097/LOG_0031.pdf). The genus is at least two. The known centrality statement applies to every affine homeomorphism f, so fh=hf; see [Boissy–Lanneau, arXiv:1005.4148v2, Lemma2.3, p.8](https://arxiv.org/pdf/1005.4148v2). Their proof uses conformal conjugation and uniqueness of the hyperelliptic involution.

Let B be the synchronized angular coordinate modulo N*pi, with B(h r)=B(r). On each cone i, continuity and agreement of physical directions give

    B(f r)=F(B(r))+c_i   modulo N*pi,

where c_i is constant in pi*Z modulo N*pi. For a ray r on cone0,

    B(f h r)=B(h f r)=B(f r),
    B(h r)=B(r).

The two equations force c_1=c_0. Thus the full orientation-preserving affine group is B-uniform. For the initial and reversed-terminal rays r_+,r_- of a saddle connection, write B(r_-)-B(r_+)=k*pi modulo N*pi. The half-turn periodicity of F then gives the same difference after f. Hence K is invariant under the full orientation-preserving affine group.

The exact phrase “B-uniform” is Ferudun's coordinate formulation. His Lemma2.5 gives the implication from uniformity to K-invariance, and his explicit subgroup G0 suffices for his theorem. Extending uniformity to all f in this manner adds no credible discovery claim: it is the classical centrality lemma followed by the displayed coordinate calculation. The older framed-surface literature also uses the hyperelliptic exchange to compare angular positions at the two zeros: [Boissy2015, Proposition4.1, p.919](https://aif.centre-mersenne.org/item/10.5802/aif.2947.pdf).

This derivation does not assert that hyperelliptic symmetry alone forces every saddle connection to be invariant under h. It also does not replace the separate chord-reflection and reduction arguments needed for the signed type law. At n=4 the surface has genus one, and the above centrality theorem's genus assumption does not apply; the elementary marked-square calculation remains appropriate.
