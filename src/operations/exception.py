from fastapi import HTTPException

NoExistOperation = HTTPException(status_code=404, detail='Таких операций нет')

NoRights = HTTPException(status_code=403, detail='У вас нет таких полномочий')
