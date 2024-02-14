from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from .database import get_db

router = APIRouter()


@router.get('/')
def get_cars(db: Session = Depends(get_db)):
    
    cars = db.query(models.Car).all()
    return {'status': 'success', 'results': len(cars), 'cars': cars}


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_car(payload: schemas.CarBaseSchema, db: Session = Depends(get_db)):
    dealer_id = payload.dealer_id
    db_dealer_query = db.query(models.Dealer).filter(models.Dealer.id == dealer_id).first()
    if not db_dealer_query:
        raise HTTPException(status_code=404, detail="Dealer not found")

    new_car = models.Car(**payload.dict())
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return {"status": "success", "car": new_car}


@router.put("/{car_id}")
def update_dealer(car_id: int, payload: schemas.CarBaseSchema, db: Session = Depends(get_db)):
    db_car_query = db.query(models.Car).filter(models.Car.id == car_id)
    db_car = db_car_query.first()

    if not db_car:
        raise HTTPException(status_code=404, detail=f'No car with this id: {car_id} found')

    update_data = payload.dict(exclude_unset=True)
    db_car_query.filter(models.Car.id == car_id).update(update_data,
                                                       synchronize_session=False)
    db.commit()
    db.refresh(db_car)
    return {"status": "success", "Car": db_car}


@router.delete('/{car_id}')
def delete_dealer(car_id: int, db: Session = Depends(get_db)):
    car_query = db.query(models.Car).filter(models.Car.id == car_id)
    car = car_query.first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No car with this id: {car_id} found')
    car_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)