import socket
import threading
import sys
import traceback

class ChatServer:
    def __init__(self):
        self.clientes = []
        self.apodos = []
    
    def difusion(self, mensaje):
        for cliente in self.clientes[:]:
            try:
                cliente.send(mensaje)
            except:
                self.desconectar_cliente(cliente)
    
    def desconectar_cliente(self, cliente):
        if cliente in self.clientes:
            idx = self.clientes.index(cliente)
            apodo = self.apodos[idx]
            self.clientes.remove(cliente)
            self.apodos.remove(apodo)
            cliente.close()
            self.difusion(f'{apodo} ha abandonado el chat.'.encode('utf-8'))
            print(f'Cliente {apodo} desconectado.')
    
    def gestionar_cliente(self, cliente):
        while True:
            try:
                mensaje = cliente.recv(2048)
                if mensaje:
                    self.difusion(mensaje)
                else:
                    break
            except Exception as e:
                print(f"Error en gestión de cliente: {str(e)}")
                print("Detalles del error:")
                print(traceback.format_exc())
                break
        
        self.desconectar_cliente(cliente)

    def aceptar_conexiones(self, servidor):
        while True:
            cliente, direccion = servidor.accept()
            print(f'Nueva conexión: {direccion}')
            
            cliente.send('APODO'.encode('utf-8'))
            apodo = cliente.recv(2048).decode('utf-8')
            
            self.apodos.append(apodo)
            self.clientes.append(cliente)
            
            print(f'Cliente conectado como: {apodo}')
            self.difusion(f'{apodo} se ha unido al chat!'.encode('utf-8'))
            cliente.send('Conectado exitosamente'.encode('utf-8'))
            
            thread = threading.Thread(target=self.gestionar_cliente, args=(cliente,))
            thread.start()

def iniciar_servidor(host='127.0.0.1', puerto=5001):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, puerto))
    servidor.listen()
    print(f'Servidor iniciado en {host}:{puerto}')
    
    chat_server = ChatServer()
    chat_server.aceptar_conexiones(servidor)

if __name__ == "__main__":
    iniciar_servidor()