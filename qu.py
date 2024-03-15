from dotenv import load_dotenv
load_dotenv()

from utils import query


if __name__ == "__main__":
    question = 'Где находиться ваша компания? и чем вы занимаетесь?'

    output = query(question)
    print(output)
