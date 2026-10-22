"""Root-replayable whole-main minimal v7 negative controls; no external I/O."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ns={'__file__':str(HERE/'offline_whole_helper.py'),'__name__':'offline_review07_library'}
exec(compile((HERE/'offline_whole_helper.py').read_bytes(),ns['__file__'],'exec'),ns)
selected=[c for c in ns['fresh_cases']() if c['name'] in {
 'v7_preserve_hidden_lead_links_query_short_resolver',
 'v7_preserve_hidden_lead_files.links_file_suffix_encoded_concept',
 'v7_bibliography_negative_OWR 10/2025; 110.4171/OWR/2025/10',
 'v7_actual197_native_account_and_actual181_ledger',
 'v7_bibliography_negative_OWR 10/2025; https://doi.org/10.4171/OWR/2025/10; separately 10/abc',
}]
results=[ns['case_run'](c) for c in selected]
output={'mode':sys.flags.optimize,'count':len(results),'results':results,'denied_actual_services':ns['DENIED']}
p=HERE/('MINIMAL_MODE_'+str(sys.flags.optimize)+'.json');p.write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
