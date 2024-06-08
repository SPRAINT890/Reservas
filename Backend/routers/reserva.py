from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated
from schemas.Restaurante import RestauranteBase, RestauranteBDBase, RestauranteHorarioBase
from models import models
from config.bd import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import or_