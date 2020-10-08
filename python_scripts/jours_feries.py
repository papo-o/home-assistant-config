""" https://pon.fr/home-assistant-infos-du-jour-et-du-lendemain/ """
""" https://github.com/papo-o/home-assistant-config/blob/master/python_scripts/jours_feries.py """


"""  This script creates sensors that will display the saints of the day   """
"""      and the day after, of the possible holidays and birthdays         """
"""          of the day and the day after. For the birdays it              """
"""              will return years as an attribute                         """

"""       Requires python_script: to be enabled in you configuration       """

""" Usage:                                                                 """
"""                                                                        """
""" automation:                                                            """
"""   alias: Refresh jours feries sensors                                  """
"""   trigger:                                                             """
"""     platform: time                                                     """
"""     at: '00:00:01'                                                     """
"""   action:                                                              """
"""     service: python_script.jours_feries                                """
"""     data:                                                              """
"""       name: "jours_feries"                                             """


""" This will create 6 sensors. two for saints, two for publics hollidays, """
"""    mother and father days, grandmother and grandfather days and two    """
"""      for birthday. One for today and the other for tomorrow            """
"""         the attribute 'age' will show the number of years              """

"""       example to display sensors with the auto-entities card           """

"""    - type: custom:auto-entities                                        """
"""      card:                                                             """
"""        type: entities                                                  """
"""        title: "Infos du jour"                                          """
"""        show_header_toggle: false                                       """
"""      filter:                                                           """
"""        include:                                                        """
"""          - entity_id: /saint/                                          """
"""          - entity_id: /_ferie/                                         """
"""          - entity_id: /_anniversaire/                                  """
"""        exclude:                                                        """
"""          - state: "unavailable"                                        """

today = datetime.datetime.now().date()
aujourdhui = today.day
demain = int(aujourdhui) + 1
mois = today.month
annee = today.year
day = '{:02d}'.format(today.day)
tomorrow = '{:02d}'.format((today + datetime.timedelta(days=1)).day)
month = '{:02d}'.format(today.month)
feteaujourdhui = day+":"+month
fetedemain = tomorrow+":"+month

def listeanniversaires(an):
    """Liste des anniversaires"""
    F = []  # =liste des dates des anniversaires en date-liste d=[j,m,a]
    L = []  # =liste des libelles des anniversaires

    d = [3,5,1954] 
    F.append(d)
    L.append(u"de Pierre")
    
    d = [4,5,1978] 
    F.append(d)
    L.append(u"de Pauline")
    
    d = [5,1,1970] 
    F.append(d)
    L.append(u"de Jaqueline")

    
    return F, L

def estanniversaire(d):
    """estferie(d): => dit si une date d=[j,m,a] donnée est un anniversaire
       si la date est un anniversaire, renvoie son libellé
       sinon, renvoie "unavailable" afin de masquer le sensor"""
    j,m,a = d
    F,L = listeanniversaires(a)
    for i in range(0, len(F)):
        if j==F[i][0] and m==F[i][1]:
            a=F[i][2]
            years = annee - int(a)
            return L[i], years
    return "unavailable" , ""

annivjour, agejour = estanniversaire([aujourdhui,mois,annee])
annivdemain, agedemain = estanniversaire([demain,mois,annee])

"""The syntax is hass.states.set(entitiy_id, state, {dict of attributes}) """
hass.states.set("sensor.jour_anniversaire" , annivjour ,
  {
    "icon" : "mdi:calendar-star" ,
    "friendly_name" : "Aujourd'hui c'est l'anniversaire ",
    "années" : agejour
  }
)

hass.states.set("sensor.demain_anniversaire" , annivdemain ,
  {
    "icon" : "mdi:calendar-star" ,
    "friendly_name" : "Demain c'est l'anniversaire ",
    "années" : agedemain
  }
)

"""              Calcul des jours fériés                 """

def datepaques(an):
    """Calcule la date de Pâques d'une année donnée an (=nombre entier)"""
    a=an//100
    b=an%100
    c=(3*(a+25))//4
    d=(3*(a+25))%4
    e=(8*(a+11))//25
    f=(5*a+b)%19
    g=(19*f+c-e)%30
    h=(f+11*g)//319
    j=(60*(5-d)+b)//4
    k=(60*(5-d)+b)%4
    m=(2*j-k-g+h)%7
    n=(g-h+m+114)//31
    p=(g-h+m+114)%31
    jour=p+1
    mois=n
    return [jour, mois, an]

""" la fête des grands-mères est fixée au premier dimanche de mars"""
""" calcul du jour de la fête de mères"""
""" la fête des mères est fixée au dernier dimanche de mai sauf si cette date coïncide avec celle de la Pentecôte"""
""" auquel cas elle a lieu le premier dimanche de juin."""
""" la fête des pères est fixée au 3e dimanche de juin."""
""" Pentecôte = Pâques + 49 jours """
""" la fête des grands-pères est fixée au premier dimanche d'octobre"""

def bissextile(annee):
    if (annee % 4) == 0:
        if (annee % 100) == 0:
            if (annee % 400) == 0:
                joursFevrier = 29
            else:
                joursFevrier = 28
        else:
            joursFevrier = 29
    else:
        joursFevrier = 28
    return joursFevrier

def listejoursferies(an):
    """Liste des jours fériés France en date-liste de l'année an (nb entier)."""
    F = []  # =liste des dates des jours feries en date-liste d=[j,m,a]
    L = []  # =liste des libelles du jour ferie
    dp = datepaques(an)
    jdp,mdp,adp = dp

    # Jour de l'an
    d = [1,1,an]
    F.append(d)
    L.append(u"Jour de l'an")

    # # Jour de test
    # d = [3,5,an]
    # F.append(d)
    # L.append(u"Jour de papoo")

    # # Jour de test
    # d = [4,5,an]
    # F.append(d)
    # L.append(u"Jour de papoo1")

    # premier dimanche de mars
    derJourFev = datetime.date(an, 2, bissextile(an)).isocalendar()[2]
    if derJourFev>6:
        derJourFev=0
    #premDimMar = [7-derJourFev,3,an]
    d = [7-derJourFev,3,annee]
    F.append(d)
    L.append(u"Fête des grands-mères")
    
    # Dimanche de Paques
    d = dp
    F.append(d)
    L.append(u"Dimanche de Pâques")

    # Lundi de Paques
    d = [jdp+1,mdp,adp]
    F.append(d)
    L.append(u"Lundi de Pâques")

    # Fête du travail
    d = [1,5,an]
    F.append(d)
    L.append(u"Fête du travail")

    # Victoire des allies 1945
    d = [8,5,an]
    F.append(d)
    L.append(u"Victoire des alliés 1945")

    # Jeudi de l'Ascension
    d = [jdp+9,mdp+1,adp]
    F.append(d)
    L.append(u"Jeudi de l'Ascension")

    # Dimanche de Pentecote
    d = [jdp+19,mdp+1,adp]
    F.append(d)
    L.append(u"Pentecôte")

    # Lundi de Pentecote
    d = [jdp+20,mdp+1,adp]
    F.append(d)
    L.append(u"Lundi de Pentecôte")

    # Fete des mères
    derJourMai = datetime.date(an, 5, 31).isocalendar()[2]
    if derJourMai>6:
        derJourMai=0
    derDimMai = [31-derJourMai,5,an]
    premDimJuin = [7-derJourMai,6,an]
    if derDimMai == [jdp+19,mdp+1,adp]:
        d = premDimJuin
    else:
        d = derDimMai
    F.append(d)
    L.append(u"Fête des mères")

    # Fete des pères
    d = [21-derJourMai,6,an]
    F.append(d)
    L.append(u"Fête des pères")

    # Fete Nationale
    d = [14,7,an]
    F.append(d)
    L.append(u"Fête Nationale")

    # Assomption
    d = [15,8,an]
    F.append(d)
    L.append(u"Assomption")

    # premier dimanche d'octobre
    derJourSep = datetime.date(an, 9, 30).isocalendar()[2]
    if derJourSep>6:
        derJourSep=0
    #premDimOct = [7-derJourSep,3,an]
    d = [7-derJourSep,10,an]
    F.append(d)
    L.append(u"Fête des grands-pères")

    # Toussaint
    d = [1,11,an]
    F.append(d)
    L.append(u"Toussaint")

    # Armistice 1918
    d = [11,11,an]
    F.append(d)
    L.append(u"Armistice 1918")

    # Jour de Noel
    d = [25,12,an]
    F.append(d)
    L.append(u"Jour de Noël")

    return F, L

def estferie(d):
    """estferie(d): => dit si une date d=[j,m,a] donnée est fériée France
       si la date est fériée, renvoie son libellé
       sinon, renvoie "unavailable" afin de masquer le sensor"""
    j,m,a = d
    F,L = listejoursferies(a)
    for i in range(0, len(F)):
        if j==F[i][0] and m==F[i][1] and a==F[i][2]:
            return L[i]
    return "unavailable" 

"""The syntax is hass.states.set(entitiy_id, state, {dict of attributes}) """
hass.states.set("sensor.jour_ferie" , estferie([aujourdhui,mois,annee]) ,
  {
    "icon" : "mdi:creation" ,
    "friendly_name" : "Férié aujourd'hui"
  }
)

hass.states.set("sensor.demain_ferie" , estferie([demain,mois,annee]),
  {
    "icon" : "mdi:creation" ,
    "friendly_name" : "Férié demain"
  }
)

"""  Fête du jour et du lendemain, ne pas supprimer de date  """
fetes = {
    "01:01" : "les Ugolin",
    "02:01" : "les Basile",
    "03:01" : "les Geneviève",
    "04:01" : "les Odilon",
    "05:01" : "les Édouard",
    "06:01" : "les André",
    "07:01" : "les Raymond",
    "08:01" : "les Lucien",
    "09:01" : "les Alix de Ch",
    "10:01" : "les Guillaume",
    "11:01" : "les Paulin d Aquilee",
    "12:01" : "les Tatiana",
    "13:01" : "les Yvette",
    "14:01" : "les Nina",
    "15:01" : "les Rémi",
    "16:01" : "les Marcel",
    "17:01" : "les Roseline",
    "18:01" : "les Prisca",
    "19:01" : "les Marius",
    "20:01" : "les Sébastien",
    "21:01" : "les Agnès",
    "22:01" : "les Vincent",
    "23:01" : "les Barnard",
    "24:01" : "les François",
    "25:01" : "la Conversion de Paul",
    "26:01" : "les Paule",
    "27:01" : "les Angèle",
    "28:01" : "les Thomas",
    "29:01" : "les Gildas",
    "30:01" : "les Martine",
    "31:01" : "les Marcelle",
    "01:02" : "les Ella",
    "02:02" : "les Theophane",
    "03:02" : "les Blaise",
    "04:02" : "les Véronique",
    "05:02" : "les Agathe",
    "06:02" : "les Gaston",
    "07:02" : "les Eugénie",
    "08:02" : "les Jacqueline",
    "09:02" : "les Apolline",
    "10:02" : "les Arnaud",
    "11:02" : "les Severin",
    "12:02" : "les Felix",
    "13:02" : "les Beatrice",
    "14:02" : "les Valentin",
    "15:02" : "les Claude",
    "16:02" : "les Julienne",
    "17:02" : "les Alexis",
    "18:02" : "les Bernadette",
    "19:02" : "les Gabin",
    "20:02" : "les Aimee",
    "21:02" : "les Damien",
    "22:02" : "les Isabelle",
    "23:02" : "les Lazare",
    "24:02" : "les Modeste",
    "25:02" : "les Romeo",
    "26:02" : "les Nestor",
    "27:02" : "les Honorine",
    "28:02" : "les Romain",
    "29:02" : "les Augula",
    "01:03" : "les Aubin",
    "02:03" : "les Charles",
    "03:03" : "les Gwenole",
    "04:03" : "les Casimir",
    "05:03" : "les Olive",
    "06:03" : "les Colette",
    "07:03" : "les Félicité",
    "08:03" : "les Jean",
    "09:03" : "les Françoise",
    "10:03" : "les Vivien",
    "11:03" : "les Rosine",
    "12:03" : "les Justine",
    "13:03" : "les Rodrigue",
    "14:03" : "les Maud",
    "15:03" : "les Louise",
    "16:03" : "les Benedicte",
    "17:03" : "les Patrick",
    "18:03" : "les Cyrille",
    "19:03" : "les Joseph",
    "20:03" : "les Herbert",
    "21:03" : "les Clemence",
    "22:03" : "les Lea",
    "23:03" : "les Victorien",
    "24:03" : "les Catherine",
    "25:03" : "les Humbert",
    "26:03" : "les Larissa",
    "27:03" : "les Habib",
    "28:03" : "les Gontran",
    "29:03" : "les Gwladys",
    "30:03" : "les Amedee",
    "31:03" : "les Benjamin",
    "01:04" : "les Hugues",
    "02:04" : "les Sandrine",
    "03:04" : "les Richard",
    "04:04" : "les Isidore",
    "05:04" : "les Irene",
    "06:04" : "les Marcellin",
    "07:04" : "les Jean-Baptiste",
    "08:04" : "les Julie",
    "09:04" : "les Gautier",
    "10:04" : "les Fulbert",
    "11:04" : "les Stanislas",
    "12:04" : "les Jules 1er",
    "13:04" : "les Ida",
    "14:04" : "les Maxime",
    "15:04" : "les Paterne",
    "16:04" : "les Benoît",
    "17:04" : "les Étienne",
    "18:04" : "les Parfait",
    "19:04" : "les Emma",
    "20:04" : "les Odette",
    "21:04" : "les Anselme",
    "22:04" : "les Alexandre",
    "23:04" : "les Georges",
    "24:04" : "les Fidèle",
    "25:04" : "les Marc",
    "26:04" : "les Alida",
    "27:04" : "les Zita",
    "28:04" : "les Valérie",
    "29:04" : "les Catherine",
    "30:04" : "les Robert",
    "01:05" : "les Joseph",
    "02:05" : "les Boris",
    "03:05" : "les Philippe",
    "04:05" : "les Sylvain",
    "05:05" : "les Judith",
    "06:05" : "les Prudence",
    "07:05" : "les Gisèle",
    "08:05" : "les Desire",
    "09:05" : "les Pacôme",
    "10:05" : "les Solange",
    "11:05" : "les Estelle *",
    "12:05" : "les Achille *",
    "13:05" : "les Rolande *",
    "14:05" : "les Matthias",
    "15:05" : "les Denise",
    "16:05" : "les Honore",
    "17:05" : "les Pascal",
    "18:05" : "les Éric",
    "19:05" : "les Yves",
    "20:05" : "les Bernardin",
    "21:05" : "les Constantin",
    "22:05" : "les Émile",
    "23:05" : "les Didier",
    "24:05" : "les Donatien",
    "25:05" : "les Sophie",
    "26:05" : "les Bérenger",
    "27:05" : "les Augula",
    "28:05" : "les Germain",
    "29:05" : "les Aymard",
    "30:05" : "les Ferdinand",
    "31:05" : "les Perrine",
    "01:06" : "les Justin",
    "02:06" : "les Blandine",
    "03:06" : "les Charles",
    "04:06" : "les Clotilde",
    "05:06" : "les Igor",
    "06:06" : "les Norbert",
    "07:06" : "les Gilbert",
    "08:06" : "les Médard",
    "09:06" : "les Diane",
    "10:06" : "les Landry",
    "11:06" : "les Barnabé",
    "12:06" : "les Guy",
    "13:06" : "les Antoine",
    "14:06" : "les Élisée",
    "15:06" : "les Germaine",
    "16:06" : "les Jean-François",
    "17:06" : "les Hervé",
    "18:06" : "les Leonce",
    "19:06" : "les Romuald",
    "20:06" : "les Silvère",
    "21:06" : "les Rodolphe",
    "22:06" : "les Alban",
    "23:06" : "les Audrey",
    "24:06" : "les Jean-Baptiste",
    "25:06" : "les Prosper",
    "26:06" : "les Anthelme",
    "27:06" : "les Fernand",
    "28:06" : "les Irénée",
    "29:06" : "les Pierre et Paul",
    "30:06" : "les Martial",
    "01:07" : "les Thierry",
    "02:07" : "les Martinien",
    "03:07" : "les Thomas",
    "04:07" : "les Florent",
    "05:07" : "les Antoine",
    "06:07" : "les Mariette",
    "07:07" : "les Raoul",
    "08:07" : "les Thibaud",
    "09:07" : "les Amandine",
    "10:07" : "les Ulric",
    "11:07" : "les Benoit",
    "12:07" : "les Olivier",
    "13:07" : "les Joëlle",
    "14:07" : "les Camille",
    "15:07" : "les Donald",
    "16:07" : "les Elvire",
    "17:07" : "les Charlotte",
    "18:07" : "les Frédéric",
    "19:07" : "les Arsène",
    "20:07" : "les Marina",
    "21:07" : "les Victor",
    "22:07" : "les Marie-Madeleine",
    "23:07" : "les Brigitte",
    "24:07" : "les Christine",
    "25:07" : "les Jacques",
    "26:07" : "les Anne",
    "27:07" : "les Nathalie",
    "28:07" : "les Samson",
    "29:07" : "les Marthe",
    "30:07" : "les Juliette",
    "31:07" : "les Ignace",
    "01:08" : "les Alphonse",
    "02:08" : "les Julien",
    "03:08" : "les Lydie",
    "04:08" : "les Jean-Marie",
    "05:08" : "les Abel",
    "06:08" : "les Octavien",
    "07:08" : "les Gaetan",
    "08:08" : "les Dominique",
    "09:08" : "les Amour",
    "10:08" : "les Laurent",
    "11:08" : "les Claire",
    "12:08" : "les Clarisse",
    "13:08" : "les Hippolyte",
    "14:08" : "les Evrard",
    "15:08" : "les Marie",
    "16:08" : "les Armel",
    "17:08" : "les Hyacinthe",
    "18:08" : "les Hélène",
    "19:08" : "les Eudes",
    "20:08" : "les Bernard",
    "21:08" : "les Christophe",
    "22:08" : "les Fabrice",
    "23:08" : "les Rose",
    "24:08" : "les Barthélemy",
    "25:08" : "les Louis",
    "26:08" : "les Natacha",
    "27:08" : "les Monique",
    "28:08" : "les Augustin",
    "29:08" : "les Sabine",
    "30:08" : "les Fiacre",
    "31:08" : "les Aristide",
    "01:09" : "les Gilles",
    "02:09" : "les Ingrid",
    "03:09" : "les Grégoire",
    "04:09" : "les Rosalie",
    "05:09" : "les Raïssa",
    "06:09" : "les Bertrand",
    "07:09" : "les Reine",
    "08:09" : "les Adrien",
    "09:09" : "les Alain",
    "10:09" : "les Inès",
    "11:09" : "les Adelphe",
    "12:09" : "les Apollinaire",
    "13:09" : "les Aime",
    "14:09" : "les Lubin",
    "15:09" : "les Roland",
    "16:09" : "les Édith",
    "17:09" : "les Renaud",
    "18:09" : "les Nadège",
    "19:09" : "les Émilie",
    "20:09" : "les Davy",
    "21:09" : "les Matthieu",
    "22:09" : "les Maurice",
    "23:09" : "les Constant",
    "24:09" : "les Thecle",
    "25:09" : "les Hermann",
    "26:09" : "les Damien",
    "27:09" : "les Vincent",
    "28:09" : "les Venceslas",
    "29:09" : "les Michel",
    "30:09" : "les Jérôme",
    "01:10" : "les Thérèse",
    "02:10" : "les Léger",
    "03:10" : "les Gérard",
    "04:10" : "les François",
    "05:10" : "les Fleur",
    "06:10" : "les Bruno",
    "07:10" : "les Serge",
    "08:10" : "les Pélagie",
    "09:10" : "les Denis",
    "10:10" : "les Ghislain",
    "11:10" : "les Firmin",
    "12:10" : "les Wilfrid",
    "13:10" : "les Géraud",
    "14:10" : "les Juste",
    "15:10" : "les Thérèse",
    "16:10" : "les Edwige",
    "17:10" : "les Baudouin",
    "18:10" : "les Luc",
    "19:10" : "les René Goupil",
    "20:10" : "les Lina",
    "21:10" : "les Céline",
    "22:10" : "les Elodie",
    "23:10" : "les Jean",
    "24:10" : "les Florentin",
    "25:10" : "les Crépin",
    "26:10" : "les Dimitri",
    "27:10" : "les Émeline",
    "28:10" : "les Simon",
    "29:10" : "les Narcisse",
    "30:10" : "les Bienvenue",
    "31:10" : "les Quentin",
    "01:11" : "les Dagobert",
    "02:11" : "les defunts",
    "03:11" : "les Hubert",
    "04:11" : "les Charles",
    "05:11" : "les Sylvie",
    "06:11" : "les Bertille",
    "07:11" : "les Carine",
    "08:11" : "les Geoffroy",
    "09:11" : "les Theodore",
    "10:11" : "les Leon",
    "11:11" : "les Martin",
    "12:11" : "les Christian",
    "13:11" : "les Brice",
    "14:11" : "les Sidoine",
    "15:11" : "les Albert",
    "16:11" : "les Marguerite",
    "17:11" : "les Élisabeth",
    "18:11" : "les Aude",
    "19:11" : "les Tanguy",
    "20:11" : "les Edmond",
    "21:11" : "les Albert",
    "22:11" : "les Cécile",
    "23:11" : "les Clement",
    "24:11" : "les Flora",
    "25:11" : "les Catherine",
    "26:11" : "les Delphine",
    "27:11" : "les Severin",
    "28:11" : "les Jacques",
    "29:11" : "les Saturnin",
    "30:11" : "les Andre",
    "01:12" : "les Florence",
    "02:12" : "les Viviane",
    "03:12" : "les Xavier",
    "04:12" : "les Barbara",
    "05:12" : "les Gerald",
    "06:12" : "les Nicolas",
    "07:12" : "les Ambroise",
    "08:12" : "les Elfie",
    "09:12" : "les Pierre",
    "10:12" : "les Romaric",
    "11:12" : "les Daniel",
    "12:12" : "les Chantal",
    "13:12" : "les Lucie",
    "14:12" : "les Odile",
    "15:12" : "les Ninon",
    "16:12" : "les Alice",
    "17:12" : "les Gael",
    "18:12" : "les Gatien",
    "19:12" : "les Urbain",
    "20:12" : "les Theophile",
    "21:12" : "les Pierre",
    "22:12" : "les Xaviere",
    "23:12" : "les Armand",
    "24:12" : "les Adele",
    "26:12" : "les Etienne",
    "27:12" : "les Jean",
    "28:12" : "les Innocents",
    "29:12" : "les David",
    "30:12" : "les Roger",
    "31:12" : "les Sylvestre"
        }

"""The syntax is hass.states.set(entitiy_id, state, {dict of attributes}) """
hass.states.set("sensor.saint_du_jour" , fetes[feteaujourdhui] ,
  {
    "icon" : "mdi:church" ,
    "friendly_name" : "Saint du jour"
  }
)

hass.states.set("sensor.saint_de_demain" , fetes[fetedemain] ,
  {
    "icon" : "mdi:church" ,
    "friendly_name" : "Saint de demain"
  }
)
