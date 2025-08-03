import time
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import json
import os
from datetime import datetime

class WhatsAppBot:
    def __init__(self):
        self.driver = None
        self.menu_df = None
        self.active_orders = {}  # {phone: {'items': [], 'total': 0, 'state': 'ordering'}}
        self.load_menu()
        
    def load_menu(self):
        """Carrega o cardápio do arquivo CSV"""
        try:
            self.menu_df = pd.read_csv('cardapio.csv')
            print("✅ Cardápio carregado com sucesso!")
        except FileNotFoundError:
            print("❌ Erro: Arquivo cardapio.csv não encontrado!")
            return None
    
    def setup_driver(self):
        """Configura o driver do Chrome para WhatsApp Web"""
        try:
            print("🔧 Configurando Chrome...")
            
            chrome_options = Options()
            
            # Caminho específico do Chrome no Windows
            chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            if os.path.exists(chrome_path):
                chrome_options.binary_location = chrome_path
                print(f"✅ Chrome encontrado em: {chrome_path}")
            else:
                print("⚠️ Chrome não encontrado no caminho padrão")
            
            # Configurações essenciais para Windows
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1200,800")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            
            # Remove detecção de automação
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Configurações adicionais para estabilidade
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")
            chrome_options.add_argument("--disable-javascript")
            chrome_options.add_argument("--disable-web-security")
            
            print("📥 Baixando ChromeDriver...")
            service = Service(ChromeDriverManager().install())
            
            print("🚀 Iniciando Chrome...")
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Remove propriedades de automação
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Driver do Chrome configurado com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao configurar driver: {e}")
            print("💡 Soluções possíveis:")
            print("   1. Reinstale o Chrome")
            print("   2. Execute como administrador")
            print("   3. Verifique se há antivírus bloqueando")
            return False
        
    def connect_whatsapp(self):
        """Conecta ao WhatsApp Web"""
        try:
            print("📱 Abrindo WhatsApp Web...")
            self.driver.get("https://web.whatsapp.com/")
            
            print("⏳ Aguardando carregamento da página...")
            time.sleep(10)
            
            # Verifica se a página carregou
            print("🔍 Verificando elementos da página...")
            
            # Tenta encontrar o QR code
            qr_found = False
            try:
                qr_canvas = self.driver.find_element(By.XPATH, '//canvas[@aria-label="Scan me!"]')
                print("✅ QR Code encontrado! (canvas)")
                qr_found = True
            except:
                try:
                    qr_div = self.driver.find_element(By.XPATH, '//div[@data-testid="qrcode"]')
                    print("✅ QR Code encontrado! (div)")
                    qr_found = True
                except:
                    try:
                        qr_img = self.driver.find_element(By.XPATH, '//img[contains(@src, "qrcode")]')
                        print("✅ QR Code encontrado! (img)")
                        qr_found = True
                    except:
                        pass
            
            if not qr_found:
                print("⚠️ QR Code não encontrado pelos seletores padrão")
                print("📸 Verifique se há uma imagem de QR code na tela")
                
                # Verifica se há texto sobre QR code
                page_text = self.driver.page_source.lower()
                if "qr" in page_text or "scan" in page_text:
                    print("✅ Texto relacionado ao QR code encontrado na página")
            
            print("\n📱 INSTRUÇÕES:")
            print("1. Verifique se há uma janela do Chrome aberta")
            print("2. Procure por um QR code na tela")
            print("3. Abra o WhatsApp no seu celular")
            print("4. Vá em Configurações > Aparelhos conectados")
            print("5. Escaneie o QR code")
            print("\n⏳ Aguardando conexão (60 segundos)...")
            
            # Aguarda a conexão
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.ID, "side"))
            )
            print("✅ WhatsApp Web conectado com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao conectar ao WhatsApp: {e}")
            print("💡 Dicas:")
            print("   - Certifique-se de que o Chrome está instalado")
            print("   - Verifique se há uma janela do Chrome aberta")
            print("   - Tente escanear o QR code novamente")
            print("   - Verifique se não há outras sessões do WhatsApp Web ativas")
            return False
    
    def get_menu_item(self, number):
        """Busca um item no cardápio pelo número"""
        item = self.menu_df[self.menu_df['numero'] == number]
        if not item.empty:
            return item.iloc[0]
        return None
    
    def format_order_summary(self, items, total):
        """Formata o resumo do pedido"""
        summary = "🍽️ **Seu pedido:**\n"
        for item in items:
            summary += f"• #{item['numero']} - {item['nome']} - R$ {item['preco']:.2f}\n"
        summary += f"\n**Total: R$ {total:.2f}**\n\n"
        summary += "Digite mais números para adicionar itens ou envie 'ENVIAR' para finalizar."
        return summary
    
    def calculate_estimated_time(self, items):
        """Calcula o tempo estimado baseado no item mais demorado"""
        if not items:
            return 0
        
        max_time = max(item['tempo_estimado_minutos'] for item in items)
        return max_time
    
    def process_message(self, phone, message):
        """Processa a mensagem recebida"""
        message = message.strip().upper()
        
        # Se é a primeira mensagem ou pedido finalizado
        if phone not in self.active_orders:
            self.active_orders[phone] = {
                'items': [],
                'total': 0,
                'state': 'ordering'
            }
        
        # Comando para finalizar pedido
        if message == "ENVIAR":
            if not self.active_orders[phone]['items']:
                return "❌ Nenhum item no pedido. Digite os números dos pratos desejados."
            
            estimated_time = self.calculate_estimated_time(self.active_orders[phone]['items'])
            total = self.active_orders[phone]['total']
            
            response = f"""✅ **Pedido confirmado!**

🍽️ **Itens do pedido:**
"""
            for item in self.active_orders[phone]['items']:
                response += f"• #{item['numero']} - {item['nome']} - R$ {item['preco']:.2f}\n"
            
            response += f"""
💰 **Total: R$ {total:.2f}**
⏱️ **Tempo estimado:** {estimated_time} minutos
📍 **Endereço de entrega:** [será solicitado]

📞 **Para dúvidas:** (11) 99999-9999
🕒 **Pedido realizado em:** {datetime.now().strftime("%d/%m/%Y %H:%M")}

Obrigado por escolher nosso restaurante! 🍽️"""
            
            # Limpa o pedido ativo
            del self.active_orders[phone]
            return response
        
        # Processa números de itens
        numbers = re.findall(r'\d+', message)
        if not numbers:
            return """🍽️ **Bem-vindo ao nosso restaurante!**

Para fazer seu pedido, digite os números dos pratos desejados.
Exemplo: 1, 3, 15

Para ver o cardápio completo, acesse: [link do Streamlit]

Digite 'ENVIAR' quando terminar seu pedido."""
        
        # Adiciona itens ao pedido
        added_items = []
        for num in numbers:
            item_num = int(num)
            item = self.get_menu_item(item_num)
            if item is not None:
                item_dict = item.to_dict()
                self.active_orders[phone]['items'].append(item_dict)
                self.active_orders[phone]['total'] += item_dict['preco']
                added_items.append(item_dict)
        
        if not added_items:
            return "❌ Nenhum item válido encontrado. Verifique os números e tente novamente."
        
        # Retorna resumo do pedido
        return self.format_order_summary(
            self.active_orders[phone]['items'], 
            self.active_orders[phone]['total']
        )
    
    def send_message(self, phone, message):
        """Envia mensagem para um número específico"""
        try:
            # Formata o número do telefone
            if not phone.startswith('55'):
                phone = '55' + phone.replace('+', '').replace('-', '').replace(' ', '')
            
            # URL do WhatsApp com o número
            url = f"https://web.whatsapp.com/send?phone={phone}"
            self.driver.get(url)
            
            # Aguarda carregar a conversa
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            
            # Encontra o campo de mensagem
            message_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            message_box.clear()
            message_box.send_keys(message)
            
            # Envia a mensagem
            send_button = self.driver.find_element(By.XPATH, '//span[@data-icon="send"]')
            send_button.click()
            
            time.sleep(2)
            print(f"✅ Mensagem enviada para {phone}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem para {phone}: {e}")
            return False
    
    def monitor_messages(self):
        """Monitora mensagens recebidas"""
        print("🔍 Monitorando mensagens...")
        
        while True:
            try:
                # Procura por mensagens não lidas
                unread_messages = self.driver.find_elements(
                    By.XPATH, '//span[@data-icon="unread-count"]'
                )
                
                for unread in unread_messages:
                    try:
                        # Clica na conversa não lida
                        unread.click()
                        time.sleep(2)
                        
                        # Obtém o número do telefone
                        phone_element = self.driver.find_element(
                            By.XPATH, '//span[@data-testid="conversation-info-header-chat-title"]'
                        )
                        phone = phone_element.text
                        
                        # Obtém a última mensagem
                        messages = self.driver.find_elements(
                            By.XPATH, '//div[contains(@class, "message-in")]//span[@dir="ltr"]'
                        )
                        
                        if messages:
                            last_message = messages[-1].text
                            print(f"📱 Nova mensagem de {phone}: {last_message}")
                            
                            # Processa a mensagem
                            response = self.process_message(phone, last_message)
                            
                            # Envia resposta
                            self.send_message(phone, response)
                            
                    except Exception as e:
                        print(f"❌ Erro ao processar mensagem: {e}")
                        continue
                
                time.sleep(5)  # Verifica a cada 5 segundos
                
            except KeyboardInterrupt:
                print("\n🛑 Bot interrompido pelo usuário")
                break
            except Exception as e:
                print(f"❌ Erro no monitoramento: {e}")
                time.sleep(10)
    
    def run(self):
        """Executa o bot"""
        try:
            if not self.setup_driver():
                print("❌ Falha ao configurar o driver")
                return
            
            if self.connect_whatsapp():
                print("🤖 Bot iniciado com sucesso!")
                print("📱 Monitorando mensagens...")
                self.monitor_messages()
            else:
                print("❌ Falha ao conectar ao WhatsApp")
                
        except Exception as e:
            print(f"❌ Erro ao executar bot: {e}")
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    bot = WhatsAppBot()
    bot.run() 