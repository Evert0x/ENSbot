from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, String, Sequence, Boolean, DateTime, Integer, desc
from sqlalchemy import create_engine, Table, MetaData, ForeignKey, text, bindparam, TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from telegram import Bot
import settings

Base = declarative_base()
engine = create_engine('sqlite:///meme.db')
Session = sessionmaker(bind=engine)

class Queue(Base):
    __tablename__ = "msg_queue"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(32), nullable=False, unique=True)
    chatid = Column(String(32), nullable=False)
    replyid = Column(Integer, nullable=False)
    text = Column(String(1024), nullable=False)
    datetime = Column(TIMESTAMP(timezone=False), nullable=False)

    @staticmethod
    def delete(s, code):
        data = s.query(Queue).filter(Queue.code==code).first()
        s.delete(data)
        s.commit()

    @staticmethod
    def new(s, code, chatid, text, msgid, dt=None):
        if not dt:
            dt = datetime.utcnow() + timedelta(seconds=10)
        s.add(Queue(
            code=code,
            chatid=chatid,
            text=text,
            datetime=dt,
            replyid=msgid
        ))
        s.commit()

class Extend(Base):
    __tablename__ = "extend"

    code = Column(String(32), primary_key=True)
    userid = Column(String(32), nullable=False)
    domain = Column(String(255), nullable=False)
    msg_id = Column(Integer(), nullable=False)
    txhash = Column(String(127), nullable=True)
    text = Column(String(255), nullable=False)
    callback = Column(Boolean, nullable=False, default=False)

    @staticmethod
    def add(user, name, msg, codes=[]):
        s = Session()
        for code, text in codes:
            s.add(Extend(
                code=code,
                userid=user,
                domain=name,
                msg_id=msg,
                text=text
            ))
        s.commit()
        s.close()

    @staticmethod
    def update(code, hash):
        s = Session()
        try:
            obj = s.query(Extend).filter(Extend.code==code).first()
            if not obj:
                return None
            obj.txhash = hash
            s.commit()
            if obj.callback:
                Queue.delete(s, code)
                obj.action_when_valid()
                return "valid"
            # queue invalid message
            Queue.new(s, code, obj.userid, "You don't have the right client", obj.msg_id)
            return "invalid"
        finally:
            s.close()

    @staticmethod
    def add_callback(code):
        s = Session()
        try:
            obj = s.query(Extend).filter(Extend.code == code).first()
            if not obj:
                return None
            obj.callback = True
            s.commit()
            if obj.txhash:
                Queue.delete(s, code)
                obj.action_when_valid()
            Queue.new(s, code, obj.userid, "You don't have the right client", obj.msg_id)
            return obj.text
        finally:
            s.close()

    def action_when_valid(self):
        bot = Bot(settings.BOT_TOKEN)
        bot.send_message(
            text="Successfully initiated renewal of ENS domain!",
            reply_to_message_id=self.msg_id,
            chat_id=self.userid
        )


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
            Domains.expires <= (datetime.utcnow() + timedelta(days=30*13))
        ).all()
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