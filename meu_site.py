import streamlit as st
import ipaddress
import math

# Configuração da Página
st.set_page_config(page_title="Analista de Redes Pro", page_icon="🔍", layout="wide")

# --- FUNÇÕES DE APOIO ---
def get_ip_class(ip):
    """Identifica a classe do IP baseada no primeiro octeto."""
    primeiro_octeto = int(str(ip).split('.')[0])
    if 1 <= primeiro_octeto <= 126: return "Classe A (Grande Porte)"
    elif 128 <= primeiro_octeto <= 191: return "Classe B (Médio Porte)"
    elif 192 <= primeiro_octeto <= 223: return "Classe C (Pequeno Porte)"
    elif 224 <= primeiro_octeto <= 239: return "Classe D (Multicast)"
    else: return "Classe E (Experimental)"

def format_bin(ip_ou_mask):
    """Transforma IP ou Máscara em binário com pontos separadores."""
    return ".".join([bin(int(x))[2:].zfill(8) for x in str(ip_ou_mask).split('.')])

# --- INTERFACE ---
st.title("🔍 Analista de Redes & Sub-redes")
st.write("Análise técnica detalhada com Raio-X binário e contagem de sub-redes.")

# Entrada de dados
col_input1, col_input2 = st.columns([2, 1])
with col_input1:
    ip_input = st.text_input("IP/Prefixo de Origem (Ex: 5.6.7.0/10):", "5.6.7.0/10")
with col_input2:
    num_subnets = st.number_input("Dividir em quantas redes?", min_value=1, value=4, step=1)

try:
    # Processamento da rede principal
    rede_principal = ipaddress.ip_network(ip_input, strict=False)
    ip_puro = rede_principal.network_address
    
    # --- DIAGNÓSTICO PRINCIPAL ---
    st.subheader("📊 Diagnóstico da Rede Principal")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Rede", str(rede_principal.network_address))
    with c2:
        st.metric("Máscara Resolvida", str(rede_principal.netmask))
    with c3:
        st.metric("Classe Identificada", get_ip_class(ip_puro))
    with c4:
        st.metric("Prefixo Atual", f"/{rede_principal.prefixlen}")

    st.divider()

    # --- CÁLCULO E EXIBIÇÃO DAS SUB-REDES ---
    bits_extras = math.ceil(math.log2(num_subnets))
    novo_prefixo = rede_principal.prefixlen + bits_extras

    if novo_prefixo > 32:
        st.error("❌ Erro: O número de sub-redes solicitado ultrapassa o limite de 32 bits do IPv4.")
    else:
        subnets = list(rede_principal.subnets(new_prefix=novo_prefixo))
        total_criado = len(subnets)
        st.subheader(f"📂 Detalhamento das {total_criado} Sub-redes (/{novo_prefixo})")
        
        # Paginação
        limit = 10
        total_paginas = math.ceil(total_criado / limit)
        page = st.number_input("Página da lista:", min_value=1, max_value=total_paginas, value=1)
        
        start = (page - 1) * limit
        end = start + limit

        for i, sn in enumerate(subnets[start:end]):
            # Expansor para cada sub-rede
            with st.expander(f"🌐 Sub-rede {start + i + 1}: {sn.network_address}/{novo_prefixo}"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.write("**📍 Endereçamento**")
                    st.write(f"- **IP de Rede:** `{sn.network_address}`")
                    st.write(f"- **Primeiro Host:** `{sn.network_address + 1}`")
                    st.write(f"- **Último Host:** `{sn.broadcast_address - 1}`")
                    st.write(f"- **Broadcast:** `{sn.broadcast_address}`")
                    st.success(f"**Máscara Resolvida: {sn.netmask}**")
                    # NOVA INFORMAÇÃO SOLICITADA:
                    st.info(f"🔢 **Sub-redes deste tamanho possíveis na rede: {total_criado}**")
                
                with col_b:
                    st.write("**💻 Raio-X Binário Alinhado**")
                    st.text("Binário do IP:")
                    st.code(format_bin(sn.network_address))
                    
                    st.text("Binário da Máscara:")
                    st.code(format_bin(sn.netmask))
                    
                    st.caption(f"Prefixo: /{sn.prefixlen} | Total de IPs úteis por sub-rede: {sn.num_addresses - 2}")

        st.caption(f"Mostrando sub-redes {start+1} a {min(end, total_criado)} de um total de {total_criado}.")

except Exception as e:
    st.warning(f"Aguardando entrada válida (IP/Máscara). Exemplo: 10.0.0.0/8")
