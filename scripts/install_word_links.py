from pathlib import Path
import re
import shutil
import sys

ROOT=Path(__file__).resolve().parents[1]
TEMPLATE=ROOT/'site'/'template.html'
BUILDER=ROOT/'scripts'/'build.py'
LEX=ROOT/'obsidian-vault'/'Reference'/'Comparative Lexicon.md'
MARK='HOMER_SANSKRIT_WORD_LINKS_V1'

CSS=r'''/* HOMER_SANSKRIT_WORD_LINKS_V1 */
.sanskrit-link {font:inherit;color:#245d69;background:transparent;padding:0 1px;border:0;border-bottom:2px dotted #9c732e;border-radius:0;cursor:pointer;text-decoration:none;line-height:inherit}
.sanskrit-link:hover,.sanskrit-link:focus-visible {color:#143944;background:#f9efcc;border-bottom-style:solid;outline-offset:3px}
.sanskrit-link:focus-visible{outline:2px solid #8a5616}
@media(prefers-color-scheme:dark){.sanskrit-link{color:#b7e6ed;border-bottom-color:#f1c778}.sanskrit-link:hover,.sanskrit-link:focus-visible{color:#fff;background:#3c4e52}}
'''
JS=r'''/* HOMER_SANSKRIT_WORD_LINKS_V1 */
function decorateSanskrit(){
 const root=byId('sanskrit');
 if(sanskritMode!=='deva')return;
 const p=data.passages[passageIndex];
 const candidates=[];
 visibleNotes(p).forEach(note=>{
   const index=data.notes.indexOf(note);
   const forms=[note.sanskrit,...(note.forms||[])];
   forms.forEach(form=>{
     form=String(form).trim();
     if(!form || !/[\u0900-\u097f]/.test(form))return;
     // Explicit inflected forms only; avoid guessing across sandhi boundaries.
     candidates.push({form,index});
   });
 });
 candidates.sort((a,b)=>b.form.length-a.form.length);
 const source=root.textContent;
 const result=document.createDocumentFragment();
 let pos=0;
 while(pos<source.length){
   let selected=null;
   for(const candidate of candidates){
     if(!source.startsWith(candidate.form,pos))continue;
     // Disallow matches inside a longer unlisted Devanagari word.
     const before=pos?source[pos-1]:'';
     const after=source[pos+candidate.form.length]||'';
     if(/[\u0900-\u097f]/.test(before)||/[\u0900-\u097f]/.test(after))continue;
     selected=candidate;break;
   }
   if(selected){
     const button=document.createElement('button');
     button.type='button';button.className='sanskrit-link';
     button.dataset.lexIndex=String(selected.index);
     button.textContent=selected.form;
     button.title='Open the comparative lexicon note';
     button.setAttribute('aria-label',`Open lexicon note for ${selected.form}`);
     result.append(button);pos+=selected.form.length;
   }else{
     let next=pos+1;
     while(next<source.length && !candidates.some(c=>source.startsWith(c.form,next)))next++;
     result.append(document.createTextNode(source.slice(pos,next)));pos=next;
   }
 }
 root.replaceChildren(result);
}
byId('sanskrit').addEventListener('click',event=>{
 const button=event.target.closest('.sanskrit-link');if(!button)return;
 const note=data.notes[Number(button.dataset.lexIndex)];if(!note)return;
 activeLine=null;
 byId('lex-search').value=note.greek;
 renderNotes();
 byId('lex-title').scrollIntoView({behavior:'smooth',block:'start'});
});
'''

def replace_once(s,old,new,label):
    count=s.count(old)
    if count!=1: raise RuntimeError(f'{label}: expected one insertion point, found {count}; no files changed')
    return s.replace(old,new,1)

def main():
    for f in [TEMPLATE,BUILDER,LEX]:
        if not f.exists(): raise RuntimeError(f'Missing {f}. Extract ZIP in F:\\github\\homer-sanskrit')
    template=TEMPLATE.read_text('utf-8')
    builder=BUILDER.read_text('utf-8')
    lex=LEX.read_text('utf-8-sig')
    if MARK in template or MARK in builder:
        print('Word-link feature already installed. No changes made.');return
    template=replace_once(template,'</style>',CSS+'\n</style>','CSS')
    template=replace_once(template,'function chooseLine(n){',JS+'\nfunction chooseLine(n){','JavaScript')
    # Match the actual render() function regardless of its indentation and spacing.
    render_start=template.find('function render(){')
    render_end=template.find('function renderNotes(){',render_start)
    if render_start < 0 or render_end < 0:
        raise RuntimeError('Cannot locate render() and renderNotes() in website template; no files changed')
    render_block=template[render_start:render_end]
    hits=list(re.finditer(r'(?m)^([ \t]*)renderNotes\(\);[ \t]*$',render_block))
    if len(hits)!=1:
        raise RuntimeError(f'Could not identify render() note hook (found {len(hits)}); no files changed')
    hook=hits[0]
    indent=hook.group(1)
    render_block=render_block[:hook.end()]+f'\n{indent}decorateSanskrit();'+render_block[hook.end():]
    template=template[:render_start]+render_block+template[render_end:]
    builder=replace_once(builder,'        explanation = re.sub(r"(?m)^\\*\\*(?:Status|Lines):\\*\\*.*$", "", rest).strip()',
        '        forms_match = re.search(r"(?m)^\\*\\*Forms:\\*\\*\\s*(.+)$", rest)\n'
        '        forms = [s.strip() for s in forms_match.group(1).split(",")] if forms_match else []\n'
        '        explanation = re.sub(r"(?m)^\\*\\*(?:Status|Lines|Forms):\\*\\*.*$", "", rest).strip()\n'
        '        # HOMER_SANSKRIT_WORD_LINKS_V1', 'builder metadata')
    builder=replace_once(builder,'"status":st.group(1).strip(),"lines":lines.group(1).strip(),',
        '"status":st.group(1).strip(),"lines":lines.group(1).strip(),"forms":forms,','builder JSON')
    # Add one known inflection to the existing silver-bow note without changing its prose.
    bow_sections=re.split(r'(?=^## )',lex,flags=re.M)
    updated=False
    for idx,block in enumerate(bow_sections):
        head=block.split('\n',1)[0]
        if 'ἀργυρέοιο' in head and 'βιοῖο' in head:
            if '**Forms:**' not in block:
                m=re.search(r'(?m)^\*\*Lines:\*\*[^\n]*$',block)
                if m:
                    block=block[:m.end()]+'\n**Forms:** रजतधनुषो, रजतधनुषः'+block[m.end():]
                    updated=True
            bow_sections[idx]=block
    if updated:lex=''.join(bow_sections)
    # Back up originals before changing a byte.
    for f in [TEMPLATE,BUILDER,LEX]: shutil.copy2(f, f.with_suffix(f.suffix+'.wordlinks-backup'))
    TEMPLATE.write_text(template,encoding='utf-8')
    BUILDER.write_text(builder,encoding='utf-8')
    if updated:LEX.write_text(lex,encoding='utf-8')
    import subprocess
    proc=subprocess.run([sys.executable,str(BUILDER)],cwd=ROOT,capture_output=True,text=True)
    print(proc.stdout,proc.stderr)
    if proc.returncode:raise RuntimeError('Build failed. Original backups are available. '+proc.stderr)
    html=(ROOT/'site'/'index.html').read_text('utf-8')
    assert 'decorateSanskrit()' in html and 'sanskrit-link' in html
    print('SUCCESS: Clickable Sanskrit lexicon words installed. Open site/index.html.')
    if not updated:print('TIP: Add **Forms:** रजतधनुषो, रजतधनुषः under the silver-bow lexicon entry, if needed.')

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('ERROR:',exc)
        sys.exit(1)
