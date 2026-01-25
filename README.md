# NC2A - Jogo de Computação Gráfica


[![Python Version](https://img.shields.io/badge/python-3.12.4-blue.svg)](https://www.python.org/downloads/)
[![Pygame Version](https://img.shields.io/badge/pygame-2.6.1-green.svg)](https://www.pygame.org/news)
[![Status](https://img.shields.io/badge/status-Em_Desenvolvimento-orange.svg)](#)


## Descrição do Projeto

Jogo 2D desenvolvido em Python com Pygame para a disciplina de Computação Gráfica. O jogador controla um personagem que navega por salas de aulas do prédio NC2A (Núcleo de Ciencias Aplicadas) para realizar tarefas no prédio.

**Tecnologias:** Python 3.x, Pygame

---

## Requisitos Implementados

- [x] **SetPixel** - Função base para todos os desenhos (`graphics.py`)
- [x] **Primitivas** - Algoritmos de Bresenham (reta) e Midpoint (círculo) (`graphics.py`)
- [x] **Preenchimento de Regiões** - Scanline e Flood Fill (`graphics.py`)
- [x] **Transformações Geométricas** - Rotação, escala e translação (`transformations.py`)
- [x] **Animação** - Ventiladores rotativos e portas com interpolação linear (`graphics.py`, `rooms.py`)
- [x] **Viewport** - Mini-mapa renderizado com set_pixel (`viewport.py`)
- [x] **Clipping** - Algoritmo de Cohen-Sutherland (`clipping.py`)
- [x] **Textura Procedural** - Padrões gerados matematicamente (`graphics.py`)
- [x] **Input (Teclado/Mouse)** - Controles completos para navegação e interação (`main.py`, `game.py`)
- [x] **Menu** - Sistema de menus com navegação por teclado e mouse (`menu.py`)

---

## Estrutura de Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `main.py` | Ponto de entrada do jogo |
| `constants.py` | Constantes (cores, dimensões, estados) |
| `camera.py` | Sistema de câmera (implementado manualmente) |
| `clipping.py` | Algoritmo Cohen-Sutherland |
| `transformations.py` | Transformações geométricas |
| `graphics.py` | Primitivas de desenho |
| `viewport.py` | Mini-mapa |
| `menu.py` | Sistema de menus |
| `game.py` | Lógica principal do jogo |
| `rooms.py` | Classe das salas |
| `player.py` | Classe do jogador |

---

##  Funcionalidades

### 1. SetPixel - Função Base

Todos os desenhos do jogo utilizam a função `set_pixel` como base. Esta função define um único pixel na tela, considerando a posição da câmera e o zoom. Nenhuma função pronta do Pygame para desenho de formas é utilizada.

---

### 2. Primitivas Gráficas

**Reta (Algoritmo de Bresenham):** Desenha linhas pixel a pixel de forma eficiente, calculando incrementalmente quais pixels devem ser acesos para formar a melhor aproximação de uma linha reta.

**Círculo (Algoritmo Midpoint):** Utiliza a simetria de 8 pontos para desenhar círculos de forma eficiente, calculando apenas 1/8 do círculo e replicando para os demais octantes.

**Retângulo:** Desenhado através de 4 chamadas da função de linha.

---

### 3. Preenchimento de Regiões

**Scanline (usado no jogo):** Preenche formas regulares linha por linha, percorrendo cada pixel dentro dos limites da forma. Utilizado para retângulos e círculos preenchidos.

**Flood Fill (usado no menu):** Algoritmo de preenchimento por inundação que preenche uma região a partir de um ponto semente. Implementado de forma iterativa com pilha para evitar stack overflow. Utiliza conectividade de 4 vizinhos.

---

### 4. Transformações Geométricas

**Rotação:** Rotaciona pontos em torno de um centro usando matriz de rotação com seno e cosseno.

**Escala:** Escala pontos em relação a um centro pelos fatores especificados em X e Y.

**Translação:** Desloca pontos por um vetor de deslocamento (dx, dy).

Estas transformações são aplicadas nos ventiladores animados e no sistema de câmera.

---

### 5. Animação

**Ventiladores Rotativos:** Cada sala possui um ventilador com 4 pás que rotacionam continuamente. O ângulo de rotação é atualizado a cada frame e aplicado usando a função de rotação de ponto.

**Portas Animadas:** As portas utilizam interpolação linear (lerp) entre dois keyframes - fechada (progress = 0.0) e aberta (progress = 1.0). A animação é suave e controlada por delta time.

---

### 6. Viewport (Mini-mapa)

O mini-mapa é uma representação em escala reduzida do mundo do jogo. Funciona através de:

1. Criação de uma matriz de cores representando o mundo (cada célula = 10x10 pixels)
2. Renderização da matriz usando apenas `set_pixel`

**Elementos representados:** Salas (cinza), paredes (preto), portas (amarelo/cinza), lousas (verde), mesas (marrom claro), cadeiras (marrom escuro) e jogador (vermelho).

---

### 7. Clipping (Cohen-Sutherland)

Algoritmo que determina quais partes de uma linha devem ser desenhadas, cortando as partes que ficam fora da região visível.

**Funcionamento:**
- Cada ponto recebe um código de 4 bits indicando sua posição (INSIDE, LEFT, RIGHT, TOP, BOTTOM)
- Se ambos os pontos estão dentro → linha aceita
- Se ambos compartilham região externa → linha rejeitada
- Caso contrário → calcula interseção e recorta

Aplicado automaticamente em todas as linhas antes do desenho.

---

### 8. Textura Procedural

Texturas geradas matematicamente sem uso de imagens. Disponíveis:

- **Brick:** Padrão de tijolos
- **Checker:** Xadrez (usado no fundo do menu)
- **Stripes:** Listras horizontais
- **Dots:** Padrão de bolinhas

Cada textura é calculada pixel a pixel baseada na posição do pixel no mundo.

---

### 9. Input (Teclado e Mouse)

**Teclado:**
- Movimento: W/A/S/D ou setas direcionais
- Sprint: SHIFT (esquerdo ou direito)
- Interação: E (abrir portas, usar lousas)
- Pausa: ESC

**Mouse:**
- Hover em opções de menu
- Click para selecionar opções
- Navegação completa nos menus

---

### 10. Sistema de Menus

**Menu Principal:** Fundo com textura xadrez, caixa central preenchida com Flood Fill, ventiladores animados decorativos, opções (Iniciar, Controles, Sair).

**Menu de Pausa:** Overlay escurecido sobre o jogo, opções (Continuar, Menu Principal, Sair).

**Tela de Controles:** Lista completa dos controles do jogo.

Navegação por teclado (W/S para mover, ENTER para selecionar) e mouse (hover + click).

---

##  Classes Principais

| Classe | Responsabilidade |
|--------|------------------|
| `Player` | Posição, movimento, colisão, desenho do personagem com detalhes faciais |
| `Room` | Salas com portas animadas, lousas, mesas e cadeiras |
| `Game` | Gerenciamento de estados, criação de salas, sistema de colisão e interações |
| `Camera` | Sistema de câmera manual com conversão mundo ↔ tela e seguimento do jogador |
| `Graphics` | Todas as primitivas de desenho, preenchimentos e texturas |
| `Viewport` | Mini-mapa com matriz de cores |
| `MenuSystem` | Menus principal, pausa e controles |

---

##  Controles

| Tecla | Ação |
|-------|------|
| W / ↑ | Mover para cima |
| S / ↓ | Mover para baixo |
| A / ← | Mover para esquerda |
| D / → | Mover para direita |
| SHIFT | Correr (sprint) |
| E | Interagir (portas/lousas) |
| ESC | Pausar jogo |
| Mouse | Navegação em menus + click em objetos |

---

##  Como Executar

Para executar instale o gerenciador de pacotes `uv` para gerenciar dependências. Após isso, clone o repositório e execute os comandos abaixo no terminal:

```bash
# Clonar o repositório
git clone https://github.com/janaina-ribeiro/computacao-grafica-t1

# Navegar até o diretório do projeto
cd computacao-grafica-t1

# Criar o ambiente virtual e instalar dependências do jogo
uv sync

# Executar o jogo
uv run main.py
```

---

##  Equipe

Desenvolvido para a disciplina de Computação Gráfica.

- **Integrante 1:** Janaína Ribeiro  
- **Integrante 2:** Joaquim Ribeiro
- **Integrante 3:** Marcio Gabriel  
- **Integrante 4:** Suyane Carvalho

