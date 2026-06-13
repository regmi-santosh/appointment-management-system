from fastapi import APIRouter, Depends, HTTPException, status

from app.appointments.schemas import AppointmentCreate, Appointment as AppointmentSchema
from app.appointments.service import AppointmentService, get_appointment_service_dep
from app.users.errors import RepositoryError
from app.appointments.schemas import AppointmentUpdate
from fastapi import Response
from app.core.auth import get_current_user_id

router = APIRouter()


@router.post("/", response_model=AppointmentSchema, status_code=status.HTTP_201_CREATED)
def create_appointment(a: AppointmentCreate, svc: AppointmentService = Depends(get_appointment_service_dep), current_user: int = Depends(get_current_user_id)):
    try:
        if a.owner_id != current_user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="cannot create appointment for another user")
        created = svc.create_appointment(title=a.title, description=a.description, start_time=a.start_time, end_time=a.end_time, owner_id=a.owner_id)
    except RepositoryError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return AppointmentSchema(id=created.id, title=created.title, description=created.description, start_time=created.start_time, end_time=created.end_time, owner_id=created.owner_id)


@router.get("/{appointment_id}", response_model=AppointmentSchema)
def get_appointment(appointment_id: int, svc: AppointmentService = Depends(get_appointment_service_dep)):
    appt = svc.get_appointment(appointment_id)
    if appt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appointment not found")
    return AppointmentSchema(id=appt.id, title=appt.title, description=appt.description, start_time=appt.start_time, end_time=appt.end_time, owner_id=appt.owner_id)


@router.get("/owner/{owner_id}")
def list_owner_appointments(owner_id: int, svc: AppointmentService = Depends(get_appointment_service_dep)):
    appts = svc.list_appointments_for_owner(owner_id)
    return [AppointmentSchema(id=a.id, title=a.title, description=a.description, start_time=a.start_time, end_time=a.end_time, owner_id=a.owner_id) for a in appts]


@router.put("/{appointment_id}", response_model=AppointmentSchema)
def update_appointment(appointment_id: int, upd: AppointmentUpdate, svc: AppointmentService = Depends(get_appointment_service_dep), current_user: int = Depends(get_current_user_id)):
    try:
        data = {k: v for k, v in upd.model_dump().items() if v is not None}
        # ownership check
        appt = svc.get_appointment(appointment_id)
        if appt is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appointment not found")
        if appt.owner_id != current_user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not the owner")
        updated = svc.update_appointment(appointment_id, **data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RepositoryError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return AppointmentSchema(id=updated.id, title=updated.title, description=updated.description, start_time=updated.start_time, end_time=updated.end_time, owner_id=updated.owner_id)


@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, svc: AppointmentService = Depends(get_appointment_service_dep), current_user: int = Depends(get_current_user_id)):
    try:
        appt = svc.get_appointment(appointment_id)
        if appt is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appointment not found")
        if appt.owner_id != current_user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not the owner")
        svc.delete_appointment(appointment_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appointment not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
