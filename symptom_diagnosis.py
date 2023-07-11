"""
For a database on backpain symptoms and their respective diagnosis, convert database into a dictionary
{symptom: diagnosis}
"""

def diagnose(symptoms, data_base):
    """
    Input:

    symptoms: list
    data_base: dictionary

    Output:

    diag[has_diag, potential_diag]: list[bool, list]
    """
    diag = []
    none_count = 0
    potential_diag = []
    for symp in symptoms:
        if symp in data_base:
            potential_diag.append(data_base[symp])

        else:
            none_count+=1
            potential_diag.append(None)

    if none_count == len(symptoms):
        diag.append(False)
    else:
        diag.append(True)
    diag.append(potential_diag)

    return potential_diag

#########TESTING####################
data_base = {'chest pain': 'breathing execies', 'cough': 'cough medicine'}


potential_diagnosis = diagnose(['cough', 'headache', 'chest pain'], data_base)

print(potential_diagnosis)
