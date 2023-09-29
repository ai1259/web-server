# import socket module
from socket import *
# In order to terminate the program
import sys

def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Prepare a server socket
    serverSocket.bind(("", port))

    # Start listening for incoming connections
    serverSocket.listen(1)
    print(f"Server is listening on port {port}")

    while True:
        # Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()

        try:
            message = connectionSocket.recv(2048).decode()
            filename = message.split()[1]

            # Remove any leading slash from the filename
            filename = filename[1:]

            # Try to open the requested file
            try:
                with open(filename, "rb") as file:
                    file_data = file.read()

                # Define headers for the HTTP response
                headers = b"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"

                # Send headers followed by file data to the client
                connectionSocket.sendall(headers + file_data)

            except FileNotFoundError:
                # Send "404 Not Found" response with an HTML page
                response = b"HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"
                response += b"<html><body><h1>404 Not Found</h1></body></html>"
                connectionSocket.sendall(response)

            # Close the client socket
            connectionSocket.close()

        except Exception as e:
            # Send "500 Internal Server Error" response for other exceptions
            response = b"HTTP/1.1 500 Internal Server Error\r\n\r\n" + str(e).encode()
            connectionSocket.sendall(response)
            connectionSocket.close()

if __name__ == "__main__":
    webServer(13331)
