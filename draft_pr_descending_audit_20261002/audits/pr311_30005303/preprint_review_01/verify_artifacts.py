import ast,datetime,hashlib,json,pathlib,stat,sys
from pypdf import PdfReader
R=pathlib.Path(__file__).resolve().parent
P=R/'private/fresh_external_copy';O=R/'private/fresh_external_results'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes()
 return {'path':str(p.resolve()),'sha256':hashlib.sha256(b).hexdigest(),'size_bytes':len(b),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')}
original=json.loads((R/'PACKAGE_INPUT_PROVENANCE.json').read_text())['inputs']
for expected in original:
 if pin(pathlib.Path(expected['path']))!=expected:raise ValueError('Original input changed: '+expected['path'])
boundary=json.loads((O/'boundary.stdout').read_bytes())
if boundary!=json.loads((P/'expected/boundary.json').read_bytes()):raise ValueError('Independent boundary comparison failed')
generated=(O/'priority_laws.json').read_bytes();expected=(P/'expected/priority_laws.json').read_bytes()
if generated!=expected:raise ValueError('Independent priority byte comparison failed')
streams={p.name:pin(p) for p in sorted(O.iterdir()) if p.is_file()}
for label in ['boundary','priority_laws']:
 if (O/(label+'.stderr')).read_bytes()!=b'':raise ValueError('nonempty stderr')
 j=json.loads((O/(label+'_execution.json')).read_text())
 if j['exit_code']!=0:raise ValueError('Runner did not exit 0')
 if not all(str(P) in str(j['argv'][1]) for _ in [0]):raise ValueError('Unexpected execution location')
 if j['source_sha256']!=hashlib.sha256(pathlib.Path(j['argv'][1]).read_bytes()).hexdigest():raise ValueError('Run source changed')
for name in ['REPRODUCE.py','verify_boundary.py','verify_priority_examples.py']:
 tree=ast.parse((P/name).read_text());imports=set()
 for node in ast.walk(tree):
  if isinstance(node,ast.Import):imports.update(a.name.split('.')[0] for a in node.names)
  if isinstance(node,ast.ImportFrom):imports.add(node.module.split('.')[0])
 if not imports.issubset(sys.stdlib_module_names):raise ValueError('Nonstandard import '+str(imports))
reader=PdfReader(P/'output/pdf/mtp2_edge_closure.pdf')
uris=[]
for page in reader.pages:
 for annot in page.get('/Annots',[]):
  value=annot.get_object()
  if '/A' in value and '/URI' in value['/A']:uris.append(str(value['/A']['/URI']))
assert len(reader.pages)==5
sourcepins=[pin(p) for p in sorted((R/'private/source').glob('*.pdf'))]
out={'utc':utc(),'status':'PASS_INDEPENDENT_ARTIFACT_COMPARISON_AND_INPUT_INVARIANCE','original_inputs':original,
 'original_input_modes_all_0444':True,'independent_boundary_json_equal':True,'independent_priority_bytes_equal':True,
 'fresh_priority_output':pin(O/'priority_laws.json'),'all_runtime_imports_standard_library':True,'runtime':sys.version,'fresh_runner_stream_pins':streams,
 'pdf_pages':len(reader.pages),'pdf_uris':uris,'primary_source_pdf_pins_before_final_seal':sourcepins,
 'limitations':['Current executable fingerprints cannot establish historical native executable fingerprints.','Historical candidate_code_read=False metadata is an authorship assertion and not reconstructed from unreleased audit history.','No external outreach or publication; no original-package writes.']}
(R/'ARTIFACT_COMPARISON_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
with (R/'RESEARCH_LOG.md').open('a') as f:
 f.write('\n## '+out['utc']+' — Full read, independent reproduction, and adversarial controls (completion estimate: 90%)\n\n')
 f.write('Named release root receipt was inspected; only its twelve named package inputs were read. Original SHA/size/0444 pins independently matched and remain unchanged. Complete manuscript and all code read, all five PDF pages personally visually read, all documentation/receipt/license/manifest read. Expected JSON fully decoded and numerically cross-checked. The fresh different-location standard-library reproduction passes and independent comparisons confirm exact outputs. Mathematical adjudication finds no proof defect in density aggregation/original-edge lifting, residual-flow normalization/compactness, literal source reduction, or the supplementary facial-support argument. Independent checks cover 210 fractional-capacity networks (3810 cuts), 1420 sampled facial energies (1336 lattice supports), all expected laws/global CI equations, and five additional density cases. Four damaged-code mutants and three runner negative cases were rejected.\n\n')
 f.write('Actionable findings: the native build receipt labels one identical hash as program_sha256 across four different executables; the exact historical referent is unverified and needs correction from authentic old evidence. The priority code reports ordered minor evaluations as unique; C6 has 6384 evaluations but 1176 distinct formal polynomials up to sign (C4: 16 versus 8). A stale direct-script usage filename is a minor usability correction. Primary source scopes and bibliographic metadata checked; bounded searches do not establish novelty. The initial mutant-driver indentation failure and missing-rg-path failure are preserved, and successful retries are separately recorded. Exact remaining work: final written report, sealed provenance, and independent seal verification. No immutable publication clearance is claimed.\n')
print(json.dumps({'utc':out['utc'],'status':out['status'],'original_input_count':len(original),'pdf_pages':out['pdf_pages'],'pdf_uris':uris,'primary_source_pdf_pins_before_final_seal':sourcepins},indent=2))

