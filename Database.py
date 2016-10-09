from SingleRule import SingleRule
from scipy.interpolate import interp1d
  
from Building import SicherheitsCategory as schutz
from Building import BaustoffCategory as bau

class Default(SingleRule):
    def fun(self, building):
        SingleRule.reportAnnotation(self, "Industriebaurichtlinie - IndBauR NRW - RdErl. d. Ministeriums für Bauen, Wohnen, Stadtentwicklung und Verkehr – VI.1 - 190 v. 4.2.2015"
        )
    def __init__(self):
        super().__init__(
                ruleName = "Richtlinie",
                paragraphNumber = 00,
                title = "Titel",
                text="Stand der Richtlinie"
                )
        SingleRule.registerTest(self, self.fun)

#Löschwasser
class LoeWa(SingleRule):
    def aLoeWaFunction(self, building):
        liters = None
        hours = "für 2 Stunden"
        SingleRule.reportAnnotation(self, "§ 3, 17 BauO NRW"
        )
        SingleRule.reportAnnotation(self, "Alternativ DVGW Arbeitsbaltt W 405"
        )
        SingleRule.reportAnnotation(self, "Umkreis für LoeWa maximal 300 m"
        )
        SingleRule.reportAnnotation(self, "Geschäftsstraßen und Industriegebiete: 100 m; Geschlossene Wohngebiete: 120 m; Offene Wohngebiete: 140 m"
        )
        SingleRule.reportAnnotation(self, "Ausführung... Löschwasserteiche (DIN 14210); Unterirdische Löschwasserbehälter (DIN 14230; Unterflurhydranten (DIN EN 14339 ehemals DIN 3221); Überflurhydranten (DIN EN 14384 ehemals DIN 3222)"
        )
        if building.sicherheits == schutz.K4:
            liters = 96
            hours = "für nur 1 Stunde"
        elif building.squaremeters < 2500:
            liters = 96
        elif building.squaremeters > 4000:
            liters = 192
        else:
            qm = [2500, 4000]
            lw = [96, 192]
            f = interp1d(qm, lw)
            liters = f(building.squaremeters).item(0)

        SingleRule.reportInformation(self, '{}m³/h {}'.format(liters, hours))

    # calling init...
    def __init__(self):
        super().__init__(
                ruleName = "LoeWa",
                paragraphNumber = 5.1,
                title = "Löschwasserbedarf",
                text="Für Industriebauten ist der Löschwasserbedarf im Benehmen mit der Brandschutzdienststelle unter Berücksichtigung der Flächen der Brandabschnitte oder Brandbekämpfungsabschnitte sowie der Brandlasten festzulegen. Hierbei ist auszugehen von einem Löschwasserbedarf über einen Zeitraum von zwei Stunden von mindestens 96 m³/h bei Abschnittsflächen bis zu 2 500 m² und von mindestens 192 m³/h bei Abschnittsflächen von mehr als 4 000 m².Zwischenwerte können linear interpoliert werden. Bei Industriebauten mit selbsttätiger Feuerlöschanlage genügt eine Löschwassermenge für Löscharbeiten der Feuerwehr von mindestens 96 m³/h über einen Zeitraum von einer Stunde."
                )
        SingleRule.registerTest(self, self.aLoeWaFunction)

#Zugänglichkeit 5.2
class ZuGa(SingleRule):
    def aZuGaFunction(self, building):
        SingleRule.reportAnnotation(self, "§ 5 BauO NRW"
        )
        SingleRule.reportAnnotation(self, "Bewegungsflächen müssen eine Achslast  bis  zu  10  t  und  einem  zulässigen  Gesamtgewicht  bis  zu  16  t  befahren werden können."
        )
        SingleRule.reportAnnotation(self, "Aufstellflächen wenn Aufentahltsräume OKFF > 7 m; Anfoderungen gesondert Prüfen"
        )         
        SingleRule.reportAnnotation(self, "Ausführung... DIN 14090; örtliche Hinweise der Feuerwehr"
        )               
        if building.sicherheits == schutz.K4:
            SingleRule.reportInformation(self, 'Brandabschnitte müssen nicht unbedingt an Außenwänden liegen.'
                )
        elif building.sicherheits != schutz.K4:
            SingleRule.reportInformation(self, 'Jeder Brandabschnitt und jeder Brandbekämpfungsabschnitt muss mit mindestens einer Seite an einer Außenwand liegen und von dort für die Feuerwehr zugänglich sein.'
                )

    def bZuGaFunction(self, building):
        solution1 = ""
        solution2 = ""
        solution3 = ""
        if building.squaremeters >= 5000:
            solution1 = "erfoderlich"
            solution3 = "Auf diese ist dauerhaft und leicht erkennbar hinzuweisen."
        elif building.squaremeters < 5000:
            solution2 = "nicht erfoderlich"

        SingleRule.reportInformation(self, 'Eine Feuerwehrumfaht ist {}{}. {}'.format(solution1, solution2, solution3 ))
          
    # calling init...
    def __init__(self):
        super().__init__(
                ruleName = "ZuGa",
                paragraphNumber = 5.2,
                title = "Lage und Zugänglichkeit",
                text="Jeder Brandabschnitt und jeder Brandbekämpfungsabschnitt muss mit mindestens einer Seite an einer Außenwand liegen und von dort für die Feuerwehr zugänglich sein. Dies gilt nicht für Brandabschnitte und Brandbekämpfungsabschnitte, die eine selbsttätige Feuerlöschanlage haben. Freistehende sowie aneinandergebaute Industriebauten mit einer Grundfläche von insgesamt mehr als 5 000 m² müssen eine für Feuerwehrfahrzeuge befahrbare Umfahrt haben. Umfahrten müssen die Anforderungen der Muster-Richtlinie über Flächen für die Feuerwehr erfüllen. Über die nach § 5 Landesbauordnung für die Feuerwehr erforderlichen Zufahrten, Durchfahrten und Aufstell- und Bewegungsflächen hinaus, sind auch die Umfahrten nach Abschnitt 5.2.2 ständig freizuhalten. Hierauf ist dauerhaft und leicht erkennbar hinzuweisen (Kennzeichnung."
                )
        SingleRule.registerTest(self, self.aZuGaFunction)
        SingleRule.registerTest(self, self.bZuGaFunction)

#Hinweis 2.OG
class ZweiGe(SingleRule):    
    def aZweiGeFunction(self, building):
        SingleRule.reportAnnotation(self, "§ 5 BauO NRW"
        )    
        SingleRule.reportAnnotation(self, "Ausführung... DIN 14090"
        )          
        if building.topfloors < 2:
            return
        elif building.topfloors >= 2:
            SingleRule.reportAnnotation(self, "Für weitere Erleichterung weitere Maßnahmen prüfen.")

    # calling init...
    def __init__(self):
        super().__init__(
                ruleName = "ZweiGe",
                paragraphNumber = 5.3,
                title = "Zweigeschossige Industriebauten mit Zufahrten",
                text='Wird bei einem zweigeschossigen Industriebau das untere Geschoss mit Bauteilen einschließlich der Decken feuerbeständig und aus nichtbrennbaren Baustoffen hergestellt und werden für beide Geschosse Zufahrten für die Feuerwehr angeordnet, dann kann das obere Geschoss wie ein erdgeschossiger Industriebau behandelt werden.'
                )
        SingleRule.registerTest(self, self.aZweiGeFunction)

#Geschosse und Ebenen unter der Geländeoberfläche 
class UnterGe(SingleRule):    
    def aUnterGeFunction(self, building):
        SingleRule.reportAnnotation(self, "§ 3, 17 BauO NRW"
        )            
        if building.subfloors == 0:
                return
        elif building.subfloors > 0 and building.squaremeters > 1000 and building.sicherheits != schutz.K4:
                SingleRule.reportIllegal(self,
                "illegal weil größer 1000 m² und Kellergeschoss. Richtlinie pruefen."
                )                
                
        elif building.subfloors > 0 and building.squaremeters > 1000 and building.sicherheits == schutz.K4:
                SingleRule.reportIllegal(self,
                "Illegal weil größer 1000 m² und Kellergeschoss. Der Flächenwert von 1000 m² um das Dreieinhalbfache erhöht werden (3500 m²). Richtlinie pruefen."
                )                
                
    # calling init...
    def __init__(self):
        super().__init__(
                ruleName = "UnterGe",
                paragraphNumber = 5.4,
                title = "Geschosse und Ebenen unter der Geländeoberfläche",
                text='Geschosse von Brandabschnitten, deren Fußböden ganz oder teilweise mehr als 1 m unter der Geländeoberfläche liegen, sind durch raumabschließende, feuerbeständige Wände aus nichtbrennbaren Baustoffen in Abschnitte zu unterteilen, deren Grundfläche im ersten Unter­geschoss nicht größer als 1 000 m² und in jedem tiefer gelegenen Geschoss nicht größer als 500 m² sein darf. Tragende und aussteifende Wände und Stützen sowie Decken müssen feuerbeständig sein. Die Grundflächen von Brandbekämpfungsabschnitten, deren Fußböden ganz oder teilweise mehr als 1 m unter der Geländeoberfläche liegen, dürfen nicht größer als 1 000 m² im ersten unterirdischen Geschoss oder in der ersten unterirdischen Ebene und 500 m² in jedem tiefer gelegenen Geschoss oder Ebene sein. Die vorgenannten Anforderungen gelten nicht für Geschosse und Ebenen, wenn sie mindestens an einer Seite auf ganzer Länge für die Feuerwehr von außen ohne Hilfsmittel zugänglich sind."'
                )
        SingleRule.registerTest(self, self.aUnterGeFunction)

#Rettungswege
class RettWeg(SingleRule):
    def aRettWegFunction(self, building):

        SingleRule.reportAnnotation(self, "§ 3, 17, 36, 37 BauO NRW"
        )        
        SingleRule.reportAnnotation(self, "Alles > 35 m Erleichterung formalrechtlich beantragen"
        )  
        SingleRule.reportAnnotation(self, 'Hauptgänge berücksichtigen.')
        SingleRule.reportAnnotation(self, 'Liegt ein Ausgang ins Freie unter einem Vordach, beginnt das Freie erst am Rande des Vordachs. Unter mindestens zweiseitig offenen Vordächern ist eine zusätzliche Entfernung in der Tiefe des Vordachs, jedoch maximal 15 m, zulässig. Dies gilt nicht, wenn der Bereich unter dem Vordach einen eigenen Brandabschnitt oder Brandbekämpfungsabschnitt bildet.'
        )
        if building.squaremeters >= 1600:
           SingleRule.reportInformation(self, 'Zwei möglichst entgegengesetzt liegende bauliche Rettungswege bilden.')
        elif building.squaremeters >= 200 : 
           SingleRule.reportAnnotation(self, 'Bei Ebenen oder Einbauten ab mehr als 200 m² sind zwei Retungswege auszubilden.') 
           SingleRule.reportAnnotation(self, 'Jeder Raum mit einer Grundfläche von mehr als 200 m² muss mindestens zwei Ausgänge haben.') 

    def bRettWegFunction(self, building):
        solution4 = None
        if building.sicherheits != schutz.K1:
            return
        elif building.height <= 5:
            solution4 = 35
        elif building.height >= 10:
            solution4 = 50
        else:
            hi = [5, 10]
            la = [35, 50]
            f = interp1d(hi, la)
            solution4 = f(building.height).item(0)

        SingleRule.reportInformation(self, 'Rettungsweg {} m'.format(solution4, ))

    def cRettWegFunction(self, building):
        solution5 = None
        if building.sicherheits != schutz.K2:
            return
        elif building.height <= 5:
            solution5 = 50
        elif building.height >= 10:
            solution5 = 70
        else:
            hi = [5, 10]
            la = [50, 70]
            f = interp1d(hi, la)
            solution5 = f(building.height).item(0)

        SingleRule.reportInformation(self, 'Rettungsweg {} m. Besondere Anforderungen an die Alarmierung prüfen.'.format(solution5, ))

    # calling init...
    def __init__(self):
        super().__init__(
                ruleName = "RettWeg",
                paragraphNumber = 5.6,
                title = "Rettungswege",
                text="Zu den Rettungswegen in Industriebauten gehören insbesondere die Hauptgänge in den Produktions- und Lagerräumen, die Ausgänge aus diesen Räumen, die notwendigen Flure, die notwendigen Treppen und die Ausgänge ins Freie.Für Industriebauten mit einer Grundfläche von mehr als 1 600 m² müssen in jedem Geschoss mindestens zwei möglichst entgegengesetzt liegende bauliche Rettungswege vorhanden sein. Dies gilt für Ebenen oder Einbauten mit einer Grundfläche von jeweils mehr als 200 m² entsprechend. Jeder Raum mit einer Grundfläche von mehr als 200 m² muss mindestens zwei Ausgänge haben.Einer der Rettungswege nach Abschnitt 5.6.2 Satz 1 darf zu anderen Brandabschnitten oder zu anderen Brandbekämpfungsabschnitten oder über eine Außentreppe, über offene Gänge und/oder über begehbare Dächer auf das Grundstück führen, wenn diese im Brandfall ausreichend lang standsicher sind und die Benutzer durch Feuer und Rauch nicht gefährdet werden können. Bei Ebenen darf der zweite Rettungsweg auch über eine notwendige Treppe ohne notwendigen Treppenraum in eine unmittelbar darunterliegende Ebene oder ein unmittelbar darunterliegendes Geschoss führen, sofern diese Ebene oder dieses Geschoss Ausgänge in mindestens zwei sichere Bereiche hat. Die Rettungswege aus im Produktions- oder Lagerraum eingestellten Räumen, dürfen über den gleichen Produktions- oder Lagerraum führen. In diesem Fall sind die Räume oder Raumgruppen mit Aufenthaltsräumen offen auszuführen. Alternativ können sie durch Wände mit ausreichender Sichtverbindung abgetrennt werden. Bei geschlossenen Räumen mit mehr als 20 m² Grundfläche ist zusätzlich sicherzustellen, dass die dort anwesenden Personen im Brandfall rechtzeitig in geeigneter Weise gewarnt werden. Von jeder Stelle eines Produktions- oder Lagerraumes soll mindestens ein Hauptgang nach höchstens 15 m Lauflänge erreichbar sein. Hauptgänge müssen mindestens 2 m breit sein. Sie sollen geradlinig auf kurzem Wege zu Ausgängen ins Freie, zu notwendigen Treppenräumen, zu Außentreppen, zu Treppen von Ebenen und Einbauten, zu offenen Gängen, über begehbare Dächer auf das Grundstück, zu anderen Brandabschnitten oder zu anderen Brandbekämpfungsabschnitten führen. Diese anderen Brandabschnitte oder Brandbekämpfungsabschnitte müssen Ausgänge unmittelbar ins Freie oder zu notwendigen Treppenräumen mit einem sicheren Ausgang ins Freie haben. Von jeder Stelle eines Produktions- oder Lagerraumes muss mindestens ein Ausgang ins Freie, ein Zugang zu einem notwendigen Treppenraum, zu einer Außentreppe, zu einem offenen Gang oder zu einem begehbaren Dach, ein anderer Brandabschnitt oder ein anderer Brandbekämpfungsabschnitt bei einer mittleren lichten Höhe von bis zu 5 m in höchstens 35 m Entfernung oder bei einer mittleren lichten Höhe von mindestens 10 m in höchstens 50 m Entfernung erreichbar sein. Bei Vorhandensein einer Alarmierungseinrichtung für die Nutzer (Internalarm)  ist es zulässig, dass der Ausgang nach bei einer mittleren lichten Höhe von bis zu 5 m in höchstens 50 m Entfernung oder bei einer mittleren lichten Höhe von mindestens 10 m in höchstens 70 m Entfernung erreicht wird. Bei mittleren lichten Höhen zwischen 5 m und 10 m darf zur Ermittlung der zulässigen Entfernung zwischen den vorstehenden Werten interpoliert werden. Die Auslösung von Alarmierungseinrichtungen muss erfolgen bei Auslösen einer selbsttätigen Brandmeldeanlage oder einer selbsttätigen Feuerlöschanlage. Bei der selbsttätigen Feuerlöschanlage ist zusätzlich eine Handauslösung der Alarmierungseinrichtungen vorzusehen. Liegt ein Ausgang ins Freie unter einem Vordach, beginnt das Freie erst am Rande des Vordachs. Unter mindestens zweiseitig offenen Vordächern ist eine zusätzliche Entfernung in der Tiefe des Vordachs, jedoch maximal 15 m, zulässig. Dies gilt nicht, wenn der Bereich unter dem Vordach einen eigenen Brandabschnitt oder Brandbekämpfungsabschnitt bildet. Kontroll- und Wartungsgänge, die nur gelegentlich begangen werden und aus nicht brennbaren Baustoffen bestehen, dürfen über Steigleitern erschlossen werden. Die Steigleiter muss in einer Entfernung von maximal 100 m, bei nur einer Fluchtrichtung in maximal 50 m, erreicht werden können. Die mittlere lichte Höhe einer Ebene ergibt sich als nach Flächenanteilen gewichtetes Mittel der lichten Höhe bis zur nächsten Decke oder dem Dach. Bei der Ermittlung der mittleren lichten Höhe bleiben Einbauten sowie Ebenen mit einer maximalen Grundfläche nach Tabelle 1 unberücksichtigt. Für Einbauten sowie Ebenen mit einer maximalen Grundfläche nach Tabelle 1, ist die mittlere lichte Höhe die der Ebene oder des Geschosses, über deren/dessen Fußboden sie angeordnet sind.Die Entfernung der lichten Höhe wird in der Luftlinie, jedoch nicht durch Bauteile gemessen. Die tatsächliche Lauflänge darf jedoch nicht mehr als das 1,5-fache der jeweiligen Entfernung betragen. Liegt eine Stelle des Produktions- oder Lagerraumes nicht auf der Höhe des Ausgangs oder Zugangs, so ist von der zulässigen Lauflänge das Doppelte der Höhendifferenz abzuziehen. Bei der Ermittlung der Entfernung bleibt diese Höhendifferenz unberücksichtigt.Bei Einbauten und Ebenen mit einer maximalen Grundfläche nach Tabelle 1 dürfen die Rettungswege über notwendige Treppen ohne notwendigen Treppenraum geführt werden, wenn sie in eine unmittelbar darunterliegende Ebene oder ein unmittelbar darunterliegendes Geschoss führen, sofern diese Ebene oder dieses Geschoss Ausgänge in mindestens zwei sichere Bereiche hat und ein Ausgang in Entfernung erreicht wird. Die Lauflänge auf dem Einbau oder der Ebene bis zu einer Treppe darf in diesen Fällen höchstens bei Brandbelastung in Brandbekämpfungsabschnitten < 15 kWh/m² 50 m, bei Vorhandensein einer Alarmierungseinrichtung für die Nutzer, deren Auslösung über eine selbsttätige Brandmeldeanlage oder eine selbsttätige Feuerlöschanlage mit zusätzlicher Handauslösung der Alarmierungseinrichtung, 35 m oder im Übrigen 25 m betragen. Notwendige Treppen müssen aus nichtbrennbaren Baustoffen bestehen. Wände notwendiger Treppenräume müssen raumabschließend sein und in der Bauart von Brandwänden hergestellt werden. Die Anforderungen des § 37 Absatz 4 Satz 2 Landesbauordnung an innenliegende notwendige Treppenräume sind erfüllt, wenn diese Treppenräume an der obersten Stelle eine Öffnung zur Rauchableitung haben. In Gebäuden, bei denen die Fußbodenoberkante des höchstgelegenen Geschosses oder der höchstgelegenen Ebene, in dem oder in der ein Aufenthaltsraum möglich ist, mehr als 13 m über der Geländeoberfläche im Mittel liegt, sind besondere Vorkehrungen zu treffen, soweit dies zur Erfüllung der Anforderungen des § 37 Absatz 4 Satz 2 Landesbauordnung erforderlich ist. Öffnungen zur Rauchableitung nach Satz 1 müssen in jedem Treppenraum einen freien Querschnitt von mindestens 1 m² und Vorrichtungen zum Öffnen ihrer Abschlüsse haben, die vom Erdgeschoss sowie vom obersten Treppenabsatz aus bedient werden können. Innenliegende notwendige Treppenräume müssen in Gebäuden, bei denen die Fußbodenoberkante des höchstgelegenen Geschosses oder der höchstgelegenen Ebene, in dem oder in der ein Aufenthaltsraum möglich ist, mehr als 13 m über der Geländeoberfläche im Mittel liegt, eine Sicherheitsbeleuchtung haben."
                )
        SingleRule.registerTest(self, self.aRettWegFunction)
        SingleRule.registerTest(self, self.bRettWegFunction)
        SingleRule.registerTest(self, self.cRettWegFunction)

class CheckBrandabschnittsflaeche(SingleRule):
    def anmerkungEins(self, building):
        if building.topfloors != 1:
            return
        if building.squaremeters <= 4500 and building.sicherheits == schutz.K1:
            SingleRule.reportAnnotation(self,
                    "falls breite groeßer 40m und wärmeabzug kleiner 5%: illegal")
    def anmerkungVier(self, building):
        if building.topfloors != 1:
            return
        if building.sicherheits != schutz.K2:
            return
        if building.squaremeters >= 2700 or building.squaremeters >= 4500:
            SingleRule.reportAnnotation(self,
                    "brandabschnittsfläche von 2700 m² darf um 10% überschritten werden")

    # zif. 6.2 Spalte1 Tab. 2
    def maxSquareMeters(self, building):

        # structure: [geschosszahl][baustoff][maxAllowedSquareMeters]
        maxAllowedSquaremeters = {
            1 : {
                bau.F0A : {
                    schutz.K1 : 1800,
                    schutz.K2 : 2700,
                    schutz.K31 : 3200,
                    schutz.K32 : 3600,
                    schutz.K33 : 4200,
                    schutz.K34 : 4500,
                    schutz.K4 : 10000
                    },
                bau.F30A : {
                    schutz.K1 : 3000,
                    schutz.K2 : 4500,
                    schutz.K31 : 5400,
                    schutz.K32 : 6000,
                    schutz.K33 : 7000,
                    schutz.K34 : 7500,
                    schutz.K4 : 10000
                }
            },
            # zweigeschossig:
            2 : {
                bau.F30A : {
                    schutz.K1 : 800,
                    schutz.K2 : 1200,
                    schutz.K31 : 1400,
                    schutz.K32 : 1600,
                    schutz.K33 : 1800,
                    schutz.K34 : 2000,
                    schutz.K4 : 8500
                },
                bau.F60A : {
                    schutz.K1 : 1600,
                    schutz.K2 : 2400,
                    schutz.K31 : 2900,
                    schutz.K32 : 3200,
                    schutz.K33 : 3600,
                    schutz.K34 : 4000,
                    schutz.K4 : 8500
                },
                bau.F90A : {
                    schutz.K1 : 2400,
                    schutz.K2 : 3600,
                    schutz.K31 : 4300,
                    schutz.K32 : 4800,
                    schutz.K33 : 5500,
                    schutz.K34 : 6000,
                    schutz.K4 : 6500
                }
            },
            # dreigeschossig:
            3 : {
                bau.F60A : {
                    schutz.K1 : 1200,
                    schutz.K2 : 1800,
                    schutz.K31 : 2100,
                    schutz.K32 : 2400,
                    schutz.K33 : 2800,
                    schutz.K34 : 3000,
                    schutz.K4 : 6500
                },
                bau.F90A : {
                    schutz.K1 : 1800,
                    schutz.K2 : 2700,
                    schutz.K31 : 3200,
                    schutz.K32 : 3600,
                    schutz.K33 : 4100,
                    schutz.K34 : 4500,
                    schutz.K4 : 6500
                }
            },
            # viergeschossig:
            4 : {
                bau.F90A : {
                    schutz.K1 : 1500,
                    schutz.K2 : 2300,
                    schutz.K31 : 2700,
                    schutz.K32 : 3000,
                    schutz.K33 : 3500,
                    schutz.K34 : 3800,
                    schutz.K4 : 5000
                }
                    },
            # fünfgeschossig:
            5 : {
                bau.F90A : {
                    schutz.K1 : 1300,
                    schutz.K2 : 1800,
                    schutz.K31 : 2200,
                    schutz.K32 : 2400,
                    schutz.K33 : 2800,
                    schutz.K34 : 3000,
                    schutz.K4 : 4000
                }
            }
        }

        try:
            allowedMeters = maxAllowedSquaremeters[building.topfloors]\
                                                  [building.baustoff]\
                                                  [building.sicherheits]
        except KeyError:
            SingleRule.reportIllegal(self,"illegal weil ausserhalb der tabelle, ziffer6/7 prüfen")
            return

        if building.squaremeters > allowedMeters:
            SingleRule.reportIllegal(self,
                "illegal weil größer {} m² bei {} und {} Etagen".
                    format(allowedMeters,
                           building.sicherheits,
                           building.topfloors))


    def __init__(self):
        super().__init__(
                ruleName = "Brandabschnittsfläche",
                paragraphNumber = 6.2,
                title = "",
                text="Tabelle 2..."
                )
        SingleRule.registerTest(self, self.maxSquareMeters)
        SingleRule.registerTest(self, self.anmerkungEins)
        SingleRule.registerTest(self, self.anmerkungVier)


