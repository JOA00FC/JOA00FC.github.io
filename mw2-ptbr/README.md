# Call of Duty: Modern Warfare 2 (2009) — Tradução PT-BR JOA00FC

Tradução comunitária de legendas, menus, objetivos e cutscenes para a **versão de PC (IW4)**, testada pelo criador no **GameHub (Android/POCO F7)**. Projeto independente e não oficial.

## O que este pacote inclui

- Arquivo `sobreposicoes.json` com os textos em português para `common.ff`, `code_post_gfx.ff` e `patch.ff`.
- `subtitles.csv` com falas das cutscenes e seus horários.
- `REBUILD.py`: reconstrutor offline, com verificação rigorosa de SHA-256, backup e restauração. Precisa dos arquivos originais do usuário e OpenAssetTools 0.34.0.
- `instalar-termux.sh`: valida o jogo, baixa as fontes e oferece restauração. A reconstrução integral no Termux **ainda não foi homologada** para distribuição pública em um único clique.

O pacote **não contém FastFiles completos, o jogo, executáveis proprietários ou arquivos `.bik`**. O usuário precisa ter uma cópia legítima de MW2 PC.

## Compatibilidade

Somente os arquivos da versão testada do **Modern Warfare 2 de 2009 para PC**, nas localizações `zone/english/common.ff`, `zone/english/code_post_gfx.ff` e `zone/english/patch.ff`. O script bloqueia versões com SHA-256 diferentes.

Não funciona em MW2 Remastered (2020), Modern Warfare II (2022), nem nas versões Xbox 360 ou recompilações de console.

## Instalação limpa — primeira etapa sem modificações

Antes de traduzir, abra **Team Player** diretamente na instalação nova, ainda sem mods. O erro *Disc read error* pode existir independentemente da tradução.

Feche o GameHub, habilite o acesso ao armazenamento no Termux e rode (requer Python):

```bash
curl -fL --retry 3 https://joa00fc.github.io/mw2-ptbr/verificar-gamehub.py -o "$HOME/mw2-verificar.py" && python "$HOME/mw2-verificar.py"
```

O comando gera `/sdcard/Download/MW2_BASE_NOVA_RELATORIO.zip` contendo apenas hashes e inventário. Não envia nem altera dados do jogo e **não instala a tradução**. Confira o relatório antes de decidir que instalador é compatível.

Veja o [roteiro do vídeo do JOA00FC](./tutorial-para-canal.md) e o [verificador](./verificar-gamehub.py).

## Como usar no Android / Termux

1. Feche o jogo e o GameHub completamente.
2. Instale o Termux de fonte confiável e conceda acesso ao armazenamento usando `termux-setup-storage`.
3. Rode:

```bash
curl -fsSL https://joa00fc.github.io/mw2-ptbr/instalar-termux.sh -o $HOME/mw2-ptbr.sh && bash $HOME/mw2-ptbr.sh --verificar
```

Essa primeira etapa **apenas verifica** a base; não substitui arquivos. O modo automático de compilação em Android depende de runtime Linux x86 e permanece experimental. Nunca force manualmente um arquivo `.ff` incompatível.

## Linux PC (reconstrução avançada)

1. Baixe o ZIP deste projeto e extraia-o.
2. Baixe **OpenAssetTools v0.34.0** da [página oficial](https://github.com/Laupetin/OpenAssetTools/releases/tag/v0.34.0). O executável Linux atual é 32 bits: requer runtime i386 apropriado.
3. Confira os arquivos com:

```bash
python3 REBUILD.py --pasta '/caminho/Call of Duty - Modern Warfare 2' --verificar
```

4. Para reconstruir e instalar, após criar backup do jogo, execute:

```bash
python3 REBUILD.py --pasta '/caminho/Call of Duty - Modern Warfare 2' --oat '/caminho/ao/OpenAssetTools' --instalar
```

O script compara o SHA-256 de **todos os arquivos de saída** com a versão validada; qualquer divergência interrompe a instalação antes de substituir os `.ff`. O procedimento de reconstrução a partir de originais ainda está marcado como **beta**; não está homologado como instalador público universal.

Restauração, se o instalador tiver concluído e gerado os backups:

```bash
python3 REBUILD.py --pasta '/caminho/Call of Duty - Modern Warfare 2' --restaurar
```

## Arquivos e distribuição

Não fornecemos `common.ff`, `code_post_gfx.ff`, `patch.ff` nem o jogo. Para compartilhar a tradução, publique este pacote-fonte, não os FastFiles completos.

**Criador e testes:** JOA00FC, em colaboração com ChatGPT e ferramentas comunitárias. **Ferramenta usada:** [OpenAssetTools](https://github.com/Laupetin/OpenAssetTools), projeto independente e com licença própria.

**Status:** Funcionou em português no GameHub no teste do criador, com correção do limite de 7.000 textos e legendas das cinematográficas. Esse relato não valida automaticamente todas as versões e não constitui revisão individual de todas as frases.

**Contato:** [canal JOA00FC no YouTube](https://youtube.com/@JOA00FC).