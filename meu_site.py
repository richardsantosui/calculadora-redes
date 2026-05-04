import streamlit as st
import ipaddress
import math

st.set_page_config(page_title="Calculadora Pro do Richard", page_icon="🌐")

st.title("🌐 Calculadora de Redes do Richard")
st.write("Esta página está online na nuvem!")

ip_digitado = st.text_input("Digite o IP/Máscara (Ex: 192.168.1.0/24):", "192.168.1.0/24")

try:
    rede = ipaddress.ip_network(ip_digitado, strict=False)
    
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"**Rede:** {rede.network_address}")
        st.info(f"**Máscara:** {rede.netmask}")
    with col2:
        st.warning(f"**Broadcast:** {rede.broadcast_address}")
        st.info(f"**Total de Hosts:** {rede.num_addresses - 2}")

    st.subheader("Lista de Sub-redes")
    dividir = st.slider("Dividir em quantas sub-redes?", 2, 64, 4)
    
    # Cálculo das sub-redes (agora fora do bloco de erro e alinhado corretamente)
    bits_extras = math.ceil(math.log2(dividir))
    novo_prefixo = rede.prefixlen + bits_extras
    
    if novo_prefixo <= 32:
        subnets = list(rede.subnets(new_prefix=novo_prefixo))
        st.write(f"Novo prefixo: **/{novo_prefixo}**")
        
        # Cria a tabela com as sub-redes
        dados_tabela = [{"Sub-rede": str(s.network_address), "Broadcast": str(s.broadcast_address)} for s in subnets[:10]]
        st.table(dados_tabela)
    else:
        st.error("Não é possível dividir mais esta rede.")

except Exception as e:
    st.error(f"Formato inválido: {e}")
