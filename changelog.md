#changelog

## [1.2] - 03-03-2023 Maxime Lemaitre

### Fixed

- Faille XSS fixé en rajoutant des fonctions Flask.escape sur le contenu du title et du body dans les fonction create et update de blog.py

## [1.3] - 03-03-2023 Maxime Lemaitre

### Fixed

- Faille de mot de passe non haché dans la base de données corrigé, en hachant le mot de passe dans auth.py avec du SHA512 pour se register, puis lors de la vérification pour se login

## [1.4] - 03-03-2023 Benjamin Brunelliere

### Fixed 

- Faille possibilité de changer la valeur du cookie pour changer de session, corrigé en créant un clé dans un fichier secret, modification de la secret_key de app.py

## [1.5] - 03-03-2023 Maxime Lemaitre

### Add

- Ajout du "Ratelimit" dans auth.py pour limiter le nombre de tentatives de connections pendant une certaine période. Cela limite le brute Force

## [1.6] - 03-03-2023 Romain Charrat

### Fixed

- Faille au niveau des injections SQL, utilisation de requète paramétrées pour éviter la prise en compte des doubles quotes par le language SQL.

## [1.7] - 03-03-2023 Maxime Lemaitre

### Fixed

- Correction de la faille CSRF en ajoutant la génération de token sur chaque cookies dans app.py, puis en vérifiant celui-ci dans chaque méthode "POST" dans les fichiers HTML

## [1.8] - 03-03-2023 Benjamin Brunelliere

### Replace

- Mise en place d'un systeme de session (Flask) qui remplace les cookies, les valeurs des sessions sont chiffrées par une clé privé. 

## [v_Final] - 03-03-2023

### add

- Fusion de toutes les versions de programme, pour en avoir une version final ayant le correctif sur toutes les vulnérabilités trouvées

## [v_Final] - 03-03-2023 Benjamin Brunelliere

- Mise à jour du Css et ajout d'un media dans le dossier src
