"""Fetch real GitHub contribution data. Requires GH_TOKEN for GraphQL contributions.
No fake statistics: if the token is unavailable, contribution data remains unavailable.
"""
import datetime as dt
import json
import os
from pathlib import Path
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / 'config.json').read_text(encoding='utf-8'))
OUT = ROOT / 'data' / 'contributions.json'
TOKEN = os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
USERNAME = CFG['username']


def request(url, payload=None, auth=True):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'TitaniumOS-README', 'X-GitHub-Api-Version': '2022-11-28'}
    if TOKEN and auth:
        headers['Authorization'] = f'Bearer {TOKEN}'
    if payload is not None:
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=json.dumps(payload).encode() if payload is not None else None, headers=headers)
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.load(resp)


def main():
    now = dt.datetime.now(dt.timezone.utc)
    start = now - dt.timedelta(days=365)
    result = {'username': USERNAME, 'updated_at': now.isoformat(), 'available': False, 'days': [], 'total': None, 'repos': []}
    try:
        repos = request(f'https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated', auth=False)
        if isinstance(repos, list):
            result['repos'] = [{'name': r['name'], 'url': r['html_url'], 'description': r.get('description') or '', 'stars': r['stargazers_count']} for r in repos if not r.get('fork')][:30]
    except (urllib.error.URLError, ValueError, KeyError) as e:
        print(f'Repository fetch unavailable: {e}')
    if TOKEN:
        query = '''query($login:String!, $from:DateTime!, $to:DateTime!) {
          user(login:$login) { contributionsCollection(from:$from,to:$to) {
            contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
          } } }'''
        try:
            payload = request('https://api.github.com/graphql', {'query': query, 'variables': {'login': USERNAME, 'from': start.isoformat(), 'to': now.isoformat()}})
            if payload.get('errors'):
                raise ValueError(str(payload['errors']))
            calendar = payload['data']['user']['contributionsCollection']['contributionCalendar']
            result['days'] = [day for week in calendar['weeks'] for day in week['contributionDays']]
            result['total'] = calendar['totalContributions']
            result['available'] = True
        except (urllib.error.URLError, ValueError, KeyError, TypeError) as e:
            print(f'Contribution fetch unavailable: {e}')
    else:
        print('GH_TOKEN not provided: contribution counts will be shown as unavailable.')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # Preserve last verified calendar on temporary API errors, never replace with invented data.
    if not result['available'] and OUT.exists():
        try:
            previous = json.loads(OUT.read_text(encoding='utf-8'))
            if previous.get('available'):
                for key in ('available', 'days', 'total'):
                    result[key] = previous[key]
                result['data_as_of'] = previous.get('data_as_of', previous.get('updated_at'))
        except (ValueError, OSError):
            pass
    if result['available']:
        result['data_as_of'] = now.isoformat()
    OUT.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(f'Wrote {OUT}; calendar available={result["available"]}')


if __name__ == '__main__':
    main()
