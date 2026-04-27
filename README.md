# sap-basis-mcp

A Model Context Protocol (MCP) server for SAP Basis observability.

This project allows AI agents (such as Cline, Zed, or other MCP clients) to interact with SAP systems and retrieve operational data such as jobs, transports, dumps, work processes, and spool requests.

---

## What does this do?

This MCP server exposes SAP Basis information as structured tools:

* Jobs (SM37)
* Transports (STMS)
* Dumps (ST22)
* Work Processes (SM50 / SM66)
* Spool (SP01)

All data is retrieved using standard SAP tables and RFCs.

---

# Setup (PyRFC + SAP SDK)

This project uses **PyRFC**, which depends on the **SAP NetWeaver RFC SDK**.

Important:

* The SAP SDK is **not publicly distributed via pip**
* You must download it manually from SAP
* PyRFC will not work without it ([GitHub][1])

---

## Step 1 — Download SAP NW RFC SDK

You must download the SDK from the SAP Support Portal:

* Go to SAP Software Center
* Search for:
  **SAP NetWeaver RFC SDK 7.50**

You need:

* an SAP S-user (company access required)
* correct platform (Linux x86_64 recommended)

The SDK is SAP’s native RFC library used to communicate with SAP systems ([Soporte SAP][2])

---

## Step 2 — Extract the SDK

After downloading:

```bash
sapcar -xvf NWRFC_*.SAR
```

This will create a folder:

```txt
nwrfcsdk/
├── lib/
├── include/
```

---

## Step 3 — Configure environment variables

Set required environment variables:

```bash
export SAPNWRFC_HOME=/path/to/nwrfcsdk
export LD_LIBRARY_PATH=$SAPNWRFC_HOME/lib
```

These are required so Python can load the SAP native libraries.

---

## Step 4 — Install PyRFC

If your environment supports it:

```bash
pip install pyrfc
```

If that fails (common on Linux):

```bash
pip install --no-binary pyrfc pyrfc
```

On Linux, PyRFC is usually compiled locally against the SDK ([PyPI][3])

---

## Step 5 — Validate installation

Run:

```bash
python
```

Then:

```python
from pyrfc import Connection
```

---

## Step 6 — Project setup

Clone the repo:

```bash
git clone git@github.com:tokiou/sap-basis-mcp.git
cd sap-basis-mcp
```

Create virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Step 7 — Configure SAP credentials

Create a `.env` file:

```env
SAP_ASHOST=your_sap_host
SAP_SYSNR=00
SAP_CLIENT=100
SAP_USER=your_user
SAP_PASSWD=your_password
SAP_LANG=EN
```

---

## Step 8 — Test connection

Example:

```python
from pyrfc import Connection

conn = Connection(
    ashost="your_host",
    sysnr="00",
    client="100",
    user="user",
    passwd="password"
)

print(conn.call("STFC_CONNECTION"))
```

---

# Running the MCP

```bash
opencode
```

## Add this MCP to OpenCode

Create or update `opencode.json` in this project root:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "sap-ops-mcp": {
      "type": "local",
      "command": [
        "/absolute/path/to/sap-basis-mcp/.opencode/run_sap_ops_mcp.sh"
      ],
      "enabled": true,
      "timeout": 45000
    }
  }
}
```


---

## Example prompts (agent usage)

Use these directly in your MCP client.

Spanish:

* "Traeme los 10 jobs mas recientes y dime cuales estan fallando."
* "Muestrame los transportes recientes y valida el estado de SAPK-102BHINS4CORE."
* "Trae los dumps recientes y resumelos por usuario."
* "Muestrame los work processes en RUNNING y separalos por tipo."
* "Trae spool errors de hoy y dime si hay algo critico."
* "Hazme un resumen de salud SAP con jobs failed, dumps y work processes running."

English:

* "Show me the 10 most recent jobs and highlight which ones are failing."
* "List recent transports and check the status of SAPK-102BHINS4CORE."
* "Fetch recent dumps and summarize them by user."
* "Show RUNNING work processes and group them by type."
* "Get today's spool errors and tell me if anything looks critical."
* "Give me an SAP health summary using failed jobs, dumps, and running work processes."

---

# Available Tools

## Jobs (SM37)

* get_failed_jobs
* get_recent_jobs
* get_jobs_by_user
* get_long_running_jobs

Source: TBTCO

---

## Transports (STMS)

* get_recent_transports
* get_transport_status
* get_failed_transports

Sources: E070, E070A

---

## Dumps (ST22)

* get_recent_dumps
* get_dumps_by_user

Source: SNAP

---

## Work Processes (SM50 / SM66)

* get_work_processes
* get_running_work_processes
* get_work_processes_by_type

Source: RFC TH_WPINFO

---

## Spool (SP01)

* get_recent_spool_requests
* get_spool_errors
* get_spool_by_user

Source: TSP01

---

# Testing

Run:

```bash
pytest
```

Includes:

* Unit tests
* Integration tests against real SAP systems

---

# Notes

* No custom ABAP required
* Uses standard SAP tables and RFCs
* Some datasets (like spool) may be empty depending on system usage
* Designed for local usage (credentials via `.env`)

---

# Limitations

* No deep dump parsing
* No OS/filesystem metrics
* No centralized authentication
* Requires SAP SDK installed locally

---

# Troubleshooting

## ImportError: cannot load librfccm.so

Check:

```bash
echo $LD_LIBRARY_PATH
```

---

## pyrfc installation fails

* Ensure SDK is installed first
* Use build-from-source option

---

## No data returned

* SAP table may be empty
* Authorization issue
* No recent activity

---

# Summary

This project provides a simple way to expose SAP Basis data to AI agents using MCP, enabling programmatic access to SAP operations without relying on SAP GUI.

[1]: https://github.com/SAP-archive/PyRFC "SAP-archive/PyRFC"
[2]: https://support.sap.com/en/product/connectors/nwrfcsdk.html "SAP NetWeaver RFC SDK 7.50"
[3]: https://pypi.org/project/pyrfc "pyrfc"
