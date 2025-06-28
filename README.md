# Bomberman - Versão Final

Um jogo clássico de Bomberman desenvolvido em Python com Pygame.

## 🎮 Características

- **Dois personagens jogáveis**: Bomberman Clássico e Ninja Bomberman
- **Sistema de seleção de personagens** com interface intuitiva
- **Entrada de nome do jogador** personalizada
- **Sistema de ranking** para salvar as melhores pontuações
- **Múltiplos tipos de inimigos** com comportamentos diferentes
- **Sistema de power-ups** e melhorias
- **Músicas e efeitos sonoros** originais
- **Sistema de salvamento** de progresso

## 🚀 Como Jogar

### Instalação

1. Certifique-se de ter Python 3.7+ instalado
2. Instale o Pygame: `pip install pygame`
3. Execute o jogo: `python main.py`

### Controles

#### Menu Principal
- **Setas ↑↓**: Navegar no menu
- **Enter**: Selecionar opção
- **1/2**: Aumentar/Diminuir volume da música
- **3/4**: Aumentar/Diminuir volume dos efeitos sonoros
- **ESC**: Voltar ao menu

#### Seleção de Personagem
- **Setas ←→**: Navegar entre personagens
- **Mouse**: Clicar nos personagens
- **Enter**: Confirmar seleção
- **ESC**: Cancelar

#### Entrada de Nome
- **Teclado**: Digitar nome
- **Backspace**: Apagar caractere
- **Enter**: Confirmar nome
- **ESC**: Cancelar

#### Durante o Jogo
- **WASD** ou **Setas**: Mover o personagem
- **Espaço**: Plantar bomba
- **Ctrl Esquerdo**: Detonar bomba remota (se disponível)
- **ESC**: Pausar/Voltar ao menu

## 🎯 Personagens

### Bomberman Clássico
- **Velocidade**: Normal
- **Bombas**: Explosivas normais
- **Poder de fogo**: Padrão
- **Limite de bombas**: 2

### Ninja Bomberman
- **Velocidade**: Aumentada
- **Bombas**: De gelo (congelam inimigos)
- **Poder de fogo**: Reduzido
- **Limite de bombas**: 2

## 🎵 Sistema de Áudio

### Controles de Volume
- **Teclas 1/2**: Controlar volume da música
- **Teclas 3/4**: Controlar volume dos efeitos sonoros

### Músicas
- **Menu Principal**: BM - 01 Title Screen.mp3
- **Início de Estágio**: BM - 02 Stage Start.mp3
- **Música de Jogo**: BM - 03 Main BGM.mp3
- **Power-up**: BM - 04 Power-Up Get.mp3
- **Fim de Estágio**: BM - 05 Stage Clear.mp3
- **Power-up Especial**: BM - 07 Special Power-Up Get.mp3
- **Morte**: BM - 09 Miss.mp3

## 🏆 Sistema de Ranking

O jogo salva automaticamente as 10 melhores pontuações no arquivo `ranking.json`. Cada entrada inclui:
- Nome do jogador
- Pontuação
- Nível alcançado
- Data e hora

## 💾 Sistema de Salvamento

O progresso do jogo é salvo automaticamente no arquivo `savegame.txt` e inclui:
- Nome do jogador
- Nível atual
- Pontuação
- Vidas restantes
- Tipo de personagem
- Posição no mapa
- Inimigos restantes

## 🐛 Correções Implementadas

### Bugs Corrigidos
1. **Visualização do personagem**: Corrigido problema de renderização
2. **Navegação na seleção**: Melhorada a responsividade
3. **Inicialização de personagens**: Garantida inicialização correta
4. **Sistema de áudio**: Adicionado tratamento de erros
5. **Interface de usuário**: Melhorada a experiência do usuário

### Melhorias
1. **Feedback sonoro**: Sons de navegação e confirmação
2. **Indicadores visuais**: Setas de navegação na seleção
3. **Tratamento de erros**: Melhor robustez do código
4. **Interface responsiva**: Melhor experiência do usuário

## 🧪 Testes

Execute o arquivo de teste para verificar se tudo está funcionando:

```bash
python test_game.py
```

## 📁 Estrutura de Arquivos

```
bmb-version-finale/
├── main.py                 # Arquivo principal
├── game.py                 # Lógica do jogo
├── character.py            # Classe do personagem
├── character_selection.py  # Seleção de personagens
├── player_name_input.py    # Entrada de nome
├── assets.py              # Carregamento de recursos
├── gamesettings.py        # Configurações
├── enemy.py               # Inimigos
├── blocks.py              # Blocos do mapa
├── ranking.py             # Sistema de ranking
├── ranking_screen.py      # Tela de ranking
├── game_over_screen.py    # Tela de game over
├── info_panel.py          # Painel de informações
├── specials.py            # Power-ups
├── images/                # Imagens do jogo
├── sounds/                # Músicas e efeitos sonoros
├── ranking.json           # Arquivo de ranking
├── savegame.txt           # Arquivo de salvamento
└── test_game.py           # Arquivo de teste
```

## 🎮 Como Jogar

1. **Inicie o jogo**: Execute `python main.py`
2. **Selecione "Start"** no menu principal
3. **Escolha seu personagem**: Use as setas ou clique
4. **Digite seu nome**: Máximo 15 caracteres
5. **Jogue**: Use WASD para mover, Espaço para bombas
6. **Complete o estágio**: Elimine todos os inimigos
7. **Continue**: Avance para o próximo nível

## 🏆 Objetivo

Elimine todos os inimigos em cada estágio para avançar. Colete power-ups para melhorar suas habilidades e tente conseguir a maior pontuação possível!

## 📝 Licença

Este projeto é uma implementação educacional do jogo Bomberman.

---

**Divirta-se jogando!** 🎮 