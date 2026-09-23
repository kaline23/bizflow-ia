import streamlit as st
import datetime
import sqlite3
import pandas as pd
import os

# ---------------------------------------------------------
# BANCO DE DADOS LOCAL (SQLITE)
# ---------------------------------------------------------
def init_db():
    conn = sqlite3.connect('bizflow.db')
    c = conn.cursor()
    
    # 1. Clientes
    c.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            contato TEXT,
            servico TEXT,
            valor REAL,
            data TEXT
        )
    ''')
    
    # 2. Despesas / Custos / Contas a Pagar
    c.execute('''
        CREATE TABLE IF NOT EXISTS despesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            categoria TEXT,
            valor REAL,
            data_vencimento TEXT,
            status TEXT
        )
    ''')
    
    # 3. Estoque / Produtos
    c.execute('''
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT,
            quantidade INTEGER,
            nivel_minimo INTEGER,
            preco_custo REAL,
            preco_venda REAL
        )
    ''')

    conn.commit()
    conn.close()

# --- FUNÇÕES BANCO DE DADOS ---

# Clientes
def salvar_cliente(nome, contato, servico, valor):
    conn = sqlite3.connect('bizflow.db')
    c = conn.cursor()
    data_hoje = datetime.date.today().strftime('%d/%m/%Y')
    c.execute('INSERT INTO clientes (nome, contato, servico, valor, data) VALUES (?, ?, ?, ?, ?)', 
              (nome, contato, servico, valor, data_hoje))
    conn.commit()
    conn.close()

def listar_clientes():
    conn = sqlite3.connect('bizflow.db')
    c = conn.cursor()
    c.execute('SELECT id, nome, contato, servico, valor, data FROM clientes ORDER BY id DESC')
    dados = c.fetchall()
    conn.close()
    return dados

def atualizar_cliente(cliente_id, nome, contato, servico, valor):
    conn = sqlite3.connect('bizflow.db')
    c = conn.cursor()
    c.execute('UPDATE clientes SET nome = ?, contato = ?, servico = ?, valor = ? WHERE id = ?', 
              (nome, contato, servico, valor, cliente_id))
    conn.commit()
    conn.close()

def excluir_cliente(cliente_id):
    conn = sqlite3.connect('bizflow.db')
    c = conn.cursor()
    c.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
    conn.commit()
    conn.close()

# Despesas / Financeiro
def salvar_despesa(description, categoria, valor, data_venc, status):
    conn = sqlite3.connect('bizflow.db')
    c = conn.cursor()
    c.execute('INSERT INTO despesas (description, categoria, valor, data_vencimento, status) VALUES (?, ?, ?, ?, ?)', 
              (description, categoria, valor, data_venc, status))
    conn.commit()
    conn.close()

def listar_despesas():
    conn = sqlite3.connect('bizflow.db')
    c = conn.cursor()
    c.execute('SELECT id, description, categoria, valor, data_vencimento, status FROM despesas ORDER BY id DESC')
    dados = c.fetchall()
    conn.close()
    return dados

def atualizar_status_despesa(despesa_id, status):
    conn = sqlite3.connect('bizflow.db')
    c = conn.cursor()
    c.execute('UPDATE despesas SET status = ? WHERE id = ?', (status, despesa_id))
    conn.commit()
    conn.close()

def excluir_despesa(despesa_id):
    conn = sqlite3.connect('bizflow.db')
    c = conn.cursor()
    c.execute('DELETE FROM despesas WHERE id = ?', (despesa_id,))
    conn.commit()
    conn.close()

# Estoque / Produtos
def salvar_produto(produto, qte, min_q, p_custo, p_venda):
    conn = sqlite3.connect('bizflow.db')
    c = conn.cursor()
    c.execute('INSERT INTO estoque (produto, quantidade, nivel_minimo, preco_custo, preco_venda) VALUES (?, ?, ?, ?, ?)', 
              (produto, qte, min_q, p_custo, p_venda))
    conn.commit()
    conn.close()

def listar_estoque():
    conn = sqlite3.connect('bizflow.db')
    c = conn.cursor()
    c.execute('SELECT id, produto, quantidade, nivel_minimo, preco_custo, preco_venda FROM estoque ORDER BY id DESC')
    dados = c.fetchall()
    conn.close()
    return dados

def atualizar_produto(prod_id, produto, qte, min_q, p_custo, p_venda):
    conn = sqlite3.connect('bizflow.db')
    c = conn.cursor()
    c.execute('UPDATE estoque SET produto = ?, quantidade = ?, nivel_minimo = ?, preco_custo = ?, preco_venda = ? WHERE id = ?', 
              (produto, qte, min_q, p_custo, p_venda, prod_id))
    conn.commit()
    conn.close()

def excluir_produto(prod_id):
    conn = sqlite3.connect('bizflow.db')
    c = conn.cursor()
    c.execute('DELETE FROM estoque WHERE id = ?', (prod_id,))
    conn.commit()
    conn.close()

init_db()

# ---------------------------------------------------------
# CONFIGURAÇÃO E ESTILO VISUAL
# ---------------------------------------------------------
st.set_page_config(
    page_title="BizFlow AI - Gestão Inteligente",
    page_icon="💼",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .header-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        padding: 1.8rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .header-title { font-size: 2.2rem; font-weight: 800; margin-bottom: 0.3rem; }
    .header-subtitle { font-size: 1rem; color: #94A3B8; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BARRA LATERAL
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## 💼 **BizFlow AI**")
    st.caption("Painel do Empreendedor")
    st.divider()
    
    aba_selecionada = st.radio(
        "Módulos Principais",
        [
            "🏠 Visão Geral",
            "💰 Financeiro & Contas",
            "👥 Gestão de Clientes",
            "📦 Produtos & Estoque",
            "📣 Marketing Avançado",
            "💬 Atendimento ao Cliente",
            "📑 Relatórios"
        ]
    )

# CABEÇALHO
st.markdown("""
    <div class="header-container">
        <div class="header-title">BizFlow AI</div>
        <div class="header-subtitle">Plataforma Integrada de Gestão Operacional e Estratégica</div>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 1. VISÃO GERAL
# ---------------------------------------------------------
if aba_selecionada == "🏠 Visão Geral":
    st.subheader("📌 Resumo em Tempo Real")
    
    clientes = listar_clientes()
    despesas = listar_despesas()
    estoque = listar_estoque()
    
    df_c = pd.DataFrame(clientes, columns=["ID", "Nome", "Contato", "Serviço", "Valor", "Data"])
    df_d = pd.DataFrame(despesas, columns=["ID", "Descrição", "Categoria", "Valor", "Vencimento", "Status"])
    df_e = pd.DataFrame(estoque, columns=["ID", "Produto", "Qtd", "Mínimo", "Custo", "Venda"])
    
    rec_tot = df_c["Valor"].sum() if not df_c.empty else 0.0
    desp_pagas = df_d[df_d["Status"] == "Pago"]["Valor"].sum() if not df_d.empty else 0.0
    desp_pend = df_d[df_d["Status"] == "Pendente"]["Valor"].sum() if not df_d.empty else 0.0
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Faturamento Bruto", f"R$ {rec_tot:,.2f}")
    c2.metric("Despesas Pagas", f"R$ {desp_pagas:,.2f}")
    c3.metric("Contas a Pagar (Pendente)", f"R$ {desp_pend:,.2f}", delta=f"-R$ {desp_pend:,.2f}", delta_color="inverse")
    c4.metric("Saldo Real", f"R$ {(rec_tot - desp_pagas):,.2f}")
    
    st.divider()
    
    st.markdown("### ⚠️ Ações Necessárias")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("##### 📦 Produtos com Estoque Baixo")
        if not df_e.empty:
            criticos = df_e[df_e["Qtd"] <= df_e["Mínimo"]]
            if not criticos.empty:
                st.dataframe(criticos[["Produto", "Qtd", "Mínimo"]], use_container_width=True)
            else:
                st.success("Estoque sob controle.")
        else:
            st.info("Nenhum produto cadastrado.")

    with col_b:
        st.markdown("##### ⏳ Contas Próximas do Vencimento")
        if not df_d.empty:
            pendentes = df_d[df_d["Status"] == "Pendente"]
            if not pendentes.empty:
                st.dataframe(pendentes[["Descrição", "Valor", "Vencimento"]], use_container_width=True)
            else:
                st.success("Todas as contas registradas estão pagas!")
        else:
            st.info("Nenhuma conta registrada.")

# ---------------------------------------------------------
# 2. FINANCEIRO & CONTAS
# ---------------------------------------------------------
elif aba_selecionada == "💰 Financeiro & Contas":
    st.subheader("Controle Financeiro de Entrada e Saída")
    
    tab_cad, tab_lista = st.tabs(["➕ Cadastrar Lançamento", "📋 Gerenciar Despesas & Contas"])
    
    CATEGORIAS_FINANCEIRAS = [
        "Fornecedores / Matéria-Prima",
        "Aluguel / Condomínio",
        "Contas Consumo (Água/Luz/Net)",
        "Salários / Pró-Labore",
        "Impostos / Taxas (DAS/ISS)",
        "Marketing / Tráfego Pago",
        "Softwares / Assinaturas",
        "Manutenção / Equipamentos",
        "Taxas de Cartão / Bancárias",
        "Embalagens / Frete",
        "Outros"
    ]
    
    with tab_cad:
        c1, c2 = st.columns(2)
        with c1:
            desc = st.text_input("Descrição da Conta/Despesa:", placeholder="Ex: Compra de Estoque - Fornecedor X")
            cat = st.selectbox("Categoria Detalhada:", CATEGORIAS_FINANCEIRAS)
            val = st.number_input("Valor (R$):", min_value=0.0, step=10.0)
        with c2:
            data_v = st.date_input("Data de Vencimento:", datetime.date.today())
            stat = st.selectbox("Status de Pagamento:", ["Pendente", "Pago"])
            
            st.write("")
            if st.button("Salvar Lançamento", type="primary"):
                if desc and val > 0:
                    salvar_despesa(desc, cat, val, data_v.strftime('%d/%m/%Y'), stat)
                    st.success("Lançamento salvo com sucesso!")
                    st.rerun()

    with tab_lista:
        desp = listar_despesas()
        if desp:
            for d in desp:
                d_id, d_desc, d_cat, d_val, d_venc, d_stat = d
                
                col_i1, col_i2, col_i3, col_i4, col_i5, col_i6 = st.columns([1, 3, 2, 2, 2, 2])
                col_i1.write(f"**#{d_id}**")
                col_i2.write(f"**{d_desc}**\n*{d_cat}*")
                col_i3.write(f"R$ {d_val:,.2f}")
                col_i4.write(f"Venc: {d_venc}")
                col_i5.write(f"**{d_stat}**")
                
                with col_i6:
                    if d_stat == 'Pendente':
                        if st.button("Pagar ✅", key=f"pay_{d_id}"):
                            atualizar_status_despesa(d_id, "Pago")
                            st.rerun()
                    if st.button("Excluir 🗑️", key=f"del_desp_{d_id}"):
                        excluir_despesa(d_id)
                        st.rerun()
                st.divider()
        else:
            st.info("Nenhuma despesa registrada.")

# ---------------------------------------------------------
# 3. GESTÃO DE CLIENTES (SISTEMA SIMPLIFICADO)
# ---------------------------------------------------------
elif aba_selecionada == "👥 Gestão de Clientes":
    st.subheader("Gerenciamento de Clientes e Vendas")
    
    t_cad_c, t_ger_c = st.tabs(["➕ Cadastrar Novo Cliente", "📋 Lista e Gerenciamento de Clientes"])
    
    with t_cad_c:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            nome_c = st.text_input("Nome do Cliente:")
            contato_c = st.text_input("Contato / WhatsApp:")
        with col_c2:
            serv_c = st.text_input("Produto / Serviço Adquirido:")
            val_c = st.number_input("Valor Total da Compra (R$):", min_value=0.0, step=10.0)
            
        if st.button("Cadastrar Cliente e Venda", type="primary"):
            if nome_c and val_c > 0:
                salvar_cliente(nome_c, contato_c, serv_c, val_c)
                st.success("Cliente/Venda cadastrado com sucesso!")
                st.rerun()

    with t_ger_c:
        clientes = listar_clientes()
        if clientes:
            for cli in clientes:
                c_id, c_nome, c_contato, c_serv, c_val, c_data = cli
                
                with st.expander(f"👤 {c_nome} — R$ {c_val:,.2f} ({c_serv})"):
                    col_u1, col_u2 = st.columns([3, 1])
                    
                    with col_u1:
                        # Edição direta no painel do cliente
                        edit_nome = st.text_input("Nome:", value=c_nome, key=f"cnome_{c_id}")
                        edit_contato = st.text_input("Contato:", value=c_contato, key=f"ccont_{c_id}")
                        edit_serv = st.text_input("Serviço/Produto:", value=c_serv, key=f"cserv_{c_id}")
                        edit_val = st.number_input("Valor (R$):", value=float(c_val), key=f"cval_{c_id}")
                    
                    with col_u2:
                        st.write("### Ações")
                        if st.button("💾 Salvar Alterações", key=f"save_cli_{c_id}", type="primary"):
                            atualizar_cliente(c_id, edit_nome, edit_contato, edit_serv, edit_val)
                            st.success("Cliente atualizado!")
                            st.rerun()
                        
                        st.write("")
                        if st.button("🗑️ Excluir Cliente", key=f"del_cli_{c_id}"):
                            excluir_cliente(c_id)
                            st.warning("Cliente removido!")
                            st.rerun()
        else:
            st.info("Nenhum cliente cadastrado.")

# ---------------------------------------------------------
# 4. PRODUTOS & ESTOQUE (SISTEMA SIMPLIFICADO)
# ---------------------------------------------------------
elif aba_selecionada == "📦 Produtos & Estoque":
    st.subheader("Gerenciamento de Produtos e Estoque")
    
    t_cad_p, t_ger_p = st.tabs(["➕ Cadastrar Novo Produto", "📋 Lista e Controle de Estoque"])
    
    with t_cad_p:
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            nome_p = st.text_input("Nome do Produto:")
            qte_p = st.number_input("Quantidade em Estoque:", min_value=0, value=10)
            min_p = st.number_input("Nível Mínimo para Alerta:", min_value=1, value=3)
        with c_p2:
            custo_p = st.number_input("Preço de Custo (R$):", min_value=0.0, value=10.0)
            venda_p = st.number_input("Preço de Venda (R$):", min_value=0.0, value=25.0)
            
            if st.button("Salvar Produto no Estoque", type="primary"):
                if nome_p:
                    salvar_produto(nome_p, qte_p, min_p, custo_p, venda_p)
                    st.success("Produto adicionado com sucesso!")
                    st.rerun()

    with t_ger_p:
        prods = listar_estoque()
        if prods:
            for p in prods:
                p_id, p_nome, p_qte, p_min, p_custo, p_venda = p
                
                with st.expander(f"📦 {p_nome} — Quantidade em Estoque: {p_qte} un. (Venda: R$ {p_venda:,.2f})"):
                    col_ep1, col_ep2 = st.columns([3, 1])
                    
                    with col_ep1:
                        ep_nome = st.text_input("Produto:", value=p_nome, key=f"pn_{p_id}")
                        col_sub1, col_sub2 = st.columns(2)
                        ep_qte = col_sub1.number_input("Qtd Estoque:", value=int(p_qte), key=f"pq_{p_id}")
                        ep_min = col_sub2.number_input("Mínimo Alerta:", value=int(p_min), key=f"pm_{p_id}")
                        
                        col_sub3, col_sub4 = st.columns(2)
                        ep_custo = col_sub3.number_input("Preço Custo (R$):", value=float(p_custo), key=f"pc_{p_id}")
                        ep_venda = col_sub4.number_input("Preço Venda (R$):", value=float(p_venda), key=f"pv_{p_id}")

                    with col_ep2:
                        st.write("### Ações")
                        if st.button("💾 Salvar Alterações", key=f"save_prod_{p_id}", type="primary"):
                            atualizar_produto(p_id, ep_nome, ep_qte, ep_min, ep_custo, ep_venda)
                            st.success("Produto atualizado!")
                            st.rerun()
                        
                        st.write("")
                        if st.button("🗑️ Excluir Produto", key=f"del_prod_{p_id}"):
                            excluir_produto(p_id)
                            st.warning("Produto removido!")
                            st.rerun()
        else:
            st.info("Nenhum produto em estoque.")

# ---------------------------------------------------------
# 5. MARKETING AVANÇADO
# ---------------------------------------------------------
elif aba_selecionada == "📣 Marketing Avançado":
    st.subheader("Gerador de Conteúdo e Estratégias de Vendas")
    
    col_m1, col_m2 = st.columns([1, 2], gap="large")
    
    with col_m1:
        st.markdown("##### 🎯 Configurar Campanha")
        produto_m = st.text_input("Produto / Oferta:", placeholder="Ex: Hidratação Capilar / Coleção de Verão")
        publico_m = st.text_input("Público-Alvo:", placeholder="Ex: Mulheres que buscam praticidade / Atletas")
        desconto_m = st.text_input("Benefício / Oferta:", placeholder="Ex: 15% OFF / Frete Grátis")
        
        btn_m = st.button("✨ Criar Pacote Completo de Divulgação", type="primary")

    with col_m2:
        if btn_m and produto_m:
            st.markdown("### 📱 Materiais Gerados Prontos para Uso")
            
            st.subheader("1. Legenda Completa para Feed (Instagram/Facebook)")
            st.code(f"""
👉 Quer transformar sua experiência com {produto_m}?

Se você é {publico_m if publico_m else 'alguém que valoriza qualidade'}, esta oferta foi feita pensando em você!

Aproveite hoje mesmo: {desconto_m if desconto_m else 'Condições especiais por tempo limitado'}.

✅ Praticidade
✅ Resultados garantidos
✅ Envio/Atendimento rápido

📲 Clique no link da bio e garanta o seu antes que o lote acabe!

#marketing #{produto_m.lower().replace(' ', '')} #oferta #qualidade #novidades
            """, language="text")

            st.subheader("2. Roteiro para Stories (3 Telas)")
            st.info(f"""
            * **Tela 1 (Atenção):** "Você também sente dificuldade com [Problema do Cliente]?"
            * **Tela 2 (Solução):** "Apresentamos o **{produto_m}**! A solução ideal com {desconto_m}."
            * **Tela 3 (Chamada):** "Clique no link abaixo ou envie uma mensagem no Direct para garantir!"
            """)

            st.subheader("3. Mensagem para Disparo VIP (WhatsApp)")
            st.success(f"""
Olá! Tudo bem? 

Passando para te avisar em primeira mão: liberamos hoje uma condição exclusiva para o **{produto_m}**. 

🎁 **Benefício Especial:** {desconto_m if desconto_m else 'Atendimento VIP'}
⏰ Válido apenas para as primeiras pessoas que responderem esta mensagem.

Podemos reservar o seu?
            """)

# ---------------------------------------------------------
# 6. ATENDIMENTO AO CLIENTE
# ---------------------------------------------------------
elif aba_selecionada == "💬 Atendimento ao Cliente":
    st.subheader("Respostas Rápidas de Vendas")
    
    duvida = st.selectbox("Selecione a Situação do Atendimento:", [
        "Cliente perguntando o preço",
        "Cliente achou caro",
        "Cliente perguntando forma de pagamento e entrega",
        "Reclamação de atraso ou problema"
    ])
    
    if st.button("Gerar Resposta Profissional"):
        if duvida == "Cliente perguntando o preço":
            resp = "Olá! O valor do [Produto/Serviço] é R$ [X]. Ele inclui [Benefício 1] e [Benefício 2]. Como você gostaria de realizar o pagamento hoje? Temos condições facilitadas!"
        elif duvida == "Cliente achou caro":
            resp = "Compreendo perfeitamente! Trabalhamos com insumos de altíssima qualidade para garantir que você não tenha dores de cabeça depois. Além disso, oferecemos suporte garantido. Conseguimos parcelar em até X vezes sem juros para você!"
        elif duvida == "Cliente perguntando forma de pagamento e entrega":
            resp = "Aceitamos Pix, cartão de crédito e débito! Enviamos via [Correios/Entregador] com rastreamento rápido. Qual é o seu CEP para eu calcular o prazo exato?"
        else:
            resp = "Sinto muito por esse inconveniente! Valorizamos muito a sua experiência. Já estou checando pessoalmente a sua situação para resolver agora mesmo. Pode me confirmar o número do seu pedido?"
            
        st.code(resp, language="text")

# ---------------------------------------------------------
# 7. RELATÓRIOS
# ---------------------------------------------------------
elif aba_selecionada == "📑 Relatórios":
    st.subheader("Análise Executiva da Empresa")
    
    if st.button("📊 Emitir Relatório Consolidado", type="primary"):
        clientes = listar_clientes()
        despesas = listar_despesas()
        
        df_c = pd.DataFrame(clientes, columns=["ID", "Nome", "Contato", "Serviço", "Valor", "Data"])
        df_d = pd.DataFrame(despesas, columns=["ID", "Descrição", "Categoria", "Valor", "Vencimento", "Status"])
        
        faturamento = df_c["Valor"].sum() if not df_c.empty else 0.0
        gastos_totais = df_d["Valor"].sum() if not df_d.empty else 0.0
        lucro = faturamento - gastos_totais
        
        st.markdown(f"""
        ### 📊 Balanço Geral
        * **Receita Bruta Acumulada:** R$ {faturamento:,.2f}
        * **Despesas Totais Cadastradas:** R$ {gastos_totais:,.2f}
        * **Resultado Operacional Líquido:** R$ {lucro:,.2f}
        """)