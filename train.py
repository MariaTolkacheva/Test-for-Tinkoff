import re
import codecs
import os
import pickle


def main():
    # папка с текстами для обучения
    path = r"C:\Users\Huawei NB\pythonProject3\data\\"

    # считываем текст из каждого файла и обрабатываем его перед обучением

    all_words = []  # список упорядоченных слов из всех файлов
    for filename in os.listdir(path):
        # читаем текст из файла
        name_of = path + filename
        file = codecs.open(name_of, "r", "utf-8")
        text = file.read()
        file.close()
        # приводим текст к понятному и удобному формату
        all_words = all_words + formating(text).split()

    # создаем модель
    model = three_gram_model(all_words)
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)


# создаем 3 грам модель
def three_gram_model(text):
    slovnik = dict()
    for i in range(len(text) - 2):
        # проверяем есть ли уже такое сочетание
        if (text[i], text[i + 1]) not in slovnik:
            slovnik[(text[i], text[i + 1])] = {text[i + 2]: 1}
        elif text[i + 2] in slovnik[(text[i], text[i + 1])].keys():
            slovnik[(text[i], text[i + 1])][text[i + 2]] += 1
        else:
            slovnik[(text[i], text[i + 1])][text[i + 2]] = 1

    # теперь посчитаем вероятность для каждого продолжения
    for i in slovnik:
        k = sum(slovnik[i].values())
        for j in slovnik[i]:
            slovnik[i][j] = slovnik[i][j] / k

    return slovnik


def formating(text):
    # преобразуем текст
    text = re.sub('<.*?>', ' ', text)
    # оставим только цифры и буквы
    text = re.sub('[^a-zA-Z]', ' ', text)
    # заменим абзацы на пробелы
    text = text.replace("\n", " ")
    # сделаем все с прописной
    text = text.lower()
    # уберем пробелы
    text = ' '.join(text.split())
    return text


main()
