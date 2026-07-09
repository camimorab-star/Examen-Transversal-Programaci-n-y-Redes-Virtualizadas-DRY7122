def clasificar_as(asn):
    if 65536 <= asn <= 4294967295:
        tipo_bits = "AS de 32 bits."
    elif 0 <= asn <= 65535:
        tipo_bits = "AS de 16 bits."
    else:
        tipo_bits = "No corresponde a un AS válido de 16 ni 32 bits."
    if 64512 <= asn <= 65534:
        clasificacion = "privado"
    elif 4200000000 <= asn <= 4294967294:
        clasificacion = "privado"
    elif asn == 0 or asn == 65535 or asn == 4294967295:
        clasificacion = "reservado"
    elif asn == 23456:
        clasificacion = "reservado"
    elif 1 <= asn <= 4294967294:
        clasificacion = "público"
    else:
        clasificacion = "inválido"
    return clasificacion, tipo_bits
try:
    asn = int(input("Ingrese el número de AS de BGP: "))
    clasificacion, tipo_bits = clasificar_as(asn)
    if clasificacion == "privado":
        print(f"El AS {asn} es un AS privado.")
    elif clasificacion == "público":
        print(f"El AS {asn} es un AS público.")
    elif clasificacion == "reservado":
        print(f"El AS {asn} es reservado, no corresponde a un AS público ni privado.")
    else:
        print(f"El AS {asn} no es válido.")
    print(tipo_bits)

except ValueError:
    print("Error: debe ingresar un número entero.")