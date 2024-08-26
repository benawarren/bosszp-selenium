import pandas as pd
from deep_translator import GoogleTranslator

#translate a string to English from simplifed Chinese
def translate_to_english(text):
    #parse text
    text = text.replace("\n", "")
    #translate text to english
    try:
        translated = GoogleTranslator(source="zh-CN", target="en").translate(text)
        return translated
    except:
        return text

#translate all values in a csv file
def translate_file(file_path):
    #read in file
    data = pd.read_csv(file_path)

    #translate all values
    data['company'] = data['company'].apply(translate_to_english)
    data['description'] = data['description'].apply(translate_to_english)
    data['title'] = data['title'].apply(translate_to_english)
    data['location'] = data['location'].apply(translate_to_english)
    data['labels'] = data['labels'].apply(translate_to_english)
    data['tags'] = data['tags'].apply(translate_to_english)
    data['salary'] = data['salary'].apply(translate_to_english)

    #write translated to file
    new_file_path = file_path.split(".")[0] + "_en.csv"
    data.to_csv(new_file_path)


#translate the latest file by path here
translate_file('/Users/benwarren/Documents/GitHub/bosszp-selenium/output_data/master_file_updated_2024-08-22.csv')