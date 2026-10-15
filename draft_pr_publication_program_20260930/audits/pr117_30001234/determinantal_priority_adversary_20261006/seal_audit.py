from pathlib import Path
import datetime,hashlib,json,os
ROOT=Path(__file__).resolve().parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(name,obj):(ROOT/name).write_text(json.dumps(obj,indent=2)+'\n')
ind=json.loads((ROOT/'INDEPENDENCE_CHECKPOINT_MANIFEST.json').read_text())
for member in ind['members']:
    if pin(ROOT/member['path'])!={'bytes':member['bytes'],'sha256':member['sha256']}:raise ValueError('Independent checkpoint changed')
source=[]
shared=ROOT.parent/'primary_source_scope_adversary_20261006/private_sources'
spec=[
('Takagi2013',ROOT/'private_sources/takagi2013_published.pdf','https://msp.org/ant/2013/7-4/ant-v7-n4-p06-s.pdf','actual publisher body','Section4 printed935-940',[22,24,25],{'journal':'Algebra & Number Theory7(4)2013,917-942','doi':'10.2140/ant.2013.7.917','received':'2011-07-01','revised':'2012-04-23','accepted':'2012-05-27'}),
('ShibutaTakagi2009',shared/'shibuta_takagi_0810.1278v3.pdf','https://arxiv.org/pdf/0810.1278v3','actual primary preprint; publisher metadata only','Prop2.1 complete statement/proof and Question2.2 pp6-8; relevant setup pp1-3',[6,8],{'arxiv_version':'2009-04-09','publisher_online':'2009-05-05','issue':'September2009','doi':'10.1007/s00229-009-0270-7'}),
('OWR2009',shared/'owr21_2009.pdf','https://ems.press/content/serial-article-files/46224','actual official report','Question8 printed1139',[39],{'doi':'10.4171/owr/2009/21','year':2009}),
('Docampo',ROOT/'private_sources/docampo_1011.1930v2.pdf','https://arxiv.org/pdf/1011.1930v2','actual primary preprint; journal body not retrieved','setup pp1,4; complete Theorem5.6 proof pp21-22; references',[1,4,21,22],{'arxiv_v2':'2011-02-20','retrieved_PDF_title_date':'June2,2018','journal':'Trans.Amer.Math.Soc.365(2013),2241-2269','journal_doi':'10.1090/S0002-9947-2012-05564-4','Johnson2003_thesis_body':'not retrieved/read'}),
('Mustata',ROOT/'private_sources/mustata_1107.2676v1.pdf','https://arxiv.org/pdf/1107.2676v1','actual primary preprint; chapter metadata only','local valuation definition p5; Theorem1.1 text p6; global/local distinction and Example1.5 p8',[5,8],{'arxiv_v1':'2011-07-13','published_chapter':'2012-08-15','chapter_doi':'10.4171/114-1/16'}),
('MillerSinghVarbaro',ROOT/'private_sources/miller_singh_varbaro_1210.6729v2.pdf','https://arxiv.org/pdf/1210.6729v2','actual primary preprint; publisher metadata only','Definition1.1 p1; Theorem1.2 p2; complete proof pp4-5 and references',[1,2],{'arxiv_v2':'2013-12-19','issue_date':'December2014','publisher_online':'2015-01-06','doi':'10.1007/s00574-014-0074-6'})]
for key,p,url,kind,read,pages,history in spec:
    source.append({'key':key,'url':url,'access':kind,'private_full_body':pin(p),'text_read_boundary':read,'visually_read_physical_pages_one_based':pages,'historical_metadata':history,'full_article_read_claimed':False})
write('SOURCE_MANIFEST.json',{'UTC':now,'source_count':len(source),'private_bodies_excluded_from_public_package':True,'sources':source})
orig=ROOT.parent/'original_head_authentication_20261006'
inputs=[]
for name in ['original_attempt/CANDIDATE.md','SOURCE_STATEMENT.json','PRIOR_REPORT.json']:
    inputs.append({'path':'../original_head_authentication_20261006/'+name,**pin(orig/name)})
gate=json.loads((ROOT.parent/'MATHEMATICAL_SOURCE_GATE_20261006.json').read_text())
if gate['status']!='PASS' or gate['immutable_head']!='8163ee0dc7a0f944570925984cef2dc0fb291ad8':raise ValueError('Math gate mismatch')
if inputs[0]['sha256']!='1409e8ad35d34f3cc4a9bb14f7e42318c1dd1e0446ecba525c655fad8c978cdf':raise ValueError('Original candidate changed')
write('INPUT_AND_READ_CERTIFICATE.json',{'UTC':now,'actual_seal_pid':os.getpid(),'original_inputs':inputs,'mathematical_gate':pin(ROOT.parent/'MATHEMATICAL_SOURCE_GATE_20261006.json'),'original_prior_full_payload':{},'early_independence_preserved':True,'independent_checkpoint_manifest':pin(ROOT/'INDEPENDENCE_CHECKPOINT_MANIFEST.json'),'new_Takagi_pointer_received_from':'root after independent classical-route reasoning; no other new priority-family report read','Takagi_read_mode':'full Section4 extracted text, operative full-page actual pixels at200dpi','earlier_operative_render_dpi':175,'private_body_or_pixel_redistribution_authorized':False})
for name,expected in [('CHECK_PROCESS_RECEIPT.json',73),('TAKAGI_SCOPE_PROCESS_RECEIPT.json',33)]:
    r=json.loads((ROOT/name).read_text())
    if r['result']!='PASS' or len(r['runs'])!=4:raise ValueError('Run receipt incomplete')
    for run in r['runs']:
        if 'false_control' in run['label']:
            if run['exit_code']==0:raise ValueError('False guard accepted')
        elif run['exit_code']!=0 or run['stderr_bytes']!=0:raise ValueError('Positive run failed')
write('RESULT.json',{'UTC':now,'schema':'pr117-determinantal-priority-family/v1','immutable_head':'8163ee0dc7a0f944570925984cef2dc0fb291ad8','problem_id':30001234,'mathematics_valid':True,'priority_verdict':'EXPLICIT_PRIOR_COUNTEREXAMPLE_ALREADY_SOLVED','novel_resolution_publication_clearance':False,'exact_prior_example':'Takagi2013 Example4.4 printed940, Remark4.3 printed939, matrix(4)printed937','doi':'10.2140/ant.2013.7.917','original_target_not_genuinely_open_by_2013':True,'earliest_historical_negative_answer_date_proved_by_this_family':None,'prior_example_semantically_exact_despite_label_not_OWR_Question8':True,'same_ideal_third_generator_negated':True,'published_coordinate_permutation':[0,3,1,4,5,2],'complete_optimal_face_parameterization_is_valid_expository_addition':True,'substantive_new_theorem_established':False,'preliminary_classical_route_was_review_deduction':True,'unread_Johnson2003_thesis_required_for_final_judgment':False,'recommended_disposition':'already_solved exact imported target; retain attributed audit/reproduction, no novel-resolution preprint','remaining_family_scientific_gap':None,'family_completion_percent':100,'service_action_authority':False,'goal_complete':False,'original_substantive_attempts':'1/5','new_central_proof_search_turns':0,'actual_operator_processes':{'source_retrieval':67140,'chart_and_threshold_checks':70549,'Takagi_published_retrieval_and_renders':71837,'Takagi_coordinate_checks':72982},'positive_checks_normal_and_optimized':{'independent_bridge':73,'Takagi_scope':33},'all_false_guards_rejected':True,'report':pin(ROOT/'REPORT.md')})
members=[]
excluded={'OUTPUT_MANIFEST.json','SHA256SUMS'}
for p in sorted(ROOT.iterdir()):
    if p.is_file() and p.name not in excluded:
        if p.is_symlink():raise ValueError('Unexpected symlink')
        members.append({'path':p.name,**pin(p)})
write('OUTPUT_MANIFEST.json',{'UTC':now,'schema':'public-safe-audit-manifest/v1','private_sources_and_renders_excluded':True,'self_and_checksum_list_excluded_to_avoid_cycles':True,'member_count':len(members),'members':members})
for m in members:
    if pin(ROOT/m['path'])!={'bytes':m['bytes'],'sha256':m['sha256']}:raise ValueError('Seal readback mismatch')
lines=[m['sha256']+'  '+m['path'] for m in members]
lines.append(pin(ROOT/'OUTPUT_MANIFEST.json')['sha256']+'  OUTPUT_MANIFEST.json')
(ROOT/'SHA256SUMS').write_text('\n'.join(lines)+'\n')
print(json.dumps({'actual_seal_pid':os.getpid(),'UTC':now,'public_member_count':len(members),'report':pin(ROOT/'REPORT.md'),'result':pin(ROOT/'RESULT.json'),'manifest':pin(ROOT/'OUTPUT_MANIFEST.json'),'source_manifest':pin(ROOT/'SOURCE_MANIFEST.json')},indent=2))
