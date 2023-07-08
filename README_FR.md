## Documentation des scripts OCR et GPT-3.5 

Ce document fournit des instructions pour la configuration et l'utilisation des scripts OCR et GPT-3.5 Turbo. Ces scripts travaillent de concert pour effectuer une reconnaissance optique de caractères (OCR) sur des fichiers et générer des réponses basées sur du texte à l'aide de GPT-3.5.

### 1. Prérequis

Avant de configurer et d'utiliser les scripts OCR et GPT-3.5 Turbo, assurez-vous de disposer des prérequis suivants :

- Python 3.x installé sur votre machine. [(Installer Python)](https://www.python.org/downloads/)
- Accès à un service d'API OCR et une clé d'API. [(OCR.space)](https://ocr.space/ocrapi/freekey)
- Une clé d'API OpenAI GPT-3.5 Turbo. [(OpenAI API)](https://platform.openai.com/docs/api-reference)


### Guide de démarrage rapide
1. Téléchargez ui.zip depuis le dossier dist
2. Extraire le dossier zip
3. Double-cliquez sur ui.exe

*Si vous souhaitez simplement utiliser le logiciel, c'est tout ce que vous avez à faire.
Continuez à lire si vous souhaitez modifier les scripts ou voir des exemples.*

### Table des matières

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Utilisation](#utilisation)
4. [Exemples](#exemples)


<a name="installation"></a>
### 2. Installation

Suivez ces étapes pour installer et configurer les scripts OCR et GPT-3.5 Turbo :

1. Clonez le dépôt contenant les scripts sur votre machine locale :

   ```
   git clone <repository_url>
   ```

2. Accédez au répertoire du dépôt cloné :

   ```
   cd <repository_directory>
   ```
   
3. Installez les dépendances Python requises à l'aide de `pip` :

   ```
   pip install -r requirements.txt
   ```

Une fois ces étapes terminées, toutes les dépendances devraient être installées et vous pouvez continuer à exécuter les scripts OCR et GPT-3.5.
<a name="configuration"></a>
### 3. Configuration

Lors de l'utilisation des scripts, vous devez configurer les paramètres OCR et GPT-3.5 Turbo. Cela peut être fait à partir d'une interface utilisateur en exécutant :

   ```
   python ui.py
   ```

### (Ci-dessous est facultatif)

Si vous ne souhaitez pas utiliser l'interface utilisateur, suivez ces étapes :

1. Configuration du script OCR :

   - Ouvrez le script `config.json` dans un éditeur de texte.
   - Configurez les paramètres de l'API OCR :
     - Définissez la variable `api_url` sur l'URL du service d'API OCR.
     - Définissez la variable `api_key` sur votre clé d'API OCR.
     - Définissez la variable `language` sur la langue OCR souhaitée.
     - Définissez la variable `output_format` sur le format de sortie OCR souhaité.
   - Configurez les chemins des fichiers d'entrée et de sortie :
     - Définissez la variable `input_file` sur le chemin du fichier d'entrée.
     - Définissez la variable `output_dir` sur le répertoire où les fichiers de sortie seront enregistrés.
   - Facultativement, ajustez d'autres paramètres tels que `max_file_size` et  la configuration de journalisation selon vos besoins.

2. Configuration du script GPT-3.5 Turbo :

   - Ouvrez le script `config.json` dans un éditeur de texte.
   - Configurez les paramètres de l'API GPT-3.5 Turbo :
     - Définissez la variable `jsonConfig.openai.api_key` sur votre clé d'API GPT-3.5 Turbo.
   - Configurez les chemins des fichiers d'entrée et de sortie :
     - Définissez la variable `jsonConfig.gpt.input_file` sur le chemin du fichier d'entrée pour GPT-3.5 Turbo.
     - Définissez la variable `jsonConfig.gpt.output_file` sur le chemin où la sortie de GPT-3.5 Turbo sera enregistrée.
   - Facultativement, ajustez d'autres paramètres tels que l'invite ou la taille des fragments.

<a name="utilisation"></a>
### 4. Utilisation

Pour utiliser les scripts OCR et GPT-3.5, suivez ces étapes (**Vous pouvez également utiliser ui.py**) :

1. Préparez le fichier d'entrée :
   - Assurez-vous que le fichier d'entrée est dans un format pris en charge (PDF, JPG, JPEG ou PNG).
   - Placez le fichier d'entrée dans le dossier "input-data".

2. Exécutez le script OCR :
   - Ouvrez un terminal ou une invite de commandes.
   - Accédez au répertoire où se trouve le script OCR.
   - Exécutez la commande suivante :

     ```
     python ocr.py
     ```

   - Le script OCR traitera le fichier d'entrée, effectuera une OCR et générera une sortie dans le format spécifié.

3. Exécutez le script GPT-3.5 :
   - Ouvrez un terminal ou une invite de commandes.
   - Accédez au répertoire où se trouve le script GPT-3.5.
   - Exécutez la commande suivante :

     ```
     node gptapi.js
     ```

   - Le script GPT-3.5 lira le fichier d'entrée généré par le script OCR, générera des réponses en utilisant GPT-3.5 et enregistrera la sortie dans le fichier spécifié.

<a name="exemples"></a>
### 5. Exemples

#### Exemple générique :
1. OCR :
   - Entrée : Un fichier PDF contenant des pages numérisées d'un livre.
   - Sortie : Des fichiers PDF individuels pour chaque page, enregistrés dans le répertoire de sortie spécifié. Le texte OCR sera ajouté au fichier `ocr_output.txt`.

2. GPT-3.5 Turbo :
   - Entrée : Texte généré par OCR à partir d'un livre, une invite demandant à mettre le texte dans un format de base de données.
   - Sortie : Texte généré par GPT-3.5 Turbo, enregistré dans le fichier de sortie spécifié.

#### Exemple spécifique :

1. OCR :
    - Entrée : Une image PNG à partir d'un livre de zoo numérisé contenant des images d'animaux et du texte sur les animaux.
    - Sortie : chien, chat, morse
              marron, rouge, gris,
              5, 2, 4

2. GPT-3.5 Turbo :
   - Entrée : Le texte généré par OCR ci-dessus, l'invite : "Pouvez-vous mettre le texte ci-dessous dans un format de base de données ?".
   - Sortie: 
   
        | Animal | Couleur | Quantité |
        |--------|---------|----------|
        | Chien  | Marron  | 5        |
        | Chat   | Rouge   | 2        |
        | Morse  | Gris    | 4        |


Vous pouvez modifier la configuration et adapter les scripts à vos cas d'utilisation spécifiques, formats de fichiers et services d'API.

Veuillez noter que ces scripts fournissent une implémentation de base et que vous devrez peut-être les personnaliser davantage en fonction de vos besoins et de vos cas d'utilisation spécifiques.