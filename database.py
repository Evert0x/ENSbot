from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, String, Sequence, Boolean, DateTime, Integer, desc
from sqlalchemy import create_engine, Table, MetaData, ForeignKey, text, bindparam, TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import datetime

Base = declarative_base()
engine = create_engine('sqlite:///meme.db')
Session = sessionmaker(bind=engine)

class Domains(Base):
    __tablename__ = "domains"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String(32), nullable=False)
    ethaddress = Column(String(64), nullable=False)
    domain = Column(String(255), nullable=False, unique=True)
    expires = Column(TIMESTAMP(timezone=False), nullable=False)

    @staticmethod
    def get_expires():
        s = Session()
        data = s.query(Domains).filter(
            Domains.expires <= (datetime.datetime.utcnow() + datetime.timedelta(days=30*13))
        ).all()
        print(data)
        s.close()
        return data


    @staticmethod
    def list(userid):
        text = "The following domains are linked to your account: \n\n"

        s = Session()
        domains = s.query(Domains).filter(Domains.userid == userid).all()
        for domain in domains:
            text += "<b>%s.eth</b> - expires: %s\n" % (domain.domain, domain.expires.date())
        s.close()
        return text

    @staticmethod
    def insert_domains(domains, ethaddress, userid):
        text = "Linked the following domains to your account: \n\n"

        for domain in domains:
            s = Session()
            domain.userid = userid
            domain.ethaddress = ethaddress
            s.add(domain)
            try:
                s.flush()
                text += "<b>%s.eth</b> - expires: %s\n" % (domain.domain, domain.expires.date())
                s.commit()
            except IntegrityError:
                pass
            s.close()
        return text

if __name__ == '__main__':
    Base.metadata.create_all(engine)