import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="🍽️ Cardápio do Restaurante",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF6B6B;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #FF6B6B;
    }
    .price {
        font-size: 1.2rem;
        font-weight: bold;
        color: #28a745;
    }
    .time {
        font-size: 0.9rem;
        color: #6c757d;
        font-style: italic;
    }
    .category-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #495057;
        margin: 1rem 0 0.5rem 0;
        border-bottom: 2px solid #FF6B6B;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def load_menu():
    """Carrega o cardápio do arquivo CSV"""
    try:
        df = pd.read_csv('cardapio.csv')
        return df
    except FileNotFoundError:
        st.error("Arquivo cardapio.csv não encontrado!")
        return None

def categorize_menu(df):
    """Categoriza os itens do menu"""
    categories = {
        'Hambúrgueres': [1, 2, 3],
        'Pizzas': [4, 5, 6],
        'Massas': [7, 8],
        'Saladas': [9, 10],
        'Sopas': [11, 12],
        'Acompanhamentos': [13, 14],
        'Bebidas': [15, 16, 17],
        'Sobremesas': [18, 19, 20]
    }
    
    categorized = {}
    for category, numbers in categories.items():
        categorized[category] = df[df['numero'].isin(numbers)]
    
    return categorized

def main():
    # Header principal
    st.markdown('<h1 class="main-header">🍽️ Cardápio do Restaurante</h1>', unsafe_allow_html=True)
    
    # Informações do restaurante
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📞 **WhatsApp:** (11) 99999-9999")
    with col2:
        st.info("🕒 **Horário:** Seg-Sex: 11h-22h | Sáb-Dom: 12h-23h")
    with col3:
        st.info("📍 **Endereço:** Rua das Flores, 123 - Centro")
    
    st.markdown("---")
    
    # Carregar cardápio
    df = load_menu()
    if df is None:
        return
    
    # Categorizar menu
    categorized_menu = categorize_menu(df)
    
    # Exibir cardápio por categorias
    for category, items in categorized_menu.items():
        if not items.empty:
            st.markdown(f'<h2 class="category-header">{category}</h2>', unsafe_allow_html=True)
            
            # Criar colunas para os itens
            cols = st.columns(3)
            for idx, (_, item) in enumerate(items.iterrows()):
                col_idx = idx % 3
                with cols[col_idx]:
                    st.markdown(f"""
                    <div class="card">
                        <h3>#{item['numero']} - {item['nome']}</h3>
                        <p>{item['descricao']}</p>
                        <p class="price">R$ {item['preco']:.2f}</p>
                        <p class="time">⏱️ {item['tempo_estimado_minutos']} min</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Instruções para pedido
    st.markdown("---")
    st.markdown("### 📱 Como fazer seu pedido:")
    st.markdown("""
    1. **Escolha os números dos pratos** que deseja no cardápio acima
    2. **Envie uma mensagem no WhatsApp** para (11) 99999-9999
    3. **Digite apenas os números** dos pratos (ex: 1, 3, 15)
    4. **Confirme seu pedido** e receba o tempo estimado de entrega
    """)
    
    # Exemplo de pedido
    with st.expander("💡 Exemplo de pedido"):
        st.markdown("""
        **Cliente:** 1, 3, 15
        
        **Bot:** 
        🍽️ **Seu pedido:**
        • #1 - X-Burger - R$ 25,90
        • #3 - X-Bacon - R$ 32,00  
        • #15 - Refrigerante - R$ 6,50
        
        **Total: R$ 64,40**
        
        Digite mais números para adicionar itens ou envie "ENVIAR" para finalizar.
        
        **Cliente:** ENVIAR
        
        **Bot:** 
        ✅ **Pedido confirmado!**
        ⏱️ **Tempo estimado:** 20 minutos
        📍 **Endereço de entrega:** [será solicitado]
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6c757d;'>
        <p>🍽️ Sistema de Pedidos via WhatsApp | Desenvolvido com ❤️</p>
        <p>Última atualização: {}</p>
    </div>
    """.format(datetime.now().strftime("%d/%m/%Y %H:%M")), unsafe_allow_html=True)

if __name__ == "__main__":
    main() 