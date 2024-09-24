import pytest
import json
import logging
from pathlib import Path
from mailextractor import Email, EmailExtractor

# Configuración estricta de logging para que se muestren todos los mensajes
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Cargar el archivo JSON con los emails de prueba
@pytest.fixture
def emails_json():
    path = Path(__file__).parent / "emails.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["emails"]

# Test para verificar que los CUPS extraídos están en el texto original del email
@pytest.mark.parametrize("email_data", range(5))
def test_cups_extraction(emails_json, email_data):
    email_info = emails_json[email_data]
    logger.info(f"Probando extracción de CUPS para el email: {email_info}")

    email = Email(
        de=email_info["de"],
        para=email_info["para"],
        asunto=email_info["asunto"],
        texto=email_info["texto"]
    )
    extractor = EmailExtractor(email=email)
    extractor.extractEmailInfo()

    logger.info(f"Email procesado: {email_info['asunto']}")
    logger.info(f"CUPS extraídos: {extractor.extractedEmail.cups}")

    # Comprobamos que todos los CUPS extraídos están en el texto original
    for cups in extractor.extractedEmail.cups:
        assert cups in email_info["texto"], f"CUPS {cups} no se encuentra en el texto original"

# Test para verificar que los CIFs extraídos están en el texto original del email
@pytest.mark.parametrize("email_data", range(5))
def test_cif_extraction(emails_json, email_data):
    email_info = emails_json[email_data]
    logger.info(f"Probando extracción de CIF para el email: {email_info}")

    email = Email(
        de=email_info["de"],
        para=email_info["para"],
        asunto=email_info["asunto"],
        texto=email_info["texto"]
    )
    extractor = EmailExtractor(email=email)
    extractor.extractEmailInfo()

    logger.info(f"Email procesado: {email_info['asunto']}")
    logger.info(f"CIFs extraídos: {extractor.extractedEmail.cif}")

    # Comprobamos que todos los CIFs extraídos están en el texto original
    for cif in extractor.extractedEmail.cif:
        assert cif in email_info["texto"], f"CIF {cif} no se encuentra en el texto original"
