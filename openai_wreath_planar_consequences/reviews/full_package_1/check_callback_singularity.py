"""Domain propagation controls supplementary to the written callback audit.

The exponential of a rational transform can have an essential singularity;
it is not asserted to be globally meromorphic. Away from -2i/5 the callbacks
are holomorphic compositions. A ball containing that point makes their
reciprocal kernel nonfinite. The checks below verify nonfinite propagation
through the elementary transformed terms, including exact zero factors.
"""
import datetime
import hashlib
import json
from pathlib import Path
from flint import arb, acb, ctx
ctx.prec = 192
ii, pi = acb(0, 1), arb.pi()
h, b = arb(2)/5, arb(3).sqrt()/2
tests = []
inputs = [acb(0, -h), acb(arb(0, ".01"), arb(-h, ".01")),
          acb(arb(0, "1"), arb(0, ".5"))]
for t in inputs:
    den = t + ii*h
    assert den.contains(0)
    lam = ii/(b*den)
    z = -(arb(4)/3)/den-ii*h
    values = [lam, z, acb(0)*lam, acb(1)+lam]
    for m in (0, 1, 100):
        base = lam*(ii*pi*z*m).exp()
        values.extend([base, base*(ii*pi*z), base*(ii*pi*z)**2,
                       (acb(0)+acb(1)*base), acb(0)*base])
        for nu in (0, 1, 2):
            values.extend([base*(ii*pi*z)**nu, base*(ii*pi*z)**(28+nu)])
    assert all(not value.is_finite() for value in values)
    tests.append({"argument_ball": str(t), "nonfinite_controls": len(values),
                  "all_nonfinite": True})
record = {
    "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "status": "PASS_NONFINITE_PROPAGATION_CONTROLS",
    "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "tests": tests,
    "written_domain_argument": "Every transformed adaptive callback evaluates 1/(t+2i/5) and multiplies its lambda factor. A finite evaluation therefore excludes the sole singularity from the argument ball; on that ball all remaining operations are entire or rational with nonvanishing denominator. The direct density expressions are entire. No branch-cut operation occurs within a callback. Exponentiating the rational transform may create an essential singularity at the excluded point, which does not change this domain argument.",
    "scope": "Elementary nonfinite propagation controls, supplementary to direct inspection of all callback formulas and the official API analytic-domain contract; not a standalone audit of an arbitrary integrand."
}
Path(__file__).with_suffix(".receipt.json").write_text(json.dumps(record, indent=2)+"\n")
print(json.dumps(record, indent=2))
