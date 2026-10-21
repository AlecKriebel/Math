# Resolving incidence can destroy the normal-bundle hypothesis

One tempting route is to resolve the incidence graph, use its projection to the parameter space as a fibration, and apply an algebraicity theorem for equidimensional fibrations. The normal bundle of a lift of Y must then be checked anew.

Here is an exact example inside the original geometric category. Let Z=P³, let o∈Z, and let S=P² parameterize the lines through o. Its incidence graph G is Bl_o(P³). The evaluation G→P³ is a modification, while the second projection π:G→P² is a P¹-bundle.

Choose Y to be a line through o. Its normal bundle in Z is O_{P¹}(1)⊕O_{P¹}(1), which is Griffiths-positive. The strict transform Ỹ⊂G is a fibre of π. Since π is smooth near this fibre,

    N_{Ỹ/G} ≅ (T_{P²,[Y]})⊗O_{Ỹ} ≅ O_{P¹}^{⊕2}.

Indeed, the tangent sequence of a smooth submersion restricted to a fibre identifies the normal bundle with the pullback of the tangent space of the base. Thus the lift no longer has an ample or Griffiths-positive normal bundle. Algebraic dimension is preserved by the modification, but this does not preserve the hypothesis needed for the fibration theorem.

The example does not contradict the target: a(P³)=3. It proves that the passage to a birational incidence graph is not, by itself, a legitimate reduction to the known positive-normal fibration case. A successful version requires a different lift or a theorem controlling the resulting degenerate normal directions.
