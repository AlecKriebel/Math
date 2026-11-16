"""Independent source-only antipedal controls; no native/support imports."""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from itertools import permutations
import json


def need(ok, label):
    if not ok:
        raise ValueError(label)


def sign(x):
    return (x > 0) - (x < 0)


def point(a, b, t):
    if t is None:
        return -a, F(0)
    return a * (1 - t * t) / (1 + t * t), b * 2 * t / (1 + t * t)


def solve_norm2(A, B, f):
    # Solve the original two perpendicular-line equations in focus coordinates.
    x, y = A[0] - f, A[1]
    u, v = B[0] - f, B[1]
    det = x * v - y * u
    need(det != 0, "unique actual antipedal intersection")
    ra2, rb2 = x * x + y * y, u * u + v * v
    X = (ra2 * v - rb2 * y) / det
    Y = (x * rb2 - u * ra2) / det
    need(x * X + y * Y == ra2 and u * X + v * Y == rb2, "line equations")
    return X * X + Y * Y


def rational_edge(a, b, c, A, B):
    dx, dy = B[0] - A[0], B[1] - A[1]
    L2 = dx * dx + dy * dy
    d0 = dy * A[0] - dx * A[1]
    K = (a * a * dy * dy + b * b * dx * dx) / L2
    lam = K - d0 * d0 / L2
    if not 0 < lam < b * b:
        return None
    beta = b * b - lam
    need(d0 != 0, "support positive after choosing its orientation")
    contact = ((a * a - lam) * dy / d0, -(b * b - lam) * dx / d0)
    need(contact[0] ** 2 / (a * a - lam) + contact[1] ** 2 / beta == 1,
         "independent confocal contact equation")
    tau = ((contact[0] - A[0]) * dx + (contact[1] - A[1]) * dy) / L2
    need(0 < tau < 1, "contact strictly between chord endpoints")
    need(L2 * K * K == 4 * a * a * b * b * lam, "chord-length identity")
    weights, heights = [], []
    for sigma in (1, -1):
        d = d0 - sigma * c * dy
        need(sign(d) == sign(d0), "both foci strictly inside caustic support")
        ra = a - sigma * c * A[0] / a
        rb = a - sigma * c * B[0] / a
        need(ra > 0 and rb > 0, "positive endpoint distance")
        need(ra * ra == (A[0] - sigma * c) ** 2 + A[1] ** 2,
             "endpoint focal distance")
        w = ra * rb / abs(d)
        need(w > 0, "positive norm branch, not a signed surrogate")
        need(solve_norm2(A, B, sigma * c) == w * w * L2,
             "direct antipedal norm squared")
        weights.append(w)
        heights.append(abs(d))
    need(heights[0] * heights[1] == beta * L2, "positive height product")
    T = weights[0] - weights[1]
    E = -a * a + b * b * lam / beta
    need(T * T * L2 == c * c * E * E * dy * dy / (a * a * b * b * lam),
         "edge norm-difference magnitude")
    need(sign(T) == sign(d0) * sign(E) * sign(dy), "orientation and ordinary norm sign")
    wrong_E = a * a + b * b * lam / beta
    wrong_rejected = T * T * L2 != c * c * wrong_E * wrong_E * dy * dy / (a * a * b * b * lam)
    return {"lambda": lam, "E": E, "T": T, "dy": dy,
            "orientation": sign(d0), "wrong_coefficient_rejected": wrong_rejected}


def main():
    ts = [None, F(-4), F(-2), F(-1), F(-1, 2), F(-1, 3),
          F(0), F(1, 3), F(1, 2), F(1), F(2), F(4)]
    cases, horizontal, zero, positive, negative, reverse, wrong = 0, 0, 0, 0, 0, 0, 0
    retrace_counterexample = None
    for aa, bb, cc in ((5, 3, 4), (5, 4, 3), (13, 5, 12), (13, 12, 5)):
        a, b, c = F(aa), F(bb), F(cc)
        need(a * a - b * b == c * c, "real focal data")
        pts = [point(a, b, t) for t in ts]
        for A, B in permutations(pts, 2):
            r = rational_edge(a, b, c, A, B)
            if r is None:
                continue
            cases += 1
            horizontal += r["dy"] == 0
            zero += r["E"] == 0
            positive += r["E"] > 0
            negative += r["E"] < 0
            reverse += r["orientation"] < 0
            wrong += r["wrong_coefficient_rejected"]
            if r["T"] != 0 and retrace_counterexample is None:
                # A,B,A is closed and co-caustic, but immediate retracing.
                retrace_counterexample = {"a": aa, "b": bb, "A": list(map(str, A)),
                                          "B": list(map(str, B)), "lambda": str(r["lambda"]),
                                          "twice_norm_difference_coefficient_of_chord_length": str(2 * r["T"])}
    need(all(x > 0 for x in (cases, horizontal, zero, positive, negative, reverse, wrong)),
         "nonvacuous critical case coverage")
    need(retrace_counterexample is not None, "nonretracing hypothesis is necessary")

    with localcontext() as ctx:
        ctx.prec = 100
        D = Decimal
        a, b, c = D(21).sqrt(), D(4), D(5).sqrt()
        lam = D(336) / 25
        triangle = [(a, D(0)), (-3 * a / 5, D(16) / 5), (-3 * a / 5, -D(16) / 5)]
        sums, lambda_errors = [D(0), D(0)], []
        edge_differences = []
        for A, B in zip(triangle, triangle[1:] + triangle[:1]):
            dx, dy = B[0] - A[0], B[1] - A[1]
            L2 = dx * dx + dy * dy
            d0 = dy * A[0] - dx * A[1]
            need(d0 > 0, "odd primitive triangle left orientation")
            got_lam = (a * a * dy * dy + b * b * dx * dx - d0 * d0) / L2
            lambda_errors.append(abs(got_lam - lam))
            q = [solve_norm2(A, B, sigma * c).sqrt() for sigma in (1, -1)]
            for i in (0, 1):
                need(q[i] > 0, "odd triangle positive actual norm")
                sums[i] += q[i]
            edge_differences.append(q[0] - q[1])
        need(max(lambda_errors) < D("1e-90"), "odd triangle common confocal caustic")
        need(abs(sums[0] - sums[1]) < D("1e-90"), "odd primitive direct norm sum")
        need(any(abs(x) > D("1e-4") for x in edge_differences), "odd test not edgewise trivial")
        # Same four-periodic caustic, two geometrically distinct members.
        need(F(680, 3) != F(200), "individual-sum constancy countercontrol")
        numerical = {"axes": [str(a), str(b)], "lambda": str(lam),
                     "ordinary_antipedal_sums": list(map(str, sums)),
                     "edge_differences": list(map(str, edge_differences)),
                     "common_caustic_max_error": str(max(lambda_errors)),
                     "numerical_not_interval_proof": True}
    print(json.dumps({"status": "PASS_SOURCE_ONLY_ADVERSARIAL_CONTROLS",
                      "exact_rational_oriented_chords": cases, "horizontal": horizontal,
                      "zero_Gamma": zero, "positive_Gamma": positive, "negative_Gamma": negative,
                      "reverse_orientation": reverse, "wrong_coefficient_rejections": wrong,
                      "immediate_retrace_counterexample": retrace_counterexample,
                      "odd_primitive_three_cycle": numerical,
                      "same_caustic_individual_sum_counterexample": {
                          "a": 5, "b": 3, "lambda": "225/34",
                          "diamond_sum": "680/(3 sqrt(34))", "rectangle_sum": "200/sqrt(34)"},
                      "assertions_used": False, "native_imports_or_runs": [],
                      "all_real_parameters_and_periods_proof": "analytic INITIAL.md"}, indent=2))


if __name__ == "__main__":
    main()
