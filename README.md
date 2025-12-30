# ⚡ Bitcoin Algorithmic Tracker (Cloud Deployed)

Plataforma de ingeniería de datos financiera de grado producción. Ingesta datos de criptomonedas en tiempo real, calcula indicadores de volatilidad y visualiza tendencias mediante una arquitectura distribuida en la nube.

[![Deployment](https://img.shields.io/badge/Azure-Production-blue?logo=microsoftazure)](https://dev-peepo.me)
[![Database](https://img.shields.io/badge/Neon-Serverless_Postgres-green?logo=postgresql)](https://neon.tech)
[![Security](https://img.shields.io/badge/SSL-LetsEncrypt-success?logo=letsencrypt)](https://letsencrypt.org)
[![Stack](https://img.shields.io/badge/Python-Streamlit-red?logo=python)](https://streamlit.io)

### 🔗 Demo en Vivo: [[https://dev-peepo.me](https://finance.dev-peepo.me/)

---

## 🏗 Arquitectura de Producción

El sistema ha evolucionado de un script local a una infraestructura DevOps completa:

1.  **Ingesta Continua (Daemon):** Servicio `systemd` en Linux que consulta la API de **CoinGecko** 24/7.
2.  **Persistencia en Nube:** Base de datos **PostgreSQL Serverless (Neon DB)** para alta disponibilidad y escalabilidad.
3.  **Motor Analítico:** Procesamiento con **Pandas** para cálculo de:
    * Medias Móviles Simples (SMA 50).
    * Volatilidad en tiempo real (Desviación Estándar).
    * Variación porcentual dinámica.
4.  **Seguridad y Redes:**
    * Despliegue en **Azure Virtual Machine (Ubuntu 24.04)**.
    * **Nginx** como Proxy Inverso para gestión de puertos.
    * Certificados SSL/TLS (**HTTPS**) auto-renovables con Certbot.
5.  **Visualización:** Dashboard interactivo en **Streamlit**.

## 🛠 Tech Stack

* **Infraestructura:** Microsoft Azure (VM B2ats_v2), Nginx, Systemd.
* **Backend:** Python 3.10, Psycopg2, Dotenv.
* **Database:** Neon (Serverless PostgreSQL).
* **Frontend:** Streamlit, Pandas.
* **DevOps:** Git, SSH, Certbot.

---

## ⚙️ Instalación Local (Para Desarrollo)

Si deseas clonar y correr este proyecto en tu máquina local:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/PeepoClown04/sql-finance-system.git](https://github.com/PeepoClown04/sql-finance-system.git)
    cd sql-finance-system
    ```

2.  **Entorno Virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Configuración de Secretos:**
    Crea un archivo `.env` en la raíz con la conexión a tu base de datos (Neon o Local):
    ```ini
    # Cadena de conexión PostgreSQL
    DB_URL="postgres://usuario:password@endpoint.neon.tech/finance_db?sslmode=require"
    TELEGRAM_TOKEN="tu_token"
    CHAT_ID="tu_id"
    ```

4.  **Ejecutar:**
    ```bash
    # Iniciar Dashboard
    streamlit run dashboard.py
    ```

---

## 🚀 Despliegue (Comandos de Operación)

El servidor de producción se gestiona mediante servicios `systemd`:

```bash
# Ver estado del Dashboard
sudo systemctl status finance-dash

# Ver estado del Bot de Ingesta
sudo systemctl status finance-bot

# Ver logs en tiempo real
sudo journalctl -u finance-dash -f
