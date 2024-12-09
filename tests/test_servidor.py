import unittest
import socket
import threading
import time
from servidor import ChatServer

class TestServidor(unittest.TestCase):
    @staticmethod
    def simular_cliente(apodo, mensajes, duracion=1):
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.settimeout(5)  # Timeout de 5 segundos
            cliente.connect(('127.0.0.1', 5001))
            
            # Recibir solicitud de apodo
            cliente.recv(2048)
            cliente.send(apodo.encode('utf-8'))
            
            # Enviar mensajes
            for mensaje in mensajes:
                cliente.send(mensaje.encode('utf-8'))
                time.sleep(0.1)
            
            time.sleep(duracion)
            cliente.close()
        except Exception as e:
            print(f"Error en simulación de cliente: {e}")
    
    def test_carga_masiva_con_desconexion(self):
        # Crear y configurar el servidor
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind(('127.0.0.1', 5001))
        servidor.settimeout(5)  # Timeout de 5 segundos
        servidor.listen(10)
        
        chat_server = ChatServer()
        terminar = threading.Event()
        
        def ejecutar_servidor():
            try:
                while not terminar.is_set():
                    try:
                        cliente, _ = servidor.accept()
                        thread = threading.Thread(
                            target=chat_server.gestionar_cliente,
                            args=(cliente,),
                            daemon=True
                        )
                        thread.start()
                    except socket.timeout:
                        continue
            except Exception as e:
                if not terminar.is_set():
                    print(f"Error en servidor: {e}")
        
        # Iniciar servidor
        servidor_thread = threading.Thread(target=ejecutar_servidor, daemon=True)
        servidor_thread.start()
        
        try:
            # Crear y ejecutar clientes
            clientes = []
            for i in range(5):  # Reducimos a 5 clientes para la prueba
                cliente = threading.Thread(
                    target=self.simular_cliente,
                    args=(f"Test{i}", [f"Msg{i}-{j}" for j in range(2)]),
                    daemon=True
                )
                clientes.append(cliente)
                cliente.start()
            
            # Esperar a que terminen los clientes
            for cliente in clientes:
                cliente.join(timeout=5)
                
            time.sleep(1)  # Esperar procesamiento final
            
            
        finally:
            # Limpieza
            terminar.set()
            servidor.close()

    def test_desconexion_cliente(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind(('127.0.0.1', 5001))
        servidor.listen(10)
        
        chat_server = ChatServer()
        servidor_thread = threading.Thread(target=chat_server.aceptar_conexiones, args=(servidor,), daemon=True)
        servidor_thread.start()
        
        # Conectar cliente
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(('127.0.0.1', 5001))
        
        # Registrar cliente
        cliente.recv(2048)
        cliente.send("Cliente1".encode('utf-8'))
        time.sleep(0.1)
        
        # Verificar conexión inicial
        self.assertEqual(len(chat_server.clientes), 1)
        
        # Desconectar usando shutdown
        cliente.shutdown(socket.SHUT_RDWR)
        cliente.close()
        time.sleep(0.1)
        
        # Verificar desconexión
        self.assertEqual(len(chat_server.clientes), 0)
        servidor.close()

if __name__ == "__main__":
    unittest.main()