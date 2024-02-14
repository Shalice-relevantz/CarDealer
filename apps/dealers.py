from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from .database import get_db

router = APIRouter()


@router.get('/')
def get_dealers(db: Session = Depends(get_db)):
    
    dealers = db.query(models.Dealer).all()
    return {'status': 'success', 'results': len(dealers), 'dealers': dealers}


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_dealer(payload: schemas.DealerBaseSchema, db: Session = Depends(get_db)):
    new_dealer = models.Dealer(**payload.dict())
    db.add(new_dealer)
    db.commit()
    db.refresh(new_dealer)
    return {"status": "success", "dealer": new_dealer}


@router.put("/{dealer_id}")
def update_dealer(dealer_id: int, payload: schemas.DealerBaseSchema, db: Session = Depends(get_db)):
    db_dealer_query = db.query(models.Dealer).filter(models.Dealer.id == dealer_id)
    db_dealer = db_dealer_query.first()

    if not db_dealer:
        raise HTTPException(status_code=404, detail="Dealer not found")

    update_data = payload.dict(exclude_unset=True)
    db_dealer_query.filter(models.Dealer.id == dealer_id).update(update_data,
                                                       synchronize_session=False)
    db.commit()
    db.refresh(db_dealer)
    return {"status": "success", "Dealer": db_dealer}



@router.get('/{dealer_id}')
def get_dealer(dealer_id: int, db: Session = Depends(get_db)):
    dealer = db.query(models.Dealer).filter(models.Dealer.id == dealer_id).first()
    if not dealer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No delear with this id: {dealer_id} found")
    return {"status": "success", "dealer": dealer}


@router.delete('/{dealer_id}')
def delete_dealer(dealer_id: int, db: Session = Depends(get_db)):
    dealer_query = db.query(models.Dealer).filter(models.Dealer.id == dealer_id)
    dealer = dealer_query.first()
    if not dealer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No dealer with this id: {dealer_id} found')
    dealer_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)