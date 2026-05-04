import streamlit as st
import ipaddress

st.set_page_config(page_title="Calculadora de Redes Pro", page_icon="🌐", layout="wide")

def identificar_classe_real(ip_str):
    try:
        primeiro_octeto = int(ip_str.split('.')[0])
        if 1 <= primeiro_octeto <= 126:
            return "Classe A", 16777216, "255.0.0.0"
        elif 128 <= primeiro_octeto <= 191:
            return "Classe B", 65536, "255.255.0.0"
        elif 192 <= primeiro_octeto <= 223:
            return "Classe C", 256, "255.255.255.0"
        return "Especial", 0, "0.0.0.0"
    except:
        return "Inválido", 0, "0.0.0.0"

def formatar_binario(ip_ou_mask):
    return ".".join([bin(int(x))[2:].zfill(8) for x in str(ip_ou_mask).split('.')])

st.title("🌐 Calculadora de Redes")
st.markdown(f"**Desenvolvedor:** Richard Santos | **Foco:** Precisão Total de Classe")
st.divider()

# --- ENTRADA DE DADOS ---
col1, col2 = st.columns(2)
with col1:
    ip_input = st.text_input("Digite o IP (Ex: 9.6.0.0):", "9.6.0.0")
with col2:
    prefixo_alvo = st.number_input("Defina o Prefixo da Sub-rede (CIDR):", min_value=8, max_value=32, value=20)

try:
    nome_classe, cap_total, mask_padrao = identificar_classe_real(ip_input)
    ips_por_subrede = 2**(32 - prefixo_alvo)
    total_subredes = cap_total // ips_por_subrede if cap_total > 0 else 0

    # --- PAINEL DE CAPACIDADE (AGORA DESTRAVADO) ---
    st.subheader(f"📊 Diagnóstico de Capacidade: {nome_classe}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Classe Identificada", nome_classe)
    c2.metric("Sub-redes na Classe", f"{total_subredes:,}".replace(",", "."))
    c3.metric("Total de IPs da Classe", f"{cap_total:,}".replace(",", "."))

    st.divider()

    # --- DETALHES DA SUB-REDE ---
    st.subheader("🔍 Detalhes do Endereçamento")
    n_rede = st.number_input(f"Selecione a Sub-rede (1 a {total_subredes:,}):", min_value=1, max_value=total_subredes if total_subredes > 0 else 1, value=1)

    # Cálculo matemático para encontrar a sub-rede N sem travar
    ip_base_int = int(ipaddress.IPv4Address(ip_input.split('/')[0]))
    # Ajuste para garantir que comece do início da rede da classe se necessário
    ip_sub_int = ip_base_int + ((n_rede - 1) * ips_por_subrede)
    rede_atual = ipaddress.ip_network(f"{ipaddress.IPv4Address(ip_sub_int)}/{prefixo_alvo}", strict=False)

    res1, res2 = st.columns(2)
    with res1:
        st.success(f"**Máscara Resolvida: {rede_atual.netmask}**")
        st.write(f"📍 **ID de Rede:** `{rede_atual.network_address}`")
        st.write(f"✅ **Primeiro IP Válido:** `{rede_atual.network_address + 1}`")
        st.write(f"✅ **Último IP Válido:** `{rede_atual.broadcast_address - 1}`")
        st.write(f"📢 **Broadcast:** `{rede_atual.broadcast_address}`")
    
    with res2:
        st.markdown("### 🖥️ Estrutura de Bits")
        st.text("Binário do IP de Rede:")
        st.code(formatar_binario(rede_atual.network_address))
        st.text("Binário da Máscara:")
        st.code(formatar_binario(rede_atual.netmask))
        st.metric("Hosts Úteis nesta rede", f"{ips_por_subrede - 2:,}".replace(",", "."))

except Exception as e:
    st.error("Erro ao processar. Verifique se o IP digitado é válido.")
