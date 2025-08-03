# 🍽️ Sistema de Restaurante via WhatsApp

Sistema completo para gerenciamento de pedidos de restaurante através do WhatsApp, com interface web para visualização do cardápio e dashboard administrativo.

## 🚀 Funcionalidades

### 📱 Bot do WhatsApp
- Recebe pedidos via WhatsApp
- Processa números dos pratos automaticamente
- Calcula tempo estimado de entrega
- Confirma pedidos com resumo completo

### 🌐 Interface Web (Streamlit)
- **Cardápio Interativo**: Visualização atrativa do menu
- **Dashboard Administrativo**: Controle de pedidos e estatísticas
- **Categorização**: Menu organizado por categorias
- **Responsivo**: Interface adaptável para diferentes dispositivos

### 📊 Sistema de Gerenciamento
- Controle de status dos pedidos
- Estatísticas de vendas
- Exportação de dados
- Histórico completo de pedidos

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- Conta do WhatsApp
- Conexão com internet

## 🛠️ Instalação

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd sistema_restaurantes
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure o cardápio:**
Edite o arquivo `cardapio.csv` com seus produtos:
```csv
numero,nome,descricao,preco,tempo_estimado_minutos
1,X-Burger,Hambúrguer artesanal com queijo,25.90,15
```

## 🚀 Como Usar

### 1. Iniciar o Cardápio Web
```bash
streamlit run app_streamlit.py
```
Acesse: http://localhost:8501

### 2. Iniciar o Bot do WhatsApp
```bash
python whatsapp_bot.py
```
- Escaneie o QR Code no WhatsApp Web
- O bot ficará monitorando mensagens automaticamente

### 3. Dashboard Administrativo
```bash
streamlit run dashboard_admin.py
```
Acesse: http://localhost:8502

## 📱 Como Fazer Pedidos

1. **Visualize o cardápio** no site do Streamlit
2. **Envie uma mensagem** no WhatsApp para o número configurado
3. **Digite os números** dos pratos desejados (ex: 1, 3, 15)
4. **Confirme o pedido** digitando "ENVIAR"
5. **Receba o tempo estimado** de entrega

### Exemplo de Pedido:
```
Cliente: 1, 3, 15

Bot: 🍽️ Seu pedido:
• #1 - X-Burger - R$ 25,90
• #3 - X-Bacon - R$ 32,00
• #15 - Refrigerante - R$ 6,50

Total: R$ 64,40

Digite mais números para adicionar itens ou envie 'ENVIAR' para finalizar.

Cliente: ENVIAR

Bot: ✅ Pedido confirmado!
⏱️ Tempo estimado: 20 minutos
```

## 📊 Dashboard Administrativo

### Funcionalidades:
- **Métricas em tempo real**: Pedidos, receita, status
- **Gráficos interativos**: Análise de vendas e itens populares
- **Gerenciamento de pedidos**: Atualizar status, cancelar pedidos
- **Exportação de dados**: Relatórios em CSV
- **Filtros avançados**: Por data, status, cliente

### Status dos Pedidos:
- **Pendente**: Pedido recebido, aguardando preparo
- **Em Preparo**: Pedido sendo preparado
- **Concluído**: Pedido finalizado
- **Cancelado**: Pedido cancelado

## ⚙️ Configurações

### Personalizar Cardápio
Edite o arquivo `cardapio.csv`:
```csv
numero,nome,descricao,preco,tempo_estimado_minutos
```

### Configurar WhatsApp
No arquivo `whatsapp_bot.py`, altere:
- Número do WhatsApp do restaurante
- Mensagens de boas-vindas
- Tempo de resposta

### Configurar Interface
No arquivo `app_streamlit.py`, personalize:
- Nome do restaurante
- Informações de contato
- Cores e estilo

## 📁 Estrutura do Projeto

```
sistema_restaurantes/
├── app_streamlit.py          # Interface do cardápio
├── whatsapp_bot.py          # Bot do WhatsApp
├── dashboard_admin.py       # Dashboard administrativo
├── order_manager.py         # Gerenciador de pedidos
├── cardapio.csv            # Dados do cardápio
├── requirements.txt        # Dependências Python
├── orders.json            # Banco de dados dos pedidos
└── README.md              # Documentação
```

## 🔧 Solução de Problemas

### Bot não conecta ao WhatsApp
- Verifique se o Chrome está atualizado
- Certifique-se de que o WhatsApp Web está funcionando
- Tente escanear o QR Code novamente

### Erro ao carregar cardápio
- Verifique se o arquivo `cardapio.csv` existe
- Confirme se o formato está correto
- Verifique as permissões do arquivo

### Dashboard não atualiza
- Verifique se o arquivo `orders.json` existe
- Confirme as permissões de escrita
- Reinicie o aplicativo Streamlit

## 📈 Próximas Funcionalidades

- [ ] Integração com sistemas de pagamento
- [ ] Notificações automáticas de status
- [ ] Sistema de fidelidade
- [ ] Relatórios avançados
- [ ] Integração com delivery
- [ ] App mobile nativo

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Suporte

Para dúvidas ou suporte:
- Email: suporte@restaurante.com
- WhatsApp: (11) 99999-9999
- GitHub Issues: [Link do repositório]

---

**Desenvolvido com ❤️ para restaurantes que querem inovar!**