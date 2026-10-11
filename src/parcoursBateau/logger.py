import json
import os
import struct
import gzip 
from datetime import datetime

class Logger:
    def __init__(self, log_interval: int = 1, mode: str = "json", tri: str = "all", top_k: int = 20, save_neurones: int = 0):
        """Classe de logging pour stocker les données de la simulation à chaque frame et à la fin de chaque époque.
        log_interval : fréquence d'enregistrement des frames (ex: 1 = toutes les frames
        mode : "json" ou "binary" pour le format de sauvegarde
        tri : "all" pour tout sauvegarder, "best" pour ne sauvegarder que
                les top_k créatures à la fin de chaque époque
        top_k : nombre de créatures à sauvegarder si tri="best"
        save_neurones : sauvegarde au 1er frame de l'époque le réseau des x premiers bateaux
        """
        self.history = {}
        self.tempbuffer = {}
        self.log_interval = log_interval
        self.mode = mode
        self.tri = tri
        self.top_k = top_k
        self.save_neurones = save_neurones


    def add_frame(self, epoque: int, frame: int, creatures: list, objectifs: list):
        """À appeler à chaque frame pour stocker les données temporairement."""
        if frame % self.log_interval == 0:
            # On stocke temporairement en utilisant l'ID comme clé pour faciliter le filtrage
            self.tempbuffer[frame] = {
                "c": {c.id: [round(x, 3) for x in c.to_list()] for c in creatures},
                "o": [[round(x, 3) for x in o.to_list()] for o in objectifs]
            }

    def end_epoque(self, epoque: int, final_creatures: list):
        """À appeler à la fin de chaque époque/génération pour filtrer et archiver."""
        self.history[epoque] = {}
        
        valid_ids = None
        if self.tri == "best":
            # On trie les créatures par score décroissant et on garde les top_k
            top_creatures = sorted(final_creatures, key=lambda c: c.score, reverse=True)[:self.top_k]
            valid_ids = {c.id for c in top_creatures}

        # Identifier les bateaux dont on veut sauvegarder les neurones
        top_n_ids = {}
        if self.save_neurones > 0:
            top_n_creatures = sorted(final_creatures, key=lambda c: c.score, reverse=True)[:self.save_neurones]
            top_n_ids = {c.id: c for c in top_n_creatures}

        first_frame = min(self.tempbuffer.keys()) if self.tempbuffer else None

        for frame, data in self.tempbuffer.items():
            filtered_c = []
            
            for c_id, c_data in data["c"].items():
                if valid_ids is not None and c_id not in valid_ids:
                    continue
                
                c_list = list(c_data)

                # Seulement à la 1ère frame : ajouter le cerveau des meilleurs
                if frame == first_frame and self.save_neurones > 0 and c_id in top_n_ids:
                    creature = top_n_ids[c_id]
                    
                    # Récupération de toutes les couches + la sortie
                    neurones_data = [couche.save_for_log() for couche in creature.cerveau.couches]
                    neurones_data.append(creature.cerveau.outputs.save_for_log())
                    
                    # Pad avec 0.0 si la liste est incomplète, puis insert à l'index 4 (5ème élément)
                    while len(c_list) < 4:
                        c_list.append(0.0)
                    c_list.insert(4, neurones_data)

                filtered_c.append(c_list)

            # On recrée la structure attendue par la méthode save (liste de listes)
            self.history[epoque][frame] = {
                "c": filtered_c,
                "o": data["o"]
            }
        
        # On vide le buffer pour la génération suivante
        self.tempbuffer = {}

    def save(self, filepath: str = "logs"):
        """Sauvegarde de l'historique dans un fichier compressé (gzip) au format JSON ou binaire."""

        #Securité : on vérifie qu'il y a des données à sauvegarder
        if not self.history:
            return
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Préparation des métadonnées
        metadata = {
            "date": timestamp,
            "log_interval": self.log_interval,
            "mode": self.mode,
            "tri": self.tri,
            "top_k": self.top_k,
            "save_neurones": self.save_neurones
        }

        # MODE JSON:
        # On utilise gzip pour compresser le fichier JSON, ce qui est plus efficace que de stocker un gros JSON non compressé.
        # Le format JSON est plus lisible et facilement exploitable pour des analyses ultérieures, mais peut être plus volumineux que le binaire.
        # plus lent sur Unity

        if self.mode == "json":
            # On change l'extension en .json.gz
            full_path = os.path.join(filepath, f"log_{timestamp}.json.gz")
            try:
                                # Création de l'objet global avec métadonnées et historique
                export_data = {
                    "metadata": metadata,
                    "history": self.history
                }
                # "wt" signifie Write Text (gzip gère la conversion en binaire)
                with gzip.open(full_path, "wt", encoding="utf-8") as f:
                    # separators=(',', ':') enlève tous les espaces inutiles
                    json.dump(export_data, f, separators=(',', ':'))
                
                print(f"Sauvegarde compressée réussie : {full_path}")
            except Exception as e:
                print(f"Erreur : {e}")

        # MODE BINAIRE:
        # Le format binaire est plus compact et plus rapide à lire/écrire, mais
        # il nécessite une structure de données très rigide et n'est pas lisible

        elif self.mode == "binary":
            full_path = os.path.join(filepath, f"log_{timestamp}.bin")
            try:
                with open(full_path, "wb") as f:
                    # Magic Number pour identifier le fichier lors de la simu
                    f.write(b'TER01')
                    
                    # 1. Écrire le nombre d'époques (Int - 4 octets)
                    f.write(struct.pack('I', len(self.history)))

                    for epoque, frames in self.history.items():
                        # 2. Écrire l'ID de l'époque et le nombre de frames
                        f.write(struct.pack('II', int(epoque), len(frames)))

                        for frame, data in frames.items():
                            creatures = data.get("c", [])
                            objectifs = data.get("o", [])
                            
                            # 3. Header de la frame : ID frame, Nb créatures et Nb objectifs
                            f.write(struct.pack('III', int(frame), len(creatures), len(objectifs)))

                            # 4. On aplatit et on pack les créatures
                            flat_c = [val for c in creatures for val in c]
                            if flat_c:
                                f.write(struct.pack(f'{len(flat_c)}f', *flat_c))
                            
                            # 5. On aplatit et on pack les objectifs
                            flat_o = [val for o in objectifs for val in o]
                            if flat_o:
                                f.write(struct.pack(f'{len(flat_o)}f', *flat_o))

                print(f"Sauvegarde binaire réussie : {full_path}")
            except Exception as e:
                print(f"Erreur binaire : {e}")
        else:
            print(f"Mode de sauvegarde inconnu : {self.mode}")

    def unzip_log(self, compressed_filepath: str) -> dict:
        try:
            with gzip.open(compressed_filepath, "rt", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"Erreur lors de la décompression : {e}")
            return {}