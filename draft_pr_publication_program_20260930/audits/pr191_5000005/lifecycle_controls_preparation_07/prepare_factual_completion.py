"""PROPOSED merged-scope and combined-current-map factual acceptance."""
import json,sys
from lifecycle_common import production_entrypoint,factual_prepare,factual_accept
if __name__=='__main__':
 if sys.argv[1]=='prepare':out=production_entrypoint(factual_prepare,sys.argv[2])
 elif sys.argv[1]=='accept':out=production_entrypoint(factual_accept)
 else:raise RuntimeError('Unknown action')
 print(json.dumps(out))
