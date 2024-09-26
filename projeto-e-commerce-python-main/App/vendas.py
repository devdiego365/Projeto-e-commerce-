import os
from security import *
import time
import re
from TextUtils import *
from datetime import datetime
from produto import *


def show_sales_history():
    clearScreen()
    printTitle("Histórico de Vendas", BLUE, WHITE)
    
    try:
        # Open the sales file
        with open("./data/sell_log.txt", "r", encoding="utf-8") as sell_file:
            sales = sell_file.readlines()

            if not sales:
                gotoxy(1, 5)
                print("Nenhuma venda registrada.")
                gotoxy(1, 6)
                input("Pressione ENTER para voltar ao menu...")
                return

        # View all sales

        for i, sale in enumerate(sales, start=1):
            gotoxy(2, 3 + i)
            print(f"{sale.strip()}")

        # After displaying sales, ask the user to press ENTER to return to the main menu
        gotoxy(2, 5 + i)
        input("Pressione ENTER para voltar ao menu...")

    except FileNotFoundError:
        gotoxy(2, 5)
        print("Erro: Arquivo de vendas não encontrado.")
        gotoxy(2, 6)
        input("Pressione ENTER para voltar ao menu...")
    except Exception as e:
        gotoxy(2, 5)
        print(f"Erro inesperado: {e}")
        gotoxy(2, 6)
        input("Pressione ENTER para voltar ao menu...")

    clearScreen()



def show_cancelled_sales_history():
    clearScreen()
    printTitle("Histórico de Vendas Canceladas", WHITE)
    
    try:
        # Open the canceled sales file
        with open("./data/canceled_sales.txt", "r", encoding="utf-8") as cancel_file:
            cancelled_sales = cancel_file.readlines()
            
            if not cancelled_sales:
                gotoxy(1, 5)
                print("Nenhuma venda cancelada registrada.")
                gotoxy(1, 6)
                input("Pressione ENTER para voltar ao menu...")
                main()
            else:
                # Variable to control the print line
                start_row = 5
                
                for sale in cancelled_sales:
                    gotoxy(2, start_row)
                    print(sale.strip())
                    
                    
                    start_row += 1

                gotoxy(1, start_row + 1)
                input("Pressione ENTER para voltar ao menu...")
                main()

    except FileNotFoundError:
        gotoxy(1, 5)
        print("Erro: Arquivo de vendas canceladas não encontrado.")
        gotoxy(1, 6)
        input("Pressione ENTER para voltar ao menu...")



def new_sale():
    clearScreen()
    printTitle("Nova Venda", MAGENTA, MAGENTA)

    try:
        with open("./data/products.txt", "r", encoding="utf-8") as file:
            products = []
            date_regex = re.compile(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$")

            for line in file:
                try:
                    fields = line.strip().split(";")
                    if len(fields) < 5:
                        gotoxy(2, 7)
                        print(f"Erro ao processar a linha: {line}. Formatação incorreta.")
                        continue
                    
                    code = int(fields[0].split(":")[1].strip())
                    name = fields[1].split(":")[1].strip()
                    selling_price = float(fields[4].split(":")[1].strip())
                    
                    products.append((code, name, selling_price))

                except (IndexError, ValueError) as e:
                    gotoxy(2, 7)
                    print(f"Erro ao processar a linha: {line}. Erro: {e}")
                    continue
            
            if not products:
                gotoxy(2, 7)
                print("Nenhum produto disponível para venda.")
                return

            drawBox(1, 5, 120, 16, WHITE)
            gotoxy(2, 6)
            selected_product = int(input("Digite o código do produto: "))
            product_found = next((p for p in products if p[0] == selected_product), None)

            if product_found:
                gotoxy(2, 7)
                print(f"Produto selecionado: {product_found[1]} - Preço de venda: R${product_found[2]:.2f}")
                
                gotoxy(2, 8)
                quantity = int(input("Digite a quantidade: "))
                
                gotoxy(2, 9)
                while True:
                    selling_date = input("Digite a data da venda (dd/mm/aaaa): ")
                    if re.match(date_regex, selling_date):
                        break
                    gotoxy(2, 10)
                    print("Erro: Data inválida. Formato dd/mm/aaaa.")

                gotoxy(2, 11)
                payment_method = input("Informe o método de pagamento: ")

                # Generate a new sales ID based on previous sales
                try:
                    with open("./data/sell_log.txt", "r", encoding="utf-8") as sell_file:
                        last_sale = sell_file.readlines()[-1]
                        last_id = int(last_sale.split(";")[0].split(":")[1].strip())
                        sale_id = last_id + 1
                except (FileNotFoundError, IndexError):
                    # If the file does not exist or is empty, we start with ID 1
                    sale_id = 1

                # Sell ​​instance creation
                sale = Sell(
                    id=sale_id,
                    item=product_found[1],
                    price=product_found[2],
                    quantity=quantity,
                    date=selling_date,
                    payment_method=payment_method
                )

                # Record the sale in the log file
                with open("./data/sell_log.txt", "a", encoding="utf-8") as sell_file:
                    sell_file.write(str(sale) + "\n")

                # View sale confirmation
                gotoxy(2, 12)
                printColored(f"Venda ID {sale_id} realizada: {quantity}x {product_found[1]} a R${product_found[2]:.2f} cada com {payment_method} como forma de pagamento.", GREEN)
                gotoxy(2, 13)
                print(f"Total: R${sale.total_price:.2f}")
                gotoxy(2, 14)
                input("Pressione ENTER para voltar ao menu...")
                main()

            else:
                gotoxy(2, 15)
                printColored("Erro: Produto não encontrado.", RED)

    except FileNotFoundError:
        gotoxy(2, 7)
        print("Erro: Arquivo de produtos não encontrado.")
    except Exception as e:
        gotoxy(2, 7)
        print(f"Erro inesperado: {e}")


    except FileNotFoundError:
        print("Erro: Arquivo de produtos não encontrado.")
    except Exception as e:
        print(f"Erro inesperado: {e}")


def cancel_sale():
    clearScreen()
    printTitle("Cancelar Venda", RED, RED)
    
    try:
        # Open the sales file
        with open("./data/sell_log.txt", "r", encoding="utf-8") as sell_file:
            sales = sell_file.readlines()
            
            if not sales:
                gotoxy(1, 5)
                print("Nenhuma venda registrada.")
                gotoxy(1, 6)
                input("Pressione ENTER para voltar ao menu...")
                main()

        # Show all recorded sales
        gotoxy(1, 5)
        print("Vendas registradas:\n")
        for sale in sales:
            print(f"{sale.strip()}")

        # Request the ID of the sale to be canceled
        sale_id = int(input("\nDigite o ID da venda que deseja cancelar (ou '0' para cancelar a operação): "))

        if sale_id == 0:
            os.system('cls')
            printTitle("Cancelamento de venda abortado.", GREEN)
            gotoxy(1, 5)
            input("Pressione ENTER para voltar ao menu...")
            main()

        # Check if the entered ID is valid
        sale_found = None
        for sale in sales:
            sale_data = sale.split(";")
            if int(sale_data[0].split(":")[1].strip()) == sale_id:
                sale_found = sale
                break

        if not sale_found:
            os.system('cls')
            printTitle("Erro: Venda com ID não encontrada.", RED)
            gotoxy(1, 5)
            input("Pressione ENTER para voltar ao menu...")
            main()

        # Remove the found sale from the list
        sales.remove(sale_found)

        # Save remaining sales to file by overwriting original file
        with open("./data/sell_log.txt", "w", encoding="utf-8") as sell_file:
            sell_file.writelines(sales)

        # Record cancellation in a new cancellation log file
        with open("./data/canceled_sales.txt", "a", encoding="utf-8") as cancel_file:
            cancel_file.write(f"Venda cancelada: {sale_found.strip()}\n")

        os.system('cls')
        printTitle(f"A venda com ID {sale_id} foi cancelada com sucesso.", MAGENTA)
        gotoxy(1, 5)
        input("Pressione ENTER para voltar ao menu...")

    except FileNotFoundError:
        os.system('cls')
        printTitle("Erro: Arquivo de vendas não encontrado.", YELLOW)
        gotoxy(2, 5)
        input("Pressione ENTER para voltar ao menu...")
    except ValueError:
        os.system('cls')
        printTitle("Erro: Entrada inválida, por favor digite um número.")
        gotoxy(2, 5)
        input("Pressione ENTER para voltar ao menu...")
    except Exception as e:
        os.system('cls')
        print(f"Erro inesperado: {e}")
        gotoxy(2, 5)
        input("Pressione ENTER para voltar ao menu...")

    clearScreen()
    main()


