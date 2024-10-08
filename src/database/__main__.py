from database import database_storer, ExtractedMail

email_1 = ExtractedMail(
    de="juan.garcia@empresa.com",
    para=["pedro.martinez@empresa.com", "carmen.lopez@empresa.com"],
    asunto="Actualización del proyecto Alfa",
    texto=(
        "Hola equipo,\n\nLes escribo para informarles sobre los últimos avances del proyecto Alfa. "
        "Hemos completado el desarrollo de la fase inicial y estamos listos para la siguiente etapa.\n\n"
        "Saludos,\nJuan"
    ),
    cif=["B12345678"],
    cups=["ES1234567890XYZ"],
    summary="Informe sobre el estado del proyecto Alfa."
)

email_2 = ExtractedMail(
    de="soporte@banco.com",
    para=["cliente@correo.com"],
    asunto="Aviso importante: Verificación de seguridad",
    texto=(
        "Estimado cliente,\n\nHemos detectado actividad inusual en su cuenta y necesitamos que verifique su identidad. "
        "Por favor, acceda a su área de cliente y siga las instrucciones.\n\nGracias por su colaboración,\nEl equipo de soporte"
    ),
    cif=["A98765432"],
    cups=[],
    summary="Aviso de seguridad para la cuenta del cliente."
)

email_3 = ExtractedMail(
    de="noticias@boletin.com",
    para=["suscriptor@correo.com"],
    asunto="Resumen semanal de noticias",
    texto=(
        "Hola,\n\nAquí tienes el resumen de las noticias más importantes de esta semana: "
        "1. Cambios en la política fiscal. 2. El impacto del cambio climático. 3. Innovaciones tecnológicas en 2024.\n\n"
        "Esperamos que lo disfrutes.\nEl equipo de Noticias"
    ),
    cif=[],
    cups=[],
    summary="Resumen semanal con noticias destacadas."
)

email_4 = ExtractedMail(
    de="rh@empresa.com",
    para=["empleado@empresa.com"],
    asunto="Convocatoria de reunión: Evaluación de desempeño",
    texto=(
        "Estimado/a empleado/a,\n\nLe invitamos a una reunión el próximo martes 3 de octubre a las 10:00 AM "
        "para discutir su evaluación de desempeño anual. Por favor, confirme su asistencia.\n\nSaludos,\nRRHH"
    ),
    cif=["B54321098"],
    cups=["ES9876543210ABC"],
    summary="Convocatoria para evaluación de desempeño del empleado."
)

email_5 = ExtractedMail(
    de="comunicaciones@utilities.com",
    para=["cliente@dominio.com"],
    asunto="Factura de electricidad de septiembre",
    texto=(
        "Estimado cliente,\n\nAdjuntamos la factura correspondiente al mes de septiembre. "
        "El importe total es de 89,75 €. Si tiene alguna consulta, no dude en contactarnos.\n\nGracias por confiar en nosotros,\nAtención al cliente"
    ),
    cif=["A11122334"],
    cups=["ES3216549870JKL"],
    summary="Factura de electricidad del mes de septiembre."
)

test_1 = database_storer(extractedMail=email_1)
test_1.saveMail2DB()
test_2 = database_storer(extractedMail=email_2)
test_2.saveMail2DB()
test_3 = database_storer(extractedMail=email_3)
test_3.saveMail2DB()
test_4 = database_storer(extractedMail=email_4)
test_4.saveMail2DB()
test_5 = database_storer(extractedMail=email_5)
test_5.saveMail2DB()