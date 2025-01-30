#funciones basicas reutilizables

#funciones para convertir enlaces de Gdrive
def convert_google_drive_link_to_xlsx(google_drive_link):
    # Extraer el ID del documento
    file_id = google_drive_link.split('/d/')[1].split('/')[0]

    # Formar el enlace para descargar como XLSX
    xlsx_url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx&id={file_id}"

    return xlsx_url



def comproCursoAnterior(campo):
    if campo == 'sin info':
        return 'sin info'
    elif campo.startswith(('No', 'Ninguno')):
        return 'No'
    else:
        return 'Sí'

