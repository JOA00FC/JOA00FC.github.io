"""Publica novos videos no canal Telegram autorizado, sem expor tokens."""
import base64
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
from youtube_discord import CHANNEL, FEED, parse_feed, pending, request, http_failure, fetch_videos

CHAT = '@JOA00FCYT'
BOT = 'JOA00FCYT_bot'
STATE_PATH = '.automation/youtube-telegram-state.json'

class SetupError(Exception):
    pass


def telegram_request(bot_token, method, data=None, defer=lambda seconds: None):
    """Retry only explicit flood-control rejections, never ambiguous sends."""
    waited = 0
    for attempt in range(3):
        try:
            result = json.loads(request('https://api.telegram.org/bot' + bot_token + '/' + method,
                                        'POST', data or {}))
        except urllib.error.HTTPError as exc:
            if exc.code != 429:
                raise
            try:
                result = json.loads(exc.read())
            except (ValueError, UnicodeError):
                result = {}
            finally:
                exc.close()
            result['error_code'] = 429
        if result.get('error_code') == 429:
            seconds = result.get('parameters', {}).get('retry_after', 60)
            if type(seconds) is not int or seconds < 0:
                seconds = 60
            seconds += 1
            print('Telegram: limite em ' + method + '; aguardar ' + str(seconds) + ' segundos.', flush=True)
            if attempt == 2 or waited + seconds > 45:
                defer(seconds)
                raise SetupError('Espera do Telegram registrada; avisos pendentes serao retomados depois.')
            time.sleep(seconds)
            waited += seconds
            continue
        if result.get('ok') is not True:
            raise SetupError('Telegram nao confirmou a operacao ' + method + '.')
        return result['result']


def main():
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '').strip()
    if not re.fullmatch(r'\d+:[A-Za-z0-9_-]+', bot_token):
        raise SetupError('Secret TELEGRAM_BOT_TOKEN ausente ou invalido.')
    token = os.environ['GITHUB_TOKEN']
    repo = os.environ['GITHUB_REPOSITORY']
    endpoint = 'https://api.github.com/repos/' + repo + '/contents/' + STATE_PATH

    started = dt.datetime.now(dt.timezone.utc).isoformat()
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
        payload = {'message': 'Atualiza registro de avisos do Telegram [skip ci]', 'branch': 'main',
                   'content': base64.b64encode(json.dumps(value, ensure_ascii=False, indent=2).encode()).decode()}
        if sha:
            payload['sha'] = sha
        result = json.loads(request(endpoint, 'PUT', payload, token))
        sha = result['content']['sha']

    def defer(seconds):
        if state is not None:
            state['retry_not_before'] = time.time() + seconds
            save(state)

    if state and time.time() < state.get('retry_not_before', 0):
        print('Telegram em espera solicitada pela API; fila preservada.')
        return

    def telegram(method, data=None):
        return telegram_request(bot_token, method, data, defer)

    # Harmless reads validate the precise bot, destination and posting rights.
    me = telegram('getMe')
    if not me.get('is_bot') or me.get('username', '').lower() != BOT.lower():
        raise SetupError('O token nao pertence ao bot JOA00FCYT_bot.')
    chat = telegram('getChat', {'chat_id': CHAT})
    if chat.get('type') != 'channel' or chat.get('username', '').lower() != CHAT[1:].lower():
        raise SetupError('O destino nao corresponde ao canal @JOA00FCYT.')
    member = telegram('getChatMember', {'chat_id': chat['id'], 'user_id': me['id']})
    if member.get('status') != 'administrator' or not member.get('can_post_messages'):
        raise SetupError('Adicione o bot como administrador com permissao Postar mensagens.')
    print('Bot e canal corretos; permissao de postagem confirmada.')
    videos = fetch_videos(state)

    if state is None:
        save({'channel_id': CHANNEL, 'chat_id': chat['id'], 'started_at': started,
              'seen': [v['id'] for v in videos]})
        print('Inicializado: videos existentes registrados; nenhum aviso antigo enviado.')
        return
    if state.get('channel_id') != CHANNEL or state.get('chat_id') != chat['id'] or not isinstance(state.get('seen'), list):
        raise SetupError('Estado inconsistente; envio interrompido para evitar destino incorreto ou repeticoes.')
    queued = {v['id']: v for v in state.get('pending', [])}
    queued.update({v['id']: v for v in pending(videos, state)})
    new = [v for v in queued.values() if v['id'] not in state['seen']]
    changed = state.get('pending', []) != new or 'retry_not_before' in state
    state['pending'] = new
    state.pop('retry_not_before', None)
    if changed:
        save(state)
    for index, video in enumerate(new):
        if index:
            time.sleep(4)
        url = 'https://www.youtube.com/watch?v=' + video['id']
        result = telegram('sendMessage', {
            'chat_id': chat['id'],
            'text': '🎬 Novo vídeo no JOA00FC!\n\n' + video['title'][:300] + '\n\n' + url,
            'link_preview_options': {'is_disabled': False, 'url': url}})
        if not result.get('message_id') or result.get('chat', {}).get('id') != chat['id']:
            raise SetupError('Telegram nao confirmou a mensagem no canal esperado.')
        state['seen'].append(video['id'])
        state['pending'] = [v for v in state['pending'] if v['id'] != video['id']]
        save(state)
        print('Aviso enviado para o video ' + video['id'])
    print('Checagem concluida: ' + str(len(new)) + ' aviso(s) enviado(s).')


if __name__ == '__main__':
    try:
        main()
    except SetupError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
    except urllib.error.HTTPError as exc:
        print(http_failure(exc), file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print('Falha: ' + type(exc).__name__ + '. Credenciais e URLs privadas omitidas.', file=sys.stderr)
        sys.exit(1)

