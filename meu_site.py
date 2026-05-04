import streamlit as st
import ipaddress
import math

# Configuração de Interface Profissional
st.set_page_config(page_title="Sistema de Endereçamento IPv4", page_icon="⚙️", layout="wide")

# --- FUNÇÕES TÉCNICAS ---
def identificar_classe(ip):
    primeiro_octeto = int(str(ip).split('.')[0])
    if 1 <= primeiro_octeto <= 126: return "Classe A"
    elif 128 <= primeiro_octeto <= 191: return "Classe B"
    elif 192 <= primeiro_octeto <= 223: return "Classe C"
    return "Especial/Experimental"

def formatar_binario(valor):
    return ".".join([bin(int(x))[2:].zfill(8) for x in str(valor).split('.')])

# --- CABEÇALHO FORMAL ---
st.title("🖥️ Sistema de Gestão e Planejamento de Sub-redes")
st.markdown(f"**Desenvolvido por:** Richard Santos | **Finalidade:** Auditoria e Divisão de Redes IPv4")
st.divider()

# Painel de Entrada de Parâmetros
col_input1, col_input2 = st.columns([2, 1])
with col_input1:
    entrada_ip = st.text_input("Endereço de Rede com Prefixo CIDR (Ex: 10.0.0.0/8):", "189.6.0.0/16")
with col_input2:
    divisoes_solicitadas = st.number_input("Quantidade de Sub-redes desejadas:", min_value=1, value=16, step=1)

try:
    # Processamento de Dados de Infraestrutura
    rede_mestra = ipaddress.ip_network(entrada_ip, strict=False)
    
    st.subheader("📋 Especificações Técnicas da Rede Principal")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Endereço de Rede", str(rede_mestra.network_address))
    m2.metric("Máscara Decimal", str(rede_mestra.netmask))
    m3.metric("Segmentação", identificar_classe(rede_mestra.network_address))
    m4.metric("Prefixo", f"/{rede_mestra.prefixlen}")

    st.divider()

    # Lógica de Segmentação (VLSM)
    bits_adicionais = math.ceil(math.log2(divisoes_solicitadas))
    novo_prefixo = rede_mestra.prefixlen + bits_adicionais

    if novo_prefixo > 32:
        st.error("Solicitação Inválida: O número de sub-redes excede a capacidade de bits do protocolo IPv4.")
    else:
        lista_subredes = list(rede_mestra.subnets(new_prefix=novo_prefixo))
        total_redes = len(lista_subredes)
        
        st.subheader(f"📂 Relatório de Segmentação: {total_redes} Sub-redes Geradas (/{novo_prefixo})")
        
        # Paginação para análise de dados
        idx_pagina = st.number_input("Página de Relatório:", min_value=1, max_value=math.ceil(total_redes/10), value=1)
        inicio, fim = (idx_pagina - 1) * 10, idx_pagina * 10

        for i, sn in enumerate(lista_subredes[inicio:fim]):
            with st.expander(f"🌐 Detalhamento Técnico - Sub-rede {inicio + i + 1}: {sn.network_address}/{novo_prefixo}"):
                col_dados, col_bin = st.columns(2)
                
                with col_dados:
                    st.markdown("**Parâmetros de Endereçamento**")
                    tabela = {
                        "Atributo": ["Network ID", "Gateway Sugerido", "Último Host Válido", "Broadcast Address", "Máscara"],
                        "Valor": [str(sn.network_address), str(sn.network_address + 1), str(sn.broadcast_address - 1), str(sn.broadcast_address), str(sn.netmask)]
                    }
                    st.table(tabela)
                    st.info(f"Capacidade: {sn.num_addresses - 2} hosts utilizáveis.")
                
                with col_bin:
                    st.markdown("**Análise de Camada 3 (Binário)**")
                    st.text("Estrutura do IP:")
                    st.code(formatar_binario(sn.network_address))
                    st.text("Máscara de Sub-rede:")
                    st.code(formatar_binario(sn.netmask))
                    st.caption(f"Capacidade Total do Bloco Principal: {total_redes} redes equivalentes.")

except Exception as erro:
    st.warning("Aguardando inserção de dados em formato CIDR válido.")
