import streamlit as st
import ipaddress

# Configuração de Interface
st.set_page_config(page_title="Calculadora de Redes", page_icon="🌐", layout="wide")

def identificar_classe_detalhada(ip):
    primeiro_octeto = int(str(ip).split('.')[0])
    if 1 <= primeiro_octeto <= 126:
        return "Classe A", "Redes de grande porte (Escala Global)."
    elif 128 <= primeiro_octeto <= 191:
        return "Classe B", "Redes de médio porte (Corporativas)."
    elif 192 <= primeiro_octeto <= 223:
        return "Classe C", "Redes de pequeno porte (Domésticas/Locais)."
    return "Classe Especial", "Uso reservado ou multicast."

# --- NOVO NOME APLICADO ---
st.title("🌐 Calculadora de Redes")
st.markdown(f"**Desenvolvedor:** Richard Santos | **Foco:** Precisão e Alta Performance")
st.divider()

col1, col2 = st.columns(2)
with col1:
    entrada_ip = st.text_input("Bloco CIDR de Origem (Ex: 10.0.0.0/8):", "9.6.0.0/16")
with col2:
    prefixo_alvo = st.number_input("Novo Prefixo das Sub-redes (CIDR):", min_value=1, max_value=32, value=20)

try:
    rede_pai = ipaddress.ip_network(entrada_ip, strict=False)
    classe, desc = identificar_classe_detalhada(rede_pai.network_address)
    
    if prefixo_alvo < rede_pai.prefixlen:
        st.error(f"Erro: O prefixo alvo /{prefixo_alvo} é menor que o bloco original /{rede_pai.prefixlen}")
    else:
        # CÁLCULOS TÉCNICOS
        total_subredes = 2**(prefixo_alvo - rede_pai.prefixlen)
        ips_por_subrede = 2**(32 - prefixo_alvo)
        # O Total do Bloco é baseado na máscara de ORIGEM
        total_ips_bloco_original = 2**(32 - rede_pai.prefixlen)

        # --- EXIBIÇÃO DE MÉTRICAS ---
        st.subheader("📊 Relatório de Capacidade")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Classe Identificada", classe)
        c2.metric("Sub-redes Possíveis", f"{total_subredes:,}".replace(",", "."))
        c3.metric("Total de IPs no Bloco", f"{total_ips_bloco_original:,}".replace(",", "."))

        st.info(f"**Análise da {classe}:** {desc}")
        
        st.divider()

        # --- NAVEGAÇÃO ---
        st.subheader("🔍 Detalhes por Sub-rede")
        n_rede = st.number_input(f"Selecione a sub-rede para análise (1 a {total_subredes:,}):", 
                                 min_value=1, max_value=total_subredes, value=1)
        
        # Cálculo de salto para performance
        salto = ips_por_subrede
        ip_calculado = ipaddress.IPv4Address(int(rede_pai.network_address) + ((n_rede - 1) * salto))
        sub_atual = ipaddress.ip_network(f"{ip_calculado}/{prefixo_alvo}")

        res1, res2 = st.columns(2)
        with res1:
            st.success(f"**Máscara Resolvida: {sub_atual.netmask}**")
            st.write(f"- **ID de Rede:** `{sub_atual.network_address}`")
            st.write(f"- **Broadcast:** `{sub_atual.broadcast_address}`")
        with res2:
            st.write(f"**Hosts Úteis:** `{ips_por_subrede - 2:,}`".replace(",", "."))
            st.write(f"- **Faixa:** `{sub_atual.network_address + 1}` até `{sub_atual.broadcast_address - 1}`")

except Exception:
    st.warning("Aguardando entrada de dados válida.")
