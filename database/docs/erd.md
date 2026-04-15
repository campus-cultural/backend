#User
role: Enum(admin, student, professor)
password: str
password_hash: str
email: str
name: str
is_active: bool
ra: str | None. Constraints: if not student must be null

#Evento
id: int
titulo: str
is_active: bool
descricao: str
data: datetime
user_id: fk
created_at: datetime
updated_at: datetime

#EventoImagem
evento_id: int
binary_image: Uint8List[]

#EventoInscricao
id: int
user_id: int fk
event_id: int fk
has_attended: bool
data_inscricao: datetime
