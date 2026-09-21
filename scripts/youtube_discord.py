"""YouTube Atom -> Discord. Credentials are supplied only through Actions secrets."""
import base64
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

CHANNEL = 'UCMCFPb1NakRDqWgd0lmpPcg'
FEED = 'https://www.youtube.com/feeds/videos.xml?channel_id=' + CHANNEL
STATE_PATH = '.automation/youtube-discord-state.json'
NS = {'a': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015'}


def request(url, method='GET', data=None, token=None):
    headers = {'User-Agent': 'JOA00FC-video-notifier/1.0'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
        headers['Accept'] = 'application/vnd.github+json'
    if data is not None:
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=None if data is None else json.dumps(data).encode(), headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read()


def parse_feed(raw):
    root = ET.fromstring(raw)
    if root.findtext('yt:channelId', namespaces=NS) not in (CHANNEL, CHANNEL[2:]):
        raise ValueError('Feed recebido nao corresponde ao canal configurado.')
    videos = []
    for entry in root.findall('a:entry', NS):
        vid = entry.findtext('yt:videoId', namespaces=NS)
        title = entry.findtext('a:title', namespaces=NS)
        published = entry.findtext('a:published', namespaces=NS)
        if not vid or not re.fullmatch(r'[A-Za-z0-9_-]{11}', vid) or not title or not published:
            raise ValueError('Entrada de video incompleta.')
        dt.datetime.fromisoformat(published.replace('Z', '+00:00'))
        videos.append({'id': vid, 'title': title, 'published': published})
    if not videos:
        raise ValueError('Feed vazio: estado anterior preservado.')
    return sorted(videos, key=lambda item: item['published'])


def pending(videos, state):
    start = dt.datetime.fromisoformat(state['started_at'])
    seen = set(state['seen'])
    return [v for v in videos if v['id'] not in seen and dt.datetime.fromisoformat(v['published'].replace('Z', '+00:00')) >= start]


def main():
    webhook = os.environ.get('DISCORD_WEBHOOK_URL', '').strip()
    if not re.fullmatch(r'https://(?:canary\.|ptb\.)?discord(?:app)?\.com/api(?:/v\d+)?/webhooks/\d+/[A-Za-z0-9._-]+', webhook):
        raise ValueError('Configure o secret DISCORD_WEBHOOK_URL com a URL do webhook do Discord.')
    token = os.environ['GITHUB_TOKEN']
    repo = os.environ['GITHUB_REPOSITORY']
    endpoint = 'https://api.github.com/repos/' + repo + '/contents/' + STATE_PATH
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    videos = parse_feed(request(FEED))
    # Read-only verification, never prints webhook or token.
    info = json.loads(request(webhook))
    if info.get('type') != 1:
        raise ValueError('O webhook deve ser do tipo de entrada de mensagens.')
    sha = None
    try:
        stored = json.loads(request(endpoint + '?ref=main', token=token))
        sha = stored['sha']
        state = json.loads(base64.b64decode(stored['content']))
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise
        state = None

    def save(value):
        nonlocal sha
        payload = {'message': 'Atualiza registro de avisos do YouTube [skip ci]', 'branch': 'main',
                   'content': base64.b64encode(json.dumps(value, ensure_ascii=False, indent=2).encode()).decode()}
        if sha:
            payload['sha'] = sha
        result = json.loads(request(endpoint, 'PUT', payload, token))
        sha = result['content']['sha']

    if state is None:
        save({'channel_id': CHANNEL, 'started_at': started, 'seen': [v['id'] for v in videos]})
        print('Inicializado: webhook validado; videos existentes registrados sem publicar avisos antigos.')
        return
    if state.get('channel_id') != CHANNEL or not isinstance(state.get('seen'), list):
        raise ValueError('Estado inconsistente: execucao interrompida para evitar repeticoes.')
    new = pending(videos, state)
    for video in new:
        payload = {'content': '🎬 Novo vídeo no JOA00FC!\n' + video['title'][:300] + '\nhttps://www.youtube.com/watch?v=' + video['id'],
                   'allowed_mentions': {'parse': []}}
        # wait=true requires Discord to confirm the created message.
        result = json.loads(request(webhook + '?wait=true', 'POST', payload))
        if not result.get('id'):
            raise ValueError('Discord nao confirmou a mensagem; estado nao avancou.')
        state['seen'].append(video['id'])
        save(state)
        print('Aviso enviado para o video ' + video['id'])
    print('Checagem concluida: ' + str(len(new)) + ' aviso(s) enviado(s).')


if __name__ == '__main__':
    try:
        main()
    except urllib.error.HTTPError as exc:
        print('Falha HTTP ' + str(exc.code) + '. Confira o servico e as permissoes; nenhuma credencial foi registrada.', file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        # Network exceptions may contain a credential-bearing URL: print only the type.
        print('Falha: ' + type(exc).__name__ + '. Confira secrets, conectividade, feed e estado. Credenciais omitidas.', file=sys.stderr)
        sys.exit(1)
