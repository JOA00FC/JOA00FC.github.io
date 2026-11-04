# MW2 (2009) PC — campanha PT-BR FINAL 1.0

Versão final no escopo acordado: textos revisados, sem recriar imagens e vídeos. Os textos instalados são os mesmos da versão 0.2 que você confirmou funcionar. Não foram acrescentadas novas traduções nesta consolidação. Quem já possui a 0.2 íntegra receberá confirmação de que a tradução já está presente.

## Instalação única no Termux

Feche o jogo. Salve MW2_PTBR_CAMPANHA_FINAL_1.0.zip em Download. Execute, sem extrair o ZIP:

```sh
python ~/storage/downloads/MW2_PTBR_CAMPANHA_FINAL_1.0.zip --game "/storage/emulated/0/X360/Call of Duty - Modern Warfare 2" --action install
```

Mantenha o Termux aberto até a confirmação. Não apague nem restaure a versão anterior antes. O instalador aceita a base original verificada, a 0.1 e a 0.2 deste projeto, preservando os backups originais. Ele verifica os hashes e reconstrói apenas o necessário. Reserve aproximadamente 4 GB adicionais em uma instalação limpa; o espaço mínimo é calculado antes de gravar. Para quem já tem a 0.2, os arquivos traduzidos não precisam ser reconstruídos.

Use o caminho real da pasta que contém iw4sp.exe se ele for diferente do exemplo. O nome X360 da pasta não muda o alvo: esta tradução é para o jogo PC, não para os arquivos de Xbox 360.

Python já foi instalado no seu aparelho. Em uma configuração nova do Termux, execute termux-setup-storage, conceda acesso aos arquivos e instale Python com pkg install -y python.

## Restaurar ou verificar

Execute o mesmo ZIP sem --action install para abrir o menu: 1 instalar, 2 restaurar originais, 3 verificar, 4 sair.

Os backups ficam em MW2_PTBR_BACKUP_01, dentro da pasta do jogo. Não apague essa pasta. O instalador final restaura os 24 arquivos abrangidos; o pacote antigo 0.1 conhece apenas dois deles. Bases desconhecidas e backups alterados são recusados. Falhas tratadas acionam reversão. Se o processo for encerrado abruptamente, mantenha o backup e execute novamente antes de abrir o jogo.

## Conteúdo

Menus e opções, objetivos, instruções, HUD textual, legendas de diálogos, nomes de missões, armas e acessórios, mensagens de erro e inicialização, créditos e legendas externas dos vídeos de carregamento. São 5.912 entradas revisadas, das quais 5.085 foram alteradas. Nomes próprios, símbolos e números podem permanecer iguais após revisão.

Ative Legendas nas opções. O idioma-base continua English e os FastFiles permanecem em zone/english. Não copie os deltas da pasta payload para o jogo: o instalador é quem reconstrói os arquivos.

## O que permanece original

Áudio; texto desenhado nas imagens do HUD (por exemplo YOU, AMMO e TARGET); texto gravado dentro dos vídeos; placas e demais texturas. Multiplayer e SpecOps não são o objetivo desta tradução. As 1.422 chaves não traduzidas estão listadas em RELATORIO_TEXTOS.json, incluindo conteúdo de outros modos, legado e entradas vazias. Não foi comprovado que nenhuma delas possa aparecer dinamicamente na campanha.

Nenhum executável, save, driver ou ajuste de desempenho é instalado. Os recursos não textuais dos FastFiles são reaproveitados; consulte VALIDACAO.json para o escopo das comparações técnicas anteriores. Os testes do pacote final estão em TESTES_FINAIS.json. A confirmação do usuário é da base 0.2; não há registro de teste de todas as missões.

Base específica: PC IW4, executável 1.1.0.1525 e hashes da instalação fornecida. Confira COBERTURA.md e EXEMPLOS_NO_JOGO.md. Esta entrega encerra o escopo aceito; não afirma cobertura universal de todos os textos possíveis.

## Download público

[Baixar versão final 1.0](https://joa00fc.github.io/mw2-ptbr/download/MW2_PTBR_CAMPANHA_FINAL_1.0.zip)

SHA-256: `46c988fb84eb89234c3cee68e21d84977de209517cb81fee2dc93e96d93f5bdd`
