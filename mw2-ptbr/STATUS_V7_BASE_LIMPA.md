# MW2 PT-BR JOA00FC — Teste V7 na base limpa (03/11/2026)

## Estado atual

- A instalação limpa de **Call of Duty: Modern Warfare 2 (2009) para PC (IW4)** abriu a missão **Team Player** normalmente no GameHub, **antes** da tradução.
- Os três FastFiles originais dessa instalação foram identificados por SHA-256.
- A tradução a partir do pacote-fonte público foi recompilada localmente com OpenAssetTools 0.34.0.
- Verificação dos recursos: `common.ff` 4.240 localize; `code_post_gfx.ff` 1.590; `patch.ff` 124; **total 5.954**, abaixo do limite de 7.000. 
- Todas as 1.567 referências de tradução configuradas no projeto foram conferidas na exportação dos FastFiles recompilados.
- `video/subtitles.csv` preservou as 192 linhas e os horários originais.
- Os nomes e quantidades dos recursos originais dos dois grandes arquivos foram preservados. O patch ganhou 68 recursos apenas do tipo `localize`.
- Os testes em cópia local de **backup, instalação, restauração, integridade SHA-256 e bloqueio de versão desconhecida** foram aprovados.

**Importante: a V7 ainda não passou pelo teste real no GameHub depois da recompilação.** Não anuncie como instalação universal ou como correção definitiva do erro `Disc read error` até confirmar no aparelho que Team Player funciona e as cutscenes continuam legendadas.

## Identificação da base limpa suportada no teste

| Arquivo | SHA-256 original |
|---|---|
| `common.ff` | `f109313cc652fa1890223966bdb52157dd620f18183ccf4c4350cf61ed0c5e35` |
| `code_post_gfx.ff` | `1802c26386e08cb17660f19d3f511b89e081dfbbed8ad04b360f62fd5c6ae047` |
| `patch.ff` | `11be5452fa0f40aa7169c7a04810f9a5df8c0c782d0e9e403159159a322735c1` |

A versão de teste foi entregue ao mantenedor como pacote privado com backup automático. **Não publicar FastFiles completos, executáveis ou dados proprietários do jogo.** O material público do GitHub continua sendo a fonte da tradução, para reconstrução com cópia legítima da versão PC.

## Critérios de aprovação para o tutorial do YouTube

1. Instalar a V7 sobre a base limpa, preservando os backups originais.
2. Carregar **Team Player** diretamente sem `Disc read error`.
3. Reiniciar o jogo, carregar a campanha, conferir tradução do menu e legendas da cutscene.
4. Avançar na campanha para verificar missões seguintes.
5. Conferir a restauração dos três FastFiles caso apareça algum problema.

O roteiro do vídeo permanece em [tutorial-para-canal.md](./tutorial-para-canal.md).
