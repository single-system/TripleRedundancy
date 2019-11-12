#!/usr/bin/env python3          # This is server.py file

import socket
import sys
import time

# create a socket object, (SOCKET_FAMILY, SOCKET_TYPE)


try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(" Server socket created")
except socket.error:
    print(f"Failed to create socket. Error Code ")
    sys.exit()

# Define the UDP_IP_ADDRESS and UDP_PORT_NO to use for the connection
hostname = socket.gethostname()  # get local machine name
host = socket.gethostbyname(hostname)
port = 8888

# bind to the port
serverSocket.bind((host, port))
chunks = {}  # list to hold chunks of data


def decode3ps(data):
    data = data.decode('utf-8')
    if data[0:3] not in chunks:
        chunks[data[0:3]] = data[3:]

    print(dict(sorted(chunks.items())))
    return chunks


def assemble_msg(msg_dic):
    msg = ''.join(str(msg_dic[x]) for x in sorted(msg_dic))
    return msg


def main():
    while True:
        # Accept connections
        data, address = serverSocket.recvfrom(2048)
        # print(f"Data received:  {data}")
        print('data received')
        # print(f' Message received from client: {assemble_msg(decode3ps(data))}\n')

        # For the sake of testing
        time.sleep(1)

        reply = 'OK...' + str(data)

        serverSocket.sendto(bytes(reply, "utf-8"), address)

    # serverSocket.close()


if __name__ == '__main__':
    main()
