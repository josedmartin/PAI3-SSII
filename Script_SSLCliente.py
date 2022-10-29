from socket import *
import ssl,sys


cipher = "ECDHE-RSA-AES128-GCM-SHA256"

with open("Config.config") as configfile:
        ip_elegido =  configfile.readline().rstrip()
        puerto_elegido = configfile.readline().rstrip()
        cipherPack_seleccionado = configfile.readline().rstrip()
IPServidor = ip_elegido.replace("ip_cliente=","")
puertoServidor = puerto_elegido.replace("Puerto_elegido=","")
cipherPack_elegido = cipherPack_seleccionado.replace("cipherPack_A_Eleccion=","")

def crear_mensaje(socket):
    usuario = input("Indique el usuario: ")
    password = input("Indique la contraseña: ")
    mensaje = input("Escriba un mensaje: ")
    datos_mensaje= usuario + password + mensaje + ssl.SSLSocket.version(socket)
    return datos_mensaje


def client_conect():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations('Keys/new.pem')
    if cipherPack_elegido !='0':
        context.set_ciphers(cipher)
    print("Los CipherSuite elegidos son los siguientes:",context.get_ciphers())
    soc=socket()
    conex_wrap = context.wrap_socket(soc, server_hostname=IPServidor)
    conex_wrap.connect((IPServidor,int(puertoServidor)))
    print("Conexión exitosa...")
    #escribimos el mensaje
    mensaje = crear_mensaje(conex_wrap)
    conex_wrap.send(mensaje.encode())
    #recibimos el mensaje
    respuesta = conex_wrap.recv(4096).decode()
    print(respuesta)
    
    conex_wrap.close()
    sys.exit()

if __name__ == "__main__":
    client_conect()