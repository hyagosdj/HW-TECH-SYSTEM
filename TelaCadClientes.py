from PySimpleGUI import PySimpleGUI as sg
import sqlite3
import pywhatkit
import keyboard
import time
from datetime import datetime

class TelaPythonSGUI():
    sg.theme('DarkBlue13')

    def criar_janela():
        menu = [
            ['ARQUIVOS', ['CLIENTES', 'SALVAR']],
            ['EDITAR', ['NOME', 'SOBRENOME', 'CONTATO', 'ENDEREÇO']],
            ['AJUDA', ['INFO']]
        
        ]

        col1 = [
            [sg.Text('[ O Futuro Começa Aqui ]', font='Blacksword 16', pad= (120, 0))],
            [sg.Text('ID do Cliente:')],
            [sg.Input(key='id', size=30, font='Arial 10 bold')],
            [sg.Text('Nome:')],
            [sg.Input(key='nome', size=30, font='Arial 10 bold')],
            [sg.Text('Sobrenome:')],
            [sg.Input(key='sobrenome', size=30, font='Arial 10 bold')],
            [sg.Text('Número:')],
            [sg.Input(key='ddd', size=5, font='Arial 10 bold'), sg.Input(key='numero', size=15, font='Arial 10 bold')],
            [sg.Text('Endereço:')],
            [sg.Input(key='endereco', size=30, font='Arial 10 bold')],
            [sg.Text('Nº da Residência:')],
            [sg.Input(key='nres', size=13, font='Arial 10 bold')],
            [sg.Text('Complemento:')],
            [sg.Input(key='complemento', size=30, font='Arial 10 bold')],
            [sg.Text('\n')],
            [sg.Button('REGISTRAR', size=15, font='Arial 10 bold', button_color='blue'), sg.Button('LIMPAR CAMPOS', size=15, font='Arial 10 bold', button_color='gray'), 
            sg.Button('ALTERAR DADOS', size= 15, font='Arial 10 bold', button_color='Brown'), sg.Button('ENVIAR WhatsApp', size=15, font='Arial 10 bold', button_color='Green')],
        ]

        col2 = [
            [sg.Output(background_color='black', text_color='white', size=(55, 26), font= 'Century 9 bold', key='saida')],
            [sg.Text(' ' * 20), sg.Button('LIMPAR TELA', size= 15, font='Arial 10 bold', button_color='black'), 
            sg.Button('EXCLUIR CLIENTE', size= 15, font='Arial 10 bold', button_color='red')],
        ]

        layout = [
            [sg.Menu(menu, background_color='White', key='clientes')],
            [sg.Text('[ HW Tech Production ]', font='Blacksword 20', pad= (100, 10, (10, 10)))],
            [sg.Column(col1, pad=(30, 0, (0,6))), sg.Column(col2, pad=(30, 0, (0,0)))],
            [sg.Text(' ' * 250), sg.Text('[By.: HyagoS™]', font='Blacksword 15')]
        ]
        return sg.Window('HW TECH SYSTEM', layout= layout, finalize= True)

    janela = criar_janela()

    while True:
        window, events, values = sg.read_all_windows()
        id = values['id']
        nome = values['nome']
        sobrenome = values['sobrenome']
        ddd = values['ddd']
        numero = values['numero']
        end = values['endereco'].replace(' ', '')
        nres = values['nres']
        complemento = values['complemento']

        limpar = window['id'].set_focus(), 
        window['id'].update(''),
        window['nome'].update(''),
        window['sobrenome'].update(''),
        window['numero'].update(''),
        window['ddd'].update(''),
        window['endereco'].update(''),
        window['nres'].update(''),
        window['complemento'].update('')

        contatos = []

        # Conexão com Bando de Dados
        banco = sqlite3.connect('first_database.db')
        cursor = banco.cursor()
        cursor.execute("CREATE TABLE if not exists clientes (Id integer primary key, Nome text, Sobrenome text, DDD integer, Contato integer, Endereço text, Numero integer, Complemento text)")
        banco.commit()

        def get_clientes():
            banco = sqlite3.connect('first_database.db')
            cursor = banco.cursor()
            cursor.execute('SELECT * FROM clientes')
            linhas = cursor.fetchall()
            print('*' * 62)
            print('NOMES DOS CLIENTES:')
            print('*' * 62)            
            for linha in linhas:
                print('ID: ', linha[0])
                print('Nome: ', linha[1], linha[2])
                print('Contato: ', linha[3], linha[4])
                print('Endereço: ', linha[5], linha[6], linha[7], '\n')
                print('*' * 62)

        if events == sg.WINDOW_CLOSED:
            break

        elif events == 'REGISTRAR':
            try:
                if values['id'].isnumeric() and values['nome'].isalpha() and len(values['nome']) >= 3 and values['sobrenome'].isalpha() and values['ddd'].isdigit() and 1 < len(values['ddd']) <= 3 and values['numero'].isdigit() and 7 < len(values['numero']) <= 9 and values['nres'].isdigit() and len(end) >= 3 and end and not end == None and not values['complemento'] == None:
                    # TABELA DO BANCO DE DADOS
                    cursor.execute("INSERT INTO clientes VALUES ('"+str(id)+"', '"+nome+"', '"+sobrenome+"', '"+str(ddd)+"', '"+str(numero)+"', '"+str(values['endereco'])+"','"+str(nres)+"', '"+str(complemento)+"')")
                    banco.commit()

                    # Limpar campos após registrar
                    limpar
                    window['saida'].update('')
                    print('*' * 62)
                    print('CLIENTE CADASTRADO:')
                    print('*' * 62)
                    print(f"ID: {values['id']} \nNome: {values['nome'].strip().replace(' ', '')} {values['sobrenome'].strip().replace(' ', '')} \
\nNúmero: ({values['ddd']}) {values['numero']}\nEndereço: {values['endereco'].strip()}, Nº: {values['nres']}, {values['complemento']}\n")
                    print('*' * 62)
                else:
                    sg.popup('VERIFIQUE SE DIGITOU CORRETAMENTE TODOS OS CAMPOS!\n\nLembrando:\n\nID: São únicas, \n\nNome: Maior ou igual três (3) letras\n\nDDD: Três (3) dígitos\n\n'
                    'Número: Nove (9) dígitos, caso sua a região não tenha 9, colocar o numeral: 0, no início.\n\nNº da Residência: Somente dígitos.\n\nComplemento: Opcional.\n\n', font='Arial 12 bold', title='ALERTA!')
            except:
                sg.popup('O Campo ID é exclusivo para cada cliente.\n\nVÁ NA BARRA DE MENU: SELECIONE: ARQUIVOS[CLIENTES] e verifique!', font='Arial 10 bold', title='ALERTA!')

        elif events == 'LIMPAR CAMPOS':
            if not id and not nome and not sobrenome and not ddd and not numero and not end and not nres and not complemento:
                sg.popup('OS CAMPOS JÁ ESTÃO LIMPOS.', font='Arial 10 bold', title='ERRO!' )
            else:
                # Tornar o bloco de código abaixo em uma função 
                limpar
                sg.popup('CAMPOS LIMPOS COM SUCESSO!', font='Arial 12 bold', title='ALERTA!')

        elif events == 'LIMPAR TELA':
            # Encontrar uma forma de saber se a tela já está em branco
            window['saida'].update('')    
            sg.popup('TELA LIMPA COM SUCESSO!', font='Arial 12 bold', title='ALERTA!')

        elif events == 'EXCLUIR CLIENTE':
            sg.popup('A EXCLUSÃO DE CLIENTES É DE ACORDO COM A [ID] REF AO MESMO.', font='Arial 10 bold', title='LEMBRETE!')
            try:
                if not values['id']:
                    sg.popup('VOCÊ DEVE INSERIR UM [ID] EXISTENTE PARA EXCLUIR UM CLIENTE', font='Arial 10 bold', title='ERRO!')

                elif values['id'].isdigit():
                    cursor.execute("SELECT Id FROM clientes WHERE Id= '"+id+"'")
                    clientes = cursor.fetchall()
                    for c in clientes:
                        if c[0] == int(id):
                            cursor.execute("DELETE FROM clientes WHERE Id = '"+id+"'")
                            banco.commit()
                            banco.close()
                            sg.popup(f'CLIENTE EXCLUÍDO COM SUCESSO!', font='Century 10 bold', title='ALERTA!')
                            window['saida'].update('')
                            get_clientes()
                            break
                    else:
                        sg.popup(f"O ID: {values['id']} NÃO FOI LOCALIZADO!\n\nVERIFIQUE EM: BARRA DE MENU → [ARQUIVOS → [CLIENTES]]",
                        font='Arial 10 bold', title='ATENÇÃO!')
                else:
                    sg.popup(f"LEMBRE-SE: SOMENTE DÍGITO(S)!", font='Arial 10 bold', title='ALERTA!')
            except:
                sg.popup('ERRO: VOCÊ DIGITOU CORRETAMENTE?', font='Arial 10 bold', title='ERRO!')
            
        elif events == 'CLIENTES':
            window['saida'].update('')
            get_clientes()

        elif events == 'SALVAR':
            banco = sqlite3.connect('first_database.db')
            cursor = banco.cursor()
            cursor.execute('SELECT * FROM clientes')
            itens = cursor.fetchall()
            for item in itens:
                with open('CLIENTES.txt', 'a+') as a:
                    a.write(f'ID DO CLIENTE: {item[0]}, Nome: {item[1]} {item[2]}, Contato: ({item[3]}) {item[4]}, Endereço: {item[5]}, Nº: {item[6]}, Complemento: {item[7]}.\n')

            else:
                sg.popup('CLIENTES SALVOS, VERIFIQUE DENTRO DA PASTA DESTE PROGRAMA.', font='Arial 10 bold', title='AVISO!')

        elif events == 'INFO':
            window['saida'].update('')
            print('*' * 62)
            print('• ESSE SISTEMA FOI CRIADO PELO ESTUDANTE DE PYTHON • \n\
                                        HYAGO WENDEL')
            print('*' * 62)
            print('\nEssa é uma produção educacional onde foi investido tempo e \nconhecimento e muita prática para compor um sistema integrado \ncom \
banco de dados e com interface gráfica para facilitar a \ninteração com os usuários finais\n')
            print('Essa ferramenta deve ser utilizada da seguinte maneira: \n')
            print('• REGISTRAR CLIENTE')
            print('Preencha todos os campos, caso deixe algo incorreto o sistema \napagará as informações já preenchidas.')
            print('Após preencher essas informações e revisá-las, então você deve \nclicar em [REGISTRAR].\n')
            print('• EXCLUIR CLIENTE')
            print('Para excluir um Cliente, você pode simplesmente clicar na aba \n[ARQUIVOS] e clicar em [CLIENTES]')
            print('Essa opção mostrará os dados de todos os Clientes, identifique o \nID do qual deseja excluir e coloque no campo ID do Cliente e \nPressione \
em [EXCLUIR CLIENTE].\n')
            print('• LIMPAR CAMPO OU TELA')
            print('Outra coisa está a sua disposição são os botões de \n[LIMPAR CAMPOS] e o de [LIMPAR TELA].\n')
            print('• ALTERAR INFORMAÇÕES')
            print('Para alterar informações, basta selecionar o [ID DO CLIENTE] e \nalterar a informação que desejar.')
            print('Agora você pressiona o botão [ALTERAR DADOS] para confirmar \na alteração.')
            print('No painel ao lado aparecerá a lista de cliente para você verificar \ntudo que foi feito.\n')
            print('• ENVIAR MENSAGEM POR WHATSAPP')
            print('Você também possui o botão de [ENVIAR WHATSAPP], porém, \nvocê deve seguir estes passos: ')
            print('1- Abrir o seu WhatsApp Web e conectar corretamente no seu \nNavegador.')
            print('2- Preencher no formato completo o campo de número de contato: \n+5585123456789')
            print('3- Preencher o campo de mensagem com a mensagem que desejar.')
            print('4- Clicar em [ENVIAR MENSAGEM] e aguardar todo o processo ser concluído.\n')
            print('*Duração média de 5 minutos até o fim do processo.*\n')
            print('Para seu auxílio, terá a sua disposição um botão: \n[MOSTRAR TODOS] que mostrará todos os contatos \ncadastrados.\n')
            print('• ABAS')
            print('São elas: ARQUIVOS | EDITAR | AJUDA\n')
            print('ARQUIVOS: é onde você encontrará as funcionalidades [SALVAR] que salvará os dados dos clientes em um arquivo .TXT dentro da \npasta atual do sistema e a \
de Listar todos os Clientes \npressionando em [CLIENTES]\n')
            print('EDITAR: nesta servirá para preencher automaticamente os campos que deseja editar, porém precisará preencher o campo \n[ID DO CLIENTE] \
referente ao que quer editar/alterar\n')
            print('AJUDA: Este mostrará informações relevantes e uma breve \nexplicação das funcionalidades que este sistema possui e por quem foi criado e qual a finalidade do mesmo.')
            print('\n' + '*' * 62)

        elif events == 'NOME':
            banco = sqlite3.connect('first_database.db')
            cursor = banco.cursor()
            cursor.execute('SELECT * FROM clientes')
            nomes = cursor.fetchall()
            if not id or not id.isdigit():
                sg.popup('Informe o [ID DO CLIENTE] que deseja alterar o NOME.', font='Arial 10 bold', title='Erro!')

            if id.isdigit():
                for nome in nomes:
                    if nome[0] == int(id):
                        window['id'].update(nome[0])
                        window['nome'].update(nome[1])
                        break
                else:
                    sg.popup('Informe o [ID DO CLIENTE] existente.', font='Arial 10 bold', title='Erro!')

        elif events == 'SOBRENOME':
            banco = sqlite3.connect('first_database.db')
            cursor = banco.cursor()
            cursor.execute('SELECT * FROM clientes')
            sobrenomes = cursor.fetchall()
            if not id or not id.isdigit():
                sg.popup('Informe o [ID DO CLIENTE] que deseja alterar o SOBRENOME.', font='Arial 10 bold', title='Erro!')

            if id.isdigit():
                for sobrenome in sobrenomes:
                    if sobrenome[0] == int(id):
                        window['id'].update(sobrenome[0])
                        window['sobrenome'].update(sobrenome[2])
                        break
                else:
                    sg.popup('Informe o [ID DO CLIENTE] existente.', font='Arial 10 bold', title='Erro!')
    
        elif events == 'CONTATO':
            banco = sqlite3.connect('first_database.db')
            cursor = banco.cursor()
            cursor.execute('SELECT * FROM clientes')
            contatos = cursor.fetchall()
            if not id or not id.isdigit():
                sg.popup('Informe o [ID DO CLIENTE] que deseja alterar o CONTATO.', font='Arial 10 bold', title='Erro!')

            if id.isdigit():
                for contato in contatos:
                    if contato[0] == int(id):
                        window['id'].update(contato[0])
                        window['ddd'].update(contato[3])
                        window['numero'].update(contato[4])
                        break
                else:
                    sg.popup('Informe o [ID DO CLIENTE] existente.', font='Arial 10 bold', title='Erro!')

        elif events == 'ENDEREÇO':
            banco = sqlite3.connect('first_database.db')
            cursor = banco.cursor()
            cursor.execute('SELECT * FROM clientes')
            enderecos = cursor.fetchall()
            if not id or not id.isdigit():
                sg.popup('Informe o [ID DO CLIENTE] que deseja alterar o ENDEREÇO.', font='Arial 10 bold', title='Erro!')
            
            if id.isdigit():
                for endereco in enderecos:
                    if endereco[0] == int(id):
                        window['id'].update(endereco[0])
                        window['endereco'].update(endereco[5])
                        window['nres'].update(endereco[6])
                        window['complemento'].update(endereco[7])
                        break
                else:
                    sg.popup('Informe o [ID DO CLIENTE] existente.', font='Arial 10 bold', title='Erro!')

        elif events == 'ALTERAR DADOS':
            banco = sqlite3.connect('first_database.db')
            cursor = banco.cursor()
            try:
                if not id or id.isspace() or id.isalpha() or not id.isdigit():
                    sg.popup('DIGITE O ID REFERENTE AO CLIENTE QUE DESEJA ALTERAR DADOS', font='Arial 10 bold', title='ERRO!')
                    
                elif values['id'].isdigit():
                    cursor.execute("SELECT Id FROM clientes WHERE Id= '"+id+"'")
                    ids = cursor.fetchall()
                    for i in ids:
                        if i[0] == int(id):

                            if nome.isalpha() and not nome == None and id.isdigit():
                                cursor.execute("UPDATE clientes SET Nome = '"+nome+"' WHERE Id = '"+id+"'")
                                banco.commit()
                                window['saida'].update('')
                                get_clientes()

                            if sobrenome.isalpha() and not sobrenome == None and id.isdigit():
                                cursor.execute("UPDATE clientes SET Sobrenome = '"+sobrenome+"' WHERE Id = '"+id+"'")
                                banco.commit()
                                window['saida'].update('')
                                get_clientes()

                            if ddd.isdigit() and not ddd == None and id.isdigit():
                                cursor.execute("UPDATE clientes SET DDD = '"+ddd+"'  WHERE Id = '"+id+"'")
                                banco.commit()
                                window['saida'].update('')
                                get_clientes()

                            if numero.isdigit() and not numero == None and id.isdigit():
                                cursor.execute("UPDATE clientes SET Contato = '"+numero+"' WHERE Id = '"+id+"'")
                                banco.commit()
                                window['saida'].update('')
                                get_clientes()

                            if end.isalpha() and not end == None and id.isdigit():
                                cursor.execute("UPDATE clientes SET Endereço = '"+end+"' WHERE Id = '"+id+"'")
                                banco.commit()
                                window['saida'].update('')
                                get_clientes()

                            if nres.isdigit() and not nres == None and id.isdigit():
                                cursor.execute("UPDATE clientes SET Numero = '"+nres+"' WHERE Id = '"+id+"'")
                                banco.commit()
                                window['saida'].update('')
                                get_clientes()

                            if complemento and id.isdigit():
                                cursor.execute("UPDATE clientes SET Complemento = '"+complemento+"' WHERE Id = '"+id+"'")
                                banco.commit()
                                window['saida'].update('')
                                get_clientes()
                        break
                    else:
                        sg.popup(f"ESSE ID: [{values['id']}] NÃO FOI LOCALIZADO!", font='Arial 10 bold', title='ERRO!')
            except:
                sg.popup('SE ALGO NÃO TIVER ALTERADO, VERIFIQUE SE DIGITOU CORRETAMENTE.', font='Arial 10 bold', title='ERRO!')

        elif events == 'ENVIAR WhatsApp':
            sg.popup('LEMBRE-SE!\n\nNúmero: Símbolo: (+)+(DDI)+(DDD - sem o [0])+(Contato)\n\nExemplo: +5585123456789',
             font='Arial 14 bold', title='IMPORTANTE!')
            
            def criar_janela_numero():
                sg.theme('DarkBlue13')
                linha = [
                    [sg.Text('Insira o Número:', font='Arial 11 bold'), sg.Input(key='wanumero', font='Century 11 bold')],
                    [sg.Output(background_color='black', text_color='white', size=(65, 8), font= 'Century 9 bold', key='numsaida')],
                ]

                layout = [
                    [sg.Frame(' ADICIONE O(S) NÚMERO(S) ', layout= linha, key='container')],
                    [sg.Button('ADICIONAR', font='Arial 10 bold'), sg.Button('CONCLUIDO', font='Arial 10 bold')]
                ]
                return sg.Window('NÚMERO(S) WHATSAPP', layout= layout, finalize=True)
        
            janelanum = criar_janela_numero()

            while True:
                window, events, values = sg.read_all_windows()
                wanumero = values['wanumero']

                if events == sg.WINDOW_CLOSED:
                    janelanum.close()
                    break

                elif events == 'ADICIONAR':
                    if not wanumero or not len(wanumero) == 14 or wanumero.isspace() or wanumero.isalpha():
                        sg.popup('ERRO AO ADICIONAR NÚMERO', font='Arial 10 bold', title='ERROR!')

                    elif len(wanumero) == 14:
                        contatos.append(wanumero)
                        window['wanumero'].update('')
                        window['numsaida'].update('')
                        for contato in contatos:
                            print(contato)
                            print('*' * 74)
                
                elif events == 'CONCLUIDO':
                    if len(contatos) == 0:
                        sg.popup('INSIRA PRIMEIRO UM NÚMERO PARA ENVIAR A MENSAGEM!', font='Arial 10 bold', title='ERRO!')
                    else:
                        sg.popup('DIGITE AGORA SUA MENSAGEM!', font='Arial 10 bold', title='INFO!')

                        def criar_janela_wa():

                        # Layout
                            sg.theme('DarkBlue13')
                            colwa1 = [
                                [sg.Text('Estas são as instruções que devem ser levadas em consideração:\n', font='Century 13 bold')],
                                [sg.Text('Formato que deve ser inserido: DDI+DDD+NÚMERO', font='Century 12 bold')],
                                [sg.Text('EXEMPLO:\n\n+5585123456789\n\n', font='Arial 14 bold', pad=(100,10))],
                                [sg.Text('Mensagem:', font='Arial 11 bold'), sg.Text(' ' * 5), sg.Input(key='wamensagem', font='Century 11 bold', size=(45, 5))]
                            ]
                            
                            colwa2 = [
                                [sg.Output(background_color='black', font='Arial 12 bold', text_color='white', size=(60, 20), key='saidawa')]
                            ]
                            

                            layout = [
                                [sg.Text('ENVIE SUAS MENSAGENS POR AQUI:', font='Arial 15 bold', pad=(90,5)), sg.Text('CLIENTES CADASTRADOS:', font='Arial 15 bold', pad=(160,5))],
                                [sg.Column(colwa1, pad=(0,0, (0,0))), sg.Column(colwa2, pad=(0,0, (0,0)))],
                                [sg.Button('ENVIAR MENSAGEM', font='Arial 10 bold', size=(20,3), button_color='Green', pad=(200,15)),
                                sg.Button('MOSTRAR TODOS', font='Arial 10 bold', size=(20,3), button_color='Black', pad=(210,15))]
                            ]
                            # Janela
                            return sg.Window("MENSAGEM(NS) DO WHATSAPP", layout= layout, finalize=True)

                        # Extrair os dados da tela
                        janelawa = criar_janela_wa()
                        
                        while True:
                            window, events, values = sg.read_all_windows()
                            
                            if events == sg.WINDOW_CLOSED:
                                janelawa.close()
                                break

                            if events == 'MOSTRAR TODOS':
                                window['saidawa'].update('')
                                banco = sqlite3.connect('first_database.db')
                                cursor = banco.cursor()
                                cursor.execute('SELECT * FROM clientes')
                                clientes = cursor.fetchall()
                                print('*' * 90)
                                print('NOMES DOS CLIENTES:')
                                print('*' * 90)
                                for cliente in clientes:
                                    print('ID: ', cliente[0])
                                    print('Nome: ', cliente[1], cliente[2])
                                    print('Contato: ', cliente[3], cliente[4])
                                    print('Endereço ', cliente[5], cliente[6], cliente[7], '\n')
                                    print('*' * 90)

                            if events == 'ENVIAR MENSAGEM':
                                sg.popup('CERTIFIQUE-SE QUE SEU WHATSAPP ESTEJA CONECTADO NA WEB E QUE SEU NAVEGADOR ESTEJA ABERTO E AGUARDE A CONCLUSÃO!',
                                font='Century 12 bold', title='LEMBRE-SE!')
                                wamensagem = values['wamensagem']
                                
                                if len(wamensagem) >= 2 and not values['wamensagem'].isspace():
                                    sg.popup('O WHATSAPP WEB SERÁ ABERTO EM + OU - 2 MINUTOS E SUA MENSAGEM SERÁ ENVIADA EM 15 SEGUNDOS APÓS A ABERTURA. AGUARDE!',
                                    font='Century 12 bold', title='AVISO!')
                                    window['wamensagem'].update('')
                                    keyboard.press_and_release('windows + d')

                                    # 3. Definir intervalo de envio.
                                    while len(contatos) >= 1:
                                        # Enviar mensagens
                                        pywhatkit.sendwhatmsg(contatos[0], wamensagem, datetime.now().hour, datetime.now().minute + 2, wait_time = 25)
                                        del contatos[0]
                                        time.sleep(30)
                                        keyboard.press_and_release('ctrl + w')
                                    else:
                                        sg.popup('MENSAGEM(NS) ENVIADA(S) COM SUCESSO', font='Arial 10 bold', title='INFORMATIVO')
                                else:
                                    sg.popup('HÁ ALGUM CONTEÚDO NO CAMPO DE MENSAGEM?! NÃO IDENTIFIQUEI!', font='Arial 10 bold', title='ERRO!')
