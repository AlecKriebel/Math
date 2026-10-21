"""PROPOSED explicit reviewed allowlist; no broad directory publication."""
import json
from lifecycle_common import production_entrypoint,final_scope
if __name__=='__main__':print(json.dumps(production_entrypoint(final_scope)))
