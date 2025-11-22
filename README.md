# moteur-recherche-lumina

discord: https://discord.gg/QkwWDKeMjF

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


En cas de problème, vous pouvez soit me contacter par [discord](https://discord.com/users/927137288763342868) ou par [mail](mailto:axel@ruikdev.me)




# engine-search-lumina


To use Lumina locally:

1: start the [main api](https://github.com/work-search/api_princ)
  enter in the console the starting site (for example work.weblink.ovh)
  the scrapping being in progress, waiting (to start, waiting 24h for example)
  when the number of sites is enough for you (you can obviously continue to index them)
  you need to retrieve the site’s BDD (it is the file sites_web.db). You will need to put it in the same directory as [the engine site](https://github.com/work-search/moteur-recherche-lumina)
  (you can also do the same steps with [the API for articles](https://github.com/work-search/API_article), but you are not obliged)

2: start the [site](https://github.com/work-search/moteur-recherche-lumina/)
  Go to the app.py file. This is the backend file of the entire site.
  Appointment at approximately line 125 to add one or more accounts to join /login the site in this form:
  users = {{
    "compteexemple1": "mdpexemple1",
    "compteexemple2": "mdpexemple2"
  }
  when it’s good, don’t forget to save the file, and you can start the file **app.py**
  And there you go, normally, if everything goes well, appointment on port 5000 of your machine.
  If nothing appears on port 5000 (in your browser), check the console, and check the last line of app.py


In case of a problem, you can either contact me by [discord](https://discord.com/users/927137288763342868) or by [mail](mailto:axel@athenox.dev)




## License

This project is licensed under the [GNU Affero General Public License v3.0](LICENSE).

You are free to use, modify, and distribute this code under the terms of the AGPL-3.0 license.  
Any modifications made and used over a network (including server-side deployments) must also be released under the AGPL-3.0.
