"""PROPOSED fresh-MAIN/original-head two-parent integration; never moves refs."""
import json,sys
from lifecycle_common import production_entrypoint,integration_prepare,integration_accept
if __name__=='__main__':
 if sys.argv[1]=='prepare':out=production_entrypoint(integration_prepare,sys.argv[2])
 elif sys.argv[1]=='accept':out=production_entrypoint(integration_accept)
 else:raise RuntimeError('Unknown action')
 print(json.dumps(out))
