# moteur-recherche-lumina

discord: https://discord.gg/QkwWDKeMjF

Pour utiliser Lumina en local :

1: start l'[api principal](https://github.com/work-search/lumibot)
  rentrer dans la console le site de départ (par exemple work.weblink.ovh)
  le scrapping étant en cours, attendait (pour commencer, attendais 24h par exemple)
  quand le nombre de sites vous suffit (vous pourrez bien évidemment continuer à en indexer)
  vous devez récupérer le BDD du site (il s'agit du fichier sites_web.db). Vous devrez le mettre dans le même répertoire que [le site du moteur](https://github.com/work-search/moteur-recherche-lumina) (dossier database)
  
2: start le [site](https://github.com/work-search/moteur-recherche-lumina/)
  Et voilà, normalement, si tout se passe bien, rdv sur le port 5000 de votre machine.
  Si jamais rien n'apparaît sur le port 5000 (dans votre navigateur), vérifiez la console, et vérifiez la dernière ligne d'app.py


En cas de problème, vous pouvez soit me contacter par [discord](https://discord.com/users/927137288763342868) ou par [mail](mailto:axel@ruikdev.me)





## License

This project is licensed under the [GNU Affero General Public License v3.0](LICENSE).

You are free to use, modify, and distribute this code under the terms of the AGPL-3.0 license.  
Any modifications made and used over a network (including server-side deployments) must also be released under the AGPL-3.0.
