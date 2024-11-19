import os
import pyfiglet

#Path the directory of file
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)
current_directory = os.getcwd()

''' USER INPUT, FILE HANDLING, DAN HISTORY '''
#Menyimpan hasil kalkulasi ke dalam file .txt (History)
def save_calculation(ip_address, netmask, results):
    with open('ip_calc_history.txt', 'a') as f:
        f.write("\n" + "="*60 + "\n")
        f.write(f"IP Address: {ip_address}\n")
        f.write(f"Netmask: {netmask}\n")
        f.write("="*27 + "RESULT" + "="*27 + "\n")
        for key, value in results.items():
            f.write(f"{key}: {value}\n")
        f.write("="*60 + "\n")


#Display calculation history
def view_history():
    try:
        with open('ip_calc_history.txt', 'r') as f:
            baca = f.read()
            result = pyfiglet.figlet_format('Your History')
            if baca == '':
                print("="*50 + "\n")
                print(result)
                print("="*60)
                print("\nHistory kosong! Silahkan lakukan perhitungan kembali...")
            else:
                with open('ip_calc_history.txt', 'r') as f:
                    print("="*60 + "\n")
                    print(result)
                    print(f.read())
    except FileNotFoundError:
        print("="*60)
        print("\nHistory kalkulasi tidak ditemukan.")


#Clear calculation results from a text file
def clear_history():
    try:
        # Cek keberadaan file
        try:
            with open('ip_calc_history.txt', 'r') as f:
                baca = f.read()
        except FileNotFoundError:
            print("="*60)
            print("\nFile history tidak ditemukan. Lakukan kalkulasi dahulu...")
            return
        
        # Jika file kosong
        if baca == '':
            print("="*60)
            print("\nHistory kosong! Silahkan lakukan perhitungan kembali...")
        else:
            with open('ip_calc_history.txt', 'w') as f:
                f.write('')
            print("="*60)
            print("\nHistory telah dibersihkan!")
    except Exception as e:
        print(f"Error: {e}")


def delete_history():
    history_file = 'ip_calc_history.txt'
    if os.path.exists(history_file):
        try:
            os.remove(history_file)
            print("="*60 + "\n")
            print("History file deleted successfully.")
        except OSError as e:
            print("="*60 + "\n")
            print(f"Error deleting the file: {e}")
    else:
        print("="*60 + "\n")
        print("No history file found.")


def increment_calculation_count():
    count_file = 'calculation_count.txt'
    if not os.path.exists(count_file) or os.path.getsize(count_file) == 0:
        with open(count_file, 'w') as f:
            f.write('0')

    try:
        with open(count_file, 'r') as f:
            count = int(f.read().strip())
    except (ValueError, OSError) as e:
        print(f"Error reading count file: {e}. Resetting count to 0.")
        count = 0

    count += 1

    with open(count_file, 'w') as f:
        f.write(str(count))
    print("="*60 + "\n")
    print(f"Total calculations performed: {count}")


def display_calculation_count():
    count_file = 'calculation_count.txt'
    if not os.path.exists(count_file) or os.path.getsize(count_file) == 0:
        print("="*60 + "\n")
        print("Total calculations performed: 0")
        return

    try:
        with open(count_file, 'r') as f:
            count = int(f.read().strip())
        print("="*60 + "\n")
        print(f"Total calculations performed: {count}")
    except (ValueError, OSError) as e:
        print(f"Error reading count file: {e}.")


''' DISPLAY START FUNCTION '''
def display_start():
    result = pyfiglet.figlet_format('IP Calculator')
    print(result)
display_start()

#Input The IP Address and Prefix 
def get_user_input():
    while True:
        print("\n" + "="*60)
        print("1. Calculate new IP")
        print("2. View history")
        print("3. Clear history")
        print("4. Delete file history")
        print("5. Increment calculation count")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            print("\n"+"="*60)
            netmask = int(input("Input Prefix = "))
            ip_address = input("Input IP Address = ")
            if ip_address.count('.') != 3 or len(ip_address) > 15 or len(ip_address) < 7 or ip_address[0] == '0':
                continue
            else:
                return netmask, ip_address
        elif choice == '2':
            view_history()
        elif choice == '3':
            clear_history()
        elif choice == '4':
            delete_history()
        elif choice == '5':
            display_calculation_count()
        elif choice == '6':
            exit()
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")


''' KALKULASI IP ADDRESS DAN SUBNETMASK '''
#Function for Sum IP Address for full IP and host IP
def sumIP(prefix):
    if prefix >= 24:
        print("\n(Kelas C)")
    elif prefix < 24 and prefix >=16:
        print("\n(Kelas B)")
    else:
        print("\n(Kelas A)")
    
    full_IP = 2**(32-prefix)
    host_IP = full_IP - 2
    return full_IP,host_IP

# Function for Calculate The Subnetmask (Class B and C) like 255.255.255.0 --> /24
def subnetting(full_IP,netmask):
    #Class C
    if netmask >= 24:
        subnetmask = 256 - full_IP
        return f'255.255.255.{subnetmask}'
    #Class B
    elif netmask < 24 and netmask >= 16:
        subnetmask = 256 - (full_IP // 256)
        return f'255.255.{subnetmask}.0'
    #Class A
    elif netmask < 16 and netmask >= 8:
        subnetmask = 256 - (full_IP // (256**2))
        return f'255.{subnetmask}.0.0'
    else:
        print("Invalid Prefix")

# Function for Calculate Network Address from The Particular Network
def networkIP(x, jumlahIP):
    #Class C
    if jumlahIP <= 256:
        Networks = x.split('.')
        Network = int(Networks[3])
        if Network < jumlahIP:
            Networks.insert(3,0)
            Networks.pop()
            octetNet = ""
            for i in Networks:
                octetNet += (str(i) + '.')
            return octetNet[:-1]
        else:
            operation = (int(Networks[3]) // jumlahIP) * jumlahIP
            Networks.insert(3,operation)
            Networks.pop()
            octetNet = ""
            for i in Networks:
                octetNet += (str(i) + '.')
            return octetNet[:-1]
    #Class B
    elif jumlahIP > 256 and jumlahIP <= (256**2):
        Networks = x.split('.')
        Network = int(Networks[2])
        if Network < (jumlahIP / 256):
            Networks.insert(2,0)
            Networks.insert(3,0)
            del Networks[4:]
            octetNet = ""
            for i in Networks:
                octetNet += (str(i) + '.')
            return octetNet[:-1]
        else:
            jumlahIP = jumlahIP // 256
            operation = (int(Networks[3]) // jumlahIP) * jumlahIP
            Networks.insert(2,operation)
            Networks.insert(3,0)
            del Networks[4:]
            octetNet = ""
            for i in Networks:
                octetNet += (str(i) + '.')
            return octetNet[:-1]
    #Class A
    else:
        Networks = x.split('.')
        Network = int(Networks[1])
        if Network < (jumlahIP // (256**2)):
            Networks.insert(1,0)
            Networks.insert(2,0)
            Networks.insert(3,0)
            del Networks[4:]
            octetNet = ""
            for i in Networks:
                octetNet += (str(i) + '.')
            return octetNet[:-1]
        else:
            jumlahIP = jumlahIP // (256**2)
            operation = (int(Networks[1]) // jumlahIP) * jumlahIP
            Networks.insert(1,operation)
            Networks.insert(2,0)
            Networks.insert(3,0)
            del Networks[4:]
            octetNet = ""
            for i in Networks:
                octetNet += (str(i) + '.')
            return octetNet[:-1]

# Function for Calculate Broadcast Address from The Particular Network
def broadcastIP(x, jumlahIP):
    #Class C
    if jumlahIP <= 256:
        Network = x.split('.')
        Networks = int(Network[3])
        Broadcast = Networks + jumlahIP - 1
        Network.insert(3,Broadcast)
        Network.pop()
        octetBroad = ''
        for i in Network:
            octetBroad += (str(i) + '.')
        return octetBroad[:-1]
    #Class B
    elif jumlahIP > 256 and jumlahIP <= (256**2):
        Network = x.split('.')
        Networks = int(Network[2])
        Broadcast = Networks + (jumlahIP // 256) - 1
        Network.insert(2,Broadcast)
        Network.insert(3,255)
        del Network[4:]
        octetBroad = ''
        for i in Network:
            octetBroad += (str(i) + '.')
        return octetBroad[:-1]
    #Class A
    else:
        Network = x.split('.')
        Networks = int(Network[1])
        Broadcast = Networks + (jumlahIP // (256**2)) - 1
        Network.insert(1,Broadcast)
        Network.insert(2,255)
        Network.insert(3,255)
        del Network[4:]
        octetBroad = ''
        for i in Network:
            octetBroad += (str(i) + '.')
        return octetBroad[:-1]

def rangeIP(first, last, netmask):
    #Class C
    if netmask >= 24:
        firstRange = first.split('.')
        lastRange = last.split('.')

        firstIP = int(firstRange[3]) + 1
        lastIP = int(lastRange[3]) - 1

        # Insert the first IP for Range Host
        firstRange.insert(3,firstIP)
        firstRange.pop()
        firstRangeHost = ''
        for i in firstRange:
            firstRangeHost += (str(i) + '.')

        # Insert the last IP for Range Host
        lastRange.insert(3,lastIP)
        lastRange.pop()
        lastRangeHost = ''
        for i in lastRange:
            lastRangeHost += (str(i) + '.')

        return {
            'full_range': f"{first} - {last}",
            'host_range': f"{firstRangeHost[:-1]} - {lastRangeHost[:-1]}"
        }
    #Class B
    elif netmask < 24 and netmask >= 16:
        firstRange = first.split('.')
        lastRange = last.split('.')

        firstIP = int(firstRange[2])  
        lastIP = int(lastRange[2]) 

        # Insert the first IP for Range Host
        firstRange.insert(2,firstIP)
        firstRange.insert(3,1)
        del firstRange[4:]
        firstRangeHost = ''
        for i in firstRange:
            firstRangeHost += (str(i) + '.')

        # Insert the last IP for Range Host
        lastRange.insert(2,lastIP)
        lastRange.insert(3,254)
        del lastRange[4:]
        lastRangeHost = ''
        for i in lastRange:
            lastRangeHost += (str(i) + '.')

        return {
            'full_range': f"{first} - {last}",
            'host_range': f"{firstRangeHost[:-1]} - {lastRangeHost[:-1]}"
        }
    #Class A
    else:
        firstRange = first.split('.')
        lastRange = last.split('.')

        firstIP = int(firstRange[1])  
        lastIP = int(lastRange[1]) 

        # Insert the first IP for Range Host
        firstRange.insert(1,firstIP)
        firstRange.insert(2,0)
        firstRange.insert(3,1)
        del firstRange[4:]
        firstRangeHost = ''
        for i in firstRange:
            firstRangeHost += (str(i) + '.')

        # Insert the last IP for Range Host
        lastRange.insert(1,lastIP)
        lastRange.insert(2,255)
        lastRange.insert(3,254)
        del lastRange[4:]
        lastRangeHost = ''
        for i in lastRange:
            lastRangeHost += (str(i) + '.')

        return {
            'full_range': f"{first} - {last}",
            'host_range': f"{firstRangeHost[:-1]} - {lastRangeHost[:-1]}"
        }


''' RUN PROGRAM UTAMA '''
def main():
    while True:
        netmask, ip_address = get_user_input()
        # Calculate results
        full_IP, host_IP = sumIP(netmask)
        subnet = subnetting(full_IP,netmask)
        network = networkIP(ip_address, full_IP)
        broadcast = broadcastIP(network, full_IP)
        range_ips = rangeIP(network, broadcast, netmask)
        
        # Prepare results dictionary
        results = {
            'Total IP': full_IP,
            'Total Host': host_IP,
            'Subnetmask': subnet,
            'Network Address': network,
            'Broadcast Address': broadcast,
            'Range IP': range_ips['full_range'],
            'Range Host': range_ips['host_range']
        }
        
        # Display results
        print("="*60)
        for key, value in results.items():
            print(f"{key}: {value}")
        print("="*60)
        
        # Save calculation to history
        save_calculation(ip_address, netmask, results)
        increment_calculation_count()

if __name__ == "__main__":
    main()