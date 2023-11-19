"""
Author: Emma Harel
Program name: client2.6
Description: A client that requests 4 things from the server: TIME, RAND, NAME, and EXIT.
The client receives a message from the server that contains the length of the message, a dollar sign($) and the message
itself.
Date: 18/11/23
"""

import socket
import logging

MAX_PACKET = 1024

logging.basicConfig(filename='client26.log', level=logging.DEBUG)


def valid_req(req):
    """
    checks if the client is trying to send a valid request.
    """
    if req == "TIME":
        return True
    elif req == "NAME":
        return True
    elif req == "RAND":
        return True
    elif req == "EXIT":
        return True
    else:
        return False


def response_msg(res):
    """
    Separates the length of the message from the message
    """
    res_arr = res.split('$')
    return res_arr[1]


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect(('127.0.0.1', 1729))
        logging.debug("Client connected to: 127.0.0.1:1729")
        print('Try one of the following requests: TIME, RAND, and NAME. Write EXIT to exit server ')
        request = input("Enter request: ")
        logging.debug("Client sent: " + request)
        while not valid_req(request):
            print("Illegal request, try again")
            request = input("Enter request: ")
            logging.debug("Client sent: " + request)
        my_socket.send(request.encode())
        response = response_msg(my_socket.recv(MAX_PACKET).decode())
        logging.debug("Client received: " + response)
        while response != "EXIT":
            print("Server sent: " + response)
            request = input("Enter request: ")
            logging.debug("Client sent: " + request)
            while not valid_req(request):
                print("Illegal request, try again")
                request = input("Enter request: ")
                logging.debug("Client sent: " + request)
            my_socket.send(request.encode())
            response = response_msg(my_socket.recv(MAX_PACKET).decode())
            logging.debug("Client received: " + response)
        my_socket.close()
    except socket.error as err:
        print('received socket error ' + str(err))
        logging.error(err)
    finally:
        my_socket.close()


if __name__ == "__main__":
    assert str(valid_req("TIME")) == "True"
    assert str(valid_req("I DON'T love cyber <3")) == "False"
    assert response_msg("5$cyber") == "cyber"
    main()
