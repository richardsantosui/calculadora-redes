import streamlit as st
import ipaddress
import math

st.set_page_config(page_title="Analista de Redes Pro", page_icon="🔍", layout="wide")

st.title("🔍 Analista de Redes & Sub-redes")
st.write("Análise técnica profunda de endereçamento IPv4.")

# Entrada de dados
col_input1, col_input2 = st.columns([2, 1])
with col_input1:
    ip_input = st.text_input("IP/Prefixo de Origem:", "189.8.0.0/16")
with col_input2:
    num_subnets = st.number_input("Dividir em quantas redes?", min_value=1, value=4, step=1)

try:
    rede_principal = ipaddress.ip_network(ip_input, strict=False)
    
    # --- VISÃO GERAL DA REDE PAI ---
    st.subheader("📊 Visão Geral da Rede Principal")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Endereço de Rede", str(rede_principal.network_address))
    c2.metric("Máscara Curinga (Wildcard)", str(rede_principal.hostmask))
    c3.metric("Classe Sugerida", rede_principal.network_address.reverse_pointer.split('.')[2])
    c4.metric("Bits de Host", 32 - rede_principal.prefixlen)

    # --- CÁLCULO DE SUB-REDES ---
    bits_extras = math.ceil(math.log2(num_subnets))
    novo_prefixo = rede_principal.prefixlen + bits_extras

    if novo_prefixo > 32:
        st.error("❌ Divisão impossível: Bits insuficientes no IPv4.")
    else:
        subnets = list(rede_principal.subnets(new_prefix=novo_prefixo))
        st.divider()
        st.subheader(f"📂 Detalhamento das {len(subnets)} Sub-redes (/{novo_prefixo})")
        
        # Paginação para não travar o navegador
        limit = 20
        page = st.number_input("Página:", min_value=1, value=1)
        start = (page - 1) * limit
        end = start + limit

        for i, sn in enumerate(subnets[start:end]):
            # Criamos um expansor para cada sub-rede
            with st.expander(f"🌐 Sub-rede {start + i + 1}: {sn.network_address}/{novo_prefixo}"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.write("**Informações de Endereçamento**")
                    st.write(f"- **Primeiro Host utilizável:** {sn.network_address + 1}")
                    st.write(f"- **Último Host utilizável:** {sn.broadcast_address - 1}")
                    st.write(f"- **Broadcast:** {sn.broadcast_address}")
                    st.write(f"- **Total de IPs úteis:** {sn.num_addresses - 2}")
                
                with col_b:
                    st.write("**Detalhes Técnicos**")
                    st.code(f"Máscara Decimal: {sn.netmask}")
                    st.code(f"Binário da Rede: {bin(int(sn.network_address))}")
                    st.code(f"Prefixo (CIDR): /{novo_prefixo}")

        st.info(f"Mostrando sub-redes de {start+1} a {min(end, len(subnets))}. Use o campo 'Página' acima para navegar.")

except Exception as e:
    st.warning("Aguardando um IP válido com máscara (Ex: 172.16.0.0/12)")
