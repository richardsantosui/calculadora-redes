import streamlit as st
import ipaddress

st.set_page_config(page_title="Capacidade Máxima IPv4", page_icon="♾️", layout="wide")

def identificar_classe_detalhada(ip):
    primeiro_octeto = int(str(ip).split('.')[0])
    if 1 <= primeiro_octeto <= 126:
        return "Classe A", "Redes de grande porte (Escala Global)."
    elif 128 <= primeiro_octeto <= 191:
        return "Classe B", "Redes de médio porte (Corporativas)."
    elif 192 <= primeiro_octeto <= 223:
        return "Classe C", "Redes de pequeno porte (Domésticas/Locais)."
    return "Classe Especial", "Uso reservado ou multicast."

st.title("♾️ Calculadora de Capacidade Máxima de Endereçamento")
st.markdown(f"**Desenvolvedor:** Richard Santos | **Foco:** Precisão em Larga Escala")
st.divider()

col1, col2 = st.columns(2)
with col1:
    entrada_ip = st.text_input("Bloco CIDR de Origem:", "10.0.0.0/8")
with col2:
    prefixo_alvo = st.number_input("Prefixo de Destino (CIDR):", min_value=1, max_value=32, value=24)

try:
    # Usamos o objeto ip_network para gerenciar os bits
    rede_pai = ipaddress.ip_network(entrada_ip, strict=False)
    classe, desc = identificar_classe_detalhada(rede_pai.network_address)
    
    if prefixo_alvo < rede_pai.prefixlen:
        st.error(f"Erro de Hierarquia: O prefixo alvo /{prefixo_alvo} não cabe dentro de /{rede_pai.prefixlen}")
    else:
        # CÁLCULOS SEM LIMITES DEBITS
        diff_bits_redes = prefixo_alvo - rede_pai.prefixlen
        diff_bits_hosts = 32 - prefixo_alvo
        
        # Usamos potências de 2 puras para garantir a capacidade total
        total_subredes = 2**diff_bits_redes
        total_ips_por_rede = 2**diff_bits_hosts
        total_ips_no_bloco = 2**(32 - rede_pai.prefixlen)

        # --- EXIBIÇÃO DE CAPACIDADE SEM TRAVAMENTO ---
        st.subheader("📊 Relatório de Potencial de Rede")
        
        c1, c2, c3 = st.columns(3)
        # Exibimos os números formatados com separador de milhar para facilitar a leitura
        c1.metric("Classe Identificada", classe)
        c2.metric("Sub-redes Possíveis", f"{total_subredes:,}".replace(",", "."))
        c3.metric("IPs Totais no Bloco", f"{total_ips_no_bloco:,}".replace(",", "."))

        st.info(f"**Análise Técnica da {classe}:** {desc}")
        
        # --- BOX DE TOTALIZAÇÃO FINAL ---
        st.success(f"### 🛡️ Capacidade Total Destravada: {total_ips_no_bloco:,} endereços IP identificados no bloco original.".replace(",", "."))

        st.divider()

        # Localizador Rápido
        st.subheader("🔍 Localizador de Endereço")
        n_rede = st.number_input(f"Selecione a sub-rede (1 a {total_subredes:,}):", min_value=1, max_value=total_subredes, value=1)
        
        # Matemática de salto para evitar processamento de listas pesadas
        salto = total_ips_por_rede
        ip_calculado = ipaddress.IPv4Address(int(rede_pai.network_address) + ((n_rede - 1) * salto))
        sub_atual = ipaddress.ip_network(f"{ip_calculado}/{prefixo_alvo}")

        # Resultados detalhados
        res1, res2 = st.columns(2)
        with res1:
            st.write(f"**Sub-rede Selecionada:** `{sub_atual}`")
            st.write(f"**Máscara de Rede:** `{sub_atual.netmask}`")
        with res2:
            st.write(f"**IP de Broadcast:** `{sub_atual.broadcast_address}`")
            st.write(f"**Hosts Úteis:** `{total_ips_por_rede - 2:,}`".replace(",", "."))

except Exception:
    st.warning("Aguardando definição de bloco CIDR válido para cálculo de capacidade.")
