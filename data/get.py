import pandas as pd

def get_job_titles(csv_file):
    # Carrega o arquivo CSV para um DataFrame
    data = pd.read_csv(csv_file)

    # Extrai os dados do campo job_title
    job_titles = data['employee_residence'].unique().tolist()

    return job_titles

# Nome do arquivo CSV
csv_file = 'data.csv'

# Obtém os títulos dos cargos
job_titles = get_job_titles(csv_file)

# Imprime os títulos dos cargos
print(job_titles)
