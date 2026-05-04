import streamlit as st
import ipaddress
import math

st.set_page_config(page_title="Capacidade Total IPv4", page_icon="🧮", layout="wide")

def formatar_binario(valor):
    return ".".join([bin(int(x))[2:].zfill(8) for x in str(valor).split('.')])

st.title("🧮 Calculadora de Capacidade Total de Redes")
st.markdown(f"**Desenvolvido por:** Richard Santos | **Foco:** Análise de Escala e VLSM")
st.divider()

# Entrada de Dados
col1, col2 = st.columns(2)
with col1:
    entrada_ip = st.text_input("Bloco CIDR Principal (Ex: 10.0.0.0/8):", "189.6.0.0/16")
with col2:
    prefixo_alvo = st.number_input("Prefixo das Sub-redes (Ex: /24):", min_value=1, max_value=32, value=24)

try:
    rede_pai = ipaddress.ip_network(entrada_ip, strict=False)
    
    if prefixo_alvo < rede_pai.prefixlen:
        st.error(f"O prefixo alvo (/{prefixo_alvo}) deve ser maior que o original (/{rede_pai.prefixlen}).")
    else:
        # --- CÁLCULOS DE CAPACIDADE TOTAL ---
        total_subredes = 2**(prefixo_alvo - rede_pai.prefixlen)
        ips_por_subrede = 2**(32 - prefixo_alvo)
        hosts_uteis = ips_por_subrede - 2 if ips_por_subrede > 2 else 0
        total_ips_global = total_subredes * ips_por_subrede

        # --- PAINEL DE MÉTRICAS GLOBAIS ---
        st.subheader("🌐 Relatório de Capacidade Global")
        m1, m2, m3 = st.columns(3)
        m1.metric("Sub-redes Possíveis", f"{total_subredes:,}")
        m2.metric("Hosts Úteis por Rede", f"{hosts_uteis:,}")
        m3.metric("Total de IPs no Bloco", f"{total_ips_global:,}")

        st.divider()

        # --- VISUALIZAÇÃO DE AMOSTRA E BUSCA ---
        st.subheader(f"🔍 Explorador de Segmentação (1 de {total_subredes:,})")
        
        # Slider para navegar em QUALQUER rede, não importa se são milhares
        n_rede = st.select_slider(
            "Arraste para navegar entre as sub-redes ou use as setas:",
            options=range(1, total_subredes + 1),
            value=1
        )

        # Cálculo matemático direto da sub-rede N (sem carregar a lista inteira na RAM)
        # Isso permite que o site calcule a rede 1.000.000 instantaneamente
        salto = ips_por_subrede
        ip_da_rede = ipaddress.IPv4Address(int(rede_pai.network_address) + ((n_rede - 1) * salto))
        sub_atual = ipaddress.ip_network(f"{ip_da_rede}/{prefixo_alvo}")

        # Exibição Técnica
        c_left, c_right = st.columns(2)
        with c_left:
            st.markdown(f"### Detalhes da Rede #{n_rede}")
            st.success(f"**Máscara Resolvida: {sub_atual.netmask}**")
            st.write(f"- **ID de Rede:** `{sub_atual.network_address}`")
            st.write(f"- **Broadcast:** `{sub_atual.broadcast_address}`")
            st.write(f"- **Faixa Útil:** `{sub_atual.network_address + 1}` até `{sub_atual.broadcast_address - 1}`")
        
        with c_right:
            st.markdown("### Estrutura Binária")
            st.text("IP:")
            st.code(formatar_binario(sub_atual.network_address))
            st.text("Máscara:")
            st.code(formatar_binario(sub_atual.netmask))

except Exception as e:
    st.warning("Insira um bloco CIDR válido para iniciar a análise de capacidade.")
