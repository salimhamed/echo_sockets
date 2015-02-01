import select
import socket
import sys


def server(log_buffer=sys.stderr):
    """
    Launch a server that echoes messages back to client.
    """
    # set an address for our server
    address = ('127.0.0.1', 10000)

    # TODO: Replace the following line with your code which will instantiate
    #       a TCP socket with IPv4 Addressing, call the socket you make 'sock'
    server = socket.socket(socket.AF_INET,
                         socket.SOCK_STREAM,
                         socket.IPPROTO_TCP)

    # TODO: Set an option to allow the socket address to be reused immediately
    #       see the end of http://docs.python.org/2/library/socket.html
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # log that we are building a server
    print >>log_buffer, "making a server on {0}:{1}".format(*address)

    # TODO: bind your new sock 'sock' to the address above and begin to listen
    #       for incoming connections
    server.bind(address)
    server.listen(5)

    # setup arguments for select.select for parallel processing of incoming
    # connections (http://pymotw.com/2/select/)

    # list of sockets from which we expect to read
    inputs = [server]

    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            print >>log_buffer, 'waiting for a connection'

            # Use select.select() to manage parallel request to the server.
            #
            # 'input_ready':  This will be the list of sockets to be checked
            # for incoming data.
            #
            # 'output_ready':  This will be the list of sockets that will
            # recieve outgoing data.
            #
            # 'except_ready':  This will be the list of sockets that may have
            # an error.
            input_ready, output_ready, except_ready = \
                select.select(inputs, [], [])

            for s in input_ready:
                # if the object in the list is the server socket, then connect
                # to the client and append the new socket connect with the
                # client to the inputs list
                if s is server:
                    conn, addr = server.accept()
                    inputs.append(conn)

                # handle all other sockets
                else:
                    data = s.recv(16)
                    print >>log_buffer, 'received "{0}"'.format(data)

                    if data:
                        s.sendall(data)
                    else:
                        s.close()
                        inputs.remove(s)

    except KeyboardInterrupt:
        # TODO: Use the python KeyboardIntterupt exception as a signal to
        #       close the server socket and exit from the server function.
        #       Replace the call to `pass` below, which is only there to
        #       prevent syntax problems
        sock.close()


if __name__ == '__main__':
    server()
    sys.exit(0)
