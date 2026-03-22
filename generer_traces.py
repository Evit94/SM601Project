"""Script pour generer les traces d'execution de tous les graphes."""
import subprocess
import os

traces = ""
for i in range(1, 11):
    stdin_input = f"{i}\n2\n3\n0\n"
    result = subprocess.run(
        ["python3", "-c",
         "from src.affichage import menu_principal; menu_principal()"],
        input=stdin_input,
        capture_output=True,
        text=True,
        timeout=10,
    )
    sep = "=" * 80
    traces += f"{sep}\n"
    traces += f"  TRACE D'EXECUTION - GRAPHE {i}\n"
    traces += f"{sep}\n\n"
    traces += result.stdout
    traces += "\n\n"

os.makedirs("traces", exist_ok=True)
with open(os.path.join("traces", "traces_execution.txt"), "w") as f:
    f.write(traces)

print("Traces generees avec succes.")
print(f"Taille du fichier : {len(traces)} caracteres")
