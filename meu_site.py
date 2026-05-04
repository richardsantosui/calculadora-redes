import streamlit as st
import ipaddress
import math

st.set_page_config(page_title="Analista de Redes Pro", page_icon="🔍", layout="wide")

st.title("🔍 Analista de Redes & Sub-redes")

# --- FUNÇÃO PARA DESCOBRIR A CLASSE REAL ---
def get_ip_class(ip):
    primeiro_octeto = int(str(ip).split('.')[0])
    if 1 <= primeiro_octeto <= 126: return "Classe A (Grande Porte)"
    elif 128 <= primeiro_octeto <= 191: return "Classe B (Médio Porte)"
    elif 192 <= primeiro_octeto <= 223: return "Classe C (Pequeno Porte)"
    elif 224 <= primeiro_octeto <= 239: return "Classe D (Multicast)"
    else: return "Classe E (Experimental)"

# Entrada de dados
col_input1, col_input2 = st.columns([2, 1])
with col_input1:
    ip_input = st.text_input("IP/Prefixo de Origem:", "5.6.7.0/10")
with col_input2:
    num_subnets = st.number_input("Dividir em quantas redes?", min_value=1, value=4, step=1)

try:
    rede_principal = ipaddress.ip_network(ip_input, strict=False)
    ip_puro = rede_principal.network_address
    
    st.subheader("📊 Diagnóstico da Rede Principal")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Endereço de Rede", str(rede_principal.network_address))
    c2.metric("Máscara Decimal", str(rede_principal.netmask)) # Mudamos de Wildcard para Decimal
    c3.metric("Classe do IP", get_ip_class(ip_puro)) # Agora localiza a classe corretamente
    c4.metric("Máscara CIDR", f"/{rede_principal.prefixlen}")

    st.divider()

    # --- CÁLCULO DE SUB-REDES ---
    bits_extras = math.ceil(math.log2(num_subnets))
    novo_prefixo = rede_principal.prefixlen + bits_extras

    if novo_prefixo > 32:
        st.error("❌ Divisão impossível: Bits insuficientes.")
    else:
        subnets = list(rede_principal.subnets(new_prefix=novo_prefixo))
        st.subheader(f"📂 Detalhamento das {len(subnets)} Sub-redes (/{novo_prefixo})")
        
        page = st.number_input("Página:", min_value=1, value=1)
        start = (page - 1) * 10
        end = start + 10

        for i, sn in enumerate(subnets[start:end]):
            with st.expander(f"🌐 Sub-rede {start + i + 1}: {sn.network_address}/{novo_prefixo}"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write("**Faixa de IPs**")
                    st.write(f"- **Rede:** {sn.network_address}")
                    st.write(f"- **Primeiro Host:** {sn.network_address + 1}")
                    st.write(f"- **Último Host:** {sn.broadcast_address - 1}")
                    st.write(f"- **Broadcast:** {sn.broadcast_address}")
                with col_b:
                    st.write("**Binário e Máscara**")
                    st.code(f"Máscara: {sn.netmask}")
                    # Mostra o binário do primeiro octeto para confirmar a classe
                    binario = bin(int(sn.network_address))[2:].zfill(32)
                    st.code(f"Binário: {binario[:8]}.{binario[8:16]}.{binario[16:24]}.{binario[24:]}")

except Exception as e:
    st.warning("Formato de IP inválido. Exemplo: 192.168.1.0/24")
