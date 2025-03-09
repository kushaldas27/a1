import socket
import sys

keyValueStore = {}
counterStore = {}

def handleGetKey(requestPath):
    if requestPath in keyValueStore:
        if requestPath in counterStore:
            counterStore[requestPath] -= 1
            if counterStore[requestPath] == 0:
                del counterStore[requestPath]
            return "200 OK  "
        else:
            return "200 OK  "
    else:
        return "404 NotFound  "

def handlePostKey(requestPath, contentBody):
    if requestPath in counterStore:
        return "405 MethodNotAllowed  "
    keyValueStore[requestPath] = contentBody
    return "200 OK  "

def handleDeleteKey(requestPath):
    if requestPath not in keyValueStore:
        return "404 NotFound  "
    if requestPath in counterStore:
        return "405 MethodNotAllowed  "
    value = keyValueStore.pop(requestPath)
    return "200 OK  "

def handlePostCounter(requestPath, body):
    if requestPath not in keyValueStore:
        return "405 MethodNotAllowed  "
    if requestPath in counterStore:
        counterStore[requestPath] += int(body)
    else:
        counterStore[requestPath] = int(body)
    return "200 OK  "

def handleGetCounter(requestPath):
    if requestPath not in keyValueStore:
        return "404 NotFound  "
    if requestPath in counterStore:
        return "200 OK  "
    return "200 OK  "

def handleRequest(clientSocket):
    request = clientSocket.recv(1024)
    request = request.decode("utf-8")

    # Client disconnected
    if len(request) == 0:
        return False
    
    headerFields, contentBody = request.strip().split("  ")
    # Set first two substrings to method and path
    method, path = headerFields.split(" ")[:2]

    if method == "GET":
        if path.startswith("/key"):
            return handleGetKey(path[:5])
        elif path.startswith("/counter"):
            return handleGetCounter(path[9:])
        else:
            return "404 NotFound  "
        
    elif method == "POST":
        if path.startswith("/key"):
            return handlePostKey(path[:5], contentBody)
        elif path.startswith("/counter"):
            return handlePostCounter(path[9:], contentBody)
        else:
            return "404 NotFound  "
    
    elif method == "DELETE":
        if path.startswith("/key"):
            return handleDeleteKey(path[:5], contentBody)
        else:
            return "404 NotFound  "
    
    response = response.encode()
    clientSocket.send(response)
    return True

def runServer(port):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(("0.0.0.0"), port)
    serverSocket.listen(1)

    while True:
        clientSocket, clientAddress = serverSocket.accept()
        while True:
            connected = handleRequest(clientSocket)
            if not connected:
                break
        clientSocket.close()

if __name__ == "__main__":
    port = int(sys.argv[1])
    runServer(port)