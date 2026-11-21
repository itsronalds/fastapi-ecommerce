from src.db.session import Base, engine
import src.models

def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    print('Tablas creadas')


if __name__ == '__main__':
    init_db()
