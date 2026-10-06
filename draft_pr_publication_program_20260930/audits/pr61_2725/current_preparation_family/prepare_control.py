"""MIT licensed. Own source-preparation consistency only, not a math checker."""
import ast,json,pathlib
from binding_checks import verify_bindings
root=pathlib.Path(__file__).resolve().parent
result=verify_bindings(root)
for p in root.glob("*.py"): ast.parse(p.read_bytes(),filename=str(p))
result["status"]="PASS_ATTRIBUTED_KNOWN_RESULT_SOURCE_CONSISTENCY_ONLY"
print(json.dumps(result,sort_keys=True))
