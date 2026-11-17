const root="/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/mink-riesz-k3-stage-sol-20261117";
const metas=new Map();
for(const k of ["topmeta","basemeta","candmeta"]){
for(const line of load("minkSeal_"+k).trim().split("\n")){
 const a=line.split("|");if(a.length!==4)throw Error("metadata delimiter");
 const [p,n,m,t]=a;if(!p.startsWith(root)||!["Regular File","Directory"].includes(t))throw Error("type/path");
 const r=p===root?".":p.slice(root.length+1);
 if(r!=="."&&(r.startsWith("/")||r.split("/").some(x=>["",".",".."].includes(x))))throw Error("canonical");
 const val={path:r,bytes:+n,mode:"0"+m,type:t};const old=metas.get(r);if(old&&(old.mode!==val.mode||old.type!==val.type))throw Error("duplicate mismatch");metas.set(r,val);
}}
const hashes=new Map();
for(const k of ["tophash","basehash","candhash"]){
for(const line of load("minkSeal_"+k).trim().split("\n")){const h=line.slice(0,64),p=line.slice(66);if(!/^[0-9a-f]{64}$/.test(h)||!p.startsWith(root+"/"))throw Error("hash row");const r=p.slice(root.length+1);if(hashes.has(r))throw Error("duplicate hash");hashes.set(r,h);}
}
const files=[...metas.values()].filter(x=>x.type==="Regular File"),dirs=[...metas.values()].filter(x=>x.type==="Directory");
if(files.length!==1616||dirs.length!==771||hashes.size!==files.length||metas.get(".").mode!=="0755")throw Error("finite count");
const parents=new Set();
for(const x of metas.values())if(x.path!=="."){const pos=x.path.lastIndexOf("/");parents.add(pos<0?".":x.path.slice(0,pos));}
if([...parents].some(r=>!metas.has(r)||metas.get(r).type!=="Directory"))throw Error("missingparent");
const hidden=r=>r!=="."&&r.split("/").some(x=>x.startsWith("."));
const fileRows=files.map(x=>{if(!hashes.has(x.path)||x.mode!=="0644")throw Error("filepin");return {path:x.path,bytes:x.bytes,SHA256:hashes.get(x.path),mode:x.mode,hidden:hidden(x.path),empty:x.bytes===0};}).sort((a,b)=>a.path<b.path?-1:1);
const dirRows=dirs.map(x=>({path:x.path,mode:x.mode,empty:!parents.has(x.path),hidden:hidden(x.path)})).sort((a,b)=>a.path<b.path?-1:1);
const topPins=Object.fromEntries(fileRows.filter(x=>!x.path.includes("/")).map(({path,bytes,SHA256,mode})=>[path,{bytes,SHA256,mode}]));
store("minkStageTopPins",topPins);
const man={schema:"finite-mink-riesz-k3-private-stage-manifest-v1",UTC:"2026-11-17T13:52:09Z",root,root_mode:"0755",regular_files:1618,child_directories:770,payload_files:fileRows,directories:dirRows,hidden_files:fileRows.filter(x=>x.hidden).length,hidden_directories:dirRows.filter(x=>x.hidden).length,empty_payload_files:fileRows.filter(x=>x.empty).map(x=>x.path),empty_directories:dirRows.filter(x=>x.empty).map(x=>x.path),symlinks:0,special_objects:0,exact_already_created_terminal_recursive_hash_exclusions:[root+"/OWNED_MANIFEST.json",root+"/FINAL.json"],terminal_modes:{"OWNED_MANIFEST.json":"0644","FINAL.json":"0644"},other_exclusions:[],all_hidden_ignored_empty_bytes_modes_and_topology_included:true,no_future_subtree_or_basename_exclusion:true,terminal_pair_external_pins_required:true};
store("minkStageManifest",man);
text({payload_files:fileRows.length,regular_files_after_terminals:1618,childdirs:770,directory_rows_including_root:771,hidden_files:man.hidden_files,hidden_directories:man.hidden_directories,empty_files:man.empty_payload_files,empty_dirs:man.empty_directories.length,all_file_modes:"0644",root_mode:"0755",top_artifacts:topPins});
text(await tools.apply_patch("*** Begin Patch\n*** Add File: "+root+"/OWNED_MANIFEST.json\n"+JSON.stringify(man,null,2).split("\n").map(x=>"+"+x).join("\n")+"\n*** End Patch"));
text(await tools.exec_command({cmd:"shasum -a 256 "+root+"/OWNED_MANIFEST.json",max_output_tokens:1000}));
text(await tools.exec_command({cmd:"stat -f '%z %Lp' "+root+"/OWNED_MANIFEST.json",max_output_tokens:1000}));
