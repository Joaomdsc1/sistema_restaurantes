import pandas as pd
import json
from datetime import datetime, timedelta
import os

class OrderManager:
    def __init__(self):
        self.orders_file = "orders.json"
        self.orders = self.load_orders()
        self.menu_df = self.load_menu()
    
    def load_menu(self):
        """Carrega o cardápio do arquivo CSV"""
        try:
            return pd.read_csv('cardapio.csv')
        except FileNotFoundError:
            print("❌ Erro: Arquivo cardapio.csv não encontrado!")
            return None
    
    def load_orders(self):
        """Carrega pedidos salvos do arquivo JSON"""
        if os.path.exists(self.orders_file):
            try:
                with open(self.orders_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_orders(self):
        """Salva pedidos no arquivo JSON"""
        try:
            with open(self.orders_file, 'w', encoding='utf-8') as f:
                json.dump(self.orders, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Erro ao salvar pedidos: {e}")
    
    def create_order(self, phone, items, total, estimated_time):
        """Cria um novo pedido"""
        order = {
            'id': len(self.orders) + 1,
            'phone': phone,
            'items': items,
            'total': total,
            'estimated_time': estimated_time,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'estimated_delivery': (datetime.now() + timedelta(minutes=estimated_time)).isoformat(),
            'address': None,
            'notes': None
        }
        
        self.orders.append(order)
        self.save_orders()
        
        print(f"✅ Pedido #{order['id']} criado para {phone}")
        return order
    
    def get_order(self, order_id):
        """Busca um pedido pelo ID"""
        for order in self.orders:
            if order['id'] == order_id:
                return order
        return None
    
    def update_order_status(self, order_id, status):
        """Atualiza o status de um pedido"""
        order = self.get_order(order_id)
        if order:
            order['status'] = status
            self.save_orders()
            print(f"✅ Status do pedido #{order_id} atualizado para: {status}")
            return True
        return False
    
    def get_pending_orders(self):
        """Retorna todos os pedidos pendentes"""
        return [order for order in self.orders if order['status'] == 'pending']
    
    def get_orders_by_phone(self, phone):
        """Retorna todos os pedidos de um telefone específico"""
        return [order for order in self.orders if order['phone'] == phone]
    
    def get_today_orders(self):
        """Retorna todos os pedidos de hoje"""
        today = datetime.now().date()
        today_orders = []
        
        for order in self.orders:
            order_date = datetime.fromisoformat(order['created_at']).date()
            if order_date == today:
                today_orders.append(order)
        
        return today_orders
    
    def get_order_summary(self):
        """Retorna um resumo dos pedidos"""
        total_orders = len(self.orders)
        pending_orders = len(self.get_pending_orders())
        today_orders = len(self.get_today_orders())
        
        total_revenue = sum(order['total'] for order in self.orders)
        today_revenue = sum(order['total'] for order in self.get_today_orders())
        
        return {
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'today_orders': today_orders,
            'total_revenue': total_revenue,
            'today_revenue': today_revenue
        }
    
    def format_order_for_display(self, order):
        """Formata um pedido para exibição"""
        items_text = ""
        for item in order['items']:
            items_text += f"• #{item['numero']} - {item['nome']} - R$ {item['preco']:.2f}\n"
        
        created_time = datetime.fromisoformat(order['created_at']).strftime("%d/%m/%Y %H:%M")
        estimated_delivery = datetime.fromisoformat(order['estimated_delivery']).strftime("%d/%m/%Y %H:%M")
        
        return f"""
🍽️ **Pedido #{order['id']}**
📱 **Telefone:** {order['phone']}
🕒 **Criado em:** {created_time}
⏱️ **Tempo estimado:** {order['estimated_time']} min
🚚 **Entrega estimada:** {estimated_delivery}
📊 **Status:** {order['status'].upper()}

**Itens:**
{items_text}
💰 **Total: R$ {order['total']:.2f}**
"""
    
    def export_orders_to_csv(self, filename="orders_export.csv"):
        """Exporta todos os pedidos para CSV"""
        if not self.orders:
            print("❌ Nenhum pedido para exportar")
            return False
        
        try:
            # Prepara dados para exportação
            export_data = []
            for order in self.orders:
                for item in order['items']:
                    export_data.append({
                        'order_id': order['id'],
                        'phone': order['phone'],
                        'item_number': item['numero'],
                        'item_name': item['nome'],
                        'item_price': item['preco'],
                        'order_total': order['total'],
                        'status': order['status'],
                        'created_at': order['created_at'],
                        'estimated_time': order['estimated_time']
                    })
            
            df = pd.DataFrame(export_data)
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"✅ Pedidos exportados para {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao exportar pedidos: {e}")
            return False
    
    def get_menu_statistics(self):
        """Retorna estatísticas dos itens mais pedidos"""
        if not self.orders:
            return {}
        
        item_counts = {}
        item_revenue = {}
        
        for order in self.orders:
            for item in order['items']:
                item_num = item['numero']
                item_name = item['nome']
                
                if item_num not in item_counts:
                    item_counts[item_num] = {'name': item_name, 'count': 0, 'revenue': 0}
                
                item_counts[item_num]['count'] += 1
                item_counts[item_num]['revenue'] += item['preco']
        
        # Ordena por quantidade
        sorted_items = sorted(item_counts.items(), key=lambda x: x[1]['count'], reverse=True)
        
        return dict(sorted_items)
    
    def cleanup_old_orders(self, days=30):
        """Remove pedidos antigos (mais de X dias)"""
        cutoff_date = datetime.now() - timedelta(days=days)
        original_count = len(self.orders)
        
        self.orders = [
            order for order in self.orders 
            if datetime.fromisoformat(order['created_at']) > cutoff_date
        ]
        
        removed_count = original_count - len(self.orders)
        if removed_count > 0:
            self.save_orders()
            print(f"✅ {removed_count} pedidos antigos removidos")
        
        return removed_count

# Função para testar o sistema
def test_order_manager():
    """Função para testar o sistema de gerenciamento de pedidos"""
    manager = OrderManager()
    
    # Simula alguns pedidos
    test_items = [
        {'numero': 1, 'nome': 'X-Burger', 'preco': 25.90, 'tempo_estimado_minutos': 15},
        {'numero': 15, 'nome': 'Refrigerante', 'preco': 6.50, 'tempo_estimado_minutos': 2}
    ]
    
    # Cria pedido de teste
    order = manager.create_order(
        phone="11999999999",
        items=test_items,
        total=32.40,
        estimated_time=15
    )
    
    print("📊 Resumo do sistema:")
    summary = manager.get_order_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\n🍽️ Estatísticas do menu:")
    stats = manager.get_menu_statistics()
    for item_num, data in list(stats.items())[:5]:
        print(f"  #{item_num} - {data['name']}: {data['count']} pedidos, R$ {data['revenue']:.2f}")

if __name__ == "__main__":
    test_order_manager() 