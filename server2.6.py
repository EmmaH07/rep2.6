"""
Author: Emma Harel
Program name: server2.6
Description: a server that has 4 functions - TIME, RAND, NAME, and EXIT. the server sends a response based on the
clients request. The response contains the length of the message, a dollar sign($) and the message itself.
Date: 18/11/23
"""
import socket
import datetime
import random
import logging

QUEUE_LEN = 1
MAX_PACKET = 4

logging.basicConfig(filename='server26.log', level=logging.DEBUG)


def time():
    """
    returns the current time.
    """
    return str(datetime.datetime.now())


def name():
    """
    returns the server's name.
    """
    return "server2.6"


def rand():
    """
    returns a random number between 1 and 10.
    """
    return random.randint(1, 10)


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.bind(('0.0.0.0', 1729))
        my_socket.listen(QUEUE_LEN)
        logging.debug("server is waiting for a new client")
        while True:
            client_socket, client_address = my_socket.accept()
            logging.debug("server connected to: " + client_address[0] + ":" + str(client_address[1]))
            try:
                request = client_socket.recv(MAX_PACKET).decode()
                logging.debug("Server received: " + request)
                while request != "EXIT":
                    if request == "TIME":
                        t = time()
                        res = str(len(t)) + "$" + t
                        logging.debug("Server sent: " + res)
                        client_socket.send(res.encode())
                    elif request == "NAME":
                        res = str(len(name())) + "$" + name()
                        logging.debug("Server sent: " + res)
                        client_socket.send(res.encode())
                    elif request == "RAND":
                        num = str(rand())
                        res = str(len(num)) + "$" + num
                        logging.debug("Server sent: " + res)
                        client_socket.send(res.encode())
                    else:
                        client_socket.send("Illegal request".encode())

                    request = client_socket.recv(MAX_PACKET).decode()
                    logging.debug("Server received: " + request)

                logging.debug("server disconnected from: " + client_address[0] + ":" + str(client_address[1]))
                res = str(len("EXIT")) + "$" + "EXIT"
                logging.debug("Server sent: " + res)
                client_socket.send(res.encode())
                logging.debug("server is waiting for a new client")

            except socket.error as err:
                print('received socket error on client socket' + str(err))
                logging.error("received socket error on client socket: " + str(err))
            finally:
                client_socket.close()

    except socket.error as err:
        print('received socket error on server socket' + str(err))
        logging.error("received socket error on server socket")

    finally:
        my_socket.close()


if __name__ == "__main__":
    assert 1 <= rand() <= 10
    assert name() == "server2.6"
    main()
