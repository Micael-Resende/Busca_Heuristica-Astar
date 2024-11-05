Aqui está o `README.md` para o projeto:

---

# Mundo Barbie - Jogo A* Heurístico

Este é um jogo baseado no algoritmo de busca A* para a personagem Barbie, onde ela deve convencer três amigos a participarem de um concurso de programação. O projeto utiliza `Python` com `Pygame` para a interface gráfica e apresenta o mundo de Barbie em um mapa configurável, permitindo que o usuário interaja com o ambiente e personagens.

## Funcionalidades

- **Algoritmo A***: Implementação de uma busca otimizada para encontrar o caminho de menor custo para visitar três amigos e retornar ao ponto inicial.
- **Mapa Configurável**: O mapa é lido de um arquivo CSV (`mapa.csv`) e cada célula representa diferentes tipos de terrenos com custos distintos.
- **Interatividade com o Usuário**: Opção para selecionar o modo manual ou automático. No modo manual, é possível editar a cor do mapa e selecionar amigos para Barbie tentar convencer.
- **Interface Gráfica com Pygame**: Utiliza elementos gráficos para exibir o mapa, os personagens e o caminho da Barbie.
- **Áudio de Fundo**: Reprodução de música para ambientar o jogo.
- **Opção de Reiniciar o Jogo**: O jogador pode reiniciar o jogo e escolher um novo modo de jogo após a conclusão de cada partida.

## Tecnologias e Bibliotecas Utilizadas

- **Python**: Linguagem principal para desenvolvimento do jogo.
- **Pygame**: Biblioteca para criação da interface gráfica.
- **Heapq**: Utilizada para a fila de prioridade no algoritmo A*.
- **CSV**: Utilizado para leitura e configuração do mapa.
- **PIL**: Manipulação de imagens para os personagens.

## Como Jogar

1. **Inicialize o jogo**: Execute o arquivo principal para iniciar o jogo e abrir a tela inicial.
2. **Escolha o modo de jogo**: Após a tela inicial, escolha entre o modo "Manual e Editar Cor" ou "Automático".
   - **Manual**: Permite editar as cores do mapa e selecionar amigos.
   - **Automático**: Realiza uma busca automática para convencer três amigos.
3. **Objetivo**: Convencer três amigos a aceitarem o convite para o concurso de programação. O custo total do caminho é calculado com base nos diferentes tipos de terreno.

### Controles

- **Clique nos botões**: Para selecionar opções na tela inicial e reiniciar.
- **Mouse**: No modo manual, clique nas células do mapa para alterar as cores ou selecionar amigos.

## 🗺️ Arquivo de Mapa (`mapa.csv`) 

- O mapa é representado por uma matriz de números, onde cada número corresponde a um tipo de terreno com um custo específico de movimentação:
  - `0`: Grama (verde) - custo 2
  - `1`: Edifício (laranja) - custo infinito (obstáculo)
  - `2`: Paralelepípedo (branco) - custo 10
  - `3`: Terra (marrom) - custo 3
  - `4`: Asfalto (cinza) - custo 1

## 💻 Estrutura do Projeto

- **main.py**: Arquivo principal do jogo.
- **mapa.csv**: Arquivo CSV que representa o mapa do jogo.
- **sons/**: Pasta que contém o áudio de fundo (`barbie_sound.mp3`).
- **imagens/**: Pasta com a imagem da Barbie para a tela inicial e outros elementos gráficos.
- **personagens/**: Pasta com imagens dos personagens que representam os amigos no mapa.

## Exemplo de Jogo

Ao iniciar, Barbie aparece no ponto inicial e percorre o mapa tentando convencer três amigos. Cada movimento é guiado pelo algoritmo A* para otimizar o custo. A busca termina quando Barbie retorna ao ponto de partida após convencer três amigos.

## 🛠️ Instalação e Execução

1. **Pré-requisitos**:
   - Python 3.x
   - Bibliotecas: Pygame, PIL (Pillow)

2. **Instale as dependências**:
   ```bash
   pip install pygame pillow
   ```

3. **Execute o jogo**:
   ```bash
   python main.py
   ```

## Contribuição

Contribuições são bem-vindas! Por favor, faça um fork do projeto e envie um pull request com as melhorias.

## Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

Esse README fornece uma visão geral completa, informações de instalação, uso, e detalhes técnicos do projeto.

---

Made by Micael Resende
