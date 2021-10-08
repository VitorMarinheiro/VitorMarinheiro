import numpy as np
import sys
import json
import random

global jogador_atual


def mover(direction):
    # realiza a leitura do README
    readme = open("README.md", "r").read()

    # Salva as categorias do arquivo
    cabecalho_do_readme = readme[0:readme.find('<!-- fim_do_cabecalho -->')] + '<!-- fim_do_cabecalho -->\n'
    cabecalho_do_jogo = readme[readme.find('<!-- inicio_do_cabecalho_do_jogo -->'):readme.find(
        '<!-- fim_do_cabecalho_do_jogo -->')] + '<!-- fim_do_cabecalho_do_jogo -->\n'
    tabuleiro = readme[
                readme.find('<!-- inicio_do_tabuleiro -->'):readme.find('<!-- final_do_tabuleiro -->')].replace(
        '<!-- inicio_do_tabuleiro -->', '')
    botoes = readme[readme.find('<!-- inicio_dos_botoes -->'):readme.find('<!-- final_dos_botoes -->')]
    comoissofunciona = readme[readme.find('<!-- inicio_como_isso_funciona -->'):readme.find(
        '<!-- final_como_isso_funciona -->')] + '<!-- final_como_isso_funciona -->\n'
    pontuacoes = readme[
                 readme.find('<!-- inicio_das_pontuacoes -->'):readme.find(
                     '<!-- final_das_pontuacoes -->')]
    frequencias = readme[
                 readme.find('<!-- inicio_da_frequencia -->'):readme.find(
                     '<!-- final_da_frequencia -->')]
    rodape = readme[
                 readme.find('<!-- inicio_do_rodape -->'):len(readme)]

    # Trata o tabuleiro
    campos = tabuleiro.split('|', 100)
    campos = list(filter((' - ').__ne__, campos))
    campos = list(filter(('\n').__ne__, campos))
    campos = list(filter(('\n\n').__ne__, campos))

    # Cria o tabuleiro 2D
    arr = np.array(campos)
    newarr = arr.reshape(6, 6)
    b = np.where(newarr == " :mag_right: ")

    # Valida se eh uma direcao possivel
    if validar_caminho(newarr, direction[0], b, True):
        incrementar_jogadas()

        if direction[0] == 'snakeup':
            aux_valor = newarr[int(b[0]) - 1][int(b[1])]
            newarr[int(b[0]) - 1][int(b[1])] = newarr[int(b[0])][int(b[1])]
            if ("space_invader" not in aux_valor):
                newarr[int(b[0])][int(b[1])] = aux_valor
            else:
                newarr[int(b[0])][int(b[1])] = '  '
                newarr = criar_novo_bug(newarr)
                incrementar_pontuacao()

        if direction[0] == 'snakedown':
            aux_valor = newarr[int(b[0]) + 1][int(b[1])]
            newarr[int(b[0]) + 1][int(b[1])] = newarr[int(b[0])][int(b[1])]
            if ("space_invader" not in aux_valor):
                newarr[int(b[0])][int(b[1])] = aux_valor
            else:
                newarr[int(b[0])][int(b[1])] = '  '
                newarr = criar_novo_bug(newarr)
                incrementar_pontuacao()

        if direction[0] == 'snakeleft':
            aux_valor = newarr[int(b[0])][int(b[1]) - 1]
            newarr[int(b[0])][int(b[1]) - 1] = newarr[int(b[0])][int(b[1])]
            if ("space_invader" not in aux_valor):
                newarr[int(b[0])][int(b[1])] = aux_valor
            else:
                newarr[int(b[0])][int(b[1])] = '  '
                newarr = criar_novo_bug(newarr)
                incrementar_pontuacao()

        if direction[0] == 'snakeright':
            aux_valor = newarr[int(b[0])][int(b[1]) + 1]
            newarr[int(b[0])][int(b[1]) + 1] = newarr[int(b[0])][int(b[1])]
            if ("space_invader" not in aux_valor):
                newarr[int(b[0])][int(b[1])] = aux_valor
            else:
                newarr[int(b[0])][int(b[1])] = '  '
                newarr = criar_novo_bug(newarr)
                incrementar_pontuacao()

    # Volta o array de 2D para 1D
    result = newarr.flatten()

    # Transforma o tabuleiro 2D em tabuleiro do markdown
    tabuleiro = "<!-- inicio_do_tabuleiro -->\n|" + result[0] + "|" + result[1] + "|" + result[2] + "|" + result[
        3] + "|" + result[4] + "|" + \
                result[5] + "|\n| - | - | - | - | - | - |\n|" + result[6] + "|" + result[7] + "|" + result[
                    8] + "|" + result[9] + "|" + result[10] + "|" + result[11] + "|\n|" + result[12] + "|" + result[
                    13] + "|" + result[14] + "|" + result[15] + "|" + result[16] + "|" + result[17] + "|\n|" + \
                result[18] + "|" + result[19] + "|" + result[20] + "|" + result[21] + "|" + result[22] + "|" + \
                result[23] + "|\n|" + result[24] + "|" + result[25] + "|" + result[26] + "|" + result[27] + "|" + \
                result[28] + "|" + result[29] + "|\n|" + result[30] + "|" + result[31] + "|" + result[32] + "|" + \
                result[33] + "|" + result[34] + "|" + result[35] + "|\n\n<!-- final_do_tabuleiro -->\n"

    # Inserir caminhos possiveis no readme
    botoes = setar_opcoes_de_caminho_no_read_me(newarr, np.where(newarr == " :mag_right: "))

    # Alterar o cabecalho com a pontuacao geral atual
    cabecalho_do_jogo = atualizar_cabecalho_do_jogo(cabecalho_do_jogo)

    # alterar as pontuacoes
    pontuacoes = atualizar_pontuacoes(pontuacoes)

    # altera os jogadores mais frequentes
    frequencias = atualizar_jogadores_frequentes(frequencias)

    # Cria o novo arquivo
    arquivo = cabecalho_do_readme + cabecalho_do_jogo + tabuleiro + botoes + comoissofunciona + pontuacoes + frequencias + rodape

    # Altera o Readme
    open('README.md', 'w').close()
    f = open("README.md", "a")
    f.write(arquivo)
    f.close()

def atualizar_jogadores_frequentes(frequencias):
    melhoresjogadores = lista_jogadores_frequentes()
    cabecalho = frequencias.split('\n\n')
    frequencias = frequencias.split('----------------------- |')
    jogadores = frequencias[1].split('|')

    jogadores[0] = '\n' + str(melhoresjogadores[0]["jogadas"]) + ' |'
    jogadores[1] = ' ' + str(melhoresjogadores[0]["name"]) + ' |'
    jogadores[2] = '\n' + str(melhoresjogadores[1]["jogadas"]) + ' |'
    jogadores[3] = ' ' + str(melhoresjogadores[1]["name"]) + ' |'
    jogadores[4] = '\n' + str(melhoresjogadores[2]["jogadas"]) + ' |'
    jogadores[5] = ' ' + str(melhoresjogadores[2]["name"]) + ' |'

    final = frequencias[0] + '----------------------- |' + jogadores[0] + jogadores[1] + jogadores[2] + jogadores[3] + \
            jogadores[4] + jogadores[5] + '\n\n' + cabecalho[1] + '<!-- final_da_frequencia -->\n'

    return final


def atualizar_pontuacoes(pontuacoes):
    melhoresjogadores = lista_melhores_jogadores()
    cabecalho = pontuacoes.split('\n\n')
    pontuacoes = pontuacoes.split('----------------------- |')
    jogadores = pontuacoes[1].split('|')

    jogadores[0] = '\n' + str(melhoresjogadores[0]["pontuacao"]) + ' |'
    jogadores[1] = ' ' + str(melhoresjogadores[0]["name"]) + ' |'
    jogadores[2] = '\n' + str(melhoresjogadores[1]["pontuacao"]) + ' |'
    jogadores[3] = ' ' + str(melhoresjogadores[1]["name"]) + ' |'
    jogadores[4] = '\n' + str(melhoresjogadores[2]["pontuacao"]) + ' |'
    jogadores[5] = ' ' + str(melhoresjogadores[2]["name"]) + ' |'

    final = pontuacoes[0] + '----------------------- |' + jogadores[0] + jogadores[1] + jogadores[2] + jogadores[3] + \
            jogadores[4] + jogadores[5] + '\n\n' + cabecalho[1] + '<!-- final_das_pontuacoes -->\n'

    return final


def lista_melhores_jogadores():
    a_file = open("src/jogadores.json", "r")
    json_object = json.load(a_file)
    a_file.close()
    json_jogadores = json_object["jogadores"]

    # captura a lista de maiores pontuacoes
    pontuacoes = []
    for jogador in json_jogadores:
        pontuacoes.append(jogador["pontuacao"])

    # Captura os jogadores com essas pontuacoes
    pontuacoes.sort(reverse=True)
    jogadores = []
    for pontuacao in pontuacoes:
        jogadores.append(
            next(item for item in json_jogadores if (item["pontuacao"] == pontuacao and jogadores.count(item) == 0)))
    return jogadores[0], jogadores[1], jogadores[2]


def lista_jogadores_frequentes():
    a_file = open("src/jogadores.json", "r")
    json_object = json.load(a_file)
    a_file.close()
    json_jogadores = json_object["jogadores"]

    # captura a lista de maiores pontuacoes
    jogadas = []
    for jogador in json_jogadores:
        jogadas.append(jogador["jogadas"])

    # Captura os jogadores com essas pontuacoes
    jogadas.sort(reverse=True)
    jogadores = []
    for jogada in jogadas:
        jogadores.append(
            next(item for item in json_jogadores if (item["jogadas"] == jogada and jogadores.count(item) == 0)))
    return jogadores[0], jogadores[1], jogadores[2]


def atualizar_cabecalho_do_jogo(cabecalho):
    campos = cabecalho.split(':')
    index = campos.index("star")

    # Captura a pontuacao
    f = open('src/status.json', )
    data = json.load(f)
    pontuacao = data['points']
    f.close()

    # Altera o valor do campo
    campos[index - 1] = " " + str(pontuacao) + " "

    count = 0
    for item in campos:
        if count < len(campos) - 1:
            campos[count] = campos[count] + ':'
            count = count + 1

    cabecalho = ''.join(campos)
    return cabecalho


def validar_caminho(tabuleiro, direcao, snake_pos, playing):
    aux_x = 0
    aux_y = 0

    # Valida as direcoes passadas
    if direcao == "snakeup":
        aux_x = int(snake_pos[0]) - 1
        aux_y = int(snake_pos[1])

    if direcao == "snakedown":
        aux_x = int(snake_pos[0]) + 1
        aux_y = int(snake_pos[1])

    if direcao == "snakeleft":
        aux_x = int(snake_pos[0])
        aux_y = int(snake_pos[1]) - 1

    if direcao == "snakeright":
        aux_x = int(snake_pos[0])
        aux_y = int(snake_pos[1]) + 1

    if ":construction:" in tabuleiro[aux_x][aux_y]:
        return False
    else:
        return True


def criar_novo_bug(tabuleiro):
    # Volta o array de 2D para 1D
    tabuleiro = tabuleiro.flatten()

    # Captura os indices vazios
    indices = [index for index, element in enumerate(tabuleiro) if element == '  ']
    index = random.randint(0, len(indices) - 1)

    # insere um novo bug
    tabuleiro[indices[index]] = " :space_invader: "

    return tabuleiro.reshape(6, 6)


def incrementar_jogadas():
    a_file = open("src/jogadores.json", "r")
    json_object = json.load(a_file)
    a_file.close()

    # Busca pelo jogador
    jogador_encontrado_bool = False

    json_jogadores = json_object["jogadores"]
    for jogador in json_jogadores:
        if jogador["name"] == jogador_atual:
            jogador_encontrado_bool = True
            jogador["jogadas"] = jogador["jogadas"] + 1

    # Caso o jogador nao seja encontrado adiciona um novo para ele
    if jogador_encontrado_bool == False:
        json_jogadores.append({u'jogadas': 1, u'name': u'' + jogador_atual + '', u'pontuacao': 0})

    # Atualiza o arquivo de jogadores
    a_file = open("src/jogadores.json", "w")
    json.dump(json_object, a_file)
    a_file.close()


def incrementar_pontuacao():
    # Incrementa a pontuacao do Status
    pontuacao = open("src/status.json", "r")
    json_object = json.load(pontuacao)
    pontuacao.close()

    json_object["points"] = json_object["points"] + 1

    pontuacao = open("src/status.json", "w")
    json.dump(json_object, pontuacao)
    pontuacao.close()

    # Incrementa a pontuacao do jogador
    jsonjogadores = open("src/jogadores.json", "r")
    json_object = json.load(jsonjogadores)
    jsonjogadores.close()

    json_jogadores = json_object["jogadores"]
    for jogador in json_jogadores:
        if jogador["name"] == jogador_atual:
            jogador["pontuacao"] = jogador["pontuacao"] + 1

    # Atualiza o arquivo de jogadores
    a_file = open("src/jogadores.json", "w")
    json.dump(json_object, a_file)
    a_file.close()


def setar_opcoes_de_caminho_no_read_me(tabuleiro, snake_pos):

    tabulation = '&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; '
    pre_url_open_issue = '(https://github.com/VitorMarinheiro/VitorMarinheiro/issues/new?title='
    post_url_open_issue = '&body=Just+push+%27Submit+new+issue%27+green+button.+The+README+will+be+updated+after+approximately+25+seconds)'

    # Valida UP
    if validar_caminho(tabuleiro, "snakeup", snake_pos, False):
        up = tabulation+'&nbsp; &nbsp; &nbsp;[:arrow_up:]'+pre_url_open_issue+'snakeup'+post_url_open_issue+'<br /> '
    else:
        up = tabulation+'\n&nbsp; &nbsp; &nbsp;:x:<br />'

    # Valida Left
    if validar_caminho(tabuleiro, "snakeleft", snake_pos, False):
        left = tabulation+'[:arrow_left:]'+pre_url_open_issue+'snakeleft'+post_url_open_issue
    else:
        left = tabulation+':x:'

    # Valida Down
    if validar_caminho(tabuleiro, "snakedown", snake_pos, False):
        down = '[:arrow_down:]'+pre_url_open_issue+'snakedown'+post_url_open_issue
    else:
        down = ':x:'

    # Valida Right
    if validar_caminho(tabuleiro, "snakeright", snake_pos, False):
        right = '[:arrow_right:]'+pre_url_open_issue+'snakeright'+post_url_open_issue
    else:
        right = ':x:'

    return '<!-- inicio_dos_botoes -->\n' + up + '\n' + left + '\n' + down + '\n' + right + '\n\n<!-- final_dos_botoes -->\n'


if __name__ == '__main__':
    jogador_atual = sys.argv[2:][0]
    mover(sys.argv[1:])
