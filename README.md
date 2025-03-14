# Sistema de Finanças Pessoais

O **Sistema de Finanças Pessoais** é um programa em Python que ajuda você a gerenciar suas finanças de forma eficiente. Ele permite registrar recebimentos, gastos, financiamentos e cartões de crédito, além de fornecer estatísticas mensais e relatórios completos. O programa salva os dados em um arquivo Excel para persistência e fácil acesso.

## Funcionalidades

- **Recebimentos**: Registre valores recebidos e o dia do mês em que foram recebidos.
- **Gastos**: Registre gastos por categoria, com opção de pagamento no débito ou crédito.
- **Financiamentos**: Cadastre financiamentos e pague parcelas, com suporte para descontos em pagamentos antecipados.
- **Cartões de Crédito**: Cadastre cartões de crédito, gerencie faturas e parcelas futuras.
- **Estatísticas Mensais**: Visualize o saldo atual, gastos por categoria, parcelas pendentes e faturas.
- **Relatório Completo**: Gere um relatório detalhado de todas as transações e parcelas.

## Requisitos

- Python 3.x
- Bibliotecas necessárias: `pandas`, `openpyxl`

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
10. Sair
```

### Exemplos de Uso

1. **Adicionar Recebimento**:
   - Digite o valor recebido e o dia do mês.
   - Exemplo: `Valor recebido: R$ 5000`, `Dia do recebimento: 5`.

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
   - Visualize o saldo atual, gastos por categoria, parcelas pendentes e faturas.

9. **Ver Relatório Completo**:
   - Gere um relatório detalhado de todas as transações e parcelas.

### Salvamento de Dados

Todos os dados são salvos automaticamente em um arquivo Excel (`financas.xlsx`) após cada operação. O arquivo contém abas separadas para:

- Recebimentos
- Gastos
- Financiamentos
- Cartões de Crédito
- Faturas
- Parcelas

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias, correções ou novas funcionalidades.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
