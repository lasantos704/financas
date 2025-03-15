import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
import os

class FinancasPessoais:
    def __init__(self, arquivo_excel='financas.xlsx'):
        self.arquivo_excel = arquivo_excel
        self.saldo = 0.0
        self.recebimentos = []
        self.gastos = defaultdict(list)
        self.financiamentos = []
        self.cartoes = []  # Lista de cartões de crédito
        self.faturas = []  # Faturas dos cartões
        self.parcelas = []  # Parcelas de gastos no crédito
        self.categorias = set()
        self.investimentos = []  # Lista de investimentos

        # Verifica se o arquivo Excel já existe
        if os.path.exists(self.arquivo_excel):
            self.carregar_dados()
        else:
            self.criar_arquivo_inicial()

        # Cria a pasta de relatórios se não existir
        if not os.path.exists("relatorios"):
            os.makedirs("relatorios")

    def criar_arquivo_inicial(self):
        print("\n--- Bem-vindo ao Sistema de Finanças Pessoais ---")
        print("Arquivo Excel não encontrado. Criando novo arquivo...")

        # Solicitar saldo inicial
        self.saldo = self.solicitar_valor("Digite seu saldo inicial: R$ ")

        # Solicitar cadastro de cartões de crédito
        print("\nVamos cadastrar seus cartões de crédito.")
        while True:
            nome_cartao = input("Nome do cartão (ou 'sair' para encerrar): ")
            if nome_cartao.lower() == 'sair':
                break
            limite = self.solicitar_valor(f"Limite do cartão '{nome_cartao}': R$ ")
            dia_vencimento = int(input(f"Dia de vencimento da fatura do cartão '{nome_cartao}': "))

            # Cadastrar fatura atual do cartão
            print(f"\nCadastrar fatura atual do cartão '{nome_cartao}':")
            fatura_atual = self.solicitar_valor(f"Valor da fatura atual do cartão '{nome_cartao}': R$ ")
            self.faturas.append({'cartao': nome_cartao, 'valor': fatura_atual, 'pago': False})

            # Cadastrar parcelas futuras do cartão
            print(f"\nCadastrar parcelas futuras do cartão '{nome_cartao}':")
            while True:
                descricao_parcela = input("Descrição da parcela (ou 'sair' para encerrar): ")
                if descricao_parcela.lower() == 'sair':
                    break
                valor_parcela = self.solicitar_valor(f"Valor da parcela '{descricao_parcela}': R$ ")
                parcelas_total = int(input(f"Número total de parcelas: "))
                parcelas_restantes = int(input(f"Número de parcelas restantes: "))
                self.parcelas.append({
                    'cartao': nome_cartao,
                    'valor': valor_parcela,
                    'descricao': descricao_parcela,
                    'parcela_atual': parcelas_total - parcelas_restantes + 1,
                    'parcelas_total': parcelas_total,
                    'pago': False
                })

            self.cadastrar_cartao(nome_cartao, limite, dia_vencimento)

        # Salvar dados iniciais
        self.salvar_dados()
        print(f"Arquivo {self.arquivo_excel} criado com sucesso!")

    def solicitar_valor(self, mensagem):
        while True:
            try:
                valor = input(mensagem).replace(',', '.')  # Substitui vírgula por ponto
                return float(valor)
            except ValueError:
                print("Valor inválido. Use números com ponto (.) ou vírgula (,) como separador decimal.")

    def carregar_dados(self):
        try:
            # Carregar recebimentos
            df_recebimentos = pd.read_excel(self.arquivo_excel, sheet_name='Recebimentos')
            self.recebimentos = df_recebimentos.to_dict('records')

            # Carregar gastos
            df_gastos = pd.read_excel(self.arquivo_excel, sheet_name='Gastos')
            for _, row in df_gastos.iterrows():
                self.gastos[row['Categoria']].append({
                    'valor': row['Valor'],
                    'descricao': row['Descricao'],
                    'tipo': row['Tipo'],
                    'cartao': row['Cartao'],
                    'parcelado': row['Parcelado'],
                    'parcelas_total': row['ParcelasTotal'],
                    'parcelas_restantes': row['ParcelasRestantes']
                })
                self.categorias.add(row['Categoria'])

            # Carregar financiamentos
            df_financiamentos = pd.read_excel(self.arquivo_excel, sheet_name='Financiamentos')
            self.financiamentos = df_financiamentos.to_dict('records')

            # Carregar cartões de crédito
            df_cartoes = pd.read_excel(self.arquivo_excel, sheet_name='Cartoes')
            self.cartoes = df_cartoes.to_dict('records')

            # Carregar faturas
            df_faturas = pd.read_excel(self.arquivo_excel, sheet_name='Faturas')
            self.faturas = df_faturas.to_dict('records')

            # Carregar parcelas
            df_parcelas = pd.read_excel(self.arquivo_excel, sheet_name='Parcelas')
            self.parcelas = df_parcelas.to_dict('records')

            # Carregar investimentos
            df_investimentos = pd.read_excel(self.arquivo_excel, sheet_name='Investimentos')
            self.investimentos = df_investimentos.to_dict('records')

            # Atualizar saldo
            self.saldo = sum(recebimento['valor'] for recebimento in self.recebimentos)
            self.saldo -= sum(sum(gasto['valor'] for gasto in gastos) for gastos in self.gastos.values())
            self.saldo -= sum((fin['valor_total'] / fin['parcelas']) * fin['parcelas_pagas'] for fin in self.financiamentos)

        except Exception as e:
            print(f"Erro ao carregar dados do Excel: {e}")

    def salvar_dados(self):
        try:
            # Salvar recebimentos
            df_recebimentos = pd.DataFrame(self.recebimentos)

            # Salvar gastos
            df_gastos = pd.DataFrame([{
                'Categoria': cat,
                'Valor': gasto['valor'],
                'Descricao': gasto['descricao'],
                'Tipo': gasto['tipo'],
                'Cartao': gasto['cartao'],
                'Parcelado': gasto.get('parcelado', False),
                'ParcelasTotal': gasto.get('parcelas_total', 1),
                'ParcelasRestantes': gasto.get('parcelas_restantes', 1)
            } for cat, gastos in self.gastos.items() for gasto in gastos])

            # Salvar financiamentos
            df_financiamentos = pd.DataFrame(self.financiamentos)

            # Salvar cartões de crédito
            df_cartoes = pd.DataFrame(self.cartoes)

            # Salvar faturas
            df_faturas = pd.DataFrame(self.faturas)

            # Salvar parcelas
            df_parcelas = pd.DataFrame(self.parcelas)

            # Salvar investimentos
            df_investimentos = pd.DataFrame(self.investimentos)

            with pd.ExcelWriter(self.arquivo_excel) as writer:
                df_recebimentos.to_excel(writer, sheet_name='Recebimentos', index=False)
                df_gastos.to_excel(writer, sheet_name='Gastos', index=False)
                df_financiamentos.to_excel(writer, sheet_name='Financiamentos', index=False)
                df_cartoes.to_excel(writer, sheet_name='Cartoes', index=False)
                df_faturas.to_excel(writer, sheet_name='Faturas', index=False)
                df_parcelas.to_excel(writer, sheet_name='Parcelas', index=False)
                df_investimentos.to_excel(writer, sheet_name='Investimentos', index=False)

            print(f"\nDados salvos em {self.arquivo_excel}")
        except Exception as e:
            print(f"Erro ao salvar dados no Excel: {e}")

    def adicionar_recebimento(self, valor, dia, descricao):
        self.saldo += valor
        self.recebimentos.append({'valor': valor, 'dia': dia, 'descricao': descricao})
        self.salvar_dados()

    def adicionar_gasto(self, valor, categoria, descricao, tipo='débito', cartao=None, parcelado=False, parcelas=1):
        if tipo == 'crédito' and cartao is None:
            print("Para gastos no crédito, é necessário informar o cartão.")
            return

        if tipo == 'crédito':
            cartao_encontrado = next((c for c in self.cartoes if c['nome'] == cartao), None)
            if not cartao_encontrado:
                print(f"Cartão '{cartao}' não encontrado.")
                return
            if cartao_encontrado['limite'] < valor:
                print(f"Limite insuficiente no cartão '{cartao}'.")
                return
            cartao_encontrado['limite'] -= valor

            if parcelado:
                valor_parcela = valor / parcelas
                for i in range(parcelas):
                    self.parcelas.append({
                        'cartao': cartao,
                        'valor': valor_parcela,
                        'descricao': descricao,
                        'parcela_atual': i + 1,
                        'parcelas_total': parcelas,
                        'pago': False
                    })
            else:
                self.faturas.append({'cartao': cartao, 'valor': valor, 'pago': False})

        elif valor > self.saldo:
            print("Saldo insuficiente!")
            return

        self.saldo -= valor if tipo == 'débito' else 0
        self.gastos[categoria].append({
            'valor': valor,
            'descricao': descricao,
            'tipo': tipo,
            'cartao': cartao,
            'parcelado': parcelado,
            'parcelas_total': parcelas,
            'parcelas_restantes': parcelas
        })
        self.categorias.add(categoria)
        self.salvar_dados()

    def adicionar_financiamento(self, valor_total, parcelas, descricao):
        if any(fin['descricao'] == descricao for fin in self.financiamentos):
            print(f"Já existe um financiamento cadastrado com a descrição '{descricao}'.")
            return
        self.financiamentos.append({
            'valor_total': valor_total,
            'parcelas': parcelas,
            'parcelas_pagas': 0,
            'descricao': descricao
        })
        self.salvar_dados()

    def pagar_parcela_financiamento(self, descricao):
        for financiamento in self.financiamentos:
            if financiamento['descricao'] == descricao:
                if financiamento['parcelas_pagas'] < financiamento['parcelas']:
                    print(f"\n--- Pagar Parcelas do Financiamento: {financiamento['descricao']} ---")
                    parcelas_pendentes = financiamento['parcelas'] - financiamento['parcelas_pagas']
                    valor_parcela = financiamento['valor_total'] / financiamento['parcelas']
                    print(f"Valor da parcela: R$ {valor_parcela:.2f}")
                    print(f"Parcelas pendentes: {parcelas_pendentes}")

                    # Selecionar parcelas a pagar
                    parcelas_a_pagar = input("Digite os números das parcelas a pagar (separados por vírgula): ")
                    parcelas_a_pagar = [int(p.strip()) for p in parcelas_a_pagar.split(',') if p.strip().isdigit()]

                    if not parcelas_a_pagar:
                        print("Nenhuma parcela selecionada.")
                        return

                    # Verificar se as parcelas selecionadas são válidas
                    for parcela_num in parcelas_a_pagar:
                        if parcela_num < 1 or parcela_num > financiamento['parcelas']:
                            print(f"Parcela {parcela_num} inválida.")
                            return

                    # Calcular valor total das parcelas selecionadas
                    valor_total = valor_parcela * len(parcelas_a_pagar)
                    print(f"Valor total das parcelas selecionadas: R$ {valor_total:.2f}")

                    # Verificar desconto
                    desconto = input("Há desconto para pagamento antecipado? (s/n): ").lower()
                    if desconto == 's':
                        valor_total = self.solicitar_valor("Digite o valor total com desconto: R$ ")

                    if valor_total > self.saldo:
                        print("Saldo insuficiente para pagar as parcelas selecionadas.")
                        return

                    # Pagar as parcelas selecionadas
                    self.saldo -= valor_total
                    financiamento['parcelas_pagas'] += len(parcelas_a_pagar)
                    print(f"Parcelas {', '.join(map(str, parcelas_a_pagar))} pagas com sucesso!")
                    self.salvar_dados()
                else:
                    print("Todas as parcelas já foram pagas!")
                return
        print("Financiamento não encontrado!")

    def cadastrar_cartao(self, nome, limite, dia_vencimento):
        if any(c['nome'] == nome for c in self.cartoes):
            print(f"Já existe um cartão cadastrado com o nome '{nome}'.")
            return
        self.cartoes.append({'nome': nome, 'limite': limite, 'dia_vencimento': dia_vencimento})
        self.salvar_dados()

    def pagar_fatura(self, cartao):
        fatura = sum(f['valor'] for f in self.faturas if f['cartao'] == cartao and not f['pago'])
        if fatura == 0:
            print(f"Não há fatura pendente para o cartão '{cartao}'.")
            return

        if fatura > self.saldo:
            print("Saldo insuficiente para pagar a fatura!")
            return

        self.saldo -= fatura
        for f in self.faturas:
            if f['cartao'] == cartao and not f['pago']:
                f['pago'] = True
        print(f"Fatura do cartão '{cartao}' paga com sucesso!")
        self.salvar_dados()

    def pagar_parcela_antecipada(self):
        print("\n--- Pagar Parcelas Antecipadas ---")
        for i, parcela in enumerate(self.parcelas):
            if not parcela['pago']:
                print(f"{i + 1}. {parcela['descricao']} (Parcela {parcela['parcela_atual']}/{parcela['parcelas_total']}): R$ {parcela['valor']:.2f}")

        try:
            escolha = input("Digite os números das parcelas a pagar (separados por vírgula): ")
            escolha = [int(p.strip()) for p in escolha.split(',') if p.strip().isdigit()]

            if not escolha:
                print("Nenhuma parcela selecionada.")
                return

            # Verificar se as parcelas selecionadas são válidas
            for parcela_num in escolha:
                if parcela_num < 1 or parcela_num > len(self.parcelas):
                    print(f"Parcela {parcela_num} inválida.")
                    return

            # Calcular valor total das parcelas selecionadas
            valor_total = sum(self.parcelas[p - 1]['valor'] for p in escolha)
            print(f"Valor total das parcelas selecionadas: R$ {valor_total:.2f}")

            # Verificar desconto
            desconto = input("Há desconto para pagamento antecipado? (s/n): ").lower()
            if desconto == 's':
                valor_total = self.solicitar_valor("Digite o valor total com desconto: R$ ")

            if valor_total > self.saldo:
                print("Saldo insuficiente para pagar as parcelas selecionadas.")
                return

            # Pagar as parcelas selecionadas
            self.saldo -= valor_total
            for p in escolha:
                self.parcelas[p - 1]['pago'] = True
            print(f"Parcelas {', '.join(map(str, escolha))} pagas com sucesso!")
            self.salvar_dados()
        except (ValueError, IndexError):
            print("Opção inválida.")

    def gerar_relatorio_txt(self, relatorio, nome_arquivo):
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(relatorio)
        print(f"Relatório salvo em {nome_arquivo}")

    def estatisticas_mes(self):
        relatorio = "\n--- Estatísticas do Mês ---\n"
        relatorio += f"Saldo Atual: R$ {self.saldo:.2f}\n"

        total_gastos = sum(sum(gasto['valor'] for gasto in gastos) for gastos in self.gastos.values())
        relatorio += f"Total de Gastos: R$ {total_gastos:.2f}\n"

        relatorio += "\nGastos por Categoria:\n"
        for categoria, gastos in self.gastos.items():
            total_categoria = sum(gasto['valor'] for gasto in gastos)
            relatorio += f"{categoria}: R$ {total_categoria:.2f}\n"

        relatorio += "\nFinanciamentos:\n"
        for financiamento in self.financiamentos:
            relatorio += f"{financiamento['descricao']}: {financiamento['parcelas_pagas']}/{financiamento['parcelas']} parcelas pagas\n"

        relatorio += "\nFaturas Pendentes:\n"
        for cartao in self.cartoes:
            fatura = sum(f['valor'] for f in self.faturas if f['cartao'] == cartao['nome'] and not f['pago'])
            relatorio += f"{cartao['nome']}: R$ {fatura:.2f}\n"

        relatorio += "\nParcelas Pendentes:\n"
        for parcela in self.parcelas:
            if not parcela['pago']:
                relatorio += f"{parcela['descricao']} (Parcela {parcela['parcela_atual']}/{parcela['parcelas_total']}): R$ {parcela['valor']:.2f}\n"

        nome_arquivo = f"relatorios/estatisticas_mes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.gerar_relatorio_txt(relatorio, nome_arquivo)

    def relatorio_completo(self):
        relatorio = "\n--- Relatório Completo ---\n"
        relatorio += f"Saldo Atual: R$ {self.saldo:.2f}\n"

        relatorio += "\nRecebimentos:\n"
        for recebimento in self.recebimentos:
            relatorio += f"Dia {recebimento['dia']}: R$ {recebimento['valor']:.2f} - {recebimento['descricao']}\n"

        relatorio += "\nGastos por Categoria:\n"
        for categoria, gastos in self.gastos.items():
            relatorio += f"\n{categoria}:\n"
            for gasto in gastos:
                relatorio += f"  {gasto['descricao']}: R$ {gasto['valor']:.2f} ({gasto['tipo']})\n"

        relatorio += "\nFinanciamentos:\n"
        for financiamento in self.financiamentos:
            relatorio += f"{financiamento['descricao']}: {financiamento['parcelas_pagas']}/{financiamento['parcelas']} parcelas pagas\n"

        relatorio += "\nCartões de Crédito:\n"
        for cartao in self.cartoes:
            relatorio += f"{cartao['nome']}: Limite R$ {cartao['limite']:.2f}, Vencimento dia {cartao['dia_vencimento']}\n"

        relatorio += "\nFaturas Pendentes:\n"
        for cartao in self.cartoes:
            fatura = sum(f['valor'] for f in self.faturas if f['cartao'] == cartao['nome'] and not f['pago'])
            relatorio += f"{cartao['nome']}: R$ {fatura:.2f}\n"

        relatorio += "\nParcelas Pendentes:\n"
        for parcela in self.parcelas:
            if not parcela['pago']:
                relatorio += f"{parcela['descricao']} (Parcela {parcela['parcela_atual']}/{parcela['parcelas_total']}): R$ {parcela['valor']:.2f}\n"

        nome_arquivo = f"relatorios/relatorio_completo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.gerar_relatorio_txt(relatorio, nome_arquivo)

    def relatorio_mensal(self, mes, ano):
        relatorio = f"\n--- Relatório Mensal: {mes}/{ano} ---\n"
        recebimentos_mes = [r for r in self.recebimentos if datetime.strptime(str(r['dia']), '%d').month == mes and datetime.strptime(str(r['dia']), '%d').year == ano]
        gastos_mes = [g for gastos in self.gastos.values() for g in gastos if datetime.strptime(str(g['dia']), '%d').month == mes and datetime.strptime(str(g['dia']), '%d').year == ano]

        total_recebimentos = sum(r['valor'] for r in recebimentos_mes)
        total_gastos = sum(g['valor'] for g in gastos_mes)

        relatorio += f"Total de Recebimentos: R$ {total_recebimentos:.2f}\n"
        relatorio += f"Total de Gastos: R$ {total_gastos:.2f}\n"
        relatorio += f"Saldo do Mês: R$ {total_recebimentos - total_gastos:.2f}\n"

        nome_arquivo = f"relatorios/relatorio_mensal_{mes}_{ano}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.gerar_relatorio_txt(relatorio, nome_arquivo)

    def relatorio_anual(self, ano):
        relatorio = f"\n--- Relatório Anual: {ano} ---\n"
        for mes in range(1, 13):
            recebimentos_mes = [r for r in self.recebimentos if datetime.strptime(str(r['dia']), '%d').month == mes and datetime.strptime(str(r['dia']), '%d').year == ano]
            gastos_mes = [g for gastos in self.gastos.values() for g in gastos if datetime.strptime(str(g['dia']), '%d').month == mes and datetime.strptime(str(g['dia']), '%d').year == ano]

            total_recebimentos = sum(r['valor'] for r in recebimentos_mes)
            total_gastos = sum(g['valor'] for g in gastos_mes)

            relatorio += f"\n--- Mês {mes} ---\n"
            relatorio += f"Total de Recebimentos: R$ {total_recebimentos:.2f}\n"
            relatorio += f"Total de Gastos: R$ {total_gastos:.2f}\n"
            relatorio += f"Saldo do Mês: R$ {total_recebimentos - total_gastos:.2f}\n"

        nome_arquivo = f"relatorios/relatorio_anual_{ano}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.gerar_relatorio_txt(relatorio, nome_arquivo)

    def adicionar_categoria(self, categoria):
        if categoria in self.categorias:
            print(f"A categoria '{categoria}' já existe.")
        else:
            self.categorias.add(categoria)
            print(f"Categoria '{categoria}' adicionada com sucesso!")
            self.salvar_dados()

    def adicionar_investimento(self, valor, produto, banco, rendimento_mensal):
        investimento_existente = next((inv for inv in self.investimentos if inv['produto'] == produto and inv['banco'] == banco), None)
        if investimento_existente:
            print(f"Investimento no produto '{produto}' do banco '{banco}' já existe.")
            opcao = input("Deseja adicionar um valor a este investimento? (s/n): ").lower()
            if opcao == 's':
                investimento_existente['valor'] += valor
                print(f"Valor adicionado ao investimento existente. Novo valor: R$ {investimento_existente['valor']:.2f}")
            else:
                print("Nenhum valor adicionado.")
        else:
            self.investimentos.append({
                'valor': valor,
                'produto': produto,
                'banco': banco,
                'rendimento_mensal': rendimento_mensal
            })
            print(f"Novo investimento cadastrado: {produto} no banco {banco}.")
        self.salvar_dados()

    def adicionar_rendimento_investimento(self, produto, banco, rendimento):
        investimento = next((inv for inv in self.investimentos if inv['produto'] == produto and inv['banco'] == banco), None)
        if investimento:
            investimento['valor'] += rendimento
            print(f"Rendimento de R$ {rendimento:.2f} adicionado ao investimento {produto} no banco {banco}.")
            self.salvar_dados()
        else:
            print(f"Investimento no produto '{produto}' do banco '{banco}' não encontrado.")

# Função para exibir o menu
def exibir_menu():
    print("\n--- Menu de Finanças Pessoais ---")
    print("1. Adicionar Recebimento")
    print("2. Adicionar Gasto")
    print("3. Adicionar Financiamento")
    print("4. Pagar Parcela de Financiamento")
    print("5. Cadastrar Cartão de Crédito")
    print("6. Pagar Fatura do Cartão")
    print("7. Pagar Parcela Antecipada")
    print("8. Ver Estatísticas do Mês")
    print("9. Ver Relatório Completo")
    print("10. Adicionar Categoria")
    print("11. Gerar Relatório Mensal")
    print("12. Gerar Relatório Anual")
    print("13. Adicionar Investimento")
    print("14. Adicionar Rendimento de Investimento")
    print("15. Sair")
    return input("Escolha uma opção: ")

# Exemplo de uso
financas = FinancasPessoais()

while True:
    opcao = exibir_menu()

    if opcao == '1':
        valor = financas.solicitar_valor("Valor recebido: R$ ")
        dia = int(input("Dia do recebimento (1-31): "))
        descricao = input("Descrição do recebimento: ")
        financas.adicionar_recebimento(valor, dia, descricao)

    elif opcao == '2':
        valor = financas.solicitar_valor("Valor gasto: R$ ")
        categoria = input("Categoria do gasto: ")
        descricao = input("Descrição do gasto: ")
        tipo = input("Tipo (débito/crédito): ").lower()
        cartao = None
        parcelado = False
        parcelas = 1
        if tipo == 'crédito':
            cartao = input("Nome do cartão: ")
            parcelado = input("Parcelado? (s/n): ").lower() == 's'
            if parcelado:
                parcelas = int(input("Número de parcelas: "))
        financas.adicionar_gasto(valor, categoria, descricao, tipo, cartao, parcelado, parcelas)

    elif opcao == '3':
        valor_total = financas.solicitar_valor("Valor total do financiamento: R$ ")
        parcelas = int(input("Número de parcelas: "))
        descricao = input("Descrição do financiamento: ")
        financas.adicionar_financiamento(valor_total, parcelas, descricao)

    elif opcao == '4':
        descricao = input("Descrição do financiamento: ")
        financas.pagar_parcela_financiamento(descricao)

    elif opcao == '5':
        nome = input("Nome do cartão: ")
        limite = financas.solicitar_valor("Limite do cartão: R$ ")
        dia_vencimento = int(input("Dia de vencimento da fatura: "))
        financas.cadastrar_cartao(nome, limite, dia_vencimento)

    elif opcao == '6':
        cartao = input("Nome do cartão: ")
        financas.pagar_fatura(cartao)

    elif opcao == '7':
        financas.pagar_parcela_antecipada()

    elif opcao == '8':
        financas.estatisticas_mes()

    elif opcao == '9':
        financas.relatorio_completo()

    elif opcao == '10':
        categoria = input("Nome da nova categoria: ")
        financas.adicionar_categoria(categoria)

    elif opcao == '11':
        mes = int(input("Mês (1-12): "))
        ano = int(input("Ano: "))
        financas.relatorio_mensal(mes, ano)

    elif opcao == '12':
        ano = int(input("Ano: "))
        financas.relatorio_anual(ano)

    elif opcao == '13':
        valor = financas.solicitar_valor("Valor do investimento: R$ ")
        produto = input("Produto do investimento: ")
        banco = input("Banco: ")
        rendimento_mensal = financas.solicitar_valor("Rendimento mensal (%): ")
        financas.adicionar_investimento(valor, produto, banco, rendimento_mensal)

    elif opcao == '14':
        produto = input("Produto do investimento: ")
        banco = input("Banco: ")
        rendimento = financas.solicitar_valor("Valor do rendimento: R$ ")
        financas.adicionar_rendimento_investimento(produto, banco, rendimento)

    elif opcao == '15':
        print("Saindo do sistema...")
        break

    else:
        print("Opção inválida. Tente novamente.")
