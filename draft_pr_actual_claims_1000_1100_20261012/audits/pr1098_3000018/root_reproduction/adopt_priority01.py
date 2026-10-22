from pathlib import Path
import hashlib,json,subprocess,datetime
A=Path(__file__).resolve().parents[1];R=A/'reviews/priority_01'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();require(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
seal=load(R/'FINAL_SEAL.json')
for key in ['manifest','input_pins','input_recheck_resumed','report','verdict','original_derivations','resumption_addendum','reproduction_resumed','source_ledger']:
    r=seal[key];check(R/r['path'],r)
outputs=load(R/'OUTPUT_PINS.json')['records'];inputs=load(R/'INPUT_PINS.json')['files']
for r in outputs:check(R/r['path'],r)
for r in inputs:check(A/r['path'],r)
sources=load(R/'SOURCE_READ_LEDGER.json')['retained_primary_bodies']
for r in sources:
    check(R/r['path'],r)
    require(sha((R/r['text_path']).read_bytes())==r['text_sha256'],'source text changed')
commands=[]
for name,expected in [('check_prior_interfaces.py','EXACT_CONTROLS_NORMAL.json'),('check_classical_union_resume.py','CLASSICAL_UNION_CONTROLS_NORMAL.json')]:
    results=[]
    for optimized in [False,True]:
        argv=['python3','-B']+(['-O'] if optimized else [])+[str(R/name)]
        p=subprocess.run(argv,capture_output=True);require(p.returncode==0,p.stderr.decode(errors='replace'))
        result=json.loads(p.stdout);require(result==load(R/expected),'complete reviewed priority JSON differs');results.append(result)
        q=subprocess.run(argv+['--self-test-invalid'],capture_output=True);require(q.returncode!=0,'invalid guard accepted')
        commands.append({'script':name,'optimized':optimized,'exit_code':p.returncode,'complete_JSON_equals_review':True,'stdout_sha256':sha(p.stdout),'invalid_exit':q.returncode,'invalid_stderr_sha256':sha(q.stderr)})
    require(results[0]==results[1],'full normal/O JSON differs')
verdict=load(R/'VERDICT.json')
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
record={'utc':utc,'status':'ADOPT_QUALIFIED_EXTENSIVE_PRIORITY_PENDING_GLOBALLY_ATTRIBUTED_COMPLETE_PREPRINT','pr':1098,'head':'f37a3ff66595fcf75bb18bf859be8594c3662242','full_REPORT_PRIOR_COMPARISON_DERIVATIONS_ADDENDUM_VERDICT_SOURCE_LEDGER_read':True,'outputs_rehashed':len(outputs),'frozen_inputs_rehashed':len(inputs),'retained_PDF_and_text_pairs_rehashed':len(sources),'root_direct_primary_reads':['HLW1511.00422v2 full Lemma4.1 proof PDF15 and adjacent16','StockmeyerMeyer1973 full Theorem6.1 proof actualPDF7–8; exact clause versus variable-invalid union qualification independently assessed'],'root_actual_control_replays':commands,'mandatory_global_preparation_conditions':verdict['mandatory_preparation_conditions'],'required_global_preparation_changes':verdict['required_global_preparation_changes'],'full_result_priority':'UNKNOWN','conservative_simple_and_oriented_realization_priority':'UNKNOWN','method_priority':'EXACT_BANK_AND_CRT_INGREDIENTS_PRIOR; remaining implementation UNKNOWN','worldwide_preexisting_openness':'UNKNOWN','unread_material':'Full MayrWeihmann, complete HujsaDevillers and unlocated older work remain UNKNOWN; no full theorem corollary established from read interfaces.','mathematical_actionable_findings':0,'publication_ready':False,'published':False,'services_held_after_pr':1032,'priority_output_pins_sha256':sha((R/'OUTPUT_PINS.json').read_bytes()),'priority_seal_sha256':sha((R/'FINAL_SEAL.json').read_bytes()),'completion_percent_of_priority_adoption':100}
(A/'ROOT_PRIORITY_ADOPTION.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'PASS','utc':utc,'outputs':len(outputs),'inputs':len(inputs),'source_pairs':len(sources),'mandatory_P2_conditions':len(verdict['mandatory_preparation_conditions']),'ready':False}))
