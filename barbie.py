import heapq
import time
import os
import pygame
import random
import csv
import pygame.mixer
import itertools
from PIL import Image

# Suprimir a mensagem inicial do Pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# Custos de cada tipo de terreno
terrenoCusto = {
    0: 2,            # grama (verde)
    1: float('inf'), # edifício (laranja)
    2: 10,           # paralelepípedo (branco)
    3: 3,            # terra (marrom)
    4: 1             # asfalto (cinza)
}

# Funções auxiliares para calcular custo e distância
def get_custoTerreno(terreno):
    return terrenoCusto.get(terreno, float('inf'))

# Calcula a distância de Manhattan entre dois pontos no plano cartesiano, somando as diferenças absolutas entre as coordenadas x e y dos pontos.
def calcular_distancia_manhattan(ponto1, ponto2):
    return abs(ponto1[0] - ponto2[0]) + abs(ponto1[1] - ponto2[1])

# Função para importar o mapa a partir de um arquivo CSV
def importar_mapa_csv(arquivo_csv):
    mapa = []
    with open(arquivo_csv, newline='') as csvfile:
        leitor = csv.reader(csvfile, delimiter=';')
        for linha in leitor:
            mapa.append([int(valor.strip()) for valor in linha if valor.strip() != ''])
    return mapa

# Função para calcular o custo total do caminho baseado nos tipos de terreno
def calcular_custo_total(path, map):
    custo_total = 0
    for node in path:
        tipo_terreno = map[node[0]][node[1]]
        if tipo_terreno == 1:  # Edifício
            return float('inf')
        custo_total += terrenoCusto.get(tipo_terreno, float('inf'))
    return custo_total

# Função para obter os vizinhos de um nó específico no grid
def get_vizinhos(atual, grid):
    linha, col = atual
    vizinhos = []
    movimentos_possiveis = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for move in movimentos_possiveis:
        nova_linha, nova_coluna = linha + move[0], col + move[1]
        if (0 <= nova_linha < len(grid) and 0 <= nova_coluna < len(grid[0]) and grid[nova_linha][nova_coluna] != 1):
            vizinhos.append((nova_linha, nova_coluna))
    return vizinhos

# Função heurística para a busca A*
def heuristic(a, b):
    ax, ay = a
    bx, by = b
    return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5

# A função a_star_segment implementa o algoritmo de busca A* para encontrar o caminho de menor custo entre dois pontos (start e goal) em um grid. Ou seja # Função de busca A* para um segmento (de um ponto a outro).
def a_star_segment(grid, start, goal, map):
    heap = [(0, start)] # Cria uma Heap(uma fila de prioridade)
    veio_de = {}
    custo_ate_agora = {start: 0}

    while heap: # heap é uma estrutura de dados especializada que permite acesso eficiente ao elemento mínimo ou máximo de um conjunto de dados
        _, no_atual = heapq.heappop(heap)
        if no_atual == goal:
            # Reconstrói o caminho e acumula custo
            path = []
            while no_atual in veio_de:
                path.append(no_atual) #acrescentar
                no_atual = veio_de[no_atual]
            path.append(start)
            return path[::-1], calcular_custo_total(path, map)

        for vizinho in get_vizinhos(no_atual, grid):
            custo_terreno = get_custoTerreno(grid[vizinho[0]][vizinho[1]])
            novo_custo = custo_ate_agora[no_atual] + custo_terreno
            if vizinho not in custo_ate_agora or novo_custo < custo_ate_agora[vizinho]:
                custo_ate_agora[vizinho] = novo_custo
                prioridade = novo_custo + heuristic(goal, vizinho)
                heapq.heappush(heap, (prioridade, vizinho))
                veio_de[vizinho] = no_atual

    return [], float('inf')

# Função principal de busca A* para visitar todos os amigos
def a_star_otimizado(grid, start, metas, map):
    start_time = time.time()
    amigos_aceitos, caminho_final, custo_total = [], [], 0
    posicao_atual = start
    
    # Armazena uma cópia das metas originais para revisão contínua
    metas_originais = metas[:]

    # Continua até que 3 amigos sejam convencidos
    while len(amigos_aceitos) < 3:
        # Ordena os amigos restantes pela menor distância a partir da posição atual
        metas.sort(key=lambda amigo: calcular_distancia_manhattan(posicao_atual, amigo))
        
        for amigo in metas:
            # Calcula o caminho para o próximo amigos
            sub_path, sub_cost = a_star_segment(grid, posicao_atual, amigo, map)

            if sub_cost < float('inf'): # Se o caminho for viável
                caminho_final.extend(sub_path[1:])  # Evita duplicação de pontos iniciais de cada subpath
                custo_total += sub_cost
                posicao_atual = amigo

                # Chance aleatória de aceitação
                if amigo not in amigos_aceitos and random.choice([True, False]):
                    amigos_aceitos.append(amigo)
                    print(f"Amigo na posicao {amigo} aceitou o convite!")

                # Para o loop se já convencemos 3 amigos
                if len(amigos_aceitos) >= 3:
                    break
        
        # Se já visitamos todos os amigos e ainda não convencemos 3, reiniciamos as metas
        if len(amigos_aceitos) < 3:
            print("Revisitar amigos para tentar convencer mais...")
            metas = [amigo for amigo in metas_originais if amigo not in amigos_aceitos]
            
             # Se as metas estão vazias e não conseguimos convencer 3 amigos, termina a execução
            if not metas:
                print("Nao foi possivel convencer 3 amigos.")
                break
    
    # Retorna para a Casa da Barbie se houve sucesso
    if amigos_aceitos:
        sub_path, sub_cost = a_star_segment(grid, posicao_atual, start, map)
        caminho_final.extend(sub_path[1:])
        custo_total += sub_cost

    # Exibe a lista final de amigos que aceitaram
    print("Amigos que aceitaram o convite ao final do processo:", amigos_aceitos)
    
    # Calcula o tempo total de execução do algoritmo(função)
    elapsed_time = time.time() - start_time
    
    # Retorna o caminho final, custo total e o tempo de execução
    return caminho_final, custo_total, elapsed_time


# Função para exibir o custo e o tempo de execução
def exibir_custo_total_e_tempo(custo_total, elapsed_time):
    print("\n")
    print(f"Custo Total do Caminho: {custo_total}")
    print(f"Tempo de Execucao da Funcao: {elapsed_time:.4f} segundos")

# Funções de desenho no Pygame
def draw_map(tela, map_matrix, cor_mapa, tamanho_bloco):
    for i, linha in enumerate(map_matrix):
        for j, celula in enumerate(linha):
            color = cor_mapa.get(celula, (255, 255, 255))
            pygame.draw.rect(tela, color, pygame.Rect(j * tamanho_bloco, i * tamanho_bloco, tamanho_bloco, tamanho_bloco))
    pygame.display.update()

def draw_special_points(tela, special_points, color, tamanho_bloco):
    for x, y in special_points:
        pygame.draw.rect(tela, color, (y * tamanho_bloco, x * tamanho_bloco, tamanho_bloco, tamanho_bloco))
    pygame.display.update()

def draw_path(tela, path, metas, starts, tamanho_bloco):
    for coord in path[1:]:
        if coord not in metas and coord not in starts:
            x, y = coord
            pygame.draw.rect(tela, (255, 192, 203), (y * tamanho_bloco, x * tamanho_bloco, tamanho_bloco, tamanho_bloco))
            pygame.display.update()
            pygame.time.delay(30)

def desenhar_personagens(tela, personagens, tamanho_bloco):
    for coord, character in personagens.items():
        x, y = coord
        img = pygame.image.load(character)
        img = pygame.transform.scale(img, (tamanho_bloco, tamanho_bloco))
        tela.blit(img, (y * tamanho_bloco, x * tamanho_bloco))
    pygame.display.update()

def contornar_casas_amigos(tela, amigos, tamanho_bloco):
    for amigo in amigos:
        x, y = amigo
        pygame.draw.rect(tela, (139, 0, 0), (y * tamanho_bloco, x * tamanho_bloco, tamanho_bloco, tamanho_bloco), 2)
    pygame.display.update()

# Funções de interface para interação com o usuário
def exibir_texto(tela, texto, posicao, fonte, cor=(255, 255, 255)):
    texto_surface = fonte.render(texto, True, cor)
    tela.blit(texto_surface, posicao)

def tela_jogar_novamente():
    tela.fill((0, 0, 0))  # Fundo preto
    fonte = pygame.font.SysFont("Helvetica", 36)
    exibir_texto(tela, "Jogar Novamente?", (300, 200), fonte)
    botao_sim = pygame.Rect(250, 300, 150, 50)
    botao_nao = pygame.Rect(450, 300, 150, 50)

    pygame.draw.rect(tela, (0, 255, 0), botao_sim)  # Botão verde para "Sim"
    pygame.draw.rect(tela, (255, 0, 0), botao_nao)  # Botão vermelho para "Não"

    exibir_texto(tela, "Sim", (290, 310), fonte)
    exibir_texto(tela, "Não", (490, 310), fonte)

    pygame.display.update()

    # Espera pela escolha do usuário
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if botao_sim.collidepoint(mouse_pos):
                    return "sim"
                elif botao_nao.collidepoint(mouse_pos):
                    pygame.quit()
                    return None

def tela_escolher_modo():
    tela.fill((0, 0, 0))  # Fundo preto
    fonte = pygame.font.SysFont("Helvetica", 36)
    exibir_texto(tela, "Escolha o modo de jogo", (250, 200), fonte)
    botao_manual = pygame.Rect(150, 300, 275, 50)
    botao_automatico = pygame.Rect(450, 300, 250, 50)

    pygame.draw.rect(tela, (0, 128, 255), botao_manual)  # Botão azul para "Manual e Editar"
    pygame.draw.rect(tela, (128, 0, 128), botao_automatico)  # Botão roxo para "Automático"

    exibir_texto(tela, "Manual e Editar Cor", (160, 310), fonte)
    exibir_texto(tela, "Automático", (500, 310), fonte)

    pygame.display.update()

    # Espera pela escolha do usuário
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if botao_manual.collidepoint(mouse_pos):
                    return "manual"
                elif botao_automatico.collidepoint(mouse_pos):
                    return "automatico"

def editar_cor_mapa(map, cor_mapa):
    editando = True
    fonte = pygame.font.SysFont("Helvetica", 24)
    exibir_texto(tela, "Clique em uma celula para alterar sua cor. Pressione Enter para concluir.", (50, 700), fonte)

    while editando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                editando = False  # Sai da edição ao pressionar Enter
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                x, y = mouse_pos[1] // tamanho_bloco, mouse_pos[0] // tamanho_bloco
                if 0 <= x < len(map) and 0 <= y < len(map[0]):
                    # Alterna as cores
                    tipo_terreno = map[x][y]
                    nova_cor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    cor_mapa[tipo_terreno] = nova_cor
                    draw_map(tela, map, cor_mapa, tamanho_bloco)
                    contornar_casas_amigos(tela, metas, tamanho_bloco)
                    desenhar_personagens(tela, personagens, tamanho_bloco)
        pygame.display.update()

def selecionar_amigos(metas):
    fonte = pygame.font.SysFont("Helvetica", 24)
    exibir_texto(tela, "Clique para selecionar 3 amigos. Pressione Enter para iniciar.", (50, 700), fonte)
    amigos_selecionados = []

    while len(amigos_selecionados) < 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and len(amigos_selecionados) == 3:
                return amigos_selecionados
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                x, y = mouse_pos[1] // tamanho_bloco, mouse_pos[0] // tamanho_bloco
                if (x, y) in metas and (x, y) not in amigos_selecionados:
                    amigos_selecionados.append((x, y))
                    pygame.draw.rect(tela, (255, 0, 0), (y * tamanho_bloco, x * tamanho_bloco, tamanho_bloco, tamanho_bloco), 3)

        pygame.display.update()

    return amigos_selecionados

def iniciar_jogo(map, cor_mapa, modo):
    # Redefine a tela e desenha o mapa e elementos iniciais
    tela.fill((0, 0, 0))
    draw_map(tela, map, cor_mapa, tamanho_bloco)
    draw_special_points(tela, [start], (0, 0, 255), tamanho_bloco)
    contornar_casas_amigos(tela, metas, tamanho_bloco)
    desenhar_personagens(tela, personagens, tamanho_bloco)

    if modo == "manual":
        editar_cor_mapa(map, cor_mapa)
        amigos_selecionados = selecionar_amigos(metas)
        if amigos_selecionados is None:
            return
        print("Amigos selecionados:", amigos_selecionados)
        caminho_final, custo_total, elapsed_time = a_star_otimizado(map, start, amigos_selecionados, map)
        draw_path(tela, caminho_final, amigos_selecionados, [start], tamanho_bloco)
        exibir_custo_total_e_tempo(custo_total, elapsed_time)

    elif modo == "automatico":
        caminho_final, custo_total, elapsed_time = a_star_otimizado(map, start, metas, map)
        draw_path(tela, caminho_final, metas, [start], tamanho_bloco)
        exibir_custo_total_e_tempo(custo_total, elapsed_time)


# Inicialização do Pygame e variáveis principais
pygame.init()
pygame.font.init()
pygame.mixer.init()
map = importar_mapa_csv('mapa.csv')
tamanho_bloco = 840 // max(len(map), len(map[0]))
tela = pygame.display.set_mode((840, 840))
pygame.display.set_caption("MUNDO BARBIE")
cor_mapa = {
    0: (0, 255, 0),       # Verde
    1: (255, 165, 0),     # Laranja
    2: (255, 255, 255),   # Branco
    3: (150, 75, 0),      # Marrom
    4: (86, 86, 86)       # Cinza
}

# Dicionário de personagens e suas coordenadas
personagens = {
    (4, 12): "personagens/cute.png",
    (5, 34): "personagens/boy.png", 
    (9, 8): "personagens/cute.png",
    (23, 37): "personagens/girl.png",
    (35, 14): "personagens/cute.png",
    (36, 36): "personagens/king.png",
    (22, 18): "personagens/barbie.png"
}

# Posições dos amigos (metas) e posição inicial
metas = [(4, 12), (5, 34), (9, 8), (23, 37), (35, 14), (36, 36)]
start = (22, 18)

# Função para exibir a tela inicial com botões
def tela_inicial():
    tela.fill((255, 105, 180))  # Fundo rosa choque
    fonte_titulo = pygame.font.SysFont("Helvetica", 48, bold=True)
    texto_titulo = fonte_titulo.render("MUNDO BARBIE", True, (255, 255, 255))
    tela.blit(texto_titulo, (250, 50))

    # Carregar e exibir a imagem
    imagem_barbie = pygame.image.load("imagens/barbie.png")
    imagem_barbie = pygame.transform.scale(imagem_barbie, (400, 400))
    tela.blit(imagem_barbie, (220, 150))

    # Definir botões com bordas arredondadas logo abaixo da imagem
    fonte_botao = pygame.font.SysFont("Helvetica", 32)
    botao_iniciar = pygame.Rect(270, 570, 300, 50)
    botao_sair = pygame.Rect(270, 640, 300, 50)

    pygame.draw.rect(tela, (0, 128, 0), botao_iniciar, border_radius=25)
    pygame.draw.rect(tela, (128, 0, 0), botao_sair, border_radius=25)

    texto_iniciar = fonte_botao.render("Iniciar Game", True, (255, 255, 255))
    texto_sair = fonte_botao.render("Sair", True, (255, 255, 255))

    tela.blit(texto_iniciar, (botao_iniciar.x + (botao_iniciar.width - texto_iniciar.get_width()) // 2, 
                              botao_iniciar.y + (botao_iniciar.height - texto_iniciar.get_height()) // 2))
    tela.blit(texto_sair, (botao_sair.x + (botao_sair.width - texto_sair.get_width()) // 2, 
                           botao_sair.y + (botao_sair.height - texto_sair.get_height()) // 2))

    pygame.display.update()

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if botao_iniciar.collidepoint(mouse_pos):
                    esperando = False
                elif botao_sair.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()
            elif event.type == pygame.KEYDOWN:
                esperando = False

print(r'''
                ,-`'-.
               /    , \
              (   ((_)))
              )  /  a a
             /  C     >
            (    \   =(
           /      )  ( )
          (   .--'.   ;-.
          )  '     `''   `
         /   |  , .--\|-(|
        (    |  |'       `
         `(  |  |     )   )
           `.|  |       .'
             |  |       ||
             (  ()      ||
              \  \      \|
               \  \      `
              /  \ \      \
             '    \ \      `
            /      | )>     \
           '       /\/\      `
          /       (_.,_)      \
         '       /      \      `
        (       (        )      )
         `-=.__  `--==--' __.=-'
gpyy           |`-.__.._.''
 &             |     |   |
jnj            `     |   |
 &              \    /   )
VK               :   )  /
                /   '   |
               |    |   |
               `    |   |
                \   |\  |
                 \  |)_ (
                 )  (_ \ \
                / \  \\ \_\_
                l\ \__\`____>
                  \____>
''')

# Loop principal do jogo
if __name__ == "__main__":
    
    # Carrega o áudio da Barbie
    pygame.mixer.music.load("sons/barbie_sound.mp3")

    # Inicia o áudio da Barbie quando o jogo começa
    pygame.mixer.music.play(-1)  # -1 faz com que o áudio seja reproduzido em loop

    tela_inicial()
    iniciar_jogo(map, cor_mapa, "automatico")

    while True:
        jogar_novamente = tela_jogar_novamente()
        if jogar_novamente == "sim":
            modo_jogo = tela_escolher_modo()
            if modo_jogo:
                iniciar_jogo(map, cor_mapa, modo_jogo)
        else:
            break
    pygame.quit()
