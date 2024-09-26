import os
from security import *
import time
import re
from TextUtils import *
from datetime import datetime
from vendas import *


def cancel_order():
    try:
        # Read orders from the file
        with open("./data/orders.txt", "r", encoding="UTF-8") as file:
            orders = file.readlines()
    except FileNotFoundError:
        print("Erro: Arquivo de pedidos não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return

    if not orders:
        print("Nenhum pedido encontrado.")
        input("Pressione ENTER para voltar ao menu...")
        os.system('cls')
        main()
        return

    print("Pedidos cadastrados:")
    for line in orders:
        order_data = line.strip().split(";")
        order_id = order_data[0].split(":")[1].strip()
        print(f"ID do pedido: {order_id}")

    order_id_to_cancel = input("Digite o ID do pedido que deseja cancelar: ").strip()

    # Check if the order ID exists
    order_found = False
    new_content = []

    for line in orders:
        order_data = line.strip().split(";")
        current_order_id = order_data[0].split(":")[1].strip()

        if current_order_id == order_id_to_cancel:
            order_found = True
            print(f"Pedido {order_id_to_cancel} cancelado com sucesso!")
            continue  # Skip the line to remove the order
        
        new_content.append(line)  # Keep orders that are not canceled

    # Rewrite the file without the canceled order
    if order_found:
        with open("./data/orders.txt", "w", encoding="UTF-8") as file:
            file.writelines(new_content)
    else:
        print(f"Pedido com ID {order_id_to_cancel} não encontrado.")

    input("Pressione ENTER para voltar ao menu...")
    os.system('cls')
    main()

def show_purchase_history():
    try:
        # Read orders from the file
        with open("./data/orders.txt", "r", encoding="UTF-8") as file:
            orders = file.readlines()
    except FileNotFoundError:
        print("Erro: Arquivo de pedidos não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return

    if not orders:
        print("Nenhum pedido encontrado.")
    else:
        printTitle("Histórico de Compras", GREEN, WHITE)
        print("\n")

        for line in orders:
            order_data = line.strip().split(";")
            order_id = order_data[0].split(":")[1].strip()
            product_code = order_data[1].split(":")[1].strip()
            quantity = order_data[2].split(":")[1].strip()
            total_price = order_data[3].split(":")[1].strip()
            order_date = order_data[4].split(":")[1].strip()

            print(f"ID do Pedido: {order_id}")
            print(f"Código do Produto: {product_code}")
            print(f"Quantidade: {quantity}")
            print(f"Preço Total: R$ {total_price}")
            print(f"Data: {order_date}")
            print("─" * 40)

    input("Pressione ENTER para continuar...")
    os.system('cls') 
    main()