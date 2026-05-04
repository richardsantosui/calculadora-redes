import streamlit as st
import ipaddress

# Configuração de Interface Profissional
st.set_page_config(page_title="Calculadora de Redes", page_icon="🌐", layout="wide")

# --- FUNÇÕES TÉCNICAS ---
def identificar_classe_real(ip_str):
    try:
        primeiro_octeto = int(ip_str.split('.')[0])
        if 1 <= primeiro_octeto <= 126:
            return "Classe A", 16777216, 8, "Redes de grande porte (Escala Global)."
        elif 128 <= primeiro_octeto <= 191:
            return "Classe B", 65536, 16, "Redes de médio porte (Corporativas)."
        elif 192 <= primeiro_octeto <= 223:
            return "Classe C", 256, 24, "Redes de pequeno porte (Domésticas/Locais)."
        return "Especial", 0, 0, "Uso reservado ou multicast."
    except:
        return "Inválido", 0, 0, ""

def formatar_binario(ip_ou_mask):
    return ".".join([bin(int(x))[2:].zfill(8) for x in str(ip_ou_mask).split('.')])

# --- CABEÇALHO ---
st.title("🌐 Calculadora de Redes")
st.markdown(f"**Desenvolvedor:** Richard Santos | **Foco:** Precisão Total e Validação de Escopo")
st.divider()

# --- ENTRADA DE DADOS ---
col_input1, col_input2 = st.columns(2)
with col_input1:
    ip_input = st.text_input("Digite o Endereço IP (Ex: 10.0.0.0):", "9.6.0.0")
with col_input2:
    prefixo_alvo = st.number_input("Defina o Prefixo da Sub-rede (CIDR):", min_value=1, max_value=32, value=20)

try:
    nome_classe, cap_total, pref_minimo, desc_classe = identificar_classe_real(ip_input)
    
    # --- VALIDAÇÃO DE LÓGICA DE REDE ---
    if prefixo_alvo < pref_minimo:
        st.error(f"❌ **Divisão Impossível:** Para a **{nome_classe}**, o prefixo da sub-rede deve ser no mínimo **/{pref_minimo}**.")
        st.warning(f"O prefixo escolhido (/{prefixo_alvo}) tentaria criar uma rede maior do que a capacidade total da própria Classe.")
    else:
        # Cálculos de Capacidade
        ips_por_subrede = 2**(32 - prefixo_alvo)
        total_subredes = cap_total // ips_por_subrede if cap_total > 0 else 0

        # --- PAINEL DE MÉTRICAS GLOBAIS ---
        st.subheader(f"📊 Diagnóstico de Capacidade: {nome_classe}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Classe Identificada", nome_classe)
        c2.metric("Sub-redes na Classe", f"{total_subredes:,}".replace(",", "."))
        c3.metric("Total de IPs da Classe", f"{cap_total:,}".replace(",", "."))
        
        st.info(f"**Análise Técnica:** {desc_classe}")
        st.divider()

        # --- DETALHES DA SUB-REDE SELECIONADA ---
        st.subheader("🔍 Detalhes do Endereçamento")
        
        # LINHA CORRIGIDA (Abaixo):
        max_redes = total_subredes if total_subredes > 0 else 1
        n_rede = st.number_input(f"Selecione a Sub-rede para análise (1 a {max_redes:,}):", min_value=1, max_value=max_redes, value=1)

        # Cálculo matemático direto
        ip_base_int = int(ipaddress.IPv4Address(ip_input.split('/')[0]))
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
            st.markdown("### 🖥️ Estrutura de Bits & Hosts")
            st.metric("Hosts Úteis nesta rede", f"{ips_por_subrede - 2:,}".replace(",", "."))
            st.text("Binário do IP de Rede:")
            st.code(formatar_binario(rede_atual.network_address))
            st.text("Binário da Máscara:")
            st.code(formatar_binario(rede_atual.netmask))

except Exception as e:
    st.error("⚠️ Erro de processamento. Certifique-se de inserir um endereço IP válido no formato X.X.X.X")
