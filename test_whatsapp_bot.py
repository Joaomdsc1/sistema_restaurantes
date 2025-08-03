import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def test_whatsapp_connection():
    """Testa a conexão com WhatsApp Web"""
    driver = None
    try:
        print("🔧 Configurando Chrome...")
        
        # Configurações mínimas para Windows
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1200,800")
        
        # Remove detecção de automação
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        print("📥 Baixando ChromeDriver...")
        service = Service(ChromeDriverManager().install())
        
        print("🚀 Iniciando Chrome...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Remove propriedades de automação
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("📱 Abrindo WhatsApp Web...")
        driver.get("https://web.whatsapp.com/")
        
        print("⏳ Aguardando carregamento...")
        time.sleep(10)
        
        # Verifica se a página carregou
        print("🔍 Verificando elementos da página...")
        
        # Tenta encontrar o QR code
        try:
            qr_canvas = driver.find_element(By.XPATH, '//canvas[@aria-label="Scan me!"]')
            print("✅ QR Code encontrado! (canvas)")
        except:
            try:
                qr_div = driver.find_element(By.XPATH, '//div[@data-testid="qrcode"]')
                print("✅ QR Code encontrado! (div)")
            except:
                try:
                    qr_img = driver.find_element(By.XPATH, '//img[contains(@src, "qrcode")]')
                    print("✅ QR Code encontrado! (img)")
                except:
                    print("⚠️ QR Code não encontrado pelos seletores padrão")
                    print("📸 Verifique se há uma imagem de QR code na tela")
        
        # Verifica se há texto sobre QR code
        page_text = driver.page_source.lower()
        if "qr" in page_text or "scan" in page_text:
            print("✅ Texto relacionado ao QR code encontrado na página")
        
        print("\n📱 INSTRUÇÕES:")
        print("1. Verifique se há uma janela do Chrome aberta")
        print("2. Procure por um QR code na tela")
        print("3. Abra o WhatsApp no seu celular")
        print("4. Vá em Configurações > Aparelhos conectados")
        print("5. Escaneie o QR code")
        print("\n⏳ Aguardando 30 segundos para você escanear...")
        
        # Aguarda conexão
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "side"))
            )
            print("🎉 CONECTADO COM SUCESSO!")
            return True
        except:
            print("⏰ Tempo esgotado. Verifique se:")
            print("   - O QR code foi escaneado corretamente")
            print("   - O WhatsApp está conectado à internet")
            print("   - Não há outras sessões do WhatsApp Web ativas")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    finally:
        if driver:
            print("🔄 Fechando navegador...")
            driver.quit()

if __name__ == "__main__":
    print("🧪 TESTE DO WHATSAPP BOT")
    print("=" * 40)
    
    success = test_whatsapp_connection()
    
    if success:
        print("\n✅ Teste concluído com sucesso!")
    else:
        print("\n❌ Teste falhou. Verifique as configurações.")
    
    input("\nPressione Enter para sair...") 