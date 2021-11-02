""" https://pon.fr/home-assistant-infos-du-jour-et-du-lendemain/ """
""" https://github.com/papo-o/home-assistant-config/blob/master/python_scripts/jours_feries_uniquement.py """


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
"""     service: python_script.jours_feries_uniquement                     """
"""     data:                                                              """
"""       name: "jours_feries"                                             """


"""               This will create two for publics hollidays,              """
"""        mother and father days, grandmother and grandfather days        """
"""               One for today and the other for tomorrow                 """

"""       example to display sensors with the auto-entities card           """

"""    - type: custom:auto-entities                                        """
"""      card:                                                             """
"""        type: entities                                                  """
"""        title: "Infos du jour"                                          """
"""        show_header_toggle: false                                       """
"""      filter:                                                           """
"""        include:                                                        """
"""          - entity_id: /_ferie/                                         """
"""        exclude:                                                        """
"""          - state: "unavailable"                                        """

today = datetime.datetime.now().date()
aujourdhui = today.day
demain = int(aujourdhui) + 1
mois = today.month
annee = today.year
day = '{:02d}'.format(today.day)

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
    # d = [2,11,an]
    # F.append(d)
    # L.append(u"Jour de papoo")

    # # Jour de test
    # d = [3,11,an]
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

"""The syntax is hass.states.set(entity_id, state, {dict of attributes}) """
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
