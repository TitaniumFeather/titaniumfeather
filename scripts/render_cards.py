"""Titanium OS / Minimal. Generates self-contained animated SVGs. Python stdlib only.
Run: python scripts/render_cards.py ; STATIC=1 python scripts/render_cards.py
Edit config.json for text, project URLs and identity. No GitHub API required.
"""
import html, json, os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
C=json.loads((R/'config.json').read_text(encoding='utf-8'))
OUT=R/'cards'; OUT.mkdir(exist_ok=True)
STATIC=os.environ.get('STATIC')=='1'
BG='#080A0B'; PANEL='#101415'; IVORY='#F1EEE5'; GOLD='#D7B54A'; CYAN='#19A9D1'; MUTED='#A3A39A'; LINE='#293034'
def e(s): return html.escape(str(s),quote=True)
def t(x,y,s,size=18,color=IVORY,weight=400,spacing=0,family='sans',extra=''):
    fam="'Arial Narrow',Impact,'DejaVu Sans',sans-serif" if family=='sans' else "'DejaVu Sans Mono',Consolas,monospace"
    return f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" letter-spacing="{spacing}" fill="{color}" {extra}>{e(s)}</text>'
def r(x,y,w,h,fill=PANEL,stroke='none',rx=0,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" {extra}/>'
def path(d,color=CYAN,width=1,extra=''):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" {extra}/>'
def svg(name,w,h,body):
    css="""<style>
    .reveal{animation:reveal .85s cubic-bezier(.2,.75,.2,1) both}.draw{stroke-dasharray:900;stroke-dashoffset:900;animation:draw 2.6s ease forwards}.glow{animation:glow 4s ease-in-out infinite}.scan{animation:scan 4s ease-in-out infinite}.float{animation:float 6s ease-in-out infinite}
    @keyframes reveal{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}@keyframes draw{to{stroke-dashoffset:0}}@keyframes glow{50%{opacity:.3}}@keyframes scan{0%,100%{transform:translateY(0)}50%{transform:translateY(125px)}}@keyframes float{50%{transform:translateY(-7px)}}
    @media(prefers-reduced-motion:reduce){*{animation:none!important;stroke-dashoffset:0!important;opacity:1!important}}
    """+(' *{animation:none!important;stroke-dashoffset:0!important;opacity:1!important}' if STATIC else '')+'</style>'
    (OUT/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{e(name)}">{css}{body}</svg>',encoding='utf-8')
def grid(w,h,step=42):
    return ''.join(path(f'M{x} 0 V{h}',LINE,.55, 'opacity=".28"') for x in range(0,w,step))+''.join(path(f'M0 {y} H{w}',LINE,.55,'opacity=".28"') for y in range(0,h,step))
def header(w,label,num):
    return t(32,34,'MA  /  TITANIUMFEATHER',13,GOLD,700,2,'mono')+t(w-32,34,f'{label}   /   {num}',12,MUTED,500,1,'mono','text-anchor="end"')+path(f'M32 49 H{w-32}',LINE)
def hero():
    w,h=1200,455
    b=r(0,0,w,h,BG)+grid(w,h,58)+header(w,'PORTFOLIO 2026','00')
    b+=t(40,100,'SOFTWARE ENGINEER  ·  CREATIVE BUILDER',15,GOLD,500,3,'mono')
    name=C['name'].upper().split()
    b+='<g class="reveal" style="animation-delay:.12s">'+t(32,225,name[0],137,IVORY,900,-6)+'</g>'
    b+='<g class="reveal" style="animation-delay:.28s">'+t(32,355,' '.join(name[1:]),149,IVORY,900,-7)+'</g>'
    b+=t(40,410,'BUILDING WITH PRECISION. PROGRAMMING WITH PURPOSE.',16,MUTED,400,2,'mono')
    # abstract architectural wireframe, right side
    b+=path('M880 96 L1010 68 L1143 126 L1013 158 Z',CYAN,1.4,'class="draw" opacity=".8"')
    b+=path('M880 96 V300 L1013 366 V158 M1013 366 L1143 306 V126 M880 300 L1010 273 L1143 306',CYAN,1.4,'class="draw" opacity=".65"')
    b+=path('M925 127 L1058 98 V307 L925 333 Z',GOLD,1.4,'class="draw" opacity=".7"')
    b+=path('M1058 98 L1098 115 V323 L1058 307 M925 333 L965 349 L1098 323',GOLD,1.1,'class="draw" opacity=".55"')
    for x,y in [(876,95),(1013,158),(1143,126),(1013,366),(925,333)]:b+=f'<circle cx="{x}" cy="{y}" r="3" fill="{GOLD}"/>'
    b+=t(893,393,'FIG. 01  /  STRUCTURE IN MOTION',10,CYAN,400,1,'mono')
    svg('hero.svg',w,h,b)
def statement():
    w,h=1200,270
    b=r(0,0,w,h,BG)+header(w,'THE PERSON BEHIND THE CODE','01')
    b+=t(40,115,'Curiosity is the',63,IVORY,700,-2)
    b+=t(40,190,'whole point.',78,GOLD,800,-3)
    b+=path('M655 83 V216',LINE,1)
    b+=t(690,105,'I study computer science at the University of Toronto.',20,IVORY)
    b+=t(690,145,'I like building at the intersection of systems,',20,MUTED)
    b+=t(690,180,'intelligence, and things people actually use.',20,MUTED)
    b+=t(690,226,'LESS TALK. MORE THINGS THAT WORK.',12,CYAN,500,2,'mono')
    svg('about.svg',w,h,b)
def section():
    w,h=1200,146
    b=r(0,0,w,h,BG)+header(w,'SELECTED WORK','02')
    b+=t(36,117,'Ideas, made real.',66,IVORY,800,-2)
    b+=t(1163,111,'04 / BUILDS',14,GOLD,500,2,'mono','text-anchor="end"')
    svg('projects-heading.svg',w,h,b)
def art(i):
    if i==0:
        a=r(650,83,475,228,'#0B1519',CYAN,10)+r(666,103,443,29,'#15242B',rx=4)
        a+= ''.join(f'<circle cx="{x}" cy="117" r="4" fill="{c}"/>' for x,c in [(685,GOLD),(699,CYAN),(713,MUTED)])
        a+=r(666,146,105,150,'#10232B',rx=4)+r(784,146,325,150,'#11191B',rx=4)
        a+=t(803,176,'lunara / workspace',13,CYAN,500,0,'mono')
        for k in range(3):a+=r(806+k*93,196,77,72,'#18323B',CYAN if k==1 else LINE,4)
        a+=path('M841 196 V268 M806 231 H883',GOLD,1.5,'class="draw"')
        return a
    if i==1:
        a=r(704,68,338,255,'#0C171B',CYAN,14)+r(724,87,298,216,'#111C20',LINE,7)
        # schematic scan cross section
        for rad in [100,80,61,40]:a+=f'<ellipse cx="873" cy="196" rx="{rad}" ry="{rad*.85}" fill="none" stroke="{CYAN if rad%2==0 else GOLD}" stroke-width="1.3" opacity=".55"/>'
        a+=path('M873 110 V283 M762 196 H985',CYAN,1,'opacity=".6"')
        a+=path('M804 173 Q834 133 861 170 T931 160 Q967 192 927 232 T853 246 Q801 236 804 173',GOLD,2,'class="draw"')
        a+=r(724,125,298,2,CYAN,rx=1,extra='class="scan" opacity=".8"')
        a+=t(1065,113,'SCAN / 002',12,CYAN,400,1,'mono')
        return a
    if i==2:
        a=r(650,78,485,240,'#0C171B',LINE,9)
        for yy in range(116,293,40):a+=path(f'M674 {yy} H1111',LINE,.8)
        for xx in range(685,1111,55):a+=path(f'M{xx} 100 V293',LINE,.8)
        a+=path('M679 264 L723 250 L755 259 L789 201 L823 222 L858 184 L892 202 L930 135 L964 160 L1003 122 L1044 145 L1100 109',CYAN,3,'class="draw"')
        a+=path('M679 278 L723 272 L755 267 L789 249 L823 256 L858 236 L892 231 L930 215 L964 224 L1003 203 L1044 211 L1100 188',GOLD,1.7,'class="draw" opacity=".75"')
        a+=t(688,105,'SIGNAL / MARKET STRUCTURE',12,GOLD,400,1,'mono')
        return a
    a=r(670,74,445,245,'#0C171B',CYAN,9)+r(670,74,445,29,'#16272C',rx=9)
    a+=''.join(f'<circle cx="{x}" cy="89" r="4" fill="{c}"/>' for x,c in [(690,GOLD),(705,CYAN),(720,MUTED)])
    a+=r(690,120,405,83,'#17282C',rx=4)+r(707,141,186,12,IVORY,rx=3)+r(707,162,125,8,GOLD,rx=3)
    a+=r(690,218,122,81,'#12252C',rx=4)+r(823,218,122,81,'#172F37',rx=4)+r(956,218,139,81,'#12252C',rx=4)
    a+=path('M977 261 L1003 237 L1029 261 L1052 245 L1080 261',CYAN,2,'class="draw"')
    return a
def project(i,p):
    w,h=1200,365
    b=r(0,0,w,h,BG)+r(16,8,w-32,h-16,PANEL,LINE,12)
    b+=t(44,56,p['category'],13,GOLD,600,2,'mono')
    b+='<g class="reveal" style="animation-delay:.1s">'+t(42,135,p['name'],56,IVORY,800,-2)+'</g>'
    b+=t(45,186,p['description'],18,MUTED)
    b+=path('M45 225 H555',LINE,1)+t(45,265,p['stack'],13,CYAN,500,1,'mono')
    b+=t(45,321,'EXPLORE PROJECT  ↗',15,GOLD,600,1,'mono')
    b+=art(i)
    svg(f'project-{i+1}.svg',w,h,b)
def footer():
    w,h=1200,215
    b=r(0,0,w,h,BG)+header(w,'OPEN FOR WHAT COMES NEXT','03')
    b+=t(36,128,'Have something ambitious in mind?',48,IVORY,750,-1)
    b+=t(40,180,'LET’S BUILD IT.',17,GOLD,600,3,'mono')
    b+=t(1160,182,'PORTFOLIO  /  GITHUB',14,CYAN,500,1,'mono','text-anchor="end"')
    svg('footer.svg',w,h,b)
hero();statement();section()
for i,p in enumerate(C['projects']):project(i,p)
footer()
print('Generated 8 SVGs in cards/')
