import spacy
from spacy import displacy
import itertools
import os
import re


def get_output(data):
    test = nlp(data)

    # for token in test:
    #     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
    #           token.shape_, token.is_alpha, token.is_stop)

    emails = []
    dollar_amounts = []
    companies = []

    list_cycle = itertools.cycle(test)
    next(list_cycle)
    for i in range(len(test)):
        next_element = next(list_cycle)
        if re.match(r"[^@]+@[^@]+\.[^@]+", test[i].text):
            emails.append(test[i])
        if(test[i].pos_ == "SYM" and test[i].tag_ == "$"):
            dollar_amounts.append(next_element)
        if(test[i].pos_ == "PROPN" and test[i].tag_ == "NNP"):
            if(test[i].dep_ == "compound" and next_element.dep_ == "pobj"):
                companies.append(f'{test[i]} {next_element}')
            else:
                if(test[i].dep_ == "pobj" and test[i-1].dep_ != "compound"):
                    companies.append(f'{test[i]}')

    email_cycle = itertools.cycle(emails)
    next(email_cycle)
    company_cycle = itertools.cycle(companies)
    next(company_cycle)
    dollar_amount_cycle = itertools.cycle(dollar_amounts)
    next(dollar_amount_cycle)

    for i in range(len(emails)):
        print(f'{emails[i]}:', end="")
        for j in range(len(companies)):
            print(f' ${dollar_amounts[j]} to {companies[j]}', end="")
            if(len(companies)-j > 1):
                print(',', end="")
        print()

    total = 0.0
    temp = ""

    for i in range(len(dollar_amounts)):
        temp = dollar_amounts[i].text.replace(',', '')
        total += float(temp)

    return total


nlp = spacy.load("en_core_web_sm")

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, 'EmailLog.txt')) as f:
    content = f.readlines()
content = [x.strip() for x in content]
email = ""
overalTotal = 0.00
for line in content:
    if(line != "<<End>>"):
        email = email + " " + line
    else:
        overalTotal += get_output(email)
        email = ""
print(f'Total Requests: ${overalTotal:,}')
# displacy.serve(test1, style="dep")
