# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 10:52:21 2023

@author: Iza
"""
import tkinter as tk
from tkinter import filedialog

OFU = ['B','Ba','Bi','Bp','Bz','K','dr','Tk','Ti','Tp','Wm','Wp','Ws','Tr','Ls','Lz','N']
OFU1 = ['S','Br','Wsr','W','Lzr']
OZU = ['Ł','Ps','Ls','Lz','R']
OZK = ['I','II','III','IV','V','VI']
OZK1 = ['I','II','IIIa','IIIb','IVa','IVb','V','VI','VIz']

file1='kontrolny plik.txt'
file = file1.encode('utf-8').decode('cp1250')

def sprawdz():
    file_path = filedialog.askopenfilename()  # Wybierz plik do wczytania
    with open(file_path, 'r') as file:
        data = file.readlines()

    def podziel(name):
        p = []
        if '-' not in name:
            p.append(name)
        else:
            parts = name.split("-")
            for part in parts:
                p.append(part)
        return p

    def pomin(input_string, letters_to_skip):
        for letter in letters_to_skip:
            if input_string.startswith(letter):
                input_string = input_string[len(letter):]
        return input_string
    def warunek1(name):
        if name.startswith('R'):
            name = pomin(name,'R')
            for letter in OZK1:
                if letter == name:
                    return True
        elif name.startswith(('Ł', 'Ps', 'Ls', 'Lz')):
            name = pomin(name,('Ł', 'Ps', 'Ls', 'Lz'))
            for letter in OZK:
                if letter == name:
                    return True
        else: return False
    def warunek2(name1, name2):
        for l in OFU1:
            if l in name1:
                if name2.startswith('R'):
                    name2 = pomin(name2,'R')
                    for letter in OZK1:
                        if letter == name2:
                            return True
                elif name2.startswith(('Ł', 'Ps')):
                    name2 = pomin(name2,('Ł', 'Ps'))
                    for letter in OZK:
                        if letter == name2:
                            return True
                elif name1 == 'W' and name2.startswith(('Ls', 'Lz')):
                    name2 = pomin(name2,('Ls', 'Lz'))
                    for letter in OZK:
                        if letter == name2:
                            return True
            else: return False

    dzialki=[]
    bledne=[]
    prawidlowe=[]

    for line in data:
        newLine=line.strip()
        if 3<len(newLine)<20:
            dzialki.append(newLine)
    print(dzialki)

    for i in dzialki:
        if i.count('/') != 1:
            bledne.append("{0}  -  Zła składnia nazwy: nieprawidłowa ilość ukośników w nazwie.".format(i))
            print("Zła ilość ukośników w nazwie: ",i)
            # pass
        elif ' ' in i:
            bledne.append("{0}  -  Zła składnia nazwy: brak myślnika, odstęp między znakami.".format(i))
            print("Brak myślnika, odstęp między znakami: ", i)
            pass
        else:
            part0 = i.split('/')[0]
            part = i.split('/')[1]
            for znak in part0:
                if not (znak.isnumeric() or znak == '-'):
                    bledne.append("{0}  -  Zły zapis numeru punktu.".format(i))
                    print("Zły zapis numeru punktu: ", i)
            else:
                name = podziel(part)
                # print(name)
                if len(name) == 1:
                    if name[0] in OFU or warunek1(name[0]):
                        prawidlowe.append(i)
                    elif name[0] == 'E':
                        bledne.append("{0}  -  Nieprawidłowe oznaczenie OFU, użytek ekologiczny nie jest aktualny.".format(i))
                        print("Użytek ekologiczny nie jest aktualny: ", i)
                    elif name[0] in OFU1:
                        bledne.append("{0}  -  Dana wartość OFU musi być powiązana z OZU i OZK.".format(i))
                        print("Dana wartość OFU musi być powiązana z OZK: ", i)
                    else:
                        bledne.append("{0}  -  Złe przyjęcie wartości OZK.".format(i))
                        print("Zła przyjęcie wartości OZK: ", i)
                elif len(name) == 2:
                    if name[0] in OFU1 and warunek2(name[0],name[1]) == True:
                        prawidlowe.append(i)
                    elif name[0] in OFU:
                        bledne.append("{0}  -  Podany grunt ({1}) nie podlega gleboznawczej klasyfikacji gruntów.".format(i,name[0]))
                        print("Podany grunt nie podlega gleboznawczej klasyfikacji gruntów: ", i)
                    elif name[0] == 'E':
                        bledne.append("{0}  -  Nieprawidłowe oznaczenie OFU, użytek ekologiczny nie jest aktualny.".format(i))
                        print("Użytek ekologiczny nie jest aktualny: ", i)
                elif len(name) == 3:
                    if name[0] == 'E':
                        bledne.append("{0}  -  Nieprawidłowe oznaczenie OFU, użytek ekologiczny nie jest aktualny.".format(i))
                        print("Użytek ekologiczny nie jest aktualny ", i)

    wyniki.delete(1.0, tk.END)
    n=1
    for wynik in bledne:
        wyniki.insert(tk.END,str(n) + '. ' + wynik + '\n')
        n += 1
def zapisz():
    bledy = wyniki.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Pliki tekstowe", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(bledy)
root = tk.Tk()
root.title("Sprawdzanie błędów w pliku")

wczytaj_button = tk.Button(root, text="Wczytaj plik i sprawdź błędy", command=sprawdz)
wczytaj_button.pack(pady=10)

zapisz_button = tk.Button(root, text="Zapisz błędy do pliku", command=zapisz)
zapisz_button.pack(pady=10)

wyniki = tk.Text(root, height=30, width=90)
wyniki.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

root.mainloop()