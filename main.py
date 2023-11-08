word_data = {}


def add_word():
    word = input("Please enter word")
    definition = input("Please enter definition")
    note = input("Please enter note")

    word_data.update({word: {"definition": definition, "note": note}})

