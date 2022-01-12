import threading
import socket
import argparse
import os


# create thread when class is instantiated
class Server(threading.Thread):
    """
    Supports management of server connections.
    Attributes:
        connections (list): A list of ServerSocket objects representing the active connections.
        host (str): The IP address of the listening socket.
        port (int): The port number of the listening socket.
    """
    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.host = host
        self.port = port

    def run(self):
        """
        1. create a new socket
        2. set socket options
        3. bind socket to port
        4. enable server to accept connections and confirm socket address
        5. listen for new client connections
        6. accept connections on socket
        7. once connected, print remote and socket address
        8. create new thread of the connection and the socket engaged in listening
        9. add new connection to a list to be managed globally
        """

        """
        Creates the listening socket. The listening socket will use the SO_REUSEADDR option to
        allow binding to a previously-used socket address. This is a small-scale application which
        only supports one waiting connection at a time.
        For each new connection, a ServerSocket thread is started to facilitate communications with
        that particular client. All ServerSocket objects are stored in the connections attribute.
        """
        # Create a new socket using the given address family, socket type and protocol number.
        # AF_INET is used by IP networking
        # SOCK_STREAM used for reliable flow-controlled data streams provided by TCP
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        
        # Set the value of the given socket option
        """SO_REUSEADDR to allow reuse of local addresses. For AF_INET sockets this means that a socket may 
        bind, except when there is an active listening socket bound to the address. """
        # requires a nonzero optval to turn the option on, and a zero value to turn the option off.
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind the socket to address. The socket must not already be bound.
        sock.bind((self.host, self.port))

        # Enable a server to accept connections.
        sock.listen(1)
        # Return the socket’s own address. This is useful to find out the port number of an IPv4/v6 socket, for instance.
        print('Listening at ', sock.getsockname())

        # facilitate TCP handshake
        # infinite loop to listen for new client connections
        while True:
            """Accept a connection. The socket must be bound to an address and listening for connections. 
            The return value is a pair (conn, address) where conn is a new socket object usable to send and 
            receive data on the connection, and address is the address bound to the socket on the other end of the connection."""
            sc, sock_name = sock.accept()

            # getpeername - Return the remote address to which the socket is connected.
            # This is useful to find out the port number of a remote IPv4/v6 socket, for instance.

            # getsockname - Return the socket’s own address.
            # returns socket address to which the socket object is bound
            print("Accepting connection from {} to {}".format(sc.getpeername(), sc.getsockname()))

            """to keep listening for new connections while establishing a connection with a client create
            new thread of the connection and the socket engaged in listening that runs parallel to Server thread"""
            server_socket = ServerSocket(sc, sock_name, self)

            # start new thread
            server_socket.start()

            # manage all active connections
            self.connections.append(server_socket)
            print("Ready to receive messages from ", sc.getpeername())

    def broadcast(self, msg, src):
        """
        Sends a message to all connected clients, except the source of the message.
        Args:
            msg (str): The message to broadcast.
            src (tuple): The socket address of the source client.
        """
        # iterate over all active client connections
        for c in self.connections:
            # broadcast msg to all but the source
            if c.sockname != src:
                c.send(msg)

    def remove_connection(self, connection):
        """
        Removes a ServerSocket thread from the connections attribute.
        Args:
            connection (ServerSocket): The ServerSocket thread to remove.
        """
        self.connections.remove(connection)


# class for individual connections between clients
class ServerSocket(threading.Thread):
    """
    Supports communications with a connected client.
    Attributes:
        sc (socket.socket): The connected socket.
        sockname (tuple): The client socket address.
        server (Server): The parent thread.
    """
    def __init__(self, sc, sock_name, server):
        super().__init__()
        self.sc = sc
        self.sock_name = sock_name
        self.server = server

    def run(self):
        """
        Receives data from the connected client and broadcasts the message to all other clients.
        If the client has left the connection, closes the connected socket and removes itself
        from the list of ServerSocket threads in the parent Server thread.
        """
        # infinite loop for the server to keep searching for data sent by clients
        while True:
            # recv - Receive data from the socket. The return value is a bytes object representing the data received.
            # The maximum amount of data to be received at once is specified by bufsize.
            # blocking call - program pauses until data arrives
            msg = self.sc.recv(1024).decode('ascii')
            if msg:
                print("{} says {!r}".format(self.sock_name, msg))
                self.server.broadcast(msg, self.sock_name)
            # if recv returns an empty string
            else:
                # client has closed socket. exit
                print("{} has closed the connection".format(self.sock_name))
                self.sc.close()

                # remove ServerSocket from list of active connections
                self.server.remove_connection(self)
                return

    def send(self, msg):
        """
        Sends a message to the connected server.
        Args:
            message (str): The message to be sent.
        """
        # Send data to the socket. The socket must be connected to a remote socket.
        self.sc.sendall(msg.encode('ascii'))


def exit(server):
    """
    Allows the server administrator to shut down the server.
    Typing 'q' in the command line will close all active connections and exit the application.
    """
    while True:
        x = input('')
        if x == 'q':
            print("Closing connections")
            for c in server.connections:
                c.sc.close()
            print("Shutting down server")
            os._exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()

    # Create and start server thread
    server = Server(args.host, args.p)
    server.start()

    exit = threading.Thread(target = exit, args = (server,))
    exit.start()

