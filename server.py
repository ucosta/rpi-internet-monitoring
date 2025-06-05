import socket

# Server configuration
HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 5900       # Port to listen on

# Create TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Allow reusing the address, helpful for quick restarts
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Service listening on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()  # Accept new connection
        with conn:
            print(f"Connection accepted from {addr}")

            # Receive Data (HTTP Request) - up to 1024 bytes
            data = conn.recv(1024)
            if not data:
                print(f"No data received from {addr}, closing connection.")
                continue  # If no data, wait for new connection

            # Print received data (for debugging)
            # print(f"Received data: {data.decode('utf-8', errors='ignore')}")

            # HTTP Response
            response_body = "It's Alive!"
            # Construct HTTP headers
            response_headers = [
                "HTTP/1.1 200 OK",
                "Content-Type: text/plain; charset=utf-8",
                f"Content-Length: {len(response_body)}",
                "Connection: close"  # Instruct client to close connection after response
            ]

            # Join headers and body, separated by an empty line (\r\n\r\n)
            response = "\r\n".join(response_headers) + "\r\n\r\n" + response_body

            # Send response (encoded to bytes)
            try:
                conn.sendall(response.encode('utf-8'))
                print(f"Response sent to {addr}")
            except socket.error as e:
                print(f"Socket error while sending to {addr}: {e}")import socket

# Server configuration
HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 5900       # Port to listen on

# Create TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Allow reusing the address, helpful for quick restarts
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Service listening on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()  # Accept new connection
        with conn:
            print(f"Connection accepted from {addr}")

            # Receive Data (HTTP Request) - up to 1024 bytes
            data = conn.recv(1024)
            if not data:
                print(f"No data received from {addr}, closing connection.")
                continue  # If no data, wait for new connection

            # Print received data (for debugging)
            # print(f"Received data: {data.decode('utf-8', errors='ignore')}")

            # HTTP Response
            response_body = "It's Alive!"
            # Construct HTTP headers
            response_headers = [
                "HTTP/1.1 200 OK",
                "Content-Type: text/plain; charset=utf-8",
                f"Content-Length: {len(response_body)}",
                "Connection: close"  # Instruct client to close connection after response
            ]

            # Join headers and body, separated by an empty line (\r\n\r\n)
            response = "\r\n".join(response_headers) + "\r\n\r\n" + response_body

            # Send response (encoded to bytes)
            try:
                conn.sendall(response.encode('utf-8'))
                print(f"Response sent to {addr}")
            except socket.error as e:
                print(f"Socket error while sending to {addr}: {e}")
