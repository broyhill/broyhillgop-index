#!/usr/bin/env python3
"""Rebuild GOD FILE v4 (index.html) so search -> click -> open works from any browser.

What it does (re-runnable; original v4 entries are never dropped):
  A. Data Committee Drive card points at the real folder (19Senn2EGWDJ_ro0K0GlsvES77FKXtdy9).
  B. Adds every platform file in broyhill/BroyhillGOP (from `git ls-tree`), ecosystem assigned by
     PATH OWNERSHIP only (E## directory, E##-NAME directory, ecosystem_##_ filename) per
     docs/canonical/BGOP_SEARCH_ENGINE_MASTER_PLAN.md pipeline steps 2 and 12 and
     ECO_NATIVE_INTEGRATION_MATRIX_2026-06-01.md (mentions are not ownership).
  C. Every entry gets a real URL: GitHub blob link when the file exists in the repo, otherwise a
     Google Drive search for the file name. file:// links are gone. COPY still copies the path.

Usage (any workstation; reads local files, writes index.html; no network, no database):
  git -C <BroyhillGOP clone> ls-tree -r -z --name-only HEAD > repo_files.z
  git -C <BroyhillGOP clone> ls-tree -r -l HEAD | awk -F'\t' '{split($1,a," "); print a[4]"\t"$2}' > repo_sizes.tsv
  python3 tools/build_v4_index.py --repo-list repo_files.z --repo-sizes repo_sizes.tsv --repo-sha <sha>
(--repo-sizes may list only some paths; an original whose only evidence is a unique file name is
linked only when its v4 size equals the repo blob size.)
This repo is reference-only for the platform (no DB connections); the script only regenerates
the static index page that Vercel serves from this repo.
"""
import argparse
import datetime as dt
import json
import re
import sys
from collections import Counter, defaultdict

DATA_COMMITTEE = "https://drive.google.com/drive/folders/19Senn2EGWDJ_ro0K0GlsvES77FKXtdy9"

# Master plan step 2 quality filter: archives and non-platform files out.
SKIP_PREFIXES = ("vendor/", "archive/")
SKIP_SEGMENTS = {"node_modules", ".git", "__pycache__"}
SKIP_EXT = {
    "png", "jpg", "jpeg", "gif", "svg", "ico", "webp", "bmp", "tif", "tiff",
    "woff", "woff2", "ttf", "eot", "otf",
    "mp4", "mov", "mp3", "wav", "m4a", "webm",
    "zip", "gz", "tgz", "tar", "7z", "rar",
    "map", "lock", "pyc", "ds_store",
    "css", "scss", "less",
}

ECO_DIR = re.compile(r"^E(\d{2,3})([a-z]?)(?:$|[-_ ])", re.I)
ECO_FILE = re.compile(r"ecosystem[_-]?(\d{2,3})([a-z]?)(?=[_.-])", re.I)


def eco_from_path(path):
    """Path ownership only: first E## directory, else ecosystem_##_ in a segment."""
    segs = path.split("/")
    for seg in segs[:-1]:
        m = ECO_DIR.match(seg)
        if m:
            return "E" + m.group(1) + m.group(2).lower()
    for seg in segs:
        m = ECO_FILE.search(seg)
        if m:
            return "E" + m.group(1) + m.group(2).lower()
    return None


def ext_of(name):
    base = name.rsplit("/", 1)[-1]
    return base.rsplit(".", 1)[-1].lower() if "." in base else ""


def keep_repo_file(path):
    if path.startswith(SKIP_PREFIXES):
        return False
    segs = path.split("/")
    if SKIP_SEGMENTS.intersection(segs):
        return False
    base = segs[-1]
    if base.startswith(".") and base not in (".env.example",):
        return False
    e = ext_of(base)
    if e in SKIP_EXT or base.endswith((".min.js", ".min.css")):
        return False
    return True


def words(path):
    return re.sub(r"[_\-/.]+", " ", path).lower().strip()


def load_array(html, name, opener, closer):
    m = re.search(r"const " + name + r"=(" + re.escape(opener) + r".*?" + re.escape(closer) + r");\n", html, re.S)
    if not m:
        sys.exit(f"cannot find const {name}")
    return m, json.loads(m.group(1))


def normalize_old(f):
    """The 55 entries with the n/s/m/t schema (no cat/path/src) get the standard schema."""
    if "path" in f and "cat" in f and "src" in f:
        if f["path"].endswith("/") or f.get("ext") == "dir":
            f["n"] = f["path"].rstrip("/").rsplit("/", 1)[-1] + "/"
            f["ext"] = "dir"
        f.setdefault("ext", ext_of(f.get("n", "")))
        return f
    p = f.get("path") or f.get("n", "")
    cat = f.get("cat") or eco_from_path(p) or "OTHER"
    src = f.get("src") or (p.split("/", 1)[0] if "/" in p else "Local")
    is_dir = p.endswith("/") or f.get("t") == "dir"
    name = p.rstrip("/").rsplit("/", 1)[-1] + ("/" if is_dir else "")
    return {
        "cat": cat, "n": name, "ext": "dir" if is_dir else (f.get("ext") or f.get("t") or ext_of(p)),
        "s": f.get("s", 0), "path": p, "src": src, "tags": words(p),
    }


def best_repo_match(old_path, candidates, old_size=0, sizes=None):
    """Repo path that is the same file as the old Mac path, or None.

    Evidence accepted: the parent folder name agrees too, or the name occurs exactly once in the
    repo AND the v4 size equals the repo blob size. A bare name collision (deploy.sh, README.md)
    is never a match.
    """
    old = [s.lower() for s in old_path.rstrip("/").split("/")]

    def shared(c):
        cs = [s.lower() for s in c.split("/")]
        k = 0
        while k < min(len(cs), len(old)) and cs[-1 - k] == old[-1 - k]:
            k += 1
        return k

    best = max(candidates, key=lambda c: (shared(c), -len(c)))
    if shared(best) >= 2:
        return best
    if len(candidates) == 1 and old_size and sizes and sizes.get(best) == old_size:
        return best
    return None


NEW_RENDER = r"""/*V4R-START*/
const LIMIT=200;
let GROUPS={};
function escH(s){return String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
const GHB='https://github.com/broyhill/BroyhillGOP/blob/main/',GDS='https://drive.google.com/drive/search?q=';
F.forEach(f=>{
  if(!f.n)f.n=f.path.split('/').pop();
  if(!f.n)f.n=f.path.replace(/\/+$/,'').split('/').pop()+'/';
  const g=f.g===1?f.path:f.g;
  f.u=g?GHB+g.split('/').map(encodeURIComponent).join('/'):GDS+encodeURIComponent(f.n);
  f.lk=g?'gh':'gd';
  f._h=(f.n+' '+f.cat+' '+(CATS[f.cat]||'')+' '+f.src+' '+(f.tags||'')+' '+(f.path||'')).toLowerCase();
});
function rowHtml(f){
  const href=f.u||'#';
  const lk=f.lk==='gh'?'<span class="lk gh" title="Opens the file on GitHub">GH</span>':'<span class="lk gd" title="No GitHub copy found; searches your Google Drive for this file name">DRIVE</span>';
  return `<div class="file-row">
    <span class="icon">${icons[f.ext]||'📁'}</span>
    <span class="fname">${lk}<a href="${escH(href)}" target="_blank" rel="noopener" title="${escH(f.path)}">${escH(f.n)}</a></span>
    <span class="fsize">${fmtSize(f.s)}</span>
    <span class="badge ${escH(f.ext)}">${escH(f.ext)}</span>
    <span class="fsrc" title="${escH(f.src)}">${escH(f.src)}</span>
    <span class="cpbtn" data-p="${escH(f.path)}">COPY</span>
  </div>`;
}
function fillCat(box,cat,all){
  const items=GROUPS[cat]||[];
  const shown=all?items:items.slice(0,LIMIT);
  box.innerHTML=shown.map(rowHtml).join('')+(shown.length<items.length?`<div class="more" data-cat="${escH(cat)}">Show all ${items.length} files</div>`:'');
  box.dataset.filled='1';
}
function ecoNum(c){const m=c.match(/^E(\d{2,3})/);return m?parseInt(m[1],10):null}
function render(){
  const rawQ=document.getElementById('search').value.trim();
  const sf=document.getElementById('srcFilter').value;
  const terms=rawQ?expandQuery(rawQ):[];
  const origTerms=rawQ?rawQ.toLowerCase().split(/\s+/):[];
  let filtered=F.filter(f=>{
    if(terms.length>0&&!origTerms.some(t=>f._h.includes(t))&&!terms.some(t=>f._h.includes(t)))return false;
    if(sf&&!f.src.includes(sf))return false;
    if(activeType&&f.ext!==activeType)return false;
    return true;
  });
  if(terms.length>0){
    filtered.forEach(f=>{
      const hay=(f.n+' '+f.cat).toLowerCase();
      f._score=0;
      const nl=f.n.toLowerCase(),pl=(f.path||'').toLowerCase(),q=rawQ.toLowerCase(),qu=q.replace(/\s+/g,'_');
      if(nl.includes(q)||nl.includes(qu))f._score+=25;else if(pl.includes(q)||pl.includes(qu))f._score+=12;
      origTerms.forEach(t=>{if(nl.includes(t))f._score+=10;else if(pl.includes(t))f._score+=3});
      terms.forEach(t=>{if(hay.includes(t))f._score+=1});
    });
    filtered.sort((a,b)=>b._score-a._score);
  }
  GROUPS={};
  filtered.forEach(f=>{(GROUPS[f.cat]=GROUPS[f.cat]||[]).push(f)});
  const catOrder=Object.keys(GROUPS).sort((a,b)=>{
    const ia=PRIORITY.indexOf(a),ib=PRIORITY.indexOf(b);
    if(ia>=0&&ib>=0)return ia-ib;
    if(ia>=0)return-1;if(ib>=0)return 1;
    const ea=ecoNum(a),eb=ecoNum(b);
    if(ea!==null&&eb!==null)return ea-eb||a.localeCompare(b);
    if(ea!==null)return-1;if(eb!==null)return 1;
    return a.localeCompare(b);
  });
  const main=document.getElementById('main');
  const open=terms.length>0;
  main.innerHTML=catOrder.map(cat=>`
    <div class="cat-section">
      <div class="cat-header${open?' open':''}" data-cat="${escH(cat)}">
        <span class="cid">${escH(cat)}</span>
        <span class="cname">${escH(CATS[cat]||cat)}</span>
        <span class="ccount">${GROUPS[cat].length}</span>
        <span class="arrow">▶</span>
      </div>
      <div class="cat-files${open?' open':''}"></div>
    </div>`).join('');
  if(open)main.querySelectorAll('.cat-header').forEach(h=>fillCat(h.nextElementSibling,h.dataset.cat,false));
  document.getElementById('results').textContent=`${filtered.length} files in ${catOrder.length} categories`+(terms.length>0?' (searching: '+rawQ+' + synonyms)':'');
  const tc={};filtered.forEach(f=>tc[f.ext]=(tc[f.ext]||0)+1);
  document.getElementById('stats').innerHTML=`
    <div class="stat"><div class="num">${filtered.length}</div><div class="label">Files</div></div>
    <div class="stat"><div class="num">${catOrder.length}</div><div class="label">Categories</div></div>
    ${Object.entries(tc).sort((a,b)=>b[1]-a[1]).slice(0,8).map(([t,c])=>`<div class="stat"><div class="num">${c}</div><div class="label">.${escH(t)}</div></div>`).join('')}`;
  document.getElementById('typeFilters').innerHTML=Object.entries(tc).sort((a,b)=>b[1]-a[1]).slice(0,30).map(([t,c])=>
    `<span class="fbtn ${activeType===t?'on':''}" data-t="${escH(t)}">.${escH(t)} (${c})</span>`).join('');
}
document.getElementById('main').addEventListener('click',e=>{
  const cp=e.target.closest('.cpbtn');if(cp){copyPath(cp.dataset.p);return}
  const more=e.target.closest('.more');if(more){fillCat(more.parentElement,more.dataset.cat,true);return}
  const h=e.target.closest('.cat-header');
  if(h){h.classList.toggle('open');const box=h.nextElementSibling;box.classList.toggle('open');if(box.classList.contains('open')&&!box.dataset.filled)fillCat(box,h.dataset.cat,false)}
});
document.getElementById('typeFilters').addEventListener('click',e=>{const b=e.target.closest('.fbtn');if(b)setType(b.dataset.t)});
function toggleAll(open){document.querySelectorAll('.cat-header').forEach(h=>{const box=h.nextElementSibling;h.classList.toggle('open',open);box.classList.toggle('open',open);if(open&&!box.dataset.filled)fillCat(box,h.dataset.cat,false)})}
let _t;document.getElementById('search').addEventListener('input',()=>{clearTimeout(_t);_t=setTimeout(render,150)});
/*V4R-END*/"""

EXTRA_CSS = (
    ".lk{display:inline-block;font-size:8px;font-weight:700;padding:1px 4px;border-radius:3px;margin-right:6px;"
    "font-family:'JetBrains Mono',monospace;vertical-align:middle}"
    ".lk.gh{background:#111827;color:#fff}.lk.gd{background:#ede9fe;color:#5b21b6}"
    ".more{padding:6px 10px;font-size:11px;color:var(--accent);cursor:pointer;font-weight:700}"
    ".more:hover{color:var(--green)}\n"
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", default="index.html")
    ap.add_argument("--repo-list", required=True, help="git ls-tree -r -z --name-only output")
    ap.add_argument("--repo-sha", required=True)
    ap.add_argument("--repo-sizes", help="size<TAB>path lines (git ls-tree -l); enables size-proven name matches")
    a = ap.parse_args()

    html = open(a.html, encoding="utf-8").read()
    fm, F = load_array(html, "F", "[", "]")
    _, CATS = load_array(html, "CATS", "{", "}")

    old = [normalize_old(f) for f in F if not str(f.get("src", "")).startswith("GitHub")]
    for f in old:
        for k in ("u", "lk", "gh", "g"):
            f.pop(k, None)

    raw = open(a.repo_list, "rb").read().decode("utf-8")
    repo_all = [p for p in raw.split("\0") if p]
    repo = [p for p in repo_all if keep_repo_file(p)]

    sizes = {}
    if a.repo_sizes:
        for line in open(a.repo_sizes, encoding="utf-8"):
            if "\t" in line:
                sz, path = line.rstrip("\n").split("\t", 1)
                if sz.isdigit():
                    sizes[path] = int(sz)

    by_base = defaultdict(list)
    for p in repo:
        by_base[p.rsplit("/", 1)[-1].lower()].append(p)

    linked = set()
    gh_old = 0
    for f in old:
        cands = None if f.get("ext") == "dir" else by_base.get(f["n"].lower())
        hit = best_repo_match(f["path"], cands, int(f.get("s") or 0), sizes) if cands else None
        if hit:
            f["g"] = hit  # repo path; the page builds the GitHub URL
            linked.add(hit)
            gh_old += 1
        # no g -> the page builds a Google Drive search URL from the file name

    new = []
    for p in repo:
        top = p.split("/", 1)[0] if "/" in p else "(root)"
        cat = eco_from_path(p) or ("GH_" + re.sub(r"[^A-Za-z0-9]+", "_", top).strip("_").upper())
        # compact: n/size/tags are derived in the page; g=1 means path IS the repo path
        new.append({"cat": cat, "ext": ext_of(p), "path": p, "src": "GitHub/" + top, "g": 1})

    allf = old + new
    out = json.dumps(allf, ensure_ascii=False, separators=(",", ":"))
    out = out.replace("</", "<\\/")
    html = html[: fm.start(1)] + out + html[fm.end(1):]

    # A. Data Committee card
    html = html.replace("https://drive.google.com/drive/folders/unknown", DATA_COMMITTEE)

    # Header counts (computed, not typed)
    ext = Counter(f["ext"] for f in allf)
    cats = len({f["cat"] for f in allf})
    today = dt.date.today().strftime("%B %-d, %Y")
    sub = (f'<div class="sub">Updated {today} &bull; <span class="tag dl">Local Files</span> '
           f'<span class="tag gd">Google Drive</span> <span class="tag nc">GitHub @ {a.repo_sha[:7]}</span> &bull; '
           f'{len(allf):,} files &bull; {cats} categories &bull; {ext["md"]:,} MD &bull; {ext["sql"]:,} SQL</div>')
    html = re.sub(r'<div class="sub">Updated .*?</div>', lambda _: sub, html, count=1)
    note = ('<div class="sub" style="margin-top:6px;color:var(--green);font-size:11px">Click any file to open it: '
            '<b>GH</b> opens it on GitHub, <b>DRIVE</b> searches your Google Drive for it. COPY still grabs the path.</div>')
    html = re.sub(r'<div class="sub" style="margin-top:6px;color:var\(--green\);font-size:11px">.*?</div>',
                  lambda _: note, html, count=1)

    # Source filter gets a GitHub option
    if '<option value="GitHub">' not in html:
        html = html.replace('<option value="NCBOE">NCBOE-FEC</option>',
                            '<option value="NCBOE">NCBOE-FEC</option>\n<option value="GitHub">GitHub repo</option>')

    # Lazy, escaped renderer (replaces render() through the search listener)
    if "/*V4R-START*/" in html:
        start = html.index("/*V4R-START*/")
        end = html.index("/*V4R-END*/") + len("/*V4R-END*/")
    else:
        start = html.index("function render(){")
        marker = "document.getElementById('search').addEventListener('input',render);"
        end = html.index(marker) + len(marker)
    html = html[:start] + NEW_RENDER + html[end:]
    # toggleAll is redefined in NEW_RENDER; drop the original one-liner if present
    html = re.sub(r"function toggleAll\(open\)\{document\.querySelectorAll\('\.cat-header'\)\.forEach\(h=>\{if\(open\).*?\}\)\}\n", "", html, count=1)

    if ".lk{" not in html:
        html = html.replace("</style>", EXTRA_CSS + "</style>", 1)

    open(a.html, "w", encoding="utf-8").write(html)

    print(json.dumps({
        "original_v4_entries": len(old),
        "original_linked_to_github": gh_old,
        "original_drive_search_fallback": len(old) - gh_old,
        "repo_files_total": len(repo_all),
        "repo_files_after_quality_filter": len(repo),
        "repo_files_added": len(new),
        "repo_files_also_linked_from_originals": len(linked),
        "total_entries": len(allf),
        "categories": cats,
        "md": ext["md"], "sql": ext["sql"],
        "html_bytes": len(html.encode("utf-8")),
    }, indent=2))


if __name__ == "__main__":
    main()
