from NEAT.cerveau import Cerveau
from pathlib import Path

seeds = ["seed1", "seed2", "seed3", "seed42"]
svg = ["10-11-12-13", "13"]
cerveaux = []
SAUVEGARDE_DIR = Path(__file__).resolve().parent / "sauvegardes bateaux" / "benchmark"

for i in range(len(svg)):
    c = Cerveau(1, 1, 1, 1, 1)
    for seed in seeds:
        c.load(SAUVEGARDE_DIR / seed, f"{svg[i]}.json")
        c.visualiser_num()

