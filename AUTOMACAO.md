# Avisos automáticos do YouTube

Origem: https://www.youtube.com/@JOA00FC

- Discord: webhook definido no secret DISCORD_WEBHOOK_URL.
- Telegram: canal público @JOA00FCYT, bot @JOA00FCYT_bot, secret TELEGRAM_BOT_TOKEN.

Cada integração verifica o feed público a cada 15 minutos, em horários diferentes. A execução pode atrasar no GitHub. O computador e o celular não precisam ficar ligados.

A primeira execução valida o acesso e registra o histórico, sem publicar vídeos antigos. As seguintes enviam título e link das novas entradas do feed. Shorts e transmissões podem aparecer no feed; não existe detecção específica do começo de uma live. A lista do feed é limitada: uma interrupção prolongada ou muitos uploads entre verificações pode fazer publicações passarem sem aviso.

O registro fica em .automation, separado por destino. Não apague esses arquivos: a ausência inicia um novo registro e ignora o histórico. A mensagem é registrada depois da confirmação de envio; uma falha entre o envio e a gravação pode causar repetição na tentativa seguinte.

Em Actions, abra YouTube para Discord ou YouTube para Telegram para acompanhar execuções, usar Run workflow ou desativar a integração. Falhas aparecem em vermelho; os logs não exibem tokens. Corrija o secret ou as permissões e execute novamente.

Em repositórios públicos, o GitHub pode desativar agendamentos após 60 dias sem atividade no repositório. Confira Actions se ficar muito tempo sem publicar e reative o workflow se necessário.

Nunca coloque tokens nos arquivos do repositório. Para trocar o token, atualize o respectivo secret em Settings > Secrets and variables > Actions. O bot do Telegram precisa ser administrador do canal com Postar mensagens permitido.

Referências:
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule
- https://core.telegram.org/bots/api
