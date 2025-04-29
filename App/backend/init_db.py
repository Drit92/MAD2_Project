from application.data.models import db, Role

def create_roles():
    # Check if roles already exist, if so, return
    existing_roles = Role.query.all()
    if existing_roles:
        return
   
    # Define predefined roles
    roles_data = [
        {'name': 'admin', 'description': 'Administrator role'},
        {'name': 'user', 'description': 'Regular user role'},
        {'name': 'creator', 'description': 'Creator user role'},
        
        # Add more roles as needed
    ]

    # Create Role objects and add them to the session
    for role_data in roles_data:
        role = Role(**role_data)
        db.session.add(role)
   
    # Commit the changes to the database
    db.session.commit()

if __name__ == "__main__":
    from main import app
    with app.app_context():
        create_roles()