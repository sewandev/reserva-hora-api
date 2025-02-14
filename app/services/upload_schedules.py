from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
from io import BytesIO

class UploadSchedulesService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upload_schedules(self, file: bytes, filename: str, content_type: str):
        """
        Procesa un archivo Excel para cargar horarios disponibles.
        
        Args:
            file (bytes): Contenido del archivo Excel.
            filename (str): Nombre del archivo.
            content_type (str): Tipo MIME del archivo.
        
        Returns:
            dict: Mensaje de éxito.
        
        Raises:
            HTTPException: Si el archivo no es un Excel o si ocurre un error al procesarlo.
        """
        # Validar que el archivo es un Excel
        if not filename.endswith(".xlsx"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file format. Only .xlsx files are allowed."
            )

        # Validar el tipo MIME
        if content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Only Excel files are allowed."
            )

        try:
            # Leer el archivo Excel
            df = pd.read_excel(BytesIO(file))

            # Verificar que el archivo tenga las columnas esperadas
            required_columns = {"medic_id", "start_time", "end_time"}
            if not required_columns.issubset(df.columns):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required columns. Expected: {required_columns}"
                )

            # Procesar el DataFrame y guardar los datos en la base de datos
            for index, row in df.iterrows():
                medic_id = row["medic_id"]
                start_time = row["start_time"]
                end_time = row["end_time"]
                # Llamar al repositorio para crear el slot
                # await AppointmentRepository.create_slot(...)

            return {"message": "Schedules uploaded successfully"}

        except KeyError as e:
            # Manejo de errores si falta una columna en el archivo
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required column in the file: {str(e)}"
            )
        except Exception as e:
            # Manejo de errores inesperados
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while processing the file: {str(e)}"
            )