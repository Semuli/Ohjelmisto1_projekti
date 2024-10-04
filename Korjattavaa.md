# Korjattavat asiat

### Tietokanta

- Scoreboradissa on kirjoitusvirhe: Scrore pitäisi olla score
- Skriptillä luodusta scoreboardista puuttuu primary key.
- Scoreboardissa ei ole auto_increment päällä, niin sinne ei voi liäsätä tietoa ilman, että antaa samalla aina uuden id:n <--- uuden uniikin id:n luominen ohjelmassa koodilla ei vaikuta mahdolliselta...
- ^Position sarakkeen nimi? Pitäisikö olla id? Taulun tiedot ei kuitenkaan päivity siten, että position sarake pitäisi paikkansa.


### Koodi

- Toi lentokenttien hakeminen tuottaa välillä erroreita. Current sijainti liian etelässä/pohjoisessa/idässä/lännessä? Ei pysty siksi hakemaan lentokenttiä kaikista suunnista? Tossa alla on kuvankaappauksia näistä erroreista.

![error1](https://github.com/user-attachments/assets/bad06281-bab5-4455-968b-ac6e6c37e70b)

![error2](https://github.com/user-attachments/assets/66f0f550-a6dd-4056-9b91-a7885718e65a)

![error3](https://github.com/user-attachments/assets/c784e124-1930-41ea-a5f2-9d14891e3645)

![error4](https://github.com/user-attachments/assets/119085bf-6099-47eb-9881-ee3f79e2ce6b)
