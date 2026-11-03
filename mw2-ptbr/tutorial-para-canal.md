# Roteiro para o canal JOA00FC: MW2 (2009) PT-BR no GameHub

**Título sugerido:** MODERN WARFARE 2 (2009) EM PORTUGUÊS NO ANDROID | Tradução JOA00FC + GameHub

## Sequência da gravação

1. **Abertura:** mostrar a campanha em português e apresentar o projeto como tradução independente, não oficial.
2. **Jogo limpo:** mostrar a pasta `X360/Call of Duty - Modern Warfare 2`. Esclarecer que é MW2 (2009) **de PC**, e não Xbox 360 ou remasterizado.
3. **Teste de integridade no jogo:** abrir *Team Player* diretamente pelo menu **Selecionar missão**, antes da tradução. Se aparecer *Disc read error*, interromper a instalação e reparar os arquivos.
4. **Termux:** conceder acesso ao armazenamento e instalar Python, se necessário, com `pkg install python`.
5. **Verificação:** fechar o GameHub, colar o comando abaixo e mostrar o relatório `Download/MW2_BASE_NOVA_RELATORIO.zip`.
6. **Projeto no GitHub:** mostrar o site e o pacote-fonte disponível. Explicar que ele **não** contém os arquivos `.ff` originais nem o jogo.
7. **Instalação da tradução:** gravar a substituição **somente depois de validar a nova base e testar o processo de reconstrução**. Demonstrar backup, restaurar e testar *Team Player*, textos de menus e cutscenes.
8. **Encerramento:** apontar para o site e pedir que reportem erros com missão e captura.

## Comando único de verificação

```bash
curl -fL --retry 3 https://joa00fc.github.io/mw2-ptbr/verificar-gamehub.py -o "$HOME/mw2-verificar.py" && python "$HOME/mw2-verificar.py"
```

Este é um **verificador**, não um instalador automático. Não altera arquivos nem baixa o jogo.

## Descrição sugerida para o vídeo

Projeto de tradução PT-BR independente de Call of Duty: Modern Warfare 2 (2009) para PC, testado no GameHub para Android. Inclui tradução de menus, objetivos e legendas, inclusive cinematográficas. O pacote público atual é de fontes; a instalação universal está em beta e depende de confirmar a versão do jogo.

Página oficial: https://joa00fc.github.io/mw2-ptbr/
Fontes e documentação: https://github.com/JOA00FC/JOA00FC.github.io/tree/main/mw2-ptbr
Canal: https://youtube.com/@JOA00FC

A tradução não inclui cópia do jogo nem FastFiles proprietários.

## Etapa de manutencao (somente autor do projeto)

A instalacao limpa do GameHub carregou Team Player normalmente. Os hashes de `common.ff` e `code_post_gfx.ff` diferem da base usada na V6 anterior. Antes de gravar uma instalacao completa para o YouTube, reconstruiremos a traducao sobre os arquivos novos.

Comando do coletor (somente para quem mantem o projeto):

```bash
curl -fL --retry 3 https://joa00fc.github.io/mw2-ptbr/coletar-base-limpa.py -o "$HOME/mw2-coletar.py" && python "$HOME/mw2-coletar.py"
```

O ZIP criado em Download contem arquivos proprietarios do jogo. **Nao publicar este ZIP ou os FastFiles completos no GitHub nem no site.** O download publico deve continuar sendo o pacote-fonte da traducao ou, no futuro, patches diferenciais aplicaveis aos arquivos de cada jogador.

