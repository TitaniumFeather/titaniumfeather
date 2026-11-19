"""Generate self-contained, animated SVG cards. No third-party dependencies.
STATIC=1 renders all elements at their final state for screenshots.
"""
import calendar
import datetime as dt
import html
import json
import os
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / 'config.json').read_text(encoding='utf-8'))
DATA_PATH = ROOT / 'data' / 'contributions.json'
DATA = json.loads(DATA_PATH.read_text(encoding='utf-8')) if DATA_PATH.exists() else {}
OUT = ROOT / 'cards'
OUT.mkdir(exist_ok=True)
C = CFG['theme']
STATIC = os.getenv('STATIC') == '1'


def esc(s):
    return html.escape(str(s), quote=True)


def txt(x, y, value, size=18, fill=None, weight=400, family='sans', extra=''):
    fam = 'ui-monospace, SFMono-Regular, Consolas, monospace' if family == 'mono' else 'Inter, Segoe UI, Arial, sans-serif'
    return f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" fill="{fill or C["text"]}" font-weight="{weight}" {extra}>{esc(value)}</text>'


def rect(x, y, w, h, fill=None, rx=12, stroke=None, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill or C["panel"]}" {f"stroke={chr(34)}{stroke}{chr(34)}" if stroke else ""} {extra}/>'


def svg(name, width, height, body, css=''):
    base = '''
      .enter { animation: rise .75s cubic-bezier(.2,.8,.2,1) both; }
      .fade { animation: fade .9s ease both; }
      .pulse { animation: pulse 3s ease-in-out infinite; }
      .shine { animation: shine 6s linear infinite; }
      @keyframes rise { from { opacity:0; transform:translateY(17px) } to { opacity:1; transform:translateY(0) } }
      @keyframes fade { from { opacity:0 } to { opacity:1 } }
      @keyframes pulse { 0%,100% { opacity:.35 } 50% { opacity:1 } }
      @keyframes shine { 0%,65% { opacity:.12 } 80% { opacity:.8 } 100% { opacity:.12 } }
      @media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation:none!important; transition:none!important; opacity:1!important; } }
    '''
    if STATIC:
        base += '*, *::before, *::after { animation:none!important; opacity:1!important; }'
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(name)}">
    <style>{base}{css}</style>{body}</svg>'''
    (OUT / name).write_text(content, encoding='utf-8')


def shell(w, h, heading, sub=''):
    body = rect(1, 1, w-2, h-2, C['background'], 20, C['border'])
    body += rect(25, 24, 9, 9, '#FF7272', 5) + rect(42, 24, 9, 9, '#F5C76D', 5) + rect(59, 24, 9, 9, '#63D9AC', 5)
    body += txt(85, 33, heading, 12, C['muted'], 600, 'mono')
    if sub:
        body += txt(w-26, 33, sub, 11, C['accent'], 500, 'mono', 'text-anchor="end"')
    body += f'<path d="M25 50 H{w-25}" stroke="{C["border"]}"/>'
    return body


# A custom ASCII feather, not a depiction of the user's face.
FEATHER = [
'                  .',
'                 /|',
'                //|',
'             . ///|',
'            / ////|',
'           / /////|',
'          / //////|',
'         / ///////|',
'        / ////////|',
'       / /////////|',
'       \\\\\\\\\\\\\\\\\\ |',
'        \\\\\\\\\\\\\\\\ |',
'         \\\\\\\\\\\\\\ |',
'          \\\\\\\\\\\\ |',
'           \\\\\\\\\\ |',
'            \\\\\\ |',
'             \\\\ |',
'              \\ |',
'                 |',
'                 |',
]


def hero():
    w, h = 1100, 440
    b = shell(w, h, 'titaniumfeather / profile', 'SYSTEM ONLINE')
    b += rect(32, 70, 670, 330, C['panel'], 16, C['border'])
    b += txt(58, 107, '01 / INITIALIZING PROFILE', 14, C['accent'], 600, 'mono')
    b += '<g class="enter" style="animation-delay:.1s">' + txt(58, 180, CFG['name'].upper(), 55, C['text'], 750) + '</g>'
    b += '<g class="enter" style="animation-delay:.35s">' + txt(58, 223, CFG['headline'], 19, C['accent'], 650, 'mono') + '</g>'
    b += '<g class="enter" style="animation-delay:.55s">' + txt(58, 263, CFG['subtitle'], 18, C['muted']) + '</g>'
    b += txt(58, 341, 'BUILDING SYSTEMS  /  SHIPPING PRODUCTS', 15, C['muted'], 500, 'mono')
    b += txt(58, 371, 'PYTHON    C++    REACT    LINUX    AI/ML', 14, C['accent'], 500, 'mono')
    b += rect(723, 70, 344, 330, '#0D192B', 16, C['border'])
    b += txt(747, 101, 'ASCII / FEATHER.SYS', 13, C['muted'], 500, 'mono')
    for i, line in enumerate(FEATHER):
        b += f'<g class="fade" style="animation-delay:{.8+i*.075:.3f}s">' + txt(776, 128+i*12.2, line, 12, C['accent'], 400, 'mono', 'xml:space="preserve"') + '</g>'
    b += txt(747, 377, 'ARTWORK: EDITABLE ASCII', 11, C['muted'], 500, 'mono')
    svg('hero.svg', w, h, b)


def parse_days():
    out = []
    for item in DATA.get('days', []):
        try:
            out.append((dt.date.fromisoformat(item['date']), max(0, int(item['contributionCount']))))
        except (ValueError, KeyError, TypeError):
            continue
    return sorted(out)


def heatmap(days):
    w, h = 1100, 240
    b = shell(w, h, 'contribution_matrix / last 365 days', 'LIVE GITHUB DATA' if days else 'AWAITING API DATA')
    if not days:
        b += txt(42, 125, 'Contribution calendar unavailable — configure GH_TOKEN in GitHub Actions.', 19, C['muted'])
    else:
        by_date = dict(days)
        end = max(d for d, _ in days)
        start = end - dt.timedelta(days=364)
        first = start - dt.timedelta(days=(start.weekday()+1)%7)
        for i in range(53):
            for j in range(7):
                day = first + dt.timedelta(days=i*7+j)
                if not start <= day <= end:
                    continue
                n = by_date.get(day, 0)
                color = '#1D2D43' if n == 0 else '#234B70' if n <= 2 else '#347CA9' if n <= 5 else '#65B8FF'
                b += rect(37+i*19.3, 73+j*19.5, 14, 14, color, 3, extra=f'class="fade" style="animation-delay:{i*.014+j*.012:.3f}s"')
        b += txt(40, 227, 'LESS', 11, C['muted'], 500, 'mono')
        for i, color in enumerate(['#1D2D43','#234B70','#347CA9','#65B8FF']):
            b += rect(83+i*18, 216, 12, 12, color, 2)
        b += txt(162, 227, 'MORE', 11, C['muted'], 500, 'mono')
    svg('heatmap.svg', w, h, b)


def streak(days):
    if not days:
        return 0
    counts = dict(days)
    d = max(counts)
    if counts.get(d, 0) == 0:
        d -= dt.timedelta(days=1)
    n = 0
    while counts.get(d, 0) > 0:
        n += 1
        d -= dt.timedelta(days=1)
    return n


def activity(days):
    w, h = 1100, 370
    b = shell(w, h, 'activity_analytics / contribution overview', 'ROLLING YEAR')
    if not days:
        b += txt(42, 150, 'Verified contribution statistics will appear after the first data refresh.', 19, C['muted'])
        svg('activity.svg', w, h, b)
        return
    total = DATA.get('total')
    if total is None:
        total = sum(n for _, n in days)
    active = sum(1 for _, n in days if n > 0)
    current_streak = streak(days)
    busiest = max(days, key=lambda pair: pair[1])
    stats = [('CONTRIBUTIONS', str(total)), ('ACTIVE DAYS', str(active)), ('CURRENT STREAK', f'{current_streak}d'), ('BUSIEST DAY', str(busiest[1]))]
    for i, (label, value) in enumerate(stats):
        x = 30+i*268
        b += rect(x, 70, 244, 92, C['panel'], 12, C['border'])
        b += txt(x+17, 99, label, 12, C['muted'], 500, 'mono')
        b += txt(x+17, 142, value, 34, C['text'], 750)
    months = defaultdict(int)
    for d, n in days:
        months[(d.year, d.month)] += n
    end = max(d for d, _ in days)
    keys = []
    for offset in range(11, -1, -1):
        y = end.year
        m = end.month-offset
        while m <= 0:
            m += 12
            y -= 1
        keys.append((y, m))
    values = [months[k] for k in keys]
    maximum = max(values) or 1
    b += txt(36, 198, 'MONTHLY CONTRIBUTIONS', 13, C['muted'], 600, 'mono')
    for i, ((year, month), value) in enumerate(zip(keys, values)):
        x = 45+i*86
        height = max(2, 105*value/maximum) if value else 2
        b += rect(x, 315-height, 51, height, C['accent'] if value == maximum else '#31658F', 5, extra=f'class="fade" style="animation-delay:{.25+i*.075:.2f}s"')
        b += txt(x+25, 337, calendar.month_abbr[month].upper(), 12, C['muted'], 500, 'mono', 'text-anchor="middle"')
        b += txt(x+25, 306-height, str(value), 12, C['text'], 500, 'mono', 'text-anchor="middle"')
    svg('activity.svg', w, h, b)


def specialties():
    items = [('systems.svg', '01 / SYSTEMS', 'ENGINEER', 'Linux · Automation · C++', 'Architecture and low-level tooling'),
             ('intelligence.svg', '02 / INTELLIGENCE', 'AI / ML', 'Models · Inference · APIs', 'Intelligent products and workflows'),
             ('products.svg', '03 / PRODUCTS', 'BUILDER', 'React · Backend · UX', 'From prototype to production')]
    for filename, kicker, title, stack, desc in items:
        w, h = 360, 215
        b = rect(1, 1, w-2, h-2, C['panel'], 17, C['border'])
        b += rect(24, 24, 37, 4, C['accent'], 2)
        b += txt(24, 58, kicker, 13, C['accent'], 600, 'mono')
        b += '<g class="enter" style="animation-delay:.3s">' + txt(24, 107, title, 32, C['text'], 750) + '</g>'
        b += txt(24, 151, stack, 15, C['muted'])
        b += txt(24, 185, desc, 13, C['muted'])
        b += f'<circle cx="326" cy="37" r="13" fill="none" stroke="{C["accent"]}" stroke-width="2" class="pulse"/>'
        svg(filename, w, h, b)


def projects():
    for i, project in enumerate(CFG['projects']):
        w, h = 530, 180
        b = rect(1, 1, w-2, h-2, C['panel'], 16, C['border'])
        b += txt(25, 38, f'{i+1:02d} / {project["category"]}', 13, C['accent'], 650, 'mono')
        b += '<g class="enter" style="animation-delay:.2s">' + txt(25, 83, project['name'], 29, C['text'], 700) + '</g>'
        b += txt(25, 117, project['description'][:64], 14, C['muted'])
        b += txt(25, 153, project['stack'], 13, C['accent'], 400, 'mono')
        b += txt(497, 45, '↗', 25, C['accent'], 500, extra='text-anchor="end"')
        svg(f'project-{i+1}.svg', w, h, b)


def tech():
    w, h = 1100, 180
    b = shell(w, h, 'technology_stack / tools of choice')
    for i, name in enumerate(CFG['skills'][:10]):
        x = 31+(i%5)*213
        y = 70+(i//5)*49
        b += rect(x, y, 196, 38, C['panel'], 9, C['border'])
        b += txt(x+15, y+25, name, 16, C['text'], 550, 'mono')
        b += rect(x+179, y+14, 8, 8, C['accent'], 4, extra='class="pulse"')
    svg('tech-stack.svg', w, h, b)


def main():
    days = parse_days() if DATA.get('available') else []
    hero()
    heatmap(days)
    activity(days)
    specialties()
    projects()
    tech()
    print(f'Rendered {len(list(OUT.glob("*.svg")))} SVG cards (STATIC={STATIC})')


if __name__ == '__main__':
    main()
