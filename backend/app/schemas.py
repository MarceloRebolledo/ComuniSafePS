from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, ConfigDict

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
    user_id: Optional[int] = None

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: str
    bio: Optional[str] = ""
    location: Optional[str] = ""
    latitude: float = -38.737
    longitude: float = -72.591
    notifications_enabled: bool = True
    notification_radius_km: float = 5.0
    is_verified: bool = False
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    notifications_enabled: Optional[bool] = None
    notification_radius_km: Optional[float] = None

# Author Nested Response
class AuthorResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)

# Comment schemas
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    report_id: int
    created_at: datetime
    author: AuthorResponse

    model_config = ConfigDict(from_attributes=True)

# Report schemas
class ReportBase(BaseModel):
    title: str
    description: str
    latitude: float
    longitude: float
    address: Optional[str] = None
    category: str
    severity: str

class ReportCreate(ReportBase):
    image_urls: List[str] = []

class ReportResponse(ReportBase):
    id: int
    status: str
    municipality_ticket: Optional[str] = None
    image_urls: List[str]
    created_at: datetime
    author: AuthorResponse
    likes_count: int
    comments_count: int
    user_liked: bool = False

    model_config = ConfigDict(from_attributes=True)

class ReportStatusUpdate(BaseModel):
    status: str  # "abierto", "derivado_muni", "resuelto", "rechazado"

# Notification schemas
class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    body: str
    type: str
    is_read: bool
    created_at: datetime
    related_report_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# Verification and Password Recovery schemas
class EmailVerificationRequest(BaseModel):
    email: EmailStr
    code: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    code: str
    new_password: str
