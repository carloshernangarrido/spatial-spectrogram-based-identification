import json
import datetime
import inspect
import subprocess
from pathlib import Path


def get_git_commit():
    """Devuelve el hash del commit actual si existe git"""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return None


def log_inputs(module, output_dir="datos_corrida/logs", extra=None):
    """
    Guarda automáticamente todos los parámetros públicos
    definidos en inputs.py
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    data = {
        "timestamp": timestamp,
        "inputs_file": inspect.getsourcefile(module),
        "git_commit": get_git_commit(),
        "parameters": {},
    }

    if extra is not None:
        data["extra"] = extra

    for name, value in vars(module).items():
        if name.startswith("_"):
            continue
        if callable(value):
            continue

        try:
            json.dumps(value)
            data["parameters"][name] = value
        except TypeError:
            data["parameters"][name] = str(value)

    # JSON
    json_path = Path(output_dir) / f"run_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    # TXT
    txt_path = Path(output_dir) / f"run_{timestamp}.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"Run timestamp: {timestamp}\n")
        f.write(f"Inputs file: {data['inputs_file']}\n")
        f.write(f"Git commit: {data['git_commit']}\n\n")

        for k, v in data["parameters"].items():
            f.write(f"{k}: {v}\n")

    print(f"✔ Parámetros guardados en:\n  {json_path}\n  {txt_path}")

    return json_path
