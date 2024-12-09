from cliente import ChatClient, crear_cliente, iniciar_cliente, obtener_apodo
from unittest.mock import patch, MagicMock

def test_msj_vacio():
    mensaje = ""
    assert not ChatClient.validar_mensaje(mensaje)

def test_crear_cliente_mock():
    with patch('socket.socket') as MockSocket:
        mock_instance = MagicMock()
        MockSocket.return_value = mock_instance
        mock_instance.connect.return_value = None

        direccion = '127.0.0.1'
        puerto = 5001
        cliente = crear_cliente(direccion, puerto)

        mock_instance.connect.assert_called_with((direccion, puerto))
        assert cliente is mock_instance

def test_imput():
    entradas = ["", "ab", "", "usuario_valido"]
    with patch('builtins.input', side_effect=entradas):
        apodo = obtener_apodo()
        assert apodo == "usuario_valido"

def cliente_generado():
    mock_cliente = MagicMock()
    return mock_cliente

def test_iniciar_cliente_con_hilos_mockeados():
    with patch('threading.Thread') as MockThread:
        # Configurar el mock del Thread
        mock_thread = MagicMock()
        MockThread.return_value = mock_thread
        
        # Crear cliente mock
        cliente = cliente_generado()
        apodo = 'usuario_test'
        
        # Iniciar cliente
        iniciar_cliente(cliente, apodo)
        
        # Verificar llamadas
        assert MockThread.call_count == 2, "Thread debería ser llamado dos veces"
        
        # Verificar que los hilos se iniciaron
        assert mock_thread.start.call_count == 2, "start() debería ser llamado dos veces"