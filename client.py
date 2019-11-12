#!/usr/bin/env python3           # This is client.py file

import socket
import random
import math
import sys
import string

import time


# create a socket object

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define the UDP_IP_ADDRESS and UDP_PORT_NO to use for the connection
hostname = socket.gethostname()  # get local machine name
host = socket.gethostbyname(hostname)
port = 8888
packet_data_size = 100  # 10 used during testing for convenience.


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


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def run_tests():
    msg = id_generator(30)

    rate = 10

    # finally save to file

    msg = bytes(msg, "utf-8")
    return msg, rate


def send_message(msg, rate, data):
    for i in range(3):  # send msg 3 times
        try:

            # start timer
            send(msg, rate)
            # receive data from server (data, address)
            data, address = clientSocket.recvfrom(2048)

            # end timer

            print('data', data)

        except socket.error:
            print("Error Code")
            # sys.exit()
        print(f" Server reply: {data}")


def main():
    arguments = sys.argv[1:]

    # connection to hostname on the port.
    data = b''
    clientSocket.connect((host, port))

    if arguments and arguments[0] == 'run_tests':
        # create 50 random messages and time them

        for n in range(5):
            start = time.time()
            msg, rate = run_tests()
            send_message(msg, rate, data)
            end = time.time()

            print('time elapsed:', end - start)

    else:
        while True:

            msg = input('Enter message to send : ')
            rate = input('Enter loss rate : ')  # packet loss rate
            while not msg:
                msg = input('Enter message to send : ')

            msg = bytes(msg, "utf-8")

            send_message(msg, rate, data)

    # Set the whole string
    # Send Message
    # clientSocket.sendto(bytes(msg, "utf-8"), (host, port))


if __name__ == '__main__':
    main()
