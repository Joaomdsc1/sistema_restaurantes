"""
Arquivo de configuração do sistema de restaurante
Personalize as configurações aqui
"""

# Configurações do Restaurante
RESTAURANTE_NOME = "Restaurante Delícias"
RESTAURANTE_TELEFONE = "(11) 99999-9999"
RESTAURANTE_ENDERECO = "Rua das Flores, 123 - Centro"
RESTAURANTE_HORARIO = "Seg-Sex: 11h-22h | Sáb-Dom: 12h-23h"

# Configurações do WhatsApp
WHATSAPP_NUMERO = "11999999999"  # Número do WhatsApp do restaurante
WHATSAPP_MENSAGEM_BOAS_VINDAS = """🍽️ **Bem-vindo ao {}!**

Para fazer seu pedido, digite os números dos pratos desejados.
Exemplo: 1, 3, 15

Para ver o cardápio completo, acesse: [link do Streamlit]

Digite 'ENVIAR' quando terminar seu pedido."""

# Configurações do Sistema
TEMPO_ENTREGA_EXTRA = 5  # Minutos extras para entrega
TEMPO_PREPARO_MINIMO = 10  # Tempo mínimo de preparo
TEMPO_PREPARO_MAXIMO = 30  # Tempo máximo de preparo

# Configurações das Portas
PORTA_CARDAPIO = 8501
PORTA_DASHBOARD = 8502

# Configurações de Cores (CSS)
CORES = {
    'primaria': '#FF6B6B',
    'secundaria': '#2E86AB',
    'sucesso': '#28a745',
    'aviso': '#ffc107',
    'erro': '#dc3545',
    'texto': '#495057',
    'fundo': '#f8f9fa'
}

# Configurações de Categorias do Menu
CATEGORIAS_MENU = {
    'Hambúrgueres': [1, 2, 3],
    'Pizzas': [4, 5, 6],
    'Massas': [7, 8],
    'Saladas': [9, 10],
    'Sopas': [11, 12],
    'Acompanhamentos': [13, 14],
    'Bebidas': [15, 16, 17],
    'Sobremesas': [18, 19, 20]
}

# Configurações de Status dos Pedidos
STATUS_PEDIDOS = {
    'pending': 'Pendente',
    'preparing': 'Em Preparo',
    'completed': 'Concluído',
    'cancelled': 'Cancelado'
}

# Configurações de Mensagens
MENSAGENS = {
    'pedido_confirmado': """✅ **Pedido confirmado!**

🍽️ **Itens do pedido:**
{itens}

💰 **Total: R$ {total:.2f}**
⏱️ **Tempo estimado:** {tempo} minutos
📍 **Endereço de entrega:** [será solicitado]

📞 **Para dúvidas:** {telefone}
🕒 **Pedido realizado em:** {data_hora}

Obrigado por escolher nosso restaurante! 🍽️""",

    'pedido_parcial': """🍽️ **Seu pedido:**
{itens}

**Total: R$ {total:.2f}**

Digite mais números para adicionar itens ou envie 'ENVIAR' para finalizar.""",

    'item_nao_encontrado': "❌ Item #{numero} não encontrado no cardápio. Verifique o número e tente novamente.",

    'pedido_vazio': "❌ Nenhum item no pedido. Digite os números dos pratos desejados.",

    'erro_processamento': "❌ Erro ao processar pedido. Tente novamente ou entre em contato conosco."
}

# Configurações de Log
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'sistema_restaurante.log'
}

# Configurações de Backup
BACKUP_CONFIG = {
    'auto_backup': True,
    'backup_interval_hours': 24,
    'backup_retention_days': 30,
    'backup_folder': 'backups'
}

def get_restaurante_info():
    """Retorna informações do restaurante"""
    return {
        'nome': RESTAURANTE_NOME,
        'telefone': RESTAURANTE_TELEFONE,
        'endereco': RESTAURANTE_ENDERECO,
        'horario': RESTAURANTE_HORARIO
    }

def get_whatsapp_config():
    """Retorna configurações do WhatsApp"""
    return {
        'numero': WHATSAPP_NUMERO,
        'mensagem_boas_vindas': WHATSAPP_MENSAGEM_BOAS_VINDAS.format(RESTAURANTE_NOME)
    }

def get_system_config():
    """Retorna configurações do sistema"""
    return {
        'tempo_entrega_extra': TEMPO_ENTREGA_EXTRA,
        'tempo_preparo_minimo': TEMPO_PREPARO_MINIMO,
        'tempo_preparo_maximo': TEMPO_PREPARO_MAXIMO,
        'porta_cardapio': PORTA_CARDAPIO,
        'porta_dashboard': PORTA_DASHBOARD
    } 