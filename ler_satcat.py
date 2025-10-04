#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ler e exibir dados do arquivo satcat.csv usando pandas
"""

import pandas as pd
import os

def load_dataframe():
    """
    Localiza e carrega o dataset a partir da pasta recomendada `data/raw`.
    Dá preferência ao Excel UCS; faz fallback para CSV se necessário.
    Retorna (df, caminho_arquivo) ou (None, None) em caso de erro.
    """
    data_dir = os.path.join("data", "raw")
    excel_path = os.path.join(data_dir, "UCS-Satellite-Database 5-1-2023.xlsx")
    csv_path = os.path.join(data_dir, "satcat.csv")
    legacy_csv_path = "satcat.csv"

    try:
        if os.path.exists(excel_path):
            print(f"Carregando dados do arquivo {os.path.basename(excel_path)}...")
            print("=" * 60)
            df = pd.read_excel(excel_path, engine="openpyxl")
            return df, excel_path
        elif os.path.exists(csv_path):
            print(f"Carregando dados do arquivo {os.path.basename(csv_path)}...")
            print("=" * 60)
            df = pd.read_csv(csv_path)
            return df, csv_path
        elif os.path.exists(legacy_csv_path):
            print(f"Carregando dados do arquivo {os.path.basename(legacy_csv_path)}...")
            print("=" * 60)
            df = pd.read_csv(legacy_csv_path)
            return df, legacy_csv_path
        else:
            print("ERRO: Nenhum arquivo de dados encontrado.")
            print("Coloque o dataset em 'data/raw' (UCS-*.xlsx ou satcat.csv).")
            return None, None
    except Exception as e:
        print(f"ERRO ao carregar o dataset: {str(e)}")
        return None, None

def main():
    """
    Função principal para ler e exibir dados do arquivo satcat.csv
    """
    df, arquivo = load_dataframe()
    if df is None:
        return
    try:
        
        # Informações básicas sobre o dataset
        print(f"INFORMACOES GERAIS:")
        print(f"   - Total de registros: {len(df):,}")
        print(f"   - Total de colunas: {len(df.columns)}")
        print(f"   - Tamanho do arquivo: {os.path.getsize(arquivo) / (1024*1024):.1f} MB")
        print()
        
        # Exibir informações sobre as colunas
        print("COLUNAS DISPONIVEIS:")
        for i, coluna in enumerate(df.columns, 1):
            print(f"   {i:2d}. {coluna}")
        print()
        
        # Exibir primeiras linhas
        print("PRIMEIRAS 10 LINHAS:")
        print("-" * 60)
        print(df.head(10).to_string(index=False))
        print()
        
        # Estatísticas básicas
        print("ESTATISTICAS BASICAS:")
        print("-" * 60)
        print(df.describe(include='all'))
        print()
        
        # Informações sobre valores nulos
        print("VALORES NULOS POR COLUNA:")
        print("-" * 60)
        valores_nulos = df.isnull().sum()
        for coluna, nulos in valores_nulos.items():
            if nulos > 0:
                percentual = (nulos / len(df)) * 100
                print(f"   {coluna}: {nulos:,} ({percentual:.1f}%)")
        print()
        
        # Análise por tipo de objeto
        print("DISTRIBUICAO POR TIPO DE OBJETO:")
        print("-" * 60)
        if 'OBJECT_TYPE' in df.columns:
            tipos = df['OBJECT_TYPE'].value_counts()
            for tipo, quantidade in tipos.items():
                print(f"   {tipo}: {quantidade:,}")
        print()
        
        # Análise por país/owner
        print("TOP 10 PAISES/OWNERS:")
        print("-" * 60)
        if 'OWNER' in df.columns:
            owners = df['OWNER'].value_counts().head(10)
            for owner, quantidade in owners.items():
                print(f"   {owner}: {quantidade:,}")
        print()
        
        # Análise por status operacional
        print("STATUS OPERACIONAL:")
        print("-" * 60)
        if 'OPS_STATUS_CODE' in df.columns:
            status = df['OPS_STATUS_CODE'].value_counts()
            for stat, quantidade in status.items():
                print(f"   {stat}: {quantidade:,}")
        print()
        
        # Últimas linhas
        print("ULTIMAS 5 LINHAS:")
        print("-" * 60)
        print(df.tail(5).to_string(index=False))
        
        print("\nDados carregados e exibidos com sucesso!")
        
    except Exception as e:
        print(f"ERRO ao processar o arquivo: {str(e)}")
        print("Verifique se o arquivo está no formato correto e se o pandas está instalado.")

def menu_interativo():
    """
    Menu interativo para explorar os dados
    """
    df, _arquivo = load_dataframe()
    if df is None:
        return
    
    while True:
        print("\n" + "="*60)
        print("MENU INTERATIVO - EXPLORAR DADOS SATCAT")
        print("="*60)
        print("1. Ver primeiras N linhas")
        print("2. Ver últimas N linhas")
        print("3. Filtrar por país/owner")
        print("4. Filtrar por tipo de objeto")
        print("5. Filtrar por status operacional")
        print("6. Buscar por nome do objeto")
        print("7. Estatísticas de uma coluna específica")
        print("8. Sair")
        print("-"*60)
        
        opcao = input("Escolha uma opção (1-8): ").strip()
        
        if opcao == "1":
            try:
                n = int(input("Quantas linhas deseja ver? "))
                print(f"\nPrimeiras {n} linhas:")
                print(df.head(n).to_string(index=False))
            except ValueError:
                print("ERRO: Por favor, digite um número válido.")
        
        elif opcao == "2":
            try:
                n = int(input("Quantas linhas deseja ver? "))
                print(f"\nÚltimas {n} linhas:")
                print(df.tail(n).to_string(index=False))
            except ValueError:
                print("ERRO: Por favor, digite um número válido.")
        
        elif opcao == "3":
            if 'OWNER' in df.columns:
                print("\nPaíses/owners disponíveis:")
                owners = df['OWNER'].value_counts()
                for i, (owner, count) in enumerate(owners.head(20).items(), 1):
                    print(f"   {i:2d}. {owner} ({count:,} objetos)")
                
                owner_input = input("\nDigite o nome do país/owner (ou número): ").strip()
                try:
                    # Tentar como número
                    owner_index = int(owner_input) - 1
                    owner = list(owners.index)[owner_index]
                except (ValueError, IndexError):
                    # Usar como texto
                    owner = owner_input
                
                filtrado = df[df['OWNER'] == owner]
                print(f"\nObjetos do país/owner '{owner}':")
                print(f"Total encontrado: {len(filtrado):,}")
                if len(filtrado) > 0:
                    print(filtrado.head(10).to_string(index=False))
            else:
                print("ERRO: Coluna 'OWNER' não encontrada.")
        
        elif opcao == "4":
            if 'OBJECT_TYPE' in df.columns:
                print("\nTipos de objetos disponíveis:")
                tipos = df['OBJECT_TYPE'].value_counts()
                for i, (tipo, count) in enumerate(tipos.items(), 1):
                    print(f"   {i}. {tipo} ({count:,} objetos)")
                
                tipo_input = input("\nDigite o tipo de objeto (ou número): ").strip()
                try:
                    # Tentar como número
                    tipo_index = int(tipo_input) - 1
                    tipo = list(tipos.index)[tipo_index]
                except (ValueError, IndexError):
                    # Usar como texto
                    tipo = tipo_input
                
                filtrado = df[df['OBJECT_TYPE'] == tipo]
                print(f"\nObjetos do tipo '{tipo}':")
                print(f"Total encontrado: {len(filtrado):,}")
                if len(filtrado) > 0:
                    print(filtrado.head(10).to_string(index=False))
            else:
                print("ERRO: Coluna 'OBJECT_TYPE' não encontrada.")
        
        elif opcao == "5":
            if 'OPS_STATUS_CODE' in df.columns:
                print("\nStatus operacionais disponíveis:")
                status = df['OPS_STATUS_CODE'].value_counts()
                for i, (stat, count) in enumerate(status.items(), 1):
                    print(f"   {i}. {stat} ({count:,} objetos)")
                
                status_input = input("\nDigite o status (ou número): ").strip()
                try:
                    # Tentar como número
                    status_index = int(status_input) - 1
                    stat = list(status.index)[status_index]
                except (ValueError, IndexError):
                    # Usar como texto
                    stat = status_input
                
                filtrado = df[df['OPS_STATUS_CODE'] == stat]
                print(f"\nObjetos com status '{stat}':")
                print(f"Total encontrado: {len(filtrado):,}")
                if len(filtrado) > 0:
                    print(filtrado.head(10).to_string(index=False))
            else:
                print("ERRO: Coluna 'OPS_STATUS_CODE' não encontrada.")
        
        elif opcao == "6":
            if 'OBJECT_NAME' in df.columns:
                nome = input("\nDigite o nome do objeto para buscar: ").strip()
                if nome:
                    # Busca parcial (case insensitive)
                    filtrado = df[df['OBJECT_NAME'].str.contains(nome, case=False, na=False)]
                    print(f"\nObjetos contendo '{nome}':")
                    print(f"Total encontrado: {len(filtrado):,}")
                    if len(filtrado) > 0:
                        print(filtrado.head(10).to_string(index=False))
                    else:
                        print("Nenhum objeto encontrado.")
            else:
                print("ERRO: Coluna 'OBJECT_NAME' não encontrada.")
        
        elif opcao == "7":
            print("\nColunas disponíveis:")
            for i, coluna in enumerate(df.columns, 1):
                print(f"   {i:2d}. {coluna}")
            
            try:
                coluna_num = int(input("\nDigite o número da coluna: ")) - 1
                coluna = df.columns[coluna_num]
                print(f"\nEstatísticas da coluna '{coluna}':")
                print(df[coluna].describe())
            except (ValueError, IndexError):
                print("ERRO: Número de coluna inválido.")
        
        elif opcao == "8":
            print("Obrigado por usar o explorador de dados SATCAT!")
            break
        
        else:
            print("ERRO: Opção inválida. Escolha entre 1-8.")

if __name__ == "__main__":
    print("EXPLORADOR DE DADOS SATCAT")
    print("=" * 60)
    
    # Executar análise básica
    main()
    
    # Perguntar se quer usar o menu interativo
    resposta = input("\nDeseja usar o menu interativo para explorar os dados? (s/n): ").strip().lower()
    if resposta in ['s', 'sim', 'y', 'yes']:
        menu_interativo()