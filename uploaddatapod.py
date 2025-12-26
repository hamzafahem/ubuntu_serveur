import os
import requests
import json
from pathlib import Path
import time
from datetime import datetime

# ============================================================================
# ⚙️ CONFIGURATION
# ============================================================================
API_BASE_URL = "http://vps-2865504b.vps.ovh.net:8082/docket/api"
UTILS_API_URL = "http://localhost:8082/api/utils"
JWT_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiQURNSU4iLCJzdWIiOiJhZG1pbkBtZWRhZnJpY2EuY29tIiwiaWF0IjoxNzY0MjM0OTk3LCJleHAiOjE3NjQzMjEzOTd9.ILj5BGIQBMR2tWJ0Vn0YYHvbNLS4YnN8WYYOIBWsGZ0"
DEST_DIR = r"C:\Users\Hamza Maanaoui\Desktop\Docket-med_VersionFinalAdapter\DocketFILE"
# r"Z:\Documents\Docket-med_VersionFinalAdapter\Docket-med55\docket-medaf\DossierLTA-POD\dockets"

JSON_HEADERS = {
    "Authorization": f"Bearer {JWT_TOKEN}",
    "accept": "*/*",
    "Content-Type": "application/json"
}

# ============================================================================
# 📝 GÉNÉRATION DU RAPPORT
# ============================================================================
def generate_report(stats_data, output_dir=DEST_DIR):
    """Génère un rapport détaillé en format texte"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"RAPPORT_UPLOAD_{timestamp}.txt"
    report_path = os.path.join(output_dir, report_filename)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("📊 RAPPORT D'UPLOAD - DOCKET SYSTEM\n")
        f.write("="*80 + "\n")
        f.write(f"📅 Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"📁 Répertoire: {DEST_DIR}\n")
        f.write("\n")
        
        # STATISTIQUES GÉNÉRALES
        f.write("="*80 + "\n")
        f.write("📈 STATISTIQUES GÉNÉRALES\n")
        f.write("="*80 + "\n")
        f.write(f"📁 Dossiers totaux analysés: {stats_data['total_folders']}\n")
        f.write(f"✅ Dockets existants dans la base: {stats_data['existing_dockets']}\n")
        f.write(f"🆕 Dockets créés: {stats_data['created_dockets']}\n")
        f.write(f"❌ Dockets non créés (échecs): {stats_data['failed_creations']}\n")
        f.write(f"📄 Dossiers avec LTA: {stats_data['folders_with_lta']}\n")
        f.write(f"📦 Dossiers avec POD: {stats_data['folders_with_pod']}\n")
        f.write("\n")
        
        # RÉSULTATS UPLOAD
        f.write("="*80 + "\n")
        f.write("📤 RÉSULTATS D'UPLOAD\n")
        f.write("="*80 + "\n")
        f.write(f"✅ Uploads réussis: {stats_data['successful_uploads']}\n")
        f.write(f"❌ Uploads échoués: {stats_data['failed_uploads']}\n")
        f.write(f"📋 Total LTA uploadés: {stats_data['lta_uploaded']}\n")
        f.write(f"📦 Total POD uploadés: {stats_data['pod_uploaded']}\n")
        f.write(f"⏱️ Temps total: {stats_data['total_time']:.2f} secondes\n")
        f.write(f"⚡ Vitesse moyenne: {stats_data['avg_speed']:.2f} fichiers/seconde\n")
        f.write("\n")
        
        # DOCKETS NON TROUVÉS
        if stats_data['missing_dockets']:
            f.write("="*80 + "\n")
            f.write("❌ DOCKETS NON TROUVÉS DANS LA BASE (AVANT CRÉATION)\n")
            f.write("="*80 + "\n")
            f.write(f"Total: {len(stats_data['missing_dockets'])} dossiers\n")
            f.write("-"*80 + "\n")
            for i, folder in enumerate(stats_data['missing_dockets'], 1):
                f.write(f"{i}. {folder}\n")
            f.write("\n")
        
        # DOCKETS CRÉÉS AVEC SUCCÈS
        if stats_data['successfully_created']:
            f.write("="*80 + "\n")
            f.write("✅ DOCKETS CRÉÉS AVEC SUCCÈS\n")
            f.write("="*80 + "\n")
            f.write(f"Total: {len(stats_data['successfully_created'])} dossiers\n")
            f.write("-"*80 + "\n")
            for i, (folder, docket_id) in enumerate(stats_data['successfully_created'], 1):
                f.write(f"{i}. {folder} → ID: {docket_id}\n")
            f.write("\n")
        
        # ÉCHECS DE CRÉATION
        if stats_data['creation_failures']:
            f.write("="*80 + "\n")
            f.write("❌ ÉCHECS DE CRÉATION DE DOCKETS\n")
            f.write("="*80 + "\n")
            f.write(f"Total: {len(stats_data['creation_failures'])} dossiers\n")
            f.write("-"*80 + "\n")
            for i, folder in enumerate(stats_data['creation_failures'], 1):
                f.write(f"{i}. {folder}\n")
            f.write("\n")
        
        # UPLOADS RÉUSSIS
        if stats_data['successful_upload_details']:
            f.write("="*80 + "\n")
            f.write("✅ DÉTAILS DES UPLOADS RÉUSSIS\n")
            f.write("="*80 + "\n")
            f.write(f"Total: {len(stats_data['successful_upload_details'])} fichiers\n")
            f.write("-"*80 + "\n")
            for i, detail in enumerate(stats_data['successful_upload_details'], 1):
                f.write(f"{i}. [{detail['type']}] {detail['folder']} → {detail['file']}\n")
            f.write("\n")
        
        # ÉCHECS D'UPLOAD
        if stats_data['failed_upload_details']:
            f.write("="*80 + "\n")
            f.write("❌ DÉTAILS DES ÉCHECS D'UPLOAD\n")
            f.write("="*80 + "\n")
            f.write(f"Total: {len(stats_data['failed_upload_details'])} fichiers\n")
            f.write("-"*80 + "\n")
            for i, detail in enumerate(stats_data['failed_upload_details'], 1):
                f.write(f"{i}. [{detail['type']}] {detail['folder']} → {detail['file']}\n")
                if 'error' in detail:
                    f.write(f"   Erreur: {detail['error']}\n")
            f.write("\n")
        
        # DOSSIERS SANS FICHIERS
        if stats_data['folders_without_files']:
            f.write("="*80 + "\n")
            f.write("⚠️ DOSSIERS SANS FICHIERS LTA/POD\n")
            f.write("="*80 + "\n")
            f.write(f"Total: {len(stats_data['folders_without_files'])} dossiers\n")
            f.write("-"*80 + "\n")
            for i, folder in enumerate(stats_data['folders_without_files'], 1):
                f.write(f"{i}. {folder}\n")
            f.write("\n")
        
        f.write("="*80 + "\n")
        f.write("📋 FIN DU RAPPORT\n")
        f.write("="*80 + "\n")
    
    print(f"\n📝 Rapport généré: {report_filename}")
    return report_path

# ============================================================================
# 🗂️ MAPPING AUTOMATIQUE
# ============================================================================
def get_docket_mapping_from_api():
    """Récupère le mapping des dockets depuis l'API Spring Boot"""
    url = f"{UTILS_API_URL}/docket-mapping"
    print(f"🔍 Récupération du mapping depuis l'API...")
    try:
        response = requests.get(url, headers=JSON_HEADERS, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                mapping = data.get("mapping", {})
                total = data.get("totalDockets", 0)
                print(f"✅ Mapping récupéré: {total} dockets")
                return mapping
            else:
                print(f"❌ Erreur API: {data.get('error')}")
                return None
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

# ============================================================================
# 🆕 CRÉATION AUTOMATIQUE DE DOCKET
# ============================================================================
def create_docket_from_folder_name(folder_name):
    """Crée un docket automatiquement depuis le nom du dossier"""
    url = f"{API_BASE_URL}/dockets"
    
    parts = folder_name.split('-')
    
    payload = {
        "docketNumber": folder_name,
        "status": "CREATED",
        "shipper": "AUTO_IMPORT",
        "consignee": "AUTO_IMPORT",
        "origin": parts[0] if len(parts) > 0 else "Unknown",
        "destination": "AUTO",
        "weight": 0.0,
        "volume": 0.0
    }
    
    try:
        response = requests.post(url, headers=JSON_HEADERS, json=payload, timeout=30)
        if response.status_code in (200, 201):
            data = response.json()
            docket_id = data.get('id')
            print(f"   ✅ Docket créé: ID={docket_id}")
            return docket_id
        else:
            print(f"   ❌ Erreur création: {response.status_code}")
            return None
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return None

# ============================================================================
# 🔧 CRÉATION MANUELLE DES 6 DOCKETS PROBLÉMATIQUES
# ============================================================================
def create_missing_dockets_manually():
    """Crée les 6 dockets problématiques avec les bons numéros"""
    
    # Mapping: nom_dossier → vrai_numero_docket (du fichier POD)
    manual_mappings = {
        '135-66526390': '235-66526390',
        '157-08924149': '157-89241493',
        '157-09615372': '157-96153724',
        '157-89241861': '157-89241891',
        '235-03711439': '235-37114394',
        '235-04206346': '235-42063464'
    }
    
    print("\n🔧 CRÉATION MANUELLE DES 6 DOCKETS PROBLÉMATIQUES")
    print("="*60)
    
    created = []
    failed = []
    
    for folder_name, correct_number in manual_mappings.items():
        print(f"\n📁 Dossier: {folder_name}")
        print(f"   🔢 Numéro correct: {correct_number}")
        
        url = f"{API_BASE_URL}/dockets"
        parts = correct_number.split('-')
        
        payload = {
            "docketNumber": correct_number,
            "status": "CREATED",
            "shipper": "AUTO_IMPORT",
            "consignee": "AUTO_IMPORT",
            "origin": parts[0] if len(parts) > 0 else "Unknown",
            "destination": "AUTO",
            "weight": 0.0,
            "volume": 0.0
        }
        
        try:
            response = requests.post(url, headers=JSON_HEADERS, json=payload, timeout=30)
            if response.status_code in (200, 201):
                data = response.json()
                docket_id = data.get('id')
                print(f"   ✅ Docket créé: ID={docket_id}")
                created.append((correct_number, docket_id))
            else:
                print(f"   ❌ Erreur {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   💬 {error_data.get('message', 'Erreur inconnue')}")
                except:
                    pass
                failed.append(correct_number)
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            failed.append(correct_number)
        
        time.sleep(0.3)
    
    print("\n" + "="*60)
    print(f"📊 RÉSULTAT: {len(created)} créés ✅ | {len(failed)} échecs ❌")
    print("="*60)
    
    if created:
        print("\n✅ Dockets créés:")
        for num, docket_id in created:
            print(f"   • {num} → ID: {docket_id}")
    
    if failed:
        print("\n❌ Échecs:")
        for num in failed:
            print(f"   • {num}")
    
    return created, failed

# ============================================================================
# 📤 UPLOAD ULTIME
# ============================================================================
def upload_document_ultimate(docket_id, document_type, file_path, file_description=""):
    """Solution ultime pour l'upload"""
    try:
        if not os.path.exists(file_path):
            print(f"   ❌ Fichier introuvable: {file_path}")
            return False, "Fichier introuvable"

        file_size = os.path.getsize(file_path) / (1024 * 1024)
        if file_size > 10:
            print(f"   ⚠️ Fichier trop volumineux ({file_size:.1f}MB)")
            return False, f"Fichier trop volumineux ({file_size:.1f}MB)"

        url = f"{API_BASE_URL}/dockets/{docket_id}/documents?type={document_type}"
        
        if file_description:
            print(f"   📤 {file_description}")

        session = requests.Session()
        session.headers.clear()
        session.headers.update({
            "Authorization": f"Bearer {JWT_TOKEN}",
            "accept": "*/*"
        })

        with open(file_path, 'rb') as f:
            file_content = f.read()

        boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(file_path)}"\r\n'
            f"Content-Type: application/pdf\r\n"
            f"\r\n"
        ).encode('utf-8') + file_content + f"\r\n--{boundary}--\r\n".encode('utf-8')

        headers_manual = {
            "Authorization": f"Bearer {JWT_TOKEN}",
            "accept": "*/*",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body))
        }

        resp = session.post(url, data=body, headers=headers_manual, timeout=60)

        if resp.status_code in (200, 201):
            print("   ✅ Réussi")
            return True, None
        else:
            error_msg = f"HTTP {resp.status_code}"
            try:
                error_data = resp.json()
                error_msg = error_data.get('message', error_msg)
            except:
                pass
            print(f"   ❌ Erreur {resp.status_code}")
            return False, error_msg

    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False, str(e)

# ============================================================================
# 🔍 ANALYSE COMPLÈTE
# ============================================================================
def analyze_all_folders(base_path):
    """Analyse TOUS les dossiers locaux"""
    print("🔍 Analyse de TOUS les dossiers locaux...")
    all_folders = [d for d in base_path.iterdir() if d.is_dir()]
    structure_info = {}

    for folder in all_folders:
        folder_name = folder.name.strip()
        structure_info[folder_name] = {
            'lta_file': None,
            'pod_file': None,
            'has_lta': False,
            'has_pod': False
        }

        # LTA
        lta_path = folder / "LTA"
        if lta_path.exists():
            pdf_files = sorted(list(lta_path.glob("*.pdf")) + list(lta_path.glob("*.PDF")))
            if pdf_files:
                structure_info[folder_name]['lta_file'] = pdf_files[0]
                structure_info[folder_name]['has_lta'] = True

        # POD
        pod_path = folder / "POD"
        if pod_path.exists():
            pdf_files = sorted(list(pod_path.glob("*.pdf")) + list(pod_path.glob("*.PDF")))
            if pdf_files:
                structure_info[folder_name]['pod_file'] = pdf_files[0]
                structure_info[folder_name]['has_pod'] = True

    # Statistiques
    total_folders = len(all_folders)
    folders_with_lta = sum(1 for info in structure_info.values() if info['has_lta'])
    folders_with_pod = sum(1 for info in structure_info.values() if info['has_pod'])

    print(f"📊 STRUCTURE ANALYSÉE:")
    print(f"   📁 Dossiers totaux: {total_folders}")
    print(f"   📄 Dossiers avec LTA: {folders_with_lta}")
    print(f"   📦 Dossiers avec POD: {folders_with_pod}")

    return structure_info

# ============================================================================
# 🔁 UPLOAD TOUS LES DOSSIERS (AVEC RAPPORT)
# ============================================================================
def upload_all_folders_with_auto_create():
    """Upload TOUS les dossiers - crée les dockets manquants + génère un rapport"""
    base = Path(DEST_DIR)
    if not base.exists():
        print(f"❌ Dossier source introuvable: {DEST_DIR}")
        return

    # Initialiser les statistiques
    stats = {
        'total_folders': 0,
        'existing_dockets': 0,
        'created_dockets': 0,
        'failed_creations': 0,
        'folders_with_lta': 0,
        'folders_with_pod': 0,
        'successful_uploads': 0,
        'failed_uploads': 0,
        'lta_uploaded': 0,
        'pod_uploaded': 0,
        'total_time': 0,
        'avg_speed': 0,
        'missing_dockets': [],
        'successfully_created': [],
        'creation_failures': [],
        'successful_upload_details': [],
        'failed_upload_details': [],
        'folders_without_files': []
    }

    print("🔄 Récupération du mapping...")
    docket_mapping = get_docket_mapping_from_api()
    if docket_mapping is None:
        docket_mapping = {}

    # Analyser TOUS les dossiers
    structure_info = analyze_all_folders(base)
    stats['total_folders'] = len(structure_info)
    stats['folders_with_lta'] = sum(1 for info in structure_info.values() if info['has_lta'])
    stats['folders_with_pod'] = sum(1 for info in structure_info.values() if info['has_pod'])

    # Préparer l'upload
    upload_queue = []
    dockets_to_create = []

    print("\n🔍 Vérification des dockets...")
    
    for folder_name, folder_info in structure_info.items():
        # Vérifier si le docket existe
        if folder_name not in docket_mapping:
            dockets_to_create.append(folder_name)
            stats['missing_dockets'].append(folder_name)
        else:
            docket_id = docket_mapping[folder_name]
            
            # Ajouter LTA si existe
            if folder_info['has_lta']:
                upload_queue.append({
                    'type': 'LTA',
                    'docket_id': docket_id,
                    'folder_name': folder_name,
                    'file_path': folder_info['lta_file'],
                    'description': f"LTA: {folder_info['lta_file'].name}"
                })

            # Ajouter POD si existe
            if folder_info['has_pod']:
                upload_queue.append({
                    'type': 'POD',
                    'docket_id': docket_id,
                    'folder_name': folder_name,
                    'file_path': folder_info['pod_file'],
                    'description': f"POD: {folder_info['pod_file'].name}"
                })
            
            # Vérifier dossiers sans fichiers
            if not folder_info['has_lta'] and not folder_info['has_pod']:
                stats['folders_without_files'].append(folder_name)

    stats['existing_dockets'] = len(structure_info) - len(dockets_to_create)

    print(f"\n📊 BILAN:")
    print(f"   ✅ Dockets existants: {stats['existing_dockets']}")
    print(f"   🆕 Dockets à créer: {len(dockets_to_create)}")
    print(f"   📄 Fichiers prêts: {len(upload_queue)}")

    # Créer les dockets manquants
    if dockets_to_create:
        print(f"\n🆕 Création de {len(dockets_to_create)} dockets manquants...")
        print(f"📋 Liste des dockets manquants:")
        for i, folder in enumerate(dockets_to_create, 1):
            print(f"   {i}. {folder}")
        
        confirm_create = input("\n   Créer automatiquement ? (o/N): ").strip().lower()
        
        if confirm_create == 'o':
            for folder_name in dockets_to_create:
                print(f"\n📁 {folder_name}")
                docket_id = create_docket_from_folder_name(folder_name)
                
                if docket_id:
                    stats['created_dockets'] += 1
                    stats['successfully_created'].append((folder_name, docket_id))
                    docket_mapping[folder_name] = docket_id
                    
                    folder_info = structure_info[folder_name]
                    
                    # Ajouter LTA
                    if folder_info['has_lta']:
                        upload_queue.append({
                            'type': 'LTA',
                            'docket_id': docket_id,
                            'folder_name': folder_name,
                            'file_path': folder_info['lta_file'],
                            'description': f"LTA: {folder_info['lta_file'].name}"
                        })
                    
                    # Ajouter POD
                    if folder_info['has_pod']:
                        upload_queue.append({
                            'type': 'POD',
                            'docket_id': docket_id,
                            'folder_name': folder_name,
                            'file_path': folder_info['pod_file'],
                            'description': f"POD: {folder_info['pod_file'].name}"
                        })
                else:
                    stats['failed_creations'] += 1
                    stats['creation_failures'].append(folder_name)
                
                time.sleep(0.3)
            
            print(f"\n✅ {stats['created_dockets']} dockets créés, {stats['failed_creations']} échecs")

    # Afficher récapitulatif final
    total_lta = sum(1 for item in upload_queue if item['type'] == 'LTA')
    total_pod = sum(1 for item in upload_queue if item['type'] == 'POD')
    
    print(f"\n📦 FICHIERS À UPLOADER:")
    print(f"   📁 Dossiers: {len(set(item['folder_name'] for item in upload_queue))}")
    print(f"   📄 Total fichiers: {len(upload_queue)}")
    print(f"   📋 LTA: {total_lta}")
    print(f"   📦 POD: {total_pod}")

    if not upload_queue:
        print("❌ Aucun fichier à uploader")
        # Générer rapport même si pas d'upload
        generate_report(stats)
        return

    # Confirmation upload
    print(f"\n⚠️ Vous allez uploader {len(upload_queue)} fichiers")
    confirm = input("   Continuer ? (o/N): ").strip().lower()
    if confirm != 'o':
        print("❌ Annulé")
        # Générer rapport partiel
        generate_report(stats)
        return

    # Upload
    print("\n🚀 DÉBUT DE L'UPLOAD...")
    print("="*60)
    start_time = time.time()

    for i, item in enumerate(upload_queue, 1):
        print(f"\n[{i}/{len(upload_queue)}] 📁 {item['folder_name']}")
        print(f"   🆔 Docket: {item['docket_id']}")
        
        ok, error = upload_document_ultimate(
            item['docket_id'],
            item['type'],
            item['file_path'],
            item['description']
        )

        if ok:
            stats['successful_uploads'] += 1
            if item['type'] == 'LTA':
                stats['lta_uploaded'] += 1
            else:
                stats['pod_uploaded'] += 1
            
            stats['successful_upload_details'].append({
                'type': item['type'],
                'folder': item['folder_name'],
                'file': item['file_path'].name,
                'docket_id': item['docket_id']
            })
        else:
            stats['failed_uploads'] += 1
            stats['failed_upload_details'].append({
                'type': item['type'],
                'folder': item['folder_name'],
                'file': item['file_path'].name,
                'docket_id': item['docket_id'],
                'error': error
            })

        # Afficher progression toutes les 10 uploads
        if i % 10 == 0:
            elapsed = time.time() - start_time
            avg_speed = i / elapsed if elapsed > 0 else 0
            remaining = len(upload_queue) - i
            eta = remaining / avg_speed if avg_speed > 0 else 0
            print(f"\n   📊 Progression: {i}/{len(upload_queue)} ({i*100//len(upload_queue)}%)")
            print(f"   ⚡ Vitesse: {avg_speed:.1f} fichiers/sec")
            print(f"   ⏱️ Temps restant estimé: {eta/60:.1f} minutes")

        if i % 5 == 0:
            time.sleep(0.5)
        else:
            time.sleep(0.2)

    end_time = time.time()
    stats['total_time'] = end_time - start_time
    if stats['total_time'] > 0:
        stats['avg_speed'] = len(upload_queue) / stats['total_time']

    print("\n" + "="*60)
    print("📊 RAPPORT FINAL")
    print("="*60)
    print(f"🆕 Dockets créés: {stats['created_dockets']}")
    print(f"✅ Uploads réussis: {stats['successful_uploads']}")
    print(f"❌ Uploads échoués: {stats['failed_uploads']}")
    print(f"📋 LTA uploadés: {stats['lta_uploaded']}")
    print(f"📦 POD uploadés: {stats['pod_uploaded']}")
    print(f"📄 Total fichiers: {len(upload_queue)}")
    print(f"⏱️ Temps total: {stats['total_time']:.1f} secondes ({stats['total_time']/60:.1f} minutes)")
    print(f"⚡ Vitesse moyenne: {stats['avg_speed']:.2f} fichiers/seconde")

    # Générer le rapport
    report_path = generate_report(stats)
    print(f"\n✅ Rapport détaillé sauvegardé dans:")
    print(f"   {report_path}")

# ============================================================================
# 🎮 MENU PRINCIPAL
# ============================================================================
if __name__ == "__main__":
    print("="*60)
    print("🚀 DOCKET UPLOAD SYSTEM - VERSION COMPLÈTE")
    print("="*60)
    print("📁 Répertoire:", DEST_DIR)
    print("="*60)
    
    while True:
        print("\n📋 MENU PRINCIPAL:")
        print("1. 📊 Voir les statistiques")
        print("2. 🚀 UPLOAD TOUS LES DOSSIERS (avec rapport)")
        print("3. 🔧 Créer les 6 dockets manuellement")
        print("4. ❌ Quitter")
        
        choice = input("\nVotre choix (1-4): ").strip()
        
        if choice == "1":
            base = Path(DEST_DIR)
            if base.exists():
                analyze_all_folders(base)
            else:
                print(f"❌ Dossier introuvable: {DEST_DIR}")
            
        elif choice == "2":
            upload_all_folders_with_auto_create()
            
        elif choice == "3":
            create_missing_dockets_manually()
            
        elif choice == "4":
            print("\n" + "="*60)
            print("👋 Au revoir!")
            print("="*60)
            break
        else:
            print("❌ Choix invalide, veuillez choisir entre 1 et 4")