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

# Simula uma corrupção nos dados. Porém, só detecta o erro, não corrige. 
def noise_simulation(final_frame: str, mode_parity: str):

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

                try:

                    cont_yes = input("Do you want to invert another bit to simulate a double error? (Y/N): ").upper()
                    print()

                    if cont_yes != 'Y':

                        break

                except:

                    print("Invalid option! Please enter Y or N.")
                    print()
         
            else:
         
                print(f"Invalid position! Please enter an int number between 0 and {len(final_frame) - 1}")
                print()
         
        except ValueError:
         
            print(f"Invalid position! Please enter an int number between 0 and {len(final_frame) - 1}")
            print()
     
    received_frame = "".join(data_list)

    print(f"Received frame: {received_frame}")
    print()

    ones_count = 0

    for bit in received_frame:

        if bit == '1':

            ones_count += 1
     
    if (mode_parity == "even" and ones_count % 2 == 0) or (mode_parity == "odd" and ones_count % 2 != 0):

        print("No error detection. The frame is valid.")
        print()
                 
    else:
         
        print("Error detected! The frame was corrupted.")
        print()


# Exibe o menu de opções para o cálculo de paridade simples.
def simple_parity_menu():

    print("SIMPLE PARITY MENU")
    print()
    print("-" * 40)
    print()

    data_bits = input("Enter the data bits: ")
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

                    noise_simulation(final_frame, mode_parity)
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

