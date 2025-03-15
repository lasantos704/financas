# Sistema de Finanças Pessoais

O **Sistema de Finanças Pessoais** é um programa em Python que ajuda você a gerenciar suas finanças de forma eficiente. Ele permite registrar recebimentos, gastos, financiamentos, cartões de crédito e investimentos, além de fornecer estatísticas mensais, relatórios completos e análises de investimentos. O programa salva os dados em um arquivo Excel para persistência e gera relatórios em arquivos `.txt` para fácil consulta.

---

## Funcionalidades

- **Recebimentos**: Registre valores recebidos, o dia do mês e uma descrição.
- **Gastos**: Registre gastos por categoria, com opção de pagamento no débito ou crédito.
- **Financiamentos**: Cadastre financiamentos e pague parcelas, com suporte para descontos em pagamentos antecipados.
- **Cartões de Crédito**: Cadastre cartões de crédito, gerencie faturas e parcelas futuras.
- **Investimentos**: Cadastre investimentos, adicione valores e registre rendimentos mensais.
- **Estatísticas Mensais**: Visualize o saldo atual, gastos por categoria, parcelas pendentes e faturas.
- **Relatórios Completo, Mensal e Anual**: Gere relatórios detalhados de todas as transações, parcelas e investimentos.
- **Categorias Personalizadas**: Adicione novas categorias de gastos dinamicamente.
- **Geração de Relatórios em TXT**: Salve relatórios em arquivos `.txt` para consulta posterior.

---

## Requisitos

- Python 3.x
- Bibliotecas necessárias: `pandas`, `openpyxl`

---

## Instalação

1. Clone este repositório ou faça o download do código-fonte.
2. Instale as dependências necessárias:

   ```bash
   pip install pandas openpyxl
   ```

3. Execute o programa:

   ```bash
   python financas_pessoais.py
   ```

---

## Como Usar

### Menu Principal

Ao iniciar o programa, você verá o seguinte menu:

```
--- Menu de Finanças Pessoais ---
1. Adicionar Recebimento
2. Adicionar Gasto
3. Adicionar Financiamento
4. Pagar Parcela de Financiamento
5. Cadastrar Cartão de Crédito
6. Pagar Fatura do Cartão
7. Pagar Parcela Antecipada
8. Ver Estatísticas do Mês
9. Ver Relatório Completo
10. Adicionar Categoria
11. Gerar Relatório Mensal
12. Gerar Relatório Anual
13. Adicionar Investimento
14. Adicionar Rendimento de Investimento
15. Sair
```

### Exemplos de Uso

1. **Adicionar Recebimento**:
   - Digite o valor recebido, o dia do mês e a descrição.
   - Exemplo: `Valor recebido: R$ 5000`, `Dia do recebimento: 5`, `Descrição: Salário`.

2. **Adicionar Gasto**:
   - Escolha a categoria, descrição e tipo (débito ou crédito).
   - Se for no crédito, informe o cartão e se o gasto será parcelado.
   - Exemplo: `Categoria: Alimentação`, `Descrição: Supermercado`, `Tipo: débito`.

3. **Adicionar Financiamento**:
   - Informe o valor total, número de parcelas e descrição.
   - Exemplo: `Valor total: R$ 10000`, `Parcelas: 10`, `Descrição: Carro`.

4. **Pagar Parcela de Financiamento**:
   - Selecione o financiamento e as parcelas a pagar.
   - Verifique se há desconto e informe o valor total.

5. **Cadastrar Cartão de Crédito**:
   - Informe o nome do cartão, limite e dia de vencimento da fatura.
   - Exemplo: `Nome: Nubank`, `Limite: R$ 5000`, `Dia de vencimento: 10`.

6. **Pagar Fatura do Cartão**:
   - Selecione o cartão e pague a fatura pendente.

7. **Pagar Parcela Antecipada**:
   - Selecione as parcelas a pagar e verifique se há desconto.

8. **Ver Estatísticas do Mês**:
   - Gera um arquivo `.txt` com o saldo atual, gastos por categoria, parcelas pendentes e faturas.

9. **Ver Relatório Completo**:
   - Gera um arquivo `.txt` com todas as transações, parcelas e investimentos.

10. **Adicionar Categoria**:
    - Adicione uma nova categoria de gastos.
    - Exemplo: `Nome da categoria: Lazer`.

11. **Gerar Relatório Mensal**:
    - Informe o mês e o ano para gerar um relatório mensal em `.txt`.

12. **Gerar Relatório Anual**:
    - Informe o ano para gerar um relatório anual em `.txt`.

13. **Adicionar Investimento**:
    - Informe o valor, produto, banco e rendimento mensal.
    - Exemplo: `Valor: R$ 1000`, `Produto: Tesouro Direto`, `Banco: Banco X`, `Rendimento mensal: 0.5%`.

14. **Adicionar Rendimento de Investimento**:
    - Informe o produto, banco e valor do rendimento.
    - Exemplo: `Produto: Tesouro Direto`, `Banco: Banco X`, `Rendimento: R$ 50`.

---

### Salvamento de Dados

- **Dados Financeiros**: Todos os dados são salvos automaticamente em um arquivo Excel (`financas.xlsx`) após cada operação. O arquivo contém abas separadas para:
  - Recebimentos
  - Gastos
  - Financiamentos
  - Cartões de Crédito
  - Faturas
  - Parcelas
  - Investimentos

- **Relatórios**: Os relatórios são salvos na pasta `relatorios` com nomes únicos baseados na data e hora da geração. Exemplos:
  - `relatorios/estatisticas_mes_20231015_143022.txt`
  - `relatorios/relatorio_completo_20231015_143022.txt`
  - `relatorios/relatorio_mensal_10_2023_20231015_143022.txt`
  - `relatorios/relatorio_anual_2023_20231015_143022.txt`

---

## Exemplo de Saída nos Relatórios

### Estatísticas do Mês (`estatisticas_mes_*.txt`)
```
--- Estatísticas do Mês ---
Saldo Atual: R$ 10000.00
Total de Gastos: R$ 1500.00

Gastos por Categoria:
Alimentação: R$ 500.00
Transporte: R$ 300.00

Financiamentos:
Carro: 5/10 parcelas pagas

Faturas Pendentes:
Nubank: R$ 700.00

Parcelas Pendentes:
Restaurante (Parcela 1/3): R$ 66.67
```

### Relatório Completo (`relatorio_completo_*.txt`)
```
--- Relatório Completo ---
Saldo Atual: R$ 10000.00

Recebimentos:
Dia 5: R$ 5000.00 - Salário
Dia 10: R$ 3000.00 - Bônus

Gastos por Categoria:
Alimentação:
  Supermercado: R$ 500.00 (débito)
  Restaurante: R$ 200.00 (crédito)

Financiamentos:
Carro: 5/10 parcelas pagas

Cartões de Crédito:
Nubank: Limite R$ 5000.00, Vencimento dia 10

Faturas Pendentes:
Nubank: R$ 700.00

Parcelas Pendentes:
Restaurante (Parcela 1/3): R$ 66.67
```

### Relatório Mensal (`relatorio_mensal_*.txt`)
```
--- Relatório Mensal: 10/2023 ---
Total de Recebimentos: R$ 8000.00
Total de Gastos: R$ 1500.00
Saldo do Mês: R$ 6500.00
```

### Relatório Anual (`relatorio_anual_*.txt`)
```
--- Relatório Anual: 2023 ---

--- Mês 1 ---
Total de Recebimentos: R$ 5000.00
Total de Gastos: R$ 1000.00
Saldo do Mês: R$ 4000.00

--- Mês 2 ---
Total de Recebimentos: R$ 6000.00
Total de Gastos: R$ 1200.00
Saldo do Mês: R$ 4800.00
```

---

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias, correções ou novas funcionalidades.

---

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
