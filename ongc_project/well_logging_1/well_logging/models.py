from well_logging import db

class upload(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    data_file=db.Column(db.String(20),nullable=False,default="B_1.las")
    image_file =db.Column(db.String(20),nullable=False,default="img_1.jpg")

    def __repr__(self):
        return f"upload('{self.image_file}')"