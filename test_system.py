#!/usr/bin/env python3
"""
Script de teste para verificar o funcionamento do sistema
"""

import sys
import os
import pandas as pd
import json
from datetime import datetime
from pathlib import Path

def test_imports():
    """Testa se todas as dependências podem ser importadas"""
    print("🔍 Testando importações...")
    
    try:
        import streamlit
        print("✅ Streamlit importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar Streamlit: {e}")
        return False
    
    try:
        import pandas
        print("✅ Pandas importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar Pandas: {e}")
        return False
    
    try:
        import selenium
        print("✅ Selenium importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar Selenium: {e}")
        return False
    
    try:
        import plotly
        print("✅ Plotly importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar Plotly: {e}")
        return False
    
    return True

def test_files():
    """Testa se todos os arquivos necessários existem"""
    print("\n📁 Testando arquivos...")
    
    required_files = [
        'cardapio.csv',
        'app_streamlit.py',
        'whatsapp_bot.py',
        'dashboard_admin.py',
        'order_manager.py',
        'config.py',
        'requirements.txt'
    ]
    
    all_files_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} encontrado")
        else:
            print(f"❌ {file} não encontrado")
            all_files_exist = False
    
    return all_files_exist

def test_cardapio_csv():
    """Testa se o arquivo CSV do cardápio está correto"""
    print("\n🍽️ Testando cardápio CSV...")
    
    try:
        df = pd.read_csv('cardapio.csv')
        
        # Verifica colunas obrigatórias
        required_columns = ['numero', 'nome', 'descricao', 'preco', 'tempo_estimado_minutos']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ Colunas faltando: {missing_columns}")
            return False
        
        print(f"✅ CSV carregado com {len(df)} itens")
        print(f"✅ Colunas: {list(df.columns)}")
        
        # Verifica tipos de dados
        if not df['numero'].dtype in ['int64', 'int32']:
            print("❌ Coluna 'numero' deve ser numérica")
            return False
        
        if not df['preco'].dtype in ['float64', 'float32']:
            print("❌ Coluna 'preco' deve ser numérica")
            return False
        
        if not df['tempo_estimado_minutos'].dtype in ['int64', 'int32']:
            print("❌ Coluna 'tempo_estimado_minutos' deve ser numérica")
            return False
        
        print("✅ Tipos de dados corretos")
        
        # Mostra alguns itens
        print("\n📋 Primeiros 3 itens do cardápio:")
        for _, item in df.head(3).iterrows():
            print(f"  #{item['numero']} - {item['nome']} - R$ {item['preco']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar CSV: {e}")
        return False

def test_order_manager():
    """Testa o gerenciador de pedidos"""
    print("\n📊 Testando gerenciador de pedidos...")
    
    try:
        from order_manager import OrderManager
        
        manager = OrderManager()
        print("✅ OrderManager criado com sucesso")
        
        # Testa criação de pedido
        test_items = [
            {'numero': 1, 'nome': 'X-Burger', 'preco': 25.90, 'tempo_estimado_minutos': 15},
            {'numero': 15, 'nome': 'Refrigerante', 'preco': 6.50, 'tempo_estimado_minutos': 2}
        ]
        
        order = manager.create_order(
            phone="11999999999",
            items=test_items,
            total=32.40,
            estimated_time=15
        )
        
        print(f"✅ Pedido de teste criado: #{order['id']}")
        
        # Testa resumo
        summary = manager.get_order_summary()
        print(f"✅ Resumo do sistema: {summary['total_orders']} pedidos")
        
        # Testa estatísticas
        stats = manager.get_menu_statistics()
        print(f"✅ Estatísticas: {len(stats)} itens diferentes pedidos")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar OrderManager: {e}")
        return False

def test_config():
    """Testa o arquivo de configuração"""
    print("\n⚙️ Testando configurações...")
    
    try:
        from config import get_restaurante_info, get_whatsapp_config, get_system_config
        
        # Testa informações do restaurante
        restaurante_info = get_restaurante_info()
        print(f"✅ Restaurante: {restaurante_info['nome']}")
        print(f"✅ Telefone: {restaurante_info['telefone']}")
        
        # Testa configurações do WhatsApp
        whatsapp_config = get_whatsapp_config()
        print(f"✅ WhatsApp: {whatsapp_config['numero']}")
        
        # Testa configurações do sistema
        system_config = get_system_config()
        print(f"✅ Porta cardápio: {system_config['porta_cardapio']}")
        print(f"✅ Porta dashboard: {system_config['porta_dashboard']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar configurações: {e}")
        return False

def test_streamlit_apps():
    """Testa se os apps Streamlit podem ser importados"""
    print("\n🌐 Testando apps Streamlit...")
    
    try:
        # Testa importação do app do cardápio
        import app_streamlit
        print("✅ app_streamlit.py importado com sucesso")
        
        # Testa importação do dashboard
        import dashboard_admin
        print("✅ dashboard_admin.py importado com sucesso")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar apps Streamlit: {e}")
        return False

def test_whatsapp_bot():
    """Testa se o bot do WhatsApp pode ser importado"""
    print("\n🤖 Testando bot do WhatsApp...")
    
    try:
        import whatsapp_bot
        print("✅ whatsapp_bot.py importado com sucesso")
        
        # Testa criação da classe
        bot = whatsapp_bot.WhatsAppBot()
        print("✅ WhatsAppBot criado com sucesso")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar bot do WhatsApp: {e}")
        return False

def run_all_tests():
    """Executa todos os testes"""
    print("🧪 Iniciando testes do sistema...")
    print("=" * 50)
    
    tests = [
        ("Importações", test_imports),
        ("Arquivos", test_files),
        ("Cardápio CSV", test_cardapio_csv),
        ("Configurações", test_config),
        ("Order Manager", test_order_manager),
        ("Apps Streamlit", test_streamlit_apps),
        ("Bot WhatsApp", test_whatsapp_bot)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro no teste {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumo dos resultados
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! O sistema está pronto para uso.")
        print("\n🚀 Para iniciar o sistema:")
        print("   python run_system.py")
        print("\n📱 Para iniciar apenas o cardápio:")
        print("   python run_system.py cardapio")
        print("\n📊 Para iniciar apenas o dashboard:")
        print("   python run_system.py dashboard")
        print("\n🤖 Para iniciar apenas o bot:")
        print("   python run_system.py bot")
    else:
        print("⚠️ Alguns testes falharam. Verifique os erros acima.")
        print("\n💡 Dicas:")
        print("   - Execute: pip install -r requirements.txt")
        print("   - Verifique se todos os arquivos estão presentes")
        print("   - Confirme se o Python 3.8+ está instalado")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 