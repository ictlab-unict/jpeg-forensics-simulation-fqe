import sys
import numpy as np
from PIL import Image
import subprocess
import os
import argparse


def coeff_zigzag_to_column_to_column(coeff):
    #dato un coefficiente in ordine colonna per colonna (tra i primi 33) ne restituisce il corrispondente in ordine zig zag
    map=[]
    map.append(1)
    map.append(3)
    map.append(4)
    map.append(10)
    map.append(11)
    map.append(21)
    map.append(22)
    map.append(36)
    map.append(2)
    map.append(5)
    map.append(9)
    map.append(12)
    map.append(20)
    map.append(23)
    map.append(35)
    map.append(37)
    map.append(6)
    map.append(8)
    map.append(13)
    map.append(19)
    map.append(24)
    map.append(34)
    map.append(38)
    map.append(49)
    map.append(7)
    map.append(14)
    map.append(18)
    map.append(25)
    map.append(33)
    map.append(39)
    map.append(48)
    map.append(50)
    map.append(15)

    return map[coeff]


def coeff_column_to_column_to_zigzag_index(coeff):
    # dato un coefficiente in ordine zig zag (tra i primi 33) ne restituisce il corrispondente in ordine colonna per colonna
    map=[]
    map.append(0)
    map.append(8)
    map.append(1)
    map.append(2)
    map.append(9)
    map.append(16)
    map.append(24)
    map.append(17)
    map.append(10)
    map.append(3)
    map.append(4)
    map.append(11)
    map.append(18)
    map.append(25)
    map.append(32)

    return map[coeff]

def chisquare_distance(multiple,ref):
    # used che distance d(x,y) = sum( (xi-yi)^2 / (xi+yi) )
    all_chi_squared = []
    for element in multiple:
        all_chi_squared.append(np.sum((element - ref[0]) ** 2 / (element + ref[0] + 1e-6)))
    return all_chi_squared

def get_dct_coeffs_distribution(path,width,height):

    #leggo valori DCT dal file (senza aprire l'immagine ed evitando l'errore di truncation)
    p = subprocess.Popen(["./jpeg " + path],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)

    out, info_jpeg = p.communicate()
    executable = os.access('jpeg', os.X_OK)
    if not executable:
        print("Permission denied on jpeg file. jpeg file must be executable to work!")
        sys.exit(0)
    '''
    print(info_jpeg)
    if "Permission denied" in info_jpeg.encode('utf-8'):
        
    '''
    coefficents = np.array(out.splitlines()).astype('int')

    #ottengo larghezza e altezza massima dei blocchi 8X8
    while (width%8) !=0:
        width-=1
    while (height%8) !=0:
        height-=1

    #ottengo le distribuzioni dei 64 coefficienti
    distributions = np.zeros((int(width*height/64), 64))
    n_dist=0

    for i in range(0, len(coefficents), 64):
        if ((i+64) <= (width * height)):
            dist=np.reshape(coefficents[i:i + 64],(8,8))
            dist=np.transpose(dist)
            dist=np.reshape(dist,(1,-1))
            distributions[n_dist]=dist
            n_dist+=1
    return distributions


def get_coefficients_first_compression(img_to_analyze,max_coeff,prints=True):
    # lista dei valori individuabili all'interno della matrice Q1
    # max_coeff rappresenta il numero massimo che possiamo trovare tra i primi 15 coeff(1 DC - 14 AC)
    QF1_range = range(1, max_coeff + 1)

    # legato al QF1_range, rappresenta il coefficenta massimo che vogliamo individuare
    # 33 rappresenta l'indice massimo che stiamo studiando, quindi il 15mo coefficiente
    # perche python scorre per colonna, ed il 15mo coefficiente in zig zag order corrisponde al 32mo scorrendo per colonne
    # (quindi dei 33 coeff calcolati io ne uso solo 15)
    coeff_vec = range(0, 33)

    # range per la generazione degli istogrammi
    _range = np.array(range(0, 1026)) - 0.5

    #carico immagine, estraendo dimensioni e seconda tabella di quantizzazione
    _img = Image.open(img_to_analyze)
    Q2 = _img.quantization
    width, height = _img.size
    img = np.array(_img)
    _img.close()

    # eseguo il crop dell'immagine per spostandomi di 4 pixel per rompere gli schemi dei blocchi 8X8 della quantizzazione JPEG
    imgCrop = img[4:height - 4, 4:width - 4]

    # altezza e larghezza dell'immagine croppata
    cropped_height = height - 8
    cropped_width = width - 8

    # istogrammi (1025 bin) generati da tutte le immagini che sarranno doppiamente quantizzate (simulazione)
    # per ognuno dei coeff possibili (len(QF1_range)), in ognuna delle posizioni (len(coeff_vec))
    h_QF1_all = np.zeros((len(QF1_range), len(_range) - 1, len(coeff_vec)))

    if prints:
        print("START DOUBLE COMPRESSION SIMULATIONS (max_coeff="+str(max_coeff)+")")
    for q1_value,QF1 in enumerate(QF1_range):
        if prints:
            print("SIMULATION q1 : "+str(QF1))
        #q1_value: indice
        #QF1 : valore (pari a q1_value+1)

        #salvo l'immagine con tabella custom uniforme (la tabella contiene tutti i valori uguali [q1_value,q1_value,q1_value,q1_value........])
        table = np.zeros(64).astype('int') + QF1
        tables = {}
        tables[0] = table.tolist()
        im = Image.fromarray(imgCrop)
        im.save('c1.jpg', format='jpeg', qtables=tables)

        #apro l'immagine croppata quantizzata
        img_QF1 = Image.open('c1.jpg')

        #la risalvo con QF2 fissato (lo posso leggere dal file di input)
        img_QF1.save('c2.jpg', format='jpeg', qtables=Q2)

        #riapro la croppata doppiamente quantizzata
        img_QF1_QF2 = Image.open('c2.jpg')

        #estraggo le 64 distribuzioni (una per ogni coeff dalla doppia quantizzazione simulata al variare del coeff q1)
        coeffs_distribution_simulations=get_dct_coeffs_distribution('c2.jpg',cropped_width, cropped_height)

        # elimino le simulazioni
        os.remove('c1.jpg')
        os.remove('c2.jpg')



        #estraggo la seconda tabella di quantizzazione
        qtable = img_QF1_QF2.quantization[0]
        for coeff in coeff_vec:
            #estraggo il coefficiente associato alla tabella
            coeff_column_to_column = coeff_zigzag_to_column_to_column(coeff)
            q2 = qtable[coeff_column_to_column]

            #e lo moltiplico per le distribuzioni (simulando la IDCT ed ottenere i valori dul dominio spaziale senza errore di truncate)
            data_AC = coeffs_distribution_simulations[:, coeff]
            data_AC = data_AC * q2

            #genero istogrammi associati ai coefficenti con valore assoluto
            data_AC = np.absolute(data_AC)
            h_QF1, _ = np.histogram(data_AC, _range)
            h_QF1_all[q1_value, :, coeff] = h_QF1

    if prints:
        print("EXTRACT IMAGE REAL INFO")
    #immagine da analizzare
    img_ref = Image.open(img_to_analyze)
    # estraggo la seconda tabella di quantizzazione
    qtable = img_ref.quantization[0]
    # estraggo le 64 distribuzioni
    coeffs_distribution_real = get_dct_coeffs_distribution(img_to_analyze, width, height)

    if prints:
        print("START COMPARISON")
    D_all = []
    for coeff in coeff_vec:

        # estraggo il coefficiente associato alla tabella di seconda quantizzazione
        coeff_column_to_column = coeff_zigzag_to_column_to_column(coeff)
        q2 = qtable[coeff_column_to_column]

        # e lo moltiplico per le distribuzioni (simulando la IDCT ed ottenere i valori dul dominio spaziale senza errore di truncate)
        data_AC_ref = coeffs_distribution_real[:, coeff]
        data_AC_ref = data_AC_ref * q2

        # genero istogrammi associati ai coefficenti con valore assoluto
        data_AC_ref = np.absolute(data_AC_ref)
        h_ref, _ = np.histogram(data_AC_ref, _range)

        #calcolo la distanza tra tutte le simulazioni e la reale
        D_all_coeff = chisquare_distance(h_QF1_all[:, :, coeff], np.reshape(h_ref, (1, -1)))
        D_all.append(np.reshape(D_all_coeff, (-1)))
    D_all = np.transpose(np.asarray(D_all))

    q1_matrix = []
    #per i primi 15 coeff (la predizione di + coefficienti comporta la modifica di coeff_vec)
    for coeff in range(0, 15):
        #ottengo l'indice in ordinamento zigzag
        zig_zag_coeff = coeff_column_to_column_to_zigzag_index(coeff)
        #estraggo la distribuzione + simile (in termini di distanza minima)
        #e ne prendo la posizione +1 (associazione distribuzione_coefficiente/posizione)
        q1_matrix.append(np.argmin(D_all[:, zig_zag_coeff]) + 1)


    return q1_matrix

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simulate to estimate first compression quantization.')
    parser.add_argument("-i", dest="filename", required=True,
        help="input JPEG file", type=lambda x: is_valid_file(parser, x))
    parser.add_argument("-n", dest="max_coeff", default=19, required=False,
        help="max coefficient expected between first 15 coeffs")
    args = parser.parse_args()

    #immagini compresse con tabelle standard QF1=60 e QF2=90 quindi Q1={}
    img = args.filename
    max_coeff = args.max_coeff

    #restituisce i primi 15 coefficienti
    FQE_15_coeffs=get_coefficients_first_compression(img,max_coeff,True)
    print("PREDICTED q1 (first 15):")
    print(FQE_15_coeffs)