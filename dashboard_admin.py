import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from order_manager import OrderManager
import json

# Configuração da página
st.set_page_config(
    page_title="📊 Dashboard Administrativo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #2E86AB;
    }
    .status-pending {
        color: #ffc107;
        font-weight: bold;
    }
    .status-completed {
        color: #28a745;
        font-weight: bold;
    }
    .status-cancelled {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def load_order_manager():
    """Carrega o gerenciador de pedidos"""
    return OrderManager()

def main():
    # Header principal
    st.markdown('<h1 class="main-header">📊 Dashboard Administrativo</h1>', unsafe_allow_html=True)
    
    # Carrega o gerenciador de pedidos
    order_manager = load_order_manager()
    
    # Sidebar para filtros
    st.sidebar.title("🔍 Filtros")
    
    # Filtro de status
    status_filter = st.sidebar.selectbox(
        "Status do Pedido",
        ["Todos", "Pendente", "Em Preparo", "Concluído", "Cancelado"]
    )
    
    # Filtro de data
    date_filter = st.sidebar.date_input(
        "Data",
        value=datetime.now().date(),
        max_value=datetime.now().date()
    )
    
    # Métricas principais
    st.subheader("📈 Métricas Principais")
    
    summary = order_manager.get_order_summary()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total de Pedidos",
            value=summary['total_orders'],
            delta=summary['today_orders']
        )
    
    with col2:
        st.metric(
            label="Pedidos Pendentes",
            value=summary['pending_orders']
        )
    
    with col3:
        st.metric(
            label="Pedidos Hoje",
            value=summary['today_orders']
        )
    
    with col4:
        st.metric(
            label="Receita Total",
            value=f"R$ {summary['total_revenue']:.2f}",
            delta=f"R$ {summary['today_revenue']:.2f}"
        )
    
    # Gráficos
    st.subheader("📊 Análises")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de pedidos por status
        if order_manager.orders:
            status_counts = {}
            for order in order_manager.orders:
                status = order['status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            if status_counts:
                fig_status = px.pie(
                    values=list(status_counts.values()),
                    names=list(status_counts.keys()),
                    title="Pedidos por Status"
                )
                st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        # Gráfico de receita por dia (últimos 7 dias)
        if order_manager.orders:
            # Agrupa pedidos por data
            daily_revenue = {}
            for order in order_manager.orders:
                order_date = datetime.fromisoformat(order['created_at']).date()
                if order_date not in daily_revenue:
                    daily_revenue[order_date] = 0
                daily_revenue[order_date] += order['total']
            
            # Últimos 7 dias
            last_7_days = []
            for i in range(7):
                date = datetime.now().date() - timedelta(days=i)
                last_7_days.append(date)
            
            revenue_data = []
            for date in reversed(last_7_days):
                revenue_data.append({
                    'Data': date.strftime('%d/%m'),
                    'Receita': daily_revenue.get(date, 0)
                })
            
            if revenue_data:
                df_revenue = pd.DataFrame(revenue_data)
                fig_revenue = px.line(
                    df_revenue,
                    x='Data',
                    y='Receita',
                    title="Receita dos Últimos 7 Dias"
                )
                st.plotly_chart(fig_revenue, use_container_width=True)
    
    # Itens mais pedidos
    st.subheader("🍽️ Itens Mais Pedidos")
    
    stats = order_manager.get_menu_statistics()
    if stats:
        # Cria DataFrame para o gráfico
        items_data = []
        for item_num, data in list(stats.items())[:10]:  # Top 10
            items_data.append({
                'Item': f"#{item_num} - {data['name']}",
                'Quantidade': data['count'],
                'Receita': data['revenue']
            })
        
        df_items = pd.DataFrame(items_data)
        
        fig_items = px.bar(
            df_items,
            x='Quantidade',
            y='Item',
            orientation='h',
            title="Top 10 Itens Mais Pedidos"
        )
        st.plotly_chart(fig_items, use_container_width=True)
    
    # Lista de pedidos
    st.subheader("📋 Pedidos Recentes")
    
    # Filtra pedidos
    filtered_orders = order_manager.orders.copy()
    
    if status_filter != "Todos":
        status_map = {
            "Pendente": "pending",
            "Em Preparo": "preparing", 
            "Concluído": "completed",
            "Cancelado": "cancelled"
        }
        filtered_orders = [
            order for order in filtered_orders 
            if order['status'] == status_map[status_filter]
        ]
    
    # Filtra por data
    filtered_orders = [
        order for order in filtered_orders
        if datetime.fromisoformat(order['created_at']).date() == date_filter
    ]
    
    if filtered_orders:
        # Ordena por data de criação (mais recente primeiro)
        filtered_orders.sort(key=lambda x: x['created_at'], reverse=True)
        
        for order in filtered_orders[:10]:  # Mostra apenas os 10 mais recentes
            with st.expander(f"Pedido #{order['id']} - {order['phone']} - R$ {order['total']:.2f}"):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write("**Itens:**")
                    for item in order['items']:
                        st.write(f"• #{item['numero']} - {item['nome']} - R$ {item['preco']:.2f}")
                
                with col2:
                    created_time = datetime.fromisoformat(order['created_at']).strftime("%d/%m %H:%M")
                    st.write(f"**Criado:** {created_time}")
                    st.write(f"**Tempo:** {order['estimated_time']} min")
                
                with col3:
                    # Status com cores
                    status_class = f"status-{order['status']}"
                    st.markdown(f'<p class="{status_class}">**Status:** {order["status"].upper()}</p>', 
                              unsafe_allow_html=True)
                    
                    # Botões de ação
                    if order['status'] == 'pending':
                        if st.button(f"Em Preparo #{order['id']}", key=f"prep_{order['id']}"):
                            order_manager.update_order_status(order['id'], 'preparing')
                            st.rerun()
                    
                    elif order['status'] == 'preparing':
                        if st.button(f"Concluído #{order['id']}", key=f"comp_{order['id']}"):
                            order_manager.update_order_status(order['id'], 'completed')
                            st.rerun()
                    
                    if st.button(f"Cancelar #{order['id']}", key=f"cancel_{order['id']}"):
                        order_manager.update_order_status(order['id'], 'cancelled')
                        st.rerun()
    else:
        st.info("Nenhum pedido encontrado com os filtros aplicados.")
    
    # Ações administrativas
    st.subheader("⚙️ Ações Administrativas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Exportar Pedidos (CSV)"):
            if order_manager.export_orders_to_csv():
                st.success("Pedidos exportados com sucesso!")
            else:
                st.error("Erro ao exportar pedidos.")
    
    with col2:
        if st.button("🧹 Limpar Pedidos Antigos"):
            removed = order_manager.cleanup_old_orders(days=30)
            st.success(f"{removed} pedidos antigos removidos!")
    
    with col3:
        if st.button("🔄 Atualizar Dashboard"):
            st.rerun()
    
    # Informações do sistema
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ Informações do Sistema")
    st.sidebar.write(f"**Total de Pedidos:** {summary['total_orders']}")
    st.sidebar.write(f"**Receita Total:** R$ {summary['total_revenue']:.2f}")
    st.sidebar.write(f"**Última Atualização:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")

if __name__ == "__main__":
    main() 