# 🚀 Instruções Rápidas - Sistema de Restaurante

## ⚡ Início Rápido

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Testar Sistema
```bash
python test_system.py
```

### 3. Iniciar Sistema Completo
```bash
python run_system.py
```

## 📱 Como Usar

### 🌐 Cardápio Web
- **URL:** http://localhost:8501
- **Comando:** `python run_system.py cardapio`
- **Função:** Visualizar menu do restaurante

### 📊 Dashboard Administrativo
- **URL:** http://localhost:8502
- **Comando:** `python run_system.py dashboard`
- **Função:** Gerenciar pedidos e ver estatísticas

### 🤖 Bot do WhatsApp
- **Comando:** `python run_system.py bot`
- **Função:** Receber pedidos via WhatsApp
- **Configuração:** Escanear QR Code quando solicitado

## 📋 Fluxo de Pedido

1. **Cliente acessa:** http://localhost:8501
2. **Escolhe pratos:** Anota números dos itens desejados
3. **Envia WhatsApp:** Mensagem com números (ex: "1, 3, 15")
4. **Bot responde:** Resumo do pedido
5. **Cliente confirma:** Envia "ENVIAR"
6. **Bot confirma:** Tempo estimado de entrega

## ⚙️ Configurações

### Personalizar Restaurante
Edite `config.py`:
```python
RESTAURANTE_NOME = "Seu Restaurante"
RESTAURANTE_TELEFONE = "(11) 99999-9999"
WHATSAPP_NUMERO = "11999999999"
```

### Atualizar Cardápio
Edite `cardapio.csv`:
```csv
numero,nome,descricao,preco,tempo_estimado_minutos
1,Seu Prato,"Descrição do prato",25.90,15
```

## 🔧 Comandos Úteis

```bash
# Sistema completo
python run_system.py

# Apenas cardápio
python run_system.py cardapio

# Apenas dashboard
python run_system.py dashboard

# Apenas bot WhatsApp
python run_system.py bot

# Testar sistema
python test_system.py

# Ver ajuda
python run_system.py help
```

## 📁 Arquivos Importantes

- `cardapio.csv` - Dados do menu
- `config.py` - Configurações do sistema
- `orders.json` - Banco de dados dos pedidos
- `app_streamlit.py` - Interface do cardápio
- `dashboard_admin.py` - Dashboard administrativo
- `whatsapp_bot.py` - Bot do WhatsApp
- `order_manager.py` - Gerenciador de pedidos

## 🚨 Solução de Problemas

### Bot não conecta
- Verifique se o Chrome está atualizado
- Escaneie o QR Code novamente
- Verifique conexão com internet

### Erro no cardápio
- Verifique se `cardapio.csv` existe
- Confirme formato do CSV
- Reinicie o aplicativo

### Dashboard não carrega
- Verifique se `orders.json` existe
- Confirme permissões de escrita
- Reinicie o aplicativo

## 📞 Suporte

- **Email:** suporte@restaurante.com
- **WhatsApp:** (11) 99999-9999
- **Documentação:** README.md

---

**🍽️ Sistema pronto para uso!** 