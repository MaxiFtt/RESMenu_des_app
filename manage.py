#!/usr/bin/env python3

from flask import(Blueprint,
render_template, request, url_for, redirect,
send_from_directory, session, flash)
from RESMenu_des_app import db
from .login import *
bp = Blueprint('manage',__name__, url_prefix='/')
@bp.route("/manage/search", methods=['GET'])
@login_required
@verif_required
@staff_required
def search():
        productoNombre = request.args.get("nombre",None)
        productosRaw = db.session.execute("SELECT * FROM productos WHERE nombre = :n",
                        {"n":productoNombre})
        productos = []
        for x in productosRaw:
                productos.append(x)
        if len(productos) == 0:
                flash("Tu consulta no ha retornado resultados")
                return redirect("/manage")
        return render_template("search_results.html", productos=productos)
@bp.route("/manage")
@login_required
@verif_required
@staff_required
def select():
    productos = db.session.execute("SELECT * FROM productos")
    return render_template("manage.html", productos=productos)

@bp.route("/manage/insert", methods=['GET','POST'])
@login_required
@verif_required
@staff_required
def insert():
    if request.method == "POST":
        productoNombre = request.form["nombre"]
        productoPrecio = request.form["precio"]
        productoCantidad = request.form["cantidad"]
        productoDesc = request.form["descripcion"]
        horariod = request.form["horariod"]
        horarioh = request.form["horarioh"]
        db.session.execute("""INSERT INTO productos
        (nombre,precio,cantidad, descripcion, disponibilidad_desde, disponibilidad_hasta, propietario)
        VALUES(:n,:p ,:c, :d, :dd,:dh,:prop)""",
        {
        "n":productoNombre,
        "p":productoPrecio,
        "c":productoCantidad,
        "d": productoDesc,
        "dd": horariod,
        "dh": horarioh,
        "prop": session["id"]
        })
        db.session.commit()
        return redirect("/manage")
    else:
        productos = db.session.execute("SELECT * FROM productos")
        return render_template('index.html',productos=productos)
@bp.route("/manage/remove/<int:id>")
@login_required
@verif_required
@staff_required
def remove(id):
    db.session.execute("UPDATE productos SET estado='oculto' WHERE id = :id",{"id":id})
    db.session.commit()
    return redirect("/manage")

@bp.route("/manage/recover/<int:id>")
@login_required
@verif_required
@staff_required
def recover(id):
    db.session.execute("UPDATE productos SET estado='visible' WHERE id = :id",{"id":id})
    db.session.commit()
    return redirect("/manage")
@bp.route("/manage/delete/<int:id>")
@login_required
@verif_required
@staff_required
def delete(id):
    db.session.execute("DELETE FROM productos WHERE estado='oculto' AND id = :id",{"id":id})
    db.session.commit()
    return redirect("/manage")
@bp.route("/manage/update/<int:id>", methods=["GET","POST"])
@login_required
@verif_required
@staff_required
def update(id):
    if request.method == "POST":
        productoNombre = request.form["nombre"]
        productoPrecio = request.form["precio"]
        productoCantidad = request.form["cantidad"]
        productoDesc = request.form["descripcion"]
        horariod = request.form["horariod"]
        horarioh = request.form["horarioh"]
        db.session.execute("""UPDATE productos
        SET nombre= :n ,
        precio= :p,
        descripcion = :d,
        cantidad = :c,
        disponibilidad_desde = :dd,
        disponibilidad_hasta = :dh
        WHERE id= :id
        """,
        {
        "n":productoNombre,
        "p":productoPrecio,
        "c":productoCantidad,
        "d": productoDesc,
        "dd": horariod,
        "dh": horarioh,
        "id":id
        })
        db.session.commit()
        return redirect("/manage")
