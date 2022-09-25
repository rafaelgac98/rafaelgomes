#from crypt import methods
import os
from flask import Flask, request, render_template
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

#MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
app.config['MYSQL_DATABASE_DB'] = 'bd'
app.config['MYSQL_DATABASE_HOST'] = '172.17.0.2'
mysql.init_app(app)

@app.route('/')
def main():
    return render_template('aulamvc.html')

@app.route('/gravar', methods=['POST','GET'])
def gravar():
  nome = request.form['nome']
  preco = request.form['preco']
  categoria = request.form['categoria']
  if nome and preco and categoria:
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('insert into tbl_produto (produto_name, produto_preco, produto_categoria) VALUES (%s, %s, %s)', (nome, preco, categoria))
    conn.commit()
  return render_template('aulamvc.html')

@app.route('/listar', methods=['POST','GET'])
def listar():
  conn = mysql.connect()
  cursor = conn.cursor()
  cursor.execute('select produto_name, produto_preco, produto_categoria from tbl_produto')
  data = cursor.fetchall()
  conn.commit()
  return render_template('lista.html', datas=data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5005))
    app.run(host='0.0.0.0', port=port)


# CREATE TABLE tbl_produto ( produto_id BIGINT NOT NULL AUTO_INCREMENT, produto_name VARCHAR(45) NULL, produto_preco VARCHAR(45) NULL, produto_categoria VARCHAR(45) NULL, PRIMARY KEY (produto_id));