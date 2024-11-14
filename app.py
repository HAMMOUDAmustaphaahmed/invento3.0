from flask import Flask,render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy import Numeric,desc
from werkzeug.security import check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql+mysqlconnector://avnadmin:AVNS_C96xtkYSwqY0qMlZ2aS@mysql-2ef51fa8-hammouda-9afc.h.aivencloud.com:19722/invento')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'invento_clé_secrète'
# Initialize SQLAlchemy with the app
db = SQLAlchemy(app)


from functools import wraps

# Décorateur pour restreindre l'accès basé sur les rôles d'utilisateur
def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = session.get('role', None)  # ou utiliser une autre clé si tu stockes différemment
            # Vérifier si l'utilisateur est connecté
            if user_role == None:
                
                return render_template('auth-401.html')  # Rediriger vers la page de connexion
            
            # Récupérer le rôle de l'utilisateur depuis la session
            
            
            # Vérifier si le rôle de l'utilisateur est dans les rôles autorisés
            if user_role not in roles:
                return render_template('auth-403.html')  # Rediriger vers la page d'accueil ou une autre page
            
            return f(*args, **kwargs)
        return decorated_function
    return wrapper


@app.errorhandler(404)
def page_not_found(e):
    return render_template('auth-404.html'), 404


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('signin.html')

# Route for login
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        

        # Fetch the user from the database
        user = User.query.filter_by(username=username).first()

        # Check if user exists
        if user is None:
            return render_template('auth-401.html')
           
        # Check if the password matches
        if user and check_password_hash(user.password, password):
           
            session['role'] = user.role  # Store the username in the session
            session['logged_in'] = True
            session['emplacement']=user.emplacement
            return redirect(url_for("admin"))  # Redirect to the admin page
        else:
            session['role']='None'
            flash("Nom d'utilisateur ou mot de passe incorrect !", "danger")  # Provide feedback to the user
    
    return render_template("signin.html")

@app.route('/logout')
def logout():
        session.clear()  # Efface la session pour déconnecter l'utilisateur
        return redirect(url_for('login'))

# Route pour la page d'administration
@app.route('/admin')
@roles_required('admin')
def admin():
        articles_data = Article.query.all()
        articles_count=0
        quantite_totale=0
        valeur_totale_articles=0
        notification_count_quantite=0
        for article in articles_data:
            articles_count+=1
            quantite_totale += article.quantite  # Ajoute la quantité de chaque article
            if article.quantite <= article.quantite_min:
                notification_count_quantite +=1
            valeur_totale_articles += article.quantite * article.prix_achat
        
        achats_data = Achat.query.all()
        achats_count=0
        achat_quantite_totale=0
        achat_prix_totale=0
        for achat in achats_data:
            achats_count+=1
            achat_quantite_totale += achat.quantite  # Ajoute la quantité de chaque article
            achat_prix_totale += (float(achat.quantite)*float(achat.prix_achat))

        ventes_data = Vente.query.all()
        ventes_count=0
        vente_quantite_totale=0
        vente_prix_totale=0
        for vente in ventes_data:
            ventes_count+=1
            vente_quantite_totale += vente.quantite  # Ajoute la quantité de chaque article
            vente_prix_totale += float(vente.prix_vente) * float(vente.quantite) 
        
        fournisseurs_data=Fournisseur.query.all()
        fournisseurs_count = Fournisseur.query.count()
        usines_data=Usine.query.all()
        usines_count=Usine.query.count()
        demandes_ventes_data=DemandeVente.query.filter_by(etat=1,reception=1).all()
        demandes_achats_data=DemandeAchat.query.filter_by(etat=1,reception=1).all()
        demandes_ventes_count=DemandeVente.query.filter_by(etat=1,reception=1).count()
        demandes_achats_count=DemandeAchat.query.filter_by(etat=1,reception=1).count()
        users_data=User.query.all()
        users_count=User.query.count()
        confirmation_sortie_data=DemandeVente.query.filter_by(etat=0,reception=1).all()
        confirmation_sortie_count=DemandeVente.query.filter_by(etat=0,reception=1).count()
        confirmation_arriver_data=DemandeVente.query.filter_by(etat=0,reception=1).all()
        confirmation_arriver_count=DemandeVente.query.filter_by(etat=0,reception=1).count()

        # Récupérer les articles ayant une quantité inférieure ou égale à la quantité minimale
        articles_quantite_min_data = Article.query.filter(Article.quantite <= Article.quantite_min).all()

        return render_template('index.html',
                               articles_quantite_min_data=articles_quantite_min_data,
                               users_count=users_count,
                           users_data=users_data,
                           articles_count=articles_count,
                           achats_count=achats_count,ventes_count=ventes_count,
                           usines_count=usines_count,
                           fournisseurs_count=fournisseurs_count,
                           demandes_achats_data=demandes_achats_data,
                           demandes_ventes_data=demandes_ventes_data,
                           demandes_achats_count=demandes_achats_count,
                           demandes_ventes_count=demandes_ventes_count,
                           notification_count_quantite=int(notification_count_quantite),
                           quantite_totale=quantite_totale,
                           articles=articles_data,
                           achats=achats_data,
                           achat_quantite_totale=achat_quantite_totale,
                           achat_prix_totale=achat_prix_totale,
                           ventes=ventes_data,
                           vente_prix_totale=vente_prix_totale,
                           quantite_vente_totale=vente_quantite_totale,
                           prix_vente_totale=vente_prix_totale,
                           confirmation_arriver_data=confirmation_arriver_data,
                           confirmation_arriver_count=confirmation_arriver_count,
                           confirmation_sortie_data=confirmation_sortie_data,
                           confirmation_sortie_count=confirmation_sortie_count,
                           fournisseurs_data=fournisseurs_data,
                           usines_data=usines_data,
                           valeur_totale_articles=valeur_totale_articles)
    


@app.route('/rechercher_tout', methods=['GET', 'POST'])
@roles_required('admin')
def rechercher_tout():
    if request.method == 'POST':
        info = request.form.get("search_info")

        # Rechercher dans différentes tables
        result1 = Article.query.filter(
            (Article.code_article.ilike(f"%{info}%")) | (Article.libelle_article.ilike(f"%{info}%"))
        ).all()

        result2 = Achat.query.filter(
            (Achat.code_article.ilike(f"%{info}%")) | (Achat.libelle_article.ilike(f"%{info}%"))
        ).all()

        result3 = Vente.query.filter(
            (Vente.code_article.ilike(f"%{info}%")) | (Vente.libelle_article.ilike(f"%{info}%"))
        ).all()

        result4 = Usine.query.filter(
            Usine.nom_usine.ilike(f"%{info}%")
        ).all()

        result5 = Fournisseur.query.filter(
            Fournisseur.nom_fournisseur.ilike(f"%{info}%")
        ).all()

        # Filtrer les résultats non vides
        results = {
            'articles': result1,
            'achats': result2,
            'ventes': result3,
            'usines': result4,
            'fournisseurs': result5,
        }

        # Vérifier s'il y a des résultats
        if any(results.values()):
            return render_template('search_result.html', **results)
        else:
            message = "Aucun résultat trouvé."
            return f"""<script>alert("{message}");window.history.back();</script>"""
    return render_template('search_result.html')


@app.route('/ajouter_article',methods=["GET", "POST"])

def ajouter_article():
            articles=Article.query.all()
            fournisseurs=Fournisseur.query.all()
            if request.method == 'POST':
                # Retrieve form data
                article_data = {
                'code_article': request.form.get('code_article'),
                'libelle_article': request.form.get('libelle_article'),
                'prix_achat': request.form.get('prix_achat'),
                'assignation': request.form.get('assignation'),
                'quantite': request.form.get('quantite'),
                'fournisseur': request.form.get('fournisseur'),
                'quantite_min': request.form.get('quantite_min'),
                'image': request.form.get('devis')
            }

                # Call the function to add user
                if fun_ajouter_article(article_data):
                    message = "Article ajouté avec succès."
                    # Return a JavaScript alert with the message and then redirect
                    return f"""<script>alert("{message}");window.location.href = "{url_for('index')}";</script>"""
                else:
                    message = "Erreur lors de l'ajout de l'article 1."
                    # Return a JavaScript alert with the message and then redirect
                    return f"""<script>alert("{message}");window.location.href = "{url_for('ajouter_article')}";</script>"""
            return render_template('ajouter_article.html',fournisseurs=fournisseurs,articles=articles)
     
    
    


    # routes.py

@app.route('/rechercher_details_article', methods=['GET', 'POST'])
@roles_required('admin')
def rechercher_details_article():
    Artciles_data = Article.query.all()
    if request.method == 'POST':
        code_article = request.form.get("code_article")
        site = request.form.get("site")  # Récupérer la valeur de l'assignation (site)

        # Si l'utilisateur a sélectionné un site spécifique, on filtre en fonction
        if site != "tout":
            article_data = Article.query.filter_by(code_article=code_article, assignation=site).all()
        else:
            # Sinon, on affiche tous les articles correspondant au code_article
            article_data = Article.query.filter_by(code_article=code_article).all()

    
    return render_template('details_article.html', article_data=article_data, Artciles_data=Artciles_data)


             

@app.route('/rechercher_article', methods=['GET', 'POST'])
@roles_required('admin')
def rechercher_article():
    all_articles = Article.query.all()
    if request.method == 'POST':
        code_article = request.form.get("code_article")
        site = request.form.get("site")

        if site != "tout":
            articles = Article.query.filter_by(code_article=code_article, assignation=site).all()
            if articles:
                return render_template('editer_article.html', articles=articles, all_articles=all_articles)
            else:
                message = "Article not found."
                flash(message, 'warning')  # Utiliser flash pour afficher un message d'alerte
                return render_template('editer_article.html', all_articles=all_articles)


        elif site == 'tout':
            articles = Article.query.filter_by(code_article=code_article).all()
            return render_template('editer_article.html', articles=articles, all_articles=all_articles)
    else:
        return render_template('editer_article.html',all_articles=all_articles)


                
@app.route('/editer_article', methods=['POST','GET'])
@roles_required('admin')
def editer_article():
        all_articles=Article.query.all()
        id_article= request.form.get('id_article')
        action = request.form.get('action')  # Récupérer l'action (edit ou delete)
        article = fun_info_article(id_article)
       
        if action == 'edit':
            if article:
                # Mettre à jour les informations de l'article
                article.code_article = request.form.get('code_article')
                article.libelle_article = request.form.get('libelle_article')
                article.prix_achat = request.form.get('prix')
                article.assignation = request.form.get('assignation')
                article.quantite = request.form.get('quantite')
                article.fournisseur = request.form.get('fournisseur')
                article.quantite_min = request.form.get('quantite_min')
                article.image = request.form.get('devis')
                


                # Valider les données et committer les mises à jour
                try:
                    
                    db.session.commit()
                    message = "Article modifié avec succès."
                    # Return a JavaScript alert with the message and then redirect
                    return f"""<script>alert("{message}");window.location.href = "{url_for('editer_article')}";</script>"""
                    
                except :
                    db.session.rollback()
                    message = "Erreur lors de la mise à jour de l'article. 1 "
                    # Return a JavaScript alert with the message and then redirect
                    return f"""<script>alert("{message}");window.location.href = "{url_for('editer_article')}";</script>"""
            else:
                message = "Article not found."
                # Return a JavaScript alert with the message and then redirect
                return f"""<script>alert("{message}");window.location.href = "{url_for('editer_article')}";</script>"""

        elif action == 'delete':
            if article:
                # Supprimer l'article de la base de données
                db.session.delete(article)
                db.session.commit()
                message = "Article supprimé avec succès."
                # Return a JavaScript alert with the message and then redirect
                return f"""<script>alert("{message}");window.location.href = "{url_for('editer_article')}";</script>"""

                
               
            else:
                message = "Article not found."
                # Return a JavaScript alert with the message and then redirect
                return f"""<script>alert("{message}");window.location.href = "{url_for('editer_article')}";</script>"""

        return render_template('editer_article.html',all_articles=all_articles)  # Rediriger si aucune action trouvée
    

@app.route('/details_article', methods=['POST','GET'])
@roles_required('admin')
def details_article():
    Artciles_data=Article.query.all()
    code_article = request.form.get('code_article')
    article = fun_info_article(code_article)
    return render_template('details_article.html',Artciles_data=Artciles_data)  # Rediriger si aucune action trouvée

@app.route('/supprimer_vente', methods=['POST'])
@roles_required('admin')
def supprimer_vente():
    code_demande = request.form.get('code_demande')

    # Rechercher la vente dans la base de données
    vente = DemandeVente.query.filter_by(code_demande=code_demande).first()

    if vente:
        try:
            # Supprimer la vente de la base de données
            db.session.delete(vente)
            db.session.commit()
            flash('La vente a été supprimée avec succès.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la suppression : {str(e)}', 'danger')
    else:
        flash('Vente introuvable.', 'danger')

    return redirect(url_for('ventes'))


@app.route('/transfere_article', methods=['POST', 'GET'])
@roles_required('admin')
def transfere_article():
    Articles_data = Article.query.all()

    if request.method == 'POST':
        # Récupérer les données du formulaire
        code_article = request.form.get('code_article')
        quantite_transfer = int(request.form['quantite_transfer'])
        site_expédition = request.form['site_expédition']
        site_destination = request.form['site_destination']

        if site_expédition == site_destination:
            
            return '<script>alert("Le site d expédition et le site de destination ne peuvent pas être identiques.");</script>'

        # Vérifier si l'article existe dans le site d'expédition
        article_expédition = Article.query.filter_by(code_article=code_article, assignation=site_expédition).first()

        if article_expédition:
            if article_expédition.quantite < quantite_transfer:
                
                return '<script>alert("Quantité insuffisante dans le site d expédition.");</script>'

            # Vérifier si l'article existe dans le site de destination
            article_destination = Article.query.filter_by(code_article=code_article, assignation=site_destination).first()

            if article_destination:
                # Ajouter la quantité transférée à l'article existant
                article_destination.quantite += quantite_transfer
                
                return '<script>alert("Quantité transferer avec succees.");</script>'
            else:
                # Créer un nouvel article pour le site de destination
                new_article = Article(
                    code_article=article_expédition.code_article,
                    libelle_article=article_expédition.libelle_article,
                    prix_achat=article_expédition.prix_achat,
                    fournisseur=article_expédition.fournisseur,
                    assignation=site_destination,
                    quantite=quantite_transfer,
                    quantite_min=article_expédition.quantite_min,
                    date=datetime.now(timezone.utc),
                    image=article_expédition.image
                )
                db.session.add(new_article)
                flash(f"Nouvel article créé pour avec la quantité transférée.", 'success')

            # Réduire la quantité dans le site d'expédition
            article_expédition.quantite -= quantite_transfer

            # Commit les changements
            db.session.commit()
        else:
            return '<script>alert("Article introuvable dans le site d expédition.");</script>'


    return render_template('transfere_article.html', Articles_data=Articles_data)




@app.route('/supprimer_article')
@roles_required('admin')
def supprimer_article():
    code_article = request.form.get('code_article')  # Get the article code from the form

    # Find the article in the database
    article = Article.query.filter_by(code=code_article).first()

    if article:
        db.session.delete(article)  # Delete the article if found
        db.session.commit()  # Commit the transaction
        message = "Article deleted successfully!."
        # Return a JavaScript alert with the message and then redirect
        return f"""<script>alert("{message}");window.location.href = "{url_for('editer_article')}";</script>"""
    else:
                message = "Article not found."
                # Return a JavaScript alert with the message and then redirect
                return f"""<script>alert("{message}");window.location.href = "{url_for('editer_article')}";</script>"""




    # routes.py
        

@app.route('/maps')
@roles_required('admin')
def maps():
        
            return render_template('maps.html')
        
        

@app.route('/charts')
@roles_required('admin')
def charts():
        
            return render_template('auth-500.html')
        

@app.route('/messages')
@roles_required('admin')
def messages():
        
            return render_template('auth-500.html')
        
        

@app.route('/ajouter_user', methods=['GET', 'POST'])
@roles_required('admin')
def ajouter_user():
            
            users=User.query.all()
            if request.method == 'POST':
                # Retrieve form data
                user_data = {
                    'username': request.form['username'],
                    'password': request.form['password'],
                    'emplacement': request.form['emplacement'],
                    'role': request.form['role'],
                    'numero_telephone': request.form['numero_telephone']
                }

                # Call the function to add user
                if fun_ajouter_user(user_data):
                    flash("Utilisateur ajouté avec succès", "success")
                else:
                    flash("Erreur lors de l'ajout de l'utilisateur", "danger")
            return render_template('ajouter_user.html',users=users)
        

@app.route('/rechercher_user', methods=['GET', 'POST'])
@roles_required('admin')
def rechercher_user():
        users=User.query.all()
        if request.method == 'POST':
            username = request.form.get("username")
            user = fun_info_user(username)
            if user:
                return render_template('editer_user.html', user=user,users=users)
            else:
                message = "user not found."

                # Return a JavaScript alert with the message and then redirect
                return f"""<script>alert("{message}");window.location.href = "{url_for('editer_user')}";</script>"""
        return render_template('editer_user.html',users=users)
        

        
@app.route('/editer_user', methods=['POST', 'GET'])
@roles_required('admin')
def editer_user():
    users=User.query.all()
    if request.method == 'POST':
        print(request.form)  # Debugging: Print all submitted form data
        id_user = request.form.get('id')
        action = request.form.get('action')
        print(f"Received id_user: {id_user}, action: {action}")

        user = User.query.get(id_user)
        if not user:
            print("user not found.")
            message = "user not found."
            return f"""<script>alert("{message}");window.location.href = "{url_for('rechercher_user')}";</script>"""

        if action == 'edit':
            user.username = request.form.get('username')  # Correct field name
            new_password = request.form.get('password')
            if new_password == user.password :
                user.password=new_password
            else :
                hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
                user.password=hashed_password
            user.emplacement = request.form.get('emplacement')
            user.numero_telephone = request.form.get('numero_telephone')
            user.role = request.form.get('role')  # Make sure this is in the form
            print("Updating user details")
            print(user)
            try:
                db.session.commit()
                message = "user modifié avec succès."
                return f"""<script>alert("{message}");window.location.href = "{url_for('rechercher_user')}";</script>"""
            except Exception as e:
                db.session.rollback()
                message = f"Erreur lors de la mise à jour du user: {e}"
                print(message)
                return f"""<script>alert("{message}");</script>"""

        elif action == 'delete':
            print("Attempting to delete user")
            try:
                db.session.delete(user)
                db.session.commit()
                message = "user supprimé avec succès."
                return f"""<script>alert("{message}");window.location.href = "{url_for('rechercher_user')}";</script>"""
            except Exception as e:
                db.session.rollback()
                message = f"Erreur lors de la suppression user: {e}"
                print(message)
                return f"""<script>alert("{message}");window.location.href = "{url_for('rechercher_user')}";</script>"""

    return render_template('editer_user.html',users=users)

    
@app.route('/supprimer_user')
@roles_required('admin')
def supprimer_user():

    username = request.form.get('username') 
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)  
        db.session.commit() 
        message = "User deleted successfully!."
        return f"""<script>alert("{message}");window.location.href = "{url_for('editer_article')}";</script>"""
    else:
        message = "User not found."
        return f"""<script>alert("{message}");window.location.href = "{url_for('editer_article')}";</script>"""
    
        
        

@app.route('/ajouter_usine',methods=['GET', 'POST'])
@roles_required('admin')
def ajouter_usine():
            usines=Usine.query.all()
            if request.method == 'POST':
                # Retrieve form data
                usine_data = {
                    'nom_usine': request.form['nom_usine'],
                    'region': request.form['region'],
                    'adresse': request.form['adresse'],
                    'latitude': request.form['latitude'],
                    'longitude': request.form['longitude'],
                    'telephone': request.form['telephone'],
                    'etat': request.form['etat']
                }

                # Call the function to add user
                if fun_ajouter_usine(usine_data):
                    flash("Usine ajouté avec succès", "success")
                else:
                    flash("Erreur lors de l'ajout de l'usine", "danger")
            return render_template('ajouter_usine.html',usines=usines)
        


   
        
@app.route('/rechercher_usine', methods=['GET', 'POST'])
@roles_required('admin')
def rechercher_usine():
        usines=Usine.query.all()
        if request.method == 'POST':
            nom_usine = request.form.get("nom_usine")
            usine = fun_info_usine(nom_usine)
            if usine:
                return render_template('editer_usine.html', usine=usine,Usines_data=usines)
            else:
                message = "Usine not found."

                # Return a JavaScript alert with the message and then redirect
                return f"""<script>alert("{message}");window.location.href = "{url_for('editer_usine')}";</script>"""
        return render_template('editer_usine.html',Usines_data=usines)
        
    
        
@app.route('/editer_usine', methods=['POST', 'GET'])
@roles_required('admin')
def editer_usine():
    Usines_data=Usine.query.all()
    if request.method == 'POST':
        print(request.form)  # Debugging: Print all submitted form data
        id_usine = request.form.get('id_usine')
        action = request.form.get('action')
        print(f"Received id_usine: {id_usine}, action: {action}")

        usine = Usine.query.get(id_usine)
        if not usine:
            print("Usine not found.")
            message = "Usine not found."
            return f"""<script>alert("{message}");window.location.href = "{url_for('rechercher_usine')}";</script>"""

        if action == 'edit':
            usine.nom_usine = request.form.get('nom_usine')  # Correct field name
            usine.region = request.form.get('region')
            usine.adresse = request.form.get('adresse')
            usine.latitude = request.form.get('latitude')
            usine.longitude = request.form.get('longitude')
            usine.telephone = request.form.get('telephone')
            usine.etat = request.form.get('etat')  # Make sure this is in the form
            print("Updating usine details")
            print(usine)
            try:
                db.session.commit()
                message = "Usine modifié avec succès."
                return f"""<script>alert("{message}");window.location.href = "{url_for('rechercher_usine')}";</script>"""
            except Exception as e:
                db.session.rollback()
                message = f"Erreur lors de la mise à jour du usine: {e}"
                print(message)
                return f"""<script>alert("{message}");</script>"""

        elif action == 'delete':
            print("Attempting to delete usine")
            try:
                db.session.delete(usine)
                db.session.commit()
                message = "Usine supprimé avec succès."
                return f"""<script>alert("{message}");window.location.href = "{url_for('rechercher_usine')}";</script>"""
            except Exception as e:
                db.session.rollback()
                message = f"Erreur lors de la suppression usine: {e}"
                print(message)
                return f"""<script>alert("{message}");window.location.href = "{url_for('rechercher_usine')}";</script>"""

    return render_template('editer_usine.html',Usines_data=Usines_data)

    
@app.route('/supprimer_usine')
@roles_required('admin')
def supprimer_usine():
        
            return render_template('editer_usine.html')
        
        
@app.route('/ajouter_fournisseur',methods=['GET', 'POST'])
@roles_required('admin')
def ajouter_fournisseur():
            fournisseurs=Fournisseur.query.all()
            if request.method == 'POST':
                # Retrieve form data
                fournisseur_data = {
                    'nom_fournisseur': request.form['nom_fournisseur'],
                    'matricule_fiscale': request.form['matricule_fiscale'],
                    'adresse': request.form['adresse'],
                    'telephone': request.form['telephone'],
                }

                # Call the function to add user
                if fun_ajouter_fournisseur(fournisseur_data):
                    flash("Fournisseur ajouté avec succès", "success")
                else:
                    flash("Erreur lors de l'ajout de fournisseur", "danger")
            return render_template('ajouter_fournisseur.html',fournisseurs=fournisseurs)
        
        
        
@app.route('/rechercher_fournisseur', methods=['GET', 'POST'])
@roles_required('admin')
def rechercher_fournisseur():
        fournisseursss=Fournisseur.query.all()
        if request.method == 'POST':
            nom_fournisseur = request.form.get("nom_fournisseur")
            fournisseur = fun_info_fournisseur(nom_fournisseur)
            if fournisseur:
                return render_template('editer_fournisseur.html', fournisseur=fournisseur,fournisseursss=fournisseursss)
            else:
                message = "Fournisseur not found."

                # Return a JavaScript alert with the message and then redirect
                return f"""<script>alert("{message}");window.location.href = "{url_for('editer_fournisseur')}";</script>"""
        return render_template('editer_fournisseur.html',fournisseursss=fournisseursss)
        
    
        
@app.route('/editer_fournisseur', methods=['POST', 'GET'])
@roles_required('admin')
def editer_fournisseur():
    fournisseursss=Fournisseur.query.all()
    if request.method == 'POST':
        id_fournisseur = request.form.get('id_fournisseur')  # Retrieve id_fournisseur
        action = request.form.get('action')  # Retrieve the action (edit or delete)
        print(f"Received id_fournisseur: {id_fournisseur}, action: {action}")  # Debug statement

        # Use ID to find the fournisseur
        fournisseur = Fournisseur.query.get(id_fournisseur)
        if not fournisseur:
            print("Fournisseur not found.")  # Debug statement
            message = "Fournisseur not found."
            return f"""<script>alert("{message}");window.location.href = "{url_for('rechercher_fournisseur')}";</script>"""

        if action == 'edit':
            # Update fournisseur details
            fournisseur.nom_fournisseur = request.form.get('nom_fournisseur')
            fournisseur.matricule_fiscale = request.form.get('matricule_fiscale')
            fournisseur.adresse = request.form.get('adresse')
            fournisseur.telephone = request.form.get('telephone')
            print("Updating fournisseur details")  # Debug statement
            print(fournisseur)
            try:
                db.session.commit()
                message = "Fournisseur modifié avec succès."
                return f"""<script>alert("{message}");window.location.href = "{url_for('rechercher_fournisseur')}";</script>"""
            except Exception as e:
                db.session.rollback()
                message = f"Erreur lors de la mise à jour du fournisseur: {e}"
                print(message)  # Debug statement
                return f"""<script>alert("{message}");</script>"""

        elif action == 'delete':
            # Delete the fournisseur
            print("Attempting to delete fournisseur")  # Debug statement
            try:
                db.session.delete(fournisseur)
                db.session.commit()
                message = "Fournisseur supprimé avec succès."
                return f"""<script>alert("{message}");window.location.href = "{url_for('rechercher_fournisseur')}";</script>"""
            except Exception as e:
                db.session.rollback()
                message = f"Erreur lors de la suppression du fournisseur: {e}"
                print(message)  # Debug statement
                return f"""<script>alert("{message}");window.location.href = "{url_for('rechercher_fournisseur')}";</script>"""

    # Render the edit form if the request method is GET
    return render_template('editer_fournisseur.html',fournisseursss=fournisseursss)  # Show the form if no action found

       
        
@app.route('/supprimer_fournisseur')
@roles_required('admin')
def supprimer_fournisseur():
        
            return render_template('editer_fournisseur.html')
        


@app.route('/ajouter_demande_achat',methods=["GET", "POST"])
@roles_required('admin')
def ajouter_demande_achat():
       
            if request.method == 'POST':
                # Retrieve form data
                demande_achat_data = {
                'code_article': request.form.get('code_article'),
                'libelle_article': request.form.get('libelle_article'),
                'assignation': request.form.get('assignation'),
                'quantite': request.form.get('quantite'),
            }

                # Call the function to add user
                if fun_ajouter_demande_achat(demande_achat_data):
                    message = "Demande d'achat ajouté avec succès."
                    # Return a JavaScript alert with the message and then redirect
                    return f"""<script>alert("{message}");window.location.href = "{url_for('admin')}";</script>"""
                else:
                    message = "La quantité de la demande dépasse la quantité dans le stock ou il ya un erreur lors de l'insertion de la demande dans la table"
                    # Return a JavaScript alert with the message and then redirect
                    return f"""<script>alert("{message}");window.location.href = "{url_for('ajouter_demande_achat')}";</script>"""
            return render_template('ajouter_demande_achat.html')
     


    


    # routes.py

@app.route('/rechercher_demande_achat', methods=['GET', 'POST'])
@roles_required('admin')
def rechercher_demande_achat():
        demandes_achats=DemandeAchat.query.all()
        if request.method == 'POST':
            code_demande = request.form.get("code_demande")
            demande_achat = DemandeAchat.query.filter_by(code_demande=code_demande).first()
            if demande_achat:
                return render_template('confirmer_demande_achat.html', demande_achat=demande_achat,demandes_achats=demandes_achats)
            else:
                message = "Demande achat not found."

                # Return a JavaScript alert with the message and then redirect
                return f"""<script>alert("{message}");window.location.href = "{url_for('confirmer_demande_achat')}";</script>"""
                
@app.route('/confirmer_demande_achat', methods=['POST','GET'])
@roles_required('admin')
def confirmer_demande_achat():
        demandes_achats=DemandeAchat.query.filter_by(etat=1,reception=1).all()
        code_demande = request.form.get('code_demande')
        action = request.form.get('action')  # Récupérer l'action (edit ou delete)
        demande_achat = DemandeAchat.query.filter_by(code_demande=code_demande).first()
       
        if action == 'confirmer':
            if demande_achat:
                # Mettre à jour les informations de l'article
                demande_achat.code_article = request.form.get('code_article')
                demande_achat.libelle_article = request.form.get('libelle_article')
                demande_achat.prix_achat = request.form.get('prix')
                demande_achat.assignation = request.form.get('assignation')
                demande_achat.quantite = request.form.get('quantite')
                demande_achat.fournisseur=request.form.get('fournisseur')
                demande_achat.prix_achat=request.form.get('prix_achat')
                demande_achat.etat=0
                # Valider les données et committer les mises à jour
                try:
                    
                    db.session.commit()
                    
                    message = "Demande d'achat modifié avec succès."
                    # Return a JavaScript alert with the message and then redirect
                    return f"""<script>alert("{message}");window.location.href = "{url_for('confirmer_demande_achat')}";</script>"""
                    
                except :
                    db.session.rollback()
                    message = "Erreur lors de la mise à jour de la demande d'achat. 1 "
                    # Return a JavaScript alert with the message and then redirect
                    return f"""<script>alert("{message}");window.location.href = "{url_for('confirmer_demande_achat')}";</script>"""
            else:
                message = "Demande d'achat not found."
                # Return a JavaScript alert with the message and then redirect
                return f"""<script>alert("{message}");window.location.href = "{url_for('confirmer_demande_achat')}";</script>"""

        elif action == 'delete':
            if demande_achat:
                # Supprimer l'article de la base de données
                demande_achat.etat=2
                demande_achat.reception=2
                db.session.commit()
                message = "Demande d'achat supprimé avec succès."
                # Return a JavaScript alert with the message and then redirect
                return f"""<script>alert("{message}");window.location.href = "{url_for('confirmer_demande_achat')}";</script>"""

                
               
            else:
                message = "Demande not found."
                # Return a JavaScript alert with the message and then redirect
                return f"""<script>alert("{message}");window.location.href = "{url_for('confirmer_demande_achat')}";</script>"""

        return render_template('confirmer_demande_achat.html',demandes_achats=demandes_achats)  # Rediriger si aucune action trouvée
    

# Fonction pour récupérer le numéro de semaine de la date
def numero_semaine(date):
    """Retourne le numéro de la semaine de l'année pour une date donnée."""
    return date.isocalendar()[1]  # Retourne le numéro de semaine pour la date

def generer_lot_achat():
    """Génère un numéro de lot unique en fonction de l'année, du numéro de semaine et d'une séquence."""
    current_date = datetime.now(timezone.utc)
    year = current_date.strftime("%Y")
    week_number = numero_semaine(current_date)
    
    # Obtenir le dernier enregistrement d'achat de la même semaine et de la même année
    dernier_achat = Achat.query.filter(Achat.lot.like(f"{year}S{str(week_number).zfill(2)}%")).order_by(Achat.lot.desc()).first()

    if dernier_achat:
        # Extraire la dernière séquence de lot
        dernier_lot = dernier_achat.lot
        dernier_sequence = int(dernier_lot[7:])
        nouvelle_sequence = dernier_sequence + 1
    else:
        # Si aucun achat n'existe pour cette semaine, démarrer à 1
        nouvelle_sequence = 1
    
    # Générer le numéro de lot
    lot_number = f"{year}S{str(week_number).zfill(2)}{str(nouvelle_sequence).zfill(6)}"
    return lot_number


# Fonction pour ajouter un achat
def ajouter_achat(code_demande, code_article, libelle_article, quantite, prix_achat, assignation, fournisseur):
    """Ajoute un nouvel achat dans la base de données avec un numéro de lot généré automatiquement."""
    lot = generer_lot_achat()  # Génère le lot
    new_achat = Achat(
        lot=lot,
        code_demande=code_demande,
        code_article=code_article,
        libelle_article=libelle_article,
        quantite=quantite,
        prix_achat=prix_achat,
        assignation=assignation,
        fournisseur=fournisseur
    )
    print(new_achat)
    
    # Ajouter et committer la transaction dans la base de données
    db.session.add(new_achat)
    db.session.commit()
    return new_achat

from decimal import Decimal

def update_article_quantity_and_pmp(code_article, quantite_ajoutee, prix_nouvel_achat):
    # Convertir les valeurs en Decimal si elles ne le sont pas déjà
    quantite_ajoutee = Decimal(quantite_ajoutee)
    prix_nouvel_achat = Decimal(prix_nouvel_achat)
    
    # Récupérer l'article correspondant au code_article
    article = Article.query.filter_by(code_article=code_article).first()
    
    # Vérifier si l'article existe
    if not article:
        print("Article non trouvé.")
        return False  # ou gérer cette situation autrement

    try:
        # Assurez-vous que les valeurs actuelles de l'article sont également des Decimals
        quantite_actuelle = Decimal(article.quantite)
        prix_actuel = Decimal(article.prix_achat)
        
        # Calculer la nouvelle quantité totale et le PMP
        quantite_totale = quantite_actuelle + quantite_ajoutee
        pmp = ((quantite_actuelle * prix_actuel) + (quantite_ajoutee * prix_nouvel_achat)) / quantite_totale
        
        # Mettre à jour la quantité et le prix d'achat (PMP)
        article.quantite = quantite_totale
        article.prix_achat = pmp
        
        # Sauvegarder les changements dans la base de données
        db.session.commit()
        return True
    
    except Exception as e:
        print(f"Erreur lors de la mise à jour de l'article: {e}")
        db.session.rollback()  # Rollback si une erreur survient
        return False



@app.route('/confirmer_reception_achat', methods=['POST', 'GET'])
@roles_required('admin')
def confirmer_reception_achat():
    demandes_achats = DemandeAchat.query.filter_by(etat=0, reception=1).all()  # Récupérer toutes les demandes d'achats pour l'affichage
    
    if request.method == 'POST':
        code_demande = request.form.get('code_demande')
        action = request.form.get('action')  # Récupérer l'action (ici, 'confirmer')
        
        # Trouver la demande d'achat correspondante
        demande_achat = DemandeAchat.query.filter_by(code_demande=code_demande).first()
       
        if demande_achat and action == 'confirmer':
            if demande_achat.reception == 1:  # Vérifier si la réception est encore en attente
                # Mettre à jour les informations de la demande d'achat
                demande_achat.reception = 0  # Marquer comme reçu
                demande_achat.etat = 0 # Mettre l'état à confirmé (par exemple)
                
                nouvel_achat = ajouter_achat(
                    code_demande=demande_achat.code_demande,
                    code_article=demande_achat.code_article,
                    libelle_article=demande_achat.libelle_article,
                    quantite=demande_achat.quantite,
                    prix_achat=demande_achat.prix_achat,
                    assignation=demande_achat.assignation,
                    fournisseur=demande_achat.fournisseur
                )
                print(nouvel_achat)
                update_article_quantity_and_pmp(demande_achat.code_article,demande_achat.quantite,demande_achat.prix_achat)
                
                # Valider les données et committer les mises à jour
                try:
                    db.session.commit()
                    flash(f"Achat ajouté avec succès avec le lot {nouvel_achat.lot}", "success")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Erreur lors de la réception de l'achat: {e}", "error")
                return redirect(url_for('confirmer_reception_achat'))  # Rediriger vers la même page pour éviter le rechargement de la page

    # Afficher la page avec la liste des demandes d'achats
    return render_template('confirmer_reception_achat.html', demandes_achats=demandes_achats)
# Route to add a new sales request
@app.route('/ajouter_demande_vente', methods=["GET", "POST"])
@roles_required('admin')
def ajouter_demande_vente():
    # Fetching data for dropdowns
    Articles_data = Article.query.all()
    usines_data = Usine.query.all()
    
    if request.method == 'POST':
        try:
            # Retrieve and validate form data
            demande_vente_data = {
                'code_article': request.form.get('code_article'),
                'libelle_article': request.form.get('libelle_article'),
                'quantite': int(request.form.get('quantite', 0)),          
                'vers': request.form.get('vers'),
                'commande': request.form.get('commande'),
                'assignation': request.form.get('site'),
            }

            # Check if article exists with the specified assignment
            article = Article.query.filter_by(code_article=demande_vente_data['code_article'], assignation=demande_vente_data['assignation']).first()
            if not article:
                message = "Article non trouvé."
                return f"""<script>alert("{message}");window.location.href = "{url_for('ajouter_demande_vente')}";</script>"""

            # Verify stock quantity
            if demande_vente_data['quantite'] > article.quantite:
                message = "La quantité demandée dépasse la quantité en stock."
                return f"""<script>alert("{message}");window.location.href = "{url_for('ajouter_demande_vente')}";</script>"""

            # Call function to add sales request
            if fun_ajouter_demande_vente(demande_vente_data):
                message = "Demande de vente ajoutée avec succès."
                return f"""<script>alert("{message}");window.location.href = "{url_for('admin')}";</script>"""
            else:
                message = "Erreur lors de l'ajout de la demande de vente, erreur dans la route."
                return f"""<script>alert("{message}");window.location.href = "{url_for('ajouter_demande_vente')}";</script>"""

        except ValueError:
            # Handle invalid integer conversion
            message = "La quantité doit être un nombre entier."
            return f"""<script>alert("{message}");window.location.href = "{url_for('ajouter_demande_vente')}";</script>"""
        except Exception as e:
            # General error handling
            print(f"Unexpected error: {e}")
            message = "Erreur inattendue lors du traitement de la demande."
            return f"""<script>alert("{message}");window.location.href = "{url_for('ajouter_demande_vente')}";</script>"""

    # Render the form with available articles and usines data
    return render_template('ajouter_demande_vente.html', Articles_data=Articles_data, usines_data=usines_data)

# Function to add a sales request
def fun_ajouter_demande_vente(data):
    try:
        new_demande_vente = DemandeVente(
            code_article=data['code_article'],
            libelle_article=data['libelle_article'],
            quantite=data['quantite'],
            vers=data['vers'],
            assignation=data['assignation'],
            commande=data['commande'],
            etat=1,
            reception=1,
        )
        
        db.session.add(new_demande_vente)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de l'ajout de la demande de vente, erreur dans la fonction d'ajout de demande de vente : {e}")
        db.session.rollback()
        return False
@app.route('/rechercher_demande_vente', methods=['GET', 'POST'])
@roles_required('admin')
def rechercher_demande_vente():
        demandes_ventes=DemandeVente.query.all()
        if request.method == 'POST':
            code_demande = request.form.get("code_demande")
            demande_vente = DemandeVente.query.filter_by(code_demande=code_demande, etat=1, reception=1).first()
            if demande_vente:
                return render_template('confirmer_demande_vente.html', demande_vente=demande_vente,demandes_ventes=demandes_ventes)
            else:
                message = "Demande vente not found."

                # Return a JavaScript alert with the message and then redirect
                return f"""<script>alert("{message}");window.location.href = "{url_for('confirmer_demande_vente')}";</script>"""
  


@app.route('/confirmer_demande_vente', methods=['POST', 'GET'])
@roles_required('admin')
def confirmer_demande_vente():
    demandes_ventes = DemandeVente.query.filter_by(etat=1, reception=1).all()
    if request.method == 'POST':
        code_demande = request.form.get('code_demande')
        action = request.form.get('action')

        demande_vente = DemandeVente.query.filter_by(code_demande=code_demande).first()

        if action == 'confirmer' and demande_vente:
            # Confirmer la demande de vente
            demande_vente.prix_vente = float(request.form.get('prix_vente'))
            demande_vente.etat = 0  # Marquer comme confirmé
            demande_vente.reception = 1  # Réception marquée

            try:
                db.session.commit()
                flash("Demande de vente confirmée avec succès.", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Erreur lors de la confirmation de la demande de vente : {e}", "error")

            return redirect(url_for('confirmer_demande_vente'))

        elif action == 'delete' and demande_vente:
            demande_vente.etat = 2  # Marquer comme supprimé
            demande_vente.reception = 2
            try:
                db.session.commit()
                flash("Demande de vente supprimée avec succès.", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Erreur lors de la suppression de la demande de vente : {e}", "error")

            return redirect(url_for('confirmer_demande_vente'))

    return render_template('confirmer_demande_vente.html', demandes_ventes=demandes_ventes)

@app.route('/confirmer_expedition_vente', methods=['POST', 'GET'])
@roles_required('admin')
def confirmer_expedition_vente():
    demandes_ventes = DemandeVente.query.filter_by(etat=0, reception=1).all()  # Récupérer toutes les demandes d'achats pour l'affichage
    
    if request.method == 'POST':
        code_demande = request.form.get('code_demande')
        action = request.form.get('action')  # Récupérer l'action (ici, 'confirmer')
        
        # Trouver la demande d'achat correspondante
        demande_vente = DemandeVente.query.filter_by(code_demande=code_demande).first()
       
        if demande_vente and action == 'confirmer':
            if demande_vente.reception == 1:  # Vérifier si la réception est encore en attente
                # Mettre à jour les informations de la demande d'achat
                demande_vente.reception = 0  # Marquer comme reçu
                demande_vente.etat = 0  # Mettre l'état à confirmé (par exemple)
                
                nouvel_vente = ajouter_vente(
                    code_demande=demande_vente.code_demande,
                    code_article=demande_vente.code_article,
                    libelle_article=demande_vente.libelle_article,
                    quantite=demande_vente.quantite,
                    prix_vente=demande_vente.prix_vente,
                    vers=demande_vente.vers,
                   
                    
                )
                article=Article.query.filter_by(code_article=demande_vente.code_article).first()
                article.quantite=article.quantite-demande_vente.quantite
                db.session.commit()
                
                # Valider les données et committer les mises à jour
                try:
                    db.session.commit()
                    flash(f"Achat ajouté avec succès avec le lot {demande_vente.lot}", "success")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Erreur lors de la réception de l'achat: {e}", "error")
                return redirect(url_for('confirmer_reception_achat'))  # Rediriger vers la même page pour éviter le rechargement de la page

    # Afficher la page avec la liste des demandes d'achats
    return render_template('confirmer_expedition_vente.html', demandes_ventes=demandes_ventes)

def update_achat_vente_article(demande_vente):
    
    
    total_quantite_a_vendre = demande_vente.quantite
    code_article = demande_vente.code_article
    print(f"Début de l'expédition de la vente pour {code_article} avec une quantité demandée de {total_quantite_a_vendre}")

    # 2. Récupérer les achats non vendus pour le code_article en utilisant LIFO (dernier achat d'abord)
    achats = Achat.query.filter_by(code_article=code_article, vendue=0).order_by(Achat.date.desc()).all()

    # 3. Processus LIFO pour gérer la vente
    for achat in achats:
        if total_quantite_a_vendre == 0:
            break
        
        # Si la quantité restante de cet achat est supérieure à la quantité de vente restante
        if achat.quantite_restante is not None and achat.quantite_restante > 0:
            if achat.quantite_restante >= total_quantite_a_vendre:
                # On a assez de quantité restante dans cet achat pour cette vente
                achat.quantite_restante -= total_quantite_a_vendre
                achat.vendue = 1  # Marquer comme vendu
                total_quantite_a_vendre = 0  # Vente terminée
                print(f"Vente réalisée avec l'achat du lot {achat.lot}, quantités restantes mises à jour.")
            else:
                # Pas assez de quantité restante, vendre tout ce qu'on peut de cet achat et passer au suivant
                total_quantite_a_vendre -= achat.quantite_restante
                achat.quantite_restante = 0
                achat.vendue = 1
                print(f"Vente partielle réalisée avec l'achat du lot {achat.lot}, quantité restante épuisée.")
        else:
            # Si l'achat n'a plus de quantité restante, on passe au suivant
            continue
        
        db.session.commit()

    # 4. Mettre à jour la table article
    article = Article.query.filter_by(code_article=code_article).first()
    if article:
        article.quantite -= demande_vente.quantite
        db.session.commit()
        print(f"Quantité de l'article {code_article} mise à jour dans la table article.")

    # 5. Mettre à jour la table achats pour les achats utilisés (vendus)
    for achat in achats:
        if achat.vendue == 1:
            achat.vendue = 1
            db.session.commit()

    # 6. Vérification et mise à jour des achats avec `quantite_restante`
    for achat in achats:
        if achat.quantite_restante is not None and achat.quantite_restante > 0:
            achat.quantite_restante = achat.quantite_restante
            db.session.commit()
    
    print(f"Vente confirmée pour {total_quantite_a_vendre} articles du code {code_article}.")
    return total_quantite_a_vendre


def ajouter_vente(code_demande, code_article, libelle_article, quantite, prix_vente, vers):
    """Ajoute un nouvel achat dans la base de données avec un numéro de lot généré automatiquement."""
   
    new_vente = Vente(
       
        code_demande=code_demande,
        code_article=code_article,
        libelle_article=libelle_article,
        quantite=quantite,
        prix_vente=prix_vente,
        vers=vers,
        
    )
    print(new_vente)
    
    # Ajouter et committer la transaction dans la base de données
    db.session.add(new_vente)
    db.session.commit()
    return new_vente


def generer_lot_vente():
    """Génère un numéro de lot unique en fonction de l'année, du numéro de semaine et d'une séquence."""
    current_date = datetime.now(timezone.utc)
    year = current_date.strftime("%Y")
    week_number = numero_semaine(current_date)
    
    # Obtenir le dernier enregistrement d'achat de la même semaine et de la même année
    dernier_vente = Vente.query.filter(Vente.lot.like(f"{year}S{str(week_number).zfill(2)}%")).order_by(Vente.lot.desc()).first()

    if dernier_vente:
        # Extraire la dernière séquence de lot
        dernier_lot = dernier_vente.lot
        dernier_sequence = int(dernier_lot[7:])
        nouvelle_sequence = dernier_sequence + 1
    else:
        # Si aucun achat n'existe pour cette semaine, démarrer à 1
        nouvelle_sequence = 1
    
    # Générer le numéro de lot
    lot_number = f"{year}S{str(week_number).zfill(2)}{str(nouvelle_sequence).zfill(6)}"
    return lot_number



def fun_ajouter_user(data):
    try:
        # Hash the password
        password=data['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create a new user
        new_user = User(
            username=data['username'],
            password=hashed_password,
            emplacement=data['emplacement'],
            role=data['role'],
            numero_telephone=data['numero_telephone']
        )
        # Add and commit to the database
        db.session.add(new_user)
        db.session.commit()
        fun_history_ajouter_user(data)
        return True
    except Exception as e:
        print(f"Erreur lors de l'ajout de l'utilisateur : {e}")
        db.session.rollback()  # Roll back changes on error
        return False

def fun_ajouter_demande_achat(data):
    code_article=data['code_article']
    article=Article.query.filter_by(code_article=code_article).first()
   
    try:        
            # Create a new Article
            new_demande_achat = DemandeAchat(
                code_article=data['code_article'],
                libelle_article=data['libelle_article'],
                assignation=data['assignation'],
                quantite=data['quantite'],
                etat=1,
                date=datetime.now(timezone.utc),
                reception=1,
                
            )
            
            # Add and commit to the database
            db.session.add(new_demande_achat)
            db.session.commit()
            fun_history_ajouter_demande_achat(data)
            return True
        
    except Exception as e:
            print(f"Erreur lors de l'ajout de la demande d'achat: {e}")
            db.session.rollback()  # Roll back changes on error
            return False
        

def fun_ajouter_article(data):

    try:
       
        
        # Create a new Article
        new_article = Article(
            code_article=data['code_article'],
            libelle_article=data['libelle_article'],
            prix_achat=data['prix_achat'],
            assignation=data['assignation'],
            quantite=data['quantite'],
            fournisseur=data['fournisseur'],
            date=datetime.now(timezone.utc),
            quantite_min=data['quantite_min'],
            image=data['image']
        )

        # Add and commit to the database
        db.session.add(new_article)
        db.session.commit()
        fun_history_ajouter_article(data)
        return True
    except Exception as e:
        print(f"Erreur lors de l'ajout de l'article: {e}")
        db.session.rollback()  # Roll back changes on error
        return False

def fun_ajouter_usine(data):

    try:
       
        
        # Create a new Usine
        new_usine = Usine(
            nom_usine=data['nom_usine'],
            region=data['region'],
            adresse=data['adresse'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            telephone=data['telephone'],
            etat=data['etat']
        )

        # Add and commit to the database
        db.session.add(new_usine)
        db.session.commit()
        fun_history_ajouter_usine(data)
        return True
    except Exception as e:
        print(f"Erreur lors de l'ajout de l'usine: {e}")
        db.session.rollback()  # Roll back changes on error
        return False


def fun_ajouter_fournisseur(data):
    try:
        # Create a new Fournisseur
        new_fournisseur = Fournisseur(
            nom_fournisseur=data['nom_fournisseur'],
            matricule_fiscale=data['matricule_fiscale'],
            adresse=data['adresse'],
            telephone=data['telephone'],
        )
        # Add and commit to the database
        db.session.add(new_fournisseur)
        db.session.commit()
        fun_history_ajouter_fournisseur(data)
        return True
    except Exception as e:
        print(f"Erreur lors de l'ajout de fournisseur: {e}")
        db.session.rollback()  # Roll back changes on error
        return False

def fun_history_ajouter_fournisseur(data):
    
    new_history=History(
        fournisseur=data['nom_fournisseur'],
        action="ajout d'un nouveau fournisseur",
        details=str(' matricule fiscale : '+data['matricule_fiscale']+' addresse : '+data['adresse']+' telephone : '+data['telephone'])
        )
    db.session.add(new_history)
    db.session.commit()
    return True
    
def fun_history_ajouter_user(data):
    
    new_history=History(
        user=data['username'],
        action="ajout d'un nouveau user",
        details=str(' emplacement : '+data['emplacement']+' role : '+data['role']+' telephone : '+data['telephone'])
        )
    db.session.add(new_history)
    db.session.commit()
    return True
    
def fun_history_ajouter_article(data):
    
    new_history=History(
        code_article=data['code_article'],
        libelle_article=data['libelle_article'],
        emplacement=data['assignation'],
        prix=data['prix_achat'],
        action="ajout d'un nouveau article",
        fournisseur=data['fournisseur'],
        details=str('date : ' + str(datetime.now(timezone.utc)) + 'quantite_min : ' + data['quantite_min'])
        )
    db.session.add(new_history)
    db.session.commit()
    return True

def fun_history_ajouter_demande_achat(data):
    new_history=History(
        code_article=data['code_article'],
        libelle_article=data['libelle_article'],
        emplacement=data['assignation'],
        
        action="ajout d'un nouveau demande d'achat",
       
        details=str('date : ' + str(datetime.now(timezone.utc)))
        )
    db.session.add(new_history)
    db.session.commit()
    return True     


def fun_history_ajouter_usine(data):
    
    new_history=History(
        nom_usine=data['nom_usine'],
        emplacement=data['region'],
        action="ajout d'un nouveau usine",
        details=str('addresse : ' + data['telephone'] + 'etat : ' + data['etat']))
    db.session.add(new_history)
    db.session.commit()
    return True

def fun_history_editer_article(data):
    
    new_history=History(
        code_article=data['code_article'],
        libelle_article=data['libelle_article'],
        prix=data['prix_achat'],
        fournisseur=data['fournisseur'],
        action="editre un article")
    db.session.add(new_history)
    db.session.commit()
    return True
    
def fun_info_demande_achat(code_demande):
    demande_achat_data = DemandeAchat.query.filter_by(code_demande=code_demande)
    return demande_achat_data

def fun_info_article(id_article):
    article_data = Article.query.filter_by(id_article=id_article).first()
    return article_data

def fun_info_fournisseur(nom_fournisseur):
    fournisseur_data = Fournisseur.query.filter_by(nom_fournisseur=nom_fournisseur).first()
    return fournisseur_data
                
def fun_info_usine(nom_usine):
    usine_data = Usine.query.filter_by(nom_usine=nom_usine).first()
    return usine_data

def fun_info_user(username):
     user_data=User.query.filter_by(username=username).first()
     return user_data




@app.route('/achats', methods=['POST', 'GET'])
@roles_required('admin')
def achats():
    achats_data=Achat.query.all()
    return render_template('achats.html',achats_data=achats_data)
@app.route('/ventes', methods=['POST', 'GET'])
@roles_required('admin')
def ventes():
    ventes_data=Vente.query.all()
    return render_template('ventes.html',ventes_data=ventes_data)


# User Model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    emplacement = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    numero_telephone = db.Column(db.Integer, nullable=True)

# Article Model
class Article(db.Model):
    __tablename__ = 'articles'
    id_article = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code_article = db.Column(db.String(20), nullable=False)
    libelle_article = db.Column(db.String(255), nullable=False)
    prix_achat = db.Column(db.Float, nullable=False)
    assignation = db.Column(db.String(255), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    fournisseur = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    quantite_min = db.Column(db.Integer, nullable=False)
    image=db.Column(db.String(255),nullable=True)

# Supplier Model (Fournisseur)
class Fournisseur(db.Model):
    __tablename__ = 'fournisseur'
    id_fournisseur = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_fournisseur = db.Column(db.String(255), nullable=False)
    matricule_fiscale = db.Column(db.String(50), nullable=True)
    adresse = db.Column(db.String(255), nullable=True)
    telephone = db.Column(db.String(50), nullable=True)

# Purchase Model (Achats)
from datetime import datetime, timezone
from sqlalchemy import func, desc


class Achat(db.Model):
    __tablename__ = 'achats'
    
    lot = db.Column(db.String(255), primary_key=True)
    code_demande = db.Column(db.String(255), nullable=False)
    code_article = db.Column(db.Integer, nullable=False)
    libelle_article = db.Column(db.String(255), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix_achat = db.Column(db.Float, nullable=False)
    assignation = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    fournisseur = db.Column(db.String(255), nullable=False)
    vendue = db.Column(db.Integer, nullable=False, default=0)
    quantite_restante = db.Column(db.Integer, nullable=True, default=0) 
    
# Sales Model (Ventes)
class Vente(db.Model):
    __tablename__ = 'ventes'
    id_vente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code_demande = db.Column(db.Integer, nullable=True)
    code_article = db.Column(db.String(255), nullable=True)
    libelle_article = db.Column(db.String(20), nullable=True)
    quantite = db.Column(db.Integer, nullable=True)
    prix_vente = db.Column(Numeric(6, 3), nullable=True)
    assignation = db.Column(db.String(20), nullable=True)
    vers = db.Column(db.String(20), nullable=True)
    demandeur = db.Column(db.String(20), nullable=True)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

# Sales Request Model (DemandeVente)
class DemandeVente(db.Model):
    __tablename__ = 'demande_vente'
    code_demande = db.Column(db.Integer, primary_key=True)
    code_article = db.Column(db.String(50), nullable=False)
    libelle_article = db.Column(db.String(20), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix_vente = db.Column(Numeric(6, 3), nullable=True)
    assignation = db.Column(db.String(20), nullable=True)
    date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    demandeur = db.Column(db.String(20), nullable=True)
    vers = db.Column(db.String(20), nullable=False)
    commande = db.Column(db.String(20), nullable=True)
    etat = db.Column(db.Integer, nullable=False)
    reception = db.Column(db.Integer, nullable=False)
    commentaire = db.Column(db.String(255), nullable=True)

# Purchase Request Model (DemandeAchat)
class DemandeAchat(db.Model):
    __tablename__ = 'demande_achat'
    code_demande = db.Column(db.Integer, primary_key=True)
    code_article = db.Column(db.String(50), nullable=False)
    libelle_article = db.Column(db.String(20), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix_achat = db.Column(Numeric(6, 3), nullable=True)
    assignation = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    demandeur = db.Column(db.String(20), nullable=True)
    vers = db.Column(db.String(20), nullable=True)
    commande = db.Column(db.String(20), nullable=True)
    etat = db.Column(db.Integer, nullable=False)
    reception = db.Column(db.Integer, nullable=False)
    commentaire = db.Column(db.String(255), nullable=True)
    fournisseur = db.Column(db.String(255), nullable=True)

# History Model
class History(db.Model):
    __tablename__ = 'history'
    id_history = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code_demande = db.Column(db.Integer, nullable=True)
    code_article = db.Column(db.String(50), nullable=True)
    libelle_article = db.Column(db.String(255), nullable=True)
    quantite = db.Column(db.Integer, nullable=True)
    prix = db.Column(db.Float, nullable=True)
    fournisseur = db.Column(db.String(20), nullable=True)
    emplacement = db.Column(db.String(20), nullable=True)
    action = db.Column(db.String(50), nullable=True)
    user = db.Column(db.String(20), nullable=True)
    details = db.Column(db.String(255), nullable=True)
    usine = db.Column(db.String(20), nullable=True)
    date_action = db.Column(db.TIMESTAMP, nullable=True)
    date_approuver_demande = db.Column(db.TIMESTAMP, nullable=True)
    date_reception = db.Column(db.TIMESTAMP, nullable=True)

# Factory Model (Usine)
class Usine(db.Model):
    __tablename__ = 'usine'
    id_usine = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_usine = db.Column(db.String(20), nullable=False)
    region = db.Column(db.String(20), nullable=False)
    adresse = db.Column(db.String(20), nullable=True)
    latitude = db.Column(db.String(20), nullable=True)
    longitude = db.Column(db.String(20), nullable=True)
    telephone = db.Column(db.String(20), nullable=True)
    etat = db.Column(db.String(20), nullable=False)  
    


if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True)
