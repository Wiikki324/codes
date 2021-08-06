import random



print("NOPPAPASIANSSI")
print("Anna  numerona monikosivuisia heitetään")
print("esim. 10 tai 6")

while True:

    try:
        noppa = (int(input("nopat: ")))
    except ValueError:
        print("anna arvo numerona")
        continue

    break


while True:
    if noppa < 2 or noppa > 10:
        noppa = 6
        print("Jospa heitetään 6 sivuista noppaa vaan..")
    ok = 1

    # Avataan nopan tallennettut pelit

    nopannimi = ("d" + str(noppa))
    print(nopannimi)
    # jos filua ei ole, luodaan nolla-arvoilla
    try:
        tiedosto = open(str(nopannimi) + ".txt", "r")
        rivit = tiedosto.readlines()
        tiedosto.close()
        if (len(rivit) != 13):
            ok = 0
    except FileNotFoundError:
        ok = 0
    if ok == 0:
        tiedosto = open(str(nopannimi) + ".txt", "w")
        tiedosto.write(str(nopannimi) + "\n")
        tiedosto.write("viimeisimmän heitot\n" + str(0) + "\n")
        tiedosto.write("pelit\n" + str(0) + "\n")
        tiedosto.write("keskiarvo\n" + str(0) + "\n")
        tiedosto.write("pisin\n" + str(0) + "\n")
        tiedosto.write("lyhin\n" + str(0) + "\n")
        tiedosto.write("heittoja yhteensä\n" + str(0) + "\n")
        tiedosto.close()

    tiedosto = open(str(nopannimi) + ".txt", "r")
    rivit = tiedosto.readlines()
    tiedosto.close()
    pelit = int(rivit[4])
    # print("pelejä pelattu: "pelit)
    keskiarvo = float(rivit[6])
    pisin = int(rivit[8])
    lyhin = int(rivit[10])
    yhteensa = int(rivit[12])

    # Aletaan heittamaan

    tulokset = list()
    poistettavat = list()
    heitot = 1
    print()
    print("Heitto", heitot)

    for i in range(noppa):
        tulokset.append(random.randrange(1, noppa + 1))
    tulokset.sort()
    print(tulokset)

    while True:

        etsitty = 1
        counter = 0
        maara = 0
        # Etsitaan toistuvat luvut
        while (counter < noppa):
            for i in tulokset:
                if i == etsitty:
                    maara = maara + 1
            if maara > 1:
                poistettavat.append(etsitty)
            etsitty = etsitty + 1
            maara = 0
            counter = counter + 1

        poistetut = list()
        poistetut = [i for i in tulokset if i in poistettavat]

        poistetutNopat = len(poistetut)
        if poistetutNopat == 0:
            break

        print("Poistetaan kaikki tulokset joita oli useampi kuin yksi:")
        print(poistetut)

        # poistetaan tulokset kädestä ne joita on enemmän kuin yksi
        # ohitetaan ne joita ei tarvitse poistaa(joita ei ole poistetut listassa) -> ei poisteta tulokset listalta
        print("Jäljelle jää:")
        for i in poistetut:
            try:
                tulokset.remove(i)
            except ValueError:
                pass
        print(tulokset)

        poistettavat.clear()
        poistetut.clear()

        uusikasi = list()
        jaljella = noppa - len(tulokset)
        print()
        heitot = heitot + 1
        print("Heitto", heitot)
        print("heitetään uusi käsi", jaljella, "noppaa")
        for i in range(jaljella):
            uusikasi.append(random.randrange(1, noppa + 1))
        uusikasi.sort()
        print(uusikasi)
        for i in uusikasi:
            tulokset.append(i)
        print("koko käsi")
        tulokset.sort()
        print(tulokset)
    print()
    print("*****Voitit!*****")
    print()
    print(heitot, "heittoa")
    print()
    print("*****************")
    print("___________")

    # print(len(rivit))
    # tallennettavat tiedot pelista
    pelit = pelit + 1
    if pisin < heitot:
        pisin = heitot
    if lyhin > heitot or lyhin == 0:
        lyhin = heitot
    yhteensa = yhteensa + heitot
    keskiarvo = round(yhteensa / pelit, 3)

    # pelidataatulostetaan
    print("pelit: " + str(pelit))
    print("keskiarvo: " + str(keskiarvo))
    print("pisin: " + str(pisin))
    print("lyhin: " + str(lyhin))
    print("heittoja yhteensä: " + str(yhteensa))
    print()

    # Keino tallenttaa pelien määrä, heittojen keskiarvo
    #maksimiheitot, minimiheitot, jne

    #nopannimi = ("d" + str(noppa))
    
    # print(noppa1)
    tiedosto = open(str(nopannimi) + ".txt", "w")
    tiedosto.write(str(nopannimi) + "\n")
    tiedosto.write("viimeisimmän heitot\n" + str(heitot) + "\n")
    tiedosto.write("pelit\n" + str(pelit) + "\n")
    tiedosto.write("keskiarvo\n" + str(keskiarvo) + "\n")
    tiedosto.write("pisin\n" + str(pisin) + "\n")
    tiedosto.write("lyhin\n" + str(lyhin) + "\n")
    tiedosto.write("heittoja yhteensä\n" + str(yhteensa) + "\n")
    tiedosto.close()

    # tiedosto.write(str(heitot))

    vastaus = input("heitä uudestaan samoilla nopilla: paina Enteriä\n"
                    "vaihda noppia: paina v\n"
                    "lopeta: paina q\n")
    if vastaus == ("q"):
        break
    if vastaus == "v":
        while True:

            try:
                noppa = (int(input("nopat: ")))
            except ValueError:
                print("anna arvo numerona")
                continue
            break
