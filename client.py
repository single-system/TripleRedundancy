#!/usr/bin/env python3           # This is client.py file

import socket
import random
import math

# create a socket object

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define the UDP_IP_ADDRESS and UDP_PORT_NO to use for the connection
hostname = socket.gethostname()  # get local machine name
host = socket.gethostbyname(hostname)
port = 8888
packet_data_size = 10  # 10 used during testing for convenience.


def lostpackets(rate, total_number_of_packets):
    """Take Packet loss rate in percentage and return a list of lost packets"""
    list_of_lost_packets = []
    if not rate:
        n_lost_packets = 0
    else:
        n_lost_packets = math.ceil(int(rate) * total_number_of_packets / 100)

    print(f'number of loss packet {n_lost_packets}')

    try:
        list_of_lost_packets = random.sample(range(1, int(total_number_of_packets)), int(n_lost_packets))
    except ValueError:
        print('Sample size exceeded population size.')

    return list_of_lost_packets


def send(data, lost_rate):
    """Sends packet"""
    total_sent = 0
    sent = 0
    counter = 0
    total_number_of_p = int(len(data) / packet_data_size)
    list_of_lost_packets = lostpackets(lost_rate, total_number_of_p)
    print(f'list of lost packets {list_of_lost_packets}, Total number of packets {total_number_of_p}')

    while total_sent < len(data) and len(data) > packet_data_size:

        chunk = total_sent + packet_data_size

        if counter in list_of_lost_packets:
            counter += 1
            total_sent = total_sent + packet_data_size
            continue
        else:
            try:
                counter_string = str(counter).rjust(3, '0')
                msg = bytes(counter_string, "utf-8") + data[total_sent: chunk]
                sent = clientSocket.sendto(msg, (host, port)) - len(bytes(str(counter_string), "utf-8"))
                print(f"{counter}.   {sent} bytes sent")
                print(f"Message sent:   {msg}\n")
            except socket.error:
                print(f"Server not available. Error Code")

        total_sent = total_sent + sent
        counter += 1
    else:
        try:
            if data[total_sent:] != b"":
                counter_string = str(counter).rjust(3, '0')
                msg = bytes(counter_string, "utf-8") + data[total_sent:]
                sent = clientSocket.sendto(msg, (host, port)) - len(bytes(str(counter_string), "utf-8"))
                print(f"{counter}.   {sent} bytes sent")
                print(f"Message sent:   {msg}\n")

        except socket.error:
            print(f"Server not available. Error Code")


def run_tests():
    # create 50 random messages
    # and time them
    msg = 'asd'
    rate = 10

    # finally save to file

    return msg, rate


def main(run_tests):
    # connection to hostname on the port.
    data = b''
    clientSocket.connect((host, port))

    if run_tests:
        msg, rate = run_tests()
    else:
        while True:

            msg = input('Enter message to send : ')
            rate = input('Enter loss rate : ')  # packet loss rate
            while not msg:
                msg = input('Enter message to send : ')

            msg = bytes(msg, "utf-8")

    # Set the whole string
    # Send Message
    # clientSocket.sendto(bytes(msg, "utf-8"), (host, port))
    for i in range(3):  # send msg 3 times
        try:
            send(msg, rate)
            # receive data from server (data, address)
            data, address = clientSocket.recvfrom(2048)

        except socket.error:
            print("Error Code")
            # sys.exit()
        print(f" Server reply: {data}")


if __name__ == '__main__':
    main()
