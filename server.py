import socket
import os
import textract

IP = "127.0.0.1"
PORT = 1234
BUFFER_SIZE = 2048
UPLOADS_DIR = "uploads"
pdf_texts = {}  # Dictionary to store extracted text

if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

def parsing_request(request):
    headers = request.split("\r\n")
    method, path, _ = headers[0].split(" ")
    return method, path

def extract_text_from_file(file_path):
    text = textract.process(file_path).decode('utf-8')
    return text

def saving_uploaded_file(body):
    filename_marker = b"filename=\""
    start = body.decode().find(filename_marker) + len(filename_marker)
    end = body.find(b"\"", start)
    filename = body[start:end].decode()
    if not filename.lower().endswith('.pdf'):
        return None
    pdf_data_marker = b"\r\n\r\n"
    start = body.find(pdf_data_marker, end) + len(pdf_data_marker)
    end = body.find(b"\r\n--", start)
    pdf_data = body[start:end]
    file_path = os.path.join(UPLOADS_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(pdf_data)
    return file_path

def parse_request(request):
    lines = request.split('\n')
    method, path, *_ = lines[0].split(' ')
    headers = {}
    for line in lines[1:]:
        if not line.strip():
            break
        key, value = line.split(': ', 1)
        headers[key] = value.strip()
    body = lines[-1]
    return method, path, headers, body

def response_200(data):
    return f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{data}\r\n'

def response_404():
    return 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<html><body>Invalid request.</body></html>\r\n'

def response_400(message):
    return f'HTTP/1.1 400 Bad Request\r\nContent-Type: application/json\r\n\r\n{{"error": "{message}"}}\r\n'

def handling_client(client_socket):
    request = client_socket.recv(BUFFER_SIZE).decode('utf-8', errors='ignore')
    method, path, headers, body = parse_request(request)
    if method == 'GET':
        if path == '/':
            with open("index.html", "r") as file:
                index_content = file.read()
            response = response_200(index_content)
        else:
            response = response_404()
    elif method == 'POST':
        if path == '/upload':
            file_path = saving_uploaded_file(body)
            if file_path:
                text = extract_text_from_file(file_path)
                pdf_texts[file_path] = text
                response = response_200("<html><body><h2>PDF uploaded successfully!</h2></body></html>")
            else:
                response = response_400('Invalid File!')
        else:
            response = response_404()
    else:
        response = response_400('Method not supported')
    client_socket.send(response.encode())
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(5)
    print(f"http://{IP}:{PORT}")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")
        handling_client(client_socket)

main()