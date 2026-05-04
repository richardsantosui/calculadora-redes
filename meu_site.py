import streamlit as st
import ipaddress
import math

st.set_page_config(page_title="Capacidade Total IPv4", page_icon="🧮", layout="wide")

def identificar_classe_detalhada(ip):
    """Retorna a classe do IP e uma breve explicação técnica."""
    primeiro_octeto = int(str(ip).split('.')[0])
    if 1 <= primeiro_octeto <= 126:
        return "Classe A", "Redes de grande porte. O primeiro octeto define a rede."
    elif 128 <= primeiro_octeto <= 191:
        return "Classe B", "Redes de médio porte. Os dois primeiros octetos definem a rede."
    elif 192 <= primeiro_octeto <= 223:
        return "Classe C", "Redes de pequeno porte. Os três primeiros octetos definem a rede."
    elif 224 <= primeiro_octeto <= 239:
        return "Classe D", "Multicast (Uso especial)."
    else:
        return "Classe E", "Experimental/Reservada."

def formatar_binario(valor):
    return ".".join([bin(int(x))[2:].zfill(8) for x in str(valor).split('.')])

st.title("🧮 Calculadora de Capacidade Total de Redes")
st.markdown(f"**Desenvolvido por:** Richard Santos | **Status:** Alta Performance")
st.divider()

col1, col2 = st.columns(2)
with col1:
    entrada_ip = st.text_input("Bloco CIDR Principal (Ex: 10.0.0.0/8):", "9.6.0.0/16")
with col2:
    prefixo_alvo = st.number_input("Novo Prefixo das Sub-redes (CIDR):", min_value=1, max_value=32, value=20)

try:
    rede_pai = ipaddress.ip_network(entrada_ip, strict=False)
    classe, desc = identificar_classe_detalhada(rede_pai.network_address)
    
    if prefixo_alvo < rede_pai.prefixlen:
        st.error(f"O prefixo alvo (/{prefixo_alvo}) deve ser maior que o original (/{rede_pai.prefixlen}).")
    else:
        # Cálculos de capacidade
        total_subredes = 2**(prefixo_alvo - rede_pai.prefixlen)
        ips_por_subrede = 2**(32 - prefixo_alvo)
        hosts_uteis = ips_por_subrede - 2 if ips_por_subrede > 2 else 0
        total_ips_global = total_subredes * ips_por_subrede

        # --- PAINEL DE MÉTRICAS GLOBAIS ---
        st.subheader("🌐 Relatório de Capacidade Global")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Classe do IP", classe)
        m2.metric("Sub-redes Possíveis", f"{total_subredes:,}")
        m3.metric("Hosts Úteis / Rede", f"{hosts_uteis:,}")
        m4.metric("Total IPs no Bloco", f"{total_ips_global:,}")
        
        st.info(f"**Explicação da {classe}:** {desc}")
        st.divider()

        # --- NAVEGAÇÃO DE ALTA PERFORMANCE ---
        st.subheader(f"🔍 Explorador de Segmentação")
        
        # Trocamos o slider por número para não travar em redes grandes
        n_rede = st.number_input(f"Digite qual sub-rede deseja ver (1 até {total_subredes:,}):", 
                                 min_value=1, max_value=total_subredes, value=1)

        # Cálculo matemático direto (Otimizado)
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
    st.warning("Insira um bloco CIDR válido para iniciar (Ex: 10.0.0.0/8).")
