from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.db.database import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    image_b64 = Column(Text, nullable=False)
    _thumbnail = Column('thumbnail',Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="images")

    def generate_thumbnail(self, thumbnail_generator):
        self._thumbnail = thumbnail_generator(self.image_b64)

    @hybrid_property
    def thumbnail(self):
        return self._thumbnail
