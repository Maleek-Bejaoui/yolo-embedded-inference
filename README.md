# Détection d’objets avec YOLO sur Raspberry Pi

## 1. Présentation du projet

Ce projet consiste à implémenter un système de **détection d’objets en temps réel à l’aide de YOLO** sur **Raspberry Pi**.  
L’ensemble du projet est installé et exécuté dans un **environnement virtuel Python**, garantissant l’isolation, la reproductibilité et la facilité de déploiement sur un autre Raspberry Pi.

Le projet est **finalisé et fonctionnel**.  
Ce document décrit **toutes les étapes d’installation et d’exécution** permettant de reproduire l’environnement.

---

## 2. Pré-requis matériels

- Raspberry Pi (recommandé : Raspberry Pi 4 ou Raspberry Pi 5)
- Caméra :
  - Caméra USB **ou**
  - Caméra CSI (Raspberry Pi Camera) ✅ 
- Carte microSD (16 Go minimum recommandé)
- Connexion Internet
---

## 3. Pré-requis logiciels
- Raspberry Pi Imager
- Système d’exploitation : **Raspberry Pi OS (64 bits recommandé)**
  - PRETTY_NAME="Debian GNU/Linux 12 (bookworm)
  - VERSION ="12 (bookworm)"
- Python : **Python 3.11.2**
- Git
---

## 4. Mise à jour du système

Avant toute installation d'OS, mettre à jour le système :

```bash
sudo apt update 
sudo apt upgrade 
sudo reboot
```
---

## 5. Configuration de la caméra CSI sur Raspberry Pi
### 5.1 Activation de la caméra
Éditer le fichier de configuration du firmware :
    
    sudo nano /boot/firmware/config.txt

Dans le fichier, Activer la détection automatique de la caméra et forcer le capteur IMX219.
Commenter (ou supprimer) la ligne existante si présente :
    
    camera_auto_detect=0

Ajouter les  lignes suivantes :    
    
    camera_auto_detect=1   
    dtoverlay=imx219

Afin de s’assurer que les modifications sont bien prises en compte par le système, il est recommandé d’effectuer un redémarrage :)


---

## 6. Test matériels & logiciels
### 6.1. Test de la caméra
Vérifier que la caméra est correctement détectée par le système :

    rpi:~/PATH $ rpi-cam-hello

 ✅ Résultat attendu : La caméra s’ouvre et affiche un flux vidéo pendant environ 6s.

### 6.2 Test internet 

Vérifier que le Raspberry Pi est connecté à Internet ( ping 4 fois )  :

    rpi:~/PATH $ ping -c 4 www.free.fr // c'est hello Internet pour nous les SE :)

 ✅ Résultat attendu : 4 packets transmitted , 4 received , 0% packet loss 


### 6.3 check version python 
    rpi:~/PATH $ python --version 

La version de Python doit être ≥ 3.9.
Le projet a été testé et validé avec Python 3.11.2.

:) Félicitations, le matériel et l’environnement système sont fonctionnels.

---

## 7. Création de l’environnement virtuel Python

Créer l’environnement virtuel Python :

    python3 -m venv yolo_env

Un fichier de configuration nommé **pyvenv.cfg** est automatiquement créé dans le répertoire yolo_env.

Il est possible de modifier ce fichier en changeant la ligne suivante du `false` vers `true`

    include-system-site-packages = true

Cela permet à l’environnement virtuel d’accéder aux bibliothèques Python déjà installées au niveau du système, ce qui peut simplifier certaines installations.
Le système reste toutefois isolé et n’utilise pas les bibliothèques installées dans l’environnement virtuel.

Activer ensuite l’environnement virtuel :

    source yolo_env/bin/activate


Toutes les commandes Python suivantes doivent être exécutées dans cet environnement.

---

## 8. Installation des dépendances système

Depuis l’environnement virtuel yolo_env, installer les bibliothèques Python :

### 8.1 Installation des bibliothèques python

Depuis l’environnement virtuel `yolo_env`, lancer l’installation :

    (yolo_env) rpi:~/PATH $ pip install --upgrade pip
    (yolo_env) rpi:~/PATH $ pip install -r requirements.txt

⏳ Cette étape peut prendre environ **10 minutes**, selon la connexion et le Raspberry Pi utilisé.

---

### 8.2 Vérification de l’installation 

Vérifier que YOLO est correctement installé :
⚠️ Lors du premier chargement, ne pas interrompre l’exécution (Ctrl+C), certaines initialisations peuvent prendre quelques instants.

    (yolo_env) rpi:~/PATH $ python3
    >>> from ultralytics import YOLO
    >>>

Si aucune erreur n’apparaît, l’installation de YOLO est terminée avec succès.

L’installation est désormais terminée.
Toutefois, cette étape peut introduire un problème de compatibilité.
La section suivante explique l’erreur rencontrée et la méthode pour la résoudre.

---

### 8.3 Test caméra après installation (`rpi-cam-hello`)

Relancer un test de la caméra :

    (yolo_env) rpi:~/PATH $  rpi-cam-hello

⚠️ Si une erreur apparaît à cette étape, cela indique généralement un conflit de dépendances Python (ex. NumPy), traité dans la section suivante.

#### Explication du problème

- La bibliothèque **rpicam** (caméra Raspberry Pi) dépend de **NumPy 1.24.2**
- Le package **Ultralytics** installe automatiquement une version plus récente de NumPy (**NumPy 2.1.3**)
- Cette mise à jour **casse la compatibilité avec rpicam**
- Résultat :
  - La caméra fonctionne **hors environnement virtuel**
  - Mais **ne fonctionne plus dans l’environnement YOLO**

👉 Ce comportement est normal :  
les environnements Python sont **isolés**, mais certaines dépendances système restent sensibles aux versions de bibliothèques.

---

#### Correction du conflit NumPy

Pour résoudre le problème, il faut **forcer une version compatible de NumPy** dans l’environnement virtuel YOLO.

Dans l’environnement `yolo_env`, exécuter :

    (yolo_env) rpi:~/PATH $ pip uninstall numpy==2.1.3
    (yolo_env) rpi:~/PATH $ pip install numpy==1.24.2
    (yolo_env) rpi:~/PATH $ pip list | grep numpy     // pour verfier la version   

Cela restaure la compatibilité avec la bibliothèque caméra.

---

### 8.4 Test YOLO + caméra avec `main_hello.py`

Cette étape consiste à valider le bon fonctionnement de l’ensemble du pipeline :
- accès à la caméra  CSI,
- chargement du modèle YOLO,
- inférence en temps réel sur le flux vidéo.



