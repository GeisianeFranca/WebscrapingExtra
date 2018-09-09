import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  passwd="12345",
  database="test"
)

mycursor = mydb.cursor()

#mycursor.execute("CREATE TABLE Mercado (IdMercado int auto_increment primary key, Nome VARCHAR(255))")

#mycursor.execute("CREATE TABLE Produtos (IdProduto int not null auto_increment primary key,Nome varchar (255), Categoria varchar (255), Subcategoria varchar (255), Fabricante varchar (255), Preco float, Peso float, Quantidade int, IdMercado int, constraint fk_produto_mercado foreign key (IdMercado) references Mercado (IdMercado)")

# mycursor.execute("CREATE TABLE Produtos (IdProduto int not null auto_increment primary key,"
#                 "Nome varchar (255),"
#                 "Categoria varchar (255),"
#                 "Subcategoria varchar (255),"
#                 "Fabricante varchar (255),"
#                 "Preco float,"
#                 "Peso float,"
#                 "Quantidade int,"
#                 "IdMercado int,"
#                 "constraint fk_mercado_produto foreign key(IdMercado) references Mercado (IdMercado))")


val = ("Arroz Integral 7 Cereais CAMIL Pacote 1kg")
mycursor.execute("SELECT * from Produtos where Nome ='"+val+"' and IdMercado = 4")

if mycursor.fetchone() != None:
    mycursor.execute("UPDATE Produtos set preco = 10.00 where IdMercado = 4 and Nome = 'Arroz Integral 7 Cereais CAMIL Pacote 1kg'")
mydb.commit()


mydb.close()