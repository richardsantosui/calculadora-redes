import streamlit as st
import ipaddress
import math

st.set_page_config(page_title="Calculadora Pro do Richard", page_icon="🌐", layout="wide")

st.title("🌐 Calculadora de Redes Profissional")
st.write("Configuração avançada de sub-redes.")

# Entrada de IP
ip_digitado = st.text_input("Digite o IP/Máscara (Ex: 10.0.0.0/8):", "10.0.0.0/8")

try:
    rede = ipaddress.ip_network(ip_digitado, strict=False)
    
    # Cards informativos
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rede", str(rede.network_address))
    c2.metric("Broadcast", str(rede.broadcast_address))
    c3.metric("Máscara", str(rede.netmask))
    c4.metric("Hosts Totais", f"{rede.num_addresses - 2:,}")

    st.divider()

    # Escolha de divisão
    st.subheader("🛠️ Planejamento de Divisão")
    
    # Agora você digita o número, sem limite de 64!
    quantidade_subredes = st.number_input("Em quantas sub-redes quer dividir?", min_value=2, value=16, step=2)
    
    bits_extras = math.ceil(math.log2(quantidade_subredes))
    novo_prefixo = rede.prefixlen + bits_extras
    
    if novo_prefixo <= 32:
        subnets = list(rede.subnets(new_prefix=novo_prefixo))
        total_criado = len(subnets)
        
        st.success(f"Criei **{total_criado}** sub-redes com prefixo **/{novo_prefixo}**")
        
        # Sistema de "Páginas" para ver qual você quiser
        st.write("### 🔍 Visualizar Sub-redes")
        if total_criado > 10:
            start_idx = st.number_input(f"Mostrar a partir da sub-rede nº:", min_value=1, max_value=total_criado, value=1) - 1
            num_show = st.slider("Quantas mostrar por vez?", 5, 50, 10)
        else:
            start_idx = 0
            num_show = total_criado

        # Gerar tabela
        dados_tabela = []
        for i, s in enumerate(subnets[start_idx : start_idx + num_show]):
            dados_tabela.append({
                "Nº": start_idx + i + 1,
                "Rede": str(s.network_address),
                "Primeiro Host": str(s.network_address + 1),
                "Último Host": str(s.broadcast_address - 1),
                "Broadcast": str(s.broadcast_address)
            })
        
        st.table(dados_tabela)
        st.info(f"Mostrando {len(dados_tabela)} de {total_criado} sub-redes.")
        
    else:
        st.error("ERRO: O número de sub-redes exige mais bits do que o IPv4 permite (máximo /32).")

except Exception as e:
    st.error(f"Aguardando IP válido... (Erro: {e})")
