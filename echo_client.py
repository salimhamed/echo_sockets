import socket
import sys


def client(msg, log_buffer=sys.stderr):
    """
    Send a message to the echo server.
    """
    server_address = ('localhost', 10000)
    # TODO: Replace the following line with your code which will instantiate
    #       a TCP socket with IPv4 Addressing, call the socket you make 'sock'
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_STREAM,
                         socket.IPPROTO_TCP)
    print >>log_buffer, 'connecting to {0} port {1}'.format(*server_address)

    # TODO: connect your socket to the server here.
    sock.connect(server_address)

    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        print >>log_buffer, 'sending "{0}"'.format(msg)
        # TODO: send your message to the server here.
        sock.sendall(msg)

        # TODO: the server should be sending you back your message as a series
        #       of 16-byte chunks.  You will want to log them as you receive
        #       each one.  You will also need to check to make sure that
        #       you have received the entire message you sent __before__
        #       closing the socket.
        #
        #       Make sure that you log each chunk you receive.  Use the print
        #       statement below to do it. (The tests expect this log format)
        buffersize = 16
        while True:
            chunk = sock.recv(buffersize)
            print >>log_buffer, 'received "{0}"'.format(chunk)
            if len(chunk) < buffersize:
                break

    finally:
        # TODO: after you break out of the loop receiving echoed chunks from
        #       the server you will want to close your client socket.
        print >>log_buffer, 'closing socket'
        sock.close()


def list_services(port_range=(0, 10)):
    """
    Function that lists the services provided by a given range of ports.

    Parameters
    ==========
    port_range: tuple of lower and upper bounds of port range, in the format
        (lower_bound, upper_bound)
    """
    # validate arguments passed to function
    if port_range[0] < 0:
        raise TypeError("Lower bound must be greater than 0.")
    elif port_range[1] > 65535:
        raise TypeError("Upper bound must be less than 65535.")
    elif port_range[0] > port_range[1]:
        raise TypeError("Lower bound must be less than Upper Bound.")

    # create a list of
    for i in xrange(port_range[0], port_range[1]):
        try:
            print socket.getservbyport(i)
        except socket.error:
            print 'No service for port {}.'.format(i)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usg = '\nusage: python echo_client.py "this is my message"\n'
        print >>sys.stderr, usg
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
