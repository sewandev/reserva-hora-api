from datetime import datetime
from pydantic import BaseModel, field_validator, ValidationInfo

# Clase base que contiene los atributos necesarios para crear una cita.
class AppointmentBase(BaseModel):
    patient_id: int
    medic_id: int
    start_time: datetime
    end_time: datetime

    # Valida que la fecha de inicio sea anterior a la fecha de fin.
    @field_validator("end_time")
    def validate_times(cls, end_time: datetime, info: ValidationInfo) -> datetime:
        start_time = info.data.get("start_time")
        if start_time is not None and end_time <= start_time:
            raise ValueError("End time must be after start time")
        return end_time

# Hereda los atributos de AppointmentBase necesarios para crear una cita.
class AppointmentCreate(AppointmentBase): 
    pass

# Hereda los atributos de AppointmentBase necesarios la respuesta que entregará la API junto a otros atributos que suma la clase por si misma.
class AppointmentResponse(AppointmentBase):
    id: int
    status: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "patient_id": 1,
                "medic_id": 1,
                "start_time": "2025-02-13T09:00:00",
                "end_time": "2025-02-13T10:00:00",
                "status": "pending"
            }
        }