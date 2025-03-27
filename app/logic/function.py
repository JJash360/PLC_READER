import snap7
from snap7.util import *

IP_ADDRESS_1="192.168.0.3"
IP_ADDRESS_2="192.168.8.233"
IP_ADDRESS_3="192.168.8.152"

data_types={
    "BOOL": 1,
    "BYTE": 1,
    "INT": 2,
    "REAL": 4,
    "WORD": 4,
    "DINT": 4,
    "DWORD": 4
}

db_types={
    "BOOL": 1,
    "BYTE": 1,
    "INT": 2,
    "REAL": 4,
    "WORD": 2,
    "DINT": 4,
    "DWORD": 4
}

def conectar_plc(IP_ADDRESS):
    try:
        plc=snap7.client.Client()
        plc.connect(IP_ADDRESS,0,1)
        print(f"Conectado con el PLC con IP: {IP_ADDRESS}")
    except Exception as e:
        print(f"Error al conectar PLC: {e}")

    return plc

def leer_memory(IP_ADDRESS,number_memory,bit,data_type):
    #M{number_memory}.{bit}
    #MD{number_memory}

    if data_type not in data_types:
        raise ValueError(f"Tipo de dato '{data_type}' no válido.")
    
    size = data_types[data_type]  # Obtener tamaño del dato

    try:
        plc=conectar_plc(IP_ADDRESS)
        data=plc.read_area(snap7.type.Areas.MK,0,number_memory,size)

        if data_type=="BOOL":
            resultado=(data[0] >> bit) & 1
        elif data_type=="BYTE":
            resultado=int.from_bytes(data, byteorder='big')
        elif data_type=="INT":
            resultado=get_int(data,0)
        elif data_type=="REAL":
            resultado=get_real(data,0)
        elif data_type=="WORD":
            resultado=get_word(data,0)
        elif data_type=="DINT":
            resultado=get_dint(data,0)
        elif data_type=="DWORD":
            resultado=get_dword(data,0)
        plc.disconnect()
        return resultado
    
    except Exception as e:
        print(f"Error al leer la memoria: {e}")
        return None 

def leer_datablock(IP_ADDRESS,db_number,offset,data_type):
    #DB{db_number}.DBD{offset}

    if data_type not in db_types:
        raise ValueError(f"Tipo de dato '{data_type}' no válido.")
    
    size = db_types[data_type]  # Obtener tamaño del dato

    try:
        plc=conectar_plc(IP_ADDRESS)
        data=plc.db_read(db_number,offset,size)

        if data_type=="BOOL":
            resultado=bool(data[0] & 1)
        elif data_type=="BYTE":
            resultado=int.from_bytes(data, byteorder='big')
        elif data_type=="INT":
            resultado=get_int(data,0)
        elif data_type=="REAL":
            resultado=get_real(data,0)
        elif data_type=="WORD":
            resultado=get_word(data,0)
        elif data_type=="DINT":
            resultado=get_dint(data,0)
        elif data_type=="DWORD":
            resultado=get_dword(data,0)
        plc.disconnect()
        return resultado
    
    except Exception as e:
        print(f"Error al leer el datablock: {e}")
        return None

import snap7
from snap7.util import *

data_types = {
    "BOOL": 1,
    "BYTE": 1,
    "INT": 2,
    "REAL": 4,
    "WORD": 2,
    "DINT": 4,
    "DWORD": 4
}

def escribir_memory(IP_ADDRESS, number_memory, offset, data_type, value):
    #M{number_memory}.{offset}
    #MD{number_memory}
    
    if data_type not in data_types:
        raise ValueError(f"Tipo de dato '{data_type}' no válido.")

    try:
        plc = snap7.client.Client()
        plc.connect(IP_ADDRESS, 0, 1)  # Conectar al PLC

        # Leer el estado actual de la memoria M
        size = data_types[data_type]
        memory = plc.mb_read(number_memory, size)

        # Escribir el nuevo valor en la memoria
        if data_type == "BOOL":
            set_bool(memory, 0, offset, value)  # Escribir en bit específico
        elif data_type == "BYTE":
            memory[0] = value
        elif data_type == "INT":
            set_int(memory, 0, value)
        elif data_type == "REAL":
            set_real(memory, 0, value)
        elif data_type == "WORD":
            set_word(memory, 0, value)
        elif data_type == "DINT":
            set_dint(memory, 0, value)
        elif data_type == "DWORD":
            set_dword(memory, 0, value)

        # Escribir en la memoria M del PLC
        plc.mb_write(number_memory, size, memory)

        plc.disconnect()
        print(f"Memoria M{number_memory}.{offset} actualizada con {value}")
    
    except Exception as e:
        print(f"Error al escribir en la memoria M{number_memory}.{offset}: {e}")


def activar_bit(IP_ADDRESS,number_memory,offset):
    try:
        plc=conectar_plc(IP_ADDRESS)
        bit=plc.mb_read(number_memory,1)
        set_bool(bit,0,offset,True)
        plc.mb_write(number_memory,1,bit)
        set_bool(bit,0,offset,False)
        plc.mb_write(number_memory,1,bit)
        plc.disconnect()
        print(F"Memoria M{number_memory}.{offset} funcionando")
    except Exception as e:
        print(f"Error con la memoria M{number_memory}.{offset}: {e}")

