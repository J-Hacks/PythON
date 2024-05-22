import socket

def check_port(target_host):

    start_port = int(input("Enter start Port : "))

    end_port = int(input("Enter end Port : "))

    for port in range(start_port, end_port + 1):

        try:

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            client.settimeout(1)

            result = client.connect_ex((target_host, port))

            if result == 0:

                print(f"Port {port} is open")

            client.close()

        except Exception as e:

            print(f"Error checking port {port}: {str(e)}")

def choose(arg_ument):

    match arg_ument:

        case 0:

            return "Ra_nge"

        case 1:

            return "Single"

        # case 2:

        #     return "two"

        case default:

            return "something"

def check_port1(target_host):

    PORT = int(input("\nEnter Port : "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.settimeout(1)

    result = sock.connect_ex((target_host,PORT))

    if result == 0:

        print(f"\n{PORT} is open\n\n\n")

    else:

        print(f"\n{PORT} is not open\n\n\n\n")

    sock.close()

print('''CHOOSE YOUR OPTION :\n\n\t0-) To check between range of ports \n\n\t1-) To check single port ''')

arg_ument = int(input("\nEnter your option : "))

if choose(arg_ument) == "Ra_nge" :

    target_host = input("\nEnter IpAddress: ")

    check_port(target_host)

elif choose(arg_ument) == "Single" :

    target_host = input("\nEnter IpAddress: ")

    check_port1(target_host)

elif choose(arg_ument) == "something" :

    print("\n\nwrong option choosed\n\n")



   






