\# 🛡️ Ataque MAC Flooding (Inundación de CAM)



\*\*Autor:\*\* Anthony | \*\*Matrícula:\*\* 2025-1335 | \*\*Práctica #:\*\* \[P2]

🎥 \*\*Demostración en Video:\*\* https://youtu.be/16XaJxJ2-3U



\---



\## 📌 Objetivo del Laboratorio

Saturar la tabla de direcciones MAC (CAM table) del switch para forzarlo a actuar como un Hub viejo en modo \*Fail-Open\*, lo que permite capturar el tráfico ajeno.



\## 💻 Funcionamiento del Script

\* \*\*Objetivo:\*\* Llenar la memoria de direcciones MAC del switch inyectando cientos de miles de tramas de red con direcciones de origen falsas y aleatorias.

\* \*\*Parámetros usados:\*\* `PACKET\_RATE=10000`, `PACKET\_COUNT=100000`.

\* \*\*Funcionamiento:\*\* Se construyen paquetes TCP/IP completos donde la MAC de origen y de destino son pseudoaleatorias, utilizando un bucle optimizado para maximizar la velocidad.



\## 🚨 Impacto (Verificación Antes)

En el Switch Cisco, al ejecutar `show mac address-table count`, verás que el número de direcciones dinámicas aprendidas llega a su límite máximo (miles de entradas).



\---



\## 🔒 Contra-medidas (Mitigación)

Implementamos la misma defensa que en el ataque anterior: \*\*Port Security\*\*. Al imponer un límite estricto en el número de MACs permitidas por puerto, se hace físicamente imposible saturar la tabla global del hardware.



\*\*Configuración en el Switch Cisco:\*\*

```text

enable

configure terminal

interface range Ethernet0/0 - 2

&#x20;switchport port-security

&#x20;switchport port-security maximum 2

&#x20;switchport port-security violation restrict

exit

```



\## ✅ Verificación Después

En el Switch Cisco, ejecutando el comando `show mac address-table count`, el conteo de la tabla de direcciones se mantendrá en un número bajo y saludable (usualmente menos de 10).

