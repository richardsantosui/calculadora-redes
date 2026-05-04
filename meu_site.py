import streamlit as st
import ipaddress

st.set_page_config(page_title="Calculadora de Redes", page_icon="🌐", layout="wide")

def calcular_capacidade_real(ip_str):
    """Calcula a capacidade total baseada na classe real do IP (A, B ou C)."""
    primeiro_octeto = int(ip_str.split('.')[0])
    if 1 <= primeiro_octeto <= 126:
        return 16777216, "Classe A"
    elif 128 <= primeiro_octeto <= 191:
        return 65536, "Classe B"
    elif 192 <= primeiro_octeto <= 223:
        return 256, "Classe C"
    return 0, "Especial"

st.title("🌐 Calculadora de Redes")
st.markdown(f"**Desenvolvedor:** Richard Santos | **Foco:** Precisão de Bloco")
st.divider()

col1, col2 = st.columns(2)
with col1:
    # Removemos o /16 fixo para deixar o usuário definir a rede de origem
    entrada_ip = st.text_input("Endereço IP de Origem (Ex: 9.0.0.0):", "9.6.0.0")
with col2:
    prefixo_alvo = st.number_input("Prefixo das Sub-redes (CIDR):", min_value=8, max_value=32, value=20)

try:
    # Identifica a capacidade real do IP digitado
    capacidade_total, classe = calcular_capacidade_real(entrada_ip)
    
    # Criamos a rede baseada no prefixo alvo para os detalhes
    ip_puro = entrada_ip.split('/')[0]
    
    # --- PAINEL DE MÉTRICAS ---
    st.subheader(f"📊 Relatório de Capacidade - {classe}")
    c1, c2, c3 = st.columns(3)
    
    # Cálculo de quantas sub-redes desse tamanho cabem na classe inteira
    ips_por_subrede = 2**(32 - prefixo_alvo)
    subredes_na_classe = capacidade_total // ips_por_subrede

    c1.metric("Classe Identificada", classe)
    c2.metric("Sub-redes Possíveis na Classe", f"{subredes_na_classe:,}".replace(",", "."))
    c3.metric("Total de IPs da Classe", f"{capacidade_total:,}".replace(",", "."))

    st.divider()

    # --- NAVEGAÇÃO ---
    st.subheader("🔍 Detalhes por Sub-rede")
    n_rede = st.number_input(f"Selecione a sub-rede (1 a {subredes_na_classe:,}):", 
                             min_value=1, max_value=subredes_na_classe, value=1)
    
    # Cálculo do IP exato da sub-rede selecionada
    ip_base_int = int(ipaddress.IPv4Address(ip_puro))
    ip_sub_int = ip_base_int + ((n_rede - 1) * ips_por_subrede)
    sub_atual = ipaddress.ip_network(f"{ipaddress.IPv4Address(ip_sub_int)}/{prefixo_alvo}", strict=False)

    res1, res2 = st.columns(2)
    with res1:
        st.success(f"**Máscara Resolvida: {sub_atual.netmask}**")
        st.write(f"- **ID de Rede:** `{sub_atual.network_address}`")
        st.write(f"- **Primeiro IP Válido:** `{sub_atual.network_address + 1}`")
        st.write(f"- **Último IP Válido:** `{sub_atual.broadcast_address - 1}`")
        st.write(f"- **Broadcast:** `{sub_atual.broadcast_address}`")
    with res2:
        st.markdown(f"### Estatísticas da Rede #{n_rede}")
        st.metric("Hosts Úteis nesta Sub-rede", f"{ips_por_subrede - 2:,}".replace(",", "."))

except Exception as e:
    st.warning("Insira um endereço IP válido.")
