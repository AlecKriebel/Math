# Scope correction and a counterexample to a single-level converse

Problem identifier: 30001707 / OWR-4799-003. Inspection date: 2026-10-06.

**Status: partial, with a proved correction to the catalog formulation. The original noncompact one-way conjecture is not resolved here.** The results below refute the single-orbit converse under an explicitly specified standard quantization. They also show why an unrestricted notion of a family is inadequate. No claim of a new general theorem or a resolution of the intended Oberwolfach conjecture is made.

## 1. What the original source actually asks

Kobayashi's contribution in the 2011 report, pp. 466–469, uses noncompact reductive groups G and H and assumes Q(O) is a well-defined irreducible unitary representation. Conjecture 1(1), p. 467, gives the implication

    [for every H-coadjoint orbit C, #(mu^{-1}(C)/H) <= 1]
       ==> Q(O)|_H is multiplicity-free.

It does not assert the reverse implication for a single orbit. Conjecture 1(2) states a family converse without specifying a general parameter-domain or saturation condition. Multiplicity-freeness is expressed through commutativity of the intertwiner algebra, not merely through discrete summands. The catalog's single-orbit equivalence therefore strengthens the source. This was checked in extracted text and in a rendered image of p. 467. [S1]

For a unitary representation, intertwiners here mean bounded intertwiners. For a type-I group, multiplicity-free means direct-integral multiplicity at most one almost everywhere; it need not mean a discrete decomposition. An empty quotient has cardinality zero. A nonempty quotient of cardinality one is a single H-orbit, even if its reduction is singular. A bound asserted at every geometric orbit is stronger than an almost-everywhere spectral assertion. No replacement of one of these quantifiers by another is made below.

## 2. A fully explicit failure of the single-orbit converse

### Quantization convention and groups

Use uncorrected Kähler quantization Q(M,L)=H^0(M,L), with the invariant positive Hermitian structure. Let G=SU(3), let M=CP^2 with its Fubini–Study form normalized so that the prequantum line bundle is O(1), and let

    H = {diag(e^{i theta},1,e^{-i theta}) : theta in R}.

This is a closed connected circle subgroup. Identifying su(3)^* with traceless Hermitian matrices by an invariant real pairing, the equivariant map

    [z] |-> zz*/(z*z) - I/3

identifies M with the coadjoint orbit of diag(2/3,-1/3,-1/3). Choose the pairing/KKS sign compatible with the positive Fubini–Study form. The H-moment coordinate is

    mu([z0:z1:z2]) = (|z0|^2-|z2|^2)/(|z0|^2+|z1|^2+|z2|^2).

Changing all sign conventions only replaces mu by -mu and leaves every conclusion unchanged. This fixes the quantization convention; no equivalence with a half-form or rho-shifted orbit assignment is assumed.

### Representation calculation

Global sections of O(1) are linear forms on C^3. Thus Q(M,O(1))=(C^3)^*, the irreducible dual defining representation of SU(3). On restricting to H, the three coordinate forms have distinct weights -1,0,1. The restriction is a direct sum of three inequivalent one-dimensional unitary representations. Its bounded commutant is C^3, hence it is multiplicity-free.

### Complete geometric orbit-count calculation

H is abelian, so its coadjoint orbits are the singleton levels {c}, c in R. Put

    p_j([z])=|z_j|^2/(|z0|^2+|z1|^2+|z2|^2).

Each p_j is H-invariant, sum p_j=1, and mu=p_0-p_2. Necessarily -1<=mu<=1. Equality at 1 or -1 forces respectively [1:0:0] or [0:0:1], so those quotients each have one point; levels outside [-1,1] are empty.

For every -1<c<1 and every real s in the nonempty interval

    max(0,-c) < s < (1-c)/2,

consider

    z(s)=[sqrt(s+c):sqrt(1-2s-c):sqrt(s)].

All three radicands are positive, sum to one, and mu(z(s))=c. Moreover p_2(z(s))=s. Distinct s cannot lie in the same H-orbit. There are continuum-many choices of s. Since CP^2 itself has cardinality continuum, this is also an upper bound. Consequently

    n(M,{c}) = 0                    if |c|>1,
               1                    if |c|=1,
               cardinality(R)       if |c|<1.

This is an exact argument, not an inference from numerical samples. In particular c=0 gives a failure even at an integral moment value. The same failure occurs at the regular value c=1/2, so it is not an artifact of a singular level. To check regularity, the moment map of a circle action is critical precisely at its fixed points; the three distinct coordinate weights give exactly the three coordinate fixed points with moment values 1,0,-1.

**Conclusion.** A multiplicity-free quantization at one level need not force the geometric bound. This counterexample refutes the catalog's unrestricted converse. It does not refute the implication in Section 1: here that implication's geometric hypothesis fails.

## 3. Tensor powers: an exact warning about the family quantifier

For every integer k>=1, use the scaled orbit and O(k), whose quantization is the space of homogeneous polynomials of degree k in three variables. A monomial z0^a z1^b z2^d has a+b+d=k and H-weight j=d-a. For j>=0, put d=a+j and b=k-j-2a. The permitted integers are

    0 <= a <= floor((k-j)/2).

Interchanging a and d handles j<0. Therefore the exact weight multiplicity is

    m_k(j) = floor((k-|j|)/2)+1      if |j|<=k,
             0                      otherwise.

This proves the formula for every k, not only the checked range. In particular m_1(-1)=m_1(0)=m_1(1)=1, whereas m_2(0)=2, represented by z1^2 and z0*z2. Every k>=2 has m_k(0)>=2. The full positive tensor-power family is thus not multiplicity-free. The example cannot refute a conjecture that assumes multiplicity-freeness at every positive scaling level.

There is also a precise reason that merely requiring infinitely many distinct orbits, without further control, is insufficient. Let A=R_{>0} under multiplication and set

    G'=SU(3) x A,   H'=H x A.

These are connected noncompact real reductive linear groups; they do have a compact factor, and the orbits used next are compact. For each t in R, the central coadjoint orbit {t} of A has equivariant point quantization chi_t(a)=exp(i*t*log(a)). On M_t=M x {t}, take the product quantization

    Q_t=(C^3)^* tensor chi_t.

This is irreducible and unitary for G'. Its H'-restriction has exactly the three distinct characters (-1,t),(0,t),(1,t), so it is multiplicity-free for every real t. The orbit M_t and the character chi_t vary genuinely with t. Nevertheless the moment map is (mu,t), and its quotient over {(c,t)} is exactly mu^{-1}(c)/H. Hence every member violates the geometric bound for |c|<1.

This disproves the precise universal assertion allowing arbitrary real-parameter families under this stated Kähler/product quantization. It is a warning about missing family hypotheses, **not a claimed resolution of the intended Conjecture 1(2)**: it is not a scaling family, does not have simple G', and does not supply a universal definition of the source's Q. Excluding it requires an explicit additional restriction, not a silent change of quantifiers.

## 4. Prior results in the intended noncompact setting

Kobayashi–Nasrin's 2018 paper [S3], Theorem A, treats a noncompact simple Hermitian G, a connected holomorphic symmetric subgroup H, and scalar-type elliptic orbits meeting i([k,k]+p)^perp. It proves the geometric zero-or-one bound for every H-orbit. Fact 2.1 supplies the associated scalar-type unitary lowest-weight multiplicity-free restriction theorem. The paper explicitly connects its results to the 2011 workshop announcement. These are credited prior results, not a solution produced here. Its introduction also stresses difficulties in assigning reductive orbits to irreducible unitary representations; it does not assert a universal theorem for all reductive subgroups.

An elementary noncompact benchmark already appears in [S2], Section 4, equations (4.2)–(4.5): holomorphic discrete series of SL(2,R) restricted to the positive diagonal subgroup have multiplicity-one continuous spectrum. Here is the corresponding geometric calculation, included as a reproducible check of the quantifiers. In sl(2,R), with the trace pairing, fix a>0 and write the positive elliptic orbit as

    X = [[x,y-z],[y+z,-x]],   z^2-x^2-y^2=a^2,   z>0.

The positive diagonal group diag(r,r^{-1}) fixes x and multiplies the upper-right entry b by r^2 and the lower-left entry d by r^{-2}. At fixed x, put C=a^2+x^2>0. Every matrix in the level is uniquely

    X(x,u) = [[x,-C/u],[u,-x]],   u>0.

Indeed z=(u+C/u)/2>0 and y=(u-C/u)/2. The group sends u to r^{-2}u, transitively on all u>0. Every real x occurs, so every level quotient is a singleton. The moment coordinate is x up to a fixed nonzero factor. This gives an all-real-parameter orbit calculation, and [S2] provides the matching continuous branching law. It proves only this previously known example, not the general conjecture.

Paradan [S4] provides quantization/reduction theorems for holomorphic discrete series under his stated hypotheses. Those theorems cannot automatically turn a single quantization dimension into the cardinality of an arbitrary reduced space. Hochs–Song–Yu [S5] concern compact K; their result is not an arbitrary noncompact-H theorem. The publicly accessible abstract of Nasrin's 2024 chapter [S6] describes special settings, including singular elliptic orbits; its full text was not inspected. No general solution was found in this bounded review. That search outcome is not a proof that none exists.

## 5. What is and is not established

Proved here: the explicit orbit-count formula and the single-level converse counterexample in Section 2; the all-k weight formula and stated central-family counterexample in Section 3; and the elementary orbit transitivity calculation in Section 4. The relevant standard quantizations and all hypotheses are stated. No novelty claim is made for these elementary observations.

Credited prior: the noncompact holomorphic symmetric-pair scalar-type theorem and the SL(2,R) continuous-spectrum example.

Unresolved by this work: the original one-way implication for general intended noncompact reductive pairs; a precise intended family formulation beyond the explicitly stated versions above; singular/limit parameters for which Q is zero, reducible, undefined, or convention-dependent. Such a Q is not silently admitted under the original irreducibility assumption.

The exact problem page was requested but returned HTTP 403, and the web retrieval tool could not access it. The supplied complete record was authenticated against both expected hashes, but a fresh live-page/content match is unverified. Thus the statement correction is against that authenticated record and the successfully inspected primary source.

The supplied scripts perform exact rational and finite combinatorial checks and integrity checks. They do not formally verify the analytic representation theory, authenticate external literature, establish uncountable cardinality from finite data, or certify a general mathematical solution. An independent mathematical audit remains necessary before publication.
