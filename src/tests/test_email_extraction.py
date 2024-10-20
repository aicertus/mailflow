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

# Nuevos tests con emails ficticios y verificación exacta de CUPS y CIFs

# Test hardcoded para verificar la extracción exacta de un CUPS
def test_hardcoded_cups_extraction():
    email_text = "Estimado cliente, su CUPS es ES12345678901234567890 y debe ser verificado."
    expected_cups = ["ES12345678901234567890"]
    
    email = Email(
        de="cliente@ejemplo.com",
        para=["soporte@empresa.com"],
        asunto="Verificación de CUPS",
        texto=email_text
    )
    extractor = EmailExtractor(email=email)
    extractor.extractEmailInfo()

    logger.info(f"CUPS extraídos: {extractor.extractedEmail.cups}")
    
    # Verificamos que el CUPS extraído es exactamente el esperado
    assert extractor.extractedEmail.cups == expected_cups, f"El CUPS extraído no coincide: {extractor.extractedEmail.cups}"

# Test hardcoded para verificar la extracción exacta de un CIF
def test_hardcoded_cif_extraction():
    email_text = "La factura asociada al CIF B12345678 ha sido emitida correctamente."
    expected_cif = ["B12345678"]
    
    email = Email(
        de="facturacion@empresa.com",
        para=["cliente@ejemplo.com"],
        asunto="Emisión de factura",
        texto=email_text
    )
    extractor = EmailExtractor(email=email)
    extractor.extractEmailInfo()

    logger.info(f"CIFs extraídos: {extractor.extractedEmail.cif}")
    
    # Verificamos que el CIF extraído es exactamente el esperado
    assert extractor.extractedEmail.cif == expected_cif, f"El CIF extraído no coincide: {extractor.extractedEmail.cif}"

# Test hardcoded con múltiples CUPS
def test_multiple_cups_extraction():
    email_text = "En su cuenta se han detectado dos CUPS: ES09876543210987654321 y ES11223344556677889900. Por favor, revise."
    expected_cups = ["ES09876543210987654321", "ES11223344556677889900"]
    
    email = Email(
        de="support@empresa.com",
        para=["user@ejemplo.com"],
        asunto="Detección de CUPS",
        texto=email_text
    )
    extractor = EmailExtractor(email=email)
    extractor.extractEmailInfo()

    logger.info(f"CUPS extraídos: {extractor.extractedEmail.cups}")
    
    # Verificamos que los CUPS extraídos son exactamente los esperados
    assert extractor.extractedEmail.cups == expected_cups, f"Los CUPS extraídos no coinciden: {extractor.extractedEmail.cups}"

# Test hardcoded con un CUPS incorrecto para verificar el fallo
def test_incorrect_cups_extraction():
    email_text = "El CUPS proporcionado es ES00000000000000000001. Revíselo."
    expected_cups = ["ES00000000000000000001"]
    
    email = Email(
        de="verificacion@empresa.com",
        para=["soporte@ejemplo.com"],
        asunto="Revisión de CUPS",
        texto=email_text
    )
    extractor = EmailExtractor(email=email)
    extractor.extractEmailInfo()

    logger.info(f"CUPS extraídos: {extractor.extractedEmail.cups}")
    
    # Verificamos que el CUPS extraído coincide con el incorrecto esperado
    assert extractor.extractedEmail.cups == expected_cups, f"El CUPS extraído no coincide: {extractor.extractedEmail.cups}"

# Test hardcoded con un CIF ficticio y su verificación exacta
def test_cif_with_noise_extraction():
    email_text = "El CIF del proveedor, B87654321, se encuentra entre otros datos importantes."
    expected_cif = ["B87654321"]
    
    email = Email(
        de="proveedor@empresa.com",
        para=["compras@empresa.com"],
        asunto="CIF del proveedor",
        texto=email_text
    )
    extractor = EmailExtractor(email=email)
    extractor.extractEmailInfo()

    logger.info(f"CIFs extraídos: {extractor.extractedEmail.cif}")
    
    # Verificamos que el CIF extraído es exactamente el esperado
    assert extractor.extractedEmail.cif == expected_cif, f"El CIF extraído no coincide: {extractor.extractedEmail.cif}"
