import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    book_publisher = relationship("Book", back_populates="publisher_book")

    def __str__(self):
        return f"Publisher: id: {self.id}, name: {self.name}"


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40))
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher_book = relationship(Publisher, back_populates="book_publisher")
    stock_book = relationship("Stock", back_populates="book_stock")

    def __str__(self):
        return f"Book: id: {self.id}, title: {self.title}, id_publisher: {self.id_publisher}"


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    stock_shop = relationship("Stock", back_populates="shop_stock")

    def __str__(self):
        return f"Shop: id: {self.id}, name: {self.name}"


class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer)

    book_stock = relationship(Book, back_populates="stock_book")
    shop_stock = relationship(Shop, back_populates="stock_shop")
    sale_stock = relationship("Sale", back_populates="stock_sale")

    def __str__(self):
        return f"Stock: id: {self.id}, id_shop: {self.id_shop}, id_book: {self.id_book}, count:{self.count}"


class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric(8, 2), nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer)

    stock_sale = relationship(Stock, back_populates="sale_stock")

    def __str__(self):
        return (f"Sale: id: {self.id}, price: {self.price}, "
                f"date: {self.date_sale}, id_stock: {self.id_stock}, count: {self.count}")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
