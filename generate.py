import re
import random
import pickle

# забираем обученную модель
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)


# приводим ввод к нужному формату
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


# составляем предсказание
def predict(model, user_input):
    # приведем вводимое в нужный формат
    user_input = formating(user_input)
    user_input = user_input.split()

    # возьмем для модели последние 2 слова
    w1 = len(user_input) - 2
    w2 = len(user_input)
    prev_words = user_input[w1:w2]

    # display prediction from highest to lowest maximum likelihood
    prediction = model[(prev_words[0], prev_words[1])]
    print("Для последних 2 слов вероятностные продолжения следующие: ", prediction)
    # рандомно выберем следующее слово
    next_word = random.choices(list(prediction.keys()))

    # добавим новое слово к предыдущим
    user_input.append(next_word[0])
    return (' '.join(user_input))


print("Введите начало фразы: ")
prefix = input('')
length = int(input('длина генерируемой последовательности'))
i = predict(model, prefix)
while length > 1:
    print(i)
    i = predict(model, str(i))
    length -= 1
print(i)
print('Полное предсказание :', i)
