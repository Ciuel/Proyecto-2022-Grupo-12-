from src.core.board.associate import Associate
from src.core.board import associates
from src.web.helpers.form_utils import bool_checker, csrf_remover



def get_associate_by_id(id):
    """ Get associate by id
    Args:
        - id (integer): Associate number. Unique, autogenerated
    Returns:
        - Associate object
    """
    return associates.get(id)

def get_associate_by_DNI(DNI_number):
    """ Get associate by DNI
    Args:
        - DNI_number (integer): Associate DNI number
    Returns:
        - Associate object
    """
    return associates.query.filter(Associate.DNI_number == DNI_number).first()

def list_associates(column=None,filter=True):
    """ List all associates
    Returns:
        - List of Associate objects
    """
    if column:
        return associates.filter(column,filter)
    return associates.list()


def list_all_associates(column=None,filter=True):
    """List all associates
    Returns:
        - List all associates
    """
    if column:
        return associates.filter(column,filter,paginate=False)
    return associates.list(paginate=False)

def create_associate(form_data):
    """ Create associate
    Returns:
        - Create associate
    """
    associate = Associate(**form_data)
    associates.add(associate)
    return associate

def update_associate(form_data,id):
    """ Update associate
    Returns:
        - Update associate
    """
    associate_data = csrf_remover(form_data)
    associate_data.update(active=bool_checker(form_data["active"]))
    associates.update(id,associate_data)

def delete_associate(id):
    """Delete associate
    Returns:
        - Delete associate
    """
    associates.delete(id)
    
#agregar_disciplina_a_asociado
def add_discipline_to_associate(associate,discipline):
    """Add discipline to associate
    Returns:
        - Add discipline to associate
    """
    associate.disciplines.append(discipline)
    associates.add(associate)

#remove_discipline_to_associate
def remove_discipline_to_associate(associate,discipline):
    """Remove discipline to associate
    Returns:
        - Remove discipline to associate
    """
    associate.disciplines.remove(discipline)
    associates.add(associate)
    
