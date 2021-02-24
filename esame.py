#classe per le eccezioni
class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    #funzione costruttore istanziata sul nome
    def __init__(self, name):
        #setto il nome del file
        self.name = name

    #uso il metodo get_data per tornare i dati del file
    def get_data(self):  

        #creo una lista dove salvare gli elementi
        time_series = []

        #apro il file con il nome scelto dall'utente 
        try:
            my_file = open(self.name, 'r')
        except:
            raise Exception('Errore nella lettura del file')
            #esco dalla funzione tornando "niente"
            return None

        #per ogni riga del mio file 
        for line in my_file:
            #separo gli elementi dalla virgola
            elements = line.split(',')
            #se non sto processando l'intestazione
            if elements[0] != 'epoch': 
                #setto il timestamp e il valore della temperatura      
                timestamp  = elements[0]
                temperature = elements[1]
                #li converto da stringa a numero, int e float rispettivamente e provo a inserire le eccezioni
                try:
                    timestamp = int(timestamp)
                #se non è possibile 
                except:#non alzo le eccezioni perché tutto deve procedere comunque senza alzare eccezioni
                    continue
                try:
                    temperature = float(temperature)
                except:#tutto deve procedere comunque senza alzare eccezioni
                    continue
                try:
                     temperature <= 0
                except:#tutto deve procedere comunque senza alzare eccezioni
                    continue

                #salvo gli elementi in una variabile che andrò ad appendere nella lista values
                values = [timestamp,temperature]
                time_series.append(values)
        #chiudo il file        
        my_file.close()
        #faccio l'iterazione sul range dal primo elemento della lista time_series 
        for i in range(1, len(time_series)):
            #controllo se i timestamps non sono ordinati
            if time_series[i][0]<time_series[i-1][0]:
                #alzo l'eccezione
                raise Exception("Timestamp fuori ordine")
            #e se ci sono doppioni 
            elif time_series[i][0]==time_series[i-1][0]:
                #alzo l'eccezione
                raise Exception("Timestamp già presente")
        #faccio ritornare la lista di valori [timesstamp,temperature ] (senza intestazione)
        return time_series

def hourly_trend_changes(time_series):

    n_trend=[]
    ore=[]
    temperature=[]
    for i in range(len(time_series)):
        #quando sono all'ultimo elemento della lista
        if i==len(time_series)-1:
            ore.append([int(time_series[i][0]/3600),time_series[i][1]])
            ore.append([-1,-1])
        #converto gli epochs, nel senso che vedo se appartengono alla stessa ora
        ore.append([int(time_series[i][0]/3600),time_series[i][1]])
    #inizializzo una variabile vuota per mettere i trend precedenti
    prec = None
    #ciclo su tutta "ore"
    for i in range(len(ore)):

        #quando sono al primo elemento della lista
        if i==0:
            #agiungo la temperatura 
            temperature.append(ore[i][1])
        
        #dal secondo elemento in poi della lista
        if i > 0 :
            if ore[i][0]==ore[i-1][0]:
                #appendo la temperatura che corrisponde all'epoch in posizione i alla lista temperature
                temperature.append(ore[i][1])
            
            #se l'epoch è diverso dal suo precedente e dall'ultimo elemento di 'ore'
            if ore[i][0] != ore[i-1][0] and ore[i][0]!=-1:
                #setto il contatore_trend a zero
                contatore_trend=0

                #itero sule temperature/ora
                for x in range(len(temperature)):
                    #quando sono al primo elemento
                    if x==0:
                        #vado avanti
                        continue

                    #quando sono al secondo elemento
                    if x==1:
                        if temperature[x]==temperature[x-1]:
                            continue
                        elif temperature[x]>temperature[x-1]:
                            variazione=True #variazione positiva
                        else:
                             variazione=False #variazione negativa
                        #se prec non è vuoto e non ha variazione
                        if prec != None and prec != variazione:
                            contatore_trend +=1
                            #ora la variazione si sostituisce a prec
                            prec=variazione

                    #dal terzo elemento in poi
                    if x>1:
                        if temperature[x]==temperature[x-1]:
                            adesso=variazione #variazione(prec)=variazione di adesso
                        elif temperature[x]>temperature[x-1]:
                            adesso=True #variazione di adesso positiva
                        else:
                            adesso=False #altrimenti negativa
                        #se variazione prec è diverso da variazione di adesso    
                        if variazione!=adesso:
                            variazione=adesso #li metto uguali e aumento di una inversione
                            contatore_trend += 1
                        #la variazione si sostituisce a prec
                        prec=variazione
                #appendo le inversioni
                n_trend.append(contatore_trend)
                temperature.clear()
                temperature.append(ore[i-1][1]) #addo le temperature dell'ora precedente
                temperature.append(ore[i][1]) #e la prima della  successiva
    #faccio ritornare la lista col numero di inversioni                    
    return n_trend

time_series_file = CSVTimeSeriesFile(name='data1.csv')
time_series = time_series_file.get_data()
print(hourly_trend_changes(time_series))