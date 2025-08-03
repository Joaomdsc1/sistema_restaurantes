#!/usr/bin/env python3
"""
Script principal para executar o sistema completo de restaurante
"""

import subprocess
import sys
import time
import os
import signal
import threading
from pathlib import Path

def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    try:
        import streamlit
        import pandas
        import selenium
        import plotly
        print("✅ Todas as dependências estão instaladas!")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        print("Execute: pip install -r requirements.txt")
        return False

def check_files():
    """Verifica se todos os arquivos necessários existem"""
    required_files = [
        'cardapio.csv',
        'app_streamlit.py',
        'whatsapp_bot.py',
        'dashboard_admin.py',
        'order_manager.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Arquivos faltando: {', '.join(missing_files)}")
        return False
    
    print("✅ Todos os arquivos necessários encontrados!")
    return True

def run_streamlit_app(port, app_file):
    """Executa aplicação Streamlit em uma thread separada"""
    try:
        cmd = [sys.executable, "-m", "streamlit", "run", app_file, "--server.port", str(port)]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"🚀 {app_file} iniciado na porta {port}")
        return process
    except Exception as e:
        print(f"❌ Erro ao iniciar {app_file}: {e}")
        return None

def run_whatsapp_bot():
    """Executa o bot do WhatsApp em uma thread separada"""
    try:
        # Tenta usar a versão Windows primeiro
        bot_file = "whatsapp_bot_windows.py"
        if not Path(bot_file).exists():
            bot_file = "whatsapp_bot.py"
        
        cmd = [sys.executable, bot_file]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"🤖 Bot do WhatsApp iniciado ({bot_file})")
        return process
    except Exception as e:
        print(f"❌ Erro ao iniciar bot do WhatsApp: {e}")
        return None

def main():
    """Função principal"""
    print("🍽️ Sistema de Restaurante via WhatsApp")
    print("=" * 50)
    
    # Verificações iniciais
    if not check_dependencies():
        return
    
    if not check_files():
        return
    
    print("\n🚀 Iniciando sistema...")
    
    processes = []
    
    try:
        # Inicia aplicações Streamlit
        print("\n📱 Iniciando aplicações web...")
        
        # Cardápio na porta 8501
        cardapio_process = run_streamlit_app(8501, "app_streamlit.py")
        if cardapio_process:
            processes.append(("Cardápio", cardapio_process))
        
        time.sleep(3)
        
        # Dashboard na porta 8502
        dashboard_process = run_streamlit_app(8502, "dashboard_admin.py")
        if dashboard_process:
            processes.append(("Dashboard", dashboard_process))
        
        time.sleep(3)
        
        # Inicia bot do WhatsApp
        print("\n📱 Iniciando bot do WhatsApp...")
        bot_process = run_whatsapp_bot()
        if bot_process:
            processes.append(("Bot WhatsApp", bot_process))
        
        print("\n✅ Sistema iniciado com sucesso!")
        print("\n🌐 Acesse:")
        print("   • Cardápio: http://localhost:8501")
        print("   • Dashboard: http://localhost:8502")
        print("\n📱 Bot do WhatsApp:")
        print("   • Escaneie o QR Code quando aparecer")
        print("   • O bot monitorará mensagens automaticamente")
        
        print("\n🛑 Pressione Ctrl+C para parar o sistema")
        
        # Aguarda interrupção
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Parando sistema...")
        
        # Para todos os processos
        for name, process in processes:
            try:
                print(f"🛑 Parando {name}...")
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print(f"⚠️ Forçando parada do {name}...")
                process.kill()
            except Exception as e:
                print(f"❌ Erro ao parar {name}: {e}")
        
        print("✅ Sistema parado com sucesso!")

def run_cardapio_only():
    """Executa apenas o cardápio"""
    print("🍽️ Iniciando apenas o cardápio...")
    run_streamlit_app(8501, "app_streamlit.py")
    print("🌐 Acesse: http://localhost:8501")
    print("🛑 Pressione Ctrl+C para parar")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n✅ Cardápio parado!")

def run_dashboard_only():
    """Executa apenas o dashboard"""
    print("📊 Iniciando apenas o dashboard...")
    run_streamlit_app(8502, "dashboard_admin.py")
    print("🌐 Acesse: http://localhost:8502")
    print("🛑 Pressione Ctrl+C para parar")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n✅ Dashboard parado!")

def run_bot_only():
    """Executa apenas o bot do WhatsApp"""
    print("🤖 Iniciando apenas o bot do WhatsApp...")
    bot_process = run_whatsapp_bot()
    print("📱 Escaneie o QR Code quando aparecer")
    print("🛑 Pressione Ctrl+C para parar")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        if bot_process:
            bot_process.terminate()
        print("\n✅ Bot parado!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        option = sys.argv[1].lower()
        
        if option == "cardapio":
            run_cardapio_only()
        elif option == "dashboard":
            run_dashboard_only()
        elif option == "bot":
            run_bot_only()
        elif option == "help":
            print("🍽️ Sistema de Restaurante - Opções:")
            print("  python run_system.py          # Sistema completo")
            print("  python run_system.py cardapio # Apenas cardápio")
            print("  python run_system.py dashboard # Apenas dashboard")
            print("  python run_system.py bot      # Apenas bot WhatsApp")
            print("  python run_system.py help     # Esta ajuda")
        else:
            print(f"❌ Opção inválida: {option}")
            print("Use 'python run_system.py help' para ver as opções")
    else:
        main() 