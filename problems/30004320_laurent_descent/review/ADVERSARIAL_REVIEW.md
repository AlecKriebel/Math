# Independent source and proof audit: Laurent descent (30004320)

**Verdict: PASS for all stated partial results; original unresolved, 5/5.**
AI-assisted independent mathematical review. No mandatory mathematical revision was found. This is not external peer review or a priority certification.

## Immutable target

The audit binds the 42-file author packet by FINAL_AUTHOR_MANIFEST.json SHA-256 `aa4ebd52776b5f6dbd8dbf95853f3af85851d6b194402e44797ddbbf31f2a1ee`, remotely at `b08662a16499edf37f0c0eae850cfa00b7778ed6`, branch `math/30004320-laurent-descent-wip`, folder `problems/30004320_laurent_descent` in AlecKriebel/Math. Every raw Git blob matches its frozen local bytes. No author file was changed. The author has exhausted five substantive turns.

## Source and interpretation

I checked the full Gille–Florence contribution in OWR52/2019, printed3264–3265, including visual inspection of both pages, and the quoted primary dependencies. The original asks descent of a rational point on an affine-group homogeneous space from k((t)) to k. The smooth schematic/fppf hypotheses in the packet's new statements must remain explicit. Geometric-point transitivity is not substituted for those hypotheses. The unrestricted implication is not proved or disproved here.

Florence's 2006 compactification result covers perfect fields, including positive characteristic. Florence–Gille's constant affine-group torsor theorem applies over arbitrary fields. These are credited inputs. A later status note is evidence of that author's stated status, not an exhaustive present-day priority search. Smoothness and the stabilizer restrictions are material, not cosmetic.

## Turn-by-turn analytic audit

### 1. Tame finite inertia

The tame Puiseux union has the requisite Galois projection with pro-p kernel. Its constant-field regularity and the prime-to-p inertia condition force a finite-gerbe lift to kill that kernel, thereby descending the entire object. Descending merely a neutral gerbe would be inadequate: the proof correctly retains the underlying G-torsor and uses the constant-torsor theorem to trivialize it. The pole-valuation Artin–Schreier example is a legitimate warning about removing the tame hypothesis from this method.

### 2. Wild finite inertia and the fixed-section warning

Brosnan–Reichstein–Vistoli Proposition5.6 supplies a section for a henselian discretely valued field without assuming a perfect residue field. Combined with Proposition5.5 it yields neutrality of a finite étale gerbe; the additional H1(k,G)=1 hypothesis then supplies the point. The argument does not silently claim that a section preserves every specified torsor.

For the wound group over F_p(a,b), the pole valuation at b proves that the displayed torsor has no constant point. The extension defined by v^p-tv=a is separable over the Laurent field and has purely inseparable residue extension. The s-adic additive equation for the displayed point is a genuine contraction. The residue Galois identification is compatible with constants, so the appropriate section-fixed field contains this extension. This counterexample concerns fixed-section acyclicity, not the original Laurent descent assertion.

### 3. Tori and multiplicative-type H2

The split Laurent-unit/cocharacter decomposition is equivariant over a finite splitting field, including splitting fields of degree divisible by p. Henselian specialization identifies the integral torsor term with H1(k,T). Parameter ramification multiplies the cocharacter contribution, and a finite group order kills its H1; this proves full-Puiseux H1 surjectivity. Constant torsor injectivity gives the other direction. No division by the splitting-group order is used.

A permutation-character resolution gives an exact sequence from the multiplicative-type group into a quasitrivial torus with torus quotient, even with p-torsion characters. Proper Severi–Brauer specialization gives the relevant Brauer injectivity; the cohomological sequence and torus H1 comparison then give fppf H2 injectivity. The torus-banded gerbe is neutralized and its prescribed Puiseux object matched by H1 twisting. This is stronger than neutrality and weaker than full faithfulness, exactly as stated. The nonconstant mu_p example explains why one cannot copy that object-surjectivity argument for all multiplicative-type groups.

### 4. Normal rigidification and non-smooth multiplicative isotropy

The characteristic identity torus is normal in inertia but need not be central. AOV AppendixA TheoremA.1 allows precisely a flat finitely presented normal subgroup, with no centrality or finiteness requirement. Its 2014 corrigendum concerns other portions of the paper and does not retract this rigidification theorem. The finite quotient object descends by the tame argument, and its fiber is a torus-banded gerbe. Purely inseparable stages do not change finite étale objects.

The smooth envelope proof uses the scheme-theoretic centralizer of a multiplicative-type subgroup in a smooth affine group. Conrad's smooth-centralizer and maximal-torus results apply, including to non-smooth diagonalizable subgroups. The central connected multiplicative subgroup belongs to a maximal torus: the relevant Cartan quotient is unipotent and has no nontrivial multiplicative-type image. The product S=HT is commutative of multiplicative type, S/T is étale of order prime to p, hence S is smooth, and S/H is a torus. The disconnected envelope is essential, as the PGL2 example illustrates. The quotient and torus-fiber descent retain the correct underlying torsor; no assertion that every multiplicative-type subgroup is contained in a connected torus is used.

### 5. Tame Weyl enhancement and wild Brauer obstruction

Enhancing a gerbe object by a maximal torus gives locally the classifying gerbe of its normalizer. Étale-local geometric conjugacy suffices; rational conjugacy is not asserted. Conrad's maximal-torus theorem supplies a torus over the actual Laurent field. The normalizer is smooth, its identity is the torus, and its component group is an extension of the original component group by the geometric Weyl group. The stated product-order condition therefore permits turn4's full-object descent. Forgetting the enhancement and trivializing the constant G-torsor proves precisely the asserted G(L)-orbit statement.

For the degree-p cyclic algebra, the Artin–Schreier polynomial is irreducible by its simple pole. The chosen conjugation convention is the inverse of a common book convention and is explicitly fixed; this does not affect central simplicity. At a stage t=s^(pq), the displayed complete free order has reduction F_p(a,b)(a^(1/p),b^(1/p)), a field of degree p². Lifting inverses makes every element with nonzero reduction a unit; factoring out the least coefficient valuation proves division and multiplicativity of the valuation. The proof also handles stages whose degree is not divisible by p by passing to a further stage. Since degree is prime, nonsplitting implies division, and a split algebra over the union would split at a finite stage.

If its Brauer class were constant, the equality and degree-p division representatives would agree at a finite Laurent stage. The left-regular determinant identity gives the intrinsic valuation v(Nrd)/p on both sides. The residue rings would then have to agree, contradicting the commutative degree-p² residue field versus the noncommutative constant central division algebra. This argument does not invoke an unproved defectlessness theorem. The obstruction is a nonconstant PGL_p torsor over the Laurent field, not a constant homogeneous-space counterexample. No necessity of the Weyl restriction for the original problem follows.

## Reproducibility and limits

All five author checkers reproduced their receipts byte-for-byte: 51,690; 4,325; 15,690; 10,817; 46,172, totaling **128,694** assertions. The packet verifier also verified **72** final/historical file bindings and **11** source PDFs. The independent checker adds **8,664** exact controls for integral cyclic-lattice coboundaries, reduced Artin–Schreier poles, truncated additive contraction, the Ore translation relation, residue-basis dimensions and the split left-regular determinant identity. These finite controls do not prove the infinite-field, gerbe or group-scheme statements; those were audited in the written argument against the primary inputs.

The unresolved cases include arbitrary wild noncommutative stabilizers, general unipotent isotropy, reductive stabilizers outside the tame Weyl/component condition, and any broader non-smooth acting-group formulation. The report supports **unsolved 5/5**, with substantive positive classes and method obstructions prominently retained. It does not certify historical novelty.

## Primary references examined

- Gille–Florence, OWR52/2019, pp3264–3265: https://ems.press/content/serial-article-files/46832
- Florence, compactifications over perfect fields, Propositions4.7 and5.4 and Lemma4.8: https://www.math.uni-bielefeld.de/lag/man/174.pdf
- Florence–Gille, constant torsors, Proposition5.2 and Theorem5.4: https://arxiv.org/pdf/1910.14509
- Brosnan–Reichstein–Vistoli, Propositions5.5–5.7: https://math.umd.edu/~pbrosnan/Papers/brv2.pdf
- Conrad, Propositions2.1.2,3.2.8; Lemma2.2.4; Theorems3.2.6,A.1.1 and Cartan discussion: https://math.stanford.edu/~conrad/papers/luminysga3smf.pdf
- Abramovich–Olsson–Vistoli, AppendixA: https://www.numdam.org/article/AIF_2008__58_4_1057_0.pdf ; corrigendum https://www.numdam.org/item/10.5802/aif.2869.pdf
- Gille–Szamuely, §§2.5–2.6, including the full cyclic presentation surrounding Corollary2.5.5: https://www.math.ens.psl.eu/~benoist/refs/Gille-Szamuely.pdf
