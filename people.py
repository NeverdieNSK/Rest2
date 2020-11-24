"""
This is the people module and supports all the ReST actions for the
PEOPLE collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Data to serve with our API
PEOPLE = {
    "Farrell": {
        "fname": "Doug",
        "person_id": "Farrell",
        "timestamp": get_timestamp(),
    },
    "Brockman": {
        "fname": "Kent",
        "person_id": "Brockman",
        "timestamp": get_timestamp(),
    },
    "Easter": {
        "fname": "Bunny",
        "person_id": "Easter",
        "timestamp": get_timestamp(),
    },
}


def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of people
    :return:        json string of list of people
    """
    # Create the list of people from our data
    return [PEOPLE[key] for key in sorted(PEOPLE.keys())]


def read_one(person_id):
    """
    This function responds to a request for /api/people/{person_id}
    with one matching person from people
    :param person_id:   last name of person to find
    :return:        person matching last name
    """
    # Does the person exist in people?
    if person_id in PEOPLE:
        person = PEOPLE.get(person_id)

    # otherwise, nope, not found
    else:
        abort(
            404, "Person with last name {person_id} not found".format(person_id=person_id)
        )

    return person


def create(person):
    """
    This function creates a new person in the people structure
    based on the passed in person data
    :param person:  person to create in people structure
    :return:        201 on success, 406 on person exists
    """
    person_id = person.get("person_id", None)
    fname = person.get("fname", None)

    # Does the person exist already?
    if person_id not in PEOPLE and person_id is not None:
        PEOPLE[person_id] = {
            "person_id": person_id,
            "fname": fname,
            "timestamp": get_timestamp(),
        }
        return make_response(
            "{person_id} successfully created".format(person_id=person_id), 201
        )

    # Otherwise, they exist, that's an error
    else:
        abort(
            406,
            "Person with last name {person_id} already exists".format(person_id=person_id),
        )


def update(person_id, person):
    """
    This function updates an existing person in the people structure
    :param person_id:   last name of person to update in the people structure
    :param person:  person to update
    :return:        updated person structure
    """
    # Does the person exist in people?
    if person_id in PEOPLE:
        PEOPLE[person_id]["fname"] = person.get("fname")
        PEOPLE[person_id]["timestamp"] = get_timestamp()

        return PEOPLE[person_id]

    # otherwise, nope, that's an error
    else:
        abort(
            404, "Person with last name {person_id} not found".format(person_id=person_id)
        )


def delete(person_id):
    """
    This function deletes a person from the people structure
    :param person_id:   last name of person to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Does the person to delete exist?
    if person_id in PEOPLE:
        del PEOPLE[person_id]
        return make_response(
            "{person_id} successfully deleted".format(person_id=person_id), 200
        )

    # Otherwise, nope, person to delete not found
    else:
        abort(
            404, "Person with last name {person_id} not found".format(person_id=person_id)
        )