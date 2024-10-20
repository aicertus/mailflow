import json
from typing import List
from mailextractor import EmailExtractor, Email  # Importamos la clase EmailExtractor y Email del módulo creado

# JSON con los datos del email
email_data_json = '''
{
    "de": "cliente@example.com",
    "para": ["soporte@empresa.com"],
    "asunto": "Consulta sobre el suministro",
    "texto": "Estimado soporte, por favor revisa el suministro del CUPS ES12345678901234567890. También adjunto el CIF B12345678 para la factura."
}
'''

# Cargar el JSON en un diccionario de Python
email_data = json.loads(email_data_json)

# Crear una instancia de Email a partir de los datos del JSON
email_obj = Email(**email_data)

# Crear el extractor y pasar el email para extraer la información
email_extractor = EmailExtractor(email=email_obj)

# Mostrar la información extraída
print("Información extraída del email:")
print("De:", email_extractor.extractedEmail.de)
print("Para:", email_extractor.extractedEmail.para)
print("Asunto:", email_extractor.extractedEmail.asunto)
print("Texto:", email_extractor.extractedEmail.texto)
print("CIFs extraídos:", email_extractor.extractedEmail.cif)
print("CUPS extraídos:", email_extractor.extractedEmail.cups)
print("Resumen:", email_extractor.extractedEmail.summary)
