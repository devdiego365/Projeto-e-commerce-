import os
from security import *
import time
import re
from TextUtils import *
from datetime import datetime
from program import *



def register_product_and_purchase():
    # Open the product file for writing
    try:
        with open("./data/products.txt", "a+", encoding="UTF-8") as products_file:
            products_file.seek(0)
            product_lines = products_file.readlines()

            # Track the last used product code
            last_product_code = 0
            if product_lines:
                last_product_line = product_lines[-1]
                last_product_code = int(last_product_line.strip().split(";")[0].split(":")[1])

            # Request product data
            printTitle("Ordem de compra", GREEN, WHITE)
            drawBox(1, 5, 120, 16, MAGENTA)
            gotoxy(2, 6)
            product_name = input("Digite o nome do produto: ")
            gotoxy(2, 7)
            product_desc = input("Descreva o produto: ")
            gotoxy(2, 8)
            buying_price = float(input("Digite o preço de compra do produto: "))
            gotoxy(2, 9)
            selling_price = float(input("Digite o preço de venda do produto: "))
            gotoxy(2, 10)
            product_amount = int(input("Digite a quantidade comprada: "))

            # Validate purchase date
            date_regex = re.compile(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$")
            while True:
                gotoxy(2, 11)
                order_date = input("Digite a data da compra no formato dd/mm/aaaa: ")
                if date_regex.match(order_date):
                    break
                else:
                    print("Data inválida. Insira no formato correto (dd/mm/aaaa).")

            # Calculate total purchase value (quantity * purchase price)
            total_buying_value = buying_price * product_amount

            # Create new product and add to archive
            new_product = Product(code=last_product_code + 1, name=product_name, description=product_desc, buying_price=buying_price, selling_price=selling_price)
            products_file.write(f"{new_product}\n")
            gotoxy(2, 12)
            print(f"Produto '{new_product.name}' registrado com sucesso!")

    except Exception as e:
        gotoxy(2, 12)
        print(f"Erro ao manipular o arquivo de produtos: {e}")
        return

    # Register in order file
    try:
        with open("./data/orders.txt", "a+", encoding="UTF-8") as orders_file:
            orders_file.seek(0)
            order_lines = orders_file.readlines()

            # Track the last used order ID
            last_order_id = 0
            if order_lines:
                last_order_line = order_lines[-1]
                last_order_id = int(last_order_line.strip().split(";")[0].split(":")[1])

            # Calculate total purchase price (selling price * quantity)
            total_selling_value = selling_price * product_amount

            # Create new order and add to file
            new_order = Order(order_id=last_order_id + 1, product_id=new_product.code, product_amount=product_amount, order_price=total_selling_value, order_date=order_date)
            orders_file.write(f"ID da compra: {new_order.order_id}; Código: {new_product.code}; Quantidade: {new_order.product_amount}; Preço Compra Total: {total_buying_value:.2f}; Preço Venda Total: {total_selling_value:.2f}; Data: {new_order.order_date}\n")
            gotoxy(2, 14)
            printColored(f"Compra registrada com sucesso! Total da compra: R$ {total_selling_value:.2f}", GREEN, end="")

    except Exception as e:
        gotoxy(2, 14)
        printColored(f"Erro ao registrar a compra: {e}", RED, end="")
        return

    # Return to main menu  
    gotoxy(2, 15)
    input("Pressione ENTER para voltar ao menu principal...")
    os.system('cls')
    main()


def delete_product():
    # Open the file with registered products
    with open("./data/products.txt", "r", encoding="UTF-8") as file:
        lines = file.readlines()

    # If the file is empty
    if not lines:
        print("Nenhum produto encontrado...")
        return

    # Display registered products
    printTitle("Produtos cadastrados: ", GREEN, WHITE)
    print("\n")
    products = []
    for line in lines:
        # Create a Product object for each line of the file
        product_data = line.strip().split(";")
        product = Product(
            code=int(product_data[0].split(":")[1]),
            name=product_data[1].split(":")[1],
            description=product_data[2].split(":")[1],
            buying_price=float(product_data[3].split(":")[1]),
            selling_price=float(product_data[4].split(":")[1]),
        )
        products.append(product)

        # View product details
        print(f"Produto: {product.name}\nDescrição: {product.description}\nCódigo: {product.code}\nPreço de compra: R$ {product.buying_price}\nPreço de venda: R$ {product.selling_price}\n{'─'*80}")

    # Receive the product code that the user wants to delete
    try:
        product_code = int(input("Digite o código do produto que deseja apagar: "))
    except ValueError:
        print("Código inválido! Por favor, insira um número inteiro.")
        return
    
    # Check if the product with the code provided exists
    product_exists = any(p.code == product_code for p in products)
    if not product_exists:
        os.system('cls')
        printTitle("Erro: ", RED)
        drawBox(1, 4, 120, 6, MAGENTA)
        gotoxy(2, 5)
        print(f"Produto com código {product_code} não encontrado.")
        gotoxy(2, 8)
        print(input("Pressione ENTER para voltar ao menu..."))
        os.system('cls')
        main()
        return

    # Confirm removal
    os.system('cls')
    printTitle(f"Confirmar a remoção de produto de código: {product_code}...", RED, WHITE)
    
    # Filter products to remove the product with the given code
    products = [p for p in products if p.code != product_code]

    # Update the archive with remaining products
    with open("./data/products.txt", "w", encoding="UTF-8") as file:
        for product in products:
            # Rewrite each product in the file
            file.write(f"code:{product.code};name:{product.name};description:{product.description};buying_price:{product.buying_price};selling_price:{product.selling_price}\n")

    # Display the success message
    drawBox(1, 4, 120, 6, MAGENTA)
    gotoxy(2, 5)
    print(f"Produto de código {product_code} removido com sucesso.")
    
    gotoxy(2, 8)
    print(input("Pressione ENTER para voltar ao menu..."))
    os.system('cls')
    main()




def show_all_products():
    file = open("./data/products.txt", "r", encoding="UTF-8")

    if not file:
        print("Nenhum produto encontrado...")
    else:
        printTitle("Produtos cadastrados: ", GREEN, WHITE)
        print("\n")

        for line in file:
            # Create a Product object from each line
            product_data = line.strip().split(";")  # Split line on semicolon (';')
            product = Product(
                code=int(product_data[0].split(":")[1]),
                name=product_data[1].split(":")[1],
                description=product_data[2].split(":")[1],
                buying_price=float(product_data[3].split(":")[1]),
                selling_price=float(product_data[4].split(":")[1]),
            )
            # Print product details using the Product object
            print(f"Produto: {product.name}\nDescrição: {product.description}\nCódigo: {product.code}\nPreço de compra: R$ {product.buying_price}\nPreço de venda: R$ {product.selling_price}\n{'─'*80}")

    file.close()  # Close the file after processing
    input("\nPressione ENTER para continuar...")
    os.system('cls')  # Clear the screen
    main()

def update_product():
    # Open the file to read and get all products
    try:
        with open("./data/products.txt", "r", encoding="UTF-8") as file:
            lines = file.readlines()  # Read all lines of the file
    except FileNotFoundError:
        print("Erro: Arquivo de produtos não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return

    # Request the product code to be updated
    os.system('cls')
    drawBox(1, 1, 120, 25, MAGENTA)
    gotoxy(3, 3)
    product_code = int(input("Digite o código do produto que deseja atualizar: "))

    # Variable to store whether the product was found or not
    product_found= False

    # New content to be written to the file
    new_content = []

    for line in lines:
        product_data = line.strip().split(";")
        present_code = int(product_data[0].split(":")[1])

        if present_code == product_code:
            product_found = True  

            # Exibir os dados atuais do produto, um atributo por linha
            gotoxy(3, 4)
            print("Produto encontrado:")
            gotoxy(3, 5); print(f"Código: {present_code}")
            gotoxy(3, 6); print(f"Nome: {product_data[1].split(':')[1]}")
            gotoxy(3, 7); print(f"Descrição: {product_data[2].split(':')[1]}")
            gotoxy(3, 8); print(f"Preço de compra: {product_data[3].split(':')[1]}")
            gotoxy(3, 9); print(f"Preço de venda: {product_data[4].split(':')[1]}")
            gotoxy(3, 10); print("Deixe o campo vazio se não quiser alterar um atributo.")

            # Pegar os novos valores ou manter os antigos
            gotoxy(3, 11)
            new_name = input(f"Nome atual ({product_data[1].split(':')[1]}): ") or product_data[1].split(":")[1]
            gotoxy(3, 12)
            new_description = input(f"Descrição atual ({product_data[2].split(':')[1]}): ") or product_data[2].split(":")[1]
            gotoxy(3, 13)
            new_buy_price = input(f"Preço de compra atual ({product_data[3].split(':')[1]}): ") or product_data[3].split(":")[1]
            gotoxy(3, 14)
            new_sell_price = input(f"Preço de venda atual ({product_data[4].split(':')[1]}): ") or product_data[4].split(":")[1]

            # Recriar a linha com os dados atualizados
            updated_line = (f"Código: {present_code}; Nome do produto: {new_name}; "
                                f"Descrição: {new_description}; Preço de compra: {new_buy_price}; "
                                f"Preço de venda: {new_sell_price}\n")

            # Adicionar a linha atualizada ao novo conteúdo
            new_content.append(updated_line)
        else:
            # Manter as linhas não modificadas
            new_content.append(line)

    # Se o produto foi encontrado, reescrever o arquivo com os novos dados
    if product_found:
        with open("./data/products.txt", "w", encoding="UTF-8") as file:
            file.writelines(new_content)  # Reescreve o arquivo com os dados atualizados
        gotoxy(3, 15)
        print("Produto atualizado com sucesso!")
    else:
        gotoxy(3, 16)
        print(f"Produto com o código {product_code} não foi encontrado.")

    gotoxy(3, 17)
    input("Pressione ENTER para voltar ao menu...")
    os.system('cls')  # Limpar a tela
    main()