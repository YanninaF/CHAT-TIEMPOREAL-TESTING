import socket
import threading

class ChatClient:
    def __init__(self, socket=None):
        self.socket = socket
        
    @staticmethod
    def validar_mensaje(mensaje):
        return bool(mensaje.strip())
    
    @staticmethod
    def validar_apodo(apodo):
        apodo = apodo.strip()
        return 3 <= len(apodo) <= 20
    
    def escuchar(self, cliente, apodo):
        while True:
            try:
                mensaje = cliente.recv(2048).decode('utf-8')
                if mensaje == 'APODO':
                    cliente.send(apodo.encode('utf-8'))
                else:
                    print(mensaje)
            except Exception as e:
                print(f'\033[31mError de conexión: {e}\033[0m')
                cliente.close()
                break
    
    def escribir(self, cliente, apodo):
        while True:
            try:
                mensaje = input("")
                if self.validar_mensaje(mensaje):
                    mensaje_completo = f'{apodo}: {mensaje}'
                    cliente.send(mensaje_completo.encode('utf-8'))
                else:
                    print("\033[31mEl mensaje no puede estar vacío\033[0m")
            except Exception as e:
                print(f"\033[31mError: {e}\033[0m")
                break

def crear_cliente(direccion='127.0.0.1', puerto=5001):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((direccion, puerto))
    return cliente

def obtener_apodo():
    while True:
        apodo = input('Ingrese su nombre de usuario: ').strip()
        if ChatClient.validar_apodo(apodo):
            return apodo
        print("\033[31m⚠️  El apodo debe tener entre 3 y 20 caracteres\033[0m")

def iniciar_cliente(cliente, apodo):
    try:
        if apodo:
            chat_client = ChatClient(cliente)
            hilo_recibir = threading.Thread(target=chat_client.escuchar, args=(cliente, apodo))
            hilo_escribir = threading.Thread(target=chat_client.escribir, args=(cliente, apodo))
            
            hilo_recibir.start()
            hilo_escribir.start()
            
            return hilo_recibir, hilo_escribir
    except Exception as e:
        print(f"Error iniciando al cliente: {str(e)}")
        return None

if __name__ == "__main__":
    cliente = crear_cliente()
    apod = obtener_apodo()
    iniciar_cliente(cliente, apod)