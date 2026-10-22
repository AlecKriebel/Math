from pathlib import Path
import ast,hashlib,json,datetime
H=Path(__file__).resolve().parent;A=H.parent;R=A.parents[1]
prior=(A/'exact_instance_adversary/offline_exact_instance.py').read_text()
body=prior[:prior.index('STATS=[')]
body=body.replace("HELPER = AUDIT / 'reconcile_exact_instance.py'", "HELPER = AUDIT / 'reconcile_exact_instance_v2.py'")
body=body.replace("EXPECTED_HELPER='3d2489fbae11fa92b92965b80c28e4d906df91db8be4c4aafa3e8bda11f5f9fa'", "EXPECTED_HELPER='d0fe59f4967facfd64db7332aad0f9663b4771f7a116c463c89bf4c30b88eacb'")
body=body.replace('!=19284','!=19390').replace('ROOT_EXACT_INSTANCE_ACCEPTANCE.json','ROOT_EXACT_INSTANCE_V2_ACCEPTANCE.json')
body=body.replace("'env_token':os.environ.get('ZENODO_TOKEN')", "'environ':os.environ")
body=body.replace("os.environ['ZENODO_TOKEN']='OFFLINE_FIXTURE_NOT_A_TOKEN'", "os.environ={'ZENODO_TOKEN':'OFFLINE_FIXTURE_NOT_A_TOKEN'}")
body=body.replace("if originals['env_token'] is None:os.environ.pop('ZENODO_TOKEN',None)\n            else:os.environ['ZENODO_TOKEN']=originals['env_token']", "os.environ=originals['environ']")
body=body.replace("if state['reads']==2:cfg.get('edit_immediate_rows',lambda r:None)(rows)", "if state['reads']==2:cfg.get('edit_immediate_rows',lambda r:None)(rows)\n                cfg.get('edit_rows_at_read',lambda r,n:None)(rows,state['reads'])")
body=body.replace("record=copy.deepcopy(BASE_PROVIDER)", "cfg.get('edit_baseline_rows',lambda r:None)(rows)\n        record=copy.deepcopy(BASE_PROVIDER)")
body=body.replace("if state['pr_reads']==2:cfg.get('edit_final_pr',lambda r:None)(obj)", "if state['pr_reads']==2:cfg.get('edit_final_pr',lambda r:None)(obj)\n                    cfg.get('edit_pr_at_read',lambda r,n:None)(obj,state['pr_reads'])")
body=body.replace("n=state['account_gets'];size=cfg.get('page_size',25);items=copy.deepcopy(account[(n-1)*size:n*size])", "n=state['account_gets'];size=cfg.get('page_size',25);items=copy.deepcopy(account[(n-1)*size:n*size])")
# Add explicit snapshot/acceptance fault hooks without changing target code.
body=body.replace("cfg.get('edit_plan_file',lambda p:None)(audit/PLAN.name)", "cfg.get('edit_plan_file',lambda p:None)(audit/PLAN.name)\n        cfg.get('edit_acceptance_file',lambda p:None)(acceptance_path)\n        if cfg.get('missing_acceptance'):acceptance_path.unlink()\n        if cfg.get('helper_changed'):path_write(fixture_helper,SOURCES[str(HELPER)]+b'\\n# unreviewed fixture')")
body=body.replace("'receipt_saved':receipt is not None,", "'receipt_saved':receipt is not None,'receipt_row':receipt.get('row_number') if receipt else None,'receipt_new_row':receipt.get('new_row') if receipt else None,")
body=body.replace("if error and ('[Errno 28]'", "if unexpected:raise RuntimeError('Unexpected service path in fixture: '+repr(unexpected))\n        if error and ('[Errno 28]'")
(H/'offline_whole_v2.py').write_text(body)
# New independent byte copies; never hardlink original inputs.
paths=[A/'reconcile_exact_instance_v2.py',A/'LEDGER_RECONCILIATION_PLAN.json',*[R/p for p in ['publication_check.py','sweep_io.py','checkpoint.py','audits/pr0399_30001179/ops_binding.py','audits/pr0399_30001179/prepublication_check.py','../zenodo_deposit_tool/zenodo.py']],R/'raw/pr1156/zenodo_23350364.json',R/'rest_inventory.json',A/'root/private/actual_instance08_root_copy/private/source_10_ledger_live.json',A/'root/private/actual_instance08_root_copy/private/source_14_account.json',A/'ledger_adversary08/private/fresh_capture/account.json']
plan=json.loads((A/'LEDGER_RECONCILIATION_PLAN.json').read_bytes())
paths += [R/'raw/pr1156'/('payload_'+f['sha256']+'.bin') for f in plan['existing_publication']['files']]
entries=[]
for n,p in enumerate(paths):
    b=p.read_bytes();q=H/'private'/('source_%02d_'%n+p.name);q.write_bytes(b)
    entries.append({'original':str(p.resolve()),'snapshot':str(q.relative_to(H)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
(H/'SOURCE_PINS.json').write_text(json.dumps({'schema':1,'new_independent_copies':True,'original_hardlinks':False,'files':entries},indent=2)+'\n')
# Review import-time closure: full checkpoint source parsed; huge NAMES section
# checked as literal-only list extension, preserving exact original bytes.
source=(R/'checkpoint.py').read_text();tree=ast.parse(source);names_nodes=[];other=[]
for n in tree.body:
    is_names=(isinstance(n,(ast.Assign,ast.AugAssign)) and isinstance(n.targets[0] if isinstance(n,ast.Assign) else n.target,ast.Name) and (n.targets[0] if isinstance(n,ast.Assign) else n.target).id=='NAMES') or (isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and isinstance(n.value.func.value,ast.Name) and n.value.func.value.id=='NAMES')
    if is_names:
        value=n.value if not isinstance(n,ast.Expr) else n.value.args[0]
        if isinstance(value,ast.ListComp):
            other.append(ast.get_source_segment(source,n));continue
        vals=ast.literal_eval(value)
        if not isinstance(vals,list) or not all(isinstance(x,str) for x in vals):raise RuntimeError('Nonliteral NAMES')
        names_nodes.append({'line':n.lineno,'strings':len(vals)})
    else:other.append(ast.get_source_segment(source,n))
(H/'CHECKPOINT_NONNAMES_READ.txt').write_text('\n\n'.join(other)+'\n')
(H/'IMPORT_INSPECTION.json').write_text(json.dumps({'checkpoint_full_sha256':hashlib.sha256(source.encode()).hexdigest(),'checkpoint_bytes':len(source.encode()),'literal_only_names_nodes':names_nodes,'remaining_complete_source':'CHECKPOINT_NONNAMES_READ.txt','modules':['sweep_io','checkpoint','zenodo','ops_binding','publication_check','pr1156_account_reader_final'],'project_imports_satisfied_by_verified_source_byte_modules':True,'checkpoint_main_not_executed':True},indent=2)+'\n')
(H/'.gitignore').write_text('private/\n__pycache__/\nPROGRESS_MODE_*.jsonl\n')
(H/'RESEARCH_LOG.md').write_text('# Independent exact-instance v2 review\n\n'+datetime.datetime.now(datetime.timezone.utc).isoformat()+' — 35%: whole capsule, unchanged plan, reachable dependency functions and literal checkpoint data reviewed; fixed-data evidence read. New private byte copies prepared. No external operations, token access, original input writes, or operational acceptance created.\n')
print(json.dumps({'new_snapshot_files':len(entries),'copied_bytes':sum(e['bytes'] for e in entries),'helper':entries[0],'checkpoint_literal_nodes':len(names_nodes)},indent=2))
