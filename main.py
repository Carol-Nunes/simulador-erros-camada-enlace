# Função auxiliar que lê a string de dados e verifica se ela é binária 
def read_data():

    while True:

        # A função strip tira espaços excedentes antes e depois ou quabras de linha. 
        data_bits = input("Enter the data bits: ").strip()

        valid = True 

        if data_bits == "":

            valid = False

        for bit in data_bits:

            if bit != "0" and bit != "1":

                valid = False 

                break

        if valid:

            return data_bits

        print("Invalid input! Enter a non-empty sequence of 0s and 1s.")
        print()


# Calcula o bit de paridade simples para uma string de bits.
def calculate_parity(data_bits: str, mode: str = "even"):

    ones_count = 0

    for bit in data_bits:

        if bit == "1":

            ones_count += 1

    if mode == "even":

        if ones_count % 2 == 0:

            return '0'

        else:

            return '1' 

    else:

        if ones_count % 2 == 0:

            return '1'

        else:

            return '0'

# Simula uma corrupção nos dados.
def noise_simulation(final_frame: str, allow_multiple: bool):

    print("NOISE SIMULATION")
    print()
    print("-" * 40)
    print()

    data_list = list(final_frame)

    while True:
         
        try:
         
            bit_position = int(input(f"Enter the bit position to invert (0 to {len(final_frame) - 1}): "))
            print()
         
            if 0 <= bit_position and bit_position < len(final_frame):
     
                if data_list[bit_position] == '1':
                     
                    data_list[bit_position] = '0'
                     
                else:
                     
                    data_list[bit_position] = '1'

                if not allow_multiple:

                    break


                while True:

                    cont_yes = input("Do you want to invert another bit to simulate a double error? (Y/N): ").strip().upper()
                    print()

                    if cont_yes == "Y" or cont_yes == "N":

                        break

                    print("Invalid option! Please enter Y or N.")
                    print()

                if cont_yes == 'N':
                
                    break
         
            else:
         
                print(f"Invalid position! Please enter an int number between 0 and {len(final_frame) - 1}")
                print()
         
        except ValueError:
         
            print(f"Invalid position! Please enter an int number between 0 and {len(final_frame) - 1}")
            print()
     
    received_frame = "".join(data_list)

    print(f"Received frame: {received_frame}")
    print()

    return received_frame


# Exibe o menu de opções para o cálculo de paridade simples.
def simple_parity_menu():

    print("SIMPLE PARITY MENU")
    print()
    print("-" * 40)
    print()

    data_bits = read_data()
    print()

    while True:

        try:

            option = int(input("Select an option [1. Even Parity | 2. Odd Parity]: "))
            print()

            if option == 1:

                print("You chose Even Parity.")
                print()
                mode_parity = "even"
                parity_bit = calculate_parity(data_bits)
                break

            if option == 2:

                print("You chose Odd Parity.")
                print()
                mode_parity = "odd"
                parity_bit = calculate_parity(data_bits, "odd")
                break

            else:

                print("Invalid option! Please enter 1 or 2.")
                print()

        except ValueError:

                print("Invalid option! Please enter 1 or 2.")
                print()

    final_frame = data_bits + parity_bit

    print(f"The parity bit is: {parity_bit}")
    print(f"Sent frame: {final_frame}")
    print()

    while True:
    
            try:
    
                noise_option = int(input("Select an option [1. Noise Simulation | 2. Exit]: "))
                print()
    
                if noise_option == 1:

                    received_frame = noise_simulation(final_frame, True)

                    ones_count = 0

                    for bit in received_frame:

                        if bit == "1":

                            ones_count += 1

                    if (mode_parity == "even" and ones_count % 2 == 0) or (mode_parity == "odd" and ones_count % 2 != 0):
                        
                        print("No error detected by parity checking.")
                        print()

                    else:
                        
                        print("Error detected! The frame was corrupted.")
                        print()
                    
                    break
    
                if noise_option == 2:

                    print(f"Received frame: {final_frame}")
                    print("Exit...")
                    print()
                    break
    
                else:
    
                    print("Invalid option! Please enter 1 or 2.")
                    print()
    
            except ValueError:
    
                print("Invalid option! Please enter 1 or 2.")
                print()

def bi_dimensional_parity_menu():

    print("BI-DIMENSIONAL PARITY MENU")
    print()
    print("-" * 40)
    print()
    
    data_bits = read_data()
    print()

    while True: 

        try:

            num_rows = int(input("Enter the number of rows: "))
            num_columns = int(input("Enter the number of columns: "))
            print()

            if num_rows > 0 and num_columns > 0 and num_rows * num_columns == len(data_bits):

                break

            print("Invalid values! Rows and columns must be positive, and their product must equal the number of bits.")
            print()

        except ValueError:

            print("Invalid values! Please enter int numbers.")
            print()

    matrix = []
    position = 0

    print("PARIDADE DAS LINHAS")
    print()

    for row_index in range(num_rows):

        row = []

        for column_index in range(num_columns):

            row.append(data_bits[position])
            position += 1

        parity_bit = calculate_parity("".join(row))
        row.append(parity_bit)
        matrix.append(row)

        print(f"Parity bit of row {row_index + 1}: {parity_bit}")

    #Calcula a paridade de todas as colunas. incluindo a coluna de paridade das linhas
    parity_row = []

    print("PARIDADE DAS COLUNAS")
    print()

    for column_index in range(num_columns + 1):

        column_bits = ""

        for row_index in range(num_rows):

            column_bits += matrix[row_index][column_index]

        parity_bit = calculate_parity(column_bits)
        parity_row.append(parity_bit)

        print(f"Parity bit of column {column_index + 1}: {parity_bit}")

    matrix.append(parity_row)

    print("Matriz enviada:")

    for row_index in range(len(matrix)):

        if row_index == len(matrix) - 1:

            print("-" * (2 * len(matrix[0]) + 2))

        print(" ".join(matrix[row_index][:-1]),"|",matrix[row_index][-1])

    print()

    while True:

        try:

            row = int(input(f"Insira a linha que sofrerá alteração (0 - {len(matrix) - 1}): "))
            print()

            if 0 <= row and row < len(matrix):

                final_frame = "".join(matrix[row])

                received_frame = noise_simulation(final_frame, False)

                break

            else:

                print(f"Linha inválida! Insira uma linha de 0 - {len(matrix) - 1}")
                print()

        except ValueError:

            print(f"Linha inválida! Insira um número inteiro.")
            print()

    received_matrix = []

    for original_row in matrix:

        received_matrix.append(original_row.copy())

    received_matrix[row] = list(received_frame)

    print("Matriz recebida:")
    
    for row_index in range(len(received_matrix)):
    
        if row_index == len(received_matrix) - 1:
    
            print("-" * (2 * len(received_matrix[0]) + 2))
    
        print(" ".join(received_matrix[row_index][:-1]),"|",received_matrix[row_index][-1])
    
    print()

    # O receptor vai procurar se houve algum erro, olhando as paridades das linhas e das colunas.
    error_row = None
    error_column = None

    # Verifica todas as linhas, inclusive a linha de paridades.
    for row_index in range(num_rows + 1):

        count_ones = 0

        for column_index in range(num_columns + 1):

            if received_matrix[row_index][column_index] == "1":

                count_ones += 1 

        if count_ones % 2 != 0:

            error_row = row_index

            break

    # Verifica todas as colunas, inclusive a coluna de paridades.
    for column_index in range(num_columns + 1):
    
            count_ones = 0
    
            for row_index in range(num_rows + 1):
    
                if received_matrix[row_index][column_index] == "1":
    
                    count_ones += 1 
    
            if count_ones % 2 != 0:
    
                error_column = column_index
    
                break

    print(f"Um erro foi detectado! Coordenadas do erro: ({error_row}, {error_column})")
    print("Começando as correções...")
    print()

    #Uma vez que o algoritmo sabe qual bit está errado, ele consegue arrumar
    if received_matrix[error_row][error_column] == "1":

        received_matrix[error_row][error_column] = "0"

    else:

       received_matrix[error_row][error_column] = "1"

    print("Matriz corrigida:")
         
    for row_index in range(len(received_matrix)):
         
        if row_index == len(received_matrix) - 1:
         
            print("-" * (2 * len(received_matrix[0]) + 2))
         
        print(" ".join(received_matrix[row_index][:-1]),"|",received_matrix[row_index][-1])
         
    print()


def menu():

    print("LINK LAYER ERROR SIMULATOR")
    print()
    print("-" * 40)
    print()

    option = 0

    while True:
        
                try:
        
                    option = int(input("Select an option [1. Simple Parity Simulation | 2. Bi-Dimensional Parity Simulation | 3. CRC Simulation | 4. Exit]: "))
                    print()
        
                    if option == 1:
        
                        print("You chose Simple Parity Simulation")
                        print()
                        simple_parity_menu()
        
                    elif option == 2:
        
                       print("You chose Bi-Dimensional Parity Simulation")
                       bi_dimensional_parity_menu()
                       print()

                    elif option == 3: 

                        print("You chose CRC Simulation")
                        print()

                    elif option == 4:

                        print("Exit...")
                        break
        
                    else:
        
                        print("Invalid option! Please enter 1, 2, 3 or 4.")
                        print()
        
                except ValueError:
        
                    print("Invalid option! Please enter 1, 2, 3 or 4.")
                    print()


if __name__ == "__main__":

    menu()

