"""PROPOSED factual-only native generation, gated by actual publication/tracker."""
import json
from lifecycle_common import production_entrypoint,prepare_native
if __name__=='__main__':print(json.dumps(production_entrypoint(prepare_native,False)))
