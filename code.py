import pandas as pd
import re

assamese_pronouns = set(pd.read_csv('/content/assamese_pronouns.csv')['AS-PRON'].tolist())
assamese_nouns = set(pd.read_csv('/content/assamese_nouns.csv')['AS-NOUN'].tolist())
assamese_verbs = set(pd.read_csv('/content/assamese_verbs.csv')['AS-VERB'].tolist())
assamese_adjectives = set(pd.read_csv('/content/assamese_adjectives.csv')['AS-ADJ'].tolist())
assamese_adverbs = set(pd.read_csv('/content/assamese_adverbs.csv')['AS-ADV'].tolist())
assamese_conjunctions = set(pd.read_csv('/content/assamese_conjunctions.csv')['AS-CONJ'].tolist())

english_pronouns = set(pd.read_csv('/content/english_pronouns.csv')['EN-PRON'].tolist())
english_nouns = set(pd.read_csv('/content/english_nouns.csv')['EN-NOUN'].tolist())
english_verbs = set(pd.read_csv('/content/english_verbs.csv')['EN-VERB'].tolist())
english_adjectives = set(pd.read_csv('/content/english_adjectives.csv')['EN-ADJ'].tolist())
english_adverbs = set(pd.read_csv('/content/english_adverbs.csv')['EN-ADV'].tolist())
english_prepositions = set(pd.read_csv('/content/english_prepositions.csv')['EN-PREP'].tolist())
english_conjunctions = set(pd.read_csv('/content/english_conjunctions.csv')['EN-CONJ'].tolist())
english_interjections = set(pd.read_csv('/content/english_interjections.csv')['EN-INTJ'].tolist())
english_determiners = set(pd.read_csv('/content/english_determiners.csv')['EN-DT'].tolist())


assamese_noun_suffixes = ['ৰ', 'ত', 'লৈ', 'টি', 'খিনি', 'ৰে', 'ডাল', 'জনা', 'বো', 'তকৈ', 'ৰ পৰা', 'তত', 'হক', 'কে', 'কেইজন']
assamese_verb_suffixes = ['ছি', 'ছিল', 'ল', 'িব', 'য়', 'া', 'ই আছো', 'িলেহে', 'ি থাকে', 'ইলো', 'না', 'িব পৰা', 'ক', 'োৱা নাই', 'ৱে', 'হক', 'হল']
assamese_adjective_suffixes = ['তম', 'বিলাক', 'খিনি', 'পৰা', 'ীয়া', 'মুখী']
assamese_adverb_suffixes = ['তকৈ', 'দিনে', 'ই', 'তে', 'লৈকে', 'পৰা', 'হয়']

english_noun_suffixes = ['s', 'es', 'ion', 'ment', 'ity']
english_verb_suffixes = ['ed', 's', 'ing', 'ize', 'ify']
english_adjective_suffixes = ['able', 'ible', 'al', 'ful', 'ive', 'ous', 'ish', 'less']
english_adverb_suffixes = ['ly', 'ward', 'wise']


def pos_tag(token, previous_token=None, next_token=None):
    token_lower = token.lower()

    if token in assamese_pronouns:
        return 'AS-PRON'
    elif token_lower.endswith(tuple(assamese_noun_suffixes)) or token in assamese_nouns:
        return 'AS-NOUN'
    elif token_lower.endswith(tuple(assamese_verb_suffixes)) or token in assamese_verbs:
        return 'AS-VERB'
    elif token_lower.endswith(tuple(assamese_adjective_suffixes)) or token in assamese_adjectives:
        return 'AS-ADJ'
    elif token_lower.endswith(tuple(assamese_adverb_suffixes)) or token in assamese_adverbs:
        return 'AS-ADV'
    elif token in assamese_conjunctions:
        return 'AS-CONJ'

    if token_lower in english_pronouns:
        return 'EN-PRON'
    elif token_lower in english_nouns:
        return 'EN-NOUN'
    elif token_lower in english_verbs:
        return 'EN-VERB'
    elif token_lower in english_adjectives:
        return 'EN-ADJ'
    elif token_lower in english_adverbs:
        return 'EN-ADV'
    elif token_lower in english_prepositions:
        return 'EN-PREP'
    elif token_lower in english_conjunctions:
        return 'EN-CONJ'
    elif token_lower in english_interjections:
        return 'EN-INTJ'
    elif token_lower in english_determiners:
        return 'EN-DT'

    if previous_token:
        if previous_token in english_determiners and token in english_nouns:
            return 'EN-NOUN'
        elif previous_token in assamese_adjectives and token in assamese_nouns:
            return 'AS-NOUN'
        elif previous_token in english_adjectives and token in english_nouns:
            return 'EN-NOUN'
        elif previous_token in assamese_nouns and token in assamese_verbs:
            return 'AS-VERB'
    if next_token:
        if token in english_determiners and next_token in english_nouns:
            return 'EN-DT'
        elif token in assamese_conjunctions and next_token in assamese_verbs:
            return 'AS-CONJ'
        elif token in english_adjectives and next_token in english_nouns:
            return 'EN-ADJ'

    if token in assamese_conjunctions and next_token in assamese_adjectives:
        return 'AS-CONJ'

    return 'UNK'


def pos_tag_sentences(sentences):
    tagged_sentences = []
    for sent in sentences:
        tokens = sent.split()
        tagged_tokens = []
        for i, token in enumerate(tokens):
            previous_token = tokens[i-1] if i > 0 else None
            next_token = tokens[i+1] if i < len(tokens) - 1 else None
            tagged_tokens.append(pos_tag(token, previous_token, next_token))
        tagged_sentences.append((sent, ' '.join(tagged_tokens)))
    return tagged_sentences


def get_input_data():
    choice = input("Do you want to enter a sentence or a CSV file? (Enter 'sentence' or 'csv'): ").strip().lower()

    if choice == 'sentence':
        sentence = input("Please enter the sentence: ")
        return [sentence]

    elif choice == 'csv':
        file_path = input("Please enter the path to the CSV file: ").strip()
        try:
            df = pd.read_csv(file_path)
            return df['sentence'].tolist()
        except Exception as e:
            print(f"Error reading the CSV file: {e}")
            return []

    else:
        print("Invalid choice. Please enter 'sentence' or 'csv'.")
        return []


sentences = get_input_data()
if sentences:
    tagged_sentences = pos_tag_sentences(sentences)

    output_df = pd.DataFrame(tagged_sentences, columns=['Sentence', 'POS_Tags'])
    output_file = 'tagged_sentences_output.csv'
    output_df.to_csv(output_file, index=False)
    print(f"Tagged sentences saved to {output_file}")

    for sent in tagged_sentences[:10]:
        print(sent)
