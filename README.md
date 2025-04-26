# moteur-recherche-lumina


Pour utiliser Lumina en local :

1: start l'[api principal](https://github.com/work-search/api_princ)
  rentrer dans la console le site de départ (par exemple work.weblink.ovh)
  le scrapping étant en cours, attendait (pour commencer, attendais 24h par exemple)
  quand le nombre de sites vous suffit (vous pourrez bien évidemment continuer à en indexer)
  vous devez récupérer le BDD du site (il s'agit du fichier sites_web.db). Vous devrez le mettre dans le même répertoire que [le site du moteur](https://github.com/work-search/moteur-recherche-lumina)
  (vous pouvez aussi faire les mêmes étapes avec [l'API pour les articles](https://github.com/work-search/API_article), mais vous n'êtes pas obligé)

2: start le [site](https://github.com/work-search/moteur-recherche-lumina/)
  Aller dans le fichier app.py. Il s'agit du fichier backend de l'intégralité du site.
  RDV à environ la ligne 125 pour ajouter un ou plusieurs comptes pour se co à /login du site sous cette forme :
  users = {
    "compteexemple1": "mdpexemple1",
    "compteexemple2": "mdpexemple2"
  }
  quand c'est bon, n'oubliez pas de sauvegarder le fichier, et vous pouvez start le fichier **app.py**
  Et voilà, normalement, si tout se passe bien, rdv sur le port 5000 de votre machine.
  Si jamais rien n'apparaît sur le port 5000 (dans votre navigateur), vérifiez la console, et vérifiez la dernière ligne d'app.py


En cas de problème, vous pouvez soit me contacter par [discord](https://discord.com/users/927137288763342868) ou par [mail](axel@athenox.dev)
