# Função auxiliar que lê a string de dados e verifica se ela é binária.
def read_data(message: str):

    while True:

        # A função strip tira espaços antes e depois ou quebras de linha.
        data_bits = input(message).strip()

        valid = True

        if data_bits == "":

            valid = False

        for bit in data_bits:

            if bit != "0" and bit != "1":

                valid = False

                break

        if valid:

            return data_bits

        print("Entrada inválida! Digite uma sequência não vazia de 0s e 1s.")
        print()


# Calcula o bit de paridade simples para uma string de bits.
def calculate_parity(data_bits: str, mode: str = "even"):

    ones_count = 0

    for bit in data_bits:

        if bit == "1":

            ones_count += 1

    # Se a paridade for par, a quantidade de 1s precisa ser par. 
    if mode == "even":

        if ones_count % 2 == 0:

            return "0"
        
        else:

            return "1"
        
    # Se a paridade for ímpar, a quantidade de 1s precisa ser ímpar.   
    else:

        if ones_count % 2 == 0:

            return "1"
        else:

            return "0"


# Simula uma corrupção nos dados.
# O parâmetro "allow_multiple" foi usado só para permitir uma generalização de função. 
# Pois os menus 1 e 3 não tem restrição quanto a quantidade de erros, mas o 2 tem. 
def noise_simulation(final_frame: str, allow_multiple: bool):

    print("SIMULAÇÃO DE RUÍDO")
    print()
    print("-" * 40)
    print()

    data_list = list(final_frame)

    while True:

        try:

            bit_position = int(input(f"Digite a posição do bit que deseja inverter (0 a {len(final_frame) - 1}): "))
            print()

            if 0 <= bit_position and bit_position < len(final_frame):

                if data_list[bit_position] == "1":

                    data_list[bit_position] = "0"

                else:

                    data_list[bit_position] = "1"

                # Se a flag de mais erros injetados estiver ativa, esse loop roda novamente poderia rodar novamente, 
                # caso o usuário informasse que deseja adicionar mais erros de bits. 
                if not allow_multiple:

                    break

                while True:

                    cont_yes = input("Deseja inverter outro bit? (S/N): ").strip().upper()
                    print()

                    if cont_yes == "S" or cont_yes == "N":

                        break

                    print("Opção inválida! Digite S ou N.")
                    print()

                if cont_yes == "N":

                    break

            else:

                print(f"Posição inválida! Digite um número inteiro entre 0 e {len(final_frame) - 1}.")
                print()

        except ValueError:

            print(f"Posição inválida! Digite um número inteiro entre 0 e {len(final_frame) - 1}.")
            print()

    received_frame = "".join(data_list)

    print(f"Quadro enviado: {final_frame}")
    print(f"Quadro recebido: {received_frame}")
    print()

    return received_frame


# Divisão bit a bit usando XOR para cálculo do CRC.
def modulo_two_division(extended_data: str, generator: str):
    
    actual_bits = list(extended_data)
    generator_size = len(generator)

    # Roda o XOR no dado estendido. Conforme o 'pos' avança, 
    # a gente ignora o 0 que sobrou na esquerda e já puxa 
    # o próximo bit que vem vindo na sequência.
    for pos in range(len(actual_bits) - generator_size + 1):

        if actual_bits[pos] == "1":

            before = "".join(actual_bits[pos:pos + generator_size])

            # Fazemos o XOR.
            for offset in range(generator_size):

                if actual_bits[pos + offset] == generator[offset]:

                    # Bits iguais.
                    actual_bits[pos + offset] = "0"

                else:

                    # Bits diferentes.
                    actual_bits[pos + offset] = "1"

            after = "".join(actual_bits[pos:pos + generator_size])

            print(f"{before} XOR {generator} = {after}")
            print(f"Sequência atual: {''.join(actual_bits)}")
            print()

    crc_size = generator_size - 1

    # Retorna os últimos bits do tamanho do grau, que são o resto.
    return "".join(actual_bits[-crc_size:])


# Exibe o menu de opções para o cálculo de paridade simples.
def simple_parity_menu():

    print("MENU DE PARIDADE SIMPLES")
    print()
    print("-" * 40)
    print()

    data_bits = read_data("Digite os bits de dados: ")
    print()

    while True:

        try:

            option = int(input("Selecione uma opção [1. Paridade par | 2. Paridade ímpar]: "))
            print()

            if option == 1:

                print("Você escolheu paridade par.")
                print()

                mode_parity = "even"
                parity_bit = calculate_parity(data_bits)
                break

            if option == 2:

                print("Você escolheu paridade ímpar.")
                print()

                mode_parity = "odd"
                parity_bit = calculate_parity(data_bits, "odd")
                break

            else:

                print("Opção inválida! Digite 1 ou 2.")
                print()

        except ValueError:

            print("Opção inválida! Digite 1 ou 2.")
            print()

    final_frame = data_bits + parity_bit

    print(f"Bit de paridade: {parity_bit}")
    print(f"Quadro enviado: {final_frame}")
    print()

    while True:

        try:

            noise_option = int(input("Selecione uma opção [1. Simulação de ruído | 2. Sem ruído]: "))
            print()

            if noise_option == 1:

                print(f"Quadro enviado: {final_frame}")

                received_frame = noise_simulation(final_frame, True)

            elif noise_option == 2:

                print(f"Quadro enviado: {final_frame}")

                received_frame = final_frame

                print(f"Quadro recebido: {received_frame}")

                print()

            else:
                print("Opção inválida! Digite 1 ou 2.")
                print()
                continue 

            # O receptor sempre faz a verificação, independentemente se há ruído ou não. 
            # Até porque ele não sabe se tem ruído ou não. 
            print("Iniciando verificação no recetor...")

            ones_count = 0

            for bit in received_frame:

                if bit == "1":

                    ones_count += 1

            if ((mode_parity == "even" and ones_count % 2 == 0) or (mode_parity == "odd" and ones_count % 2 != 0)):
                
                print("Nenhum erro detectado pela verificação de paridade.")
                print()

            else:

                print("Erro detectado! O quadro foi corrompido.")
                print()

            break

        except ValueError:

            print("Opção inválida! Digite 1 ou 2.")
            print()


def bi_dimensional_parity_menu():

    print("MENU DE PARIDADE BIDIMENSIONAL")
    print()
    print("-" * 40)
    print()

    data_bits = read_data("Digite os bits de dados: ")
    print()

    while True:

        try:

            num_rows = int(input("Digite o número de linhas: "))
            num_columns = int(input("Digite o número de colunas: "))
            print()

            if (num_rows > 0 and num_columns > 0 and num_rows * num_columns == len(data_bits)):
                
                break

            print("Valores inválidos! As quantidades de linhas e colunas devem ser positivas, e o produto delas deve ser igual à quantidade de bits.")
            print()

        except ValueError:

            print("Valores inválidos! Digite números inteiros.")
            print()

    matrix = []
    position = 0

    print("PARIDADE DAS LINHAS")
    print()

    # Aqui, além de colocarmos os dados na matriz, também calulamos 
    # a paridade das linhas. 
    for row_index in range(num_rows):

        row = []

        for column_index in range(num_columns):

            row.append(data_bits[position])

            position += 1

        parity_bit = calculate_parity("".join(row))

        row.append(parity_bit)

        matrix.append(row)

        print(f"Bit de paridade da linha {row_index + 1}: {parity_bit}")

    # Calcula a paridade de todas as colunas,
    # incluindo a coluna de paridade das linhas.
    parity_row = []

    print("PARIDADE DAS COLUNAS")
    print()

    for column_index in range(num_columns + 1):

        column_bits = ""

        for row_index in range(num_rows):

            column_bits += matrix[row_index][column_index]

        parity_bit = calculate_parity(column_bits)

        parity_row.append(parity_bit)

        print(f"Bit de paridade da coluna {column_index + 1}: {parity_bit}")

    matrix.append(parity_row)

    print("Matriz enviada:")

    for row_index in range(len(matrix)):

        if row_index == len(matrix) - 1:

            print("-" * (2 * len(matrix[0]) + 2))

        print(" ".join(matrix[row_index][:-1]), "|", matrix[row_index][-1])

    print()

    # Inserindo erro de um bit. 
    while True:

        try:

            row = int(input(f"Insira a linha que sofrerá alteração (0 a {len(matrix) - 1}): "))
            print()

            if 0 <= row and row < len(matrix):

                final_frame = "".join(matrix[row])

                received_frame = noise_simulation(final_frame, False)

                break

            else:
                print(f"Linha inválida! Insira uma linha de 0 a {len(matrix) - 1}.")
                print()

        except ValueError:

            print("Linha inválida! Insira um número inteiro.")
            print()

    # Faz uma cópia da matriz original e altera a linha que sofreu 
    # erro de bit. 
    received_matrix = []

    for original_row in matrix:

        received_matrix.append(original_row.copy())

    received_matrix[row] = list(received_frame)

    print("Matriz enviada:")

    for row_index in range(len(matrix)):

        if row_index == len(matrix) - 1:

            print("-" * (2 * len(matrix[0]) + 2))

        print(" ".join(matrix[row_index][:-1]), "|", matrix[row_index][-1])

    print()

    print("Matriz recebida:")

    for row_index in range(len(received_matrix)):

        if row_index == len(received_matrix) - 1:

            print("-" * (2 * len(received_matrix[0]) + 2))

        print(" ".join(received_matrix[row_index][:-1]), "|", received_matrix[row_index][-1])

    print()

    error_row = None
    error_column = None

    # Receptor verifica todas as linhas, inclusive a linha de paridades.
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

    # Faz uma cópia da matriz recebida e corrige a linha que sofreu 
    # erro de bit. 
    corrected_matrix = []

    for row in received_matrix:

        corrected_matrix.append(row.copy())

    # Uma vez que o algoritmo sabe qual bit está errado,
    # ele consegue arrumar.
    if corrected_matrix[error_row][error_column] == "1":

        corrected_matrix[error_row][error_column] = "0"

    else:

        corrected_matrix[error_row][error_column] = "1"

    print("Matriz enviada:")

    for row_index in range(len(matrix)):

        if row_index == len(matrix) - 1:

            print("-" * (2 * len(matrix[0]) + 2))

        print(" ".join(matrix[row_index][:-1]), "|", matrix[row_index][-1])

    print()

    print("Matriz recebida:")

    for row_index in range(len(received_matrix)):

        if row_index == len(received_matrix) - 1:

            print("-" * (2 * len(received_matrix[0]) + 2))

        print(" ".join(received_matrix[row_index][:-1]), "|", received_matrix[row_index][-1])

    print()

    print("Matriz corrigida:")

    for row_index in range(len(corrected_matrix)):

        if row_index == len(corrected_matrix) - 1:

            print("-" * (2 * len(corrected_matrix[0]) + 2))

        print(" ".join(corrected_matrix[row_index][:-1]),"|", corrected_matrix[row_index][-1])

    print()


def crc_menu():

    print("MENU CRC")
    print()
    print("-" * 40)
    print()

    data_bits = read_data("Digite os bits de dados: ")
    print()

    while True:

        generator = read_data("Digite o polinômio gerador em binário: ")
        print()

        # O gerador tem que começar com 1 pro grau do polinômio ficar certo
        # e terminar com 1 pro termo constante não sumir (o que geraria um fator x).
        if (len(generator) >= 2 and generator[0] == "1" and generator[-1] == "1"):

            break

        print("Polinômio gerador inválido! Use pelo menos 2 bits, começando e terminando com 1.")
        print()

    # Calulamos o grau do polinômio gerador a fim de saber quantos appends de zeros
    # vamos ter que fazer nos dados. 
    degree = len(generator) - 1

    extended_data = data_bits + "0" * degree

    print(f"Dados: {data_bits}")
    print(f"Polinômio gerador: {generator}")
    print(f"Grau do polinômio: {degree}")
    print(f"Dados estendidos: {extended_data}")
    print()

    # Transmissor calcula o CRC e envia os dados + CRC calculado.
    crc = modulo_two_division(extended_data, generator)
    final_frame = data_bits + crc

    print(f"CRC: {crc}")
    print(f"Quadro enviado: {final_frame}")
    print()

    while True:

        try:
            noise_option = int(input("Selecione uma opção [1. Simulação de ruído | 2. Sem ruído]: "))
            print()

            if noise_option == 1:

                print(f"Quadro enviado: {final_frame}")
                received_frame = noise_simulation(final_frame, True)

            elif noise_option == 2:

                received_frame = final_frame

            else:

                print("Opção inválida! Digite 1 ou 2.")
                print()
                continue

            # O receptor divide o quadro recebido, sem adicionar zeros.
            # E ele faz isso sempre, independentemente se teve ruído ou não,
            # até porque ele não sabe se teve ou não. 
            receiver_crc = modulo_two_division(received_frame, generator)

            print(f"Quadro enviado: {final_frame}")
            print(f"Quadro recebido: {received_frame}")
            print(f"CRC no receptor: {receiver_crc}")

            # Se o resto no receptor (crc) for 0, quer dizer que o quadro 
            # está intacto. 
            if receiver_crc == "0" * degree:

                print("Nenhum erro detectado pela verificação de CRC.")
                print()
                break

            else:

                print("Erro detectado! O quadro foi corrompido.")
                print()
                break

        except ValueError:

            print("Opção inválida! Digite 1 ou 2.")
            print()


def menu():

    print("SIMULADOR DE ERROS DA CAMADA DE ENLACE")
    print()
    print("-" * 40)
    print()

    option = 0

    while True:

        try:

            option = int(input("Selecione uma opção [1. Simulação de paridade simples | 2. Simulação de paridade bidimensional | 3. Simulação de CRC | 4. Sair]: "))
            print()

            if option == 1:

                print("Você escolheu a simulação de paridade simples.")
                print()
                simple_parity_menu()

            elif option == 2:

                print("Você escolheu a simulação de paridade bidimensional.")
                bi_dimensional_parity_menu()
                print()

            elif option == 3:

                print("Você escolheu a simulação de CRC.")
                crc_menu()
                print()

            elif option == 4:

                print("Encerrando...")
                break

            else:

                print("Opção inválida! Digite 1, 2, 3 ou 4.")
                print()

        except ValueError:

            print("Opção inválida! Digite 1, 2, 3 ou 4.")
            print()


if __name__ == "__main__":
    menu()