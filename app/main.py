from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="Product API",
    description="API für Produktverwaltung (Starter-Version)",
    version="0.1.0"
)

# In-Memory Database (nur für Demo, geht beim Neustart verloren)
products_db = []


# ---------- Pydantic Models ----------

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    category: str

    @validator("price")
    def price_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Preis muss positiv sein")
        return v


class ProductCreate(ProductBase):
    """Input-Modell für Produkt-Erstellung"""
    pass


class ProductUpdate(BaseModel):
    """Input-Modell für Produkt-Update (alle Felder optional)"""
    name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None


class ProductResponse(ProductBase):
    """Output-Modell für API-Responses"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ---------- Endpoints ----------

@app.get("/health")
async def health_check():
    return {"status": "ok"}
