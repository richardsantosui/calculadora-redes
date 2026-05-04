import streamlit as st
import ipaddress

st.set_page_config(page_title="Calculadora Pro do Richard", page_icon="🌐")

st.title("🌐 Calculadora de Redes do Richard")
st.write("Esta página foi criada inteiramente em Python!")

# Campo de entrada
ip_digitado = st.text_input("Digite o IP/Máscara (Ex: 5.6.7.0/10):", "192.168.1.0/24")

try:
    rede = ipaddress.ip_network(ip_digitado, strict=False)
    
    # Criando colunas para ficar bonito
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"**Rede:** {rede.network_address}")
        st.info(f"**Máscara:** {rede.netmask}")
        
    with col2:
        st.warning(f"**Broadcast:** {rede.broadcast_address}")
        st.info(f"**Total de Hosts:** {rede.num_addresses - 2}")

    st.subheader("Lista de Sub-redes")
    dividir = st.slider("Dividir em quantas sub-redes?", 2, 64, 4)
    # Mostra um pedaço das sub-redes para testar
    st.write(f"Se você dividir em {dividir} partes, o prefixo mudará.")

except Exception as e:
    st.error(f"Formato inválido: {e}")
    # Adicione isso logo abaixo do st.write do slider
        bits_extras = math.ceil(math.log2(dividir))
        novo_prefixo = rede.prefixlen + bits_extras
        
        if novo_prefixo <= 32:
            subnets = list(rede.subnets(new_prefix=novo_prefixo))
            st.write(f"Novo prefixo: **/{novo_prefixo}**")
            st.table([{"Sub-rede": str(s.network_address), "Broadcast": str(s.broadcast_address)} for s in subnets[:10]])