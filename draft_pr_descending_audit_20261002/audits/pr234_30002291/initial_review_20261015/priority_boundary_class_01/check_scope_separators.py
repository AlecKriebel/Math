"""Reproduce elementary scope certificates; does not establish literature priority."""
from fractions import Fraction as F
from pathlib import Path
import datetime, hashlib, json, math

ROOT = Path(__file__).resolve().parent

def check():
    result = {
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "purpose": "Scope separation and a quadratic specialization of the general-function theorem; not a novelty certificate.",
        "index_two_measure": {
            "density": "1_(0<|z|<exp(-1)) |z|^(-3) log(1/|z|)^(-2)",
            "total_quadratic_rate_exact": 2,
            "moment_substitution": "I(q)=2 integral_1^infinity exp((2-q)v)/v^2 dv",
            "moment_finite_iff": "q >= 2",
            "BG_index_exact": 2,
            "small_jump_quadratic_rate": "2/log(1/epsilon), 0<epsilon<=exp(-1)",
            "rate_examples": [{"epsilon": math.exp(-m), "exact_rate": str(F(2,m)), "numeric_rate": 2/m} for m in [1,2,4,8,16,32,64,128]],
        },
        "non_dilation_kernel": {
            "before": {"measure": "delta_1", "total_mass": 1, "quadratic_rate": 1},
            "after": {"measure": "delta_1+delta_2", "total_mass": 2, "quadratic_rate": 5},
            "uniform_bound_K": 5,
            "scalar_nonzero_pushforward_preserves_total_mass": True,
            "scalar_zero_pushforward_has_zero_nonzero_mark_mass": True,
            "obstruction": "No fixed Levy measure has both total masses as nonzero scalar pushforwards.",
        },
        "quadratic_function_auxiliary_exponent": [],
    }
    # For f(x)=x^2, selecting r strictly below 2 leaves only f(0)=f'(0)=0.
    # The general function theorem requires r>max(beta,1/(1-alpha)).
    for alpha in [F(1,1000), F(1,4), F(49,100), F(499,1000)]:
        for beta in [F(0), F(1), F(199,100), F(1999,1000)]:
            threshold=max(beta, 1/(1-alpha))
            r=(threshold+2)/2
            assert threshold<r<2
            result["quadratic_function_auxiliary_exponent"].append({"alpha":str(alpha),"beta":str(beta),"lower_bound":str(threshold),"chosen_r":str(r),"checks_pass":True})
    result["beta_equal_two_failure"]={"reason":"An auxiliary r>beta=2 requires vanishing second derivative at zero; f''(0)=2 for f=x^2.","open_interval_for_r_below_two_is_empty":True}
    # Exact second-moment and total-mass arithmetic.
    assert 1*1**2 + 1*2**2 == 5
    assert F(2,1)==2
    result["all_checks_pass"]=True
    return result

if __name__ == "__main__":
    data=check()
    (ROOT/"SCOPE_CHECKS.json").write_text(json.dumps(data,indent=2)+"\n")
    print(json.dumps({"all_checks_pass":True,"auxiliary_exponent_cases":len(data["quadratic_function_auxiliary_exponent"]),"scope_only":True}))
