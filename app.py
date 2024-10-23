from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Armazenamento temporário de transações
transacoes = []

# Receita mensal (852 euros)
receita_mensal = 852.0

# Classe Transacao
class Transacao:
    def __init__(self, tipo, descricao, valor, categoria=None):
        self.tipo = tipo  # 'receita' ou 'despesa'
        self.descricao = descricao
        self.valor = valor
        self.categoria = categoria
        self.data = datetime.now()  # Data da transação

# Função para calcular o saldo
def calcular_saldo():
    saldo = 0
    for transacao in transacoes:
        if transacao.tipo == 'receita':
            saldo += transacao.valor
        elif transacao.tipo == 'despesa':
            saldo -= transacao.valor
    return saldo

# Função para calcular as despesas do mês atual
def calcular_despesas_mensais():
    despesas_mensais = 0
    mes_atual = datetime.now().month
    for transacao in transacoes:
        if transacao.tipo == 'despesa' and transacao.data.month == mes_atual:
            despesas_mensais += transacao.valor
    return despesas_mensais

# Função para fornecer dicas financeiras
def fornecer_dicas(saldo, despesas_mensais):
    if saldo < 0:
        return "Seu saldo está negativo. Tente reduzir suas despesas."
    elif despesas_mensais > receita_mensal:
        return "Você ultrapassou seu limite de despesas mensais! Tente cortar gastos."
    elif despesas_mensais > receita_mensal * 0.9:
        return "Atenção! Você já gastou 90% da sua receita mensal."
    elif saldo < 500:
        return "Você está com um saldo baixo. Evite grandes gastos."
    else:
        return "Seu saldo está saudável. Continue assim!"

# Função para verificar se a despesa ultrapassa a receita mensal
def verificar_limite_despesas(valor_despesa, despesas_mensais):
    if despesas_mensais + valor_despesa > receita_mensal:
        return True
    return False

# Página inicial - Lista as transações e mostra o saldo e despesas do mês
@app.route('/')
def index():
    saldo = calcular_saldo()
    despesas_mensais = calcular_despesas_mensais()
    dica = fornecer_dicas(saldo, despesas_mensais)
    return render_template('index.html', transacoes=transacoes, saldo=saldo, despesas_mensais=despesas_mensais, dica=dica, receita_mensal=receita_mensal)

# Rota para adicionar transação
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        tipo = request.form['tipo']
        descricao = request.form['descricao']
        valor = float(request.form['valor'])
        categoria = request.form.get('categoria')
        
        # Verificar se a despesa ultrapassa a receita mensal
        if tipo == 'despesa':
            despesas_mensais = calcular_despesas_mensais()
            if verificar_limite_despesas(valor, despesas_mensais):
                return render_template('aviso_despesas.html', valor=valor, despesas_mensais=despesas_mensais, receita_mensal=receita_mensal)

        # Cria uma nova transação e a adiciona à lista
        nova_transacao = Transacao(tipo, descricao, valor, categoria)
        transacoes.append(nova_transacao)

        return redirect(url_for('index'))
    
    return render_template('adicionar.html')

if __name__ == '__main__':
    app.run(debug=True)
